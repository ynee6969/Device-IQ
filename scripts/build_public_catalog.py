"""Publish only source-linked, date-eligible inventory records for the website.

The full research inventory remains separate. Run after rebuilding the research JSON.
"""
from collections import defaultdict
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "outputs/deviceiq-inventory-2026-11-24/deviceiq_inventory.json"
OUTPUT = ROOT / "lib/catalog/public-inventory.json"
START, CUTOFF = "2021-01-01", "2026-11-24"
tables = json.loads(INVENTORY.read_text(encoding="utf-8"))["tables"]
by_id = lambda name, key: {row[key]: row for row in tables[name]}
models = by_id("device_models", "device_id")
brands = by_id("brands", "brand_id")
sources = by_id("data_sources", "source_id")
releases = by_id("philippines_market_releases", "device_id")
configs = defaultdict(list)
specs = defaultdict(list)
evidence = defaultdict(list)
for row in tables["device_configurations"]:
    configs[row["device_id"]].append(row)
for row in tables["device_specifications"]:
    specs[row["device_id"]].append(row)
for row in tables["device_source_evidence"]:
    evidence[row["device_id"]].append(row)
held_out = {(row["brand_name"], row["device_name"], row["category_id"])
            for row in tables["excluded_records"] if row["exclusion_reason"].startswith("Hold out:")}


def eligible(model):
    release = releases[model["device_id"]]
    if release["verification_status"] not in {"VERIFIED_OFFICIAL_LAUNCH", "VERIFIED_AUTHORIZED_AVAILABILITY"}:
        return False
    brand = brands[model["brand_id"]]["brand_name"]
    if (brand, model["model_name"], model["category_id"]) in held_out:
        return False
    # An announced future retail release is not established as available.
    if "retail availability unconfirmed" in release["availability_status"].lower():
        return False
    source = sources.get(release["primary_source_id"])
    if not source or not source["source_url"] or not source["source_url"].startswith("https://"):
        return False
    if not source["source_type"].startswith("Official Philippine"):
        return False
    if release["philippine_release_date"]:
        return START <= release["philippine_release_date"] <= CUTOFF
    year = release["philippine_release_year"]
    observed = release["availability_observed_at"]
    return bool(year and 2021 <= year <= 2026 and observed and START <= observed <= CUTOFF
                and int(observed[:4]) == year)


def value(row):
    number = row["numeric_value"]
    if number is None:
        return row["value_text"]
    return int(number) if int(number) == number else number


published = []
for model in tables["device_models"]:
    if not eligible(model):
        continue
    device_id = model["device_id"]
    release = releases[device_id]
    brand = brands[model["brand_id"]]["brand_name"]
    linked_sources = []
    for source_id in [release["primary_source_id"], *[row["source_id"] for row in evidence[device_id]]]:
        source = sources.get(source_id)
        if source and source["source_url"] and source["source_url"] not in {s["url"] for s in linked_sources}:
            linked_sources.append({"organization": source["publisher"], "url": source["source_url"],
                                   "observedAt": source["access_date"], "publishedAt": source["publication_date"],
                                   "purpose": "Specifications and availability"})
    model_specs = {row["spec_key"]: value(row) for row in specs[device_id] if row["configuration_id"] is None}
    model_sources = {row["spec_key"]: sources[row["source_id"]]["source_url"] for row in specs[device_id]
                     if row["configuration_id"] is None and row["source_id"] in sources}
    variants = []
    for config in configs[device_id] or [None]:
        variant_specs = dict(model_specs)
        variant_sources = dict(model_sources)
        if config:
            for row in specs[device_id]:
                if row["configuration_id"] == config["configuration_id"]:
                    variant_specs[row["spec_key"]] = value(row)
                    if row["source_id"] in sources:
                        variant_sources[row["spec_key"]] = sources[row["source_id"]]["source_url"]
        price_source = sources.get(config["price_source_id"]) if config else None
        price = config["price_php"] if config else None
        # A price needs its own dated source; do not infer a new/used price.
        if price is not None and not (price_source and config["price_observed_at"] and config["price_condition"]):
            price = None
        condition = None
        if price is not None:
            condition = "used" if "used" in config["price_condition"].lower() else "new"
        variants.append({"id": config["configuration_id"] if config else f"{device_id}-unrecorded",
                         "label": config["configuration_name"] if config else "Configuration not recorded",
                         "specs": variant_specs, "specSources": variant_sources, "pricePhp": price,
                         "priceCondition": condition,
                         "priceObservedAt": config["price_observed_at"] if price is not None else None,
                         "priceSourceUrl": price_source["source_url"] if price is not None else None,
                         "listingStatus": "Not verified",
                         "notes": config["notes"] if config else "Configuration details have not been recorded."})
    published.append({"id": device_id, "category": model["category_id"], "brand": brand,
                      "model": model["model_name"], "releaseDate": model["global_release_date"],
                      "philippineAvailabilityDate": release["philippine_release_date"],
                      "philippineDateLabel": "Philippine launch date" if release["official_launch_status"] == "Official local launch" else "Philippine availability date",
                      "philippineReleaseYear": release["philippine_release_year"],
                      "localEvidenceObservedAt": release["availability_observed_at"],
                      "verificationStatus": release["verification_status"],
                      "philippineAvailability": release["market_availability_evidence"],
                      "discontinued": None, "sources": linked_sources, "variants": variants,
                      "imageId": "samsung-tab-s10-fe" if brand == "Samsung" and model["model_name"] == "Galaxy Tab S10 FE" else None})

published.sort(key=lambda row: (row["category"], row["brand"], row["model"]))
assert len(published) == 28, f"Review eligibility changes before publishing: {len(published)}"
assert len({row["id"] for row in published}) == len(published)
assert all(row["sources"] and row["variants"] for row in published)
OUTPUT.write_text(json.dumps(published, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"models": len(published), "categories": {category: sum(x["category"] == category for x in published)
               for category in ["smartphones", "tablets", "laptops"]}, "variants": sum(len(x["variants"]) for x in published)}))
