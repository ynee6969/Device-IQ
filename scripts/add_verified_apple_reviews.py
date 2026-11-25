#!/usr/bin/env python3
"""Add model-level Apple specification evidence and exact PH store offers.

Global tech specs are kept separate from Philippine availability. Only current
Apple PH listings with exact storage/connectivity and a dated price replace an
unrecorded placeholder with specific configuration rows.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-25"


def source(source_id: str, publisher: str, url: str, purpose: str, note: str,
           published: str | None = None) -> dict:
    return {"id": source_id, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def field(field_id: str, source_id: str, source_value, normalized, *,
          key: str | None = None, unit: str | None = None,
          status: str = "VERIFIED", note: str | None = None,
          price_condition: str | None = None, price_type: str | None = None,
          price_observed: str | None = None, clear_key: str | None = None) -> dict:
    row = {"fieldId": field_id, "status": status, "sourceId": source_id,
           "sourceValue": source_value, "normalizedValue": normalized,
           "note": note or "Checked against Apple's exact-model technical specifications. The workbook does not identify an exact storage configuration."}
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized
    if clear_key:
        row["clearCatalogKey"] = clear_key
    if unit:
        row["unit"] = unit
    if price_condition:
        row["priceCondition"] = price_condition
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed
    return row


def config_id(device_id: str, label: str) -> str:
    digest = hashlib.sha256(f"{device_id}|{label}".encode()).hexdigest()[:14]
    return f"config_{digest}"


# Exact model source facts. These are device-level values shared across
# configurations. We do not infer battery mAh, RAM, or a Philippine launch date.
MODELS = [
    {"model": "15 Plus", "url": "https://support.apple.com/en-us/111830", "year": 2023,
     "values": {"displayInches": 6.7, "displayType": "OLED", "resolution": "1290 x 2796", "chipset": "Apple A16 Bionic", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "5-core Apple GPU", "frontCameraMp": 12, "weightG": 201, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "128GB, 256GB, or 512GB"},
    {"model": "15 Pro", "url": "https://support.apple.com/en-us/111829", "year": 2023,
     "values": {"displayInches": 6.1, "displayType": "OLED", "resolution": "1179 x 2556", "refreshHz": 120, "chipset": "Apple A17 Pro", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "6-core Apple GPU", "frontCameraMp": 12, "weightG": 187, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "128GB, 256GB, 512GB, or 1TB"},
    {"model": "15 Pro Max", "url": "https://support.apple.com/en-us/111828", "year": 2023,
     "values": {"displayInches": 6.7, "displayType": "OLED", "resolution": "1290 x 2796", "refreshHz": 120, "chipset": "Apple A17 Pro", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "6-core Apple GPU", "frontCameraMp": 12, "weightG": 221, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "256GB, 512GB, or 1TB"},
    {"model": "16 Plus", "url": "https://support.apple.com/en-us/121030", "year": 2024,
     "values": {"displayInches": 6.7, "displayType": "OLED", "resolution": "1290 x 2796", "chipset": "Apple A18", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "5-core Apple GPU", "frontCameraMp": 12, "weightG": 199, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "128GB, 256GB, or 512GB"},
    {"model": "16 Pro", "url": "https://support.apple.com/en-us/121031", "year": 2024,
     "values": {"displayInches": 6.3, "displayType": "OLED", "resolution": "1206 x 2622", "refreshHz": 120, "chipset": "Apple A18 Pro", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "6-core Apple GPU", "frontCameraMp": 12, "weightG": 199, "video": "4K Dolby Vision video recording up to 120 fps"},
     "storage": "128GB, 256GB, 512GB, or 1TB"},
    {"model": "16 Pro Max", "url": "https://support.apple.com/en-us/121032", "year": 2024,
     "values": {"displayInches": 6.9, "displayType": "OLED", "resolution": "1320 x 2868", "refreshHz": 120, "chipset": "Apple A18 Pro", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "6-core Apple GPU", "frontCameraMp": 12, "weightG": 227, "video": "4K Dolby Vision video recording up to 120 fps"},
     "storage": "256GB, 512GB, or 1TB"},
    {"model": "iPhone 15", "url": "https://support.apple.com/en-us/111831", "year": 2023,
     "values": {"displayInches": 6.1, "displayType": "OLED", "resolution": "1179 x 2556", "chipset": "Apple A16 Bionic", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "5-core Apple GPU", "frontCameraMp": 12, "weightG": 171, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "128GB, 256GB, or 512GB"},
    {"model": "iPhone 16", "url": "https://support.apple.com/en-us/121029", "year": 2024,
     "values": {"displayInches": 6.1, "displayType": "OLED", "resolution": "1179 x 2556", "chipset": "Apple A18", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "5-core Apple GPU", "frontCameraMp": 12, "weightG": 170, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "128GB, 256GB, or 512GB", "store": "https://www.apple.com/ph/shop/buy-iphone/iphone-16/6.1-inch-display-128gb-black",
     "offers": [("128GB", 128, 62990)], "availabilityVerified": True},
    {"model": "iPhone 16e", "url": "https://support.apple.com/en-us/122208", "year": 2025,
     "values": {"displayInches": 6.1, "displayType": "OLED", "resolution": "1170 x 2532", "chipset": "Apple A18", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "4-core Apple GPU", "frontCameraMp": 12, "weightG": 167, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "128GB, 256GB, or 512GB"},
    {"model": "iPhone SE (2022)", "url": "https://support.apple.com/en-us/111866", "year": 2022,
     "values": {"displayInches": 4.7, "displayType": "LCD IPS", "resolution": "750 x 1334", "chipset": "Apple A15 Bionic", "cpu": "6-core CPU (2 performance cores, 4 efficiency cores)", "gpu": "4-core Apple GPU", "frontCameraMp": 7, "weightG": 144, "video": "4K video recording up to 60 fps"},
     "storage": "64GB, 128GB, or 256GB"},
    {"model": "iPhone 17", "url": "https://support.apple.com/en-us/125089", "year": 2025,
     "values": {"displayInches": 6.3, "displayType": "OLED", "resolution": "1206 x 2622", "refreshHz": 120, "chipset": "Apple A19", "cpu": "6-core CPU", "gpu": "5-core Apple GPU", "frontCameraMp": 18, "weightG": 177, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "256GB or 512GB", "store": "https://www.apple.com/ph/shop/buy-iphone/iphone-17/6.3-inch-display-256gb-black",
     "offers": [("256GB", 256, 69990), ("512GB", 512, 85990)],
     "completeOfferSet": True, "launch": ("https://www.apple.com/ph/newsroom/2025/09/apple-debuts-iphone-17/", "2025-09-09", 57990)},
    {"model": "iPhone 17e", "url": "https://support.apple.com/en-us/126470", "year": 2026,
     "values": {"displayInches": 6.1, "displayType": "OLED", "resolution": "1170 x 2532", "chipset": "Apple A19", "cpu": "6-core CPU", "gpu": "4-core Apple GPU", "frontCameraMp": 12, "weightG": 170, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "256GB or 512GB", "store": "https://www.apple.com/ph/shop/buy-iphone/iphone-17e",
     "offers": [("256GB", 256, 54990), ("512GB", 512, 70990)],
     "completeOfferSet": True, "launch": ("https://www.apple.com/ph/newsroom/2026/03/apple-introduces-iphone-17e/", "2026-03-02", 44990)},
    {"model": "iPhone Air", "url": "https://support.apple.com/en-us/125092", "year": 2025,
     "values": {"displayInches": 6.5, "displayType": "OLED", "resolution": "1260 x 2736", "refreshHz": 120, "chipset": "Apple A19 Pro", "cpu": "6-core CPU", "gpu": "5-core Apple GPU", "frontCameraMp": 18, "weightG": 165, "video": "4K Dolby Vision video recording up to 60 fps"},
     "storage": "256GB, 512GB, or 1TB", "store": "https://www.apple.com/ph/shop/buy-iphone/iphone-air",
     "offers": [("256GB", 256, 84990), ("512GB", 512, 100990), ("1TB", 1024, 132990)], "completeOfferSet": True},
]

TABLETS = [
    {"model": "iPad (A16/11th Gen)", "url": "https://support.apple.com/en-us/122240", "year": 2025,
     "values": {"displayInches": 10.86, "displayType": "LCD IPS", "resolution": "1640 x 2360", "chipset": "Apple A16", "cpu": "5-core CPU", "gpu": "4-core Apple GPU", "frontCameraMp": 12, "wifi": "Wi-Fi 6 (802.11ax)"}, "weightByConnectivity": {"Wi-Fi": 477, "Wi-Fi + Cellular": 481}, "storage": "128GB, 256GB, or 512GB"},
    {"model": "iPad 10th Gen", "url": "https://support.apple.com/en-us/111840", "year": 2022,
     "values": {"displayInches": 10.86, "displayType": "LCD IPS", "resolution": "1640 x 2360", "chipset": "Apple A14 Bionic", "cpu": "6-core CPU", "gpu": "4-core Apple GPU", "frontCameraMp": 12, "wifi": "Wi-Fi 6 (802.11ax)"}, "weightByConnectivity": {"Wi-Fi": 477, "Wi-Fi + Cellular": 481}, "storage": "64GB or 256GB"},
    {"model": "iPad 9th Gen", "url": "https://support.apple.com/en-us/111898", "year": 2021,
     "values": {"displayInches": 10.2, "displayType": "LCD IPS", "resolution": "1620 x 2160", "chipset": "Apple A13 Bionic", "cpu": "6-core CPU", "gpu": "4-core Apple GPU", "frontCameraMp": 12, "wifi": "Wi-Fi 5 (802.11ac)"}, "weightByConnectivity": {"Wi-Fi": 487, "Wi-Fi + Cellular": 498}, "storage": "64GB or 256GB"},
    {"model": "iPad Air 5th Gen", "url": "https://support.apple.com/en-us/111887", "year": 2022,
     "values": {"displayInches": 10.86, "displayType": "LCD IPS", "resolution": "1640 x 2360", "chipset": "Apple M1", "cpu": "8-core CPU", "gpu": "8-core Apple GPU", "ramGb": 8, "frontCameraMp": 12, "wifi": "Wi-Fi 6 (802.11ax)"}, "weightByConnectivity": {"Wi-Fi": 461, "Wi-Fi + Cellular": 462}, "storage": "64GB or 256GB"},
    {"model": "iPad Air M3", "url": "https://support.apple.com/en-us/122241", "year": 2025,
     "values": {"chipset": "Apple M3", "cpu": "8-core CPU", "gpu": "9-core Apple GPU", "ramGb": 8}, "storage": "128GB, 256GB, 512GB, or 1TB", "also": ["https://support.apple.com/en-us/122242"]},
    {"model": "iPad Air M4", "url": "https://support.apple.com/en-us/126471", "year": 2026,
     "values": {"chipset": "Apple M4", "cpu": "8-core CPU", "gpu": "9-core Apple GPU", "ramGb": 12}, "storage": "128GB, 256GB, 512GB, or 1TB", "also": ["https://support.apple.com/en-us/126472"]},
    {"model": "iPad mini 6", "url": "https://support.apple.com/en-us/111886", "year": 2021,
     "values": {"displayInches": 8.3, "displayType": "LCD IPS", "resolution": "1488 x 2266", "chipset": "Apple A15 Bionic", "cpu": "6-core CPU", "gpu": "5-core Apple GPU", "frontCameraMp": 12, "wifi": "Wi-Fi 6 (802.11ax)"}, "weightByConnectivity": {"Wi-Fi": 293, "Wi-Fi + Cellular": 297}, "storage": "64GB or 256GB"},
    {"model": "iPad mini A20 Pro", "url": "https://support.apple.com/en-us/149482", "year": 2026,
     "values": {"displayInches": 8.5, "displayType": "OLED", "resolution": "1512 x 2316", "chipset": "Apple A20 Pro", "gpu": "7-core Apple GPU", "frontCameraMp": 12}, "cpuByStorage": {128: "5-core CPU", 256: "5-core CPU", 512: "6-core CPU"}, "weightByConnectivity": {"Wi-Fi": 255, "Wi-Fi + Cellular": 263}, "storage": "128GB, 256GB, or 512GB",
     "store": "https://www.apple.com/ph/shop/buy-ipad/ipad-mini/512gb-starlight-wifi-cellular-nano-texture-glass?product=PJ6P4PP%2FA",
     "offers": [("128GB Wi-Fi", 128, 49990), ("256GB Wi-Fi", 256, 56990), ("512GB Wi-Fi", 512, 70990), ("128GB Wi-Fi + Cellular", 128, 59990), ("256GB Wi-Fi + Cellular", 256, 66990), ("512GB Wi-Fi + Cellular", 512, 80990)], "completeOfferSet": True},
    {"model": "iPad Pro M1 (2021)", "url": "https://support.apple.com/en-us/111897", "year": 2021,
     "values": {"chipset": "Apple M1", "cpu": "8-core CPU", "gpu": "8-core Apple GPU", "refreshHz": 120}, "storage": "128GB, 256GB, 512GB, 1TB, or 2TB", "also": ["https://support.apple.com/en-us/111896"]},
    {"model": "iPad Pro M2", "url": "https://support.apple.com/en-us/111842", "year": 2022,
     "values": {"chipset": "Apple M2", "cpu": "8-core CPU", "gpu": "10-core Apple GPU", "refreshHz": 120}, "storage": "128GB, 256GB, 512GB, 1TB, or 2TB", "also": ["https://support.apple.com/en-us/111841"]},
    {"model": "iPad Pro M5", "url": "https://support.apple.com/en-us/125406", "year": 2025,
     "values": {"chipset": "Apple M5", "gpu": "10-core Apple GPU", "refreshHz": 120}, "storage": "256GB, 512GB, 1TB, or 2TB", "also": ["https://support.apple.com/en-us/125407"]},
]


def evidence_row(old: dict, source_by_id: dict) -> dict:
    old_source = source_by_id.get(old.get("sourceId"), {})
    return {"value": old.get("normalizedValue"), "unit": old.get("unit"),
            "sourceUrl": old_source.get("url"), "sourceKind": "superseded secondary review",
            "observedAt": old_source.get("accessDate"), "excerpt": old.get("sourceValue"),
            "configurationMatch": "exact model-level field", "reviewStatus": "SUPERSEDED_BY_MANUFACTURER"}


def upsert_record(manual: dict, device: dict, variant_id: str, model: dict,
                  variant: dict | None = None, price: int | None = None,
                  *, first_for_model: bool = False) -> None:
    key = (device["id"], variant_id)
    review = next((r for r in manual["records"] if (r["deviceId"], r["configurationId"]) == key), None)
    if review is None:
        review = {"deviceId": device["id"], "configurationId": variant_id,
                  "brand": device["brand"], "model": device["model"],
                  "configurationLabel": (variant or {}).get("label") or "Configuration not recorded",
                  "sources": [], "fields": []}
        manual["records"].append(review)

    tech_id = "apple_" + re.sub(r"[^a-z0-9]+", "_", model["model"].lower()).strip("_") + "_tech_specs"
    tech = source(tech_id, "Apple Support", model["url"], "Official manufacturer technical specifications",
                  f"Apple technical specifications for {model['model']} (year introduced: {model['year']}); model-level values do not establish Philippine sales or the workbook's exact storage configuration.")
    sources = [tech]
    for index, url in enumerate(model.get("also", []), 1):
        sources.append(source(tech_id + f"_{index}", "Apple Support", url,
                              "Official technical specifications for the size-specific model family",
                              f"Second Apple size-specific page; cited only to corroborate shared chipset for {model['model']}."))
    store_id = None
    if model.get("store"):
        store_id = tech_id.replace("_tech_specs", "_ph_store")
        sources.append(source(store_id, "Apple Philippines Online Store", model["store"],
                              "Official Philippine product listing, exact storage configurations, and dated list prices",
                              "Apple Philippines online store product options checked on 2026-11-25. Prices are dated observations and color-independent storage tiers; no color-specific variant is created."))
    launch_id = None
    if model.get("launch"):
        url, published, amount = model["launch"]
        launch_id = tech_id.replace("_tech_specs", "_ph_launch")
        sources.append(source(launch_id, "Apple Philippines Newsroom", url,
                              "Official Philippine launch announcement and starting price",
                              "Starting price is tied only to the announcement's stated entry storage. The separate dated Apple Store observation remains the current-price record.",
                              published))

    old_sources = {s["id"]: s for s in review.get("sources", [])}
    for new_source in sources:
        if not any(s.get("id") == new_source["id"] for s in review["sources"]):
            review["sources"].append(new_source)
        if not any(s.get("url") == new_source["url"] for s in device.get("sources", [])):
            device.setdefault("sources", []).append({"organization": new_source["publisher"],
                "url": new_source["url"], "observedAt": new_source["accessDate"],
                "publishedAt": new_source.get("publicationDate"), "purpose": new_source["purpose"],
                "note": new_source["note"]})
    source_map = {s["id"]: s for s in review["sources"]}

    new_fields = []
    mapping = {"displayInches": ("display_size", "in"), "displayType": ("display_technology", None),
               "resolution": ("display_resolution", None), "refreshHz": ("display_refresh_rate", "Hz"),
               "chipset": ("chipset", None), "cpu": ("cpu", None), "gpu": ("gpu", None),
               "ramGb": ("ram_capacity", "GB"),
               "frontCameraMp": ("front_camera", "MP"), "weightG": ("weight", "g"),
               "video": ("video_recording", None), "wifi": ("wifi", None)}
    for catalog_key, value in model["values"].items():
        field_id, unit = mapping[catalog_key]
        row = field(field_id, tech_id, value if unit is None else f"{value} {unit}", value,
                    key=catalog_key, unit=unit,
                    note=f"Official Apple specifications for {model['model']}; this is a model-level fact. The exact workbook variant is {review.get('configurationLabel', 'not recorded')}.")
        if variant:
            row["note"] = "Official Apple model-level specification shared by this exact storage configuration."
        current_variant = variant or next((v for v in device.get("variants", []) if v.get("id") == variant_id), {})
        existing_value = (current_variant.get("specs") or {}).get(catalog_key)
        if existing_value is not None and str(existing_value) != str(value):
            row["replaceExisting"] = True
        new_fields.append(row)

    if model.get("weightByConnectivity"):
        if variant:
            connectivity = "Wi-Fi + Cellular" if "Cellular" in variant.get("label", "") else "Wi-Fi"
            grams = model["weightByConnectivity"][connectivity]
            new_fields.append(field("weight", tech_id, f"{connectivity}: {grams} g", grams,
                key="weightG", unit="g", note=f"Exact Apple store configuration; official technical specifications list {grams} grams for {connectivity}."))
        else:
            weights = model["weightByConnectivity"]
            value = "; ".join(f"{connectivity}: {grams} g" for connectivity, grams in weights.items())
            new_fields.append(field("weight", tech_id, value, value,
                note="Apple lists different weights by connectivity configuration. The inventory does not identify which connectivity option applies.",
                clear_key="weightG"))

    if variant and model.get("cpuByStorage"):
        storage = (variant.get("specs") or {}).get("storageGb")
        match = re.match(r"(\d+)GB", variant.get("label", ""))
        storage = storage or (int(match.group(1)) if match else None)
        cpu = model["cpuByStorage"].get(storage)
        if cpu:
            new_fields.append(field("cpu", tech_id, cpu, cpu, key="cpu",
                note="Storage-dependent CPU configuration stated in Apple's exact-model technical specifications."))

    new_fields.append(field("storage_capacity", tech_id, model["storage"],
        f"Manufacturer model options: {model['storage']}; inventory SKU not recorded.",
        note="Apple lists these model-level storage choices. This does not identify which storage configuration the inventory record represents."))
    new_fields.append(field("battery_capacity", tech_id,
        "Apple's public technical specification page reports runtime, not battery mAh capacity.", None,
        status="NOT_DISCLOSED", note="Not disclosed as an mAh capacity in the cited Apple technical specification; no battery capacity is inferred."))
    new_fields.append(field("philippine_release_date", tech_id,
        f"Apple records worldwide year introduced as {model['year']}; this is not a Philippine first-sale date.", None,
        status="PENDING_VERIFICATION", note="Worldwide model introduction does not establish the first Philippine sale date. Keep the local date unrecorded."))

    if variant and store_id and price is not None:
        storage = (variant.get("specs") or {}).get("storageGb")
        price_row = field("current_price_php", store_id,
            f"Apple PH price for {variant['label']}: PHP {price:,}", price, unit="PHP",
            note="Dated price observed on Apple's Philippine store page for the stated storage/connectivity tier; not a future-price guarantee.",
            price_condition="new", price_type="manufacturer_current_list_price", price_observed=OBSERVED)
        price_row["variantPrice"] = True
        new_fields.append(price_row)
        if storage is not None:
            new_fields.append(field("configuration", store_id, variant["label"], variant["label"],
                note="Exact storage and connectivity label taken from the Apple Philippines store selector."))
            new_fields.append(field("storage_capacity", store_id, f"{storage} GB", storage,
                key="storageGb", unit="GB", note="Exact storage capacity selected in the official Apple Philippines store."))

    if launch_id and variant and price is not None and variant.get("label", "").startswith("256GB"):
        amount = model["launch"][2]
        new_fields.append(field("official_launch_price_php", launch_id,
            f"Philippine launch starting price for 256GB: PHP {amount:,}", amount,
            unit="PHP", note="Historical official Philippine launch starting price for the 256GB entry configuration; current pricing is stored separately."))

    previous_fields = {row.get("fieldId"): i for i, row in enumerate(review.get("fields", []))}
    for row in new_fields:
        old_index = previous_fields.get(row["fieldId"])
        if old_index is not None:
            old = review["fields"][old_index]
            old_value = old.get("normalizedValue")
            new_value = row.get("normalizedValue")
            old_source = source_map.get(old.get("sourceId"), {})
            if (row["fieldId"] == "philippine_release_date"
                    and row.get("status") == "PENDING_VERIFICATION"
                    and old.get("status") in {"VERIFIED", "VERIFIED_SECONDARY"}):
                continue
            if old_value != new_value and old.get("status") in {"VERIFIED", "VERIFIED_SECONDARY"}:
                row.setdefault("candidateEvidence", []).append(evidence_row(old, source_map))
                if row.get("catalogKey"):
                    row["replaceExisting"] = True
            # Keep an exact later price snapshot when the prior observation is
            # newer; otherwise retain the new current Apple store snapshot.
            if row["fieldId"] == "current_price_php" and old.get("priceObservedAt", "") > OBSERVED:
                continue
            review["fields"][old_index] = row
        else:
            review["fields"].append(row)
            previous_fields[row["fieldId"]] = len(review["fields"]) - 1

    if model.get("offers") and first_for_model:
        existing_variant_ids = {v.get("id") for v in device.get("variants", [])}
        all_offers = [{
            "id": config_id(device["id"], label), "label": label,
            "notes": "Official Apple PH option; price observed 2026-11-25."
        } for label, _, _ in model["offers"]]
        has_placeholder = any(v.get("id", "").endswith("-unrecorded") for v in device.get("variants", []))
        if model.get("completeOfferSet") and has_placeholder and not review.get("replacementVariants"):
            review["replacementVariants"] = all_offers
            review["replaceUnrecordedPlaceholder"] = True
        else:
            additions = [item for item in all_offers if item["id"] not in existing_variant_ids]
            if additions:
                review["additionalVariants"] = additions
    if model.get("offers") or model.get("availabilityVerified"):
        review["availabilityEvidence"] = {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Listed by Apple Philippines online store",
            "philippineAvailability": "Official Apple Philippines store listing observed",
            "observedAt": OBSERVED,
            "qualityFlag": "Official Apple PH store listing; first-sale date not established",
        }
        review["openIssues"] = [{"issue": "Philippine launch or first authorized sale date not recorded",
                                 "action": "Use a dated Philippine launch notice or authorized-sale announcement; do not substitute the worldwide model-introduction date."}]


def apply(manual: dict, catalog: list[dict], model: dict, *, category: str) -> int:
    matches = [d for d in catalog if d.get("brand") == "Apple" and d.get("category") == category and d.get("model") == model["model"]]
    if len(matches) != 1:
        raise ValueError(f"Expected one Apple {category} record for {model['model']}; found {len(matches)}")
    device = matches[0]
    original = list(device.get("variants", []))
    if model.get("offers"):
        variants = [{"id": config_id(device["id"], label), "label": label,
                     "specs": {"storageGb": storage},
                     "pricePhp": price, "priceCondition": "new",
                     "priceType": "manufacturer_current_list_price", "priceObservedAt": OBSERVED,
                     "priceSourceUrl": model["store"], "notes": "Official Apple PH price observed 2026-11-25."}
                    for label, storage, price in model["offers"]]
        for index, variant in enumerate(variants):
            upsert_record(manual, device, variant["id"], model, variant, variant["pricePhp"], first_for_model=index == 0)
        return len(model["values"]) * len(variants) + len(variants) * 2
    variant = original[0]
    upsert_record(manual, device, variant["id"], model)
    return len(model["values"])


def deduplicate_apple_reviews(manual: dict, apple_device_ids: set[str]) -> None:
    """Merge historical duplicate Apple rows and prefer direct Apple evidence."""
    grouped: dict[tuple[str, str], list[dict]] = {}
    others = []
    for review in manual["records"]:
        key = (review["deviceId"], review["configurationId"])
        if review["deviceId"] not in apple_device_ids:
            others.append(review)
            continue
        grouped.setdefault(key, []).append(review)

    def rank(row: dict, source_map: dict) -> tuple[int, int, str]:
        status = row.get("status")
        status_rank = {"CONFLICTING_INFORMATION": 6, "VERIFIED": 5,
                       "VERIFIED_SECONDARY": 4, "NOT_DISCLOSED": 4,
                       "UNAVAILABLE_AFTER_RESEARCH": 4, "PENDING_VERIFICATION": 2}.get(status, 1)
        source = source_map.get(row.get("sourceId"), {})
        publisher_rank = 2 if source.get("publisher") in {"Apple Support", "Apple Philippines Online Store", "Apple Philippines Newsroom"} else 0
        return (status_rank, publisher_rank, str(source.get("accessDate") or ""))

    for key, reviews in grouped.items():
        if len(reviews) == 1:
            others.append(reviews[0])
            continue
        merged = dict(reviews[0])
        sources: dict[str, dict] = {}
        for review in reviews:
            for source in review.get("sources", []):
                sources.setdefault(source["id"], source)
        source_map = sources
        fields: dict[str, dict] = {}
        for review in reviews:
            for row in review.get("fields", []):
                field_id = row.get("fieldId")
                current = fields.get(field_id)
                if current is None:
                    fields[field_id] = row
                    continue
                old_rank, new_rank = rank(current, source_map), rank(row, source_map)
                if new_rank > old_rank:
                    chosen, superseded = row, current
                elif new_rank < old_rank:
                    chosen, superseded = current, row
                elif str(current.get("normalizedValue")) == str(row.get("normalizedValue")):
                    chosen, superseded = row, current
                else:
                    current_source = source_map.get(current.get("sourceId"), {})
                    row_source = source_map.get(row.get("sourceId"), {})
                    if row_source.get("publisher", "").startswith("Apple") and not current_source.get("publisher", "").startswith("Apple"):
                        chosen, superseded = row, current
                    elif current_source.get("publisher", "").startswith("Apple") and not row_source.get("publisher", "").startswith("Apple"):
                        chosen, superseded = current, row
                    else:
                        chosen = dict(current)
                        chosen.update({"status": "CONFLICTING_INFORMATION", "normalizedValue": None,
                                       "note": "Separate reviewed sources disagree; value withheld pending reconciliation."})
                        if chosen.get("catalogKey"):
                            chosen["catalogValue"] = None
                            chosen["replaceExisting"] = True
                        chosen["candidateEvidence"] = [
                            *current.get("candidateEvidence", []), *row.get("candidateEvidence", []),
                            evidence_row(current, source_map), evidence_row(row, source_map),
                        ]
                        fields[field_id] = chosen
                        continue
                if superseded.get("normalizedValue") != chosen.get("normalizedValue"):
                    chosen = dict(chosen)
                    chosen["candidateEvidence"] = [*chosen.get("candidateEvidence", []), evidence_row(superseded, source_map)]
                    if chosen.get("catalogKey"):
                        chosen["replaceExisting"] = True
                fields[field_id] = chosen
        merged["sources"] = list(sources.values())
        merged["fields"] = list(fields.values())
        for property_name in ("replacementVariants", "replaceUnrecordedPlaceholder", "additionalVariants", "availabilityEvidence", "openIssues"):
            value = next((r.get(property_name) for r in reversed(reviews) if r.get(property_name)), None)
            if value is not None:
                merged[property_name] = value
        others.append(merged)
    manual["records"] = others
    for review in manual["records"]:
        if review.get("deviceId") not in apple_device_ids:
            continue
        replacement_ids = {item.get("id") for item in review.get("replacementVariants", [])}
        if replacement_ids and review.get("additionalVariants"):
            remaining = [item for item in review["additionalVariants"] if item.get("id") not in replacement_ids]
            if remaining:
                review["additionalVariants"] = remaining
            else:
                review.pop("additionalVariants", None)


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    updated = 0
    reviewed_models = 0
    for model in MODELS:
        updated += apply(manual, catalog, model, category="smartphones")
        reviewed_models += 1
    for model in TABLETS:
        updated += apply(manual, catalog, model, category="tablets")
        reviewed_models += 1
    apple_ids = {d["id"] for d in catalog if d.get("brand") == "Apple" and d.get("category") in {"smartphones", "tablets"}}
    deduplicate_apple_reviews(manual, apple_ids)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"appleModelsReviewed": reviewed_models,
                      "newOrUpdatedFieldRows": updated,
                      "currentStoreModels": sum(bool(x.get("offers")) for x in [*MODELS, *TABLETS]),
                      "manualRecords": len(manual["records"])}, indent=2))


if __name__ == "__main__":
    main()
