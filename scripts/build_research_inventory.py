"""Build the reproducible DeviceIQ research database and exports.

Run from the repository root: python scripts/build_research_inventory.py
The supplied notes remain immutable in research/source_notes. No live app database is touched.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "deviceiq-inventory-2026-11-24"
SOURCE_DIR = ROOT / "research" / "source_notes"
AS_OF = "2026-11-24"
HISTORICAL_START = "2021-01-01"
ROLLING_START = "2021-11-24"
CUTOFF = "2026-11-24"

TABLES = [
    "manufacturers", "brands", "device_categories", "device_models",
    "device_configurations", "device_specifications", "philippines_market_releases",
    "data_sources", "device_source_evidence", "raw_research_claims",
    "research_queue", "excluded_records", "audit_log", "scope_settings",
]

MANUFACTURERS = {
    "Apple": ("Apple Inc.", "https://www.apple.com/ph/", "United States"),
    "Samsung": ("Samsung Electronics Co., Ltd.", "https://www.samsung.com/ph/", "South Korea"),
    "Xiaomi": ("Xiaomi Corporation", "https://www.mi.com/ph/", "China"),
    "Redmi": ("Xiaomi Corporation", "https://www.mi.com/ph/", "China"),
    "POCO": ("Xiaomi Corporation", "https://www.mi.com/ph/", "China"),
    "Acer": ("Acer Incorporated", "https://www.acer.com/ph-en/", "Taiwan"),
    "ASUS": ("ASUSTeK Computer Inc.", "https://www.asus.com/ph/", "Taiwan"),
}

ALIASES = {
    "poco": "POCO", "redmi": "Redmi", "xiaomi": "Xiaomi",
    "samsung": "Samsung", "apple": "Apple", "acer": "Acer", "asus": "ASUS",
    "redmagic": "REDMAGIC", "red magic": "REDMAGIC", "nubia / redmagic": "REDMAGIC",
    "nubia / zte": "nubia", "cherry": "CHERRY", "cherry mobile": "Cherry Mobile",
    "techlife": "TechLife", "tecno": "TECNO", "tcl": "TCL", "zte": "ZTE",
}

LAPTOP_DISCOVERY = ["Acer", "ASUS", "Dell", "HP", "Lenovo", "MSI", "Apple", "Microsoft", "Huawei", "Samsung", "Gigabyte", "Razer", "LG", "CHUWI", "Infinix", "TECNO"]

SPEC_UNITS = {
    "ramGb": "GB", "storageGb": "GB", "displayInches": "in", "refreshHz": "Hz",
    "rearCameraMp": "MP", "frontCameraMp": "MP", "batteryMah": "mAh",
    "batteryWh": "Wh", "chargingW": "W", "weightG": "g",
}


def stable_id(prefix: str, *parts: object) -> str:
    text = "|".join(str(part or "") for part in parts).casefold()
    return f"{prefix}_{hashlib.sha1(text.encode('utf-8')).hexdigest()[:14]}"


def canonical_brand(raw: str) -> str:
    return ALIASES.get(raw.strip().casefold(), raw.strip())


def brand_for_example(raw_brand: str, example: str) -> str:
    token = example.strip().casefold()
    if raw_brand.casefold() == "xiaomi" and token.startswith("redmi "):
        return "Redmi"
    if raw_brand.casefold() == "nubia / redmagic":
        return "REDMAGIC"
    return canonical_brand(raw_brand)


def model_without_brand(brand: str, model: str) -> str:
    model = model.strip()
    if model.casefold().startswith(brand.casefold() + " "):
        return model[len(brand):].strip()
    return model


def model_key(category: str, brand: str, model: str) -> tuple[str, str, str]:
    simple = model_without_brand(brand, model)
    # A plus sign is part of many marketed model names (S21+ versus S21).
    simple = re.sub(r"[^a-z0-9]+", "", simple.casefold().replace("+", "plus"))
    return category, brand.casefold(), simple


def split_examples(text: str) -> list[str]:
    parts, current, depth = [], [], 0
    for character in text:
        if character == "(":
            depth += 1
        elif character == ")":
            depth = max(0, depth - 1)
        if character == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    parts.append("".join(current).strip())
    return [part for part in parts if part]


def read_research_notes() -> tuple[list[dict], list[dict]]:
    raw_lines: list[dict] = []
    structured: list[dict] = []
    for filename in ["annual_brand_examples_2021_2026.txt", "philippine_2026_research_notes.txt"]:
        lines = (SOURCE_DIR / filename).read_text(encoding="utf-8-sig").splitlines()
        year, category = None, None
        for number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            heading = re.search(r"(Smartphone|Tablet) brands?\s*[—–-]\s*(20\d{2}) Philippine releases", line, re.I)
            if heading:
                category = "smartphones" if heading.group(1).lower().startswith("smart") else "tablets"
                year = int(heading.group(2))
            row = {"claim_id": stable_id("claim", filename, number), "source_file": filename, "source_line": number,
                   "raw_text": line, "research_year": year, "original_brand_name": None, "original_model_text": None,
                   "original_category": category, "original_release_claim": None,
                   "original_source_reference": None, "normalized_brand_id": None, "normalized_device_id": None,
                   "processing_status": "CONTEXT_ONLY", "verification_status": "PENDING_VERIFICATION",
                   "duplicate_of": None, "reviewer_notes": None}
            if filename.startswith("annual_"):
                match = re.fullmatch(r"\s*\d+\t([^\t]+)\t(.+)", line)
                if match and year and category:
                    row.update({"original_brand_name": match.group(1).strip(), "original_model_text": match.group(2).strip(),
                                "original_release_claim": f"Claimed {year} Philippine release",
                                "original_source_reference": "Annual research note; cited tracker URL not supplied",
                                "processing_status": "TABLE_ROW"})
                    structured.append(row)
            raw_lines.append(row)

        if filename.startswith("philippine_"):
            lookup = {row["source_line"]: row for row in raw_lines if row["source_file"] == filename}
            nonempty = [(i + 1, line.strip()) for i, line in enumerate(lines) if line.strip()]
            active_category = None
            for index, (line_no, text) in enumerate(nonempty):
                heading = re.search(r"(Smartphone|Tablet) brands?\s*[—–-]\s*2026 Philippine releases", text, re.I)
                if heading:
                    active_category = "smartphones" if heading.group(1).lower().startswith("smart") else "tablets"
                if text.startswith("Additional Philippine-market confirmations"):
                    active_category = None
                if active_category and text.isdigit() and index + 2 < len(nonempty):
                    brand, example = nonempty[index + 1][1], nonempty[index + 2][1]
                    if brand in {"Brand", "No."} or example in {"Brand", "No."}:
                        continue
                    if int(text) <= (17 if active_category == "smartphones" else 16):
                        row = lookup[nonempty[index + 2][0]]
                        row.update({"research_year": 2026, "original_category": active_category,
                                    "original_brand_name": brand, "original_model_text": example,
                                    "original_release_claim": "Claimed 2026 Philippine release",
                                    "original_source_reference": "2026 research note; cited publication labels are not direct URLs",
                                    "processing_status": "TABLE_ROW"})
                        structured.append(row)
    return raw_lines, structured


def catalog_seed() -> list[dict]:
    executable = "npx.cmd" if sys.platform == "win32" else "npx"
    run = subprocess.run([executable, "tsx", "scripts/export_catalog_research_seed.ts"], cwd=ROOT,
                         text=True, capture_output=True, check=True)
    return json.loads(run.stdout)


def open_database() -> sqlite3.Connection:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    database = OUTPUT / "deviceiq_philippine_inventory.sqlite"
    if database.exists():
        database.unlink()
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript((ROOT / "research" / "schema.sql").read_text(encoding="utf-8"))
    for category, label, description in [
        ("smartphones", "Smartphone", "Mobile handsets, including foldable and gaming phones"),
        ("tablets", "Tablet", "Tablet computers and detachable tablet-first devices"),
        ("laptops", "Laptop", "Portable computers including gaming, convertible and Chromebook forms"),
    ]:
        connection.execute("INSERT INTO device_categories VALUES (?,?,?)", (category, label, description))
    for key, value, description in [
        ("historical_start", HISTORICAL_START, "Start of retained calendar-year research history"),
        ("rolling_start", ROLLING_START, "Current provisional rolling five-year start"),
        ("research_cutoff", CUTOFF, "Last date researched in this snapshot"),
        ("prior_panel_start", "2021-01-01", "Earlier approved website study start"),
        ("prior_panel_planned_end", "2026-11-30", "Earlier planned cutoff; later than this snapshot"),
    ]:
        connection.execute("INSERT INTO scope_settings VALUES (?,?,?)", (key, value, description))
    return connection


def ensure_brand(db: sqlite3.Connection, raw: str) -> str:
    name = canonical_brand(raw)
    brand_id = stable_id("brand", name)
    mapping = MANUFACTURERS.get(name)
    manufacturer_id = None
    if mapping:
        manufacturer_id = stable_id("manufacturer", mapping[0])
        db.execute("INSERT OR IGNORE INTO manufacturers VALUES (?,?,?,?,?,?,?,?)",
                   (manufacturer_id, mapping[0], mapping[1], mapping[2], None, "VERIFIED_FROM_OFFICIAL_SITE", AS_OF, AS_OF))
    db.execute("INSERT OR IGNORE INTO brands VALUES (?,?,?,?,?,?,?,?,?)",
               (brand_id, name, name, manufacturer_id, mapping[1] if mapping else None,
                raw if name.casefold() != raw.casefold() else None,
                "VERIFIED_IN_PROJECT" if mapping else "PENDING_CORPORATE_REVIEW", AS_OF, AS_OF))
    return brand_id


def ensure_source(db: sqlite3.Connection, title: str, publisher: str, url: str, source_type: str,
                  publication_date: str | None = None, note: str | None = None) -> str:
    source_id = stable_id("source", url)
    db.execute("INSERT OR IGNORE INTO data_sources VALUES (?,?,?,?,?,?,?,?,?)",
               (source_id, title, publisher, url, source_type, publication_date, AS_OF, "Official Philippine source", note))
    return source_id


def ensure_model(db: sqlite3.Connection, category: str, brand: str, model: str, status: str = "PENDING_VERIFICATION") -> str:
    brand_id = ensure_brand(db, brand)
    clean = model_without_brand(brand, model)
    device_id = stable_id("device", *model_key(category, brand, clean))
    manufacturer_id = db.execute("SELECT manufacturer_id FROM brands WHERE brand_id=?", (brand_id,)).fetchone()[0]
    db.execute("INSERT OR IGNORE INTO device_models VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
               (device_id, manufacturer_id, brand_id, category, clean, None, None, None, None,
                None, None, None, None, status, 1, None, AS_OF, AS_OF))
    return device_id


def ensure_release(db: sqlite3.Connection, device_id: str, claimed_year: int | None = None) -> str:
    release_id = stable_id("release", device_id)
    db.execute("INSERT OR IGNORE INTO philippines_market_releases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
               (release_id, device_id, None, "unknown", None, None, None, "Not verified", "Not verified",
                None, None, CUTOFF, "Pending", None, "PENDING_VERIFICATION", claimed_year, None,
                "Preliminary research claim only; no linked Philippine source supplied.", AS_OF, AS_OF))
    return release_id


def add_raw_and_candidates(db: sqlite3.Connection, raw_lines: list[dict], structured: list[dict]) -> None:
    seen_claims: dict[tuple, str] = {}
    structured_ids = {row["claim_id"] for row in structured}
    for row in raw_lines:
        if row["claim_id"] in structured_ids:
            brand = canonical_brand(row["original_brand_name"])
            row["normalized_brand_id"] = ensure_brand(db, brand)
            key = (row["research_year"], row["original_category"], brand.casefold(),
                   row["original_model_text"].casefold())
            if key in seen_claims:
                row["duplicate_of"] = seen_claims[key]
                row["processing_status"] = "DUPLICATE_CLAIM"
            else:
                seen_claims[key] = row["claim_id"]
        db.execute("INSERT INTO raw_research_claims VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   tuple(row[key] for key in ["claim_id", "source_file", "source_line", "raw_text", "research_year",
                                             "original_brand_name", "original_model_text", "original_category",
                                             "original_release_claim", "original_source_reference", "normalized_brand_id",
                                             "normalized_device_id", "processing_status", "verification_status", "duplicate_of"])
                   + (row["reviewer_notes"],))

    for row in structured:
        if row["duplicate_of"]:
            continue
        for example in split_examples(row["original_model_text"]):
            brand = brand_for_example(row["original_brand_name"], example)
            category = row["original_category"]
            year = row["research_year"]
            is_series = bool(re.search(r"\bseries\b|\band\b", example, re.I))
            if is_series:
                db.execute("INSERT OR IGNORE INTO research_queue VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (stable_id("queue", row["claim_id"], example), row["claim_id"], None, example,
                            brand, category, year, "Individual base models and Philippine source URLs",
                            "Supplied label is a series or combined models", "Identify each base model and verify local release",
                            "High", "Open", None))
                continue
            device_id = ensure_model(db, category, brand, example)
            ensure_release(db, device_id, year)
            db.execute("INSERT OR IGNORE INTO research_queue VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (stable_id("queue", row["claim_id"], example), row["claim_id"], device_id, example,
                        brand, category, year, "Philippine source URL, local date, exact model name and specifications",
                        "Preliminary example only", "Verify against a manufacturer or authorized Philippine source",
                        "High" if year == 2026 else "Normal", "Open", None))


def add_specifications(db: sqlite3.Connection, device_id: str, configuration_id: str | None,
                       specs: dict, source_id: str) -> None:
    for key, value in specs.items():
        if value is None:
            continue
        db.execute("INSERT OR REPLACE INTO device_specifications VALUES (?,?,?,?,?,?,?,?)",
                   (stable_id("spec", device_id, configuration_id, key), device_id, configuration_id,
                    key, str(value), float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None,
                    SPEC_UNITS.get(key), source_id))


def verify_model(db: sqlite3.Connection, device_id: str, source_id: str, verification: str,
                 evidence: str, local_date: str | None, local_year: int | None,
                 observed_at: str | None, official_launch: str, availability_status: str) -> None:
    prior = db.execute("SELECT device_status FROM device_models WHERE device_id=?", (device_id,)).fetchone()[0]
    db.execute("UPDATE device_models SET canonical_model_name=model_name, device_status=?, updated_at=? WHERE device_id=?",
               (verification, AS_OF, device_id))
    if local_date:
        local_year = int(local_date[:4])
    if local_date and not HISTORICAL_START <= local_date <= CUTOFF:
        inclusion = "Outside historical cutoff"
    elif local_date:
        inclusion = "Included" if local_date >= ROLLING_START else "Outside rolling window"
    elif local_year and local_year >= 2022:
        inclusion = "Included"
    elif local_year == 2021 and observed_at and observed_at < ROLLING_START:
        inclusion = "Outside rolling window"
    else:
        inclusion = "Pending date"
    release_id = ensure_release(db, device_id)
    db.execute("""UPDATE philippines_market_releases SET philippine_release_date=?, release_date_precision=?,
               philippine_release_year=?, availability_date=?, availability_observed_at=?, availability_status=?,
               official_launch_status=?, market_availability_evidence=?, inclusion_status=?, verification_status=?,
               primary_source_id=?, reviewer_notes=?, updated_at=? WHERE device_id=?""",
               (local_date, "day" if local_date else "year" if local_year else "unknown", local_year,
                local_date if availability_status == "Available" and local_date else None,
                observed_at, availability_status, official_launch, evidence, inclusion, verification,
                source_id, "First local sale date not established" if not local_date else None, AS_OF, device_id))
    db.execute("INSERT OR REPLACE INTO device_source_evidence VALUES (?,?,?,?,?,?,?,?,?,?,?)",
               (stable_id("evidence", device_id, source_id, "PH release"), device_id, release_id, source_id,
                "Philippine release or availability", "Local launch or authorized availability",
                evidence, "Supports local-market presence", "High", None, AS_OF))
    if prior == "PENDING_VERIFICATION":
        db.execute("INSERT OR IGNORE INTO audit_log VALUES (?,?,?,?,?,?,?,?)",
                   (stable_id("audit", device_id, source_id), "device_models", device_id, "VERIFY",
                    prior, verification, "Linked official Philippine source reviewed", AS_OF))
    db.execute("UPDATE research_queue SET current_status='Resolved', reviewer_notes='Official Philippine source linked' WHERE device_id=? AND verification_issue='Preliminary example only'", (device_id,))
    if inclusion == "Outside rolling window":
        db.execute("INSERT OR IGNORE INTO excluded_records VALUES (?,?,?,?,?,?,?,?,?)",
                   (stable_id("exclude", device_id), None, evidence, db.execute("SELECT model_name FROM device_models WHERE device_id=?", (device_id,)).fetchone()[0],
                    db.execute("SELECT brand_name FROM brands WHERE brand_id=(SELECT brand_id FROM device_models WHERE device_id=?)", (device_id,)).fetchone()[0],
                    db.execute("SELECT category_id FROM device_models WHERE device_id=?", (device_id,)).fetchone()[0],
                    "Documented local availability before the rolling window", source_id, AS_OF))


def add_existing_catalog(db: sqlite3.Connection, catalog: list[dict]) -> None:
    for item in catalog:
        category, brand, name = item["category"], canonical_brand(item["brand"]), item["model"]
        device_id = ensure_model(db, category, brand, name)
        source = item["sources"][0]
        source_id = ensure_source(db, source["url"], source["organization"], source["url"],
                                  "Official Philippine product or store page")
        local_date = item.get("philippineAvailabilityDate")
        verification = "VERIFIED_OFFICIAL_LAUNCH" if local_date else "VERIFIED_AUTHORIZED_AVAILABILITY"
        verify_model(db, device_id, source_id, verification, item["philippineAvailability"],
                     local_date, int(local_date[:4]) if local_date else None,
                     source.get("observedAt"), "Official dated availability" if local_date else "Official product listing observed",
                     "Announced" if local_date else "Listed")
        for variant in item["variants"]:
            specs = variant["specs"]
            configuration_id = stable_id("config", device_id, variant["label"])
            db.execute("""INSERT OR IGNORE INTO device_configurations VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (configuration_id, device_id, variant["label"],
                 variant["label"] if category == "laptops" else None, None,
                 specs.get("cpu") or specs.get("chipset"), specs.get("chipset"), specs.get("cpu"), specs.get("gpu"),
                 specs.get("ramGb"), specs.get("storageGb"), specs.get("displayInches"), specs.get("resolution"),
                 specs.get("displayType"), specs.get("refreshHz"), specs.get("batteryMah"), specs.get("batteryWh"),
                 specs.get("chargingW"), specs.get("rearCameraMp"), specs.get("frontCameraMp"), specs.get("os"),
                 specs.get("wifi") or specs.get("cellular"), specs.get("weightG"), specs.get("dimensions"),
                 variant.get("pricePhp"), variant.get("priceCondition"), variant.get("priceObservedAt"),
                 source_id if variant.get("pricePhp") is not None else None, variant.get("notes"), AS_OF, AS_OF))
            add_specifications(db, device_id, configuration_id, specs, source_id)
            db.execute("INSERT OR IGNORE INTO device_source_evidence VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                       (stable_id("evidence", device_id, source_id, "specifications"), device_id,
                        stable_id("release", device_id), source_id, "Specifications", "Variant specifications",
                        "Specification fields recorded on the linked product or store page",
                        "Source linked", "High", None, AS_OF))


