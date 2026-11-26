#!/usr/bin/env python3
"""Record Philippine launch research for both POCO F4 GT configurations (row 92)."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/poco-f4-gt-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_fadbe684bc9a48"
CODE = "21121210G"
CONFIG_8_128 = f"{DEVICE}-8gb-128gb-ph"
CONFIG_12_256 = f"{DEVICE}-12gb-256gb-ph"

URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_POKO_SPECS = "https://www.po.co/global/product/poco-f4-gt/specs/"
URL_POKO_PRODUCT = "https://www.po.co/global/product/poco-f4-gt/"
URL_POKO_FAQ = "https://www.mi.com/global/support/faq/details/KA-09391/"
URL_MANUAL = "https://alsgp0.fds.api.xiaomi.com/xiaomi-b2c-i18n-upload/user-guides/537f01394686be8e29c75988741ee468.pdf"
URL_GLOBAL_LAUNCH = "https://www.youtube.com/watch?v=1r7mTInG_bU"
URL_UNBOX = "https://unbox.ph/gadget/poco-f4-gt-official-in-the-philippines-with-php-27-6k-starting-price/"
URL_REVU = "https://www.revu.com.ph/2022/04/poco-f4-gt-price-philippines-and-global/"
URL_GIZGUIDE = "https://www.gizguide.com/2022/04/poco-f4-gt-price-specs-official.html"
URL_TECHNOBABOY = "https://www.technobaboy.com/2022/04/27/poco-f4-gt-price-philippines/"
URL_HUNGRYGEEKS = "https://hungrygeeks.com.ph/poco-f4-gt-now-in-ph-starts-at-php-27590/"
URL_YUGATECH_SHOP = "https://www.yugatech.com/shop/poco-f4-gt-12-plus-256gb-global-version/"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/xiaomi-poco-f4-gt"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-poco-f4-gt-global-12gb-256gb"
URL_GSMARENA = "https://www.gsmarena.com/xiaomi_poco_f4_gt-11479.php"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-gen-1-mobile-platform"
URL_QUALCOMM_BRIEF = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/snapdragon-8-gen-1-mobile-platform-product-brief.pdf"
URL_IMAGE = "https://i01.appmifile.com/webfile/globalimg/products/pc/poco-f4-gt/specs01.png"


def src(source_id, publisher, url, purpose, note, publication_date=None):
    return {"id": source_id, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("poco_f4_gt_ntc", "National Telecommunications Commission Philippines", URL_NTC,
        "Philippine equipment registration and model-code listing",
        "The 2022 NTC GEC lists POCO model 21121210G as a smartphone; its marketing-name column is blank. POCO/Xiaomi's official user guide maps 21121210G to the POCO F4 GT, establishing the exact model match."),
    src("poco_f4_gt_manual", "Xiaomi / POCO", URL_MANUAL,
        "Primary exact model code, manufacturer, connectivity/regulatory and in-box accessory cross-check",
        "Xiaomi's POCO F4 GT user guide identifies brand POCO and model 21121210G, manufacturer Xiaomi Communications Co., Ltd.; it notes Wi-Fi 6E availability can vary by region and includes a Type-C-to-3.5 mm audio adapter."),
    src("poco_f4_gt_global_specs", "POCO Global", URL_POKO_SPECS,
        "Primary exact-model hardware, configurations, colors, and image",
        "POCO's product page lists 8/128 and 12/256 configurations, LPDDR5, UFS 3.1, Stealth Black/Knight Silver/Cyber Yellow, display, cameras, battery, charging, bands, Wi-Fi 6E, Bluetooth, audio, sensors, and Android 12-based MIUI 13 for POCO. Market-dependent features remain qualified."),
    src("poco_f4_gt_faq", "Xiaomi Global Support", URL_POKO_FAQ,
        "Primary model-specific FAQ on IP rating, chipset, display, external storage, NFC, Bluetooth, and charging",
        "Xiaomi's exact POCO F4 GT FAQ lists IP53 splash/dust resistance, Snapdragon 8 Gen 1, no external SD card, NFC (availability varies by region), Bluetooth 5.2, and display details. Local Technobaboy reports IPX4, so the IP rating is retained as a conflict."),
    src("poco_f4_gt_global_launch", "POCO Global (verified channel)", URL_GLOBAL_LAUNCH,
        "Manufacturer global launch date",
        "POCO Global's verified channel published the F4 GT launch event on April 26, 2022; the Chinese Redmi K50 Gaming announcement predates this global product launch.", "2022-04-26"),
    src("poco_f4_gt_unbox_ph", "Unbox Philippines", URL_UNBOX,
        "Philippine launch pricing, two local configurations, pre-order promotion, and retail start date",
        "Reports PHP 27,590 for 8/128 and PHP 30,990 for 12/256; early-bird prices PHP 24,390 and PHP 27,990 from April 28 to May 12, 2022; official Lazada/Shopee availability beginning May 13.", "2022-04-27"),
    src("poco_f4_gt_revu_ph", "REVU Philippines", URL_REVU,
        "Philippine variants, launch pricing, global launch date, and promotional price cross-check",
        "Published April 26, 2022. Identifies 8/128 and 12/256 Philippines offers, April 28-May 12 early-bird prices, May 13 SRPs, and the global launch event/colors.", "2022-04-26"),
    src("poco_f4_gt_gizguide_ph", "GIZGUIDE Philippines", URL_GIZGUIDE,
        "Philippine launch announcement and local technical/price cross-check",
        "Published April 26, 2022. Lists Philippine 8/128 and 12/256 SRPs and promotional prices, hardware, colors, connectivity, and the exact launch timing.", "2022-04-26"),
    src("poco_f4_gt_technobaboy_ph", "Technobaboy Philippines", URL_TECHNOBABOY,
        "Philippine price, configuration, and hardware cross-check",
        "Published April 27, 2022. Reports both local configurations and April 28-May 12 offer prices, May 13 full availability, specs, colors, and IPX4, which conflicts with Xiaomi's official IP53 FAQ.", "2022-04-27"),
    src("poco_f4_gt_hungrygeeks_ph", "HungryGeeks Philippines", URL_HUNGRYGEEKS,
        "Official online-channel and preorder corroboration",
        "Reports the 8/128 and 12/256 Philippine prices and the April 28-May 12 pre-order period through POCO's official Lazada and Shopee flagship stores.", "2022-04-27"),
    src("poco_f4_gt_yugatech_shop", "YugaTech Shop", URL_YUGATECH_SHOP,
        "Dated historical local retailer price observation for the exact 12/256 SKU",
        "The product page identifies POCO F4 GT 12+256GB Global Version, shows a November 12, 2026 verified lowest store price of PHP 30,790, and currently says no verified price; its linked POCO Official Store Global listing now says check at store. Record PHP 30,790 as a dated historical observation, not as current.", "2026-11-12"),
    src("poco_f4_gt_nanoreview", "NanoReview", URL_NANOREVIEW,
        "Secondary exact-model CPU/GPU architecture and spec cross-check",
        "Exact-model page used for Snapdragon 8 Gen 1 core layout, Adreno 730, display, battery, camera, connectivity, and configuration cross-checks. Benchmarks, ratings, global prices, and generic support claims are not copied into the inventory."),
    src("poco_f4_gt_kimovil", "Kimovil", URL_KIMOVIL,
        "Secondary global model configurations and hardware cross-check",
        "Exact model lists global 8/128 and 12/256 versions and the model alias 21121210G. International seller prices are not treated as Philippine current prices."),
    src("poco_f4_gt_gsmarena", "GSMArena", URL_GSMARENA,
        "Secondary exact model-number family and technical cross-check",
        "Exact POCO F4 GT listing identifies model 21121210G and is used for model-family/specification cross-checks. Regional details are checked against POCO and local launch evidence."),
    src("poco_f4_gt_qualcomm", "Qualcomm", URL_QUALCOMM,
        "Primary Snapdragon 8 Gen 1 platform reference",
        "Qualcomm identifies Kryo CPU up to 3 GHz, Adreno GPU family, X65 modem, and 4 nm process. The phone's Adreno 730 model is cross-checked with exact-model material; benchmark claims are omitted."),
    src("poco_f4_gt_qualcomm_brief", "Qualcomm", URL_QUALCOMM_BRIEF,
        "Primary Snapdragon 8 Gen 1 platform brief",
        "Qualcomm's product brief documents the 4 nm Snapdragon 8 Gen 1 platform and feature set; handset-specific values remain attributed to POCO/Xiaomi."),
]


def fld(field_id, status, source_id, source_value, normalized, note,
        catalog_key=None, catalog_value=None, unit=None, configuration_match=None):
    result = {"fieldId": field_id, "status": status, "sourceId": source_id,
              "sourceValue": source_value, "normalizedValue": normalized,
              "note": note, "configurationMatch": configuration_match or "POCO F4 GT 21121210G; Philippine launch configuration"}
    if catalog_key:
        result["catalogKey"] = catalog_key
        result["catalogValue"] = catalog_value
    if unit:
        result["unit"] = unit
    return result


def fields_for(config_id, ram, storage, srp, promo):
    match = f"POCO F4 GT 21121210G, Philippine {ram} GB RAM / {storage} GB storage configuration"
    def f(*args, **kwargs):
        kwargs["configuration_match"] = match
        return fld(*args, **kwargs)
    return [
        f("model_number", "VERIFIED", "poco_f4_gt_ntc", "NTC GEC lists POCO model 21121210G; Xiaomi user guide identifies this as POCO F4 GT", CODE,
          "Exact NTC model code linked to the POCO F4 GT by the manufacturer user guide."),
        f("global_release_date", "VERIFIED", "poco_f4_gt_global_launch", "POCO Global F4 GT launch event: April 26, 2022", "2022-04-26",
          "Uses the official global event date; it is separate from Philippine preorder and retail dates."),
        f("configuration", "VERIFIED_SECONDARY", "poco_f4_gt_unbox_ph", f"Philippine launch offer: {ram} GB RAM / {storage} GB storage; POCO Global lists this exact hardware configuration", f"{ram} GB RAM / {storage} GB storage; Stealth Black, Knight Silver, Cyber Yellow",
          "Local launch coverage documents both configurations and the manufacturer lists both globally. Colors are options across the same hardware configuration; no color-specific SKU distinction was found."),
        f("philippine_release_date", "VERIFIED_SECONDARY", "poco_f4_gt_unbox_ph", "Official Philippine launch reported April 26; official-store pre-order opened April 28, 2022", "2022-04-28",
          "Date label is the earliest dated authorized online preorder; retail availability at SRP was reported from May 13."),
        f("official_launch_price_php", "VERIFIED_SECONDARY", "poco_f4_gt_unbox_ph", f"Philippine SRP for {ram}/{storage} configuration: PHP {srp:,}", srp,
          "Historical PH launch SRP, cross-checked by REVU, GIZGUIDE and Technobaboy. Not a current offer.", unit="PHP",),
        f("promotional_launch_price_php", "VERIFIED_SECONDARY", "poco_f4_gt_unbox_ph", f"Preorder early-bird offer for {ram}/{storage}: PHP {promo:,}, April 28-May 12, 2022", promo,
          "Dated early-bird promotion through official online shops; not the standard SRP or current price.", unit="PHP"),
        f("current_price_php", "PENDING_VERIFICATION", "poco_f4_gt_unbox_ph", "No current dated, orderable Philippine offer was verified", None,
          "Keep current price blank; the 2022 SRP and expired early-bird prices are historical only.", unit="PHP"),
        f("display_size", "VERIFIED", "poco_f4_gt_global_specs", "6.67-inch flat AMOLED DotDisplay", 6.67,
          "POCO exact product specs; local launch sources agree.", "displayInches", 6.67, "inches"),
        f("display_technology", "VERIFIED", "poco_f4_gt_global_specs", "AMOLED DotDisplay", "AMOLED",
          "Manufacturer exact-model specification.", "displayType", "AMOLED"),
        f("display_resolution", "VERIFIED", "poco_f4_gt_global_specs", "2400 × 1080 FHD+", "2400 x 1080",
          "Manufacturer resolution.", "resolution", "2400 x 1080", "pixels"),
        f("display_refresh_rate", "VERIFIED", "poco_f4_gt_global_specs", "Up to 120 Hz", 120,
          "Manufacturer exact-model specification.", "refreshHz", 120, "Hz"),
        f("display_brightness", "VERIFIED", "poco_f4_gt_global_specs", "HBM 800 nits (typical)", "800 nits HBM (typical)",
          "POCO reports an HBM figure; it is not labelled as peak brightness.", unit="nits"),
        f("display_protection", "VERIFIED", "poco_f4_gt_global_specs", "Corning Gorilla Glass Victus", "Corning Gorilla Glass Victus",
          "Manufacturer exact-model display protection."),
        f("chipset", "VERIFIED", "poco_f4_gt_global_specs", "Qualcomm Snapdragon 8 Gen 1", "Qualcomm Snapdragon 8 Gen 1",
          "POCO exact specs and Philippine sources agree.", "chipset", "Qualcomm Snapdragon 8 Gen 1"),
        f("process_node", "VERIFIED", "poco_f4_gt_qualcomm", "Snapdragon 8 Gen 1 uses 4 nm process technology", 4,
          "Qualcomm platform-level process node.", unit="nm"),
        f("cpu", "VERIFIED_SECONDARY", "poco_f4_gt_nanoreview", "1x Cortex-X2 at 3.0 GHz + 3x Cortex-A710 at 2.5 GHz + 4x Cortex-A510 at 1.8 GHz", "1x Cortex-X2 3.0 GHz + 3x Cortex-A710 2.5 GHz + 4x Cortex-A510 1.8 GHz",
          "Exact chipset architecture cross-check; Qualcomm publishes Kryo maximum clock but not this cluster on its consumer page.", "cpu", "1x Cortex-X2 3.0 GHz + 3x Cortex-A710 2.5 GHz + 4x Cortex-A510 1.8 GHz"),
        f("gpu", "VERIFIED_SECONDARY", "poco_f4_gt_nanoreview", "Adreno 730", "Qualcomm Adreno 730",
          "Exact-model chipset cross-check; Qualcomm identifies the Adreno GPU family.", "gpu", "Qualcomm Adreno 730"),
        f("operating_system", "VERIFIED", "poco_f4_gt_global_specs", "MIUI 13 for POCO based on Android 12", "MIUI 13 for POCO based on Android 12",
          "Launch operating system only; later updates are not substituted.", "os", "MIUI 13 for POCO based on Android 12"),
        f("os_support", "PENDING_VERIFICATION", "poco_f4_gt_faq", "Current official support end date for 21121210G was not established in the reviewed primary sources", None,
          "Do not infer support duration from update releases or generic brand policy."),
        f("ram_capacity", "VERIFIED", "poco_f4_gt_global_specs", f"{ram} GB RAM configuration", ram,
          "POCO Global explicitly lists both memory configurations; local price listings bind the selected RAM to this variant.", "ramGb", ram, "GB"),
        f("ram_type", "VERIFIED", "poco_f4_gt_global_specs", "LPDDR5 RAM", "LPDDR5",
          "Manufacturer exact-model specification.", "ramType", "LPDDR5"),
        f("storage_capacity", "VERIFIED_SECONDARY", "poco_f4_gt_unbox_ph", f"Philippine launch listing: {storage} GB internal storage", storage,
          "Local listing matched to the exact POCO Global variant.", "storageGb", storage, "GB"),
        f("storage_type", "VERIFIED", "poco_f4_gt_global_specs", "UFS 3.1 storage", "UFS 3.1",
          "Manufacturer exact-model specification.", "storageType", "UFS 3.1"),
        f("storage_expansion", "VERIFIED", "poco_f4_gt_faq", "No external SD card support", "No microSD card slot",
          "Xiaomi POCO F4 GT FAQ explicitly states no external SD card support."),
        f("rear_camera_system", "VERIFIED", "poco_f4_gt_global_specs", "64 MP main + 8 MP ultra-wide + 2 MP macro", "64 MP main + 8 MP ultra-wide + 2 MP macro",
          "Manufacturer and Philippine launch sources agree.", "rearCameraMp", "64 + 8 + 2 MP"),
        f("main_camera_sensor", "VERIFIED", "poco_f4_gt_global_specs", "64 MP IMX686, f/1.9, PDAF", "Sony IMX686 64 MP, f/1.9",
          "POCO exact-model sensor specification."),
        f("ultrawide_camera", "VERIFIED", "poco_f4_gt_global_specs", "8 MP ultra-wide, f/2.2, 120° field of view", "8 MP ultra-wide, f/2.2, 120° FOV",
          "Manufacturer exact-model camera specification."),
        f("macro_camera", "VERIFIED", "poco_f4_gt_global_specs", "2 MP macro, f/2.4", "2 MP macro, f/2.4",
          "Manufacturer exact-model camera specification."),
        f("front_camera", "VERIFIED", "poco_f4_gt_global_specs", "20 MP IMX596, f/2.4", 20,
          "POCO exact-model page and local sources agree.", "frontCameraMp", 20, "MP"),
        f("video_recording", "VERIFIED", "poco_f4_gt_global_specs", "Rear video up to 4K at 60 fps; front camera recording modes are not specified on the reviewed product page", "Rear up to 4K@60fps; front maximum not recorded",
          "Only the documented rear maximum is normalized; no front recording mode is inferred.", "video", "Rear up to 4K@60fps; front maximum not recorded"),
        f("battery_capacity", "VERIFIED", "poco_f4_gt_global_specs", "4700 mAh typical capacity (dual 2350 mAh cells)", 4700,
          "POCO's published value is typical capacity; it does not provide a rated total in the reviewed product page.", "batteryMah", 4700, "mAh typical"),
        f("battery_technology", "VERIFIED_SECONDARY", "poco_f4_gt_nanoreview", "Li-Po; non-removable", "Li-Po; non-removable",
          "Exact-model secondary reference; official specs confirm dual-cell construction but not the chemistry label."),
        f("wired_charging", "VERIFIED", "poco_f4_gt_global_specs", "120W HyperCharge; 120W adapter included", 120,
          "Manufacturer and Philippine launch reports agree.", "chargingW", 120, "W"),
        f("wireless_charging", "VERIFIED_SECONDARY", "poco_f4_gt_nanoreview", "Wireless charging not supported", "Not supported",
          "Secondary exact-model specification; no wireless charging hardware is listed by POCO."),
        f("dimensions", "VERIFIED", "poco_f4_gt_global_specs", "162.5 × 76.7 × 8.5 mm", "162.5 x 76.7 x 8.5 mm",
          "POCO exact-model specification.", "dimensions", "162.5 x 76.7 x 8.5 mm", "mm"),
        f("weight", "VERIFIED", "poco_f4_gt_global_specs", "210 g", 210,
          "Manufacturer exact-model specification.", "weightG", 210, "g"),
        f("materials", "VERIFIED_SECONDARY", "poco_f4_gt_nanoreview", "Glass front with Gorilla Glass Victus, glass back, metal frame", "Glass front (Gorilla Glass Victus); glass back; metal frame",
          "Exact-model secondary build description; local sources report the same materials generally."),
        f("ingress_protection", "CONFLICTING_INFORMATION", "poco_f4_gt_faq", "Xiaomi FAQ gives IP53; Technobaboy reports IPX4", None,
          "Official support and local launch coverage disagree on the water/dust rating. Leave the normalized IP rating blank; do not choose one rating."),
        f("sim_esim", "VERIFIED", "poco_f4_gt_global_specs", "Dual Nano-SIM; eSIM not listed", "Dual Nano-SIM; eSIM not recorded",
          "POCO exact-model page lists dual SIM; it does not claim eSIM support.", "sim", "Dual Nano-SIM; eSIM not recorded"),
        f("cellular_bands", "VERIFIED", "poco_f4_gt_global_specs", "Global model bands: GSM 2/3/5/8; WCDMA 1/2/4/5/6/8/19; LTE FDD 1/2/3/4/5/7/8/12/17/18/19/20/26/28 and TDD 38/40/41; 5G NSA/SA n1/3/5/7/8/20/28/38/40/41/77/78", "Manufacturer-published global 2G/3G/4G/5G bands; local carrier support not independently tested",
          "POCO lists the global band set and states connectivity depends on market and local operator support.", "cellular", "Manufacturer-published global 2G/3G/4G/5G bands; local carrier support not independently tested"),
        f("wifi", "VERIFIED", "poco_f4_gt_manual", "Wi-Fi 6E support may vary by region and local network; POCO lists 2.4/5/6 GHz Wi-Fi 6E", "Wi-Fi 6E; region and OTA dependent",
          "POCO and Xiaomi both qualify Wi-Fi 6E availability; local coverage also lists 6E.", "wifi", "Wi-Fi 6E; region and OTA dependent"),
        f("bluetooth", "VERIFIED", "poco_f4_gt_faq", "Bluetooth 5.2", "Bluetooth 5.2",
          "Xiaomi POCO F4 GT FAQ and product specs agree."),
        f("usb", "VERIFIED", "poco_f4_gt_global_specs", "USB Type-C; Type-C-to-3.5 mm headphone adapter included", "USB Type-C; OTG; in-box 3.5 mm adapter",
          "POCO includes a Type-C audio adapter; connector generations are not inferred.", "ports", "USB Type-C; OTG; in-box 3.5 mm adapter"),
        f("nfc", "VERIFIED_SECONDARY", "poco_f4_gt_gizguide_ph", "Philippine launch spec lists NFC; manufacturer notes regional availability varies", "Yes, reported for Philippine launch unit",
          "Local launch coverage lists NFC; POCO notes availability can vary by market."),
        f("gnss", "VERIFIED", "poco_f4_gt_global_specs", "GPS L1+L5, GLONASS G1, Galileo E1+E5a, BeiDou B1I+B1C+B2a", "GPS, GLONASS, Galileo, BeiDou",
          "POCO's exact-model GNSS list. QZSS/NavIC support is not added because the primary product page does not list it.", "gnss", "GPS L1+L5, GLONASS, Galileo, BeiDou"),
        f("audio", "VERIFIED", "poco_f4_gt_global_specs", "Symmetrical quad speakers, Dolby Atmos, Hi-Res Audio; no headphone jack, Type-C adapter in box", "Symmetrical quad speakers; Dolby Atmos; Hi-Res Audio; USB-C audio",
          "POCO product page and local coverage identify quad speakers; adapter is included in box.", "sound", "Symmetrical quad speakers; Dolby Atmos; Hi-Res Audio; USB-C audio"),
        f("sensors", "VERIFIED", "poco_f4_gt_global_specs", "Proximity, 360-degree ambient light, color temperature, gyroscope, accelerometer, electronic compass, IR blaster, fingerprint, flicker, SAR sensors", "Proximity; ambient light; color temperature; gyroscope; accelerometer; compass; IR; side fingerprint; flicker; SAR",
          "POCO exact-model sensor list; magnetic pop-up triggers are also documented as a control feature, not as a sensor."),
        f("gaming_controls", "VERIFIED", "poco_f4_gt_global_specs", "Magnetic pop-up gaming triggers; CyberEngine X-axis linear motor; LiquidCool Technology 3.0", "Magnetic pop-up triggers; X-axis linear motor; LiquidCool 3.0",
          "Distinctive hardware/features on the exact POCO F4 GT product page."),
    ]


def variant_specs(ram, storage):
    return {
        "displayInches": 6.67, "displayType": "AMOLED", "resolution": "2400 x 1080",
        "refreshHz": 120, "chipset": "Qualcomm Snapdragon 8 Gen 1",
        "cpu": "1x Cortex-X2 3.0 GHz + 3x Cortex-A710 2.5 GHz + 4x Cortex-A510 1.8 GHz",
        "gpu": "Qualcomm Adreno 730", "os": "MIUI 13 for POCO based on Android 12",
        "ramGb": ram, "ramType": "LPDDR5", "storageGb": storage, "storageType": "UFS 3.1",
        "rearCameraMp": "64 + 8 + 2 MP", "frontCameraMp": 20,
        "video": "Rear up to 4K@60fps; front maximum not recorded", "batteryMah": 4700,
        "chargingW": 120, "wirelessChargingW": None, "dimensions": "162.5 x 76.7 x 8.5 mm",
        "weightG": 210, "sim": "Dual Nano-SIM; eSIM not recorded",
        "cellular": "Manufacturer-published global 2G/3G/4G/5G bands; local carrier support not independently tested",
        "wifi": "Wi-Fi 6E; region and OTA dependent", "bluetooth": "Bluetooth 5.2",
        "ports": "USB Type-C; OTG; in-box 3.5 mm adapter",
        "gnss": "GPS L1+L5, GLONASS, Galileo, BeiDou",
        "sound": "Symmetrical quad speakers; Dolby Atmos; Hi-Res Audio; USB-C audio",
    }


def variant_sources():
    return {
        "displayInches": URL_POKO_SPECS, "displayType": URL_POKO_SPECS,
        "resolution": URL_POKO_SPECS, "refreshHz": URL_POKO_SPECS,
        "chipset": URL_POKO_SPECS, "cpu": URL_NANOREVIEW, "gpu": URL_NANOREVIEW,
        "os": URL_POKO_SPECS, "ramGb": URL_POKO_SPECS, "ramType": URL_POKO_SPECS,
        "storageGb": URL_POKO_SPECS, "storageType": URL_POKO_SPECS,
        "rearCameraMp": URL_POKO_SPECS, "frontCameraMp": URL_POKO_SPECS,
        "video": URL_POKO_SPECS, "batteryMah": URL_POKO_SPECS,
        "chargingW": URL_POKO_SPECS, "dimensions": URL_POKO_SPECS,
        "weightG": URL_POKO_SPECS, "sim": URL_POKO_SPECS, "cellular": URL_POKO_SPECS,
        "wifi": URL_POKO_SPECS, "bluetooth": URL_POKO_FAQ, "ports": URL_POKO_SPECS,
        "gnss": URL_POKO_SPECS, "sound": URL_POKO_SPECS,
    }


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    # Re-running this sourced review replaces only its own two configuration
    # rows and preserves the order of every other review record.
    manual["records"] = [r for r in manual["records"] if r.get("deviceId") != DEVICE]
    device = next((r for r in catalog if r.get("id") == DEVICE), None)
    if not device or device.get("workbookRow") != 92 or device.get("model") not in {"F4 GT", "POCO F4 GT"}:
        raise SystemExit("Catalog target guard failed for workbook row 92 POCO F4 GT")

    label_8 = "8 GB RAM / 128 GB storage (Stealth Black / Knight Silver / Cyber Yellow)"
    label_12 = "12 GB RAM / 256 GB storage (Stealth Black / Knight Silver / Cyber Yellow)"
    configs = [
        (CONFIG_8_128, 8, 128, 27590, 24390, label_8),
        (CONFIG_12_256, 12, 256, 30990, 27990, label_12),
    ]
    first_review = None
    reviews = []
    for index, (config, ram, storage, srp, promo, label) in enumerate(configs):
        configuration_match = f"POCO F4 GT 21121210G, Philippine {ram} GB RAM / {storage} GB storage"
        fields = fields_for(config, ram, storage, srp, promo)
        review = {
            "deviceId": DEVICE,
            "configurationId": config,
            "brand": "POCO",
            "model": "F4 GT",
            "configuration": label,
            "configurationLabel": label,
            "modelCode": CODE,
            "sources": SOURCES,
            "fields": fields,
        }
        if index == 0:
            review.update({
                "availabilityEvidence": {
                    "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                    "availabilityStatus": "NTC lists POCO model 21121210G; Xiaomi's official user guide identifies it as POCO F4 GT. Philippine launch sources document official online flagship-store preorders and May retail availability.",
                    "philippineAvailability": "The POCO F4 GT 21121210G was launched in the Philippines on April 26, 2022. Official-channel preorder prices ran April 28-May 12; Philippine retailers reported regular online-store availability at SRP from May 13. Two configurations were documented: 8/128 and 12/256. Current stock and price are not verified.",
                    "observedAt": OBSERVED,
                    "manufacturer": "Xiaomi Communications Co., Ltd.",
                    "catalogModel": "POCO F4 GT",
                    "productLine": "POCO F series",
                    "modelNumber": CODE,
                    "philippineReleaseYear": 2022,
                    "philippineDateLabel": "Philippine preorder start date",
                    "researchNotes": "Exact model 21121210G is registered by NTC under the POCO brand and identified by the manufacturer guide as POCO F4 GT. Philippine coverage documents two separate retail configurations, 8/128 at PHP 27,590 SRP (PHP 24,390 early-bird) and 12/256 at PHP 30,990 SRP (PHP 27,990 early-bird). The early-bird prices applied April 28-May 12, 2022; SRP availability was reported from May 13. The official Xiaomi FAQ lists IP53 while one Philippine source lists IPX4; the IP rating is left blank. Current price is blank. Workbook eligibility remains Pending.",
                    "qualityFlag": "Exact NTC/model-code match and two Philippine configurations/prices verified; historic preorder promos separated from SRPs; current price unavailable; IP rating conflict retained; image reuse rights not established; study eligibility remains Pending.",
                    "openIssues": [
                        {"issue": "Xiaomi's FAQ lists IP53; Technobaboy lists IPX4", "action": "Keep ingress rating blank until exact Philippine SKU documentation resolves the conflict."},
                        {"issue": "No current dated, orderable Philippine price was verified", "action": "Keep current price blank; preserve SRPs and April 28-May 12 promos as historical snapshots."},
                        {"issue": "POCO's exact product image is available but reuse permission or a reusable license is not recorded", "action": "Keep the neutral placeholder until image rights are documented."},
                        {"issue": "Wi-Fi 6E and NFC availability are region-dependent", "action": "Preserve manufacturer qualifiers; do not treat all global features as a carrier or region guarantee."},
                        {"issue": "Workbook eligibility is Pending", "action": "Preserve the study's Pending status."},
                    ],
                },
                "replacementVariants": [
                    {"id": CONFIG_8_128, "label": label_8, "sku": None, "modelCode": CODE,
                     "notes": "Historical Philippine launch SRP PHP 27,590; April 28-May 12, 2022 early-bird promotion PHP 24,390. Current price not verified.", "workbookRow": 92},
                    {"id": CONFIG_12_256, "label": label_12, "sku": None, "modelCode": CODE,
                     "notes": "Historical Philippine launch SRP PHP 30,990; April 28-May 12, 2022 early-bird promotion PHP 27,990. Current price not verified.", "workbookRow": 92},
                ],
                "replaceUnrecordedPlaceholder": True,
            })
            first_review = review
        reviews.append(review)

    manual["records"].extend(reviews)  # Preserve established source order; existing records include ordered multi-configuration rows.

    device["manufacturer"] = "Xiaomi Communications Co., Ltd."
    device["productLine"] = "POCO F series"
    device["modelNumber"] = CODE
    device["releaseDate"] = "2022-04-26"
    device["philippineAvailabilityDate"] = "2022-04-28"
    device["philippineDateLabel"] = "Philippine preorder start date"
    device["philippineReleaseYear"] = 2022
    device["localEvidenceObservedAt"] = OBSERVED
    device["verificationStatus"] = "VERIFIED_AUTHORIZED_AVAILABILITY"
    device["scopeStatus"] = "Pending"
    device["qualityFlag"] = first_review["availabilityEvidence"]["qualityFlag"]
    device["exclusionReason"] = None
    device["exclusionEvidence"] = None
    device["philippineAvailability"] = first_review["availabilityEvidence"]["philippineAvailability"]
    device["availabilityStatus"] = first_review["availabilityEvidence"]["availabilityStatus"]
    device["discontinued"] = None
    device["researchNotes"] = first_review["availabilityEvidence"]["researchNotes"]
    device["openIssues"] = first_review["availabilityEvidence"]["openIssues"]
    device["sources"] = [
        {"organization": s["publisher"], "url": s["url"], "observedAt": OBSERVED,
         "publishedAt": s["publicationDate"], "purpose": s["purpose"], "note": s["note"]}
        for s in SOURCES
    ]
    device["variants"] = []
    for config, ram, storage, srp, promo, label in configs:
        specs = variant_specs(ram, storage)
        device["variants"].append({
            "id": config, "label": label, "specs": specs, "specSources": variant_sources(),
            "pricePhp": None, "priceCondition": None, "priceType": None,
            "priceObservedAt": None, "priceSourceUrl": None,
            "listingStatus": "Historical Philippine retail configuration; current listing not verified",
            "notes": f"Historical Philippine launch SRP PHP {srp:,}; April 28-May 12, 2022 early-bird promotion PHP {promo:,}. Current price not verified.",
            "sku": None, "modelCode": CODE, "workbookRow": 92,
        })
    device["imageId"] = DEVICE

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "POCO's official product page contains an exact-model F4 GT image, but no reusable image license or written permission to copy/embed is recorded in the project.",
        "sourcePage": URL_POKO_PRODUCT,
        "assetUrl": URL_IMAGE,
        "scope": "Exact POCO F4 GT model 21121210G; manufacturer product image",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for POCO F4 GT 21121210G",
    }

    prices = []
    for config, ram, storage, srp, promo, label in configs:
        for amount, kind, publication, excerpt in [
            (srp, "historical_ph_launch_srp", "2022-04-27", f"Historical Philippine SRP for POCO F4 GT {ram}/{storage}: PHP {srp:,}; not a current price."),
            (promo, "historical_ph_launch_promotion", "2022-04-27", f"Historical April 28-May 12, 2022 early-bird Philippine promotion for POCO F4 GT {ram}/{storage}: PHP {promo:,}; not a current price."),
        ]:
            prices.append({
                "device_id": DEVICE, "amount_php": amount, "configuration_id": config,
                "configuration_match": f"philippine_21121210g_{ram}gb_{storage}gb",
                "variant_ram_gb": ram, "variant_storage_gb": storage,
                "price_type": kind, "source_published_at": publication,
                "excerpt": excerpt, "source_url": URL_UNBOX,
                "source_kind": "historical_local_price_candidate",
                "observed_at": OBSERVED_AT, "local_availability_verified": True,
                "availability_status": "historical_price_not_current",
            })
    # A more recent dated price was verified for the exact 12/256 listing, but
    # its page has no verified current price, so retain it as history only.
    prices.append({
        "device_id": DEVICE, "amount_php": 30790, "configuration_id": CONFIG_12_256,
        "configuration_match": "philippine_listed_global_21121210g_12gb_256gb",
        "variant_ram_gb": 12, "variant_storage_gb": 256,
        "price_type": "historical_last_verified_store_price", "source_published_at": "2026-11-12",
        "excerpt": "YugaTech Shop's exact POCO F4 GT 12+256GB Global Version page records a verified lowest store price of PHP 30,790 on November 12, 2026; the page currently reports no verified price and the store link now says check at store.",
        "source_url": URL_YUGATECH_SHOP, "source_kind": "dated_local_price_snapshot",
        "observed_at": OBSERVED_AT, "local_availability_verified": True,
        "availability_status": "historical_price_not_current",
    })
    price_snapshot = {
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "POCO", "model_name": "F4 GT", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC 2022 GEC lists POCO model 21121210G; Xiaomi's official guide maps that exact code to POCO F4 GT."},
            {"device_id": DEVICE, "source_url": URL_UNBOX, "result": "Philippine launch pricing for 8/128 and 12/256 configurations, with SRPs and dated April 28-May 12 early-bird prices."},
            {"device_id": DEVICE, "source_url": URL_POKO_SPECS, "result": "Manufacturer specs confirm both configurations and exact global hardware; local records remain specific to dated Philippine launch pricing."},
            {"device_id": DEVICE, "source_url": URL_POKO_FAQ, "result": "Official FAQ states IP53; a Philippine launch source states IPX4, so ingress protection remains unresolved."},
        ],
        "prices": prices,
    }
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(price_snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Reviewed {DEVICE}: row 92, {CODE}, 2 configurations, {len(SOURCES)} sources, {len(fields_for(CONFIG_8_128, 8, 128, 27590, 24390))} assessments/configuration")


if __name__ == "__main__":
    main()
