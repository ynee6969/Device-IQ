#!/usr/bin/env python3
"""Record the source-matched Philippine HONOR X9b 5G configuration."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-x9b-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_38ef56f303cc59"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-12gb-256gb-ph"

URL_HONOR = "https://www.honor.com/ph/phones/honor-x9b/"
URL_HONOR_SPECS = "https://www.honor.com/ph/phones/honor-x9b/spec/"
URL_YUGA = "https://www.yugatech.com/news/honor-x9b-5g-specs-price-philippines/"
URL_YUGA_PRICE_LIST = "https://www.yugatech.com/honor-phone-price-list-philippines/"
URL_PTG = "https://www.pinoytechnoguide.com/reviews/honor-x9b-5g"
IMAGE_URL = "https://www-file.honor.com/content/dam/honor/ph/specs/smartphone/honor-x9b/honor-x9b-spec-orange.png"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {
        "id": sid, "publisher": publisher, "url": url,
        "publicationDate": publication_date, "accessDate": OBSERVED,
        "purpose": purpose, "note": note,
    }


def field(fid: str, source_id: str, value, normalized_value, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, configuration_match="Model-level source; Philippine configuration 12 GB RAM / 256 GB storage") -> dict:
    row = {
        "fieldId": fid, "status": status, "sourceId": source_id,
        "sourceValue": value, "normalizedValue": normalized_value,
        "note": note, "configurationMatch": configuration_match,
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
    if not device or device.get("category") != "smartphones" or device.get("brand", "").casefold() != "honor" or device.get("model") != "X9b":
        raise ValueError("The source record no longer matches the HONOR X9b workbook identity")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR X9b already has a manual review; inspect it before replacing")

    sources = [
        source(
            "honor_x9b_ph_official_product", "HONOR Philippines", URL_HONOR,
            "Official Philippine product identity and model-family reference",
            "HONOR Philippines identifies the product as HONOR X9b 5G. This official product page corroborates model identity; the accessible page text does not expose a complete specification table.",
        ),
        source(
            "honor_x9b_ph_official_specs", "HONOR Philippines", URL_HONOR_SPECS,
            "Official Philippine model specification page and product imagery",
            "The official Philippines specifications page identifies HONOR X9b and presents its color variants. Its text rendering does not expose the specification values, so values below are attributed to the contemporaneous Philippine reporting that prints them.",
        ),
        source(
            "honor_x9b_ph_launch_yugatech", "YugaTech", URL_YUGA,
            "Contemporaneous Philippine launch, exact configuration, specifications, preorder date, and price",
            "Published 2024-01-12. Reports the HONOR X9b 5G Philippine preorder from January 12–19 at PHP 16,999 and identifies a 12 GB RAM / 256 GB storage configuration with detailed specifications.",
            "2024-01-12",
        ),
        source(
            "honor_x9b_ph_price_history_yugatech", "YugaTech", URL_YUGA_PRICE_LIST,
            "Dated Philippine price-history cross-check",
            "The HONOR phone price-list row identifies HONOR X9b 5G at PHP 16,999 and marks the entry verified January 13, 2024. This is historical launch-era evidence, not a current offer.",
        ),
        source(
            "honor_x9b_ph_review_ptg", "Pinoy Techno Guide", URL_PTG,
            "Independent Philippine hands-on review and specification cross-check",
            "Published 2024-01-22. The review identifies the HONOR X9b 5G, lists 12 GB RAM / 256 GB storage, and reports the Philippine official price as PHP 16,999. It also describes the tested device and its features.",
            "2024-01-22",
        ),
    ]
    honor_id = "honor_x9b_ph_official_product"
    yuga_id = "honor_x9b_ph_launch_yugatech"
    price_id = "honor_x9b_ph_price_history_yugatech"
    ptg_id = "honor_x9b_ph_review_ptg"

    fields = [
        field("model_number", yuga_id, "No Philippine SKU or model code stated", None,
              status="NOT_DISCLOSED", note="The Philippine launch and manufacturer pages reviewed identify the marketing model but do not expose a Philippine SKU/model code."),
        field("configuration", yuga_id, "12 GB RAM / 256 GB storage", "12 GB RAM / 256 GB storage",
              status="VERIFIED_SECONDARY", note="YugaTech's contemporaneous Philippine launch report gives this exact configuration; PTG's Philippine review independently lists the same RAM and storage."),
        field("philippine_release_date", yuga_id, "Preorders ran January 12–19, 2024", "2024-01-12",
              note="This is the first documented Philippine preorder date, not a separately verified first retail-sale date."),
        field("official_launch_price_php", yuga_id, "PHP 16,999 preorder price, reported 2024-01-12", 16999,
              unit="PHP", note="Historical Philippine preorder/launch-era price for the reported 12 GB / 256 GB configuration; not a current offer."),
        field("current_price_php", price_id, "The listed PHP 16,999 entry is dated January 13, 2024; no current dated offer is supplied", None,
              status="NOT_DISCLOSED", unit="PHP", note="The accessible price history is explicitly dated 2024. No current Philippine price observation is inferred from it."),
        field("display_size", yuga_id, "6.78 inches", 6.78, key="displayInches", unit="in", note="YugaTech's Philippine specification list."),
        field("display_technology", yuga_id, "AMOLED", "AMOLED", key="displayType", note="YugaTech's Philippine specification list."),
        field("display_resolution", yuga_id, "1200 × 2652 pixels; 1.5K", "1200 x 2652", key="resolution", note="YugaTech's Philippine specification list."),
        field("display_refresh_rate", yuga_id, "120 Hz", 120, key="refreshHz", unit="Hz", note="YugaTech's Philippine specification list."),
        field("display_brightness", yuga_id, "1200 nits peak", 1200, unit="nits", note="The source labels 1200 nits as peak brightness."),
        field("display_protection", yuga_id, "Ultra-Bounce Anti-Drop Display; source reports SGS 5-Star Overall Drop Resistance certification", "Ultra-Bounce Anti-Drop Display; SGS 5-Star Overall Drop Resistance reported", note="Retains the source's marketing/certification wording without inferring a glass material or guaranteeing drop outcomes."),
        field("chipset", yuga_id, "Qualcomm Snapdragon 6 Gen 1", "Qualcomm Snapdragon 6 Gen 1", key="chipset", note="YugaTech's Philippine specification list."),
        field("cpu", yuga_id, "Octa-core, up to 2.2 GHz", "Octa-core, up to 2.2 GHz", key="cpu", note="YugaTech gives the core count and maximum clock; individual core layout is not supplied."),
        field("gpu", yuga_id, "Adreno A710", "Adreno A710", key="gpu", note="YugaTech's Philippine specification list."),
        field("operating_system", yuga_id, "MagicOS 7.2 based on Android 13", "MagicOS 7.2 (Android 13)", key="os", note="Software version reported at Philippine launch; later updates are not inferred."),
        field("ram_capacity", yuga_id, "12 GB RAM", 12, key="ramGb", unit="GB", note="Exact Philippine launch configuration. No virtual RAM is added to the physical RAM figure."),
        field("ram_type", yuga_id, "RAM type not listed", None, status="NOT_DISCLOSED", note="The source reports capacity but not memory technology."),
        field("storage_capacity", yuga_id, "256 GB storage", 256, key="storageGb", unit="GB", note="Exact Philippine launch configuration."),
        field("storage_type", yuga_id, "Storage technology not listed", None, status="NOT_DISCLOSED", note="The reviewed Philippine sources do not identify eMMC/UFS storage type."),
        field("storage_expansion", yuga_id, "Storage expansion support not listed", None, status="NOT_DISCLOSED", note="No expansion information is stated in the reviewed launch specification."),
        field("rear_camera_system", yuga_id, "108 MP f/1.75 main + 5 MP f/2.2 wide/depth + 2 MP f/2.4 macro", "108 MP main + 5 MP wide/depth + 2 MP macro", note="Module roles and apertures follow YugaTech's launch specification."),
        field("main_camera_sensor", yuga_id, "108 MP main camera; sensor model not stated", None, status="NOT_DISCLOSED", note="Resolution does not identify the camera sensor model."),
        field("ultrawide_camera", yuga_id, "5 MP f/2.2 wide/depth camera", "5 MP wide/depth", note="The source combines the wide and depth role; it does not support describing this as a dedicated ultra-wide-only module."),
        field("telephoto_camera", yuga_id, "The listed rear system consists of main, wide/depth, and macro modules; no telephoto module is listed", "No dedicated telephoto module listed", status="NOT_APPLICABLE", note="The source enumerates the complete triple-rear-camera system without a telephoto module."),
        field("front_camera", yuga_id, "16 MP f/2.45", 16, key="frontCameraMp", unit="MP", note="YugaTech's Philippine specification list."),
        field("video_recording", yuga_id, "Video recording modes not listed", None, status="NOT_DISCLOSED", note="No video resolution/frame-rate modes are provided in the reviewed launch specification."),
        field("battery_capacity", yuga_id, "5800 mAh", 5800, key="batteryMah", unit="mAh", note="YugaTech's Philippine specification list."),
        field("battery_technology", yuga_id, "Battery chemistry not listed", None, status="NOT_DISCLOSED", note="The reviewed sources state capacity but not cell chemistry or rated/typical distinction."),
        field("wired_charging", yuga_id, "35 W", 35, key="chargingW", unit="W", note="YugaTech's Philippine specification list."),
        field("wireless_charging", yuga_id, "Wireless charging not listed", None, status="NOT_DISCLOSED", note="Wireless or reverse charging is not specified in the reviewed sources."),
        field("dimensions", yuga_id, "163.6 × 75.5 × 7.98 mm", "163.6 x 75.5 x 7.98 mm", key="dimensions", unit="mm", note="YugaTech's Philippine specification list."),
        field("weight", yuga_id, "185 g", 185, key="weightG", unit="g", note="YugaTech's Philippine specification list."),
        field("materials", yuga_id, "Sunrise Orange is identified as vegan leather; materials for other colors not stated", "Sunrise Orange variant: vegan leather back; other color materials not recorded", note="Color-specific material information is not generalized to every unit or variant."),
        field("ingress_protection", yuga_id, "IP53 splash and dust resistance", "IP53", note="Rating reported by YugaTech; it does not imply water immersion resistance."),
        field("sim_esim", yuga_id, "Dual Nano-SIM", "Dual Nano-SIM", note="YugaTech's Philippine specification list."),
        field("cellular_bands", yuga_id, "5G and 4G LTE; specific bands not listed", "5G NR and 4G LTE; bands not recorded", key="cellular", note="Network generations are listed; no Philippine band mapping is inferred."),
        field("wifi", yuga_id, "802.11 a/b/g/n/ac", "802.11 a/b/g/n/ac", key="wifi", note="YugaTech's Philippine specification list."),
        field("bluetooth", yuga_id, "Bluetooth 5.1", "Bluetooth 5.1", note="YugaTech's Philippine specification list."),
        field("usb", yuga_id, "USB Type-C", "USB Type-C", key="ports", note="YugaTech's Philippine specification list; transfer speed is not stated."),
        field("nfc", yuga_id, "NFC", "Yes", note="YugaTech lists NFC support."),
        field("gnss", yuga_id, "GPS, A-GPS, GLONASS, BeiDou, Galileo", "GPS, A-GPS, GLONASS, BeiDou, Galileo", note="YugaTech's Philippine specification list."),
        field("audio", ptg_id, "No stereo loudspeakers (PTG review observation)", "No stereo loudspeakers reported", note="A hands-on review reports no stereo loudspeakers; speaker hardware details are otherwise not expanded."),
        field("sensors", yuga_id, "Sensor list not provided", None, status="NOT_DISCLOSED", note="No complete sensor list is present in the reviewed launch sources."),
    ]

    review = {
        "deviceId": DEVICE, "configurationId": CONFIG,
        "brand": "HONOR", "model": "X9b",
        "configuration": "12 GB RAM / 256 GB storage",
        "configurationLabel": "12 GB RAM / 256 GB storage",
        "sources": sources, "fields": fields,
        "replacementVariants": [{
            "id": CONFIG, "label": "12 GB RAM / 256 GB storage",
            "sku": None, "modelCode": None,
            "notes": "YugaTech's contemporaneous Philippine launch report and Pinoy Techno Guide's local review identify the 12 GB RAM / 256 GB configuration. No Philippine SKU or model code is recorded.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine preorder was reported January 12–19, 2024; current stock is not established.",
            "philippineAvailability": "YugaTech reported preorders through HONOR Experience/Partner Stores and official online shops beginning January 12, 2024.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "X Series",
            "philippineReleaseYear": 2024,
            "philippineDateLabel": "Philippine preorder start",
            "researchNotes": "The inventory label HONOR X9b matches the official HONOR Philippines product and Philippine HONOR X9b 5G reports. The documented local configuration is 12 GB RAM / 256 GB storage. PHP 16,999 and January 12, 2024 are historical preorder evidence, not a current price or retail first-sale date.",
            "qualityFlag": "Exact local SKU and retail first-sale date not recorded; price is historical",
            "openIssues": [
                {"issue": "Exact Philippine SKU/model code is not recorded", "action": "Keep SKU/model code blank until a source names it."},
                {"issue": "Current retail price and stock are not verified", "action": "Retain PHP 16,999 as launch-era evidence only; do not show it as a current offer."},
                {"issue": "Some detailed specifications are not disclosed in the reviewed sources", "action": "Keep unlisted CPU layout, memory/storage type, camera sensor model, video modes, battery chemistry, and sensors not recorded."},
                {"issue": "Exact retail first-sale date is not recorded", "action": "Label January 12, 2024 as preorder start only."},
                {"issue": "Official product image reuse terms are not established", "action": "Continue showing the neutral placeholder until image-use rights are confirmed."},
            ],
        },
    }

    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR X9b Sunrise Orange product image was identified on the official HONOR Philippines specification page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_HONOR_SPECS,
        "assetUrl": IMAGE_URL,
        "scope": "Exact HONOR X9b model, Sunrise Orange color variant; RAM/storage configuration is not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR X9b",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "X9b", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [{
            "device_id": DEVICE, "amount_php": 16999,
            "configuration_id": CONFIG, "configuration_match": "exact",
            "variant_ram_gb": 12, "variant_storage_gb": 256,
            "price_type": "independent_reported_historical_price",
            "source_published_at": "2024-01-12",
            "excerpt": "YugaTech's Philippine launch report identifies HONOR X9b 5G at 12 GB RAM / 256 GB storage and PHP 16,999 during preorders starting January 12, 2024. Historical, not current.",
            "source_url": URL_YUGA, "source_kind": "independent_ph_reference",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
        }],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "HONOR X9b inventory record matched to HONOR X9b 5G Philippine product",
        "configuration": "12 GB / 256 GB",
        "reviewedFields": len(fields),
        "preorderStart": "2024-01-12",
        "historicalPricePhp": 16999,
        "priceLoadedAsCurrent": False,
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