def add_researched_models(db: sqlite3.Connection) -> None:
    groups = json.loads((ROOT / "research" / "verified_additions.json").read_text(encoding="utf-8"))
    for group in groups:
        source_id = ensure_source(db, group["sourceTitle"], group.get("publisher", "Samsung Newsroom Philippines"),
                                  group["sourceUrl"], "Official Philippine newsroom", group["publishedAt"])
        for model in group["models"]:
            category = model["category"]
            device_id = ensure_model(db, category, model.get("brand", group.get("brand", "Samsung")), model["name"])
            local_date = group.get("philippineLaunchDate")
            year = group.get("philippineYear")
            verify_model(db, device_id, source_id, group["verificationStatus"], group["evidence"],
                         local_date, year, group.get("observedAt", group["publishedAt"]),
                         "Official local launch" if local_date else "Local presence by source date",
                         group.get("availabilityStatus", "Announced" if local_date else "Available"))
            specs = model.get("specs", {})
            configurations = model.get("configurations", [])
            if model.get("storageGb") and not configurations:
                configurations = [{"label": f"{model['storageGb']} GB storage; RAM not verified",
                                   "specs": {"storageGb": model["storageGb"]}}]
            for config in configurations:
                config_specs = config.get("specs", {})
                label = config["label"]
                configuration_id = stable_id("config", device_id, label)
                db.execute("""INSERT OR IGNORE INTO device_configurations VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (configuration_id, device_id, label, config.get("sku"), config.get("modelCode"),
                     config_specs.get("cpu") or config_specs.get("chipset"), config_specs.get("chipset"),
                     config_specs.get("cpu"), config_specs.get("gpu"), config_specs.get("ramGb"),
                     config_specs.get("storageGb"), config_specs.get("displayInches"), config_specs.get("resolution"),
                     config_specs.get("displayType"), config_specs.get("refreshHz"), config_specs.get("batteryMah"),
                     config_specs.get("batteryWh"), config_specs.get("chargingW"), config_specs.get("rearCameraMp"),
                     config_specs.get("frontCameraMp"), config_specs.get("os"), config_specs.get("connectivity"),
                     config_specs.get("weightG"), config_specs.get("dimensions"), config.get("pricePhp"),
                     config.get("priceCondition"), config.get("priceObservedAt"),
                     source_id if config.get("pricePhp") is not None else None,
                     config.get("notes", "Only source-backed fields recorded; other variants may exist."), AS_OF, AS_OF))
                add_specifications(db, device_id, configuration_id, config_specs, source_id)
            add_specifications(db, device_id, None, specs, source_id)


def add_laptop_research_queue(db: sqlite3.Connection) -> None:
    for brand in LAPTOP_DISCOVERY:
        ensure_brand(db, brand)
        for year in range(2021, 2027):
            db.execute("INSERT OR IGNORE INTO research_queue VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (stable_id("queue", "laptop-discovery", brand, year), None, None,
                        f"{brand} laptop models, {year}", brand, "laptops", year,
                        "Model-level official Philippine release list",
                        "No annual laptop inventory supplied for this brand",
                        "Search manufacturer and authorized Philippine archives; record each exact model and SKU",
                        "High", "Open", "Discovery task, not a device record"))


def add_explicit_holdouts(db: sqlite3.Connection) -> None:
    """Preserve the supplied 2026 note's explicit non-inclusion cases."""
    filename = "philippine_2026_research_notes.txt"
    lines = (SOURCE_DIR / filename).read_text(encoding="utf-8-sig").splitlines()
    holdouts = [
        ("ASUS Pad", "ASUS", "tablets", "International announcement only; Philippine retail release unestablished"),
        ("Acer Iconia Duo", "Acer", "tablets", "Unveiled internationally; Philippine release unconfirmed"),
        ("vivo Pad6 Pro", "vivo", "tablets", "Philippine release unconfirmed"),
        ("REDMAGIC 12 Pro+", "REDMAGIC", "smartphones", "China unveiling only; Philippine availability unannounced"),
        ("Xiaomi 18 Pro series", "Xiaomi", "smartphones", "Local launch described as scheduled after the 2026-11-24 cutoff"),
        ("Samsung Galaxy A18", "Samsung", "smartphones", "Local availability described as scheduled after the 2026-11-24 cutoff"),
        ("OPPO Reno17 series", "OPPO", "smartphones", "China announcement only; Philippine release unconfirmed"),
    ]
    for name, brand, category, reason in holdouts:
        line_no = next((i for i, line in enumerate(lines, 1) if line.strip() == name), None)
        if line_no is None:
            raise ValueError(f"Explicit holdout not found in original note: {name}")
        claim_id = stable_id("claim", filename, line_no)
        db.execute("INSERT OR IGNORE INTO excluded_records VALUES (?,?,?,?,?,?,?,?,?)",
                   (stable_id("exclude", "note-holdout", name), claim_id, name, name, brand, category,
                    f"Hold out: {reason}", f"Supplied 2026 research note, line {line_no}; direct local source still needed", AS_OF))
        db.execute("INSERT OR IGNORE INTO research_queue VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (stable_id("queue", "note-holdout", name), claim_id, None, name, brand, category, 2026,
                    "Direct official Philippine release or availability evidence", reason,
                    "Reassess after the cutoff using a dated Philippine source; do not count in this snapshot",
                    "High", "Open", "Explicitly held out in supplied 2026 note"))


