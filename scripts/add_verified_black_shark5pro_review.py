#!/usr/bin/env python3
"""Add source-backed Philippine records for Black Shark 5 Pro variants."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/black-shark-5-pro-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_abadb9044528e9"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_OFFICIAL = "https://global.blackshark.com/products/black-shark-5-pro"
URL_IMAGE = "https://global.blackshark.com/cdn/shop/files/5-Pro-Stellar-Black-back.png?v=1750922840&width=1000"
URL_GLOBAL_RELEASE = "https://blackshark.gg/blogs/press-room/black-shark-launches-the-mobile-gaming-flagship-black-shark-5-series-globally"
URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_MANUAL = "https://device.report/m/2abf7c84ef4337f73181cb9e701440fc40a7a6cc648177dd48951993eefb20cd.pdf"
URL_YUGA = "https://www.yugatech.com/mobile/black-shark-5-pro-now-official-price-philippines/"
URL_REVU = "https://www.revu.com.ph/2022/06/black-shark-5-pro-price-philippines/"
URL_XIAOMI_SPECS = "https://www.mi.com/blackshark5pro/specs"
URL_QUALCOMM = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/snapdragon-8-gen-1-mobile-platform-product-brief.pdf"
URL_GUFI = "https://gufi.com.ph/product-category/our-brands/black-shark/"
URL_ALT_SPECS = "https://blackshark.gg/pages/specs-blackshark5-pro"

CONFIGS = [
    {"ram": 8, "storage": 128, "srp": 37999, "promo": 36999},
    {"ram": 12, "storage": 256, "srp": 43999, "promo": 42999},
]


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("black_shark_5_pro_global_product", "Black Shark (Global)", URL_OFFICIAL,
           "Exact model name, colors, and exact-model image source page",
           "The manufacturer page identifies Black Shark 5 Pro and displays Stella Black and Nebula White. Its exact Stellar Black product image was located on the official CDN; no image reuse license was found, so the asset is not embedded."),
    source("black_shark_5_pro_global_release", "Black Shark (Global)", URL_GLOBAL_RELEASE,
           "Manufacturer global availability date and product-family launch context",
           "Black Shark's global press room states that the Black Shark 5 series became officially available June 9, 2022. The regional Chinese announcement/release date may differ; this field records the stated global availability date."),
    source("black_shark_5_pro_ntc_gec", "National Telecommunications Commission (NTC)", URL_NTC,
           "Philippine Grant of Equipment Conformity model identity",
           "The 2022 NTC GEC identifies BLACK SHARK SHARK KTUS-H0 as Black Shark 5 Pro. This is Philippine regulatory model-code evidence."),
    source("black_shark_5_pro_manual", "Black Shark 5 Pro user manual (manufacturer manual mirrored by Device.report)", URL_MANUAL,
           "Model-code confirmation, SIM size, fingerprint location, and physical port layout",
           "The manual names Black Shark 5 Pro, SHARK KTUS-H0, and BLACK SHARK. Its diagram identifies the side fingerprint lock, SIM tray, and USB Type-C port; the SIM instructions specify Nano-SIM slots 1 and 2. The PDF is hosted by a manual archive rather than the manufacturer domain."),
    source("black_shark_5_pro_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine launch, local configurations/prices, availability, and device specifications",
           "Published June 27, 2022. YugaTech reports Black Shark Philippines' July launch, July 2–18 early-bird offer, local 8/128 and 12/256 variants and SRPs, Snapdragon 8 Gen 1, display, camera system, battery, connectivity, and build dimensions." ,
           "2022-06-27"),
    source("black_shark_5_pro_revu_ph", "REVU Philippines", URL_REVU,
           "Independent contemporaneous Philippine sale date, official store channels, and launch prices",
           "Published June 26, 2022. REVU reports Black Shark's official Philippines Shopee store and SM City North EDSA pop-up, local sale beginning July 2, both Philippine Black Shark 5 Pro configurations and launch SRPs, plus the July 2–18 PHP 1,000 promotion.",
           "2022-06-26"),
    source("black_shark_5_pro_xiaomi_specs", "Xiaomi / Black Shark official specifications (China)", URL_XIAOMI_SPECS,
           "Manufacturer technical specifications for the Black Shark 5 Pro product family",
           "The official Xiaomi-hosted Black Shark 5 Pro specification page lists the Snapdragon 8 Gen 1/Adreno 730 platform, LPDDR5 and enhanced UFS 3.1 + SSD storage, display, HM2 main sensor, camera modules, battery/charging, dimensions, and SIM/network details. The page is the Chinese-market specification; local-only bands and availability are sourced separately."),
    source("qualcomm_snapdragon_8_gen_1_brief", "Qualcomm", URL_QUALCOMM,
           "Primary chipset platform process, CPU/GPU family, and USB platform capability reference",
           "Qualcomm's Snapdragon 8 Gen 1 brief reports 4 nm process technology, Kryo CPU with Cortex-X2 technology up to 3.0 GHz, and the Adreno graphics subsystem. It does not identify this handset's regional configuration."),
    source("black_shark_5_pro_gufi_range_candidate", "Gufi Philippines", URL_GUFI,
           "Unmapped Philippine retailer price-range candidate; not a dated exact-variant offer",
           "The indexed Black Shark category page shows a Black Shark 5 Pro price range PHP 41,199–44,199 and Add to cart, but the search index says it was crawled about four months earlier. It does not expose which price belongs to which RAM/storage variant or current stock for a selected option. It is retained only as a pending range candidate, not a current public variant price."),
    source("black_shark_5_pro_alt_specs_conflict", "Black Shark specification page at blackshark.gg", URL_ALT_SPECS,
           "Record alternate technical claims that conflict with local launch and Xiaomi manufacturer specifications",
           "The page lists 8 MP ultrawide, 20 MP front, Bluetooth 5.0, Wi-Fi details, and a 3.5 mm jack; the Philippine launch and Xiaomi-hosted specs report 13 MP ultrawide, 16 MP front, and local Bluetooth 5.2. This page's contradictory Black Shark 5 family entries include a Snapdragon 870/Adreno 660 pairing, so its conflicting claims are retained for audit and not silently selected."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, catalog_value="__normalized__", unit=None, note: str,
          configurationMatch=None,
          price_condition="__absent__", price_type=None, price_observed_at=None,
          listing_status=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized, "note": note}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value == "__normalized__" else catalog_value
    if unit:
        item["unit"] = unit
    if price_condition != "__absent__":
        item["priceCondition"] = price_condition
    if price_type is not None:
        item["priceType"] = price_type
    if price_observed_at is not None:
        item["priceObservedAt"] = price_observed_at
    if listing_status is not None:
        item["listingStatus"] = listing_status
    if configurationMatch is not None:
        item["configurationMatch"] = configurationMatch
    return item


def fields_for(config: dict) -> list[dict]:
    ram, storage = config["ram"], config["storage"]
    match = f"Philippine {ram} GB RAM / {storage} GB storage configuration"
    out = []

    def add(fid, sid, value, normalized, **kwargs):
        out.append(field(fid, sid, value, normalized, configurationMatch=match, **kwargs))

    add("model_number", "black_shark_5_pro_ntc_gec", "NTC GEC: BLACK SHARK SHARK KTUS-H0; the Black Shark 5 Pro manual names model SHARK KTUS-H0", "SHARK KTUS-H0", status="VERIFIED", note="The NTC 2022 GEC directly maps SHARK KTUS-H0 to Black Shark 5 Pro; the matching manufacturer manual independently confirms the model-code spelling.")
    add("global_release_date", "black_shark_5_pro_global_release", "Black Shark Global states the Black Shark 5 series was officially available June 9, 2022", "2022-06-09", status="VERIFIED", note="Manufacturer-stated global availability date. Philippine official sale was later, from July 2, 2022.")
    add("configuration", "black_shark_5_pro_yugatech_ph", f"{ram} GB RAM / {storage} GB storage Philippine launch variant", f"{ram} GB RAM / {storage} GB storage", status="VERIFIED_SECONDARY", note="This exact configuration appears in contemporaneous Philippine launch coverage. The 16/256 global version and Black Shark 5 (non-Pro) are not merged into this local SKU.")
    add("philippine_release_date", "black_shark_5_pro_revu_ph", "Official Black Shark Philippines sale begins July 2, 2022", "2022-07-02", status="VERIFIED_SECONDARY", note="Reported local sale start through the official Shopee Philippines store and brand pop-up booth; not a claim of the first individual completed sale.")
    add("official_launch_price_php", "black_shark_5_pro_yugatech_ph", f"PHP {config['srp']:,} Philippine launch SRP for {ram}/{storage} GB", config["srp"], status="VERIFIED_SECONDARY", unit="PHP", note="Historical Philippine SRP corroborated by REVU; July 2–18, 2022 early-bird price is separately recorded and neither figure is presented as current.")
    add("current_price_php", "black_shark_5_pro_gufi_range_candidate", "Indexed Gufi Philippines price range PHP 41,199–44,199; source crawl is about four months old and does not map range bounds to RAM/storage or confirm live stock", None, status="PENDING_VERIFICATION", unit="PHP", note="The retailer price range is preserved only as an unmapped candidate. No exact, current, in-stock offer was verified for this configuration; historical launch pricing is not reused as a current price.")
    add("display_size", "black_shark_5_pro_xiaomi_specs", "6.67-inch display (YugaTech rounds to 6.7 inches)", 6.67, key="displayInches", unit="in", note="Official Xiaomi specification gives 6.67 inches; local launch source uses the rounded 6.7-inch value.")
    add("display_technology", "black_shark_5_pro_xiaomi_specs", "Flexible OLED display", "Flexible OLED", key="displayType", note="Manufacturer specification names a flexible OLED panel; local launch coverage describes AMOLED.")
    add("display_resolution", "black_shark_5_pro_yugatech_ph", "FHD+ 2400 x 1080 pixels", "1080 x 2400", key="resolution", note="Local launch specification gives FHD+ at 2400 x 1080.")
    add("display_refresh_rate", "black_shark_5_pro_yugatech_ph", "144 Hz display refresh; 720 Hz touch sampling", 144, key="refreshHz", unit="Hz", note="144 Hz is the display refresh rate. The 720 Hz figure is touch sampling and is kept separate.")
    add("display_brightness", "black_shark_5_pro_yugatech_ph", "Peak brightness not stated in the cited Philippine launch source", None, status="NOT_DISCLOSED", note="No exact brightness value is asserted from the source set used for the PH configuration.")
    add("display_protection", "black_shark_5_pro_xiaomi_specs", "Panel protection material/grade is not identified in the reviewed manufacturer specification", None, status="NOT_DISCLOSED", note="No protective-glass brand or generation is inferred.")
    add("chipset", "black_shark_5_pro_yugatech_ph", "Qualcomm Snapdragon 8 Gen 1 5G", "Qualcomm Snapdragon 8 Gen 1 5G", key="chipset", note="Local launch coverage identifies the Pro chipset; the standard Black Shark 5 uses Snapdragon 870.")
    add("process_node", "qualcomm_snapdragon_8_gen_1_brief", "4 nm process technology", "4 nm", status="VERIFIED", note="Qualcomm's platform brief gives the Snapdragon 8 Gen 1 process node; this is a chipset property.")
    add("cpu", "qualcomm_snapdragon_8_gen_1_brief", "Kryo CPU with Arm Cortex-X2 technology up to 3.0 GHz; full handset core layout not recorded", "Kryo CPU; Cortex-X2 up to 3.0 GHz; core layout not recorded", key="cpu", status="VERIFIED", note="Recorded only to the level named by Qualcomm; the full core count/cluster layout is not inferred.")
    add("gpu", "black_shark_5_pro_yugatech_ph", "Adreno 730 GPU", "Adreno 730", key="gpu", note="Philippine launch coverage specifies Adreno 730 for the Snapdragon 8 Gen 1 Black Shark 5 Pro.")
    add("operating_system", "black_shark_5_pro_yugatech_ph", "Joy UI 13 based on Android 12", "Android 12; Joy UI 13", key="os", note="Launch software only; later upgrade state is not inferred.")
    add("os_support", "black_shark_5_pro_global_product", "No manufacturer OS/security update duration identified", None, status="NOT_DISCLOSED", note="No update-duration promise was identified in the reviewed manufacturer sources.")
    add("ram_capacity", "black_shark_5_pro_yugatech_ph", f"{ram} GB LPDDR5 configuration", ram, key="ramGb", unit="GB", note="Exact local variant capacity from Philippine launch coverage.")
    add("ram_type", "black_shark_5_pro_yugatech_ph", "LPDDR5, 6,400 MHz", "LPDDR5", note="Memory type and rated data rate from local launch specifications.")
    add("storage_capacity", "black_shark_5_pro_yugatech_ph", f"{storage} GB Philippine launch configuration", storage, key="storageGb", unit="GB", note="Exact local configuration capacity.")
    add("storage_type", "black_shark_5_pro_xiaomi_specs", "Enhanced UFS 3.1 + SSD storage array system 2.0", "UFS 3.1 + SSD storage array", note="Manufacturer identifies the storage technology. The capacity remains the exact local 128 GB or 256 GB SKU value.")
    add("storage_expansion", "black_shark_5_pro_manual", "Manual identifies two Nano-SIM positions; a microSD slot is not specified", None, status="PENDING_VERIFICATION", note="The reviewed local sources do not explicitly confirm microSD expansion support; absence is not inferred from the SIM tray drawing.")
    add("rear_camera_system", "black_shark_5_pro_alt_specs_conflict", "YugaTech and Xiaomi manufacturer specifications: 108 MP main + 13 MP ultrawide + 5 MP macro; blackshark.gg alternate page: 108 MP + 8 MP + 5 MP", None, status="CONFLICTING_INFORMATION", key="rearCameraMp", catalog_value=None, note="Main resolution and macro resolution agree, but ultrawide resolution conflicts. The catalog's primary-camera number remains blank while the source discrepancy is unresolved.")
    add("main_camera_sensor", "black_shark_5_pro_xiaomi_specs", "Samsung HM2 108 MP sensor, 1/1.52-inch format, f/1.75, 7P lens", "Samsung HM2, 108 MP, 1/1.52 in", note="Manufacturer specification names HM2; the value is limited to this exact product family.")
    add("ultrawide_camera", "black_shark_5_pro_alt_specs_conflict", "YugaTech/Xiaomi specs: 13 MP, 120-degree ultrawide; alternate page: 8 MP, 120-degree ultrawide", None, status="CONFLICTING_INFORMATION", note="The exact-model sources disagree on ultrawide resolution; neither is silently selected.")
    add("telephoto_camera", "black_shark_5_pro_xiaomi_specs", "No separate optical zoom telephoto module is specified; a 5 MP 3–7 cm autofocus macro camera is listed", "No separate optical zoom telephoto; 5 MP autofocus macro", status="VERIFIED", note="The manufacturer describes a close-focus macro lens. It is not presented as a long-range optical zoom camera.")
    add("front_camera", "black_shark_5_pro_alt_specs_conflict", "YugaTech/Xiaomi specs: 16 MP front camera; alternate page: 20 MP", None, status="CONFLICTING_INFORMATION", key="frontCameraMp", catalog_value=None, note="The published front-camera resolutions conflict; the catalog numeric value remains blank.")
    add("video_recording", "black_shark_5_pro_xiaomi_specs", "Rear: 4K/60 fps; 1080p/60 fps; 720p/30 fps; 1080p slow motion at 120/240/960 fps. Front: 1080p/30 fps", "Rear up to 4K/60 fps and 1080p/960 fps slow motion; front up to 1080p/30 fps", key="video", note="Manufacturer's video modes; individual features depend on camera mode and software settings.")
    add("battery_capacity", "black_shark_5_pro_yugatech_ph", "4,650 mAh battery", 4650, key="batteryMah", unit="mAh", note="Rated capacity from Philippine launch specifications.")
    add("battery_technology", "black_shark_5_pro_global_release", "Manufacturer describes a 4,650 mAh battery; cell chemistry is not stated in the primary source", "Dual-cell battery; chemistry not recorded", status="VERIFIED_SECONDARY", note="Dual-cell construction is described in manufacturer series material; lithium-ion chemistry is not inferred.")
    add("wired_charging", "black_shark_5_pro_yugatech_ph", "120 W wired charging", 120, key="chargingW", unit="W", note="Maximum wired charging rating in the Philippine launch source.")
    add("wireless_charging", "black_shark_5_pro_xiaomi_specs", "Wireless charging capability is not listed in the reviewed manufacturer specification", None, status="NOT_DISCLOSED", note="No wireless-charging support is claimed from the absence of a listing.")
    add("dimensions", "black_shark_5_pro_yugatech_ph", "163.86 x 76.53 x 9.5 mm", "163.86 x 76.53 x 9.5 mm", key="dimensions", unit="mm", note="Local launch and Xiaomi manufacturer specifications agree. The alternate page gives rounded measurement values and disclaims exact physical variation.")
    add("weight", "black_shark_5_pro_yugatech_ph", "220 g", 220, key="weightG", unit="g", note="Weight reported by the Philippine launch source and official product specification.")
    add("materials", "black_shark_5_pro_global_release", "Manufacturer describes a 3D curved glass back with nano-optical coating; frame material not recorded", "3D curved glass back; frame material not recorded", status="VERIFIED", note="Only the back material is recorded. The manufacturer press release does not identify frame material.")
    add("ingress_protection", "black_shark_5_pro_global_product", "No IP rating identified in reviewed manufacturer information", None, status="NOT_DISCLOSED", note="No water/dust rating is inferred.")
    add("sim_esim", "black_shark_5_pro_manual", "Two Nano-SIM positions; eSIM support not stated", "Dual Nano-SIM; eSIM not recorded", key="sim", status="VERIFIED", note="The model-specific manual states Nano-SIM in card slots 1 and 2. eSIM support is not inferred.")
    add("cellular_bands", "black_shark_5_pro_yugatech_ph", "5G and 4G LTE; exact band set for the Philippine SHARK KTUS-H0 SKU not established", "5G / 4G LTE; exact local bands not recorded", key="cellular", note="Local source confirms 5G/LTE. Technical band lists from other regional codes are not substituted for PH model KTUS-H0.")
    add("wifi", "black_shark_5_pro_alt_specs_conflict", "YugaTech/local launch source lists Wi-Fi 6; Black Shark global press material lists Wi-Fi 6E", None, status="CONFLICTING_INFORMATION", key="wifi", catalog_value=None, note="Wi-Fi 6 versus Wi-Fi 6E is a material generation/feature discrepancy; local configuration support is left unresolved.")
    add("bluetooth", "black_shark_5_pro_alt_specs_conflict", "YugaTech lists Bluetooth 5.2; blackshark.gg specification page lists Bluetooth 5.0", None, status="CONFLICTING_INFORMATION", note="Published Bluetooth versions conflict. The catalog does not choose between them pending exact-model clarification.")
    add("usb", "black_shark_5_pro_manual", "USB Type-C port shown in the model-specific manual; data protocol not stated", "USB Type-C; protocol not recorded", key="ports", note="Connector type only; USB generation and transfer rate are not inferred.")
    add("nfc", "black_shark_5_pro_yugatech_ph", "NFC listed", "Yes", note="Local launch specification lists NFC.")
    add("gnss", "black_shark_5_pro_yugatech_ph", "GPS, A-GPS, GLONASS, Galileo, BeiDou, and QZSS", "GPS, A-GPS, GLONASS, Galileo, BeiDou, QZSS", note="Navigation systems from Philippine launch specifications.")
    add("audio", "black_shark_5_pro_yugatech_ph", "Stereo speakers are specified; 3.5 mm headphone-jack availability is not established in PH sources", "Stereo speakers; 3.5 mm jack not recorded", key="sound", note="Local launch source confirms stereo speakers. A separate alternate page says 3.5 mm jack, but local/model-specific sources do not verify it; no jack status is asserted.")
    add("sensors", "black_shark_5_pro_manual", "Side power/fingerprint key shown in the manual; other sensor list not recorded for the PH configuration", "Side-mounted fingerprint reader; other sensors not recorded", status="VERIFIED", note="Model-specific manual diagram places fingerprint unlock on the side power key. Additional sensor types are not transferred from a different regional model-code listing.")

    if len(out) != 46:
        raise ValueError(f"Expected 46 reviewed phone fields, got {len(out)}")
    return out


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "black shark"
            or device.get("model") != "5 Pro"):
        raise ValueError("The inventory row no longer matches Black Shark 5 Pro")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Black Shark 5 Pro already has a manual review; inspect it before replacing")

    records = []
    for index, config in enumerate(CONFIGS):
        ram, storage = config["ram"], config["storage"]
        config_id = f"{DEVICE}-{ram}gb-{storage}gb-ph"
        label = f"{ram} GB RAM / {storage} GB storage"
        review = {
            "deviceId": DEVICE, "configurationId": config_id,
            "brand": "Black Shark", "model": "5 Pro",
            "configuration": label, "configurationLabel": label,
            "sources": SOURCES, "fields": fields_for(config),
        }
        if index == 0:
            review["replacementVariants"] = [{
                "id": f"{DEVICE}-{item['ram']}gb-{item['storage']}gb-ph",
                "label": f"{item['ram']} GB RAM / {item['storage']} GB storage",
                "sku": None, "modelCode": "SHARK KTUS-H0",
                "notes": "Exact Philippine Black Shark 5 Pro launch configuration reported by YugaTech and REVU. Separate from the standard Black Shark 5 and from global 16/256 variants.",
            } for item in CONFIGS]
            review["replaceUnrecordedPlaceholder"] = True
            review["availabilityEvidence"] = {
                "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                "availabilityStatus": "Philippine official sale reported from July 2, 2022 through Black Shark's official Shopee Philippines store and pop-up booth; NTC GEC identifies SHARK KTUS-H0 as Black Shark 5 Pro.",
                "philippineAvailability": "Contemporaneous Philippine reports identify the 8/128 and 12/256 Black Shark 5 Pro variants in the brand's official local sales channels. NTC's 2022 GEC records the exact PH model code. The workbook scope status remains Pending.",
                "observedAt": OBSERVED,
                "manufacturer": "Black Shark",
                "productLine": "Black Shark 5 Series",
                "modelNumber": "SHARK KTUS-H0",
                "philippineReleaseYear": 2022,
                "philippineDateLabel": "Reported Philippine official sale date",
                "researchNotes": "Matched to Black Shark 5 Pro / SHARK KTUS-H0, not the standard Black Shark 5. The NTC GEC names the marketing model and code; the manufacturer manual confirms the same code. Global manufacturer release is June 9, 2022; Philippine official sale was reported from July 2. Local launch variants are 8/128 at PHP 37,999 and 12/256 at PHP 43,999; early-bird prices were PHP 36,999 and PHP 42,999 from July 2–18, 2022. Gufi's indexed listing shows a PHP 41,199–44,199 range, but the index is about four months old and does not map the two bounds to exact variants or verify present stock, so public current prices remain blank. The alternate blackshark.gg spec page conflicts with local and Xiaomi technical sources on camera and radio values; disputed public fields stay blank. An exact official product image was located, but image reuse rights are undocumented, so the placeholder remains. The workbook scope label remains Pending.",
                "qualityFlag": "Current price range not mapped to variants; camera, Wi-Fi, and Bluetooth source conflicts; image reuse rights not established; scope remains Pending",
                "openIssues": [
                    {"issue": "Gufi lists only an indexed PHP 41,199–44,199 range; no exact variant mapping or current stock confirmation", "action": "Keep public current prices blank until a dated selected-variant offer is verified."},
                    {"issue": "Rear camera/ultrawide and front-camera values conflict with an alternate Black Shark specifications page", "action": "Preserve source claims in the audit and leave the disputed numeric catalog fields blank."},
                    {"issue": "Wi-Fi 6 versus Wi-Fi 6E and Bluetooth 5.2 versus 5.0 conflict", "action": "Keep these connectivity values unresolved for the Philippine KTUS-H0 configuration."},
                    {"issue": "Exact official product image reuse permission is not recorded", "action": "Keep the neutral placeholder until usage rights are documented."},
                    {"issue": "Workbook eligibility remains Pending", "action": "Do not change study eligibility based only on verified Philippine availability."},
                ],
            }
        records.append(review)

    manual["records"].extend(records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact Black Shark 5 Pro Stellar Black product image is available from the official product page, but no reusable image license or written permission is recorded.",
        "sourcePage": URL_OFFICIAL, "assetUrl": URL_IMAGE,
        "scope": "Exact Black Shark 5 Pro, Stellar Black finish; image does not establish a RAM/storage configuration",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Black Shark 5 Pro",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for config in CONFIGS:
        variant_id = f"{DEVICE}-{config['ram']}gb-{config['storage']}gb-ph"
        label = f"Philippine {config['ram']} GB / {config['storage']} GB configuration"
        prices.extend([
            {"device_id": DEVICE, "amount_php": config["srp"], "configuration_id": variant_id,
             "configuration_match": "exact", "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
             "price_type": "historical_ph_launch_srp", "source_published_at": "2022-06-27",
             "excerpt": f"YugaTech reported PHP {config['srp']:,} Philippine launch SRP for {label}; not a current offer.",
             "source_url": URL_YUGA, "source_kind": "historical_ph_launch_price_report", "observed_at": OBSERVED_AT,
             "local_availability_verified": True, "availability_status": "historical_ph_launch_srp_not_current"},
            {"device_id": DEVICE, "amount_php": config["promo"], "configuration_id": variant_id,
             "configuration_match": "exact", "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
             "price_type": "historical_ph_early_bird_promotion", "source_published_at": "2022-06-27",
             "excerpt": f"YugaTech reported PHP {config['promo']:,} early-bird price for {label}, offered July 2–18, 2022; not a current offer.",
             "source_url": URL_YUGA, "source_kind": "dated_ph_launch_promotion", "observed_at": OBSERVED_AT,
             "local_availability_verified": True, "availability_status": "dated_ph_promotion_not_current"},
        ])
    prices.append({
        "device_id": DEVICE, "amount_php": 41199, "range_max_php": 44199,
        "configuration_id": None, "configuration_match": "ambiguous_variant_range",
        "variant_ram_gb": None, "variant_storage_gb": None,
        "price_type": "undated_indexed_ph_retailer_range_candidate",
        "source_published_at": None,
        "excerpt": "Gufi's indexed Black Shark category page showed PHP 41,199–44,199 and Add to cart, but was crawled about four months earlier and did not map range bounds to RAM/storage or confirm current stock; not a current exact-variant offer.",
        "source_url": URL_GUFI, "source_kind": "unmapped_retailer_range_candidate",
        "observed_at": None, "local_availability_verified": False,
        "availability_status": "pending_variant_mapping_and_current_stock",
    })
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Black Shark", "model_name": "5 Pro", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [], "discovery": [], "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Black Shark 5 Pro / SHARK KTUS-H0",
        "configurations": [f"{c['ram']}/{c['storage']}" for c in CONFIGS],
        "reviewedFields": sum(len(r["fields"]) for r in records),
        "globalAvailability": "2022-06-09",
        "philippineSale": "reported from 2022-07-02",
        "launchSrpsPhp": [c["srp"] for c in CONFIGS],
        "currentPrice": "not assigned; indexed retailer range remains unmapped and undated",
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
