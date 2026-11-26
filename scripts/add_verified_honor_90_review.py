#!/usr/bin/env python3
"""Record the source-matched Philippine HONOR 90 5G configuration."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-90-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_1298822c3211ec"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-12gb-512gb-ph"
URL_HONOR = "https://www.honor.com/ph/phones/honor-90/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/honor-90-5g"
URL_YUGA = "https://www.yugatech.com/news/honor-90-5g-price-philippines/"
IMAGE_URL = "https://www.pinoytechnoguide.com/wp-content/uploads/2023/08/HONOR-90-5G.jpg.webp"


def field(fid: str, source_id: str, value, normalized_value, *, key=None, unit=None,
          status="VERIFIED_SECONDARY", note: str, config_match="Exact Philippine 12 GB / 512 GB configuration") -> dict:
    row = {
        "fieldId": fid, "status": status, "sourceId": source_id,
        "sourceValue": value, "normalizedValue": normalized_value,
        "note": note, "configurationMatch": config_match,
    }
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized_value
    if unit:
        row["unit"] = unit
    return row


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device or device.get("brand", "").casefold() != "honor" or device.get("model") != "90":
        raise ValueError("The source record no longer matches the HONOR 90 workbook identity")
    reviews = [row for row in manual.get("records", []) if row.get("deviceId") == DEVICE]
    if len(reviews) != 1 or reviews[0].get("configurationId") != OLD_CONFIG:
        raise ValueError(f"Expected one exact-page review on the blank configuration; found {len(reviews)}")
    review = reviews[0]

    ptg = next((source for source in review.get("sources", []) if source.get("url") == URL_PTG), None)
    if not ptg:
        raise ValueError("Exact HONOR 90 5G Philippine page is missing from the review")
    ptg.update({
        "publisher": "Pinoy Techno Guide", "publicationDate": "2023-08-15",
        "purpose": "Exact Philippine model, configuration, specifications, preorder date, and price reference",
        "note": "The exact HONOR 90 5G Philippine page identifies the 12 GB / 512 GB configuration, states the PHP 24,990 official price, and reports preorders from 2023-08-16 through 2023-08-25. The reported preorder start is recorded separately from a retail first-sale date.",
    })
    sources = [
        {
            "id": "honor90_ph_official_product", "publisher": "HONOR Philippines",
            "url": URL_HONOR, "publicationDate": None, "accessDate": OBSERVED,
            "purpose": "Manufacturer model identity and cross-check of product features",
            "note": "HONOR Philippines identifies the product as HONOR 90 and describes its 200 MP rear camera, 50 MP selfie camera, 5000 mAh battery, and up to 66 W charging. Local configuration, preorder dates, and historical price are documented by Philippine sources.",
        },
        {
            "id": "honor90_ph_launch_yugatech", "publisher": "YugaTech",
            "url": URL_YUGA, "publicationDate": "2023-08-15", "accessDate": OBSERVED,
            "purpose": "Contemporaneous Philippine launch, configuration, and price cross-check",
            "note": "YugaTech reports the HONOR 90 5G Philippine launch, 12 GB RAM plus 7 GB RAM Turbo, 512 GB storage, PHP 24,990 suggested retail price, and early-bird preorder from Aug 16–25, 2023.",
        },
    ]
    for source in sources:
        if not any(old.get("url") == source["url"] for old in review.get("sources", [])):
            review.setdefault("sources", []).append(source)
    ptg_id = ptg["id"]
    yuga_id = "honor90_ph_launch_yugatech"

    review["configurationId"] = CONFIG
    review["configuration"] = "12 GB RAM / 512 GB storage"
    review["configurationLabel"] = "12 GB RAM / 512 GB storage"
    review["replacementVariants"] = [{
        "id": CONFIG, "label": "12 GB RAM / 512 GB storage",
        "sku": None, "modelCode": None,
        "notes": "Pinoy Techno Guide and YugaTech both identify the Philippine 12 GB RAM / 512 GB storage configuration. YugaTech reports an additional 7 GB RAM Turbo feature; it is not counted as physical RAM. No Philippine SKU is recorded.",
    }]
    review["replaceUnrecordedPlaceholder"] = True

    overrides = {
        "cpu": ("Octa-core: 1 × Cortex-A710 at 2.5 GHz + 3 × Cortex-A710 at 2.36 GHz + 4 × Cortex-A510 at 1.8 GHz", "Octa-core: 1 × Cortex-A710 at 2.5 GHz + 3 × Cortex-A710 at 2.36 GHz + 4 × Cortex-A510 at 1.8 GHz"),
        "ultrawide_camera": ("12 MP ultra-wide/macro camera, f/2.2, autofocus, 112° FoV", "12 MP ultra-wide/macro camera, f/2.2, autofocus, 112° FoV"),
        "audio": ("HONOR Histen effects; USB Type-C audio output", "HONOR Histen effects; USB Type-C audio output"),
        "wired_charging": ("66 W HONOR SuperCharge; source reports 20% charge in 5 minutes", 66),
    }
    for item in review["fields"]:
        fid = item.get("fieldId")
        if fid in overrides:
            source_value, normalized_value = overrides[fid]
            item["sourceValue"] = source_value
            item["normalizedValue"] = normalized_value
            item["note"] = "Value is normalized from the exact Philippine product page; the source's stated specification is preserved without adding an unsupported variant detail."
            if item.get("catalogKey"):
                item["catalogValue"] = normalized_value
            if fid == "wired_charging":
                item["catalogKey"] = "chargingW"
                item["catalogValue"] = 66
                item["unit"] = "W"
        elif fid == "main_camera_sensor":
            item["status"] = "PENDING_VERIFICATION"
            item["sourceValue"] = "The page specifies a 200 MP main camera but does not identify its sensor model."
            item["normalizedValue"] = None
            item.pop("catalogKey", None)
            item.pop("catalogValue", None)
            item["note"] = "A camera resolution does not identify its sensor model. Keep the sensor identity unrecorded until a source names the sensor."
    reviewed_ids = {item.get("fieldId") for item in review["fields"]}
    review["fields"].extend([
        field("ram_capacity", ptg_id, "12 GB physical RAM; +7 GB RAM Turbo is listed separately", 12, key="ramGb", unit="GB", note="Philippine reference lists 12 GB RAM and separately lists 7 GB RAM Turbo. Only the physical 12 GB is counted."),
        field("storage_capacity", ptg_id, "512 GB", 512, key="storageGb", unit="GB", note="Exact Philippine HONOR 90 5G page lists 512 GB internal storage."),
        field("operating_system", ptg_id, "Android 13 with MagicOS 7.1", "Android 13 with MagicOS 7.1", key="os", note="Exact Philippine product page specification."),
        field("rear_camera_system", ptg_id, "200 MP main (f/1.9, autofocus) + 12 MP ultra-wide/macro (f/2.2, autofocus, 112° FoV) + 2 MP depth; LED flash", "200 MP main + 12 MP ultra-wide/macro + 2 MP depth", note="Camera modules are transcribed from the exact Philippine specification page."),
        field("telephoto_camera", ptg_id, "The page lists main, ultra-wide/macro, and depth modules; no telephoto module is listed.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE", note="The exact model page enumerates the three rear modules without a telephoto camera."),
        field("sim_esim", ptg_id, "Dual Nano-SIM", "Dual Nano-SIM", note="Exact Philippine HONOR 90 5G page lists dual Nano-SIM."),
        field("official_launch_price_php", yuga_id, "PHP 24,990 suggested retail price, reported 2023-08-15", 24990, unit="PHP", note="Historical Philippine launch-era price only; not represented as a current offer."),
        field("philippine_release_date", ptg_id, "Preorders from 2023-08-16 to 2023-08-25; announced 2023-08-15", "2023-08-16", note="First documented Philippine preorder date. It is not described as the first retail sale date."),
    ])
    if "main_camera_sensor" not in reviewed_ids:
        review["fields"].append(field("main_camera_sensor", ptg_id, "200 MP main camera; sensor model not stated", None, status="PENDING_VERIFICATION", note="The page reports camera resolution but does not identify the sensor model."))

    review["availabilityEvidence"] = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Official Philippine launch was reported on 2023-08-15; preorders began 2023-08-16. Current stock is not established.",
        "philippineAvailability": "Pinoy Techno Guide reported preorders from 2023-08-16 through 2023-08-25 in HONOR stores and official online shops. YugaTech independently reported the Philippine launch and the same configuration and price.",
        "observedAt": OBSERVED,
        "manufacturer": "HONOR",
        "productLine": "N Series",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Philippine preorder start",
        "researchNotes": "The inventory label '90' matches the manufacturer name HONOR 90 and Philippine model HONOR 90 5G. The documented Philippine configuration is 12 GB physical RAM / 512 GB storage. The 7 GB RAM Turbo feature is not counted as physical RAM. PHP 24,990 is launch-era price evidence; no current price or stock is verified.",
        "qualityFlag": "No Philippine SKU recorded; launch-era price is not current",
        "openIssues": [
            {"issue": "Exact Philippine SKU/model code is not recorded", "action": "Keep SKU and model code blank until an exact source lists them."},
            {"issue": "Current retail price and stock are not verified", "action": "Keep the 2023 PHP 24,990 price as historical evidence, not a current offer."},
            {"issue": "The 200 MP camera sensor model is not named", "action": "Keep sensor identity pending; do not substitute a guessed sensor."},
            {"issue": "Image reuse rights are not established", "action": "Continue showing the neutral placeholder."},
        ],
    }
    manual["reviewedAt"] = OBSERVED

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR 90 5G image was identified on the Philippine source page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_PTG,
        "assetUrl": IMAGE_URL,
        "scope": "Exact model; configuration not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR 90",
    }
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "90", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [{
            "device_id": DEVICE, "amount_php": 24990,
            "configuration_id": CONFIG, "configuration_match": "exact",
            "variant_ram_gb": 12, "variant_storage_gb": 512,
            "price_type": "independent_reported_official_price",
            "source_published_at": "2023-08-15",
            "excerpt": "YugaTech's Philippine launch report identifies HONOR 90 5G at 12 GB RAM / 512 GB and PHP 24,990; dated 2023-08-15. Historical, not current.",
            "source_url": URL_YUGA, "source_kind": "independent_ph_reference",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
        }],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "modelMatch": "HONOR 90 5G matched to inventory label 90",
        "configuration": "12 GB / 512 GB",
        "manualFields": len(review["fields"]),
        "preorderStart": "2023-08-16",
        "historicalPricePhp": 24990,
        "priceLoadedAsCurrent": False,
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