def add_missing_date_queue(db: sqlite3.Connection) -> None:
    rows = db.execute("""SELECT m.device_id, m.model_name, m.category_id, b.brand_name, r.philippine_release_year,
                             r.philippine_release_date, r.verification_status, r.inclusion_status
                             FROM device_models m JOIN brands b ON m.brand_id=b.brand_id
                             JOIN philippines_market_releases r ON m.device_id=r.device_id
                             WHERE r.verification_status != 'PENDING_VERIFICATION' AND r.philippine_release_date IS NULL""").fetchall()
    for row in rows:
        db.execute("INSERT OR IGNORE INTO research_queue VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (stable_id("queue", "missing-date", row["device_id"]), None, row["device_id"],
                    f"{row['brand_name']} {row['model_name']}", row["brand_name"], row["category_id"],
                    row["philippine_release_year"], "Dated first Philippine release or sale evidence",
                    "Official local presence established, original release date unknown",
                    "Find dated launch or first authorized sale source", "High", "Open", None))


def validate(db: sqlite3.Connection) -> list[str]:
    errors = []
    integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
    if integrity != "ok":
        errors.append(f"SQLite integrity: {integrity}")
    foreign_keys = db.execute("PRAGMA foreign_key_check").fetchall()
    if foreign_keys:
        errors.append(f"Foreign key failures: {len(foreign_keys)}")
    missing_evidence = db.execute("""SELECT COUNT(*) FROM philippines_market_releases r
        WHERE r.verification_status != 'PENDING_VERIFICATION' AND NOT EXISTS
        (SELECT 1 FROM device_source_evidence e WHERE e.device_id=r.device_id)""").fetchone()[0]
    if missing_evidence:
        errors.append(f"Verified models without evidence: {missing_evidence}")
    future = db.execute("""SELECT COUNT(*) FROM philippines_market_releases
        WHERE philippine_release_date > ? OR availability_observed_at > ?""", (CUTOFF, CUTOFF)).fetchone()[0]
    if future:
        errors.append(f"Dates later than cutoff: {future}")
    duplicate_models = db.execute("""SELECT COUNT(*) FROM
      (SELECT category_id, brand_id, lower(model_name), COUNT(*) c FROM device_models
       GROUP BY category_id, brand_id, lower(model_name) HAVING c>1)""").fetchone()[0]
    if duplicate_models:
        errors.append(f"Duplicate base models: {duplicate_models}")
    status_mismatch = db.execute("""SELECT COUNT(*) FROM philippines_market_releases
      WHERE inclusion_status='Included' AND verification_status='PENDING_VERIFICATION'""").fetchone()[0]
    if status_mismatch:
        errors.append(f"Pending models counted as included: {status_mismatch}")
    return errors


