#!/usr/bin/env python3
"""Record a source-backed review for the Cherry Mobile Aqua SV 5G row."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/cherry-mobile-aqua-sv-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_35bc65487e1514"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-8gb-128gb-ph"

URL_NTC = "https://www.ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/cherry-mobile-aqua-sv"
URL_YUGA_LAUNCH = "https://www.yugatech.com/mobile/cherry-mobile-aqua-sv-5g-aqua-s10-pro-price/"
URL_YUGA_HANDS_ON = "https://www.yugatech.com/news/cherry-mobile-aqua-sv-5g-w-dimensity-810-hands-on/"
URL_YUGA_PRICE_LIST = "https://www.yugatech.com/cherry-mobile-phone-price-list-philippines"
URL_BMPLUS = "https://businessmirror.com.ph/2022/05/06/cherry-mobile-aqua-sv-now-available-at-special-introductory-price-of-p9999/"
URL_MEDIATEK = "https://i.mediatek.com/dimensity-810"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None, source_kind: str | None = None) -> dict:
    item = {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}
    if source_kind:
        item["sourceKind"] = source_kind
    return item


SOURCES = [
    source("aqua_sv_ntc_gec_2022", "National Telecommunications Commission (NTC), Philippines", URL_NTC,
           "Philippine equipment-conformity evidence for the exact AQUA SV marketing name",
           "The official NTC 2022 Grant of Equipment Conformity list identifies CHERRY MOBILE AQUA SV as a smartphone. The public four-column list does not expose a numeric device model code or grant date in the entry, so neither is inferred."),
    source("aqua_sv_ptg_ph_specs", "Pinoy Techno Guide", URL_PTG,
           "Philippine-market launch/availability, listed 8 GB / 128 GB configuration, historical official price, and detailed local specification cross-check",
           "The exact-model page is dated April 29, 2022, states the phone is available in Cherry Mobile stores, authorized dealers, and online shops, and lists PHP 11,999. Its prose calls the 128 GB storage expandable but its specification table says expansion is none; that contradiction is retained. It reports Blue, while a contemporaneous launch announcement describes Luxe Green. No image is reused." ,
           "2022-04-29"),
    source("aqua_sv_yugatech_launch", "YugaTech Philippines", URL_YUGA_LAUNCH,
           "Contemporaneous Philippine launch, price, availability, and configuration cross-check",
           "YugaTech reported the Aqua SV 5G as part of Cherry Mobile's official Philippine 5G launch and listed the 8 GB / 128 GB model at PHP 11,999. The article is used as launch-era local reporting, not as a present-day price source.",
           "2022-04-29"),
    source("aqua_sv_yugatech_hands_on", "YugaTech Philippines", URL_YUGA_HANDS_ON,
           "Exact-model physical design and technical cross-check",
           "The hands-on identifies the Aqua SV 5G and reports its display, cameras, 8 GB LPDDR4X / 128 GB UFS 2.2, connectivity, Android 11, battery, dimensions, and weight. Its bottom-edge description identifies dual Nano-SIM, USB-C, microphone, and loudspeaker. It does not verify a microSD slot.",
           "2022-04-29"),
    source("aqua_sv_yugatech_historic_price_list", "YugaTech Philippines", URL_YUGA_PRICE_LIST,
           "Later dated historical price-list entry for price discrepancy review",
           "YugaTech's price list labels PHP 11,990 as verified on May 24, 2022. This differs by PHP 9 from the PHP 11,999 launch SRP reported at launch by PTG, YugaTech, and BMPlus. It is retained as a historical price-list candidate, not treated as a current offer or silently reconciled.",
           "2022-05-24", "historical_price_candidate"),
    source("aqua_sv_bmplus_intro_price", "BMPlus / BusinessMirror", URL_BMPLUS,
           "Historical Philippine SRP and dated Shopee introductory offer",
           "Published May 6, 2022, this local announcement says the original SRP was PHP 11,999 and the PHP 9,999 offer began May 8, 2022 as a one-day Shopee-exclusive deal. It also corroborates the 8 GB / 128 GB configuration. Neither amount is a current offer.",
           "2022-05-06", "historical_price_reference"),
    source("aqua_sv_mediatek_dimensity810", "MediaTek", URL_MEDIATEK,
           "Primary Dimensity 810 platform architecture and technology specifications",
           "MediaTek identifies the Dimensity 810 as a 6 nm platform with 2x Cortex-A76 up to 2.4 GHz, 6x Cortex-A55 up to 2 GHz, Mali-G57 MC2, LPDDR4X, UFS 2.2, Wi-Fi 5, and Bluetooth 5.1. Platform capabilities are applied only where the phone-specific local sources also identify the Dimensity 810 or the corresponding exact feature."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, price_type=None, catalog_value=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note,
            "configurationMatch": "Philippine Cherry Mobile Aqua SV 5G, 8 GB RAM / 128 GB storage; color is not used to distinguish a configuration"}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        item["unit"] = unit
    if price_type:
        item["priceType"] = price_type
    return item


def fields_for() -> list[dict]:
    # Deliberately retain unknowns and source conflicts; no specification is filled by inference.
    rows = [
        ("model_number", "aqua_sv_ntc_gec_2022", "The NTC 2022 GEC entry lists marketing name AQUA SV but does not show a numeric model code", None, "NOT_DISCLOSED", None, None, "No model code is inferred from the marketing name or chipset."),
        ("global_release_date", "aqua_sv_ptg_ph_specs", "The reviewed local announcement/page records a Philippine announcement on April 29, 2022; no exact global release date is supplied", None, "NOT_DISCLOSED", None, None, "Keep a global release date blank; the local announcement date is recorded separately."),
        ("configuration", "aqua_sv_ptg_ph_specs", "8 GB RAM / 128 GB storage", "8 GB RAM / 128 GB storage", "VERIFIED_SECONDARY", None, None, "PTG and contemporaneous YugaTech/BusinessMirror coverage agree on this Philippine configuration. No extra color-specific memory variants are established."),
        ("philippine_release_date", "aqua_sv_ptg_ph_specs", "PTG dated its exact-model page April 29, 2022 and says the model is available through Cherry Mobile stores, authorized dealers, and online shops", "2022-04-29", "VERIFIED_SECONDARY", None, None, "This is the dated Philippine launch/availability report, not an exact first transaction time. The May 8 Shopee offer is a later promotion."),
        ("official_launch_price_php", "aqua_sv_bmplus_intro_price", "Original Philippine SRP PHP 11,999", 11999, "VERIFIED_SECONDARY", None, "PHP", "Historical launch SRP for the 8 GB / 128 GB configuration; it is not today's price.", "historical_ph_official_launch_price"),
        ("current_price_php", "aqua_sv_ptg_ph_specs", "The reviewed references show 2022 price entries only; no current dated, orderable Philippine offer was verified", None, "PENDING_VERIFICATION", None, "PHP", "Keep current catalog price blank. Historical SRP, promotion, and YugaTech's PHP 11,990 dated price-list candidate remain in the price audit.", "no_current_offer_verified"),
        ("display_size", "aqua_sv_ptg_ph_specs", "6.6-inch display", 6.6, "VERIFIED_SECONDARY", "displayInches", "in", "Exact-model local coverage; YugaTech independently reports the same size."),
        ("display_technology", "aqua_sv_ptg_ph_specs", "AMOLED display", "AMOLED", "VERIFIED_SECONDARY", "displayType", None, "Local specification page; corroborated by YugaTech."),
        ("display_resolution", "aqua_sv_ptg_ph_specs", "FHD+ 1080 x 2400 pixels", "2400 x 1080", "VERIFIED_SECONDARY", "resolution", None, "Catalog stores height by width; source reports 1080 x 2400."),
        ("display_refresh_rate", "aqua_sv_ptg_ph_specs", "90 Hz", 90, "VERIFIED_SECONDARY", "refreshHz", "Hz", "PTG and YugaTech report 90 Hz."),
        ("display_brightness", "aqua_sv_ptg_ph_specs", "No brightness value recorded in the reviewed exact-model sources", None, "NOT_DISCLOSED", None, "nits", "Do not infer brightness from the panel type."),
        ("display_protection", "aqua_sv_yugatech_hands_on", "Corning Gorilla Glass 5", "Corning Gorilla Glass 5", "VERIFIED_SECONDARY", None, None, "Contemporaneous exact-model YugaTech hands-on; not a manufacturer specification page."),
        ("chipset", "aqua_sv_ptg_ph_specs", "MediaTek Dimensity 810", "MediaTek Dimensity 810", "VERIFIED_SECONDARY", "chipset", None, "Exact-model PTG and YugaTech coverage identify this chipset."),
        ("process_node", "aqua_sv_mediatek_dimensity810", "MediaTek Dimensity 810 is manufactured on a 6 nm process", "6 nm", "VERIFIED", None, "nm", "Chip-vendor platform detail, applied to the device's source-identified Dimensity 810."),
        ("cpu", "aqua_sv_mediatek_dimensity810", "2x Arm Cortex-A76 up to 2.4 GHz + 6x Arm Cortex-A55 up to 2 GHz", "8-core: 2x Cortex-A76 up to 2.4 GHz + 6x Cortex-A55 up to 2 GHz", "VERIFIED", "cpu", None, "MediaTek chipset specification; this is architecture data, not a benchmark."),
        ("gpu", "aqua_sv_mediatek_dimensity810", "Arm Mali-G57 MC2", "Arm Mali-G57 MC2", "VERIFIED", "gpu", None, "MediaTek chipset page and exact-model YugaTech report agree."),
        ("operating_system", "aqua_sv_ptg_ph_specs", "Android 11", "Android 11", "VERIFIED_SECONDARY", "os", None, "Launch-era version, not a claim about the version currently installed on every unit."),
        ("os_support", "aqua_sv_ptg_ph_specs", "No update duration, upgrade policy, or end-of-support date found in the reviewed references", None, "NOT_DISCLOSED", None, None, "No software-support commitment is inferred."),
        ("ram_capacity", "aqua_sv_ptg_ph_specs", "8 GB RAM", 8, "VERIFIED_SECONDARY", "ramGb", "GB", "Matches the single supported Philippine configuration."),
        ("ram_type", "aqua_sv_yugatech_hands_on", "8 GB LPDDR4X RAM", "LPDDR4X", "VERIFIED_SECONDARY", "ramType", None, "YugaTech reports LPDDR4X; MediaTek lists LPDDR4X platform support."),
        ("storage_capacity", "aqua_sv_ptg_ph_specs", "128 GB storage", 128, "VERIFIED_SECONDARY", "storageGb", "GB", "Matches the single supported Philippine configuration."),
        ("storage_type", "aqua_sv_yugatech_hands_on", "128 GB UFS 2.2 storage", "UFS 2.2", "VERIFIED_SECONDARY", "storageType", None, "YugaTech identifies UFS 2.2; MediaTek lists UFS 2.2 platform support."),
        ("storage_expansion", "aqua_sv_ptg_ph_specs", "PTG narrative says expandable storage; its specifications table says Expansion: None. YugaTech's exact-model hands-on lists the SIM tray but does not verify microSD", None, "CONFLICTING_INFORMATION", None, None, "The exact-model source contradicts itself. Keep expansion unresolved and do not assert a microSD slot."),
        ("rear_camera_system", "aqua_sv_ptg_ph_specs", "64 MP main + 5 MP ultrawide + 2 MP depth + 2 MP macro", "64 MP main + 5 MP ultrawide + 2 MP depth + 2 MP macro", "VERIFIED_SECONDARY", "rearCameraMp", "MP", "PTG and YugaTech list the same four rear modules; the catalog numeric value represents the main camera."),
        ("main_camera_sensor", "aqua_sv_ptg_ph_specs", "64 MP autofocus main camera; sensor maker and model not stated", "64 MP autofocus; sensor model not disclosed", "VERIFIED_SECONDARY", None, None, "Do not infer the sensor identity from resolution."),
        ("ultrawide_camera", "aqua_sv_ptg_ph_specs", "5 MP ultrawide camera", "5 MP ultrawide", "VERIFIED_SECONDARY", None, "MP", "Exact-model local specification."),
        ("telephoto_camera", "aqua_sv_ptg_ph_specs", "The complete listed rear system contains main, ultrawide, depth, and macro cameras; no telephoto module is listed", "No telephoto camera listed", "NOT_APPLICABLE", None, None, "Based on the complete four-module camera list."),
        ("front_camera", "aqua_sv_ptg_ph_specs", "16 MP main + 2 MP depth front cameras", 16, "VERIFIED_SECONDARY", "frontCameraMp", "MP", "Catalog numeric value records the main front camera resolution."),
        ("video_recording", "aqua_sv_ptg_ph_specs", "Rear video recording up to 4K; exact frame rates and complete mode list are not recorded", "Rear video up to 4K; frame rates not recorded", "VERIFIED_SECONDARY", "video", None, "Do not expand this into unlisted resolutions or frame rates."),
        ("battery_capacity", "aqua_sv_ptg_ph_specs", "4,200 mAh", 4200, "VERIFIED_SECONDARY", "batteryMah", "mAh", "PTG and YugaTech agree."),
        ("battery_technology", "aqua_sv_ptg_ph_specs", "Li-Po battery; non-removable", "Lithium-polymer; non-removable", "VERIFIED_SECONDARY", None, None, "Exact-model PTG specification."),
        ("wired_charging", "aqua_sv_ptg_ph_specs", "30 W wired fast charging", 30, "VERIFIED_SECONDARY", "chargingW", "W", "PTG and YugaTech agree."),
        ("wireless_charging", "aqua_sv_ptg_ph_specs", "Wireless and reverse wireless charging are not mentioned in the reviewed sources", None, "NOT_DISCLOSED", None, None, "Silence is not treated as proof that charging hardware is absent."),
        ("dimensions", "aqua_sv_yugatech_hands_on", "160.5 x 73.8 x 8.8 mm", "160.5 x 73.8 x 8.8 mm", "VERIFIED_SECONDARY", "dimensions", "mm", "YugaTech's exact-model specification list."),
        ("weight", "aqua_sv_yugatech_hands_on", "175 g", 175, "VERIFIED_SECONDARY", "weightG", "g", "YugaTech's exact-model specification list."),
        ("materials", "aqua_sv_ptg_ph_specs", "PTG says plastic back with faux-leather texture; the May 2022 local promotion calls it a leather back", None, "CONFLICTING_INFORMATION", None, None, "The back-cover material description differs. YugaTech describes a metallic frame; other frame materials remain unrecorded."),
        ("ingress_protection", "aqua_sv_ptg_ph_specs", "No IP rating or water-resistance certification is stated in the reviewed sources", None, "NOT_DISCLOSED", None, None, "No ingress-protection rating is inferred."),
        ("sim_esim", "aqua_sv_yugatech_hands_on", "Dual Nano-SIM; eSIM is not mentioned", "Dual Nano-SIM; eSIM not disclosed", "VERIFIED_SECONDARY", "sim", None, "YugaTech describes the exact-model tray for two Nano-SIM cards."),
        ("cellular_bands", "aqua_sv_ptg_ph_specs", "5G, 4G LTE, 3G HSPA+, and 2G EDGE/GPRS; exact band list not recorded", "5G / 4G LTE / 3G HSPA+ / 2G; bands not recorded", "VERIFIED_SECONDARY", "cellular", None, "Technology generations only; do not infer regional band compatibility."),
        ("wifi", "aqua_sv_ptg_ph_specs", "Dual-band Wi-Fi 802.11 b/g/n/ac", "Dual-band Wi-Fi 5 (802.11 a/b/g/n/ac)", "VERIFIED_SECONDARY", "wifi", None, "PTG exact-model page; chipset capability corroborates Wi-Fi 5."),
        ("bluetooth", "aqua_sv_ptg_ph_specs", "Bluetooth 5.1", "Bluetooth 5.1", "VERIFIED_SECONDARY", None, None, "Exact-model PTG and chipset page agree."),
        ("usb", "aqua_sv_yugatech_hands_on", "USB Type-C; PTG lists USB OTG support", "USB Type-C; OTG", "VERIFIED_SECONDARY", "ports", None, "YugaTech identifies USB-C; PTG says OTG is supported."),
        ("nfc", "aqua_sv_ptg_ph_specs", "NFC: No", False, "VERIFIED_SECONDARY", None, None, "Explicit negative value in the exact-model local specification table."),
        ("gnss", "aqua_sv_ptg_ph_specs", "GPS with A-GPS, GLONASS, Galileo, BeiDou, and QZSS", "GPS, A-GPS, GLONASS, Galileo, BeiDou, QZSS", "VERIFIED_SECONDARY", None, None, "Exact-model local specification."),
        ("audio", "aqua_sv_yugatech_hands_on", "YugaTech describes a bottom loudspeaker, microphone, and USB-C; speaker channel configuration and headphone jack are not recorded", "Loudspeaker; channel count and headphone jack not disclosed", "VERIFIED_SECONDARY", "sound", None, "No stereo-speaker or 3.5 mm-jack claim is inferred."),
        ("sensors", "aqua_sv_ptg_ph_specs", "Gyroscope, compass, ambient-light sensor, proximity sensor, accelerometer, and under-display fingerprint sensor", "Gyroscope, compass, ambient light, proximity, accelerometer, under-display fingerprint", "VERIFIED_SECONDARY", None, None, "PTG exact-model sensor and biometric listing."),
    ]
    result = [field(fid, sid, value, normalized, status=status, key=key, unit=unit, note=note,
                    price_type=optional[0] if optional else None,
                    catalog_value=64 if fid == "rear_camera_system" else None)
              for fid, sid, value, normalized, status, key, unit, note, *optional in rows]
    if len(result) != 46:
        raise ValueError(f"Expected 46 reviewed smartphone fields, got {len(result)}")
    source_ids = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in result} - source_ids)
    if missing:
        raise ValueError(f"Fields reference undefined sources: {missing}")
    return result


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine availability reported by PTG through Cherry Mobile stores, authorized dealers, and online shops; the NTC lists Cherry Mobile AQUA SV as a smartphone. Workbook eligibility remains Pending.",
        "philippineAvailability": "Exact AQUA SV identity is supported by the NTC 2022 GEC list. PTG's April 29, 2022 exact-model page reports availability through Cherry Mobile stores, authorized dealers, and online shops; the May 2022 promotion reports a Shopee offer. This verifies local-market availability, not an exact first-sale transaction time.",
        "observedAt": OBSERVED,
        "manufacturer": "Cherry Mobile",
        "catalogModel": "Aqua SV 5G",
        "productLine": "Cherry Mobile Aqua SV",
        "modelNumber": None,
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Philippine launch/availability report date",
        "researchNotes": "Matched to Cherry Mobile Aqua SV 5G; NTC uses AQUA SV. One documented Philippine configuration is 8 GB / 128 GB. Scope eligibility remains Pending. Exact model code, global release date, current price, storage expansion, color, and image reuse rights remain unresolved.",
        "qualityFlag": "Aqua SV 5G matched; model code, global date, current price, storage expansion, color, and image rights unresolved.",
        "openIssues": [
            {"issue": "The NTC public list gives the AQUA SV marketing name but no numeric model code in its published row", "action": "Keep modelNumber blank until a reliable exact product code is found."},
            {"issue": "PTG's Aqua SV page says storage is expandable in its prose but lists expansion as None in its table", "action": "Keep storage expansion unresolved; do not claim a microSD slot."},
            {"issue": "Color evidence differs: PTG lists Blue while a contemporaneous local announcement describes Luxe Green", "action": "Do not assign a single color or split the 8 GB / 128 GB configuration by color without authoritative variant evidence."},
            {"issue": "Only launch-era prices were found; no current dated, orderable Philippine offer was verified", "action": "Show current price as not recorded and keep PHP 11,999 / PHP 9,999 as historical references only."},
            {"issue": "Exact-model product images have no recorded reusable license", "action": "Continue using the neutral image placeholder until documented image permission is available."},
            {"issue": "The workbook scope and study eligibility status remains Pending", "action": "Preserve Pending and do not admit the device to eligibility-filtered results outside existing study rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "cherry mobile"
            or device.get("model") != "Aqua SV 5G"):
        raise ValueError("Inventory row no longer matches Cherry Mobile Aqua SV 5G")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") not in {OLD_CONFIG, CONFIG}:
        raise ValueError("Expected the original placeholder or this review's configuration")

    variant = {
        "id": CONFIG,
        "label": "8 GB RAM / 128 GB storage",
        "sku": None,
        "modelCode": None,
        "notes": "Single source-supported Philippine configuration. PTG lists Blue, while contemporaneous launch coverage describes Luxe Green; color is unresolved and is not used to split the configuration.",
        "workbookRow": 71,
    }
    record = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "Cherry Mobile",
        "model": "Aqua SV 5G",
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
        "reason": "Exact Aqua SV product images appear on local reference or merchant pages, but no reusable image license or written permission is recorded. Do not embed or hotlink an unlicensed image.",
        "sourcePage": URL_PTG,
        "assetUrl": None,
        "scope": "Cherry Mobile Aqua SV 5G, 8 GB / 128 GB; color evidence is conflicting",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Cherry Mobile Aqua SV 5G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 11999, "configuration_id": CONFIG,
         "configuration_match": "exact_model_and_8gb_128gb_configuration", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "historical_ph_official_launch_srp", "source_published_at": "2022-04-29",
         "excerpt": "PTG's exact-model Philippine page lists the official price as PHP 11,999; BMPlus calls PHP 11,999 the original SRP.",
         "source_url": URL_PTG, "source_kind": "historical_local_price_reference",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_srp_not_current"},
        {"device_id": DEVICE, "amount_php": 9999, "configuration_id": CONFIG,
         "configuration_match": "exact_model_and_8gb_128gb_configuration", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "historical_one_day_shopee_introductory_promotion", "source_published_at": "2022-05-06",
         "excerpt": "BMPlus announced a PHP 9,999 one-day Shopee-exclusive offer beginning May 8, 2022. This promotion is not current.",
         "source_url": URL_BMPLUS, "source_kind": "historical_local_promotion_reference",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_promotion_not_current"},
        {"device_id": DEVICE, "amount_php": 11990, "configuration_id": CONFIG,
         "configuration_match": "exact_model_historical_price_list_entry_configuration_not_repeated", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "historical_yugatech_price_list_candidate_not_launch_srp", "source_published_at": "2022-05-24",
         "excerpt": "YugaTech labels PHP 11,990 as verified May 24, 2022. This differs from launch-era PHP 11,999 reports and is retained without selecting it as the official launch SRP.",
         "source_url": URL_YUGA_PRICE_LIST, "source_kind": "historical_price_list_candidate",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_price_list_entry_not_current"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Cherry Mobile", "model_name": "Aqua SV 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "Exact local page confirms historical PHP 11,999 official price and reports the model available through Cherry Mobile stores, authorized dealers, and online shops."},
            {"device_id": DEVICE, "source_url": URL_BMPLUS, "result": "Dated May 2022 source confirms the original PHP 11,999 SRP and a one-day PHP 9,999 Shopee promotion; neither is a current offer."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Cherry Mobile Aqua SV workbook row -> Aqua SV 5G; NTC marketing name AQUA SV",
        "configuration": variant["label"],
        "reviewedFields": len(record["fields"]),
        "philippineAvailabilityReportDate": "2022-04-29",
        "historicalLaunchSrpPhp": 11999,
        "historicalPromoPhp": 9999,
        "currentPrice": "blank; launch-era references only",
        "image": "neutral placeholder; image reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
