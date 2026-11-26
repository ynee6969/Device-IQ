#!/usr/bin/env python3
"""Review Nokia G42 5G Philippine configurations against exact-model sources."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/nokia-g42-5g-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_9ba373722ace11"
CONFIG_4_128 = f"{DEVICE}-ph-4gb-128gb"
CONFIG_6_128 = f"{DEVICE}-ph-crossborder-6gb-128gb"

URL_HMD_SPECS = "https://www.hmd.com/en_int/nokia-g-42/specs"
URL_HMD_PRODUCT = "https://www.hmd.com/en_int/nokia-g-42"
URL_HMD_GUIDE = "https://www.hmd.com/en_int/support/nokia-g42-5g-user-guide/keys-and-parts"
URL_HMD_LAUNCH = "https://www.hmd.com/en_au/blog/the-story-behind-nokia-g-42-5g"
URL_YUGATECH_PH = "https://www.yugatech.com/mobile/nokia-g42-5g-specs-price-philippines/"
URL_YUGATECH_SEP = "https://specs.yugatech.com/news/smartphones-launched-in-the-philippines-september-2023/"
URL_YUGATECH_PRICES = "https://www.yugatech.com/nokia-phone-price-list-philippines"
URL_NOYPI = "https://www.noypigeeks.com/android/nokia-g42-philippines/"
URL_GIZGUIDE = "https://www.gizguide.com/2023/12/nokia-g42-5g-sale-ph.html"
URL_GSMARENA = "https://www.gsmarena.com/nokia_g42_5g_announced_with_snapdragon_480_and_50mp_main_cam-news-58995.php"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/nokia-g42"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-nokia-g42"
URL_PINOYTECHNOGUIDE = "https://www.pinoytechnoguide.com/"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("nokia_g42_hmd_specs", "HMD Global (manufacturer)", URL_HMD_SPECS,
        "Exact-model specifications and official product imagery",
        "HMD publishes Nokia G42 5G display, cameras, connectivity, battery, storage options, CPU/GPU, OS, supported update policy, build, ingress rating, audio, and sensors. This international model page does not identify the Philippine Shopee unit's regional model code or current local availability."),
    src("nokia_g42_hmd_product", "HMD Global (manufacturer)", URL_HMD_PRODUCT,
        "Manufacturer product identity and exact-model image page",
        "HMD's product page identifies the Nokia G42 5G and displays exact-model imagery. No reusable image license or permission was located."),
    src("nokia_g42_hmd_guide", "HMD Global (manufacturer)", URL_HMD_GUIDE,
        "Model-code family cross-check",
        "HMD states that this Nokia G42 5G user guide applies to TA-1581 and TA-1591. The Philippine cross-border listing does not state which code it ships; neither code is assigned to the local configurations."),
    src("nokia_g42_hmd_launch", "HMD Global (manufacturer)", URL_HMD_LAUNCH,
        "Global announcement date and product identity",
        "HMD's dated Nokia G42 story is published 28 June 2023 and describes the model launch. This is the global announcement date, not a Philippine sale date.", "2023-06-28"),
    src("nokia_g42_yugatech_ph", "YugaTech Philippines", URL_YUGATECH_PH,
        "Philippine 6/128 listing, cross-border price, local specification cross-check",
        "Published 13 September 2023. Reports the Nokia G42 5G had landed in the Philippines and lists 4 GB and 6 GB RAM options with 128 GB storage. The priced 6 GB / 128 GB option was PHP 11,242 through Nokia's cross-border Shopee store; it was not called a standard SRP. The page lists a separate promotional voucher, which is not treated as a completed transaction or a lower observed device price.", "2023-09-13"),
    src("nokia_g42_yugatech_launch_roundup", "YugaSpecs / YugaTech Philippines", URL_YUGATECH_SEP,
        "Philippine announcement-date corroboration",
        "The September 2023 local launch roundup dates the Nokia G42 5G Philippine launch to 13 September 2023. It does not identify an exact first transaction timestamp or a local regional model code.", "2023-09-13"),
    src("nokia_g42_noypigeeks_ph", "NoypiGeeks Philippines", URL_NOYPI,
        "Local launch, authorized cross-border shop, and 6/128 configuration evidence",
        "Published 14 September 2023. Reports a Nokia Mobile Facebook announcement that the 6 GB / 128 GB G42 was offered through the Nokia Official Flagship Store cross-border Shopee shop, shipping from mainland China, at PHP 11,242 with an extra voucher. This supports historical official-store Philippine orderability, not domestic warehouse origin, present stock, or a regional TA code.", "2023-09-14"),
    src("nokia_g42_gizguide_ph", "GizGuide Philippines", URL_GIZGUIDE,
        "Exact 4/128 Philippine configuration, historical SRP and promotion, hardware cross-check",
        "Published 25 December 2023. Identifies the Philippine 4 GB / 128 GB configuration, states an original SRP of PHP 11,990 and a Christmas promotional price of PHP 8,990, and provides local specifications. The article is treated as evidence of availability by its publication date, not the configuration's first-sale date.", "2023-12-25"),
    src("nokia_g42_gsmarena", "GSMArena", URL_GSMARENA,
        "Exact global model, launch timing, memory options, and hardware cross-check",
        "The exact Nokia G42 5G launch article reports 4/128 and 6/128 GB options, 28 June 2023 announcement, Snapdragon 480+, Android 13, 5,000 mAh battery, camera configuration, and display. Global configuration details are not treated as proof of Philippine sale." , "2023-06-28"),
    src("nokia_g42_nanoreview", "NanoReview", URL_NANOREVIEW,
        "Secondary technical cross-check for memory, processor, storage, and imaging fields",
        "Exact Nokia G42 profile reports LPDDR4X RAM, UFS 2.2 storage, 8 nm Snapdragon 480 Plus, CPU core arrangement, and camera/video capabilities. It warns that some specifications can differ by region; local availability and regional code are sourced separately."),
    src("nokia_g42_kimovil", "Kimovil", URL_KIMOVIL,
        "Global configuration and regional-variation cross-check",
        "Exact Nokia G42 profile lists distinct global 4/128 and 6/128 GB configurations and warns that country/region bands differ. It is not used as evidence of Philippine availability or price."),
    src("nokia_g42_yugatech_price_list", "YugaTech Philippines", URL_YUGATECH_PRICES,
        "Dated local price-history cross-check",
        "The price-list entry records a verified PHP 11,290 report dated 5 November 2023. Its age means this is historical evidence only and is not presented as a current price.", "2023-11-05"),
]

S = {item["id"]: item["id"] for item in SOURCES}


def f(fid: str, sid: str, value, normalized=None, *, key: str | None = None,
      unit: str | None = None, status: str = "VERIFIED", note: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    return row


def fields(config: str) -> list[dict]:
    is_6gb = config == "6/128"
    config_label = "6 GB RAM / 128 GB storage" if is_6gb else "4 GB RAM / 128 GB storage"
    local_source = S["nokia_g42_yugatech_ph"] if is_6gb else S["nokia_g42_gizguide_ph"]
    ram = 6 if is_6gb else 4
    rows = [
        f("model_number", S["nokia_g42_hmd_guide"],
          "HMD guide applies to TA-1581 and TA-1591; the Philippine listing does not identify which regional code applies.", None,
          status="PENDING_VERIFICATION",
          note="Do not assign either HMD guide code to a Philippine RAM/storage configuration without a local unit label, NTC record, or exact seller SKU."),
        f("global_release_date", S["nokia_g42_hmd_launch"], "HMD's global Nokia G42 5G launch story is dated 28 June 2023", "2023-06-28",
          note="Global announcement date; it does not establish Philippine availability."),
        f("configuration", local_source, config_label, config_label, status="VERIFIED_SECONDARY",
          note="Separate Philippine configurations are retained; the 4 GB and 6 GB records are not merged."),
        f("philippine_release_date", local_source,
          "Reported Philippine availability by 13 September 2023 through Nokia's cross-border Shopee store" if is_6gb else
          "GizGuide reports the 4 GB / 128 GB Philippine version on sale on 25 December 2023; its first-sale date is not stated",
          "2023-09-13" if is_6gb else None, status="VERIFIED_SECONDARY",
          note="The 6/128 date is the dated local launch/availability report, not an exact transaction timestamp. For 4/128, the first local-sale date is unknown; the dated sale report establishes availability by 25 December 2023."),
        f("official_launch_price_php", S["nokia_g42_gizguide_ph"] if not is_6gb else S["nokia_g42_yugatech_ph"],
          "GizGuide reports PHP 11,990 as the original SRP for the Philippine 4 GB / 128 GB version" if not is_6gb else
          "YugaTech reports PHP 11,242 through Nokia's cross-border Shopee store, but does not identify it as a standard SRP",
          11990 if not is_6gb else None, unit="PHP",
          status="VERIFIED_SECONDARY" if not is_6gb else "NOT_DISCLOSED",
          note="The 4/128 amount is a dated secondary-source report of the original SRP. For 6/128, the reported store listing price is preserved as a historical price observation; no separate standard SRP was verified."),
        f("current_price_php", S["nokia_g42_yugatech_price_list"],
          "The latest exact Nokia G42 price-list entry located is dated 5 November 2023; no current orderable Philippine offer was verified on 26 November 2026.", None,
          status="PENDING_VERIFICATION", unit="PHP",
          note="Current Philippine price remains blank. Do not reuse a 2023 listing as a 2026 offer."),
        f("display_size", S["nokia_g42_hmd_specs"], "6.56 inches", 6.56, key="displayInches", unit="in"),
        f("display_technology", S["nokia_g42_gizguide_ph"], "6.56-inch IPS LCD", "IPS LCD", key="displayType", status="VERIFIED_SECONDARY"),
        f("display_resolution", S["nokia_g42_hmd_specs"], "HD+ 720 x 1612 pixels", "720 x 1612", key="resolution"),
        f("display_refresh_rate", S["nokia_g42_hmd_specs"], "90 Hz", 90, key="refreshHz", unit="Hz"),
        f("display_brightness", S["nokia_g42_hmd_specs"], "450 nits typical; 400 nits minimum; up to 560 nits with brightness boost", "450 typical; 560 boost; 400 minimum", unit="nits"),
        f("display_protection", S["nokia_g42_hmd_specs"], "Corning Gorilla Glass 3", "Corning Gorilla Glass 3"),
        f("chipset", S["nokia_g42_hmd_specs"], "Qualcomm Snapdragon 480+ 5G", "Qualcomm Snapdragon 480+ 5G", key="chipset"),
        f("process_node", S["nokia_g42_nanoreview"], "8 nm process reported for Snapdragon 480 Plus", 8, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", S["nokia_g42_nanoreview"], "Octa-core: 2 x Kryo 460 Gold (Cortex-A76) up to 2.2 GHz + 6 x Kryo 460 Silver (Cortex-A55) up to 1.8 GHz", "2x Kryo 460 Gold / Cortex-A76 up to 2.2 GHz + 6x Kryo 460 Silver / Cortex-A55 up to 1.8 GHz", status="VERIFIED_SECONDARY"),
        f("gpu", S["nokia_g42_hmd_specs"], "Qualcomm Adreno 619", "Adreno 619", key="gpu"),
        f("operating_system", S["nokia_g42_hmd_specs"], "Android 13 at launch", "Android 13", key="os"),
        f("os_support", S["nokia_g42_hmd_specs"], "Two OS upgrades; three years of monthly/quarterly security updates", "2 OS upgrades; 3 years security updates"),
        f("ram_capacity", local_source, f"{ram} GB physical RAM", ram, key="ramGb", unit="GB",
          status="VERIFIED_SECONDARY",
          note="Only physical RAM is counted. HMD's 2 GB / 5 GB virtual RAM options are not added to installed RAM."),
        f("ram_type", S["nokia_g42_nanoreview"], "LPDDR4X", "LPDDR4X", status="VERIFIED_SECONDARY"),
        f("storage_capacity", local_source, "128 GB internal storage", 128, key="storageGb", unit="GB", status="VERIFIED_SECONDARY"),
        f("storage_type", S["nokia_g42_nanoreview"], "UFS 2.2", "UFS 2.2", status="VERIFIED_SECONDARY",
          note="HMD confirms 128 GB capacity but does not state the interface; UFS 2.2 is a secondary exact-model specification."),
        f("storage_expansion", S["nokia_g42_hmd_specs"], "microSD support up to 1 TB", "microSD up to 1 TB"),
        f("rear_camera_system", S["nokia_g42_hmd_specs"], "50 MP autofocus main (5P, f/1.8) + 2 MP depth + 2 MP macro; LED flash", "50 MP AF main f/1.8 + 2 MP depth + 2 MP macro; LED flash"),
        f("main_camera_sensor", S["nokia_g42_hmd_specs"], "50 MP main autofocus, 5-element lens, f/1.8; sensor part number not stated", "50 MP AF, 5-element lens, f/1.8; sensor model not recorded"),
        f("ultrawide_camera", S["nokia_g42_hmd_specs"], "HMD specifies three rear modules (main, depth, macro) and no ultrawide module", "No ultrawide module listed", status="NOT_APPLICABLE"),
        f("telephoto_camera", S["nokia_g42_hmd_specs"], "HMD specifies three rear modules (main, depth, macro) and no telephoto module", "No telephoto module listed", status="NOT_APPLICABLE"),
        f("front_camera", S["nokia_g42_noypigeeks_ph"], "8 MP front camera", 8, key="frontCameraMp", unit="MP", status="VERIFIED_SECONDARY"),
        f("video_recording", S["nokia_g42_nanoreview"], "Rear video up to 1080p at 60 fps; front video up to 1080p at 30 fps", "Rear: 1080p up to 60 fps; front: 1080p up to 30 fps", status="VERIFIED_SECONDARY"),
        f("battery_capacity", S["nokia_g42_hmd_specs"], "5000 mAh", 5000, key="batteryMah", unit="mAh"),
        f("battery_technology", S["nokia_g42_hmd_specs"], "HMD documents a QuickFix replaceable battery; battery chemistry is not stated", "QuickFix replaceable; chemistry not recorded", status="VERIFIED",
          note="Replaceability is documented; no Li-ion/Li-polymer chemistry is inferred."),
        f("wired_charging", S["nokia_g42_hmd_specs"], "20 W wired fast charging (QC 3.0 / PD 3.0 support)", 20, key="chargingW", unit="W"),
        f("wireless_charging", S["nokia_g42_hmd_specs"], "Wireless charging is not specified on the reviewed HMD product specifications", None, status="NOT_DISCLOSED"),
        f("dimensions", S["nokia_g42_hmd_specs"], "165 x 75.8 x 8.55 mm", "165 x 75.8 x 8.55 mm", key="dimensions", unit="mm"),
        f("weight", S["nokia_g42_hmd_specs"], "193.8 g", 193.8, key="weightG", unit="g"),
        f("materials", S["nokia_g42_hmd_specs"], "Plastic frame; back cover is 65% recycled plastic; Gorilla Glass 3 front", "Plastic frame; 65% recycled-plastic back; Gorilla Glass 3 front"),
        f("ingress_protection", S["nokia_g42_hmd_specs"], "IP52", "IP52"),
        f("sim_esim", S["nokia_g42_noypigeeks_ph"], "Local launch report says dual SIM / dual standby; HMD user guide lists nano-SIM; eSIM applicability not stated", "Dual nano-SIM reported; eSIM not recorded", status="VERIFIED_SECONDARY",
          note="Local dual-SIM listing is retained. The exact tray/microSD arrangement and eSIM support of the shipped regional code remain unverified."),
        f("cellular_bands", local_source, "Philippine coverage reports 4G LTE and 5G; exact regional band set for the shipped local unit is not identified", "4G LTE and 5G; local band set not recorded", key="cellular", status="VERIFIED_SECONDARY",
          note="HMD publishes international band lists, but the Philippine cross-border listing's TA code is unresolved; global band lists are not projected onto this local configuration."),
        f("wifi", S["nokia_g42_hmd_specs"], "802.11 a/b/g/n/ac/ax-ready", "Wi-Fi 6 ready (802.11 a/b/g/n/ac/ax)", key="wifi"),
        f("bluetooth", S["nokia_g42_hmd_specs"], "Bluetooth 5.1", "Bluetooth 5.1"),
        f("usb", S["nokia_g42_hmd_specs"], "USB Type-C, USB 2.0, OTG", "USB Type-C; USB 2.0; OTG", key="ports"),
        f("nfc", S["nokia_g42_hmd_specs"], "NFC", "Yes"),
        f("gnss", S["nokia_g42_hmd_specs"], "GPS / A-GPS, GLONASS, BDS, Galileo", "GPS; A-GPS; GLONASS; BDS; Galileo", key="gnss"),
        f("audio", S["nokia_g42_hmd_specs"], "One loudspeaker, 3.5 mm headphone jack, OZO Playback; FM radio requires headset", "Mono speaker; 3.5 mm jack; OZO Playback; FM radio with headset", key="sound"),
        f("sensors", S["nokia_g42_hmd_specs"], "HMD lists accelerometer, ambient-light sensor, e-compass, and proximity sensor; GizGuide additionally lists a gyroscope", None,
          status="CONFLICTING_INFORMATION",
          note="HMD's detailed official sensor list omits a gyroscope, while GizGuide reports one. The omission is not treated as proof of absence; keep the sensor list unresolved until an exact regional manual or hardware report settles it."),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field assessments, got {len(rows)}")
    valid_sources = {item["id"] for item in SOURCES}
    missing = sorted({row["sourceId"] for row in rows} - valid_sources)
    if missing:
        raise ValueError(f"Fields refer to missing sources: {missing}")
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Historical Philippine availability is reported for the 6 GB / 128 GB version through Nokia's cross-border Official Flagship Store on Shopee; a Philippine 4 GB / 128 GB sale was reported by December 2023. Current Philippine stock and price are unverified.",
        "philippineAvailability": "NoypiGeeks reports Nokia Mobile identified its Shopee cross-border shop as the Nokia Official Flagship Store and listed the 6 GB / 128 GB Nokia G42 5G for Philippine buyers in September 2023, shipping from mainland China. GizGuide later reports a Philippine 4 GB / 128 GB version on sale by 25 December 2023. These sources support historical local orderability; they do not establish a domestic stock location, exact local first transaction, current availability, or the shipped unit's TA model code.",
        "observedAt": OBSERVED,
        "manufacturer": "HMD Global Oy (Nokia brand licensee)",
        "catalogModel": "G42 5G",
        "productLine": "Nokia G-series smartphones",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Reported Philippine orderability by 13 September 2023 (6 GB / 128 GB cross-border listing)",
        "researchNotes": "Workbook row 149 Nokia G42 5G matches HMD's exact G42 product family. HMD globally covers TA-1581 and TA-1591, but reviewed local seller coverage does not state which code was shipped. Separate Philippine 4 GB / 128 GB and 6 GB / 128 GB configurations are retained. The 6/128 version was listed through Nokia's cross-border official Shopee shop by 13 September 2023; the 4/128 version was reported on sale by 25 December 2023. Current Philippine price is not verified. The record's study scope remains Pending.",
        "qualityFlag": "Exact Nokia G42 5G product family and two Philippine RAM/storage configurations matched; local regional model code remains unconfirmed; dated local prices only; current price unverified; image reuse rights not established; sensor list conflict retained; study scope remains Pending.",
        "openIssues": [
            {"issue": "The cross-border listing does not identify whether its unit is TA-1581 or TA-1591", "action": "Keep the Philippine model number blank until the seller SKU, box label, or local regulatory record confirms it."},
            {"issue": "Exact first-sale date for the 4 GB / 128 GB Philippine variant is not established", "action": "Retain the 25 December 2023 dated sale report as evidence available by that date, not as a launch date."},
            {"issue": "No current orderable Philippine price was verified", "action": "Keep current price blank; preserve 2023 price observations as historical only."},
            {"issue": "HMD and local product pages show exact-model images but no reusable license or permission was found", "action": "Keep the neutral image placeholder and preserve image source provenance."},
            {"issue": "HMD's sensor list omits a gyroscope while GizGuide lists one", "action": "Keep the sensor field unresolved rather than presenting either list as complete."},
            {"issue": "Workbook eligibility remains Pending", "action": "Preserve the supplied study-scope status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 149
            or device.get("category") != "smartphones"
            or device.get("brand") != "Nokia"
            or device.get("model") != "G42 5G"):
        raise ValueError("Workbook row 149 guard failed; expected Nokia G42 5G smartphone")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Nokia G42 already has manual-review rows; refusing duplicate replacement")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise ValueError("Expected the original unrecorded-configuration placeholder before review")

    variants = [
        {"id": CONFIG_4_128, "label": "4 GB RAM / 128 GB storage (Philippine configuration; reported on sale by 25 December 2023)",
         "modelCode": None, "sku": None,
         "notes": "GizGuide reports a Philippine 4/128 GB version and dated 2023 Christmas promotion. Exact local model code and first-sale date are unknown; current price is not verified."},
        {"id": CONFIG_6_128, "label": "6 GB RAM / 128 GB storage (Philippine cross-border Shopee configuration)",
         "modelCode": None, "sku": None,
         "notes": "NoypiGeeks and YugaTech report a Nokia Official Flagship Store cross-border listing for Philippine buyers in September 2023. HMD TA model code and present-day price are not verified."},
    ]
    targets = {(DEVICE, CONFIG_4_128), (DEVICE, CONFIG_6_128)}
    for index, (config_id, config, variant) in enumerate((
        (CONFIG_4_128, "4/128", variants[0]),
        (CONFIG_6_128, "6/128", variants[1]),
    )):
        item = {
            "deviceId": DEVICE, "configurationId": config_id, "brand": "Nokia", "model": "G42 5G",
            "configuration": variant["label"], "modelCode": None, "sku": None,
            "sources": SOURCES, "fields": fields(config),
            "availabilityEvidence": availability_evidence(),
        }
        if index == 0:
            item["replacementVariants"] = variants
            item["replaceUnrecordedPlaceholder"] = True
        add_review(manual, catalog, item)
        if index == 0:
            device["variants"] = [{"id": row["id"], "label": row["label"], "modelCode": None,
                                   "sku": None, "specs": {}, "specSources": {},
                                   "pricePhp": None, "priceCondition": None, "priceType": None,
                                   "priceObservedAt": None, "priceSourceUrl": None, "notes": row["notes"],
                                   "workbookRow": 149} for row in variants]

    deduplicate_target_reviews(manual, targets)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "The HMD product page shows an exact-model Nokia G42 5G image, but no reusable license or permission to copy or hotlink was found. Keep the neutral placeholder.",
        "sourcePage": URL_HMD_PRODUCT, "assetUrl": None,
        "scope": "Nokia G42 5G; Philippine 4/128 GB and 6/128 GB configurations",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Nokia G42 5G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 11990, "configuration_id": CONFIG_4_128,
         "configuration_match": "exact_philippine_4gb_128gb_configuration", "variant_ram_gb": 4,
         "variant_storage_gb": 128, "price_type": "historical_ph_reported_srp",
         "source_published_at": "2023-12-25",
         "excerpt": "GizGuide reported an original PHP 11,990 SRP for the Philippine Nokia G42 5G 4 GB / 128 GB configuration on 25 December 2023; this is historical, not a current offer.",
         "source_url": URL_GIZGUIDE, "source_kind": "historical_local_reported_srp",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_price_not_current"},
        {"device_id": DEVICE, "amount_php": 8990, "configuration_id": CONFIG_4_128,
         "configuration_match": "exact_philippine_4gb_128gb_configuration", "variant_ram_gb": 4,
         "variant_storage_gb": 128, "price_type": "historical_ph_christmas_promotion",
         "source_published_at": "2023-12-25",
         "excerpt": "GizGuide reported PHP 8,990 as a Christmas Shopee promotional offer, reduced from the reported PHP 11,990 SRP; historical promotion, not a current offer.",
         "source_url": URL_GIZGUIDE, "source_kind": "dated_local_price_promotion",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_promotion_not_current"},
        {"device_id": DEVICE, "amount_php": 11242, "configuration_id": CONFIG_6_128,
         "configuration_match": "exact_philippine_crossborder_6gb_128gb_listing", "variant_ram_gb": 6,
         "variant_storage_gb": 128, "price_type": "historical_ph_crossborder_store_listing",
         "source_published_at": "2023-09-13",
         "excerpt": "YugaTech reported PHP 11,242 for the 6 GB / 128 GB model via Nokia's cross-border Shopee store; a separate extra voucher was advertised. The listing price is not a verified completed transaction or current offer.",
         "source_url": URL_YUGATECH_PH, "source_kind": "historical_local_store_listing",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_price_not_current"},
        {"device_id": DEVICE, "amount_php": 11290, "configuration_id": None,
         "configuration_match": "Nokia_G42_5G_RAM_configuration_unspecified_in_price_list", "variant_ram_gb": None,
         "variant_storage_gb": None, "price_type": "historical_ph_verified_price_list",
         "source_published_at": "2023-11-05",
         "excerpt": "YugaTech's local price list reports PHP 11,290 dated 5 November 2023, but does not identify this price-list entry's RAM/storage configuration. Kept as a model-level historical observation, not assigned as the 6/128 SKU's current price.",
         "source_url": URL_YUGATECH_PRICES, "source_kind": "historical_local_price_list",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_price_configuration_unspecified"},
    ]
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Nokia", "model_name": "G42 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_HMD_SPECS, "result": "HMD exact-model specifications checked against display, platform, memory, camera, battery, connectivity, build, and sensors."},
            {"device_id": DEVICE, "source_url": URL_HMD_GUIDE, "result": "HMD guide names TA-1581 and TA-1591 but does not map either code to the Philippine cross-border seller unit."},
            {"device_id": DEVICE, "source_url": URL_NOYPI, "result": "NoypiGeeks reports Nokia Mobile's cross-border Nokia Official Flagship Store Shopee listing for the 6/128 variant and PHP 11,242."},
            {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "GizGuide reports Philippine 4/128 configuration, PHP 11,990 original SRP, and a PHP 8,990 Christmas promotion as of 25 December 2023."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "GSMArena corroborates exact G42 model and global 4/128 and 6/128 configurations; global configuration alone is not local-market evidence."},
            {"device_id": DEVICE, "source_url": URL_NANOREVIEW, "result": "NanoReview technical profile checked for memory/storage interfaces, chipset process, CPU, and video modes; region-specific claims were not substituted for local evidence."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Kimovil exact-model page corroborates distinct global 4/128 and 6/128 configurations; no Philippine listing was inferred from its global prices."},
            {"device_id": DEVICE, "source_url": URL_PINOYTECHNOGUIDE, "result": "An exact Nokia G42 page was not found in the Pinoy Techno Guide search; no generic or similar-model page was substituted."},
        ],
        "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "workbookRow": 149, "device": "Nokia G42 5G", "variants": ["4 GB / 128 GB", "6 GB / 128 GB"],
        "reviewedFieldsPerVariant": 46, "sources": len(SOURCES),
        "availability": "Historically reported on sale in the Philippines; exact TA code unresolved",
        "historicalPricesPhp": {"4/128 SRP": 11990, "4/128 promotion": 8990, "6/128 listing": 11242},
        "currentPrice": None, "imageRights": "not established; neutral placeholder retained", "scopeStatus": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
