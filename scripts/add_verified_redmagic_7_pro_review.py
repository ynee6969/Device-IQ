#!/usr/bin/env python3
"""Record sourced Philippine configuration evidence for REDMAGIC 7 Pro."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/redmagic-7-pro-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_5e189eced7d16d"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_GLOBAL = "https://global.redmagic.gg/blogs/press/redmagic-7-pro-review-on-sale-in-international-markets"
URL_GLOBAL_PRESS = "https://global.redmagic.gg/blogs/press/redmagic-7-pro-review-on-sale-in-international-markets"
URL_GLOBAL_ANNOUNCE = "https://global.redmagic.gg/blogs/news/pro-vision-gaming-is-almost-here"
URL_UNBOX = "https://unbox.ph/gadget/red-magic-7-pro-goes-global-whats-different/"
URL_GIZGUIDE = "https://www.gizguide.com/2022/04/redmagic-7-pro-arrives-in-philippines.html"
URL_NOYPI = "https://www.noypigeeks.com/android/redmagic-7-pro-philippines/"
URL_YUGA = "https://www.yugatech.com/mobile/smartphone-price-list-philippines-2022/"
URL_YUGA_SPECS = "https://www.yugatech.com/mobile/nubia-redmagic-7-pro-launched-globally/"
URL_MANILASHAKER = "https://manilashaker.com/nubia-redmagic-7-pro-5g-specs-price-philippines/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-gen-1-mobile-platform"
URL_QUALCOMM_BRIEF = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/snapdragon-8-gen-1-mobile-platform-product-brief.pdf"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/zte-nubia-red-magic-7-pro"
URL_NANOREVIEW_SOC = "https://nanoreview.net/en/soc/qualcomm-snapdragon-8-gen-1"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-nubia-red-magic-7-pro"
URL_GSMARENA = "https://www.gsmarena.com/zte_nubia_red_magic_7_pro-11364.php"
URL_APTX = "https://www.aptx.com/products/redmagic-nx709j"

CONFIGS = [
    {"id": f"{DEVICE}-16gb-256gb-ph", "label": "16 GB RAM / 256 GB storage (Obsidian)",
     "ram": 16, "storage": 256, "color": "Obsidian", "launch": 45999},
    {"id": f"{DEVICE}-16gb-512gb-ph", "label": "16 GB RAM / 512 GB storage (Supernova)",
     "ram": 16, "storage": 512, "color": "Supernova", "launch": 49999},
]


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("redmagic_7_pro_ntc", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and exact model-name match",
           "The NTC 2022 GEC lists REDMAGIC model NX709J as REDMAGIC 7 Pro. Registration supports the model identity in the Philippine regulatory record; it does not by itself prove a retail configuration."),
    source("redmagic_7_pro_global", "REDMAGIC Global", URL_GLOBAL,
           "Official international-version hardware, software, and release cross-check",
           "REDMAGIC's international-version launch recap distinguishes the global model from the China-market version, identifies 16 GB RAM with Obsidian 256 GB and Supernova 512 GB, Android 12 / REDMAGIC OS 5.0, 6.8-inch 120 Hz display, cameras, 5,000 mAh battery, and 65 W global charging. China-market 135 W charging is not applied to the Philippine version.",
           "2022-05-12"),
    source("redmagic_7_pro_global_announce", "REDMAGIC Global", URL_GLOBAL_ANNOUNCE,
           "Official international-version announcement date",
           "REDMAGIC published its REDMAGIC 7 Pro international-arrival announcement on April 12, 2022. This is the global announcement date; REDMAGIC's later product news and Philippine reports document availability separately.",
           "2022-04-12"),
    source("redmagic_7_pro_unbox_ph", "Unbox Philippines", URL_UNBOX,
           "Philippine launch timing and international hardware configuration",
           "Published April 13, 2022. Identifies the global model as launching in markets including the Philippines, with an April 22 early-bird period and an April 27 official sale date. It lists 16 GB LPDDR5 with 256/512 GB UFS 3.1, 120 Hz AMOLED, 16 MP under-display camera, 5,000 mAh battery, and 65 W global charging. It reports Bluetooth 5.1, which conflicts with REDMAGIC's press release and other exact-model records specifying 5.2.",
           "2022-04-13"),
    source("redmagic_7_pro_gizguide_ph", "GIZGUIDE Philippines", URL_GIZGUIDE,
           "Local XUNDD availability, Philippine configuration names, and launch prices",
           "Published April 30, 2022. Reports the global REDMAGIC 7 Pro was available in the Philippines from XUNDD, naming 16/256 Obsidian at PHP 45,999 and 16/512 Supernova at PHP 49,999. The report attributes the information to XUNDD; it is a historical launch price, not a current offer.",
           "2022-04-30"),
    source("redmagic_7_pro_noypi_ph", "NoypiGeeks Philippines", URL_NOYPI,
           "Independent local configuration, price, and technical cross-check",
           "Published May 2, 2022. Confirms XUNDD distribution in the Philippines, 16/256 Obsidian at PHP 45,999, and 16/512 Supernova at PHP 49,999. Its detailed list describes dual SIM, 5G, Wi-Fi 6E, Bluetooth 5.2, 5,000 mAh, and cameras; Wi-Fi 6E differs from the 802.11ax/Wi-Fi 6 description in REDMAGIC's global press material and local YugaTech coverage, so the catalog leaves the Wi-Fi generation unresolved.",
           "2022-05-02"),
    source("redmagic_7_pro_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Dated Philippine price-list corroboration and release month",
           "The 2022 Philippine smartphone price list gives PHP 45,999 for 16/256 Obsidian and PHP 49,999 for 16/512 Supernova and places the model in May. Used as a dated local price cross-check, not as current pricing."),
    source("redmagic_7_pro_yugatech_specs", "YugaTech Philippines", URL_YUGA_SPECS,
           "International variant matrix and connectivity cross-check",
           "YugaTech's exact-model global launch article identifies the global 16/256 Obsidian and 16/512 Supernova variants and describes Wi-Fi 6/802.11ax. Philippine launch coverage separately documents the local distributor and prices."),
    source("redmagic_7_pro_manilashaker_ph", "ManilaShaker Philippines", URL_MANILASHAKER,
           "Independent Philippine availability, variant, and price cross-check",
           "Published May 1, 2022. Reports that the global REDMAGIC 7 Pro was available through XUNDD in the Philippines, with the same two memory/color variants and PHP 45,999 / PHP 49,999 prices.",
           "2022-05-01"),
    source("redmagic_7_pro_qualcomm", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 8 Gen 1 platform reference",
           "Qualcomm's product page documents the Snapdragon 8 Gen 1 platform and Adreno 730 graphics family. Platform capabilities are not substituted for handset-specific implementation details."),
    source("redmagic_7_pro_qualcomm_brief", "Qualcomm", URL_QUALCOMM_BRIEF,
           "Primary chipset process and CPU capability reference",
           "Qualcomm's Snapdragon 8 Gen 1 product brief gives a 4 nm process and Kryo CPU up to 3.0 GHz with Cortex-X2 technology. Detailed core clusters are cross-checked against NanoReview and are not handset benchmark claims."),
    source("redmagic_7_pro_nanoreview", "NanoReview", URL_NANOREVIEW,
           "Exact-model secondary hardware cross-check",
           "Exact REDMAGIC 7 Pro page used for display, camera, battery, connectivity, audio, and sensor cross-checks. Regional claims are not treated as evidence of Philippine sales; the locally documented global configuration and REDMAGIC's global source take precedence."),
    source("redmagic_7_pro_nanoreview_soc", "NanoReview", URL_NANOREVIEW_SOC,
           "Independent chipset architecture cross-check",
           "Used for Snapdragon 8 Gen 1 CPU cluster details only. Device benchmark scores are not copied into the catalog."),
    source("redmagic_7_pro_kimovil", "Kimovil", URL_KIMOVIL,
           "Exact-model regional configuration and technical cross-check",
           "The exact model page distinguishes Global 16/256 and 16/512 configurations from China-market variants. Its global variant matrix corroborates the local memory/color pairings; regional price listings are not used as Philippine prices."),
    source("redmagic_7_pro_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact model code, build, media, connectivity, and battery cross-check",
           "Exact model code NX709J. The listing reports 166.3 x 77.1 x 10 mm, 235 g, UFS 3.1, video modes, dual SIM, Wi-Fi 6E, Bluetooth 5.2, and the global 65 W charging version. Wi-Fi generation conflicts with REDMAGIC's Wi-Fi 6/802.11ax material and remains unset."),
    source("redmagic_7_pro_aptx", "Qualcomm aptX product registry", URL_APTX,
           "Model-code and Bluetooth cross-check",
           "The registry explicitly maps model NX709J to marketing name REDMAGIC 7 Pro and lists Bluetooth 5.2 and a 6.8-inch display. Its broad hardware family/RAM matrix includes China configurations, so only the code/name and Bluetooth details are used here."),
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
    if unit is not None:
        item["unit"] = unit
    if price_type:
        item["priceType"] = price_type
    return item


def fields_for(variant: dict) -> list[dict]:
    config = f"Philippine REDMAGIC 7 Pro, {variant['ram']} GB RAM / {variant['storage']} GB storage ({variant['color']})"
    rows = [
        field("model_number", "redmagic_7_pro_ntc", "NTC lists REDMAGIC model NX709J as REDMAGIC 7 Pro", "NX709J", status="VERIFIED", note="Exact model code and marketed name match the NTC GEC entry and REDMAGIC 7 Pro sources.", config_match="REDMAGIC 7 Pro global version; both Philippine configurations"),
        field("global_release_date", "redmagic_7_pro_global_announce", "REDMAGIC Global's international REDMAGIC 7 Pro announcement is dated April 12, 2022; reported order start was April 27", "2022-04-12", status="VERIFIED", note="Use the official announcement date as global launch. The April 27 date marks reported order availability and is recorded in the Philippine sale-date field.", config_match="REDMAGIC 7 Pro global version"),
        field("configuration", "redmagic_7_pro_gizguide_ph", f"Philippine global version: 16 GB RAM / {variant['storage']} GB storage, {variant['color']}", f"16 GB RAM / {variant['storage']} GB storage ({variant['color']})", status="VERIFIED_SECONDARY", note="XUNDD-attributed Philippine launch coverage and REDMAGIC's global variant list identify the distinct Obsidian 16/256 and Supernova 16/512 configurations.", config_match=config),
        field("philippine_release_date", "redmagic_7_pro_unbox_ph", "Reported official sale date for the global REDMAGIC 7 Pro including the Philippines: April 27, 2022; local XUNDD availability reported April 30", "2022-04-27", status="VERIFIED_SECONDARY", note="April 27 is the reported official sale start; GIZGUIDE subsequently documented that the phone was available locally through XUNDD. The date denotes reported launch availability, not present stock.", config_match="Philippine REDMAGIC 7 Pro global launch; both configurations"),
        field("official_launch_price_php", "redmagic_7_pro_gizguide_ph", f"XUNDD-attributed Philippine launch price: PHP {variant['launch']:,} for {variant['ram']} GB / {variant['storage']} GB ({variant['color']})", variant["launch"], status="VERIFIED_SECONDARY", unit="PHP", note="GIZGUIDE, NoypiGeeks, ManilaShaker, and YugaTech's 2022 price list corroborate this dated launch price for the exact configuration. This is not a current price.", config_match=config, price_type="historical_ph_launch_price"),
        field("current_price_php", "redmagic_7_pro_kimovil", "No current dated, orderable Philippine offer was verified; Kimovil's reviewed global listing showed no live price", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank. Preserve the sourced 2022 launch price as historical data only.", config_match=config, price_type="no_current_offer_verified"),
        field("display_size", "redmagic_7_pro_global", "6.8-inch AMOLED display", 6.8, status="VERIFIED", key="displayInches", unit="in", note="REDMAGIC global and Philippine launch sources agree on display size.", config_match=config),
        field("display_technology", "redmagic_7_pro_global", "AMOLED", "AMOLED", status="VERIFIED", key="displayType", note="Official global and local sources identify an AMOLED panel.", config_match=config),
        field("display_resolution", "redmagic_7_pro_unbox_ph", "Full HD+ 1080 x 2400 pixels", "1080 x 2400", status="VERIFIED_SECONDARY", key="resolution", note="Local launch coverage and exact-model references agree on 1080 x 2400.", config_match=config),
        field("display_refresh_rate", "redmagic_7_pro_global", "120 Hz refresh rate", 120, status="VERIFIED", key="refreshHz", unit="Hz", note="REDMAGIC global and Philippine sources identify a 120 Hz panel.", config_match=config),
        field("display_brightness", "redmagic_7_pro_noypi_ph", "Local sources report 600-nit maximum/peak or 700 nits; GSMArena's measured result is a different test value", None, status="CONFLICTING_INFORMATION", unit="nits", note="Published brightness values differ by source and likely measurement convention. Leave normalized brightness blank rather than presenting one figure as directly comparable.", config_match=config),
        field("display_protection", "redmagic_7_pro_global", "Corning Gorilla Glass 5", "Corning Gorilla Glass 5", status="VERIFIED_SECONDARY", note="REDMAGIC global and Philippine launch specifications list Gorilla Glass 5.", config_match=config),
        field("chipset", "redmagic_7_pro_global", "Qualcomm Snapdragon 8 Gen 1 (SM8450)", "Qualcomm Snapdragon 8 Gen 1", status="VERIFIED", key="chipset", note="Official global material and Philippine launch coverage agree on Snapdragon 8 Gen 1.", config_match=config),
        field("process_node", "redmagic_7_pro_qualcomm_brief", "4 nm process technology", 4, status="VERIFIED", unit="nm", note="Qualcomm's product brief specifies a 4 nm process for Snapdragon 8 Gen 1.", config_match=config),
        field("cpu", "redmagic_7_pro_nanoreview_soc", "1x Cortex-X2 up to 3.0 GHz + 3x Cortex-A710 up to 2.5 GHz + 4x Cortex-A510 up to 1.8 GHz", "1x Cortex-X2 3.0 GHz + 3x Cortex-A710 2.5 GHz + 4x Cortex-A510 1.8 GHz", status="VERIFIED_SECONDARY", key="cpu", note="NanoReview's Snapdragon 8 Gen 1 cluster details; Qualcomm independently confirms the 3.0 GHz Cortex-X2-class platform. This describes the chipset, not benchmark performance.", config_match=config),
        field("gpu", "redmagic_7_pro_qualcomm", "Qualcomm Adreno 730", "Qualcomm Adreno 730", status="VERIFIED_SECONDARY", key="gpu", note="Qualcomm platform reference and exact-model specifications identify Adreno 730.", config_match=config),
        field("operating_system", "redmagic_7_pro_global", "Android 12 with REDMAGIC OS 5.0 at launch", "Android 12 with REDMAGIC OS 5.0", status="VERIFIED", key="os", note="REDMAGIC's international launch source and local launch coverage identify the factory launch software; no later upgrade is substituted.", config_match=config),
        field("os_support", "redmagic_7_pro_global", "No guaranteed OS-upgrade or security-support duration found in the reviewed manufacturer material", None, status="NOT_DISCLOSED", note="Do not infer a support period from the device's later software state.", config_match=config),
        field("ram_capacity", "redmagic_7_pro_gizguide_ph", "16 GB RAM", 16, status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="Both locally reported global variants use 16 GB RAM.", config_match=config),
        field("ram_type", "redmagic_7_pro_unbox_ph", "LPDDR5 RAM", "LPDDR5", status="VERIFIED_SECONDARY", note="Philippine launch coverage and the international specification identify LPDDR5 memory.", config_match=config),
        field("storage_capacity", "redmagic_7_pro_gizguide_ph", f"{variant['storage']} GB internal storage", variant["storage"], status="VERIFIED_SECONDARY", key="storageGb", unit="GB", note="Exact capacity belongs to the local color/configuration pair listed by XUNDD-attributed coverage and REDMAGIC's global variant matrix.", config_match=config),
        field("storage_type", "redmagic_7_pro_global", "UFS 3.1 internal storage", "UFS 3.1", status="VERIFIED_SECONDARY", note="REDMAGIC global, Unbox, and exact-model technical references identify UFS 3.1.", config_match=config),
        field("storage_expansion", "redmagic_7_pro_gsmarena", "No microSD card slot listed", "No microSD slot", status="VERIFIED_SECONDARY", note="Exact-model hardware references list fixed internal storage and no card slot.", config_match=config),
        field("rear_camera_system", "redmagic_7_pro_global", "64 MP main + 8 MP ultrawide + 2 MP third rear camera; sources differ on whether the 2 MP module is macro or depth", "64 MP main + 8 MP ultrawide + 2 MP third module", status="CONFLICTING_INFORMATION", note="The camera resolutions and three-module layout are consistent, but the third module is called macro in some references and depth in others. Avoid asserting a specific function until the discrepancy is resolved.", config_match=config),
        field("main_camera_sensor", "redmagic_7_pro_nanoreview", "No source reviewed establishes the exact main camera sensor part number for the Philippine global configurations", None, status="NOT_DISCLOSED", note="Do not infer a sensor model from resolution or chipset compatibility.", config_match=config),
        field("ultrawide_camera", "redmagic_7_pro_unbox_ph", "8 MP ultrawide camera; 120-degree field of view is listed by local specifications", "8 MP ultrawide, 120-degree field of view", status="VERIFIED_SECONDARY", note="Philippine launch sources confirm the module; the field-of-view figure is secondary technical detail.", config_match=config),
        field("telephoto_camera", "redmagic_7_pro_global", "No telephoto camera; the rear array consists of main, ultrawide, and a 2 MP macro/depth module", "No telephoto camera", status="VERIFIED_SECONDARY", note="The documented three-camera array has no telephoto module.", config_match=config),
        field("front_camera", "redmagic_7_pro_global", "16 MP under-display selfie camera", 16, status="VERIFIED", key="frontCameraMp", unit="MP", note="REDMAGIC global and Philippine launch sources identify the 16 MP under-display camera.", config_match=config),
        field("video_recording", "redmagic_7_pro_gsmarena", "Rear video up to 8K/30 fps and 4K/60 fps; front video up to 1080p/60 fps", "Rear up to 8K/30 fps and 4K/60 fps; front up to 1080p/60 fps", status="VERIFIED_SECONDARY", note="Exact-model technical specification cross-check. These are published maximum modes, not a guarantee that every codec or stabilization mode is available at each resolution.", config_match=config),
        field("battery_capacity", "redmagic_7_pro_global", "5,000 mAh battery", 5000, status="VERIFIED", key="batteryMah", unit="mAh", note="REDMAGIC global and Philippine sources agree on 5,000 mAh for the international model.", config_match=config),
        field("battery_technology", "redmagic_7_pro_gsmarena", "Li-Po, non-removable battery", "Li-Po; non-removable", status="VERIFIED_SECONDARY", note="Exact-model hardware listings identify Li-Po chemistry and a non-removable battery.", config_match=config),
        field("wired_charging", "redmagic_7_pro_global", "65 W wired charging for the international version", 65, status="VERIFIED", key="chargingW", unit="W", note="REDMAGIC explicitly distinguishes 65 W global charging from 135 W China charging; the global value is used for Philippine variants.", config_match=config),
        field("wireless_charging", "redmagic_7_pro_global", "Wireless charging support not stated in the reviewed official launch material", None, status="NOT_DISCLOSED", note="No wireless charging value is inferred from absence in promotional material.", config_match=config),
        field("dimensions", "redmagic_7_pro_gsmarena", "166.3 x 77.1 x 10 mm", "166.3 x 77.1 x 10 mm", status="VERIFIED_SECONDARY", key="dimensions", unit="mm", note="Exact-model global dimensions from independent hardware listings; minor hundredth-millimeter rounding differences appear in secondary sources.", config_match=config),
        field("weight", "redmagic_7_pro_gsmarena", "235 g", 235, status="VERIFIED_SECONDARY", key="weightG", unit="g", note="GSMArena, Kimovil, and Philippine launch coverage agree on 235 g.", config_match=config),
        field("materials", "redmagic_7_pro_gsmarena", "Glass front with Gorilla Glass 5, glass back, aluminum frame", "Gorilla Glass 5 front; glass back; aluminum frame", status="VERIFIED_SECONDARY", note="Exact-model build description; no additional coating or material is inferred.", config_match=config),
        field("ingress_protection", "redmagic_7_pro_global", "No IP rating found in the reviewed manufacturer or Philippine launch specifications", None, status="NOT_DISCLOSED", note="Keep certification blank; the absence of an IP rating in reviewed pages is not a water-resistance guarantee or proof that no certification exists.", config_match=config),
        field("sim_esim", "redmagic_7_pro_gizguide_ph", "Dual Nano-SIM global version; eSIM support not recorded", "Dual Nano-SIM; eSIM not recorded", status="VERIFIED_SECONDARY", key="sim", note="Local and exact-model specifications identify dual SIM; reviewed sources do not establish eSIM support for the Philippine unit.", config_match=config),
        field("cellular_bands", "redmagic_7_pro_unbox_ph", "Philippine launch material identifies 4G LTE and 5G; complete local band set not published in reviewed sources", "4G LTE and 5G; local band list not recorded", status="VERIFIED_SECONDARY", key="cellular", note="Record network generations only. Do not infer Philippine carrier compatibility from another region's band table.", config_match=config),
        field("wifi", "redmagic_7_pro_yugatech_specs", "YugaTech reports 802.11ax/Wi-Fi 6; NoypiGeeks and GSMArena report Wi-Fi 6E", None, status="CONFLICTING_INFORMATION", note="Wi-Fi generation conflicts across secondary sources. The reviewed official global launch recap does not resolve the 6/6E distinction; leave the normalized Wi-Fi value blank pending a regional technical declaration.", config_match=config),
        field("bluetooth", "redmagic_7_pro_aptx", "Bluetooth 5.2; one local launch article says 5.1", "Bluetooth 5.2", status="VERIFIED_SECONDARY", note="The model-specific Qualcomm registry, REDMAGIC global press material, and GSMArena specify Bluetooth 5.2; Unbox lists 5.1, which is recorded as a source discrepancy.", config_match=config),
        field("usb", "redmagic_7_pro_gsmarena", "USB Type-C 3.0 with OTG", "USB Type-C 3.0; OTG", status="VERIFIED_SECONDARY", key="ports", note="Exact-model technical references list Type-C 3.0 and OTG; Philippine coverage confirms Type-C.", config_match=config),
        field("nfc", "redmagic_7_pro_noypi_ph", "NFC supported", "Yes", status="VERIFIED_SECONDARY", note="Philippine launch technical lists and exact-model references identify NFC.", config_match=config),
        field("gnss", "redmagic_7_pro_gsmarena", "GPS (L1+L5), GLONASS, BeiDou, and Galileo", "GPS (L1+L5), GLONASS, BeiDou, Galileo", status="VERIFIED_SECONDARY", key="gnss", note="Exact-model reference lists the named positioning systems; no additional GNSS support is inferred.", config_match=config),
        field("audio", "redmagic_7_pro_unbox_ph", "Stereo speakers and 3.5 mm audio jack", "Stereo speakers; 3.5 mm audio jack", status="VERIFIED_SECONDARY", key="sound", note="Philippine launch coverage identifies stereo speakers and the headphone jack.", config_match=config),
        field("sensors", "redmagic_7_pro_gsmarena", "Under-display optical fingerprint sensor, accelerometer, gyroscope, proximity sensor, and compass", "Under-display fingerprint, accelerometer, gyroscope, proximity, compass", status="VERIFIED_SECONDARY", note="Exact-model sensor listing; no barometer or other sensor is inferred.", config_match=config),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field records, got {len(rows)}")
    defined = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in rows} - defined)
    if missing:
        raise ValueError(f"Undefined source IDs in fields: {missing}")
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine launch coverage reports the REDMAGIC 7 Pro global version available through local distributor XUNDD. Workbook eligibility remains Pending.",
        "philippineAvailability": "Philippine technology coverage reports the international REDMAGIC 7 Pro available through XUNDD in late April 2022. The locally identified configurations are 16 GB / 256 GB Obsidian and 16 GB / 512 GB Supernova. Historical launch prices are PHP 45,999 and PHP 49,999 respectively. Current stock and price have not been verified.",
        "observedAt": OBSERVED,
        "manufacturer": "ZTE Corporation (nubia / REDMAGIC)",
        "catalogModel": "REDMAGIC 7 Pro",
        "productLine": "REDMAGIC 7 Series",
        "modelNumber": "NX709J",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Reported Philippine sale start date",
        "researchNotes": "Workbook row 85 REDMAGIC 7 Pro matches NTC model NX709J and the international REDMAGIC variant family. Local XUNDD-attributed coverage identifies two distinct color/configuration pairs: Obsidian 16/256 and Supernova 16/512. The international version's 65 W charging, not the China version's 135 W, is used. Current price remains blank; 2022 launch prices are retained as historical values. Workbook eligibility remains Pending.",
        "qualityFlag": "NTC model match and two Philippine global configurations verified; 2022 launch prices corroborated; current price unavailable; display brightness, third rear-camera function, and Wi-Fi generation remain unresolved; workbook eligibility remains Pending.",
        "openIssues": [
            {"issue": "YugaTech lists Wi-Fi 6/802.11ax, while NoypiGeeks and GSMArena list Wi-Fi 6E; the reviewed manufacturer global article does not resolve the distinction", "action": "Leave the Wi-Fi field blank until a definitive regional specification resolves the conflict."},
            {"issue": "The 2 MP third rear camera is described as macro by some sources and depth by others", "action": "Record a 2 MP third rear module without asserting a function."},
            {"issue": "Display brightness figures vary by source and measurement convention", "action": "Leave normalized brightness blank."},
            {"issue": "No current dated, orderable Philippine price was verified", "action": "Keep current price blank and retain launch prices as historical only."},
            {"issue": "Exact product images are present on manufacturer and Philippine sources, but reuse rights are not established", "action": "Keep the neutral placeholder until image reuse terms or permission are documented."},
            {"issue": "Workbook eligibility is Pending", "action": "Preserve the study's Pending status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 85 or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "redmagic"
            or device.get("model", "").casefold().replace(" ", "") not in {"7pro", "redmagic7pro"}):
        raise ValueError("Workbook row 85 no longer matches REDMAGIC 7 Pro")
    current_ids = {variant.get("id") for variant in device.get("variants", [])}
    allowed_ids = {OLD_CONFIG, *(item["id"] for item in CONFIGS)}
    if current_ids - allowed_ids:
        raise ValueError(f"Unexpected REDMAGIC 7 Pro configuration IDs: {sorted(current_ids)}")

    variants = [{
        "id": item["id"], "label": item["label"], "sku": None, "modelCode": "NX709J",
        "notes": f"XUNDD-attributed Philippine launch coverage identifies {item['label']} at PHP {item['launch']:,}; historical launch price only, current offer not verified.",
        "workbookRow": 85,
    } for item in CONFIGS]
    records = []
    for index, variant in enumerate(CONFIGS):
        records.append({
            "deviceId": DEVICE,
            "configurationId": variant["id"],
            "brand": "REDMAGIC",
            "model": "REDMAGIC 7 Pro",
            "configuration": variant["label"],
            "configurationLabel": variant["label"],
            "modelCode": "NX709J",
            "sources": SOURCES,
            "fields": fields_for(variant),
            "availabilityEvidence": availability_evidence(),
            **({"replacementVariants": variants, "replaceUnrecordedPlaceholder": True} if index == 0 else {}),
        })
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].extend(records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Exact REDMAGIC 7 Pro global product images are available on manufacturer and Philippine technology pages, but reuse terms or permission to copy/embed are not recorded. Keep the neutral placeholder.",
        "sourcePage": URL_GLOBAL_PRESS,
        "assetUrl": None,
        "scope": "REDMAGIC 7 Pro global version; Philippine Obsidian 16/256 and Supernova 16/512 variants",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for REDMAGIC 7 Pro",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    price_sources = [
        ("redmagic_7_pro_gizguide_ph", "2022-04-30", "XUNDD-attributed Philippine launch price"),
        ("redmagic_7_pro_manilashaker_ph", "2022-05-01", "Philippine distributor availability and launch price"),
        ("redmagic_7_pro_noypi_ph", "2022-05-02", "Independent Philippine launch price report"),
    ]
    for variant in CONFIGS:
        for sid, published, kind in price_sources:
            prices.append({
                "device_id": DEVICE,
                "amount_php": variant["launch"],
                "configuration_id": variant["id"],
                "configuration_match": f"exact_philippine_{variant['ram']}gb_{variant['storage']}gb_{variant['color'].casefold()}_configuration",
                "variant_ram_gb": variant["ram"],
                "variant_storage_gb": variant["storage"],
                "price_type": "historical_ph_launch_price",
                "source_published_at": published,
                "excerpt": f"{kind}: REDMAGIC 7 Pro {variant['label']} listed at PHP {variant['launch']:,}; historical launch price, not a current offer.",
                "source_url": next(item["url"] for item in SOURCES if item["id"] == sid),
                "source_kind": "historical_local_price_candidate",
                "observed_at": OBSERVED_AT,
                "local_availability_verified": True,
                "availability_status": "historical_price_not_current",
            })
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "REDMAGIC", "model_name": "REDMAGIC 7 Pro", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC 2022 GEC lists REDMAGIC model NX709J as REDMAGIC 7 Pro."},
            {"device_id": DEVICE, "source_url": URL_UNBOX, "result": "Unbox reports the global version sale date as April 27, 2022, including the Philippines, and describes its two international configurations."},
            {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "GIZGUIDE attributes the two Philippine global configurations and PHP 45,999 / PHP 49,999 launch prices to local distributor XUNDD."},
            {"device_id": DEVICE, "source_url": URL_NOYPI, "result": "NoypiGeeks independently confirms XUNDD distribution, the exact configurations, and the same dated launch prices."},
            {"device_id": DEVICE, "source_url": URL_GLOBAL, "result": "REDMAGIC global confirms international 16/256 Obsidian and 16/512 Supernova variants and 65 W global charging; China-market charging is not applied."},
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC model NX709J is matched to REDMAGIC 7 Pro; technical sources disagree on Wi-Fi generation and the 2 MP camera function."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 85 REDMAGIC 7 Pro -> NTC NX709J / global version",
        "configurations": [{"label": item["label"], "historicalLaunchPricePhp": item["launch"]} for item in CONFIGS],
        "reportedPhilippineSaleStart": "2022-04-27",
        "reviewedFields": sum(len(item["fields"]) for item in records),
        "currentPrices": "blank; no current orderable Philippine offer verified",
        "image": "neutral placeholder; reuse rights not established",
        "unresolved": ["Wi-Fi 6 versus 6E", "2 MP third rear-camera function", "display brightness"],
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
        "historicalPriceCandidates": len(prices),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
