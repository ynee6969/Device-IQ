"""Persist enrichment findings separately from the rebuildable research inventory."""
import argparse
import json
import sqlite3
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS runs (
  run_at TEXT PRIMARY KEY, inventory_count INTEGER NOT NULL,
  selected_count INTEGER NOT NULL, fetched_count INTEGER NOT NULL,
  extracted_count INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS model_queue (
  device_id TEXT PRIMARY KEY, brand TEXT NOT NULL, model_name TEXT NOT NULL,
  category TEXT NOT NULL, status TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fetch_attempts (
  run_at TEXT NOT NULL, device_id TEXT NOT NULL, source_url TEXT NOT NULL,
  status TEXT NOT NULL, http_status INTEGER, page_title TEXT,
  source_kind TEXT NOT NULL DEFAULT 'official',
  PRIMARY KEY (run_at, device_id, source_url)
);
CREATE TABLE IF NOT EXISTS source_candidates (
  device_id TEXT NOT NULL, source_url TEXT NOT NULL, status TEXT NOT NULL,
  first_seen_at TEXT NOT NULL, source_kind TEXT NOT NULL DEFAULT 'official',
  PRIMARY KEY (device_id, source_url)
);
CREATE TABLE IF NOT EXISTS spec_observations (
  device_id TEXT NOT NULL, spec_key TEXT NOT NULL, value_text TEXT NOT NULL,
  excerpt TEXT NOT NULL, source_url TEXT NOT NULL, observed_at TEXT NOT NULL,
  source_kind TEXT NOT NULL DEFAULT 'official',
  review_status TEXT NOT NULL DEFAULT 'pending',
  PRIMARY KEY (device_id, spec_key, value_text, source_url, observed_at)
);
CREATE TABLE IF NOT EXISTS price_snapshots (
  device_id TEXT NOT NULL, configuration_id TEXT, amount_php REAL NOT NULL,
  configuration_match TEXT NOT NULL, price_type TEXT NOT NULL,
  excerpt TEXT NOT NULL, source_url TEXT NOT NULL, observed_at TEXT NOT NULL,
  source_kind TEXT NOT NULL DEFAULT 'official',
  variant_ram_gb INTEGER, variant_storage_gb INTEGER, source_published_at TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending',
  PRIMARY KEY (device_id, amount_php, source_url, observed_at)
);
CREATE TABLE IF NOT EXISTS conflicts (
  device_id TEXT NOT NULL, spec_key TEXT NOT NULL, found_value TEXT NOT NULL,
  existing_values TEXT NOT NULL, source_url TEXT NOT NULL, observed_at TEXT NOT NULL,
  PRIMARY KEY (device_id, spec_key, found_value, source_url, observed_at)
);
"""


def existing_spec_values(tables):
    values = defaultdict(set)
    for item in tables['device_specifications']:
        if item['value_text']:
            values[(item['device_id'], item['spec_key'])].add(str(item['value_text']).strip().lower())
    mapping = {
        'battery_mah': 'battery_mah', 'ram_gb': 'ram_gb',
        'internal_storage_gb': 'internal_storage_gb',
        'display_inches': 'display_inches', 'chipset': 'chipset',
        'operating_system': 'operating_system',
    }
    for config in tables['device_configurations']:
        for key, field in mapping.items():
            if config.get(field) is not None:
                values[(config['device_id'], key)].add(str(config[field]).strip().lower())
    return values


def comparable(key, value):
    text = unicodedata.normalize('NFKD', str(value)).casefold()
    if key in {'battery_mah', 'ram_gb', 'internal_storage_gb', 'display_inches'}:
        try:
            return str(float(text.replace(',', '')))
        except ValueError:
            pass
    if key == 'operating_system':
        found = re.search(r'hyperos\s*\d*(?:\.\d+)?', text)
        if found:
            return re.sub(r'\s+', '', found.group())
    text = re.sub(r'\([^)]*\bnm\)', ' ', text)
    text = re.sub(r'\b(?:flagship|powered by|mobile platform|mediatek|qualcomm|for galaxy)\b', ' ', text)
    return re.sub(r'[^a-z0-9+]+', ' ', text).strip()


def equivalent(key, found, known):
    found_value = comparable(key, found)
    for existing in known:
        previous = comparable(key, existing)
        if found_value == previous:
            return True
        if key == 'operating_system' and (found_value.startswith(previous + ' ') or previous.startswith(found_value + ' ')):
            return True
    return False


def ensure_column(connection, table, column, definition):
    columns = {row[1] for row in connection.execute(f'PRAGMA table_info({table})')}
    if column not in columns:
        connection.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='research/enrichment/latest.json')
    parser.add_argument('--inventory', default='outputs/deviceiq-inventory-2026-11-24/deviceiq_inventory.json')
    parser.add_argument('--database', default='research/enrichment/state.sqlite')
    parser.add_argument('--report', default='research/enrichment/REVIEW.md')
    args = parser.parse_args()
    run = json.loads(Path(args.input).read_text(encoding='utf-8'))
    tables = json.loads(Path(args.inventory).read_text(encoding='utf-8'))['tables']
    prior = existing_spec_values(tables)
    missing_baseline = sum(not prior.get((item['device_id'], item['key'])) for item in run['observations'])
    db_path = Path(args.database)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.executescript(SCHEMA)
        for table in ('fetch_attempts', 'source_candidates', 'spec_observations', 'price_snapshots'):
            ensure_column(connection, table, 'source_kind', "TEXT NOT NULL DEFAULT 'official'")
        for column, definition in (('variant_ram_gb', 'INTEGER'), ('variant_storage_gb', 'INTEGER'), ('source_published_at', 'TEXT')):
            ensure_column(connection, 'price_snapshots', column, definition)
        connection.execute('DELETE FROM conflicts WHERE observed_at=?', (run['run_at'],))
        connection.execute('INSERT OR REPLACE INTO runs VALUES (?,?,?,?,?)', (
            run['run_at'], run['inventory_count'], run['selected_count'],
            len(run['fetches']), sum(x['status'] == 'extracted' for x in run['fetches'])))
        for model in run['models']:
            connection.execute('INSERT INTO model_queue VALUES (?,?,?,?,?,?) ON CONFLICT(device_id) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at',
                               (model['device_id'], model['brand'], model['model_name'], model['category'], model['status'], run['run_at']))
        for attempt in run['fetches']:
            connection.execute('INSERT OR REPLACE INTO fetch_attempts(run_at,device_id,source_url,status,http_status,page_title,source_kind) VALUES (?,?,?,?,?,?,?)',
                               (run['run_at'], attempt['device_id'], attempt['source_url'], attempt['status'], attempt.get('http_status'), attempt.get('page_title'), attempt.get('source_kind', 'official')))
        for source in run['discovery']:
            connection.execute('INSERT OR IGNORE INTO source_candidates(device_id,source_url,status,first_seen_at,source_kind) VALUES (?,?,?,?,?)',
                               (source['device_id'], source['source_url'], source['status'], run['run_at'], source.get('source_kind', 'official')))
        for spec in run['observations']:
            connection.execute('INSERT OR IGNORE INTO spec_observations(device_id,spec_key,value_text,excerpt,source_url,observed_at,source_kind) VALUES (?,?,?,?,?,?,?)',
                               (spec['device_id'], spec['key'], spec['value'], spec['excerpt'], spec['source_url'], spec['observed_at'], spec.get('source_kind', 'official')))
            known = prior.get((spec['device_id'], spec['key']), set())
            if known and spec['key'] not in {'ram_gb', 'internal_storage_gb'} and not equivalent(spec['key'], spec['value'], known):
                connection.execute('INSERT OR IGNORE INTO conflicts VALUES (?,?,?,?,?,?)',
                                   (spec['device_id'], spec['key'], spec['value'], ', '.join(sorted(known)), spec['source_url'], spec['observed_at']))
        observations_by_field = defaultdict(list)
        for spec in run['observations']:
            observations_by_field[(spec['device_id'], spec['key'])].append(spec)
        for (device_id, key), observations in observations_by_field.items():
            for observation in observations:
                other_values = {item['value'] for item in observations if item['source_url'] != observation['source_url'] and not equivalent(key, observation['value'], {item['value']})}
                if other_values:
                    connection.execute('INSERT OR IGNORE INTO conflicts VALUES (?,?,?,?,?,?)',
                                       (device_id, key, observation['value'], ', '.join(sorted(other_values)), observation['source_url'], observation['observed_at']))
        for price in run['prices']:
            connection.execute('INSERT OR IGNORE INTO price_snapshots(device_id,configuration_id,amount_php,configuration_match,price_type,excerpt,source_url,observed_at,source_kind,variant_ram_gb,variant_storage_gb,source_published_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                               (price['device_id'], price['configuration_id'], price['amount_php'], price['configuration_match'], price['price_type'], price['excerpt'], price['source_url'], price['observed_at'], price.get('source_kind', 'official'), price.get('variant_ram_gb'), price.get('variant_storage_gb'), price.get('source_published_at')))
        counts = Counter(x['status'] for x in run['fetches'])
        conflict_count = connection.execute('SELECT count(*) FROM conflicts WHERE observed_at=?', (run['run_at'],)).fetchone()[0]
        disputed_fields = connection.execute('SELECT count(*) FROM (SELECT DISTINCT device_id, spec_key FROM conflicts WHERE observed_at=?)', (run['run_at'],)).fetchone()[0]
    report = [
        '# DeviceIQ enrichment review', '',
        f"Run: **{run['run_at']}**", '',
        f"Queued device models (smartphones, tablets, and laptops): **{run['inventory_count']}**; processed: **{run['selected_count']}**.",
        f"Source fetches: **{len(run['fetches'])}**; extracted pages: **{counts['extracted']}**.",
        f"Specification observations: **{len(run['observations'])}** (**{missing_baseline}** fields absent from the baseline); dated price snapshots: **{len(run['prices'])}**; conflicting observations: **{conflict_count}** across **{disputed_fields}** model fields.",
        f"Sitemap/search source candidates: **{len(run['discovery'])}**.", '',
        'Findings are pending review. No release dates, Philippine availability flags, or public catalog records were changed.', '',
        '## Fetch outcomes', '',
        '| Status | Count |', '| --- | ---: |',
        *[f'| {status} | {count} |' for status, count in sorted(counts.items())], '',
        '## Next review', '',
        'Open `latest.json` for source URLs, excerpts, model matches, and observation times. Resolve conflicts and configuration matches before promoting values to the research inventory.', ''
    ]
    Path(args.report).write_text('\n'.join(report), encoding='utf-8')
    print('\n'.join(report[:8]))


if __name__ == '__main__':
    main()
