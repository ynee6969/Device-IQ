#!/usr/bin/env python3
"""Record the source-matched Philippine HONOR Magic V3 configuration."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-magic-v3-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_3e151a6e24dc04"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-12gb-512gb-ph"

URL_HONOR = "https://www.honor.com/ph/phones/honor-magic-v3/"
URL_HONOR_SPECS = "https://www.honor.com/ph/phones/honor-magic-v3/spec/"
URL_HONOR_MY_SPECS = "https://www.honor.com/my/phones/honor-magic-v3/spec/"
URL_HONOR_REPORT = "https://www.honor.com/content/dam/honor/global/honor-esg/green_environmental_protection/1230pdf/phones/HONOR%20Environmental%20Report-HONOR%20Magic%20V3.pdf"
URL_YUGA = "https://www.yugatech.com/news/honor-magic-v3-specs-price-philippines/"
URL_YUGA_PRICE_LIST = "https://www.yugatech.com/honor-gadget-price-list-philippines/"
URL_YUGA_SHOP = "https://www.yugatech.com/shop/honor-magic-v3-slimmer-stro/"
URL_JAM = "https://jamonline.ph/tech-news/honor-magic-v3-specs-price-philippines/"
URL_REVU = "https://www.revu.com.ph/2024/11/honor-magic-v3-ph-nationwide-release/"
URL_UNGEEK = "https://www.ungeek.ph/2024/11/honor-magic-v3-philippines-price-and-availability-announced/"
IMAGE_URL = "https://www-file.honor.com/content/dam/honor/ph/specs/smartphone/honor-magic-v3/honor-magic-v3-id-green.png"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None, source_kind: str | None = None) -> dict:
    item = {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}
    if source_kind:
        item["sourceKind"] = source_kind
    return item


def field(fid: str, source_id: str, value, normalized_value, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, configuration_match="Exact Philippine 12 GB RAM / 512 GB storage configuration") -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": source_id,
            "sourceValue": value, "normalizedValue": normalized_value,
            "note": note, "configurationMatch": configuration_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized_value
    if unit:
        item["unit"] = unit
    return item


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device or device.get("category") != "smartphones" or device.get("brand", "").casefold() != "honor" or device.get("model") != "Magic V3":
        raise ValueError("The source record no longer matches the HONOR Magic V3 workbook identity")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR Magic V3 already has a manual review; inspect it before replacing")

    sources = [
        source("honor_magic_v3_ph_official_product", "HONOR Philippines", URL_HONOR,
               "Official Philippine product identity, dimensions, battery, charging, and foldable design cross-check",
               "HONOR Philippines identifies Magic V3 and states 9.2 mm folded / 4.35 mm unfolded / 226 g, a 5150 mAh silicon-carbon battery, 66 W wired charging, and 50 W wireless charging."),
        source("honor_magic_v3_ph_official_specs", "HONOR Philippines", URL_HONOR_SPECS,
               "Official Philippine specifications page and image source",
               "Official HONOR Philippines specification page for the exact Magic V3 model; indexed page text exposes the section labels and exact color image assets. Detailed values used below are transcribed from the contemporaneous Philippine sources."),
        source("honor_magic_v3_official_product_report", "HONOR", URL_HONOR_REPORT,
               "Manufacturer report identifying the 12 GB / 512 GB configuration, dimensions, weight, and display sizes",
               "HONOR's product environmental report identifies its assessed HONOR Magic V3 as 12 GB RAM / 512 GB storage and lists 7.92-inch inner / 6.43-inch external displays, folded dimensions 156.60 × 74.00 × 9.20 mm, unfolded dimensions 156.60 × 145.30 × 4.35 mm, and 226 g handset weight."),
        source("honor_magic_v3_official_specs_malaysia", "HONOR Malaysia", URL_HONOR_MY_SPECS,
               "Official regional technical specification cross-check for GPU model",
               "HONOR Malaysia's official Magic V3 specification page identifies the Qualcomm platform's Adreno 750 GPU. The Philippine launch sources identify the same Snapdragon 8 Gen 3 Magic V3 platform."),
        source("honor_magic_v3_ph_launch_yugatech", "YugaTech", URL_YUGA,
               "Contemporaneous Philippine availability, exact configuration, price, and detailed specifications",
               "Published 2024-11-20. Reports the Magic V3 available to buy in the Philippines at PHP 89,999 with 12 GB physical RAM and 512 GB storage. Its detailed specs include both displays, camera system, wireless charging, and regional color-dependent thickness/weight.",
               "2024-11-20"),
        source("honor_magic_v3_ph_launch_jam", "Jam Online", URL_JAM,
               "Independent Philippine launch, local price, configuration, and technology cross-check",
               "Published 2024-11-20. Reports official Philippine launch, PHP 89,999 retail price, 12 GB LPDDR5X RAM / 512 GB UFS 4.0, Android 14 with MagicOS 8.0.1, Snapdragon 8 Gen 3, camera, battery, charging, and IPX8 details.",
               "2024-11-20"),
        source("honor_magic_v3_ph_nationwide_revu", "REVU Philippines", URL_REVU,
               "Nationwide Philippine sale date, authorized channel, and specifications cross-check",
               "Published 2024-11-26. Reports the device was available for purchase at HONOR Experience and partner stores and on official stores, for PHP 89,999, after reservations opened the previous week. Confirms 226 g, IPX8, 5150 mAh, 66 W wired, 50 W wireless, and key cameras.",
               "2024-11-26"),
        source("honor_magic_v3_ph_launch_ungeek", "UnGeek", URL_UNGEEK,
               "Philippine color, price, channel, and launch report cross-check",
               "Philippine launch report gives the same PHP 89,999 price, Green and Black colorways, and Globe/retail availability.",
               "2024-11-20"),
        source("honor_magic_v3_ph_price_history_yugatech", "YugaTech", URL_YUGA_PRICE_LIST,
               "Dated Philippine launch-price history cross-check",
               "YugaTech's price-list entry marks HONOR Magic V3 5G at PHP 89,999 as verified November 20, 2024. This is launch-era price history, not a current offer.",
               "2024-11-20"),
        source("honor_magic_v3_yugatech_shop_price_history", "YugaTech Shop", URL_YUGA_SHOP,
               "Recent historical online price observation and present price-status check",
               "At access time the page showed no verified current store price and listed a last verified low of PHP 79,839 on November 12–13, 2026. The product listing does not identify a RAM/storage variant, so this amount is retained as unmatched historical price evidence only.",
               source_kind="price_history_candidate"),
    ]
    honor_id = "honor_magic_v3_ph_official_product"
    specs_id = "honor_magic_v3_ph_official_specs"
    report_id = "honor_magic_v3_official_product_report"
    my_specs_id = "honor_magic_v3_official_specs_malaysia"
    yuga_id = "honor_magic_v3_ph_launch_yugatech"
    jam_id = "honor_magic_v3_ph_launch_jam"
    revu_id = "honor_magic_v3_ph_nationwide_revu"
    shop_id = "honor_magic_v3_yugatech_shop_price_history"

    fields = [
        field("model_number", yuga_id, "Philippine SKU/model code not stated", None, status="NOT_DISCLOSED", note="Reviewed Philippine manufacturer and launch sources identify the marketing model but do not name the local SKU or model code."),
        field("configuration", report_id, "Manufacturer environmental-report configuration: 12 GB RAM / 512 GB storage", "12 GB RAM / 512 GB storage", status="VERIFIED", note="HONOR's report states its assessed Magic V3 was the 12 GB / 512 GB configuration; YugaTech's local specification lists the same configuration. YugaTech's 24 GB headline includes a separate 12 GB virtual-RAM extension."),
        field("philippine_release_date", yuga_id, "Available for purchase in the Philippines on the report date, November 20, 2024", "2024-11-20", note="Contemporaneous local reporting says it was available for purchase. This is the first documented availability report, not a separate first retail transaction receipt."),
        field("official_launch_price_php", yuga_id, "PHP 89,999, reported at Philippine availability on 2024-11-20", 89999, unit="PHP", note="Historical launch-era price for the documented Philippine model; not a current offer."),
        field("current_price_php", shop_id, "No verified current price at access; latest historical YugaTech store observation was PHP 79,839 on 2026-11-13 with configuration unreported", None, status="NOT_DISCLOSED", unit="PHP", note="YugaTech Shop currently says no verified price is available. Its last historical low does not identify a 12 GB / 512 GB variant, so it is not used as a current or exact-configuration price."),
        field("display_size", yuga_id, "7.92-inch inner foldable display and 6.43-inch cover display", 7.92, key="displayInches", unit="in", note="The public numeric catalog field uses the main inner display diagonal; the cover display remains explicitly documented here."),
        field("display_technology", yuga_id, "Inner and cover: LTPO OLED", "Inner and cover LTPO OLED", key="displayType", note="YugaTech identifies both as LTPO OLED displays."),
        field("display_resolution", yuga_id, "Inner: 2344 × 2156; cover: 2376 × 1060", "Inner 2344 x 2156; cover 2376 x 1060", key="resolution", note="Both display resolutions are recorded separately; the first is the inner foldable panel."),
        field("display_refresh_rate", yuga_id, "120 Hz adaptive on both displays", 120, key="refreshHz", unit="Hz", note="YugaTech lists adaptive refresh up to 120 Hz for both screens."),
        field("display_brightness", yuga_id, "Cover HDR peak 5000 nits; inner peak 1800 nits", "Cover HDR peak 5000 nits; inner peak 1800 nits", unit="nits", note="Different peak brightness values are preserved for the outer and inner displays."),
        field("display_protection", yuga_id, "Cover: HONOR Anti-scratch NanoCrystal Shield; inner: HONOR Super Armored inner screen", "Cover NanoCrystal Shield; inner Super Armored screen", note="The source lists different protection technologies for the two displays."),
        field("chipset", yuga_id, "Qualcomm Snapdragon 8 Gen 3", "Qualcomm Snapdragon 8 Gen 3", key="chipset", note="YugaTech's Philippine specification list."),
        field("process_node", jam_id, "4 nm", 4, unit="nm", note="Jam Online reports the Snapdragon 8 Gen 3 as a 4 nm platform."),
        field("cpu", yuga_id, "8-core CPU, up to 3.3 GHz", "Octa-core, up to 3.3 GHz", key="cpu", note="YugaTech lists the core count and maximum frequency; no core-cluster layout is recorded."),
        field("gpu", my_specs_id, "Adreno 750", "Adreno 750", key="gpu", status="VERIFIED", note="HONOR Malaysia's official Magic V3 specifications identify Adreno 750; the Philippine launch sources match the same Snapdragon 8 Gen 3 platform."),
        field("operating_system", jam_id, "Android 14 with MagicOS 8.0.1", "Android 14 / MagicOS 8.0.1", key="os", note="Launch software version; later updates are not inferred."),
        field("os_support", jam_id, "Software update policy not stated", None, status="NOT_DISCLOSED", note="The reviewed Philippine launch sources do not state a support duration or update count."),
        field("ram_capacity", yuga_id, "12 GB physical RAM; an additional 12 GB is virtual RAM in the 24 GB headline", 12, key="ramGb", unit="GB", note="Only physical RAM is recorded. The reported 24 GB total includes a virtual RAM extension and is not represented as installed physical memory."),
        field("ram_type", jam_id, "LPDDR5X", "LPDDR5X", note="Jam Online's Philippine launch report identifies memory type."),
        field("storage_capacity", yuga_id, "512 GB", 512, key="storageGb", unit="GB", note="Exact Philippine launch configuration."),
        field("storage_type", jam_id, "UFS 4.0", "UFS 4.0", note="Jam Online's Philippine launch report identifies storage technology."),
        field("storage_expansion", yuga_id, "Expandable storage not listed", None, status="NOT_DISCLOSED", note="The reviewed Philippine specifications do not list a memory-card slot or storage expansion."),
        field("rear_camera_system", yuga_id, "50 MP f/1.6 main with OIS + 40 MP f/2.2 ultra-wide (112°) + 50 MP f/3.0 periscope telephoto with OIS", "50 MP main + 40 MP ultra-wide + 50 MP periscope telephoto", note="The source provides module resolution, role, aperture, stabilization and field of view."),
        field("main_camera_sensor", yuga_id, "50 MP main, f/1.6, OIS; sensor model not named", "50 MP f/1.6 OIS; sensor model not disclosed", note="No specific sensor manufacturer/model is identified in the reviewed local sources."),
        field("ultrawide_camera", yuga_id, "40 MP f/2.2, 112° field of view", "40 MP ultra-wide; 112° FoV", note="YugaTech's Philippine specification list."),
        field("telephoto_camera", yuga_id, "50 MP periscope telephoto, f/3.0, OIS; 3.5× optical zoom", "50 MP periscope telephoto; 3.5x optical zoom", note="YugaTech identifies the periscope module and optical zoom."),
        field("front_camera", yuga_id, "20 MP f/2.2 front camera on cover and inner displays", 20, key="frontCameraMp", unit="MP", note="One 20 MP selfie camera is listed for each display location."),
        field("video_recording", yuga_id, "Supported video modes not listed in the reviewed Philippine source", None, status="NOT_DISCLOSED", note="The launch specification does not provide camera video resolution/frame-rate modes."),
        field("battery_capacity", honor_id, "5150 mAh silicon-carbon battery", 5150, key="batteryMah", unit="mAh", status="VERIFIED", note="HONOR Philippines product page and Philippine launch sources identify this capacity."),
        field("battery_technology", honor_id, "Silicon-carbon battery", "Silicon-carbon", status="VERIFIED", note="HONOR Philippines describes the silicon-carbon battery."),
        field("wired_charging", honor_id, "66 W HONOR SuperCharge", 66, key="chargingW", unit="W", status="VERIFIED", note="HONOR Philippines product page and YugaTech specify 66 W wired charging."),
        field("wireless_charging", honor_id, "50 W wireless HONOR SuperCharge; 5 W reverse wired charging", "50 W wireless; 5 W reverse wired", status="VERIFIED", note="HONOR Philippines confirms 50 W wireless; YugaTech lists 5 W reverse wired charging."),
        field("dimensions", report_id, "Folded: 156.60 × 74.00 × 9.20 mm; unfolded: 156.60 × 145.30 × 4.35 mm (manufacturer report configuration)", "Folded 156.6 x 74.0 x 9.2 mm; unfolded 156.6 x 145.3 x 4.35 mm; Green colorway is 9.3 mm folded / 4.4 mm unfolded", note="The manufacturer report provides the Black/general configuration dimensions; YugaTech gives 9.3 mm folded / 4.4 mm unfolded for Green. Both states and color-dependent thickness are retained."),
        field("weight", yuga_id, "226 g (Black) / 230 g (Green)", "226 g Black / 230 g Green", note="YugaTech lists color-specific Black and Green weights; HONOR's environmental report records 226 g for its 12 GB / 512 GB assessed configuration. Both values are retained rather than assuming a color."),
        field("materials", jam_id, "Black color uses faux leather; frame is 7-series aluminum alloy; green back material not stated", "Black faux leather; 7-series aluminum frame; Green back material not recorded", note="Color-specific material is not generalized to every version."),
        field("ingress_protection", revu_id, "IPX8 water resistance", "IPX8 (water resistance; dust rating not stated)", note="REVU reports IPX8. The X indicates that no dust-protection rating is asserted here."),
        field("sim_esim", yuga_id, "Dual Nano-SIM; eSIM supported", "Dual Nano-SIM; eSIM supported", note="YugaTech's Philippine specifications."),
        field("cellular_bands", yuga_id, "5G NR; specific local frequency bands not listed", "5G; specific bands not recorded", key="cellular", note="No band mapping is inferred from the network-generation claim."),
        field("wifi", yuga_id, "Wi-Fi 7: 802.11 a/b/g/n/ac/ax/be", "Wi-Fi 7 (802.11 a/b/g/n/ac/ax/be)", key="wifi", note="YugaTech's Philippine specification list."),
        field("bluetooth", yuga_id, "Bluetooth 5.3", "Bluetooth 5.3", note="YugaTech's Philippine specification list."),
        field("usb", yuga_id, "USB Type-C, USB 3.1 Gen 1", "USB Type-C, USB 3.1 Gen 1", key="ports", note="YugaTech's Philippine specification list."),
        field("nfc", yuga_id, "NFC", "Yes", note="YugaTech's Philippine specification list."),
        field("gnss", yuga_id, "GPS, A-GPS, GLONASS, BeiDou, Galileo, QZSS", "GPS, A-GPS, GLONASS, BeiDou, Galileo, QZSS", note="YugaTech's Philippine specification list."),
        field("audio", yuga_id, "Dual stereo speakers; IR blaster", "Dual stereo speakers; IR blaster", note="The source lists stereo speakers and IR remote; no 3.5 mm jack claim is inferred."),
        field("sensors", yuga_id, "Complete sensor list not stated", None, status="NOT_DISCLOSED", note="The reviewed launch specifications do not provide a full sensor inventory."),
    ]

    review = {
        "deviceId": DEVICE, "configurationId": CONFIG,
        "brand": "HONOR", "model": "Magic V3",
        "configuration": "12 GB RAM / 512 GB storage",
        "configurationLabel": "12 GB RAM / 512 GB storage",
        "sources": sources, "fields": fields,
        "replacementVariants": [{
            "id": CONFIG, "label": "12 GB RAM / 512 GB storage",
            "sku": None, "modelCode": None,
            "notes": "YugaTech and Jam Online report a local 12 GB RAM / 512 GB storage configuration. YugaTech's 24 GB headline counts 12 GB virtual RAM in addition to 12 GB physical; only physical RAM is recorded.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine availability for purchase was reported November 20, 2024; present stock is not established.",
            "philippineAvailability": "YugaTech reported the phone available through HONOR's official online channels and Globe postpaid on November 20, 2024. REVU later reported HONOR Experience/partner stores and official online shops nationwide.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "Magic Series",
            "philippineReleaseYear": 2024,
            "philippineDateLabel": "Philippine availability date",
            "researchNotes": "The workbook's HONOR Magic V3 matches the official HONOR Magic V3 and Philippine Magic V3 5G. Local sources identify 12 GB physical RAM / 512 GB storage; 24 GB marketing total includes virtual RAM. PHP 89,999 is launch-era price history. The latest YugaTech Shop price entry is a historical 2026 observation without configuration matching, and the Shop currently reports no verified price.",
            "qualityFlag": "Current price unavailable; recent historical store price is not configuration-matched",
            "openIssues": [
                {"issue": "Exact Philippine SKU/model code is not recorded", "action": "Keep model code and SKU blank until listed by a source."},
                {"issue": "Current exact-configuration retail price and stock are not verified", "action": "Retain only the 2024 launch price and the unmatched November 2026 price-history record."},
                {"issue": "Weight and thickness vary by color", "action": "Display both Black and Green dimensions/weights without assuming a color."},
                {"issue": "Camera sensor model, video modes, and complete sensor list are not recorded", "action": "Keep these fields unresolved rather than infer from megapixels or chipset."},
                {"issue": "Official product image reuse terms are not established", "action": "Continue showing the neutral placeholder."},
            ],
        },
    }

    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Exact HONOR Magic V3 Green product imagery was identified on the official HONOR Philippines specification page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_HONOR_SPECS,
        "assetUrl": IMAGE_URL,
        "scope": "Exact HONOR Magic V3 model, Green colorway; storage configuration is not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR Magic V3",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "Magic V3", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [{
            "device_id": DEVICE, "amount_php": 79839,
            "configuration_id": None, "configuration_match": "model_level_unmatched",
            "variant_ram_gb": None, "variant_storage_gb": None,
            "price_type": "independent_reported_historical_store_price_unmatched",
            "source_published_at": "2026-11-13",
            "excerpt": "YugaTech Shop page had no verified current price at access; its historical low shows PHP 79,839 on Nov 12–13, 2026, but the listing does not specify the configuration. Do not use as current or exact-variant price.",
            "source_url": URL_YUGA_SHOP, "source_kind": "independent_retail_price_history",
            "observed_at": OBSERVED_AT, "local_availability_verified": False,
            "availability_status": "no_current_verified_offer",
        }],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "HONOR Magic V3 inventory record matched to HONOR Magic V3 5G Philippine launch sources",
        "configuration": "12 GB / 512 GB",
        "reviewedFields": len(fields),
        "availabilityDate": "2024-11-20",
        "historicalLaunchPricePhp": 89999,
        "currentPriceLoaded": False,
        "unmatchedRecentPricePhp": 79839,
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
