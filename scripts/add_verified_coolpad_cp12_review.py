#!/usr/bin/env python3
"""Record separate source-backed Philippine configuration reviews for Coolpad CP12."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/coolpad-cp12-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_5bc54f4d744bec"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG_64 = f"{DEVICE}-4gb-64gb-ph"
CONFIG_128 = f"{DEVICE}-4gb-128gb-ph"

URL_COOLPAD_VIDEO = "https://www.youtube.com/watch?v=5fgVz_MJohM"
URL_COOLPAD_PAGE = "https://www.coolpad.com/"
URL_YUGA = "https://www.yugatech.com/mobile/coolpad-cp12-and-cool-20-smartphones-now-available-in-the-philippines/"
URL_NOYPI = "https://www.noypigeeks.com/android/coolpad-cp12/"
URL_UNBOX = "https://unboxdiaries.com/phones/coolpad-cp12/"
URL_UNISOC = "https://www.unisoc.com/en/product/SmartPhone/9863A"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("coolpad_cp12_official_video", "Coolpad Official", URL_COOLPAD_VIDEO,
           "Official product identity and official-unboxing reference",
           "Coolpad's verified channel published a CP12 unboxing video on August 24, 2023. It establishes the manufacturer's use of the CP12 product name, but the video description does not state a model code, Philippine SKU, specifications, or first sale date.",
           "2023-08-24"),
    source("coolpad_cp12_global_page", "Coolpad Global", URL_COOLPAD_PAGE,
           "Attempted official product-page review",
           "The Coolpad global website was checked for a CP12 model-specific specification page, but no readable exact-model specification content was available in this review. No facts are promoted from the site homepage."),
    source("coolpad_cp12_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine availability, configurations, launch prices, and local specification evidence",
           "Published October 5, 2023, YugaTech reports Coolpad's Philippine introduction of the CP12. Its CP12 spec list identifies 4 GB RAM, 64 GB / 128 GB storage, UNISOC SC9863A, cameras, connectivity, Android 13, battery, colors, and 3.5 mm audio. The article reports Bluetooth 4.2 while other local references say 5.0; its dimensions list 8.4 mm while two other sources list 8.3 mm. Exact-model photos appear on the page without recorded reuse terms.",
           "2023-10-05"),
    source("coolpad_cp12_noypi_ph", "NoypiGeeks Philippines", URL_NOYPI,
           "Contemporaneous Philippine launch price and exact-model specification cross-check",
           "Published October 5, 2023, it reports PHP 3,899 for 4 GB / 64 GB and PHP 4,299 for 4 GB / 128 GB, with an official Shopee store noted. It corroborates the local display, 4G chipset, memory, cameras, battery, OS, USB-C, and sensors; it lists Bluetooth 5.0 and dimensions 8.3 mm, differing from YugaTech's Bluetooth 4.2 and 8.4 mm." ,
           "2023-10-05"),
    source("coolpad_cp12_unboxdiaries", "Unbox Diaries", URL_UNBOX,
           "Exact-model specification cross-check, including the 128 GB configuration",
           "The exact-model page provides detailed 4 GB / 128 GB specs, including eMMC 5.1, 10 W charging, Li-Po battery, 1080p30 rear video, USB-C 2.0 OTG, and sensors. It says Bluetooth 5.0 and no 3.5 mm headphone jack, conflicting with YugaTech's Bluetooth 4.2 and reported headphone jack. Its price is TBA, so it does not establish a current offer."),
    source("coolpad_cp12_unisoc_sc9863a", "UNISOC", URL_UNISOC,
           "Primary SC9863A CPU, GPU, process, memory, storage-platform, connectivity, and radio-capability reference",
           "UNISOC specifies an octa-core Arm Cortex-A55 SC9863A up to 1.6 GHz, PowerVR GE8322, process alternatives 28 nm HPC+ / 22 nm, LPDDR3/LPDDR4X and eMMC 5.1 platform support, Wi-Fi b/g/n, Bluetooth 4.2, LTE, GPS/GLONASS/BeiDou, and FM. The platform's alternative capabilities are not assumed to be present in each CP12 configuration."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, config_match: str,
          catalog_value=None, price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": config_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        item["unit"] = unit
    if price_type:
        item["priceType"] = price_type
    return item


def fields_for(storage: int, launch_price: int) -> list[dict]:
    config = f"Philippine Coolpad CP12, 4 GB RAM / {storage} GB storage"
    storage_status = "VERIFIED_SECONDARY" if storage == 128 else "NOT_DISCLOSED"
    storage_raw = ("NoypiGeeks lists 128 GB eMMC 5.1 for the CP12; YugaTech confirms this Philippine configuration is 4 GB / 128 GB"
                   if storage == 128 else "The 4 GB / 64 GB Philippine configuration is confirmed, but its installed storage interface is not stated")
    storage_value = "eMMC 5.1" if storage == 128 else None
    rows = [
        ("model_number", "coolpad_cp12_official_video", "Coolpad's official channel identifies the product as CP12 but supplies no separate alphanumeric hardware model code", None, "NOT_DISCLOSED", None, None, "Keep the model-code field blank; the public product name itself is CP12."),
        ("global_release_date", "coolpad_cp12_official_video", "Coolpad's official unboxing video is dated August 24, 2023; no official global first-sale date was found", None, "NOT_DISCLOSED", None, None, "An unboxing publication date is not a first-sale date. Keep the global release date unset."),
        ("configuration", "coolpad_cp12_yugatech_ph", f"Philippine CP12 configuration: 4 GB RAM / {storage} GB storage", f"4 GB RAM / {storage} GB storage", "VERIFIED_SECONDARY", None, None, "YugaTech's Philippine launch coverage identifies both 4 GB storage variants separately; this review is for the listed configuration only."),
        ("philippine_release_date", "coolpad_cp12_yugatech_ph", "YugaTech and NoypiGeeks reported the CP12 launched/available in the Philippines on October 5, 2023", "2023-10-05", "VERIFIED_SECONDARY", None, None, "Dated local launch coverage, not an exact first transaction timestamp."),
        ("official_launch_price_php", "coolpad_cp12_yugatech_ph", f"Philippine launch price: PHP {launch_price:,} for 4 GB / {storage} GB", launch_price, "VERIFIED_SECONDARY", None, "PHP", "Historical local launch price for this exact configuration; not a current price.", None, "historical_ph_launch_price"),
        ("current_price_php", "coolpad_cp12_noypi_ph", "The reviewed local prices are dated October 2023; no current dated and orderable Philippine offer was verified", None, "PENDING_VERIFICATION", None, "PHP", "Keep the public catalog current price blank; retain launch prices in the candidate audit only.", None, "no_current_offer_verified"),
        ("display_size", "coolpad_cp12_yugatech_ph", "6.517-inch waterdrop display, commonly rounded to 6.52 inches", 6.52, "VERIFIED_SECONDARY", "displayInches", "in", "YugaTech and NoypiGeeks list this same rounded size."),
        ("display_technology", "coolpad_cp12_noypi_ph", "6.52-inch IPS LCD display", "IPS LCD", "VERIFIED_SECONDARY", "displayType", None, "NoypiGeeks and Unbox Diaries list IPS LCD."),
        ("display_resolution", "coolpad_cp12_yugatech_ph", "HD+ 1600 x 720 pixels", "1600 x 720", "VERIFIED_SECONDARY", "resolution", None, "YugaTech and NoypiGeeks agree."),
        ("display_refresh_rate", "coolpad_cp12_noypi_ph", "60 Hz", 60, "VERIFIED_SECONDARY", "refreshHz", "Hz", "NoypiGeeks and Unbox Diaries list 60 Hz."),
        ("display_brightness", "coolpad_cp12_yugatech_ph", "No brightness value recorded in the reviewed local exact-model sources", None, "NOT_DISCLOSED", None, "nits", "Do not infer brightness."),
        ("display_protection", "coolpad_cp12_yugatech_ph", "No cover-glass type or display-protection rating recorded", None, "NOT_DISCLOSED", None, None, "Keep display protection blank."),
        ("chipset", "coolpad_cp12_yugatech_ph", "UNISOC SC9863A", "UNISOC SC9863A", "VERIFIED_SECONDARY", "chipset", None, "YugaTech and NoypiGeeks identify the same exact-model chipset; UNISOC provides its official platform page."),
        ("process_node", "coolpad_cp12_unisoc_sc9863a", "UNISOC lists process alternatives 28 nm HPC+ / 22 nm for SC9863A without identifying which is used in this phone", None, "NOT_DISCLOSED", None, "nm", "Do not select one of the platform's alternative process values for the CP12."),
        ("cpu", "coolpad_cp12_unisoc_sc9863a", "Octa-core Arm Cortex-A55, maximum 1.6 GHz; Unbox Diaries reports 4x1.6 GHz plus 4x1.2 GHz", "Octa-core Cortex-A55, up to 1.6 GHz", "VERIFIED", "cpu", None, "UNISOC confirms the architecture and top frequency; the per-cluster arrangement is secondary-source detail and is not made the catalog value."),
        ("gpu", "coolpad_cp12_unisoc_sc9863a", "Imagination PowerVR GE8322 (UNISOC product page has a minor label typo in the rendered heading)", "Imagination PowerVR GE8322", "VERIFIED", "gpu", None, "UNISOC, YugaTech, and NoypiGeeks identify the GE8322."),
        ("operating_system", "coolpad_cp12_yugatech_ph", "Android 13", "Android 13", "VERIFIED_SECONDARY", "os", None, "Exact-model local launch spec."),
        ("os_support", "coolpad_cp12_yugatech_ph", "No update policy, support duration, or end-of-support date found", None, "NOT_DISCLOSED", None, None, "No software-support commitment is inferred."),
        ("ram_capacity", "coolpad_cp12_yugatech_ph", "4 GB RAM", 4, "VERIFIED_SECONDARY", "ramGb", "GB", "Both documented Philippine configurations have 4 GB RAM."),
        ("ram_type", "coolpad_cp12_unisoc_sc9863a", "The SoC platform supports LPDDR3 or LPDDR4/4X; the CP12's installed RAM type is not identified", None, "NOT_DISCLOSED", None, None, "Platform support is not proof of the installed memory type."),
        ("storage_capacity", "coolpad_cp12_yugatech_ph", f"{storage} GB storage", storage, "VERIFIED_SECONDARY", "storageGb", "GB", "This separate configuration is explicitly listed in Philippine launch coverage."),
        ("storage_type", "coolpad_cp12_noypi_ph", storage_raw, storage_value, storage_status, "storageType" if storage == 128 else None, None, "Only the 128 GB variant's local spec table identifies eMMC 5.1; the 64 GB interface remains unrecorded."),
        ("storage_expansion", "coolpad_cp12_yugatech_ph", "YugaTech lists a microSD slot; NoypiGeeks says the 128 GB configuration is expandable via microSD", "microSD supported; capacity limit and tray sharing not confirmed for PH SKUs", "VERIFIED_SECONDARY", None, None, "Do not infer a maximum card size or SIM-tray arrangement."),
        ("rear_camera_system", "coolpad_cp12_yugatech_ph", "13 MP main camera + 2 MP macro camera", "13 MP main + 2 MP macro", "VERIFIED_SECONDARY", "rearCameraMp", "MP", "Catalog numeric value is the main rear-camera resolution.", 13),
        ("main_camera_sensor", "coolpad_cp12_unboxdiaries", "13 MP wide main camera with autofocus; sensor maker/model not stated", "13 MP wide autofocus; sensor model not disclosed", "VERIFIED_SECONDARY", None, None, "No sensor identity is inferred from the resolution."),
        ("ultrawide_camera", "coolpad_cp12_yugatech_ph", "The complete listed rear system is 13 MP main + 2 MP macro; no ultrawide camera is listed", "No ultrawide camera listed", "NOT_APPLICABLE", None, None, "Based on the complete two-camera rear specification."),
        ("telephoto_camera", "coolpad_cp12_yugatech_ph", "The complete listed rear system is 13 MP main + 2 MP macro; no telephoto camera is listed", "No telephoto camera listed", "NOT_APPLICABLE", None, None, "Based on the complete two-camera rear specification."),
        ("front_camera", "coolpad_cp12_yugatech_ph", "5 MP front camera", 5, "VERIFIED_SECONDARY", "frontCameraMp", "MP", "YugaTech and NoypiGeeks agree."),
        ("video_recording", "coolpad_cp12_unboxdiaries", "Rear video listed at 1080p30; complete modes and front-camera frame rate are not specified", "Rear 1080p30; other modes not recorded", "VERIFIED_SECONDARY", "video", None, "Do not infer additional video modes from the SoC platform."),
        ("battery_capacity", "coolpad_cp12_yugatech_ph", "4,500 mAh", 4500, "VERIFIED_SECONDARY", "batteryMah", "mAh", "YugaTech and NoypiGeeks agree."),
        ("battery_technology", "coolpad_cp12_unboxdiaries", "Li-Po, non-removable", "Li-Po; non-removable", "VERIFIED_SECONDARY", None, None, "Exact-model technical listing; the local launch sources confirm capacity but do not state chemistry."),
        ("wired_charging", "coolpad_cp12_noypi_ph", "10 W wired charging", 10, "VERIFIED_SECONDARY", "chargingW", "W", "NoypiGeeks and Unbox Diaries list 10 W."),
        ("wireless_charging", "coolpad_cp12_yugatech_ph", "Wireless and reverse wireless charging are not stated in the reviewed exact-model sources", None, "NOT_DISCLOSED", None, None, "Do not infer absence from silence."),
        ("dimensions", "coolpad_cp12_noypi_ph", "164.2 x 75.7 x 8.3 mm; YugaTech reports thickness as 8.4 mm", "164.2 x 75.7 x 8.3 mm", "VERIFIED_SECONDARY", "dimensions", "mm", "Two local detailed references use 8.3 mm; YugaTech rounds/reports 8.4 mm. Preserve the difference in this note."),
        ("weight", "coolpad_cp12_yugatech_ph", "190 g", 190, "VERIFIED_SECONDARY", "weightG", "g", "YugaTech and NoypiGeeks agree."),
        ("materials", "coolpad_cp12_yugatech_ph", "NoypiGeeks describes a glass-like rear panel; Unbox Diaries lists glass front and rear, but no readable Coolpad material specification was found", None, "CONFLICTING_INFORMATION", None, None, "The descriptions are not precise enough to assert front/rear construction. Leave materials unset."),
        ("ingress_protection", "coolpad_cp12_yugatech_ph", "No IP rating or water-resistance certification recorded", None, "NOT_DISCLOSED", None, None, "No protection rating is inferred."),
        ("sim_esim", "coolpad_cp12_yugatech_ph", "Dual-SIM; eSIM not documented", "Dual-SIM; eSIM not disclosed", "VERIFIED_SECONDARY", "sim", None, "YugaTech and NoypiGeeks list dual-SIM; microSD tray sharing is not established."),
        ("cellular_bands", "coolpad_cp12_noypi_ph", "HSPA+ and 4G LTE; exact CP12 variant band list is not recorded", "HSPA+ / 4G LTE; bands not recorded", "VERIFIED_SECONDARY", "cellular", None, "The SC9863A is an LTE platform; do not infer local carrier-band compatibility."),
        ("wifi", "coolpad_cp12_yugatech_ph", "Wi-Fi 802.11 b/g/n", "Wi-Fi 802.11 b/g/n", "VERIFIED_SECONDARY", "wifi", None, "YugaTech and UNISOC list b/g/n platform support."),
        ("bluetooth", "coolpad_cp12_unisoc_sc9863a", "UNISOC and YugaTech list Bluetooth 4.2; NoypiGeeks and Unbox Diaries list Bluetooth 5.0", None, "CONFLICTING_INFORMATION", "bluetooth", None, "The chipset page lists Bluetooth 4.2, but two exact-model pages report 5.0. Keep the public Bluetooth value unset pending model-specific primary evidence."),
        ("usb", "coolpad_cp12_unboxdiaries", "USB Type-C 2.0 with OTG", "USB Type-C 2.0; OTG", "VERIFIED_SECONDARY", "ports", None, "YugaTech independently confirms the Type-C connector."),
        ("nfc", "coolpad_cp12_unboxdiaries", "NFC: No", False, "VERIFIED_SECONDARY", None, None, "Exact-model listing gives an explicit negative value; YugaTech and NoypiGeeks do not list NFC."),
        ("gnss", "coolpad_cp12_noypi_ph", "GPS, GLONASS, and BeiDou", "GPS, GLONASS, BeiDou", "VERIFIED_SECONDARY", None, None, "NoypiGeeks exact-model table; UNISOC lists GPS/GLONASS/BeiDou platform capability."),
        ("audio", "coolpad_cp12_yugatech_ph", "YugaTech lists a 3.5 mm headphone jack; Unbox Diaries says no headphone jack", None, "CONFLICTING_INFORMATION", "sound", None, "Exact-model sources directly disagree. Keep the headphone-jack/audio value unset until the Philippine hardware is checked."),
        ("sensors", "coolpad_cp12_unboxdiaries", "Side fingerprint reader, accelerometer, and proximity sensor; YugaTech also lists face unlock", "Side fingerprint reader, accelerometer, proximity; face unlock", "VERIFIED_SECONDARY", None, None, "Only sensor/authentication items explicitly listed by exact-model sources are included."),
    ]
    result = [field(fid, sid, value, normalized, status=status, key=key, unit=unit,
                    note=note, config_match=config,
                    catalog_value=catalog_value,
                    price_type=price_type)
              for fid, sid, value, normalized, status, key, unit, note, *optional in rows
              for catalog_value, price_type in [(optional[0] if len(optional) > 0 else None,
                                                 optional[1] if len(optional) > 1 else None)]]
    if len(result) != 46:
        raise ValueError(f"Expected 46 smartphone fields, got {len(result)}")
    source_ids = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in result} - source_ids)
    if missing:
        raise ValueError(f"Fields reference undefined sources: {missing}")
    return result


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "YugaTech and NoypiGeeks reported the Coolpad CP12 in the Philippine market on October 5, 2023; NoypiGeeks noted an official Shopee store. Workbook eligibility remains Pending.",
        "philippineAvailability": "Contemporaneous YugaTech and NoypiGeeks coverage reports the Coolpad CP12 launched in the Philippines on October 5, 2023, with PHP 3,899 / 4 GB / 64 GB and PHP 4,299 / 4 GB / 128 GB configurations. NoypiGeeks noted an official Shopee store. This records local launch reporting, not an exact first-sale transaction timestamp.",
        "observedAt": OBSERVED,
        "manufacturer": "Coolpad",
        "catalogModel": "CP12",
        "productLine": "Coolpad CP12",
        "modelNumber": None,
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Philippine launch report date",
        "researchNotes": "Workbook CP12 row matched to the Coolpad CP12 launched in the Philippines in October 2023. Two separately priced local configurations are documented: 4 GB / 64 GB and 4 GB / 128 GB. Current price, exact global first-sale date, separate model code, Bluetooth version, headphone jack, and image reuse remain unresolved; eligibility remains Pending.",
        "qualityFlag": "CP12 local match; two PH variants recorded; current offer, model code, some hardware details, and image rights unresolved.",
        "openIssues": [
            {"issue": "The official CP12 product name is confirmed, but the reviewed sources do not establish a separate hardware model code", "action": "Keep modelNumber blank."},
            {"issue": "YugaTech/UNISOC list Bluetooth 4.2 while NoypiGeeks and Unbox Diaries list 5.0", "action": "Leave Bluetooth unresolved pending model-specific primary evidence."},
            {"issue": "YugaTech lists a 3.5 mm jack while Unbox Diaries says no headphone jack", "action": "Leave audio/headphone-jack details unresolved."},
            {"issue": "Reported body thickness ranges from 8.3 to 8.4 mm across local sources", "action": "Retain the source precision discrepancy; this does not create separate device variants."},
            {"issue": "Only dated 2023 launch prices were verified", "action": "Show current prices as not recorded; retain the two launch prices as historical observations."},
            {"issue": "Exact product images are published by review sites without recorded reuse permission", "action": "Continue to use the neutral placeholder until documented permission is available."},
            {"issue": "Workbook eligibility status remains Pending", "action": "Preserve Pending and follow the existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "coolpad"
            or device.get("model") != "CP12"):
        raise ValueError("Inventory row no longer matches Coolpad CP12")
    existing_variant_ids = {variant.get("id") for variant in device.get("variants", [])}
    expected_variant_ids = {OLD_CONFIG, CONFIG_64, CONFIG_128}
    if existing_variant_ids - expected_variant_ids:
        raise ValueError(f"Unexpected CP12 configurations: {sorted(existing_variant_ids)}")

    variants = [
        {"id": CONFIG_64, "label": "4 GB RAM / 64 GB storage", "sku": None, "modelCode": None,
         "notes": "Blue, Silver, and Black were listed for the model; which colors apply to this storage SKU is not recorded.", "workbookRow": 134},
        {"id": CONFIG_128, "label": "4 GB RAM / 128 GB storage", "sku": None, "modelCode": None,
         "notes": "Blue, Silver, and Black were listed for the model; which colors apply to this storage SKU is not recorded.", "workbookRow": 134},
    ]
    records = []
    for index, (variant, price, storage) in enumerate(((variants[0], 3899, 64), (variants[1], 4299, 128))):
        records.append({
            "deviceId": DEVICE,
            "configurationId": variant["id"],
            "brand": "Coolpad",
            "model": "CP12",
            "configuration": variant["label"],
            "configurationLabel": variant["label"],
            "sources": SOURCES,
            "fields": fields_for(storage, price),
            "availabilityEvidence": availability_evidence(),
            **({"replacementVariants": variants, "replaceUnrecordedPlaceholder": True} if index == 0 else {}),
        })
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].extend(records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Exact CP12 photographs appear on local launch/review pages, but no reusable image license or written permission is recorded. Do not embed or hotlink an unlicensed image.",
        "sourcePage": URL_YUGA,
        "assetUrl": None,
        "scope": "Coolpad CP12; PH 4 GB / 64 GB and 4 GB / 128 GB variants",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Coolpad CP12",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for variant, storage, amount in ((variants[0], 64, 3899), (variants[1], 128, 4299)):
        prices.append({
            "device_id": DEVICE, "amount_php": amount, "configuration_id": variant["id"],
            "configuration_match": f"exact_philippine_4gb_{storage}gb_configuration",
            "variant_ram_gb": 4, "variant_storage_gb": storage,
            "price_type": "historical_ph_launch_price", "source_published_at": "2023-10-05",
            "excerpt": f"Philippine launch coverage lists PHP {amount:,} for the 4 GB / {storage} GB Coolpad CP12 configuration.",
            "source_url": URL_NOYPI, "source_kind": "historical_local_launch_price",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
            "availability_status": "historical_launch_price_not_current",
        })
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Coolpad", "model_name": "CP12", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech lists two Philippine CP12 configurations: 4 GB / 64 GB at PHP 3,899 and 4 GB / 128 GB at PHP 4,299; both prices are historical."},
            {"device_id": DEVICE, "source_url": URL_NOYPI, "result": "NoypiGeeks independently reports the same two local configuration prices and notes an official Shopee store; no active offer was verified."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Coolpad CP12 workbook row -> Philippine Coolpad CP12",
        "configurations": [{"label": item["label"], "historicalPricePhp": price} for item, price in zip(variants, (3899, 4299))],
        "reviewedFields": sum(len(item["fields"]) for item in records),
        "philippineAvailabilityReportDate": "2023-10-05",
        "currentPrices": "blank for both configurations",
        "image": "neutral placeholder; reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
