#!/usr/bin/env python3
"""Record exact Philippine HONOR 70 configuration and dated source evidence."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-70-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_5317d55fb742f4"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-8gb-256gb-ph"
URL_HONOR = "https://www.honor.com/ph/phones/honor-70/spec/"
URL_GADGETMATCH = "https://www.gadgetmatch.com/honor-70-price-availability-philippines/"
URL_YUGATECH = "https://www.yugatech.com/honor-gadget-price-list-philippines"
IMAGE_URL = "https://www-file.honor.com/content/dam/honor/ph/specs/smartphone/honor-70/spec/honor-70-white.png"


def field(fid: str, source_id: str, value, normalized_value, *, key=None, unit=None,
          status="VERIFIED", note: str, config_match="Exact 8 GB / 256 GB Philippine configuration") -> dict:
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
    if not device or device.get("brand", "").casefold() != "honor" or device.get("model") != "70":
        raise ValueError("The source record no longer matches the HONOR 70 workbook identity")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR 70 already has a manual review; inspect it before replacing")

    sources = [
        {
            "id": "honor70_ph_official_specs", "publisher": "HONOR Philippines",
            "url": URL_HONOR, "publicationDate": None, "accessDate": OBSERVED,
            "purpose": "Official Philippine model and 8 GB / 256 GB specification reference",
            "note": "The official HONOR Philippines page identifies HONOR 70, lists 8 GB + 256 GB memory, and provides the model's display, chipset, camera, battery, connectivity, and dimension specifications. It does not establish the exact local first-sale date or a current retail price.",
        },
        {
            "id": "honor70_ph_launch_gadgetmatch", "publisher": "GadgetMatch",
            "url": URL_GADGETMATCH, "publicationDate": "2022-10-19", "accessDate": OBSERVED,
            "purpose": "Contemporaneous Philippine availability and retail-price reference",
            "note": "GadgetMatch reported on 2022-10-19 that HONOR 70 5G was in the Philippines, available in HONOR stores and Lazada nationwide, with a PHP 26,990 retail price. This establishes availability by that report date, not the exact first sale or current stock.",
        },
        {
            "id": "honor70_ph_launch_price_yugatech", "publisher": "YugaTech",
            "url": URL_YUGATECH, "publicationDate": None, "accessDate": OBSERVED,
            "purpose": "Dated Philippine configuration and price-history reference",
            "note": "YugaTech's HONOR price list records HONOR 70 5G, 8 GB / 256 GB, PHP 26,990, marked verified on 2022-10-18. The entry is historical price evidence, not a current offer.",
        },
    ]
    honor_id = sources[0]["id"]
    gadget_id = sources[1]["id"]
    price_id = sources[2]["id"]
    fields = [
        field("display_size", honor_id, "6.67 inches", 6.67, key="displayInches", unit="in", note="HONOR Philippines official specification."),
        field("display_technology", honor_id, "OLED", "OLED", key="displayType", note="HONOR Philippines official specification."),
        field("display_resolution", honor_id, "FHD+ 2400 x 1080", "2400 x 1080", key="resolution", note="HONOR Philippines official specification."),
        field("display_refresh_rate", honor_id, "Up to 120 Hz", 120, key="refreshHz", unit="Hz", note="HONOR Philippines official specification."),
        field("chipset", honor_id, "Qualcomm Snapdragon 778G Plus", "Qualcomm Snapdragon 778G Plus", key="chipset", note="HONOR Philippines official specification."),
        field("cpu", honor_id, "1 × Cortex-A78 2.5 GHz + 3 × Cortex-A78 2.4 GHz + 4 × Cortex-A55 1.8 GHz", "1 × Cortex-A78 2.5 GHz + 3 × Cortex-A78 2.4 GHz + 4 × Cortex-A55 1.8 GHz", key="cpu", note="HONOR Philippines official specification; maximum frequencies may vary under workload."),
        field("gpu", honor_id, "Adreno 642L", "Adreno 642L", key="gpu", note="HONOR Philippines official specification."),
        field("operating_system", honor_id, "Magic UI 6.1 based on Android 12", "Magic UI 6.1 (Android 12)", key="os", note="HONOR Philippines official specification; later software updates are not inferred."),
        field("ram_capacity", honor_id, "8 GB", 8, key="ramGb", unit="GB", note="HONOR Philippines lists 8 GB + 256 GB memory."),
        field("storage_capacity", honor_id, "256 GB", 256, key="storageGb", unit="GB", note="HONOR Philippines lists 8 GB + 256 GB memory."),
        field("rear_camera_system", honor_id, "54 MP IMX800 main (f/1.9) + 50 MP ultra-wide and macro (f/2.2) + 2 MP depth (f/2.4)", "54 MP main + 50 MP ultra-wide/macro + 2 MP depth", note="HONOR Philippines lists the three rear camera modules and apertures."),
        field("main_camera_sensor", honor_id, "54 MP Sony IMX800 Super Sensing Main Camera", "Sony IMX800; 54 MP", note="Sensor model and resolution stated by HONOR Philippines."),
        field("ultrawide_camera", honor_id, "50 MP Ultra Wide & Macro camera", "50 MP ultra-wide and macro", note="HONOR Philippines official specification."),
        field("telephoto_camera", honor_id, "The official page lists main, ultra-wide/macro, and depth cameras; no telephoto module is listed.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE", note="The official Philippine camera specification enumerates all three rear modules and does not list a telephoto camera."),
        field("front_camera", honor_id, "32 MP Super Clear Selfie Camera (f/2.4)", 32, key="frontCameraMp", unit="MP", note="HONOR Philippines official specification."),
        field("video_recording", honor_id, "Rear up to 4K; front up to 1080p; EIS video stabilization", "Rear up to 4K; front up to 1080p; EIS", key="video", note="HONOR Philippines official specification."),
        field("battery_capacity", honor_id, "4800 mAh typical; 4700 mAh rated", 4800, key="batteryMah", unit="mAh", note="HONOR Philippines specifies 4800 mAh typical and 4700 mAh rated capacity."),
        field("battery_technology", honor_id, "Lithium Polymer; 4700 mAh rated / 4800 mAh typical", "Lithium Polymer; 4700 mAh rated / 4800 mAh typical", note="HONOR Philippines official specification."),
        field("wired_charging", honor_id, "Up to 11V/6A; supplied charger is HONOR 66W SuperCharge", 66, key="chargingW", unit="W", note="HONOR Philippines lists the supported charging profile and a 66 W SuperCharge charger."),
        field("dimensions", honor_id, "161.4 x 73.3 x 7.91 mm", "161.4 x 73.3 x 7.91 mm", key="dimensions", unit="mm", note="HONOR Philippines official specification; measurements can vary slightly by unit."),
        field("weight", honor_id, "Approximately 178 g including battery", 178, key="weightG", unit="g", note="Approximate weight stated by HONOR Philippines."),
        field("cellular_bands", honor_id, "5G NR / LTE / WCDMA / GSM; band availability depends on region and network", "5G NR, LTE, WCDMA, GSM", key="cellular", note="HONOR Philippines lists these network standards; no unsupported local band mapping is inferred."),
        field("wifi", honor_id, "802.11 a/b/g/n/ac/ax, MIMO; 2.4 GHz and 5 GHz", "802.11 a/b/g/n/ac/ax, MIMO; 2.4/5 GHz", key="wifi", note="HONOR Philippines official specification."),
        field("bluetooth", honor_id, "Bluetooth 5.2; BLE, SBC, AAC, LDAC, aptX, aptX HD", "Bluetooth 5.2; BLE, SBC, AAC, LDAC, aptX, aptX HD", note="HONOR Philippines official specification."),
        field("sim_esim", honor_id, "Official page lists single-SIM and dual-SIM model variants; local SKU mapping is not stated.", None, status="PENDING_VERIFICATION", note="The official page documents more than one SIM configuration. The Philippine 8 GB / 256 GB price-list row does not identify which SIM SKU was sold; do not assume dual SIM."),
        field("official_launch_price_php", gadget_id, "PHP 26,990 retail price reported on 2022-10-19; YugaTech lists the 8 GB / 256 GB configuration at PHP 26,990 verified 2022-10-18.", 26990, unit="PHP", status="VERIFIED_SECONDARY", note="Historical Philippine launch-era price only. It is not represented as a current price and is not loaded into the public price filter."),
    ]
    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "HONOR",
        "model": "70",
        "configuration": "8 GB RAM / 256 GB storage",
        "sources": sources,
        "fields": fields,
        "replacementVariants": [{
            "id": CONFIG,
            "label": "8 GB RAM / 256 GB storage",
            "sku": None,
            "modelCode": None,
            "notes": "Official HONOR Philippines specifications and YugaTech's dated Philippine price list identify the 8 GB / 256 GB configuration. No exact Philippine SKU is recorded.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Contemporaneous reporting states the phone was available in the Philippines by 2022-10-19; current stock and exact first-sale date are not established.",
            "philippineAvailability": "GadgetMatch reported HONOR 70 5G was in the Philippines and available via HONOR stores and Lazada nationwide on 2022-10-19.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "N Series",
            "philippineReleaseYear": 2022,
            "researchNotes": "The official HONOR Philippines specification page and YugaTech's dated price history identify the Philippine 8 GB / 256 GB configuration. GadgetMatch reports local availability by 2022-10-19. PHP 26,990 is retained as historical launch-era price evidence; current price and stock are not verified.",
            "qualityFlag": "Exact Philippine SKU and first-sale date not recorded; price is historical",
            "openIssues": [
                {"issue": "Exact first-sale date and Philippine SKU are not recorded", "action": "Keep the availability date blank; retain only the source-backed year and configuration."},
                {"issue": "Current retail price and stock are not verified", "action": "Use the dated PHP 26,990 evidence only as price history, not a current offer."},
                {"issue": "Official product images have no reusable license or permission recorded", "action": "Continue showing the neutral placeholder."},
                {"issue": "Official page lists single-SIM and dual-SIM variations without mapping them to the local SKU", "action": "Keep SIM configuration unresolved."},
            ],
        },
    }
    add_review(manual, catalog, review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR 70 product image was identified on the official Philippine product page, but reuse rights or written permission are not recorded.",
        "sourcePage": "https://www.honor.com/ph/phones/honor-70/",
        "assetUrl": IMAGE_URL,
        "scope": "Exact model; configuration not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR 70",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    snapshot = {
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "70", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [],
        "prices": [{
            "device_id": DEVICE, "amount_php": 26990,
            "configuration_id": CONFIG, "configuration_match": "exact",
            "variant_ram_gb": 8, "variant_storage_gb": 256,
            "price_type": "independent_reported_historical_price",
            "source_published_at": None,
            "excerpt": "YugaTech lists HONOR 70 5G, 8GB/256GB, PHP 26,990; entry marked Verified Oct 18, 2022. Historical price evidence, not a current offer.",
            "source_url": URL_YUGATECH, "source_kind": "independent_ph_reference",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
        }],
        "discovery": [],
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "model": "HONOR 70",
        "configuration": "8 GB / 256 GB",
        "reviewedFields": len(fields),
        "historicalPriceCandidatePhp": 26990,
        "priceLoadedAsCurrent": False,
        "availabilityYear": 2022,
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