def export_tables(db: sqlite3.Connection) -> dict[str, list[dict]]:
    csv_dir = OUTPUT / "deviceiq_inventory_csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    for table in TABLES:
        rows = [dict(row) for row in db.execute(f"SELECT * FROM {table}")]
        result[table] = rows
        columns = [item[1] for item in db.execute(f"PRAGMA table_info({table})")]
        with (csv_dir / f"{table}.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
    (OUTPUT / "deviceiq_inventory.json").write_text(json.dumps({"metadata": {
        "research_cutoff": CUTOFF, "historical_start": HISTORICAL_START,
        "rolling_start": ROLLING_START, "status": "provisional; not a census"},
        "tables": result}, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def report(db: sqlite3.Connection, errors: list[str]) -> None:
    q = lambda sql: db.execute(sql).fetchone()[0]
    stats = {
        "raw_lines": q("SELECT COUNT(*) FROM raw_research_claims"),
        "structured_claims": q("SELECT COUNT(*) FROM raw_research_claims WHERE original_model_text IS NOT NULL"),
        "duplicate_claims": q("SELECT COUNT(*) FROM raw_research_claims WHERE duplicate_of IS NOT NULL"),
        "candidate_models": q("SELECT COUNT(*) FROM device_models"),
        "verified_models": q("SELECT COUNT(*) FROM philippines_market_releases WHERE verification_status != 'PENDING_VERIFICATION'"),
        "included_models": q("SELECT COUNT(*) FROM philippines_market_releases WHERE inclusion_status='Included'"),
        "pending_models": q("SELECT COUNT(*) FROM philippines_market_releases WHERE verification_status='PENDING_VERIFICATION'"),
        "pending_date": q("SELECT COUNT(*) FROM philippines_market_releases WHERE inclusion_status='Pending date'"),
        "excluded": q("SELECT COUNT(*) FROM excluded_records"),
        "held_out": q("SELECT COUNT(*) FROM excluded_records WHERE exclusion_reason LIKE 'Hold out:%'"),
        "outside_window": q("SELECT COUNT(*) FROM excluded_records WHERE exclusion_reason NOT LIKE 'Hold out:%'"),
        "manufacturers": q("SELECT COUNT(*) FROM manufacturers"),
        "brands": q("SELECT COUNT(*) FROM brands"),
        "open_queue": q("SELECT COUNT(*) FROM research_queue WHERE current_status='Open'"),
        "missing_specs": q("""SELECT COUNT(*) FROM device_models m WHERE NOT EXISTS
           (SELECT 1 FROM device_specifications s WHERE s.device_id=m.device_id)"""),
        "missing_source": q("SELECT COUNT(*) FROM philippines_market_releases WHERE primary_source_id IS NULL"),
    }
    by_category = {row[0]: row[1] for row in db.execute("SELECT category_id,COUNT(*) FROM device_models GROUP BY category_id")}
    verified_by_category = {row[0]: row[1] for row in db.execute("""SELECT m.category_id,COUNT(*) FROM device_models m
       JOIN philippines_market_releases r ON r.device_id=m.device_id
       WHERE r.verification_status!='PENDING_VERIFICATION' GROUP BY m.category_id""")}
    (OUTPUT / "inventory_metrics.json").write_text(json.dumps({"stats": stats, "by_category": by_category,
        "verified_by_category": verified_by_category, "validation_errors": errors}, indent=2), encoding="utf-8")
    (OUTPUT / "DeviceIQ_Data_Quality_Report.md").write_text(f"""# DeviceIQ data quality report

Snapshot cutoff: {CUTOFF}. This is a provisional inventory, not an exhaustive Philippine device census.

| Measure | Count |
| --- | ---: |
| Preserved nonblank source lines | {stats['raw_lines']} |
| Brand/year/category example claims | {stats['structured_claims']} |
| Duplicate structured claims retained | {stats['duplicate_claims']} |
| Unique candidate or verified base-model records | {stats['candidate_models']} |
| Models with official Philippine-market evidence | {stats['verified_models']} |
| Models included in provisional rolling window | {stats['included_models']} |
| Pending model verification | {stats['pending_models']} |
| Verified local presence but local date unresolved | {stats['pending_date']} |
| Excluded or held-out research records | {stats['excluded']} |
| Of those: explicit 2026 holdouts | {stats['held_out']} |
| Of those: outside rolling window | {stats['outside_window']} |
| Manufacturers with a recorded corporate mapping | {stats['manufacturers']} |
| Consumer-facing brand labels | {stats['brands']} |
| Open research actions | {stats['open_queue']} |
| Models with no recorded technical specifications | {stats['missing_specs']} |
| Models without a linked model-level source | {stats['missing_source']} |

## Category counts

| Category | Candidate or verified models | Official local evidence |
| --- | ---: | ---: |
""" + "".join(f"| {category.title()} | {by_category.get(category, 0)} | {verified_by_category.get(category, 0)} |\n" for category in ["smartphones", "tablets", "laptops"]) + """
## Interpretation

The supplied annual notes list brands and examples, not all individual releases. Candidate names parsed from those examples remain pending until a model-level Philippine source is linked. Series claims remain in the verification queue until their individual models are established. The 2026 note repeats much of the annual list; duplicates are retained in raw claims and not counted twice as base models. Seven explicitly excluded or future-availability cases from that note are held out pending source review. The three 2021 Galaxy S21 records have official local availability evidence before the provisional rolling-window start and remain in the historical inventory with an exclusion flag.

Most original Philippine release dates and many configuration specifications are missing. The existing 30 catalog records establish official Philippine product or store listings, but 29 lack a dated original local launch; those remain pending for rolling-window eligibility. No live application database was reset or populated.
""", encoding="utf-8")
    (OUTPUT / "DeviceIQ_Validation_Report.md").write_text("# DeviceIQ validation report\n\n" +
        ("All structural and cutoff checks passed.\n" if not errors else "\n".join(f"- {error}" for error in errors)) +
        "\n\nChecks: SQLite integrity and foreign keys, unique base models, verified evidence, cutoff dates, and inclusion status.\n",
        encoding="utf-8")
    duplicates = [dict(row) for row in db.execute("""SELECT source_file,source_line,original_brand_name,original_model_text,duplicate_of
      FROM raw_research_claims WHERE duplicate_of IS NOT NULL ORDER BY source_file,source_line""")]
    (OUTPUT / "DeviceIQ_Duplicate_Review.md").write_text("# Duplicate claim review\n\n" +
        f"{len(duplicates)} repeated brand/year/example claims were preserved in staging. They did not create duplicate base models.\n\n" +
        "| Source line | Brand | Repeated example text | First claim ID |\n| --- | --- | --- | --- |\n" +
        "".join(f"| {item['source_file']}:{item['source_line']} | {item['original_brand_name']} | {item['original_model_text'].replace('|','/')} | {item['duplicate_of']} |\n" for item in duplicates),
        encoding="utf-8")


def main() -> None:
    raw, structured = read_research_notes()
    db = open_database()
    try:
        add_raw_and_candidates(db, raw, structured)
        add_existing_catalog(db, catalog_seed())
        add_researched_models(db)
        add_explicit_holdouts(db)
        add_laptop_research_queue(db)
        add_missing_date_queue(db)
        db.commit()
        errors = validate(db)
        export_tables(db)
        report(db, errors)
        print(json.dumps({"raw_lines": len(raw), "structured_rows": len(structured),
                          "models": db.execute("SELECT COUNT(*) FROM device_models").fetchone()[0],
                          "verified": db.execute("SELECT COUNT(*) FROM philippines_market_releases WHERE verification_status!='PENDING_VERIFICATION'").fetchone()[0],
                          "validation_errors": errors}))
        if errors:
            raise SystemExit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
