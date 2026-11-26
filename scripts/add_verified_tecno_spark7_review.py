#!/usr/bin/env python3
"""Record source-backed Philippine research for TECNO Spark 7."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/tecno-spark-7-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_cca2630fec4a42"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-3gb-64gb-ph"

URL_YUGA = "https://www.yugatech.com/mobile/tecno-spark-7-specs-price-philippines/"
URL_NOYPI = "https://www.noypigeeks.com/android/tecno-spark-7-ph/"
URL_REVU = "https://www.revu.com.ph/2021/08/tecno-spark-7-price-in-philippines/"
URL_NTC = "https://region4b.ntc.gov.ph/wp-content/uploads/2022/01/GEC_12312021.pdf"
URL_GSMARENA = "https://www.gsmarena.com/tecno_spark_7-price-10845.php"
URL_GSMARENA_LAUNCH = "https://www.gsmarena.com/tecno_spark_7_is_coming_to_india_next_week_with_6000_mah_battery_android_11-news-48591.php"
URL_MEDIATEK = "https://www.mediatek.com/products/smartphones/mediatek-helio-a25"
URL_PTG = "https://www.pinoytechnoguide.com/pricelists/TECNO"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("tecno_spark7_yugatech", "YugaTech Philippines", URL_YUGA,
           "Philippine launch, local configuration, historical price, and specification evidence",
           "Published August 13, 2021. Reports official Philippine launch, an available 3 GB / 64 GB model at PHP 4,990 through TECNO's official Shopee store, display, chipset, cameras, software, battery, dimensions, and colors.",
           "2021-08-13"),
    source("tecno_spark7_noypi", "NoypiGeeks Philippines", URL_NOYPI,
           "Independent Philippine availability, price, and specification cross-check",
           "Published August 12, 2021. Reports the 3 GB / 64 GB Spark 7 available in TECNO's official Shopee store for PHP 4,990; lists the 6.5-inch HD+ IPS panel, Helio A25, cameras, battery, software, connectivity, dimensions, and rear fingerprint reader. It says it was unknown whether the global 2 GB / 32 GB version would reach the Philippines.",
           "2021-08-12"),
    source("tecno_spark7_revu", "Revu Philippines", URL_REVU,
           "Independent Philippine launch and display/charging specification cross-check",
           "Published August 14, 2021. Identifies the local 3 GB / 64 GB model at PHP 4,990 and reports a 6.52-inch HD+ LCD at 60 Hz, Helio A25, IMG GE8320, 10 W charging, and launch software. Its display-size figure is more precise than other local reports, which round it to 6.5 inches.",
           "2021-08-14"),
    source("tecno_spark7_ntc_gec", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and marketed-name evidence",
           "The NTC GEC register associates model codes KF6j, KF6K, and PR651 with the marketing name SPARK 7 and applicant Twireless Inc. The register supports local equipment registration but does not identify which code or RAM/storage configuration was sold at retail."),
    source("tecno_spark7_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-model global release and technical cross-check",
           "The listing identifies TECNO Spark 7 and records release on April 16, 2021, Android 11 / HiOS 7.5, Helio A25, 6.5-inch 720p display, 16 MP camera, and 6000 mAh battery. The listing spans global RAM/storage options; local launch sources control the Philippine configuration."),
    source("tecno_spark7_gsmarena_india_launch", "GSMArena", URL_GSMARENA_LAUNCH,
           "Contemporaneous global-market release context",
           "GSMArena's April 11, 2021 report says the Spark 7 would go on sale in India on April 16. This supports the earliest reviewed market release date, not a worldwide simultaneous release.",
           "2021-04-11"),
    source("tecno_spark7_mediatek_a25", "MediaTek", URL_MEDIATEK,
           "Primary chipset architecture and capabilities reference",
           "MediaTek lists the Helio A25 as TSMC 12 nm, octa-core Cortex-A53 with 1.8 GHz and 1.5 GHz frequency bins, IMG PowerVR GE8320, and support for multiple memory/storage/connectivity standards. SoC capabilities are not used to infer which RAM type, storage interface, Wi-Fi, Bluetooth, or cellular bands were implemented in this handset."),
    source("tecno_spark7_ptg_price_list", "PinoyTechGuide", URL_PTG,
           "Current Philippine TECNO price-list review",
           "The current TECNO list was reviewed on November 26, 2026. It lists newer Spark models and Spark 7T / Spark 7 Pro, but not the base Spark 7. This does not establish that no used or private sale exists; no current price is assigned."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, catalog_value=None,
          price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note,
            "configurationMatch": "Exact Philippine TECNO Spark 7 3 GB RAM / 64 GB storage unless a model-level chipset source is noted"}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        item["unit"] = unit
    if price_type:
        item["priceType"] = price_type
    return item


def fields_for() -> list[dict]:
    rows = [
        field("model_number", "tecno_spark7_ntc_gec", "NTC associates KF6j, KF6K, and PR651 with marketing name SPARK 7; retail configuration mapping not shown", None, status="PENDING_VERIFICATION", note="Keep the exact model number blank. The NTC register contains multiple codes and does not map one uniquely to the Philippine 3 GB / 64 GB retail configuration."),
        field("global_release_date", "tecno_spark7_gsmarena", "GSMArena lists release on April 16, 2021; its contemporaneous report identifies India sale beginning that day", "2021-04-16", status="VERIFIED_SECONDARY", note="Use the earliest reviewed market release date as a global release-history date; this does not imply a simultaneous worldwide launch or Philippine availability."),
        field("configuration", "tecno_spark7_yugatech", "TECNO Spark 7 (3 GB + 64 GB) listed as available in the Philippines", "3 GB RAM / 64 GB storage", status="VERIFIED_SECONDARY", note="YugaTech and NoypiGeeks independently identify this local configuration. NoypiGeeks explicitly says whether the global 2 GB / 32 GB version would arrive locally was unknown; do not add it as a Philippine variant."),
        field("philippine_release_date", "tecno_spark7_noypi", "NoypiGeeks reported the 3 GB / 64 GB model available in the Philippines on August 12, 2021; YugaTech reported it available on August 13", "2021-08-12", status="VERIFIED_SECONDARY", note="This is the earliest reviewed dated local availability report, corroborated the next day; it is not an exact first-sale transaction timestamp."),
        field("official_launch_price_php", "tecno_spark7_noypi", "PHP 4,990 for the Philippine 3 GB / 64 GB model, reported August 12, 2021", 4990, status="VERIFIED_SECONDARY", unit="PHP", note="Historical launch-era price tied to the exact local configuration and official Shopee store link; do not display as a current offer.", price_type="historical_ph_launch_price"),
        field("current_price_php", "tecno_spark7_ptg_price_list", "No current dated, orderable Philippine price for the base Spark 7 was listed in the reviewed TECNO index", None, status="UNAVAILABLE_AFTER_RESEARCH", unit="PHP", note="Keep the current catalog price blank. The PHP 4,990 value is a dated 2021 launch price; absence from the current list does not rule out used/private sales.", price_type="no_current_offer_verified"),
        field("display_size", "tecno_spark7_revu", "6.52-inch display; YugaTech and NoypiGeeks round to 6.5 inches", 6.52, key="displayInches", unit="in", note="Use the more precise local Revu figure; the other local launch references use the rounded 6.5-inch value."),
        field("display_technology", "tecno_spark7_noypi", "6.5-inch HD+ IPS display; Revu describes an LCD panel", "IPS LCD", key="displayType", note="Independent Philippine launch references support an IPS LCD; LCD is the panel family and IPS is the panel type."),
        field("display_resolution", "tecno_spark7_yugatech", "HD+ 720 x 1600 pixels", "720 x 1600", key="resolution", note="YugaTech, NoypiGeeks, and Revu report the same HD+ resolution."),
        field("display_refresh_rate", "tecno_spark7_revu", "60 Hz refresh rate", 60, key="refreshHz", unit="Hz", note="Revu's local specification explicitly lists 60 Hz."),
        field("display_brightness", "tecno_spark7_revu", "No brightness value stated in the reviewed Philippine product reports", None, status="NOT_DISCLOSED", unit="nits", note="No peak, typical, or HBM brightness figure is inferred."),
        field("display_protection", "tecno_spark7_yugatech", "No named cover-glass protection or scratch-resistance rating recorded", None, status="NOT_DISCLOSED", note="No protection rating is inferred from the absence of one in the local launch specifications."),
        field("chipset", "tecno_spark7_yugatech", "MediaTek Helio A25", "MediaTek Helio A25", key="chipset", note="YugaTech and NoypiGeeks identify the Helio A25 in the Philippine model."),
        field("process_node", "tecno_spark7_mediatek_a25", "MediaTek specifies a TSMC 12 nm process for Helio A25", 12, unit="nm", note="Chipset-level manufacturing process, not a separate measurement of the handset."),
        field("cpu", "tecno_spark7_mediatek_a25", "Octa-core Arm Cortex-A53; MediaTek lists 1.8 GHz and 1.5 GHz frequency bins", "Octa-core Arm Cortex-A53 (1.8 GHz / 1.5 GHz bins)", key="cpu", note="MediaTek's chipset specification does not state how many handset cores run at each frequency; no per-cluster core counts are inferred."),
        field("gpu", "tecno_spark7_noypi", "IMG PowerVR GE8320", "IMG PowerVR GE8320", key="gpu", note="NoypiGeeks reports this GPU for the Spark 7; MediaTek identifies the same GPU as an A25 capability."),
        field("operating_system", "tecno_spark7_yugatech", "HiOS 7.5 based on Android 11", "HiOS 7.5 based on Android 11", key="os", note="Local launch reports identify Android 11 and HiOS 7.5 for the reported Philippine model."),
        field("os_support", "tecno_spark7_yugatech", "No OS upgrade or security-support policy found in reviewed sources", None, status="NOT_DISCLOSED", note="No update count, end date, or support duration is inferred."),
        field("ram_capacity", "tecno_spark7_yugatech", "3 GB RAM for the Philippine store configuration", 3, key="ramGb", unit="GB", note="Exact local configuration corroborated by YugaTech and NoypiGeeks."),
        field("ram_type", "tecno_spark7_mediatek_a25", "MediaTek lists LPDDR3 / LPDDR4 / LPDDR4x support for the A25; installed Spark 7 memory type is not stated", None, status="NOT_DISCLOSED", note="SoC compatibility is not evidence of the handset's installed RAM type."),
        field("storage_capacity", "tecno_spark7_yugatech", "64 GB storage for the Philippine store configuration", 64, key="storageGb", unit="GB", note="Exact local configuration corroborated by YugaTech and NoypiGeeks."),
        field("storage_type", "tecno_spark7_mediatek_a25", "MediaTek lists eMMC 5.1 as an A25 platform capability; no device-specific storage interface is recorded for the local SKU", None, status="NOT_DISCLOSED", note="Do not transfer a chipset-supported interface into the device record without model-specific evidence."),
        field("storage_expansion", "tecno_spark7_noypi", "Internal storage expandable via microSD; maximum card capacity not stated in the local reference", "microSD expansion; maximum capacity not recorded", note="No maximum capacity is inferred from another regional configuration."),
        field("rear_camera_system", "tecno_spark7_yugatech", "16 MP main camera plus a secondary camera described as QVGA by YugaTech and as a depth sensor by NoypiGeeks", "16 MP main + auxiliary QVGA / depth camera", key="rearCameraMp", unit="MP", note="Both Philippine references agree on the 16 MP main and a second auxiliary camera; catalog numeric value denotes only the main camera.", catalog_value=16),
        field("main_camera_sensor", "tecno_spark7_yugatech", "No sensor manufacturer or sensor model identified in reviewed Philippine launch specifications", None, status="NOT_DISCLOSED", note="The 16 MP camera resolution does not identify its sensor model."),
        field("ultrawide_camera", "tecno_spark7_noypi", "NoypiGeeks says the Spark 7 lacks an ultra-wide camera", "No ultra-wide camera reported", status="NOT_APPLICABLE", note="A local launch report explicitly says there is no ultra-wide camera."),
        field("telephoto_camera", "tecno_spark7_yugatech", "The listed rear system is 16 MP main plus QVGA auxiliary; no telephoto camera is reported", "No telephoto camera reported", status="NOT_APPLICABLE", note="No telephoto module appears in the complete local camera description."),
        field("front_camera", "tecno_spark7_yugatech", "8 MP front camera", 8, key="frontCameraMp", unit="MP", note="YugaTech and NoypiGeeks list an 8 MP front camera."),
        field("video_recording", "tecno_spark7_noypi", "Video Bokeh feature reported; capture resolution and frame rate not stated for the Philippine 3 GB / 64 GB configuration", "Video Bokeh; resolution and frame rate not recorded", key="video", note="Record the documented mode without inferring a recording resolution or frame rate."),
        field("battery_capacity", "tecno_spark7_yugatech", "6,000 mAh battery", 6000, key="batteryMah", unit="mAh", note="YugaTech, NoypiGeeks, and Revu report a 6,000 mAh capacity."),
        field("battery_technology", "tecno_spark7_noypi", "Non-removable battery; chemistry not stated", "Non-removable; battery chemistry not recorded", note="NoypiGeeks lists a non-removable battery; no Li-ion/Li-Po chemistry is inferred."),
        field("wired_charging", "tecno_spark7_revu", "10 W wired charging", 10, key="chargingW", unit="W", note="Revu's local Spark 7 specification explicitly reports 10 W."),
        field("wireless_charging", "tecno_spark7_yugatech", "Wireless and reverse charging are not stated in the reviewed local specifications", None, status="NOT_DISCLOSED", note="Do not infer lack of support from omission."),
        field("dimensions", "tecno_spark7_yugatech", "164.8 x 76.1 x 9.5 mm", "164.8 x 76.1 x 9.5 mm", key="dimensions", unit="mm", note="YugaTech and NoypiGeeks report matching dimensions."),
        field("weight", "tecno_spark7_yugatech", "No handset weight stated in the reviewed Philippine launch specifications", None, status="NOT_DISCLOSED", key="weightG", unit="g", note="Do not transfer a cross-market or implausible third-party listing into this local configuration."),
        field("materials", "tecno_spark7_yugatech", "Frame and back materials not recorded in reviewed local sources", None, status="NOT_DISCLOSED", note="No material composition is inferred from product images."),
        field("ingress_protection", "tecno_spark7_yugatech", "No IP rating recorded in reviewed local specifications", None, status="NOT_DISCLOSED", note="No water/dust rating is inferred."),
        field("sim_esim", "tecno_spark7_noypi", "Dual SIM, dual standby; SIM size and eSIM support not stated", "Dual SIM dual standby; SIM type and eSIM not recorded", key="sim", note="NoypiGeeks confirms dual SIM dual standby. Do not infer Nano-SIM or eSIM status."),
        field("cellular_bands", "tecno_spark7_yugatech", "4G LTE listed; exact Philippine frequency bands are not stated in the local launch specifications", "4G LTE; exact local bands not recorded", key="cellular", note="YugaTech reports LTE. NTC registration confirms approval of Spark 7 code entries but is not used to derive a complete handset band list."),
        field("wifi", "tecno_spark7_noypi", "Wi-Fi 802.11 b/g/n", "Wi-Fi 802.11 b/g/n", key="wifi", note="NoypiGeeks lists 802.11 b/g/n for Spark 7; MediaTek chipset capabilities are not substituted for device-specific implementation."),
        field("bluetooth", "tecno_spark7_noypi", "Bluetooth support is listed; version is not stated. YugaTech's Audio Share 2.0 name is a feature, not a Bluetooth version.", None, status="NOT_DISCLOSED", note="Do not infer Bluetooth 5 from the Helio A25 chipset specification."),
        field("usb", "tecno_spark7_noypi", "microUSB connector; USB data generation not stated", "microUSB; data standard not recorded", key="ports", note="NoypiGeeks lists microUSB. No USB 2.0 data rate is inferred."),
        field("nfc", "tecno_spark7_yugatech", "NFC support is not stated in reviewed local launch specifications", None, status="NOT_DISCLOSED", note="Omission from specifications is not treated as proof that NFC is absent."),
        field("gnss", "tecno_spark7_noypi", "GPS listed; other satellite systems not recorded in the local reference", "GPS; other GNSS constellations not recorded", key="gnss", note="Only GPS is attributed to this handset; MediaTek's additional chipset-level GNSS capability is not transferred."),
        field("audio", "tecno_spark7_noypi", "FM radio listed; headphone jack and speaker configuration not stated in the reviewed Philippine source", None, status="NOT_DISCLOSED", note="Do not infer a 3.5 mm jack or speaker count from global listings or product images."),
        field("sensors", "tecno_spark7_noypi", "Rear-mounted fingerprint scanner reported; a complete sensor list is not provided", "Rear fingerprint scanner; other sensors not recorded", note="NoypiGeeks identifies the rear fingerprint scanner. No accelerometer, proximity, or ambient-light sensors are inferred."),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field records, got {len(rows)}")
    source_ids = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in rows} - source_ids)
    if missing:
        raise ValueError(f"Fields reference undefined sources: {missing}")
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "YugaTech and NoypiGeeks report the 3 GB / 64 GB Spark 7 available through TECNO's official Shopee store in August 2021. NTC GEC records Spark 7 registrations, but the precise code-to-retail-configuration mapping is unresolved. Workbook eligibility remains Pending.",
        "philippineAvailability": "Philippine availability of TECNO Spark 7 3 GB / 64 GB was reported on August 12, 2021 by NoypiGeeks and on August 13 by YugaTech, both citing TECNO's official Shopee store. NTC lists multiple Spark 7 model codes but does not map one to this retail configuration. This is dated reported availability, not an exact first transaction date.",
        "observedAt": OBSERVED,
        "manufacturer": "TECNO Mobile",
        "catalogModel": "Spark 7",
        "productLine": "TECNO Spark",
        "modelNumber": None,
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Philippine availability report date",
        "researchNotes": "Workbook row 39 matched to TECNO Spark 7. YugaTech and NoypiGeeks identify the Philippine 3 GB / 64 GB configuration and report PHP 4,990 through TECNO's official Shopee store in August 2021; Revu independently corroborates the local model and selected specifications. The PHP 4,990 price is historical only. NTC lists multiple Spark 7 codes without mapping one to the local retail configuration. The global 2 GB / 32 GB variant is not added as a Philippine configuration. Workbook eligibility remains Pending.",
        "qualityFlag": "Philippine availability, one 3 GB / 64 GB configuration, and historical launch price verified; no current price; exact local model code and several hardware details unresolved; image reuse rights not established.",
        "openIssues": [
            {"issue": "No current dated, orderable Philippine offer was verified", "action": "Keep current price blank; preserve PHP 4,990 as historical only."},
            {"issue": "NTC associates several codes with Spark 7 without a retail configuration mapping", "action": "Leave the singular local model number blank until a manufacturer or retail document maps the exact 3 GB / 64 GB SKU."},
            {"issue": "Global 2 GB / 32 GB version is mentioned but Philippine sale was not established", "action": "Keep only the locally reported 3 GB / 64 GB variant."},
            {"issue": "Memory type, storage interface, weight, materials, battery chemistry, and exact cellular bands were not established for the Philippine configuration", "action": "Keep these fields blank rather than transferring chipset capabilities or unmatched regional specifications."},
            {"issue": "Local product photos match the model but image reuse terms were not found", "action": "Use the neutral unavailable-image placeholder until reuse permission is established."},
            {"issue": "Workbook eligibility status remains Pending", "action": "Preserve Pending and apply existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "tecno"
            or device.get("model", "").casefold() != "spark 7"):
        raise ValueError("Inventory row no longer matches TECNO Spark 7")
    current_ids = {variant.get("id") for variant in device.get("variants", [])}
    if current_ids - {OLD_CONFIG, CONFIG}:
        raise ValueError(f"Unexpected Spark 7 configurations: {sorted(current_ids)}")

    variant = {
        "id": CONFIG,
        "label": "3 GB RAM / 64 GB storage",
        "sku": None,
        "modelCode": None,
        "notes": "YugaTech and NoypiGeeks report this as the Philippine 3 GB / 64 GB official-store configuration. NoypiGeeks noted that Philippine availability of the global 2 GB / 32 GB version was unknown; it is not added as a local variant. Colors are not separate inventory SKUs.",
        "workbookRow": 39,
    }
    record = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "TECNO",
        "model": "Spark 7",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "modelCode": None,
        "sources": SOURCES,
        "fields": fields_for(),
        "availabilityEvidence": availability_evidence(),
        "replacementVariants": [variant],
        "replaceUnrecordedPlaceholder": True,
    }
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].append(record)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "YugaTech and NoypiGeeks display exact Spark 7 product photos, but no reusable image license or permission to copy/embed was recorded. Keep the neutral placeholder.",
        "sourcePage": URL_YUGA,
        "assetUrl": None,
        "scope": "TECNO Spark 7 / Philippine 3 GB RAM / 64 GB storage",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for TECNO Spark 7",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "TECNO", "model_name": "Spark 7", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NOYPI, "result": "NoypiGeeks reported the local 3 GB / 64 GB model available through TECNO's official Shopee store for PHP 4,990 on August 12, 2021; historical only."},
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech independently reported Philippine availability and the same PHP 4,990 price for the 3 GB / 64 GB configuration on August 13, 2021."},
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "The current PinoyTechGuide TECNO price index was checked; it omits the base Spark 7. This is not evidence that no second-hand/private sale exists."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "GSMArena global partner prices are not used as Philippine live offers and may refer to other variants or markets."},
        ],
        "prices": [{
            "device_id": DEVICE,
            "amount_php": 4990,
            "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_3gb_64gb_configuration",
            "variant_ram_gb": 3,
            "variant_storage_gb": 64,
            "price_type": "historical_ph_launch_price",
            "source_published_at": "2021-08-12",
            "excerpt": "NoypiGeeks reported TECNO Spark 7 3 GB / 64 GB available in the Philippines for PHP 4,990 via TECNO's official Shopee store.",
            "source_url": URL_NOYPI,
            "source_kind": "historical_local_launch_price",
            "observed_at": OBSERVED_AT,
            "local_availability_verified": True,
            "availability_status": "historical_launch_price_not_current",
        }],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 39 TECNO Spark 7 -> PH-reported 3 GB / 64 GB configuration",
        "configuration": variant["label"],
        "reviewedFields": len(record["fields"]),
        "philippineAvailabilityReportDate": "2021-08-12",
        "historicalLaunchPricePhp": 4990,
        "currentPrice": "not verified; left blank",
        "image": "neutral placeholder; reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
