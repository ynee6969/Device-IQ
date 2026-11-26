#!/usr/bin/env python3
"""Record the reviewed Philippine itel S23+ model alias and configuration."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-26"
DEVICE = "device_a8c831d7277179"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-s23-plus-8gb-256gb-ph"
PTG_URL = "https://www.pinoytechnoguide.com/smartphones/itel-s23-plus"
ITEL_URL = "https://www.itel-life.com/products/phone/s-series/s23plus/spec"
IMAGE_URL = "https://www.pinoytechnoguide.com/wp-content/uploads/2023/10/itel-S23-Plus-large.jpg"


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device:
        raise ValueError(f"Unknown inventory model: {DEVICE}")
    if device.get("model") != "S23 Plus" or device.get("brand", "").casefold() != "itel":
        raise ValueError("The source record no longer matches the reviewed workbook identity")

    rows = [row for row in manual.get("records", []) if row.get("deviceId") == DEVICE]
    if len(rows) != 1:
        raise ValueError(f"Expected one reviewed row for {DEVICE}, found {len(rows)}")
    review = rows[0]
    if review.get("configurationId") not in {OLD_CONFIG, CONFIG}:
        raise ValueError(f"Unexpected configuration identifier: {review.get('configurationId')}")

    ptg_source = next((source for source in review.get("sources", []) if source.get("url") == PTG_URL), None)
    if not ptg_source:
        raise ValueError("The exact Philippine source was not found in the reviewed model record")
    ptg_source.update({
        "publisher": "Pinoy Techno Guide",
        "publicationDate": "2023-10-06",
        "purpose": "Philippine model, configuration, price, availability, and technical reference",
        "note": "The exact itel S23+ Philippine page lists 8 GB RAM and 256 GB storage, reports PHP 7,499 as its official price, and says the phone is available through itel stores, authorized dealers, and itel's official Philippine online shops. This is a dated secondary report; it does not establish current stock or the exact first-sale date.",
    })
    itel_source = {
        "id": "itel_s23plus_official_specification",
        "publisher": "itel",
        "url": ITEL_URL,
        "publicationDate": None,
        "accessDate": OBSERVED,
        "purpose": "Official model identity and model-level specification cross-check",
        "note": "The manufacturer markets this model as itel S23+. Its product specification page lists 6.78-inch AMOLED, 5000 mAh, and 256+16 (8+8) GB memory. This confirms that the workbook label 'S23 Plus' is the same model; it does not establish Philippine launch timing or a local price.",
    }
    if not any(source.get("url") == ITEL_URL for source in review.get("sources", [])):
        review.setdefault("sources", []).append(itel_source)

    review["configurationId"] = CONFIG
    review["configuration"] = "8 GB RAM / 256 GB storage"
    review["configurationLabel"] = "8 GB RAM / 256 GB storage"
    review["replacementVariants"] = [{
        "id": CONFIG,
        "label": "8 GB RAM / 256 GB storage",
        "sku": None,
        "modelCode": None,
        "notes": "The Philippine reference lists 8 GB RAM and 256 GB storage. The manufacturer page independently lists 256+16 (8+8) GB memory. No Philippine SKU is recorded.",
    }]
    review["replaceUnrecordedPlaceholder"] = True
    review["fields"] = [
        field for field in review.get("fields", [])
        if field.get("fieldId") not in {"ram_capacity", "storage_capacity"}
    ]
    review["fields"].extend([
        {
            "fieldId": "ram_capacity", "status": "VERIFIED_SECONDARY",
            "sourceId": ptg_source["id"], "sourceValue": "8 GB RAM",
            "normalizedValue": 8, "catalogKey": "ramGb", "catalogValue": 8,
            "unit": "GB", "configurationMatch": "Exact Philippine configuration listed on source page",
            "note": "Pinoy Techno Guide lists 8 GB RAM; itel's product page describes 256+16 (8+8) GB memory. RAM type is not stated.",
        },
        {
            "fieldId": "storage_capacity", "status": "VERIFIED_SECONDARY",
            "sourceId": ptg_source["id"], "sourceValue": "256 GB",
            "normalizedValue": 256, "catalogKey": "storageGb", "catalogValue": 256,
            "unit": "GB", "configurationMatch": "Exact Philippine configuration listed on source page",
            "note": "Pinoy Techno Guide lists 256 GB storage; itel's product page lists 256 GB in its 256+16 (8+8) GB memory description.",
        },
    ])
    readable_values = {
        "cpu": "Octa-core CPU: 2 × Cortex-A75 at 2.0 GHz + 6 × Cortex-A55 at 1.8 GHz",
        "rear_camera_system": "Dual rear cameras: 50 MP main camera (f/1.6, autofocus) + VGA secondary camera; LED flash; video recording up to 1080p",
        "audio": "DTS Audio; USB Type-C audio output",
    }
    for field in review["fields"]:
        if field.get("fieldId") in readable_values:
            value = readable_values[field["fieldId"]]
            field["sourceValue"] = value
            field["normalizedValue"] = value
            if field.get("catalogKey"):
                field["catalogValue"] = value
            field["note"] = "Spacing and line breaks are normalized from the exact Philippine source page for readability; the specifications are unchanged."
        elif field.get("fieldId") == "main_camera_sensor":
            field["status"] = "PENDING_VERIFICATION"
            field["sourceValue"] = "The page lists a 50 MP main camera but does not name its sensor model."
            field["normalizedValue"] = None
            field.pop("catalogValue", None)
            field.pop("catalogKey", None)
            field["note"] = "A camera resolution is not a sensor model. Keep the sensor identity unrecorded until a source names the sensor."
    review["availabilityEvidence"] = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "A dated Philippine report said the model was available through itel stores, authorized dealers, and official online shops as of October 2023; current stock is not established.",
        "philippineAvailability": "Pinoy Techno Guide reported Philippine channel availability for the exact itel S23+ model on 2023-10-06. The exact first-sale date and current availability are not recorded.",
        "observedAt": OBSERVED,
        "manufacturer": "itel",
        "productLine": "S Series",
        "modelNumber": None,
        "philippineReleaseYear": 2023,
        "researchNotes": "The workbook label 'S23 Plus' matches the manufacturer name 'S23+' and the exact Philippine reference page. Philippine availability is evidenced by a dated report, but no exact release date or current stock is established. PHP 7,499 remains a dated, configuration-unmatched price candidate; it is not shown as a current offer.",
        "qualityFlag": "No exact Philippine SKU or first-sale date; 2023 price is not confirmed current",
        "openIssues": [
            {"issue": "Exact Philippine first-sale date and SKU are not recorded", "action": "Keep the release date blank and retain the source-backed 8 GB / 256 GB configuration without inventing a SKU."},
            {"issue": "The PHP 7,499 report does not explicitly bind price to the 8 GB / 256 GB variant", "action": "Keep it as a dated, configuration-unmatched candidate; do not display it as current price."},
            {"issue": "Product image reuse rights are not established", "action": "Continue showing the neutral image placeholder until reuse permission or a reusable license is documented."},
        ],
    }

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact itel S23+ product image was identified, but no reusable license or written permission is recorded.",
        "sourcePage": PTG_URL,
        "assetUrl": IMAGE_URL,
        "scope": "Exact model; configuration not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for itel S23+",
    }
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "model": "itel S23+ (inventory label: S23 Plus)",
        "configuration": "8 GB RAM / 256 GB storage",
        "modelLevelFields": len(review["fields"]),
        "availability": "historically verified; exact date and current stock not recorded",
        "price": "PHP 7,499 dated candidate; exact configuration match not established",
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
