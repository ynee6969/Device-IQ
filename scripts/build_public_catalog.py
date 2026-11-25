"""Generate the public research catalog from the supplied workbook.

The workbook is read only. The website consumes the checked-in JSON snapshot,
so it does not need the workbook or openpyxl at runtime.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime
from hashlib import sha256
from pathlib import Path
import argparse
import json

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKBOOK = Path.home() / "Downloads/DeviceIQ_Philippine_Device_Inventory_2021-2026.xlsx"
OUTPUT = ROOT / "lib/catalog/public-inventory.json"
METADATA = ROOT / "research/catalog-workbook-source.json"
MANIFEST = ROOT / "lib/catalog/image-manifest.json"
ALIASES = ROOT / "research/catalog-image-aliases.json"

parser = argparse.ArgumentParser()
parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK)
args = parser.parse_args()
workbook_path = args.workbook.resolve()
if not workbook_path.is_file():
    parser.error(f"Workbook not found: {workbook_path}")

workbook = openpyxl.load_workbook(workbook_path, read_only=True, data_only=True)


def rows(sheet_name):
    cells = workbook[sheet_name].iter_rows(values_only=True)
    headers = next(cells)
    return [{**dict(zip(headers, row)), "_workbook_row": index}
            for index, row in enumerate(cells, start=2) if any(value is not None for value in row)]


def text(value):
    return str(value).strip() if value is not None and str(value).strip() else None


def iso(value):
    if isinstance(value, (datetime, date)):
        return value.date().isoformat() if isinstance(value, datetime) else value.isoformat()
    return text(value)


def number(value):
    if isinstance(value, bool) or value is None:
        return None
    try:
        parsed = float(value)
        return int(parsed) if parsed.is_integer() else parsed
    except (ValueError, TypeError):
        return None


def field(value, numeric=False):
    return number(value) if numeric else text(value)


def specs_from(row, category, configuration=False):
    definitions = {
        "ramGb": ("RAM GB", True), "storageGb": ("Storage GB", True),
        "displayInches": ("Display in", True), "resolution": ("Resolution", False),
        "batteryMah": ("Battery mAh", True), "batteryWh": ("Battery Wh", True),
        "rearCameraMp": ("Rear Camera MP", True), "frontCameraMp": ("Front Camera MP", True),
        "os": ("Operating System", False),
    }
    if configuration:
        definitions.update({
            "chipset": ("Chipset", False), "cpu": ("CPU", False), "gpu": ("GPU", False),
            "displayType": ("Display Type", False), "refreshHz": ("Refresh Hz", True),
            "chargingW": ("Charging W", True), "cellular": ("Connectivity", False),
            "weightG": ("Weight g", True),
        })
    result = {key: field(row.get(column), numeric)
              for key, (column, numeric) in definitions.items()}
    processor = text(row.get("Processor"))
    if processor:
        key = "cpu" if category == "laptops" else "chipset"
        result.setdefault(key, processor)
    return {key: value for key, value in result.items() if value is not None}


master = rows("MASTER DEVICE INVENTORY")
category_rows = {row["Device ID"]: row for category in ("SMARTPHONES", "TABLETS", "LAPTOPS")
                 for row in rows(category)}
release_rows = {row["Device ID"]: row for row in rows("PHILIPPINE RELEASE RECORDS")}
configuration_rows = defaultdict(list)
for row in rows("DEVICE CONFIGURATIONS"):
    configuration_rows[row["Device ID"]].append(row)
source_rows = defaultdict(list)
for row in rows("SOURCE REFERENCES"):
    if row.get("Device ID"):
        source_rows[row["Device ID"]].append(row)
queue_rows = defaultdict(list)
for row in rows("VERIFICATION QUEUE"):
    if row.get("Device ID") and row.get("Current Status") == "Open":
        queue_rows[row["Device ID"]].append(row)
excluded_rows = rows("EXCLUDED RECORDS")
excluded_by_identity = {(row["Category"], row["Brand"], row["Device Name"]): row for row in excluded_rows}
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
aliases = json.loads(ALIASES.read_text(encoding="utf-8")) if ALIASES.exists() else {}


def sources_for(device_id, primary_url):
    collected = {}
    for row in source_rows[device_id]:
        url = text(row.get("Source URL"))
        if not url or not url.startswith("https://"):
            continue
        if url in collected:
            continue
        collected[url] = {
            "organization": text(row.get("Publisher")) or "Source in research inventory",
            "url": url,
            "observedAt": iso(row.get("Accessed")),
            "publishedAt": iso(row.get("Published")),
            "purpose": text(row.get("Supported Claim")) or "Research reference",
            "note": text(row.get("Reviewer Notes")),
        }
    if primary_url and primary_url.startswith("https://") and primary_url not in collected:
        collected[primary_url] = {"organization": "Source in research inventory", "url": primary_url,
                                  "observedAt": None, "publishedAt": None, "purpose": "Research reference", "note": None}
    return list(collected.values())


def image_id_for(device_id):
    candidate = device_id if device_id in manifest else aliases.get(device_id)
    if candidate and candidate not in manifest:
        raise ValueError(f"Image alias not in manifest: {device_id} -> {candidate}")
    return candidate


catalog = []
for item in master:
    device_id = item["Device ID"]
    category = item["Category"]
    if category not in ("smartphones", "tablets", "laptops"):
        raise ValueError(f"Unexpected category for {device_id}: {category}")
    summary = category_rows.get(device_id)
    release = release_rows.get(device_id)
    if not summary or not release:
        raise ValueError(f"Missing category or release row: {device_id}")
    brand, model = item["Brand"], item["Exact Model"]
    exclusion = excluded_by_identity.get((category, brand, model))
    scope = "Excluded" if exclusion else item["Selected Scope Status"]
    model_specs = specs_from(summary, category)
    model_source = text(summary.get("Primary Source URL"))
    variant_list = []
    configs = configuration_rows.get(device_id) or [None]
    for config in configs:
        config_specs = specs_from(config, category, True) if config else {}
        specs = {**model_specs, **config_specs}
        config_source = text(config.get("Source URL")) if config else None
        spec_sources = {key: model_source for key in model_specs} if model_source and model_source.startswith("https://") else {}
        if config_source and config_source.startswith("https://"):
            spec_sources.update({key: config_source for key in config_specs})
        price = number(config.get("Price PHP")) if config else None
        price_source = text(config.get("Source URL")) if config else None
        price_date = iso(config.get("Price Observed")) if config else None
        raw_condition = text(config.get("Price Condition")) if config else None
        condition = "used" if raw_condition and "used" in raw_condition.lower() else "new" if raw_condition and "new" in raw_condition.lower() else None
        if price is not None and (not price_source or not price_date or not raw_condition):
            raise ValueError(f"Price lacks provenance: {device_id}")
        variant_list.append({
            "id": config["Configuration ID"] if config else f"{device_id}-unrecorded",
            "label": text(config.get("Configuration")) if config else "Configuration not recorded",
            "specs": specs, "specSources": spec_sources,
            "pricePhp": price, "priceCondition": condition, "priceType": raw_condition,
            "priceObservedAt": price_date, "priceSourceUrl": price_source,
            "listingStatus": "Not verified", "notes": text(config.get("Notes")) if config else None,
            "sku": text(config.get("SKU")) if config else None,
            "modelCode": text(config.get("Model Code")) if config else None,
            "workbookRow": config["_workbook_row"] if config else None,
        })
    issue_list = [{"issue": text(row.get("Verification Issue")),
                   "action": text(row.get("Required Action"))} for row in queue_rows[device_id]]
    catalog.append({
        "id": device_id, "recordType": "device", "category": category,
        "brand": brand, "model": model,
        "manufacturer": text(item.get("Manufacturer")),
        "productLine": text(item.get("Product Line")),
        "modelNumber": text(item.get("Model Number")),
        "releaseDate": iso(item.get("Global Release Date")),
        "philippineAvailabilityDate": iso(release.get("Local Launch Date")) or iso(release.get("Availability Date")),
        "philippineDateLabel": "Philippine launch date" if iso(release.get("Local Launch Date")) else "Philippine availability date",
        "philippineReleaseYear": number(release.get("Local Release Year")),
        "claimedReleaseYear": number(item.get("Claimed Release Year")),
        "localEvidenceObservedAt": iso(release.get("Observed Date")),
        "verificationStatus": text(item.get("Verification Status")) or "PENDING_VERIFICATION",
        "scopeStatus": scope,
        "qualityFlag": text(item.get("Quality Flag")),
        "exclusionReason": text(exclusion.get("Reason")) if exclusion else None,
        "exclusionEvidence": text(exclusion.get("Supporting Evidence")) if exclusion else None,
        "philippineAvailability": text(release.get("Evidence")) or "Not recorded",
        "availabilityStatus": text(release.get("Availability Status")) or "Not recorded",
        "discontinued": None,
        "researchNotes": text(item.get("Notes")) or text(summary.get("Research Notes")),
        "openIssues": issue_list,
        "sources": sources_for(device_id, text(item.get("Primary Source URL"))),
        "variants": variant_list,
        "imageId": image_id_for(device_id),
        "workbookRow": item["_workbook_row"],
    })

matched_exclusions = {(item["category"], item["brand"], item["model"]) for item in catalog if item["scopeStatus"] == "Excluded"}
for item in excluded_rows:
    identity = (item["Category"], item["Brand"], item["Device Name"])
    if identity in matched_exclusions:
        continue
    if not str(item["Reason"]).startswith("Hold out:"):
        raise ValueError(f"Unmatched exclusion is not a held-out claim: {item['Exclusion ID']}")
    device_id = item["Exclusion ID"]
    catalog.append({
        "id": device_id, "recordType": "held_out_claim", "category": item["Category"],
        "brand": item["Brand"], "model": item["Device Name"],
        "manufacturer": None, "productLine": None, "modelNumber": None,
        "releaseDate": None, "philippineAvailabilityDate": None,
        "philippineDateLabel": "Philippine availability date", "philippineReleaseYear": None,
        "claimedReleaseYear": None, "localEvidenceObservedAt": None,
        "verificationStatus": "PENDING_VERIFICATION", "scopeStatus": "Held out",
        "qualityFlag": "Unresolved local availability",
        "exclusionReason": text(item.get("Reason")),
        "exclusionEvidence": text(item.get("Supporting Evidence")),
        "philippineAvailability": "Not verified", "availabilityStatus": "Not verified",
        "discontinued": None, "researchNotes": text(item.get("Original Record")),
        "openIssues": [], "sources": [],
        "variants": [{"id": f"{device_id}-unrecorded", "label": "Configuration not recorded",
                      "specs": {}, "specSources": {}, "pricePhp": None, "priceCondition": None,
                      "priceType": None,
                      "priceObservedAt": None, "priceSourceUrl": None,
                      "listingStatus": "Not verified", "notes": None, "sku": None,
                      "modelCode": None, "workbookRow": None}],
        "imageId": None, "workbookRow": item["_workbook_row"],
    })

catalog.sort(key=lambda item: (item["category"], item["brand"].casefold(), item["model"].casefold()))
if len(master) != 456 or len(catalog) != 463:
    raise ValueError(f"Unexpected workbook inventory counts: {len(master)} master, {len(catalog)} public")
if len({item["id"] for item in catalog}) != len(catalog):
    raise ValueError("Duplicate public catalog record ID")
if len({variant["id"] for item in catalog for variant in item["variants"]}) != sum(len(item["variants"]) for item in catalog):
    raise ValueError("Duplicate configuration ID")
OUTPUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
METADATA.write_text(json.dumps({
    "workbookName": workbook_path.name, "sha256": sha256(workbook_path.read_bytes()).hexdigest(),
    "sheetsUsed": ["MASTER DEVICE INVENTORY", "SMARTPHONES", "TABLETS", "LAPTOPS",
                   "DEVICE CONFIGURATIONS", "PHILIPPINE RELEASE RECORDS", "SOURCE REFERENCES",
                   "VERIFICATION QUEUE", "EXCLUDED RECORDS"],
    "masterRecords": len(master), "heldOutClaimsAdded": len(catalog) - len(master),
    "publicRecords": len(catalog), "configurationRows": sum(len(item["variants"]) for item in catalog),
    "scopeCounts": dict(Counter(item["scopeStatus"] for item in catalog)),
    "categoryCounts": dict(Counter(item["category"] for item in catalog)),
}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"records": len(catalog), "categories": dict(Counter(item["category"] for item in catalog)),
                  "scope": dict(Counter(item["scopeStatus"] for item in catalog)),
                  "variants": sum(len(item["variants"]) for item in catalog),
                  "images": sum(bool(item["imageId"]) for item in catalog)}))
