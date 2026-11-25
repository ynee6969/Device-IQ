import assert from 'node:assert/strict';
import { test } from 'node:test';
import { robotsAllowed, extractPage, gsmarenaReferenceUrl } from './enrich_devices.mjs';

test('GSMArena review candidates must match the exact model', () => {
  assert.equal(gsmarenaReferenceUrl('https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php', 'Galaxy S24 Ultra', 'Samsung'), true);
  assert.equal(gsmarenaReferenceUrl('https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php', 'Galaxy S24', 'Samsung'), false);
  assert.equal(gsmarenaReferenceUrl('https://www.gsmarena.com/news.php3?id=9', 'Galaxy S24', 'Samsung'), false);
  assert.equal(gsmarenaReferenceUrl('https://other.example/samsung_galaxy_s24-12773.php', 'Galaxy S24', 'Samsung'), false);
});

test('robots groups, longest rule, and disallow', () => {
  const body = 'User-agent: *\nDisallow: /private\nAllow: /private/public\n\nUser-agent: DeviceIQResearchBot\nDisallow: /hidden';
  assert.equal(robotsAllowed(body, '/hidden'), false);
  assert.equal(robotsAllowed(body, '/private'), true); // specific crawler group wins
  assert.equal(robotsAllowed('User-agent: *\nDisallow: /private\nAllow: /private/public', '/private/public'), true);
  assert.equal(robotsAllowed('User-agent: *\nDisallow: /private', '/private/item'), false);
  assert.equal(robotsAllowed('User-agent: *\nDisallow: /private$', '/private'), false);
  assert.equal(robotsAllowed('User-agent: *\nDisallow: /private$', '/private/item'), true);
});

test('extracts unambiguous source fields and exact configured PHP offer', () => {
  const html = `<title>Galaxy S26 Ultra | Samsung Philippines</title><h1>Galaxy S26 Ultra</h1>
    <table><tr><th>Battery capacity</th><td>5,000 mAh</td></tr></table>
    <script type="application/ld+json">{"@type":"Product","name":"Galaxy S26 Ultra","offers":{"priceCurrency":"PHP","price":"79990","name":"12 GB / 256 GB"}}</script>`;
  const result = extractPage(html, { model_name: 'Galaxy S26 Ultra' }, [{ configuration_id: 'c1', ram_gb: 12, internal_storage_gb: 256 }]);
  assert.equal(result.status, 'extracted');
  assert.deepEqual(result.specs.map(x => [x.key, x.value]), [['battery_mah', '5000']]);
  assert.equal(result.prices[0].configuration_id, 'c1');
  assert.equal(result.prices[0].amount_php, 79990);
});

test('rejects a different variant and non PHP price', () => {
  const variant = extractPage('<title>Galaxy S26 Ultra</title><h1>Galaxy S26 Ultra</h1><table><tr><th>Battery</th><td>5000 mAh</td></tr></table>', { model_name: 'Galaxy S26' });
  assert.equal(variant.status, 'model_mismatch');
  const currency = extractPage('<title>Galaxy S26 Ultra</title><h1>Galaxy S26 Ultra</h1><script type="application/ld+json">{"@type":"Product","name":"Galaxy S26 Ultra","offers":{"priceCurrency":"USD","price":"999"}}</script>', { model_name: 'Galaxy S26 Ultra' });
  assert.equal(currency.prices.length, 0);
});

test('omits conflicting values on one page', () => {
  const html = '<title>Pad X</title><h1>Pad X</h1><table><tr><th>Battery</th><td>5000 mAh</td></tr><tr><th>Battery</th><td>6000 mAh</td></tr></table>';
  assert.equal(extractPage(html, { model_name: 'Pad X' }).specs.length, 0);
});

test('extracts paired specification blocks without choosing a storage variant', () => {
  const html = `<title>Redmi Note 14 Specs</title><h1>Redmi Note 14</h1>
    <div><div><span class="f-bold">Processor</span></div><div><span>Helio G99-Ultra</span><span>6nm</span></div></div>
    <div><div><span class="f-bold">Battery & Charging</span></div><div><span>5500mAh(typ) battery</span><span>33W charger</span></div></div>
    <div><div><span class="f-bold">Storage & RAM</span></div><div><span>6GB+128GB | 8GB+256GB</span></div></div>`;
  const fields = extractPage(html, { model_name: 'Redmi Note 14' }).specs;
  assert.deepEqual(fields.map(x => [x.key, x.value]), [['chipset', 'Helio G99-Ultra'], ['battery_mah', '5500']]);
});

test('keeps independent Philippine prices attributed to exact variants', () => {
  const html = `<title>SAMSUNG Galaxy A56 5G – Full Specs and Official Price in the Philippines</title>
    <h1>SAMSUNG Galaxy A56 5G – Full Specs and Official Price in the Philippines</h1>
    <div class="post-details">By Daniel Gubalane on Mar 05, 2025</div>
    <table><tr><td>Chipset</td><td>Exynos 1580 (4 nm)</td></tr>
    <tr><td>Price</td><td>₱23,990.00 Official price of 8GB+128GB variant₱25,990.00 Official price of 8GB+256GB variant</td></tr></table>`;
  const configurations = [{ configuration_id: 'a', ram_gb: 8, internal_storage_gb: 128 }, { configuration_id: 'b', ram_gb: 8, internal_storage_gb: 256 }];
  const result = extractPage(html, { model_name: 'Galaxy A56 5G' }, configurations, 'independent_ph_reference');
  assert.equal(result.specs[0].value, 'Exynos 1580 (4 nm)');
  assert.deepEqual(result.prices.map(x => [x.amount_php, x.configuration_id, x.price_type]), [[23990, 'a', 'independent_reported_official_price'], [25990, 'b', 'independent_reported_official_price']]);
  assert.deepEqual(result.prices.map(x => [x.variant_ram_gb, x.variant_storage_gb]), [[8, 128], [8, 256]]);
  assert.equal(result.prices[0].source_published_at, '2025-03-05');
});

test('records a single tablet price without inventing a configuration', () => {
  const html = '<title>realme Pad X – Full Specs and Official Price in the Philippines</title><h1>realme Pad X</h1><table><tr><td>Battery</td><td>8340mAh Li-Po Battery</td></tr><tr><td>Price</td><td>₱15,999.00 - Official Price in the Philippines</td></tr></table>';
  const result = extractPage(html, { model_name: 'realme Pad X' }, [], 'independent_ph_reference');
  assert.equal(result.specs[0].value, '8340');
  assert.equal(result.prices[0].amount_php, 15999);
  assert.equal(result.prices[0].configuration_match, 'unspecified');
});
