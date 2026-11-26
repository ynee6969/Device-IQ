#!/usr/bin/env python3
"""Record sourced Philippine configuration evidence for REDMAGIC 7."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/redmagic-7-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_6908e733a06a0b"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIGS = [
    {"id": f"{DEVICE}-12gb-128gb-ph", "label": "12 GB RAM / 128 GB storage (Obsidian)",
     "ram": 12, "storage": 128, "color": "Obsidian", "launch": 34999},
    {"id": f"{DEVICE}-16gb-256gb-ph", "label": "16 GB RAM / 256 GB storage (Pulsar)",
     "ram": 16, "storage": 256, "color": "Pulsar", "launch": None},
    {"id": f"{DEVICE}-18gb-256gb-ph", "label": "18 GB RAM / 256 GB storage (Supernova)",
     "ram": 18, "storage": 256, "color": "Supernova", "launch": None},
]

URL_ZTE = "https://www.ztedevices.com.my/redmagic/redmagic-7-series/redmagic-7"
URL_GLOBAL_LAUNCH = "https://global.redmagic.gg/blogs/news/unlock-the-next-level-of-gaming-with-the-new-redmagic-7"
URL_GLOBAL_ORDER = "https://global.redmagic.gg/blogs/news/order-now-and-fast-forward-to-victory-with-the-new-redmagic-7"
URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_YUGA = "https://www.yugatech.com/mobile/nubia-redmagic-7-launched-in-the-philippines/"
URL_GADGET = "https://www.gadgetpilipinas.net/2022/03/nubia-red-magic-7-is-now-available-in-ph/"
URL_NOYPI = "https://www.noypigeeks.com/android/redmagic-7-global-philippines/"
URL_GIZGUIDE = "https://www.gizguide.com/2022/04/nubia-redmagic-7-philippines.html"
URL_SPEED = "https://www.speed.ph/nubia-redmagic-7-now-available/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-gen-1-mobile-platform"
URL_QUALCOMM_BRIEF = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/snapdragon-8-gen-1-mobile-platform-product-brief.pdf"
URL_NANOREVIEW_DEVICE = "https://nanoreview.net/en/phone/zte-nubia-red-magic-7"
URL_NANOREVIEW_SOC = "https://nanoreview.net/en/soc/qualcomm-snapdragon-8-gen-1"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-nubia-red-magic-7"
URL_GSMARENA = "https://www.gsmarena.com/zte_nubia_red_magic_7-11363.php"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("redmagic_7_zte_specs", "ZTE Malaysia / nubia", URL_ZTE,
           "Manufacturer specification cross-check for the international REDMAGIC 7",
           "The manufacturer page lists the global 12/128, 16/256, and 18/256 color configurations; Snapdragon 8 Gen 1; 6.8-inch 165 Hz AMOLED; cameras; 4,500 mAh/65 W battery; dual 5G SIM; Wi-Fi 6; Bluetooth 5.2; dimensions; and weight. It is a regional manufacturer reference, not by itself proof of Philippine sale."),
    source("redmagic_7_global_launch", "REDMAGIC Global", URL_GLOBAL_LAUNCH,
           "Primary global model launch-date reference",
           "REDMAGIC's global launch event was published February 22, 2022. The China model was announced earlier; the Philippine inventory item matches the international version, whose public order page was dated March 11." ,
           "2022-02-22"),
    source("redmagic_7_global_orders", "REDMAGIC Global", URL_GLOBAL_ORDER,
           "Primary international-version order availability and variant context",
           "Published March 11, 2022; REDMAGIC says the international REDMAGIC 7 is available to order and identifies REDMAGIC OS 5.0, 165 Hz display, 720 Hz touch sampling, and ICE 8.0 cooling.",
           "2022-03-11"),
    source("redmagic_7_ntc_gec", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and model-code match",
           "The NTC 2022 GEC list includes REDMAGIC NX679J as REDMAGIC 7. This matches the international model code; registration does not independently prove a retail configuration."),
    source("redmagic_7_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine launch, official channel availability, and exact configuration evidence",
           "Published March 11, 2022. Reports launch in the Philippines, identifies official website/Shopee Mall/LazMall channels, and lists 12/128 Obsidian, 16/256 Pulsar, and 18/256 Supernova. It reports respective prices PHP 34,999, PHP 39,999, and PHP 44,999. Other local reports disagree on some prices; retain candidates and avoid a single launch-price value where conflicting." ,
           "2022-03-11"),
    source("redmagic_7_gadgetpilipinas_ph", "Gadget Pilipinas", URL_GADGET,
           "Philippine distributor availability, three exact configurations, and historical prices",
           "Published March 12, 2022. Says the global version was locally available via XUNDD Philippines and lists 12/128 Obsidian at PHP 34,999, 16/256 Pulsar at PHP 39,999, and 18/256 Supernova at PHP 46,999. The top configuration differs from YugaTech's March 11 amount." ,
           "2022-03-12"),
    source("redmagic_7_noypigeeks_ph", "NoypiGeeks", URL_NOYPI,
           "Exact local variant, local launch pricing, and independent specifications",
           "Published March 11, 2022. Attributes the global version to official Philippine distributor XUNDD and reports 12/128 at PHP 34,999, 16/256 at PHP 36,999, and 18/256 at PHP 46,999. The 16/256 amount conflicts with YugaTech and Gadget Pilipinas. Also lists Android 12, RedMagic OS 5.0, UFS 3.1, cameras, connectivity, dimensions, and battery.",
           "2022-03-11"),
    source("redmagic_7_gizguide_ph", "GIZGUIDE Philippines", URL_GIZGUIDE,
           "Official e-commerce launch availability and price cross-check",
           "Published April 22, 2022; says REDMAGIC Philippines' Shopee Mall and LazMall stores would carry the phone from April 29. Lists PHP 34,999, PHP 39,999, and PHP 46,999 for the three variants. This is a later official-store availability/price observation, not necessarily the initial local launch price.",
           "2022-04-22"),
    source("redmagic_7_speed_ph", "Speed Philippines", URL_SPEED,
           "Dated official-store price listing and local hardware cross-check",
           "Published April 29, 2022; reports official REDMAGIC Philippines store availability and different prices: PHP 36,990, PHP 42,990, and PHP 47,990. It documents LPDDR5 RAM, UFS 3.1 storage, 65 W charging, and display/camera details. These are price observations, not current offers.",
           "2022-04-29"),
    source("redmagic_7_qualcomm", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 8 Gen 1 platform reference",
           "Qualcomm documents the Snapdragon 8 Gen 1 platform, Adreno GPU family, Kryo CPU, 4 nm technology, and related connectivity/media capabilities. Chipset capabilities are not substituted for handset-specific implementation details."),
    source("redmagic_7_qualcomm_brief", "Qualcomm", URL_QUALCOMM_BRIEF,
           "Primary platform architecture and process reference",
           "Qualcomm's product brief gives Kryo CPU up to 3.0 GHz with Cortex-X2 technology and confirms 4 nm process. The exact 1+3+4 CPU core breakdown is cross-checked against NanoReview, not assumed from platform compatibility."),
    source("redmagic_7_nanoreview_device", "NanoReview", URL_NANOREVIEW_DEVICE,
           "Exact-model technical cross-check for display, cameras, memory, battery, connectivity, audio, and sensors",
           "Exact ZTE Nubia Red Magic 7 page. Used for secondary model-specific details and cross-checks; benchmark scores are not copied into the catalog. NanoReview warns that some specifications may differ by region, so the Philippine-local sources and manufacturer regional page take precedence."),
    source("redmagic_7_nanoreview_soc", "NanoReview", URL_NANOREVIEW_SOC,
           "Independent chipset architecture cross-check",
           "Used only for Snapdragon 8 Gen 1 CPU architecture and chipset-level core details; no device benchmark score or handset-specific implementation is inferred."),
    source("redmagic_7_kimovil", "Kimovil", URL_KIMOVIL,
           "Exact-model global configuration and technical cross-check",
           "Exact Nubia RedMagic 7 page identifies the global 12/128 model and related hardware. Regional price listings are not used as Philippine prices; the page cautions that specifications may vary by country."),
    source("redmagic_7_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-model release, build, and international hardware reference",
           "Exact-model listing distinguishes February announcement/release and documents global-versus-China variant differences. Its price/china variant details are not used as Philippine data."),
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
    config = f"Philippine REDMAGIC 7, {variant['ram']} GB RAM / {variant['storage']} GB storage ({variant['color']})"
    launch_price = variant["launch"]
    price_source = "redmagic_7_gadgetpilipinas_ph" if launch_price else "redmagic_7_yugatech_ph"
    if launch_price:
        price_value = f"Philippine launch reports list PHP 34,999 for 12 GB / 128 GB (Obsidian)"
        price_status = "VERIFIED_SECONDARY"
        price_note = "Three local reports corroborate PHP 34,999 for the exact 12/128 Obsidian version. Later retailers posted different dated prices; those are kept as historical observations, not redefined as the launch price."
    elif variant["ram"] == 16:
        price_value = "Local reports list PHP 36,999, PHP 39,999, or later official-store prices above those amounts for 16 GB / 256 GB (Pulsar)"
        price_status = "CONFLICTING_INFORMATION"
        price_note = "YugaTech and Gadget Pilipinas report PHP 39,999, NoypiGeeks reports PHP 36,999 on the same launch date, and later April retail observations are higher. Leave normalized launch price blank; keep every dated candidate in the price history."
    else:
        price_value = "YugaTech reports PHP 44,999 while other local launch and official-store references report PHP 46,999 or a later higher price for 18 GB / 256 GB (Supernova)"
        price_status = "CONFLICTING_INFORMATION"
        price_note = "YugaTech's March 11 amount differs from Gadget Pilipinas and NoypiGeeks; April official-store announcements report PHP 46,999, and Speed later lists PHP 47,990. Leave normalized launch price blank and retain dated observations."
    rows = [
        field("model_number", "redmagic_7_ntc_gec", "NTC lists REDMAGIC model NX679J and marketed name REDMAGIC 7", "NX679J", status="VERIFIED", note="Philippine equipment code NX679J matches the REDMAGIC 7 model name in the 2022 NTC GEC and the global device family.", config_match="REDMAGIC 7 international model; all three local memory/color configurations"),
        field("global_release_date", "redmagic_7_global_launch", "Global REDMAGIC 7 event published February 22, 2022; international order page dated March 11; Chinese model announced February 17", "2022-02-22", status="VERIFIED_SECONDARY", note="Use the international/global launch date, not the earlier Chinese announcement or the later first-order date.", config_match="REDMAGIC 7 global version"),
        field("configuration", "redmagic_7_zte_specs", f"Philippine version: {variant['ram']} GB RAM / {variant['storage']} GB storage, {variant['color']}", f"{variant['ram']} GB RAM / {variant['storage']} GB storage ({variant['color']})", status="VERIFIED_SECONDARY", note="ZTE and Philippine launch reports list three separate global variants with matching color names. Do not combine the distinct memory/color configurations.", config_match=config),
        field("philippine_release_date", "redmagic_7_yugatech_ph", "Philippine launch report dated March 11, 2022 identifies official REDMAGIC online and mall-store channels; the XUNDD distributor report followed March 12", "2022-03-11", status="VERIFIED_SECONDARY", note="March 11 is the published launch/availability date for the international version; later official marketplace listings began April 29.", config_match="Philippine REDMAGIC 7 global launch; all three local configurations"),
        field("official_launch_price_php", price_source, price_value, launch_price, status=price_status, unit="PHP", note=price_note, config_match=config, price_type="historical_ph_launch_price"),
        field("current_price_php", "redmagic_7_gizguide_ph", "Reviewed Philippine prices are dated 2022; no current dated, orderable new-unit offer was verified", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank. Preserve contemporaneous launch and April retail price candidates by source and date.", config_match=config, price_type="no_current_offer_verified"),
        field("display_size", "redmagic_7_zte_specs", "6.8-inch AMOLED display", 6.8, status="VERIFIED", key="displayInches", unit="in", note="ZTE and Philippine launch coverage agree on the display size.", config_match=config),
        field("display_technology", "redmagic_7_zte_specs", "AMOLED", "AMOLED", status="VERIFIED", key="displayType", note="Manufacturer and Philippine launch sources identify the AMOLED display.", config_match=config),
        field("display_resolution", "redmagic_7_yugatech_ph", "FHD+ 1080 x 2400 pixels", "1080 x 2400", status="VERIFIED_SECONDARY", key="resolution", note="YugaTech and NanoReview agree on the exact 1080 x 2400 resolution.", config_match=config),
        field("display_refresh_rate", "redmagic_7_zte_specs", "165 Hz refresh rate", 165, status="VERIFIED", key="refreshHz", unit="Hz", note="ZTE, REDMAGIC global, and local coverage agree.", config_match=config),
        field("display_brightness", "redmagic_7_nanoreview_device", "NanoReview lists 530 nits rated and 700 nits HDR; a local source reports 600-nit peak", None, status="CONFLICTING_INFORMATION", unit="nits", note="Brightness figures do not align across reviewed sources. Leave the numeric brightness blank rather than choosing one rating convention.", config_match=config),
        field("display_protection", "redmagic_7_nanoreview_device", "Corning Gorilla Glass 5", "Corning Gorilla Glass 5", status="VERIFIED_SECONDARY", note="NanoReview and NoypiGeeks list Gorilla Glass 5; YugaTech confirms Corning glass without a generation.", config_match=config),
        field("chipset", "redmagic_7_zte_specs", "Qualcomm Snapdragon 8 Gen 1 (SM8450)", "Qualcomm Snapdragon 8 Gen 1", status="VERIFIED", key="chipset", note="ZTE and Philippine launch reports identify Snapdragon 8 Gen 1.", config_match=config),
        field("process_node", "redmagic_7_qualcomm_brief", "4 nm process technology", 4, status="VERIFIED", unit="nm", note="Qualcomm's Snapdragon 8 Gen 1 product brief specifies 4 nm.", config_match=config),
        field("cpu", "redmagic_7_nanoreview_soc", "1x Cortex-X2 up to 3.0 GHz + 3x Cortex-A710 up to 2.5 GHz + 4x Cortex-A510 up to 1.8 GHz", "1x Cortex-X2 3.0 GHz + 3x Cortex-A710 2.5 GHz + 4x Cortex-A510 1.8 GHz", status="VERIFIED_SECONDARY", key="cpu", note="NanoReview's Snapdragon 8 Gen 1 architecture breakdown; Qualcomm confirms up to 3 GHz and Cortex-X2 technology. This is chipset configuration, not handset benchmark performance.", config_match=config),
        field("gpu", "redmagic_7_qualcomm", "Qualcomm Adreno 730", "Qualcomm Adreno 730", status="VERIFIED_SECONDARY", key="gpu", note="Qualcomm's platform page and exact-model sources identify Adreno 730.", config_match=config),
        field("operating_system", "redmagic_7_global_orders", "REDMAGIC OS 5.0 based on Android 12 at global launch", "REDMAGIC OS 5.0 based on Android 12", status="VERIFIED_SECONDARY", key="os", note="REDMAGIC global, YugaTech, and NanoReview identify the launch software. Later upgrades are not substituted for factory OS.", config_match=config),
        field("os_support", "redmagic_7_zte_specs", "No guaranteed OS-upgrade or security-support duration found in the reviewed manufacturer or local launch material", None, status="NOT_DISCLOSED", note="Do not infer a support period from the phone's current software state.", config_match=config),
        field("ram_capacity", "redmagic_7_yugatech_ph", f"{variant['ram']} GB RAM", variant["ram"], status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="Exact Philippine global configuration from local launch coverage and ZTE's model page.", config_match=config),
        field("ram_type", "redmagic_7_speed_ph", "LPDDR5 RAM", "LPDDR5", status="VERIFIED_SECONDARY", note="The Philippine retailer launch coverage specifies LPDDR5; no distinction among local variants is reported.", config_match=config),
        field("storage_capacity", "redmagic_7_yugatech_ph", f"{variant['storage']} GB internal storage", variant["storage"], status="VERIFIED_SECONDARY", key="storageGb", unit="GB", note="Exact local configuration capacity; ZTE, YugaTech, and local price reports identify this combination.", config_match=config),
        field("storage_type", "redmagic_7_speed_ph", "UFS 3.1 internal storage", "UFS 3.1", status="VERIFIED_SECONDARY", note="Speed and NoypiGeeks identify UFS 3.1. This is the international/Philippine device, distinct from China-only hardware details.", config_match=config),
        field("storage_expansion", "redmagic_7_nanoreview_device", "No memory-card slot", "No microSD slot", status="VERIFIED_SECONDARY", note="NanoReview and NoypiGeeks list storage as non-expandable; the manufacturer configuration page lists internal storage only.", config_match=config),
        field("rear_camera_system", "redmagic_7_yugatech_ph", "Triple rear cameras: 64 MP main, 8 MP ultrawide, and 2 MP macro", "64 MP main + 8 MP ultrawide + 2 MP macro", status="VERIFIED_SECONDARY", note="YugaTech and the exact-model technical reference agree on the three rear modules.", config_match=config),
        field("main_camera_sensor", "redmagic_7_nanoreview_device", "64 MP Samsung GW3, f/1.8; local specs do not consistently state the sensor model", "64 MP Samsung GW3, f/1.8", status="VERIFIED_SECONDARY", note="NanoReview lists the Samsung GW3 and f/1.8 lens; local sources independently support the 64 MP main camera. Sensor identity is secondary technical evidence.", config_match=config),
        field("ultrawide_camera", "redmagic_7_nanoreview_device", "8 MP ultrawide, 120-degree field of view, f/2.0", "8 MP, 120-degree FOV, f/2.0", status="VERIFIED_SECONDARY", note="Exact-model NanoReview lists module details; local Philippine coverage confirms the 8 MP ultrawide camera.", config_match=config),
        field("telephoto_camera", "redmagic_7_yugatech_ph", "No telephoto module; third rear module is a 2 MP macro camera", "No telephoto camera", status="VERIFIED_SECONDARY", note="The documented three-camera system assigns the third module to macro photography, not telephoto.", config_match=config),
        field("front_camera", "redmagic_7_zte_specs", "8 MP front camera", 8, status="VERIFIED", key="frontCameraMp", unit="MP", note="ZTE and Philippine launch sources agree on the front camera resolution.", config_match=config),
        field("video_recording", "redmagic_7_yugatech_ph", "Rear video up to 8K at 30 fps; front video up to 1080p at 30 fps", "Rear up to 8K/30 fps; front up to 1080p/30 fps", status="VERIFIED_SECONDARY", note="YugaTech reports these maximum modes; NanoReview cross-checks 8K/30 and 1080p/30 capture. Do not infer modes beyond these listed maxima.", config_match=config),
        field("battery_capacity", "redmagic_7_zte_specs", "4500 mAh battery", 4500, status="VERIFIED", key="batteryMah", unit="mAh", note="ZTE and Philippine sources identify the global model's 4,500 mAh battery; the China variant's charging figures are not substituted.", config_match=config),
        field("battery_technology", "redmagic_7_nanoreview_device", "Li-ion, non-removable battery", "Li-ion; non-removable", status="VERIFIED_SECONDARY", note="NanoReview identifies Li-ion chemistry and non-replaceable construction.", config_match=config),
        field("wired_charging", "redmagic_7_zte_specs", "65 W wired fast charging for the international version", 65, status="VERIFIED", key="chargingW", unit="W", note="The manufacturer regional page and YugaTech identify 65 W for the global/Philippine version. China-market REDMAGIC 7 charging rates differ and are excluded.", config_match=config),
        field("wireless_charging", "redmagic_7_nanoreview_device", "Wireless and reverse wireless charging are not supported", "No wireless or reverse wireless charging", status="VERIFIED_SECONDARY", note="Exact-model NanoReview identifies no wireless/reverse charging; no wireless charging support is claimed by the manufacturer product material reviewed.", config_match=config),
        field("dimensions", "redmagic_7_zte_specs", "170.57 x 78.33 x 9.5 mm", "170.57 x 78.33 x 9.5 mm", status="VERIFIED", key="dimensions", unit="mm", note="ZTE's exact model page provides these dimensions; local sources round to 170.6 x 78.3 x 9.5 mm.", config_match=config),
        field("weight", "redmagic_7_zte_specs", "215 g", 215, status="VERIFIED", key="weightG", unit="g", note="ZTE and exact-model sources agree on 215 g.", config_match=config),
        field("materials", "redmagic_7_gsmarena", "Glass front with Gorilla Glass 5, glass back, aluminum frame", "Gorilla Glass 5 front; glass back; aluminum frame", status="VERIFIED_SECONDARY", note="Exact-model GSMArena build details; no additional coating or material is inferred.", config_match=config),
        field("ingress_protection", "redmagic_7_zte_specs", "No IP rating appears in the reviewed manufacturer or Philippine launch specifications", None, status="NOT_DISCLOSED", note="Keep certification blank; absence of an IP rating in these sources is not a water-resistance guarantee or a proof of no certification.", config_match=config),
        field("sim_esim", "redmagic_7_zte_specs", "Dual 5G SIM; exact-model reference lists two Nano-SIM cards and no eSIM", "Dual Nano-SIM; no eSIM listed", status="VERIFIED_SECONDARY", key="sim", note="ZTE identifies dual 5G SIM for the global model and the exact-model reference specifies dual Nano-SIM. Local launch sources match the global variant family.", config_match=config),
        field("cellular_bands", "redmagic_7_yugatech_ph", "Philippine launch sources identify 4G LTE and 5G; the reviewed local source does not publish a complete band table", "5G and 4G LTE; local band list not recorded", status="VERIFIED_SECONDARY", key="cellular", note="Record only the local network types confirmed by Philippine launch coverage. Do not substitute a China-market band table or assume carrier compatibility.", config_match=config),
        field("wifi", "redmagic_7_zte_specs", "ZTE specifies dual-band Wi-Fi 6; a secondary local list reports Wi-Fi 6E", "Wi-Fi 6, dual-band 2.4/5 GHz", status="VERIFIED", key="wifi", note="Use the manufacturer's exact model specification (Wi-Fi 6). NoypiGeeks says Wi-Fi 6E, a conflicting secondary claim not corroborated on the manufacturer page.", config_match=config),
        field("bluetooth", "redmagic_7_zte_specs", "Bluetooth 5.2", "Bluetooth 5.2", status="VERIFIED", note="Manufacturer specification and exact-model technical source agree.", config_match=config),
        field("usb", "redmagic_7_nanoreview_device", "USB Type-C; exact-model reference lists USB 3.0 and OTG", "USB Type-C; USB 3.0; OTG", status="VERIFIED_SECONDARY", key="ports", note="NanoReview gives interface version and OTG. Philippine local sources confirm Type-C; the exact-model source identifies USB 3.0.", config_match=config),
        field("nfc", "redmagic_7_nanoreview_device", "NFC supported", "Yes", status="VERIFIED_SECONDARY", note="Exact-model NanoReview and Philippine launch coverage identify NFC.", config_match=config),
        field("gnss", "redmagic_7_nanoreview_device", "GPS, GLONASS, BeiDou, Galileo, QZSS, SBAS; dual-band GPS reported in local coverage", "GPS, GLONASS, BeiDou, Galileo, QZSS, SBAS; dual-band", status="VERIFIED_SECONDARY", key="gnss", note="Exact-model and Philippine references list the named navigation systems; no additional GNSS support is inferred.", config_match=config),
        field("audio", "redmagic_7_nanoreview_device", "Stereo speakers and 3.5 mm headphone jack", "Stereo speakers; 3.5 mm audio jack", status="VERIFIED_SECONDARY", key="sound", note="Exact-model NanoReview and NoypiGeeks identify stereo speakers and the headphone jack.", config_match=config),
        field("sensors", "redmagic_7_nanoreview_device", "Barometer, proximity, gyroscope, accelerometer, ambient-light sensor, compass, and fingerprint sensor", "Barometer, proximity, gyroscope, accelerometer, ambient light, compass, under-display fingerprint", status="VERIFIED_SECONDARY", note="Exact-model technical reference lists the sensor set and fingerprint reader; REDMAGIC and YugaTech confirm the under-display fingerprint sensor.", config_match=config),
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
        "availabilityStatus": "Philippine launch coverage identifies the global REDMAGIC 7 on the official website and official Shopee Mall/LazMall channels, with the XUNDD Philippines distributor named. Workbook eligibility remains Pending.",
        "philippineAvailability": "The international REDMAGIC 7 was reported available through the Philippine distributor XUNDD and REDMAGIC's official online channels in March 2022. Local reporting identifies three configurations: 12 GB / 128 GB Obsidian, 16 GB / 256 GB Pulsar, and 18 GB / 256 GB Supernova. A later official mall-store opening was reported for April 29. Historical prices differ between reports; current availability and price are not verified.",
        "observedAt": OBSERVED,
        "manufacturer": "ZTE Corporation (nubia / REDMAGIC)",
        "catalogModel": "REDMAGIC 7",
        "productLine": "REDMAGIC 7 Series",
        "modelNumber": "NX679J",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Reported Philippine launch/availability date",
        "researchNotes": "Workbook row 84 REDMAGIC 7 matches global model NX679J, listed in the Philippine NTC GEC. Local sources identify three distinct color/configuration pairs: 12/128 Obsidian, 16/256 Pulsar, 18/256 Supernova. The global version ships with a 4,500 mAh battery and 65 W charging; China-market charging details are excluded. Launch and later retail prices differ across sources for 16/256 and 18/256, so those normalized launch prices are left blank and dated observations are retained. Current price is blank. Eligibility remains Pending.",
        "qualityFlag": "Philippine NX679J registration, global version, three local configurations and historical local availability verified; initial prices for 16/256 and 18/256 conflict; current price unavailable; brightness figures conflict; eligibility remains Pending.",
        "openIssues": [
            {"issue": "Local sources quote different launch prices for the 16 GB / 256 GB and 18 GB / 256 GB versions", "action": "Keep normalized launch prices blank; retain dated source-specific price observations."},
            {"issue": "Display brightness is reported as 530-nit rated/700-nit HDR versus 600-nit peak", "action": "Keep numeric brightness blank until the measurement convention and regional specification are resolved."},
            {"issue": "A secondary source says Wi-Fi 6E while the manufacturer page lists Wi-Fi 6", "action": "Use manufacturer-specified Wi-Fi 6 and retain the secondary discrepancy in provenance."},
            {"issue": "No current Philippine offer with a dated orderable listing was verified", "action": "Keep current price blank."},
            {"issue": "Exact product images are available on official and Philippine source pages, but no reuse license or permission is recorded", "action": "Keep the neutral placeholder until reuse rights are documented."},
            {"issue": "Workbook eligibility is Pending", "action": "Preserve the study's Pending status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "redmagic"
            or device.get("model", "").casefold() not in {"7", "redmagic 7"}):
        raise ValueError("Inventory row no longer matches REDMAGIC 7")
    variant_ids = {variant.get("id") for variant in device.get("variants", [])}
    allowed = {OLD_CONFIG, *(item["id"] for item in CONFIGS)}
    if variant_ids - allowed:
        raise ValueError(f"Unexpected REDMAGIC 7 configurations: {sorted(variant_ids)}")

    variants = [{
        "id": item["id"], "label": item["label"], "sku": None, "modelCode": "NX679J",
        "notes": f"Philippine launch sources identify {item['label']}. The launch price is {'PHP ' + format(item['launch'], ',') if item['launch'] else 'disputed across dated local sources'}; see the dated price candidate file. Current price not verified.",
        "workbookRow": 84,
    } for item in CONFIGS]
    records = []
    for index, variant in enumerate(CONFIGS):
        records.append({
            "deviceId": DEVICE,
            "configurationId": variant["id"],
            "brand": "REDMAGIC",
            "model": "REDMAGIC 7",
            "configuration": variant["label"],
            "configurationLabel": variant["label"],
            "modelCode": "NX679J",
            "sources": SOURCES,
            "fields": fields_for(variant),
            "availabilityEvidence": availability_evidence(),
            **({"replacementVariants": variants,
                "replaceUnrecordedPlaceholder": True} if index == 0 else {}),
        })
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].extend(records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Exact REDMAGIC 7 product images are available on the manufacturer and Philippine technology pages, but no reusable license or permission to copy/embed is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_ZTE,
        "assetUrl": None,
        "scope": "REDMAGIC 7 global version; Philippine Obsidian 12/128, Pulsar 16/256, and Supernova 18/256 variants",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for REDMAGIC 7",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    price_specs = [
        ("redmagic_7_yugatech_ph", "2022-03-11", [34999, 39999, 44999], "historical local launch coverage"),
        ("redmagic_7_noypigeeks_ph", "2022-03-11", [34999, 36999, 46999], "historical Philippine global-version offer"),
        ("redmagic_7_gadgetpilipinas_ph", "2022-03-12", [34999, 39999, 46999], "historical local distributor price"),
        ("redmagic_7_gizguide_ph", "2022-04-22", [34999, 39999, 46999], "historical official mall-store launch price"),
        ("redmagic_7_speed_ph", "2022-04-29", [36990, 42990, 47990], "historical later official-store listing"),
    ]
    prices = []
    for sid, published, amounts, kind in price_specs:
        for variant, amount in zip(CONFIGS, amounts):
            prices.append({
                "device_id": DEVICE,
                "amount_php": amount,
                "configuration_id": variant["id"],
                "configuration_match": f"exact_philippine_{variant['ram']}gb_{variant['storage']}gb_{variant['color'].casefold()}_configuration",
                "variant_ram_gb": variant["ram"],
                "variant_storage_gb": variant["storage"],
                "price_type": "historical_ph_launch_or_retail_price",
                "source_published_at": published,
                "excerpt": f"{kind}: REDMAGIC 7 {variant['label']} listed at PHP {amount:,}; dated historical candidate, not a current price.",
                "source_url": next(s["url"] for s in SOURCES if s["id"] == sid),
                "source_kind": "historical_local_price_candidate",
                "observed_at": OBSERVED_AT,
                "local_availability_verified": True,
                "availability_status": "historical_price_not_current",
            })
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "REDMAGIC", "model_name": "REDMAGIC 7", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "Philippine NTC 2022 GEC lists REDMAGIC model NX679J as REDMAGIC 7."},
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech identifies the global REDMAGIC 7 in Philippine channels and three memory/color configurations; its 18/256 price differs from other dated sources."},
            {"device_id": DEVICE, "source_url": URL_GADGET, "result": "Gadget Pilipinas reports XUNDD Philippines availability and three variants; it corroborates PHP 34,999 for 12/128 and PHP 39,999 for 16/256."},
            {"device_id": DEVICE, "source_url": URL_NOYPI, "result": "NoypiGeeks confirms official distributor and reports different 16/256 price (PHP 36,999); also reports 18/256 at PHP 46,999."},
            {"device_id": DEVICE, "source_url": URL_SPEED, "result": "Speed reports later official-store availability on April 29 at PHP 36,990 / 42,990 / 47,990."},
            {"device_id": DEVICE, "source_url": URL_ZTE, "result": "ZTE manufacturer page lists the global variant matrix, 65W global charging, and core specifications. China-market 120/135W values are not used."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 84 REDMAGIC 7 -> NX679J global version",
        "configurations": [{"label": item["label"], "launchPricePhp": item["launch"]} for item in CONFIGS],
        "philippineAvailabilityDate": "2022-03-11",
        "globalVersionLaunchDate": "2022-02-22",
        "reviewedFields": sum(len(item["fields"]) for item in records),
        "currentPrices": "blank; no current orderable offer verified",
        "image": "neutral placeholder; reuse rights not established",
        "unresolved": ["16/256 launch price", "18/256 launch price", "display brightness"],
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
        "historicalPriceCandidates": len(prices),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
