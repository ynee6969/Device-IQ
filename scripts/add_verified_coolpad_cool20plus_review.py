#!/usr/bin/env python3
"""Record a source-backed Philippine review for Coolpad COOL 20+."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/coolpad-cool20plus-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_14031d3cddb48d"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-6gb-128gb-ph"

URL_COOLPAD = "https://www.coolpad.com/#/product/COOL20p"
URL_YUGA_LAUNCH = "https://www.yugatech.com/mobile/coolpad-cp12-and-cool-20-smartphones-now-available-in-the-philippines/"
URL_YUGA_PRICE_LIST = "https://www.yugatech.com/smartphone-price-list-in-the-philippines-2023/"
URL_NOYPI = "https://www.noypigeeks.com/android/coolpad-cool-20-plus/"
URL_MEDIATEK = "https://www.mediatek.com/products/smartphones/mediatek-helio-g85"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("cool20plus_coolpad_global_page", "Coolpad Global", URL_COOLPAD,
           "Official product-page check for exact model identity",
           "The manufacturer COOL20p product URL was opened, but the page returned no readable product text in this review. It is recorded as an attempted primary reference only; no field value is promoted from it."),
    source("cool20plus_yugatech_ph_launch", "YugaTech Philippines", URL_YUGA_LAUNCH,
           "Philippine availability, launch configuration and price, and exact-model technical review",
           "Published October 5, 2023, this local report says Coolpad brought the COOL 20+ to the Philippines and lists the 6 GB / 128 GB model at PHP 5,699. Its detailed model table lists Helio G85, while an earlier summary paragraph says G58; the summary typo is retained in the audit note. The page images depict the model but carry no recorded reuse permission.",
           "2023-10-05"),
    source("cool20plus_yugatech_2023_price_list", "YugaTech Philippines", URL_YUGA_PRICE_LIST,
           "Independent dated Philippine price/configuration cross-check",
           "YugaTech's 2023 Philippine price list records the Coolpad COOL 20 Plus at PHP 5,699 for 6 GB / 128 GB in October 2023. This is a historical launch-era price, not a current listing."),
    source("cool20plus_noypi_launch", "NoypiGeeks Philippines", URL_NOYPI,
           "Philippine launch, exact local configuration, price, and specification cross-check",
           "Published October 5, 2023, this page reports local availability and PHP 5,699 for 6 GB / 128 GB. Its detailed specifications say Helio G85, while its opening paragraph says G95; the differing summary is documented. It lists the GPU as Mali-G52 MC3, which conflicts with YugaTech and MediaTek's G85 specification of Mali-G52 MC2.",
           "2023-10-05"),
    source("cool20plus_mediatek_helio_g85", "MediaTek", URL_MEDIATEK,
           "Primary chipset-family specification for Helio G85 CPU, GPU, memory and interfaces",
           "MediaTek identifies the Helio G85's two Cortex-A75 cores up to 2 GHz, six Cortex-A55 cores up to 1.8 GHz, Mali-G52 MC2 GPU, LPDDR4X memory support, eMMC 5.1, Wi-Fi 5, and Bluetooth 5.0. Platform capabilities are applied only where the exact-model local report also identifies the corresponding feature. MediaTek's page does not state the manufacturing process node."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, price_type=None, catalog_value=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note,
            "configurationMatch": "Philippine Coolpad COOL 20+, 6 GB RAM / 128 GB storage"}
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
        ("model_number", "cool20plus_coolpad_global_page", "The readable Coolpad product page did not expose a model code; local sources use COOL 20+ / Cool 20 Plus", None, "NOT_DISCLOSED", None, None, "Do not infer a model code from the separate Coolpad CP12."),
        ("global_release_date", "cool20plus_coolpad_global_page", "No exact global release date was verifiable from the manufacturer page; secondary date references vary by market and source", None, "NOT_DISCLOSED", None, None, "Leave the global date unset. The 2023 workbook year is retained as a claim; this field is not a first-sale date."),
        ("configuration", "cool20plus_yugatech_ph_launch", "Philippine COOL 20+ listing: 6 GB RAM / 128 GB storage", "6 GB RAM / 128 GB storage", "VERIFIED_SECONDARY", None, None, "YugaTech identifies this exact local configuration at PHP 5,699. Other non-PH memory options are not imported as local variants."),
        ("philippine_release_date", "cool20plus_yugatech_ph_launch", "YugaTech dated its report saying the COOL 20+ was now available in the Philippines October 5, 2023", "2023-10-05", "VERIFIED_SECONDARY", None, None, "This is a dated local availability report, not an exact first transaction time."),
        ("official_launch_price_php", "cool20plus_yugatech_ph_launch", "Philippine price for the 6 GB / 128 GB model: PHP 5,699", 5699, "VERIFIED_SECONDARY", None, "PHP", "Historical launch-era price corroborated by YugaTech's 2023 price list and NoypiGeeks; not a current price.", "historical_ph_launch_price"),
        ("current_price_php", "cool20plus_yugatech_ph_launch", "The reviewed Philippine price references are dated 2023; no current dated, orderable offer was verified", None, "PENDING_VERIFICATION", None, "PHP", "Keep the current catalog price blank. PHP 5,699 is retained only as a historical launch reference.", "no_current_offer_verified"),
        ("display_size", "cool20plus_yugatech_ph_launch", "6.517-inch waterdrop display; other local coverage rounds this to 6.52 inches", 6.52, "VERIFIED_SECONDARY", "displayInches", "in", "Store the exact-model display size using the common 6.52-inch rounded value."),
        ("display_technology", "cool20plus_noypi_launch", "6.52-inch IPS display", "IPS LCD", "VERIFIED_SECONDARY", "displayType", None, "Exact-model local specification; YugaTech does not identify the panel technology."),
        ("display_resolution", "cool20plus_yugatech_ph_launch", "HD+ 1600 x 720 pixels", "1600 x 720", "VERIFIED_SECONDARY", "resolution", None, "YugaTech and NoypiGeeks agree on the HD+ resolution."),
        ("display_refresh_rate", "cool20plus_yugatech_ph_launch", "Refresh rate not stated in the reviewed local model-specific sources", None, "NOT_DISCLOSED", None, "Hz", "Do not assume 60 Hz from the panel class."),
        ("display_brightness", "cool20plus_yugatech_ph_launch", "No brightness value recorded", None, "NOT_DISCLOSED", None, "nits", "No numeric brightness specification is inferred."),
        ("display_protection", "cool20plus_yugatech_ph_launch", "No cover-glass type or protection rating recorded", None, "NOT_DISCLOSED", None, None, "Keep display protection blank."),
        ("chipset", "cool20plus_yugatech_ph_launch", "The detailed COOL 20+ spec list says MediaTek Helio G85; one summary says G58, and NoypiGeeks' opening says G95 while its detailed list says G85", "MediaTek Helio G85", "VERIFIED_SECONDARY", "chipset", None, "The two exact-model structured specification lists identify G85 and the manufacturer provides official G85 platform specifications. The inconsistent summary paragraphs are retained as documented source errors, not silently copied."),
        ("process_node", "cool20plus_mediatek_helio_g85", "The reviewed MediaTek product page does not state the Helio G85 process node", None, "NOT_DISCLOSED", None, "nm", "Do not fill a process node from unrelated chipset databases."),
        ("cpu", "cool20plus_mediatek_helio_g85", "2x Arm Cortex-A75 up to 2.0 GHz + 6x Arm Cortex-A55 up to 1.8 GHz", "8-core: 2x Cortex-A75 up to 2.0 GHz + 6x Cortex-A55 up to 1.8 GHz", "VERIFIED", "cpu", None, "MediaTek's Helio G85 specification; this is platform architecture, not a benchmark."),
        ("gpu", "cool20plus_mediatek_helio_g85", "MediaTek specifies Arm Mali-G52 MC2; YugaTech reports MC2, while NoypiGeeks reports MC3", "Arm Mali-G52 MC2", "VERIFIED", "gpu", None, "The chipset vendor's specification resolves the GPU-core variant; the NoypiGeeks MC3 entry remains documented as a conflicting secondary value."),
        ("operating_system", "cool20plus_yugatech_ph_launch", "Android 11", "Android 11", "VERIFIED_SECONDARY", "os", None, "Launch-era OS, not a claim about the current software on every unit."),
        ("os_support", "cool20plus_yugatech_ph_launch", "No update policy, duration, or end-of-support date found", None, "NOT_DISCLOSED", None, None, "No software-support commitment is inferred."),
        ("ram_capacity", "cool20plus_yugatech_ph_launch", "6 GB RAM for the Philippine 128 GB configuration", 6, "VERIFIED_SECONDARY", "ramGb", "GB", "The local launch report prices 6 GB / 128 GB; other generic memory options are not added as PH variants."),
        ("ram_type", "cool20plus_mediatek_helio_g85", "The G85 platform supports LPDDR4X, but the local product report does not identify the phone's installed RAM type", None, "NOT_DISCLOSED", None, None, "A chipset capability alone does not establish the installed memory type."),
        ("storage_capacity", "cool20plus_yugatech_ph_launch", "128 GB storage for the Philippine configuration", 128, "VERIFIED_SECONDARY", "storageGb", "GB", "Exact local 6 GB / 128 GB configuration."),
        ("storage_type", "cool20plus_mediatek_helio_g85", "MediaTek lists eMMC 5.1 support for the G85 platform; the reviewed model-specific reports do not state the installed storage interface", None, "NOT_DISCLOSED", None, None, "Do not infer the phone's storage interface from SoC capability."),
        ("storage_expansion", "cool20plus_yugatech_ph_launch", "YugaTech and NoypiGeeks list a microSD card slot for the COOL 20+", "microSD supported; maximum capacity not verified for the Philippine SKU", "VERIFIED_SECONDARY", None, None, "The local spec lists support but does not state a local maximum capacity or SIM-tray arrangement."),
        ("rear_camera_system", "cool20plus_yugatech_ph_launch", "48 MP AI main camera plus a secondary depth camera; the secondary module resolution is not stated", "48 MP main + depth camera; secondary resolution not recorded", "VERIFIED_SECONDARY", "rearCameraMp", None, "The catalog numeric value represents the main camera resolution."),
        ("main_camera_sensor", "cool20plus_yugatech_ph_launch", "48 MP main camera; sensor make, model, and aperture not recorded by the reviewed local source", "48 MP main; sensor model not disclosed", "VERIFIED_SECONDARY", None, None, "No sensor identity is inferred from resolution."),
        ("ultrawide_camera", "cool20plus_yugatech_ph_launch", "The complete listed rear camera system is 48 MP main plus depth; no ultrawide module is listed", "No ultrawide camera listed", "NOT_APPLICABLE", None, None, "Based on the complete two-module camera description."),
        ("telephoto_camera", "cool20plus_yugatech_ph_launch", "The complete listed rear camera system is 48 MP main plus depth; no telephoto module is listed", "No telephoto camera listed", "NOT_APPLICABLE", None, None, "Based on the complete two-module camera description."),
        ("front_camera", "cool20plus_yugatech_ph_launch", "5 MP selfie camera", 5, "VERIFIED_SECONDARY", "frontCameraMp", "MP", "Exact-model local spec list."),
        ("video_recording", "cool20plus_yugatech_ph_launch", "Video mode and frame rate not recorded in the reviewed exact-model local sources", None, "NOT_DISCLOSED", None, None, "Do not infer supported video modes from chipset capabilities."),
        ("battery_capacity", "cool20plus_yugatech_ph_launch", "4,500 mAh", 4500, "VERIFIED_SECONDARY", "batteryMah", "mAh", "The exact-model YugaTech spec table lists 4,500 mAh; NoypiGeeks corroborates."),
        ("battery_technology", "cool20plus_yugatech_ph_launch", "Battery chemistry is not specified in the reviewed local sources", None, "NOT_DISCLOSED", None, None, "Do not infer Li-ion or Li-Po chemistry."),
        ("wired_charging", "cool20plus_noypi_launch", "10 W wired charging", 10, "VERIFIED_SECONDARY", "chargingW", "W", "NoypiGeeks' exact-model PH specification list."),
        ("wireless_charging", "cool20plus_yugatech_ph_launch", "Wireless and reverse wireless charging not stated in the reviewed local sources", None, "NOT_DISCLOSED", None, None, "Silence is not treated as confirmation of hardware absence."),
        ("dimensions", "cool20plus_yugatech_ph_launch", "164.3 x 75.66 x 8.65 mm; NoypiGeeks rounds to 164.3 x 75.7 x 8.7 mm", "164.3 x 75.66 x 8.65 mm", "VERIFIED_SECONDARY", "dimensions", "mm", "Use the exact YugaTech values for this Philippine listing and retain the rounded secondary rendering."),
        ("weight", "cool20plus_yugatech_ph_launch", "197 g; NoypiGeeks gives 197.1 g", 197, "VERIFIED_SECONDARY", "weightG", "g", "Local reports differ only in precision."),
        ("materials", "cool20plus_yugatech_ph_launch", "Reviewed YugaTech local specs do not state chassis materials; NoypiGeeks relays a company claim of a glass back but no model-specific manufacturer text could be read", None, "NOT_DISCLOSED", None, None, "Keep material claims blank until a usable primary source is available."),
        ("ingress_protection", "cool20plus_yugatech_ph_launch", "No IP rating or water-resistance certification recorded", None, "NOT_DISCLOSED", None, None, "No protection rating is inferred."),
        ("sim_esim", "cool20plus_yugatech_ph_launch", "Dual-SIM; eSIM not stated", "Dual-SIM; eSIM not disclosed", "VERIFIED_SECONDARY", "sim", None, "Exact-model local spec list."),
        ("cellular_bands", "cool20plus_yugatech_ph_launch", "HSPA+ and 4G LTE; exact device radio-band list is not recorded", "HSPA+ / 4G LTE; exact bands not recorded", "VERIFIED_SECONDARY", "cellular", None, "Do not infer band compatibility from the generic SoC specification."),
        ("wifi", "cool20plus_yugatech_ph_launch", "Wi-Fi 802.11 a/b/g/n/ac", "Wi-Fi 5 (802.11 a/b/g/n/ac)", "VERIFIED_SECONDARY", "wifi", None, "YugaTech exact-model list; MediaTek confirms Wi-Fi 5 platform capability."),
        ("bluetooth", "cool20plus_yugatech_ph_launch", "Bluetooth 5.0", "Bluetooth 5.0", "VERIFIED_SECONDARY", None, None, "Exact-model YugaTech list; chipset vendor corroborates the platform capability."),
        ("usb", "cool20plus_yugatech_ph_launch", "USB Type-C; OTG support not stated", "USB Type-C; data standard and OTG not disclosed", "VERIFIED_SECONDARY", "ports", None, "Do not infer USB version or OTG from the connector."),
        ("nfc", "cool20plus_yugatech_ph_launch", "NFC support not stated in the reviewed Philippine launch/spec sources", None, "NOT_DISCLOSED", None, None, "No negative NFC claim is inferred."),
        ("gnss", "cool20plus_yugatech_ph_launch", "GPS/A-GPS, GLONASS, BeiDou, Galileo, and QZSS", "GPS, A-GPS, GLONASS, BeiDou, Galileo, QZSS", "VERIFIED_SECONDARY", None, None, "YugaTech exact-model local specification."),
        ("audio", "cool20plus_yugatech_ph_launch", "3.5 mm headphone jack listed; loudspeaker configuration not stated", "3.5 mm headphone jack; speaker configuration not disclosed", "VERIFIED_SECONDARY", "sound", None, "No mono/stereo claim is inferred."),
        ("sensors", "cool20plus_yugatech_ph_launch", "Side-mounted fingerprint reader and face unlock listed; other sensors not listed", "Side fingerprint reader; face unlock; other sensors not recorded", "VERIFIED_SECONDARY", None, None, "Only explicitly listed authentication features are recorded."),
    ]
    result = [field(fid, sid, value, normalized, status=status, key=key, unit=unit,
                    note=note, price_type=optional[0] if optional else None,
                    catalog_value=48 if fid == "rear_camera_system" else None)
              for fid, sid, value, normalized, status, key, unit, note, *optional in rows]
    if len(result) != 46:
        raise ValueError(f"Expected 46 smartphone fields, got {len(result)}")
    known = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in result} - known)
    if missing:
        raise ValueError(f"Fields reference undefined sources: {missing}")
    return result


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "YugaTech and NoypiGeeks reported the COOL 20+ as locally introduced/available in the Philippines on October 5, 2023. Workbook eligibility remains Pending.",
        "philippineAvailability": "YugaTech and NoypiGeeks both reported the Coolpad COOL 20+ available in the Philippines in launch coverage dated October 5, 2023, including a Philippine 6 GB / 128 GB configuration and local price. This verifies a Philippine-market launch report, not the exact first transaction time.",
        "observedAt": OBSERVED,
        "manufacturer": "Coolpad",
        "catalogModel": "COOL 20+",
        "productLine": "Coolpad COOL 20+",
        "modelNumber": None,
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Philippine availability report date",
        "researchNotes": "Workbook label Coolpad Cool 20 Plus is matched to COOL 20+ in contemporaneous local launch reporting. One source-supported local configuration: 6 GB / 128 GB. Scope eligibility remains Pending. Exact model code, global release date, current price, memory type, storage type, process node, and image reuse remain unresolved.",
        "qualityFlag": "COOL 20+ matched; model code, exact global date, current price, several technical fields, and image rights unresolved.",
        "openIssues": [
            {"issue": "The reviewed Coolpad global product URL returned no readable specification text and local references show no numeric device model code", "action": "Keep modelNumber blank until the manufacturer or an official label supplies an exact code."},
            {"issue": "YugaTech and NoypiGeeks contain conflicting chipset names in opening summary text, though both detailed tables list Helio G85", "action": "Use the detailed local spec tables and MediaTek's official Helio G85 platform data; preserve the contradictory summary text in provenance."},
            {"issue": "NoypiGeeks lists Mali-G52 MC3 while YugaTech and MediaTek list Mali-G52 MC2", "action": "Use MediaTek's primary chipset specification for MC2 and retain the secondary discrepancy in the field audit."},
            {"issue": "No current dated, orderable Philippine offer was verified", "action": "Keep the current price blank and retain PHP 5,699 as a 2023 historical launch price."},
            {"issue": "Exact-model product images have no recorded reusable license", "action": "Use the neutral placeholder until documented reuse permission is established."},
            {"issue": "Workbook scope/eligibility remains Pending", "action": "Preserve Pending and follow existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "coolpad"
            or device.get("model") != "Cool 20 Plus"):
        raise ValueError("Inventory row no longer matches Coolpad Cool 20 Plus")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") not in {OLD_CONFIG, CONFIG}:
        raise ValueError("Expected the original placeholder or this review's configuration")

    variant = {
        "id": CONFIG,
        "label": "6 GB RAM / 128 GB storage",
        "sku": None,
        "modelCode": None,
        "notes": "Philippine launch coverage identifies this as the 6 GB / 128 GB local configuration. No model code is recorded.",
        "workbookRow": 133,
    }
    record = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "Coolpad",
        "model": "COOL 20+",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
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
        "reason": "Exact COOL 20+ images appear in YugaTech's local launch article, but the page does not record reusable image terms or written permission. Do not embed or hotlink an unlicensed image.",
        "sourcePage": URL_YUGA_LAUNCH,
        "assetUrl": None,
        "scope": "Coolpad COOL 20+ Philippine 6 GB / 128 GB configuration",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Coolpad COOL 20+",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [{
        "device_id": DEVICE, "amount_php": 5699, "configuration_id": CONFIG,
        "configuration_match": "exact_philippine_6gb_128gb_configuration", "variant_ram_gb": 6, "variant_storage_gb": 128,
        "price_type": "historical_ph_launch_price", "source_published_at": "2023-10-05",
        "excerpt": "YugaTech reported PHP 5,699 for the COOL 20+ 6 GB / 128 GB configuration at Philippine launch; its 2023 price list corroborates the amount.",
        "source_url": URL_YUGA_LAUNCH, "source_kind": "historical_local_launch_price",
        "observed_at": OBSERVED_AT, "local_availability_verified": True,
        "availability_status": "historical_launch_price_not_current",
    }]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Coolpad", "model_name": "COOL 20+", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_YUGA_LAUNCH, "result": "Philippine launch coverage lists PHP 5,699 for the exact 6 GB / 128 GB configuration; historical only."},
            {"device_id": DEVICE, "source_url": URL_YUGA_PRICE_LIST, "result": "YugaTech's 2023 Philippine price list corroborates the PHP 5,699 / 6 GB / 128 GB listing for October 2023."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Coolpad Cool 20 Plus workbook row -> Philippine COOL 20+",
        "configuration": variant["label"],
        "reviewedFields": len(record["fields"]),
        "philippineAvailabilityReportDate": "2023-10-05",
        "historicalLaunchPricePhp": 5699,
        "currentPrice": "blank; 2023 launch price only",
        "image": "neutral placeholder; reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
