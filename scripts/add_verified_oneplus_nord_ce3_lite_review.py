#!/usr/bin/env python3
"""Review the Philippine OnePlus Nord CE 3 Lite 5G configuration."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/oneplus-nord-ce-3-lite-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_2077faec2ddf17"
CONFIG = f"{DEVICE}-ph-8gb-256gb"

URL_ONEPLUS_SPECS = "https://www.oneplus.com/ph/nord-ce-3-lite-5g/specs"
URL_ONEPLUS_PRODUCT = "https://www.oneplus.com/ph/nord-ce-3-lite-5g"
URL_ONEPLUS_LAUNCH = "https://www.youtube.com/watch?v=MFqJFbYi6EM"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/oneplus-nord-ce-3-lite-5g"
URL_REVU = "https://www.revu.com.ph/2023/04/oneplus-nord-ce-3-lite-buds-2-price-ph/"
URL_GIZGUIDE = "https://www.gizguide.com/2023/04/oneplus-nord-ce-3-lite-5g-price-specs-philippines-official.html"
URL_GSMARENA = "https://www.gsmarena.com/oneplus_nord_ce_3_lite_hands_on-review-2550.php"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/oneplus-nord-ce-3-lite"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-oneplus-nord-ce-3-lite-5g-8gb-256gb"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("oneplus_nordce3lite_ph_specs", "OnePlus Philippines (manufacturer)", URL_ONEPLUS_SPECS,
        "Official Philippine-region specifications for the exact Nord CE 3 Lite 5G product",
        "The Philippines-specific OnePlus page lists the 8 GB / 256 GB SKU and its hardware, network bands, OS/update policy, camera modules, battery, charging, connectivity and sensors. It does not expose a CPH model code for the Philippine retail unit."),
    src("oneplus_nordce3lite_ph_product", "OnePlus Philippines (manufacturer)", URL_ONEPLUS_PRODUCT,
        "Official product identity, colors and exact-model image source page",
        "The Philippines-specific product page identifies OnePlus Nord CE 3 Lite 5G and shows Pastel Lime and Chromatic Gray imagery. Reuse permission for product imagery was not identified."),
    src("oneplus_nordce3lite_global_launch", "OnePlus (manufacturer, verified channel)", URL_ONEPLUS_LAUNCH,
        "Global announcement date and exact product identity",
        "OnePlus's verified global channel published the Nord CE 3 Lite 5G launch video on 4 April 2023. This is the global announcement date, not Philippine availability.", "2023-04-04"),
    src("oneplus_nordce3lite_ptg_ph", "Pinoy Techno Guide Philippines", URL_PTG,
        "Philippine configuration, official price, first online availability and local specification reference",
        "PTG's exact model page, dated 21 April 2023, reports an official Philippine price of PHP 14,990, 8 GB RAM / 256 GB storage, and online availability through the OnePlus Lazada shop starting 21 April; Shopee from 26 April and stores from 5 May. It is a launch-era page, not a current price source.", "2023-04-21"),
    src("oneplus_nordce3lite_revu_ph", "Revu Philippines", URL_REVU,
        "Philippine official launch, preorder dates, price and model cross-check",
        "Published 20 April 2023. Reports OnePlus Philippines' official launch, PHP 14,990 price, preorders from 21 April, online platform availability and store release from 5 May. Its launch summary says storage up to 256 GB; the official Philippine page and PTG identify the exact 8/256 configuration.", "2023-04-20"),
    src("oneplus_nordce3lite_gizguide_ph", "GizGuide Philippines", URL_GIZGUIDE,
        "Independent local launch and screen-protection discrepancy review",
        "The exact-model Philippine launch article corroborates PHP 14,990, the 8/256 configuration and core hardware. It identifies Asahi Dragontrail Star Glass; PTG and Revu describe Corning Gorilla Glass, and the OnePlus specifications page does not name the cover-glass brand. The protection type is therefore left unresolved.", "2023-04-20"),
    src("oneplus_nordce3lite_gsmarena", "GSMArena", URL_GSMARENA,
        "Exact global model announcement and hardware cross-check",
        "GSMArena published an exact Nord CE 3 Lite hands-on article on 4 April 2023. It is used as a global model cross-check only; it does not establish the Philippine retail configuration or local price.", "2023-04-04"),
    src("oneplus_nordce3lite_nanoreview", "NanoReview", URL_NANOREVIEW,
        "Independent technical cross-check for Snapdragon 695 CPU structure and process",
        "The exact-model profile reports Snapdragon 695, a 6 nm process and 2 x Kryo 660 Gold plus 6 x Kryo 660 Silver CPU cores. Its displayed memory variant is 8/128 GB; its regional variant values are not applied to the locally confirmed 8/256 GB configuration."),
    src("oneplus_nordce3lite_kimovil", "Kimovil", URL_KIMOVIL,
        "Global 8/256 configuration cross-check only",
        "Kimovil has a distinct global 8 GB / 256 GB variant page and lists an 8/128 GB version separately. It is not used as Philippine availability, price, regional code, or local band evidence."),
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


def fields() -> list[dict]:
    rows = [
        f("model_number", S["oneplus_nordce3lite_ph_specs"],
          "The OnePlus Philippines product page does not publish a CPH code; third-party code references do not tie one to the Philippine 8/256 GB listing.", None,
          status="PENDING_VERIFICATION",
          note="Keep the regional retail model number blank until the Philippine box label, exact seller SKU, or regulator record maps a code to this configuration."),
        f("global_release_date", S["oneplus_nordce3lite_global_launch"], "OnePlus global launch video published 4 April 2023", "2023-04-04",
          note="Global product announcement date; Philippine preorders began later."),
        f("configuration", S["oneplus_nordce3lite_ph_specs"], "8 GB LPDDR4X RAM / 256 GB UFS 2.2 storage", "8 GB RAM / 256 GB storage"),
        f("philippine_release_date", S["oneplus_nordce3lite_ptg_ph"],
          "Official OnePlus Lazada online availability reported from 21 April 2023; Shopee from 26 April; retail stores from 5 May", "2023-04-21",
          status="VERIFIED_SECONDARY",
          note="The top-level date records the first reported official online availability, not the later in-store date."),
        f("official_launch_price_php", S["oneplus_nordce3lite_ptg_ph"], "PHP 14,990 official Philippine launch price", 14990, unit="PHP", status="VERIFIED_SECONDARY"),
        f("current_price_php", S["oneplus_nordce3lite_ptg_ph"],
          "Reviewed sources give the April 2023 official launch price; no current dated, orderable Philippine offer was verified on 26 November 2026", None,
          status="PENDING_VERIFICATION", unit="PHP",
          note="Keep catalog price blank. PTG's affiliate links resolve to category pages, not an exact current product offer."),
        f("display_size", S["oneplus_nordce3lite_ph_specs"], "6.72 inches", 6.72, key="displayInches", unit="in"),
        f("display_technology", S["oneplus_nordce3lite_ph_specs"], "LCD; PTG identifies IPS LCD", "IPS LCD", key="displayType", status="VERIFIED_SECONDARY"),
        f("display_resolution", S["oneplus_nordce3lite_ph_specs"], "2400 x 1080 pixels; 391 ppi", "2400 x 1080", key="resolution"),
        f("display_refresh_rate", S["oneplus_nordce3lite_ph_specs"], "120 Hz adaptive refresh rate", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", S["oneplus_nordce3lite_ptg_ph"], "550 nits typical; 680 nits peak", "550 typical; 680 peak", unit="nits", status="VERIFIED_SECONDARY"),
        f("display_protection", S["oneplus_nordce3lite_gizguide_ph"],
          "GizGuide reports Asahi Dragontrail Star Glass; PTG and Revu report Corning Gorilla Glass; OnePlus Philippines does not identify the cover-glass brand", None,
          status="CONFLICTING_INFORMATION",
          note="The local pages conflict on the glass brand, and the manufacturer page does not resolve it. Do not claim either protection brand until primary regional documentation is found."),
        f("chipset", S["oneplus_nordce3lite_ph_specs"], "Qualcomm Snapdragon 695 5G", "Qualcomm Snapdragon 695 5G", key="chipset"),
        f("process_node", S["oneplus_nordce3lite_nanoreview"], "Snapdragon 695 fabricated on a 6 nm process", 6, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", S["oneplus_nordce3lite_nanoreview"], "Octa-core: 2 x Kryo 660 Gold / Cortex-A78 up to 2.2 GHz + 6 x Kryo 660 Silver / Cortex-A55 up to 1.8 GHz", "2x Kryo 660 Gold / Cortex-A78 up to 2.2 GHz + 6x Kryo 660 Silver / Cortex-A55 up to 1.8 GHz", status="VERIFIED_SECONDARY"),
        f("gpu", S["oneplus_nordce3lite_ph_specs"], "Qualcomm Adreno 619", "Adreno 619", key="gpu"),
        f("operating_system", S["oneplus_nordce3lite_ph_specs"], "OxygenOS 13.1 based on Android 13 at launch", "Android 13 with OxygenOS 13.1", key="os"),
        f("os_support", S["oneplus_nordce3lite_ph_specs"], "At least two Android OS upgrades and three years of security updates from launch", "At least 2 Android OS upgrades; 3 years security updates"),
        f("ram_capacity", S["oneplus_nordce3lite_ph_specs"], "8 GB physical LPDDR4X RAM; separate virtual RAM expansion is not counted", 8, key="ramGb", unit="GB"),
        f("ram_type", S["oneplus_nordce3lite_ph_specs"], "LPDDR4X", "LPDDR4X", status="VERIFIED"),
        f("storage_capacity", S["oneplus_nordce3lite_ph_specs"], "256 GB internal storage", 256, key="storageGb", unit="GB"),
        f("storage_type", S["oneplus_nordce3lite_ph_specs"], "UFS 2.2", "UFS 2.2", status="VERIFIED"),
        f("storage_expansion", S["oneplus_nordce3lite_ph_specs"], "Hybrid SIM / SIM-or-microSD slot; microSD support up to 1 TB", "Hybrid slot; microSD up to 1 TB"),
        f("rear_camera_system", S["oneplus_nordce3lite_ph_specs"], "108 MP main + 2 MP depth-assist + 2 MP macro; LED flash", "108 MP main + 2 MP depth + 2 MP macro; LED flash"),
        f("main_camera_sensor", S["oneplus_nordce3lite_ph_specs"], "Samsung S5KHM6SX03, 108 MP, six-element lens, f/1.7, EIS", "Samsung S5KHM6SX03 108 MP; 6P; f/1.7; EIS"),
        f("ultrawide_camera", S["oneplus_nordce3lite_ph_specs"], "Manufacturer lists main, depth-assist and macro rear modules; no ultrawide module listed", "No ultrawide module listed", status="NOT_APPLICABLE"),
        f("telephoto_camera", S["oneplus_nordce3lite_ph_specs"], "Manufacturer lists main, depth-assist and macro rear modules; no telephoto module listed", "No telephoto module listed", status="NOT_APPLICABLE"),
        f("front_camera", S["oneplus_nordce3lite_ph_specs"], "16 MP front camera, f/2.4", 16, key="frontCameraMp", unit="MP"),
        f("video_recording", S["oneplus_nordce3lite_ph_specs"], "Rear: 1080p/30 fps and 720p/30 fps; slow motion 720p/120 fps. Front: 1080p/30 fps and 720p/30 fps", "Rear: 1080p/30, 720p/30; 720p slow motion/120. Front: 1080p/30, 720p/30"),
        f("battery_capacity", S["oneplus_nordce3lite_ph_specs"], "Typical capacity 5000 mAh", 5000, key="batteryMah", unit="mAh"),
        f("battery_technology", S["oneplus_nordce3lite_ptg_ph"], "Li-polymer battery, non-removable", "Li-polymer; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", S["oneplus_nordce3lite_ph_specs"], "67 W SUPERVOOC", 67, key="chargingW", unit="W"),
        f("wireless_charging", S["oneplus_nordce3lite_ph_specs"], "Wireless charging not specified in the reviewed OnePlus Philippines specifications", None, status="NOT_DISCLOSED"),
        f("dimensions", S["oneplus_nordce3lite_ph_specs"], "165.5 x 76.0 x 8.3 mm", "165.5 x 76.0 x 8.3 mm", key="dimensions", unit="mm"),
        f("weight", S["oneplus_nordce3lite_ph_specs"], "195 g", 195, key="weightG", unit="g"),
        f("materials", S["oneplus_nordce3lite_ptg_ph"], "Glass front and plastic back; frame material not separately stated", "Glass front; plastic back; frame not recorded", status="VERIFIED_SECONDARY",
          note="Front cover-glass brand remains disputed and is recorded separately as a conflict."),
        f("ingress_protection", S["oneplus_nordce3lite_ph_specs"], "No IP rating stated on the reviewed manufacturer specification page", None, status="NOT_DISCLOSED"),
        f("sim_esim", S["oneplus_nordce3lite_ph_specs"], "Hybrid dual SIM / SIM-or-microSD slot; eSIM not stated", "Dual nano-SIM hybrid slot; eSIM not recorded"),
        f("cellular_bands", S["oneplus_nordce3lite_ph_specs"], "2G GSM 850/900/1800/1900; 3G WCDMA B1/2/4/5/6/8/19; LTE FDD B1/2/3/4/5/7/8/12/13/17/18/19/20/26/28/32/66 and TDD B38/39/40/41; 5G SA/NSA n1/3/5/7/8/20/28/38/40/41/66/77/78", "5G SA/NSA; 4G LTE; GSM/WCDMA; see manufacturer regional bands", key="cellular"),
        f("wifi", S["oneplus_nordce3lite_ph_specs"], "Wi-Fi 802.11 a/b/g/n/ac, 2.4 GHz and 5 GHz", "Wi-Fi 5 (802.11 a/b/g/n/ac), dual-band", key="wifi"),
        f("bluetooth", S["oneplus_nordce3lite_ph_specs"], "Bluetooth 5.1; aptX, aptX HD, LDAC, AAC and SBC", "Bluetooth 5.1"),
        f("usb", S["oneplus_nordce3lite_ph_specs"], "USB Type-C, USB 2.0; OTG support also listed by PTG", "USB Type-C; USB 2.0; OTG", key="ports"),
        f("nfc", S["oneplus_nordce3lite_ph_specs"], "NFC enabled", "Yes"),
        f("gnss", S["oneplus_nordce3lite_ph_specs"], "GPS, BDS, GLONASS, Galileo and QZSS", "GPS; BDS; GLONASS; Galileo; QZSS", key="gnss"),
        f("audio", S["oneplus_nordce3lite_ph_specs"], "Dual stereo speakers and 3.5 mm headphone jack; PTG lists no FM radio", "Stereo speakers; 3.5 mm jack; FM radio not listed", key="sound", status="VERIFIED_SECONDARY"),
        f("sensors", S["oneplus_nordce3lite_ph_specs"], "Accelerometer, electronic compass, gyroscope, ambient-light sensor, proximity sensor, sensor core; side-mounted fingerprint scanner", "Accelerometer; electronic compass; gyroscope; ambient light; proximity; sensor core; side fingerprint"),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field assessments, got {len(rows)}")
    rows[11]["candidateEvidence"] = [
        {"value": "Corning Gorilla Glass reported", "sourceUrl": URL_PTG, "sourceKind": "independent_ph_reference",
         "observedAt": OBSERVED, "excerpt": "PTG display specification names Corning Gorilla Glass protection.",
         "configurationMatch": "Philippine 8 GB / 256 GB exact model", "reviewStatus": "CONFLICTING_INFORMATION",
         "localAvailabilityVerified": True},
        {"value": "Asahi Dragontrail Star Glass reported", "sourceUrl": URL_GIZGUIDE, "sourceKind": "independent_ph_reference",
         "observedAt": OBSERVED, "excerpt": "GizGuide launch specifications identify Asahi Dragontrail Star Glass.",
         "configurationMatch": "Philippine OnePlus Nord CE 3 Lite 5G", "reviewStatus": "CONFLICTING_INFORMATION",
         "localAvailabilityVerified": True},
        {"value": "Corning Gorilla Glass reported", "sourceUrl": URL_REVU, "sourceKind": "independent_ph_reference",
         "observedAt": OBSERVED, "excerpt": "Revu's Philippine launch write-up describes Corning Gorilla Glass protection.",
         "configurationMatch": "Philippine OnePlus Nord CE 3 Lite 5G", "reviewStatus": "CONFLICTING_INFORMATION",
         "localAvailabilityVerified": True},
    ]
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_OFFICIAL_LAUNCH",
        "availabilityStatus": "OnePlus Philippines launch coverage confirms the local 8 GB / 256 GB version at PHP 14,990, with online availability from 21 April 2023 and in-store availability from 5 May 2023. Current stock and price are not verified.",
        "philippineAvailability": "OnePlus Philippines' local product page and launch reporting identify the Nord CE 3 Lite 5G as a Philippine-market product with 8 GB RAM / 256 GB storage and PHP 14,990 launch pricing. PTG reports online availability through OnePlus's Lazada shop from 21 April 2023, Shopee from 26 April, and stores from 5 May. This verifies historical official local launch availability, not current stock or price. The Philippine regional CPH model code remains unconfirmed.",
        "observedAt": OBSERVED,
        "manufacturer": "OnePlus",
        "catalogModel": "Nord CE 3 Lite 5G",
        "productLine": "OnePlus Nord series",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Official OnePlus online availability reported from 21 April 2023; stores from 5 May",
        "researchNotes": "Workbook row 152 OnePlus Nord CE 3 Lite matches OnePlus Philippines' exact Nord CE 3 Lite 5G product and local 8 GB / 256 GB variant. Global announcement date is 4 April 2023; local online availability started 21 April with in-store availability 5 May, at the reported PHP 14,990 official launch price. OnePlus's Philippine page does not provide a local CPH model code. Current price is not verified. PTG and Revu identify Gorilla Glass while GizGuide names Asahi Dragontrail Star Glass; the cover-glass brand remains conflicted. Workbook eligibility remains Pending.",
        "qualityFlag": "Exact Philippine OnePlus Nord CE 3 Lite 5G, 8 GB / 256 GB configuration, official launch price and historic online/store dates supported; CPH code and current price unverified; cover-glass brand conflict retained; image reuse rights not established; study scope remains Pending.",
        "openIssues": [
            {"issue": "The Philippine OnePlus page does not publish a CPH model number", "action": "Keep the local regional model code blank until OnePlus, the box label, or a reliable local regulatory record maps a code to the 8/256 SKU."},
            {"issue": "Philippine launch coverage conflicts on display cover-glass brand", "action": "Keep protection unreported until primary regional documentation resolves Gorilla Glass versus Dragontrail Star Glass."},
            {"issue": "No current dated and orderable Philippine price was verified", "action": "Keep the current price blank and retain PHP 14,990 as a historical launch SRP only."},
            {"issue": "Official and Philippine product pages show exact-model images but no reusable license or permission was found", "action": "Keep the neutral image placeholder and preserve image source metadata."},
            {"issue": "Workbook eligibility remains Pending", "action": "Preserve the supplied study-scope status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 152 or device.get("category") != "smartphones"
            or device.get("brand") != "OnePlus" or device.get("model") != "Nord CE 3 Lite"):
        raise ValueError("Workbook row 152 guard failed; expected OnePlus Nord CE 3 Lite smartphone")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("OnePlus Nord CE 3 Lite already has manual-review rows; refusing duplicate replacement")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise ValueError("Expected the original unrecorded-configuration placeholder before review")

    variant = {"id": CONFIG, "label": "8 GB RAM / 256 GB storage (Philippine configuration)",
               "modelCode": None, "sku": None,
               "notes": "OnePlus Philippines and local launch coverage identify this 8/256 GB configuration at PHP 14,990 in April 2023. The CPH regional code and current Philippine price are not verified."}
    item = {
        "deviceId": DEVICE, "configurationId": CONFIG, "brand": "OnePlus", "model": "Nord CE 3 Lite 5G",
        "configuration": variant["label"], "modelCode": None, "sku": None,
        "sources": SOURCES, "fields": fields(),
        "availabilityEvidence": availability_evidence(),
        "replacementVariants": [variant], "replaceUnrecordedPlaceholder": True,
    }
    add_review(manual, catalog, item)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "OnePlus Philippines and PTG show exact-model product imagery, but no reusable license or permission to copy or hotlink was identified. Keep the neutral placeholder.",
        "sourcePage": URL_ONEPLUS_PRODUCT, "assetUrl": None,
        "scope": "OnePlus Nord CE 3 Lite 5G; Philippine 8 GB / 256 GB configuration",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for OnePlus Nord CE 3 Lite 5G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "OnePlus", "model_name": "Nord CE 3 Lite 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_ONEPLUS_SPECS, "result": "Official Philippines specification page confirms the local 8/256 SKU and regional hardware, including full local network bands."},
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "PTG reports official PHP 14,990 price and availability via OnePlus online shops from 21 April 2023, Shopee from 26 April, stores from 5 May."},
            {"device_id": DEVICE, "source_url": URL_REVU, "result": "Revu confirms official Philippine launch, launch price and order/retail dates; launch report lists up to 256 GB storage."},
            {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "GizGuide identifies Asahi Dragontrail Star Glass while PTG/Revu say Corning Gorilla Glass; protection brand remains a conflict."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "Exact global model and 4 April 2023 announcement cross-checked; not used as local configuration evidence."},
            {"device_id": DEVICE, "source_url": URL_NANOREVIEW, "result": "Exact model CPU core configuration and 6nm process checked; its 8/128 memory entry was not substituted for Philippine 8/256."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Kimovil lists the exact global 8/256 variant separately from 8/128; no local market claim was inferred."},
            {"device_id": DEVICE, "source_url": URL_ONEPLUS_LAUNCH, "result": "OnePlus global launch video is dated 4 April 2023."},
        ],
        "prices": [{
            "device_id": DEVICE, "amount_php": 14990, "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_8gb_256gb_configuration",
            "variant_ram_gb": 8, "variant_storage_gb": 256,
            "price_type": "historical_ph_official_launch_srp", "source_published_at": "2023-04-21",
            "excerpt": "PTG reports PHP 14,990 official Philippine price for the OnePlus Nord CE 3 Lite 5G 8 GB / 256 GB configuration on its 21 April 2023 launch-era page; historical SRP, not a current offer.",
            "source_url": URL_PTG, "source_kind": "historical_local_launch_price",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_launch_price_not_current",
        }],
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "workbookRow": 152, "device": "OnePlus Nord CE 3 Lite 5G",
        "configuration": "8 GB / 256 GB Philippine version", "reviewedFields": len(item["fields"]),
        "sources": len(SOURCES), "historicalLaunchPricePhp": 14990,
        "globalAnnouncement": "2023-04-04", "philippineOnlineAvailability": "2023-04-21",
        "currentPrice": None, "modelCode": "not confirmed", "screenProtection": "conflicting",
        "imageRights": "not established; neutral placeholder retained", "scopeStatus": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
