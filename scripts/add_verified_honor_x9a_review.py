#!/usr/bin/env python3
"""Record the source-matched Philippine HONOR X9a 5G configuration."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-x9a-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_beb039b6abbf82"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-8gb-256gb-ph"

URL_HONOR = "https://www.honor.com/ph/phones/honor-x9a/"
URL_HONOR_SPECS = "https://www.honor.com/ph/phones/honor-x9a/spec/"
URL_HONOR_GLOBAL_SPECS = "https://www.honor.com/global/phones/honor-x9a/spec/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/6-series/snapdragon-695-5g-mobile-platform"
URL_YUGA_LAUNCH = "https://www.yugatech.com/news/honor-x9a-5g-launches-in-the-philippines-priced/"
URL_YUGA_REVIEW = "https://www.yugatech.com/mobile/honor-x9a-5g-review/"
URL_YUGA_PRICE_LIST = "https://www.yugatech.com/honor-phone-price-list-philippines/"
URL_FIRST_SALE = "https://phil-it.org.ph/look-mega-crowd-at-honor-x9a-5gs-first-day-sale/"
URL_REVU = "https://www.revu.com.ph/2023/02/honor-x9a-5g-review-price-specs/"
URL_JAM = "https://jamonline.ph/reviews/honor-x9a-5g-review/"
IMAGE_URL = "https://www-file.honor.com/content/dam/honor/ph/specs/smartphone/honor-x9a/honor-x9a-gl.png"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def field(fid: str, source_id: str, value, normalized_value, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str,
          configuration_match="Philippine launch configuration: 8 GB physical RAM / 256 GB storage") -> dict:
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
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "honor"
            or device.get("model") != "X9a"):
        raise ValueError("The source record no longer matches the HONOR X9a workbook identity")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR X9a already has a manual review; inspect it before replacing")

    sources = [
        source("honor_x9a_ph_official_product", "HONOR Philippines", URL_HONOR,
               "Official Philippine product identity and selected design, battery, and display claims",
               "The Philippines product page identifies HONOR X9a 5G and publishes its 120 Hz curved AMOLED display, 5100 mAh typical battery, 40 W charging, 7.9 mm depth, 175 g weight, and 8 GB + 5 GB HONOR RAM Turbo. Virtual RAM is not counted as physical RAM."),
        source("honor_x9a_ph_official_specs", "HONOR Philippines", URL_HONOR_SPECS,
               "Official Philippine specification page and exact-model image source",
               "HONOR Philippines identifies the X9a 5G and its Emerald Green and Titanium Silver image assets. The page's accessible text renderer does not expose all specification values."),
        source("honor_x9a_official_global_specs", "HONOR", URL_HONOR_GLOBAL_SPECS,
               "Manufacturer specification cross-check for model code and technical specifications",
               "HONOR's official X9a specifications identify model code RMO-NX1, 8 GB + 256 GB among global memory configurations, display, processor, camera, OS, battery, dimensions, connectivity, and sensors. Global variant lists are not used to add Philippine variants."),
        source("honor_x9a_qualcomm_platform", "Qualcomm", URL_QUALCOMM,
               "Primary source for Snapdragon 695 process, CPU family, and platform characteristics",
               "Qualcomm specifies Snapdragon 695 as a 6 nm platform with Kryo 660 CPU up to 2.2 GHz and Adreno 619 GPU. Device-specific frequency layout is taken from HONOR's X9a specifications."),
        source("honor_x9a_ph_launch_yugatech", "YugaTech", URL_YUGA_LAUNCH,
               "Contemporaneous Philippine launch, local configuration, launch price, and specifications",
               "Published 2023-01-19. Reports the Philippine launch, preorder period beginning January 20, the 8 GB RAM / 256 GB storage model, PHP 16,990 SRP, and a detailed local specification list.",
               "2023-01-19"),
        source("honor_x9a_ph_first_sale", "Philippine Information Technology Organization", URL_FIRST_SALE,
               "Documented first-day Philippine retail availability and nationwide channels",
               "Published 2023-02-05; the article states the HONOR X9a 5G officially hit stores on February 4, 2023, at PHP 16,990 through HONOR kiosks, partner stores, and online channels.",
               "2023-02-05"),
        source("honor_x9a_ph_yugatech_review", "YugaTech", URL_YUGA_REVIEW,
               "Independent local review, device experience, pricing, and exact launch configuration cross-check",
               "The local review lists the 8 GB / 256 GB PHP 16,990 configuration and the device specifications. Its FAQ describes the rear as frosted glass; that material statement conflicts with REVU's review and is not promoted as settled fact.",
               "2023-02-01"),
        source("honor_x9a_ph_revu_review", "REVU Philippines", URL_REVU,
               "Independent Philippine review and cross-check for configuration, storage expansion, audio, and materials",
               "The Philippine review identifies 8 GB RAM / 256 GB storage, no microSD slot, a single downward-firing speaker, no 3.5 mm audio port, and a plastic rear with aluminum frame. Its rear-material description conflicts with YugaTech's frosted-glass description.",
               "2023-02-07"),
        source("honor_x9a_ph_jam_review", "Jam Online", URL_JAM,
               "Independent Philippine hands-on review and camera/software cross-check",
               "The local review documents the 8 GB / 256 GB device, MagicUI 6.1 based on Android 12, Snapdragon 695, 5100 mAh battery, 40 W charging, and front video capture up to 1080p at 30 fps.",
               "2023-02-12"),
        source("honor_x9a_ph_price_history_yugatech", "YugaTech", URL_YUGA_PRICE_LIST,
               "Dated Philippine launch-price history; not a current retail offer",
               "The price-list row records HONOR X9a 5G 8 GB / 256 GB at PHP 16,990 as verified on February 7, 2023. This is historical launch-era evidence and does not establish a current price or stock.",
               "2023-02-07"),
    ]
    official = "honor_x9a_official_global_specs"
    ph_product = "honor_x9a_ph_official_product"
    launch = "honor_x9a_ph_launch_yugatech"
    retail = "honor_x9a_ph_first_sale"
    yuga_review = "honor_x9a_ph_yugatech_review"
    revu = "honor_x9a_ph_revu_review"
    jam = "honor_x9a_ph_jam_review"
    price_history = "honor_x9a_ph_price_history_yugatech"
    qualcomm = "honor_x9a_qualcomm_platform"

    fields = [
        field("model_number", official, "RMO-NX1 (HONOR global model code); Philippine retail SKU not stated", "RMO-NX1 (global model code)", status="VERIFIED", note="HONOR's official model-specific X9a specification page associates the product with RMO-NX1. Local launch sources identify X9a 5G but do not name a separate Philippine SKU."),
        field("configuration", launch, "8 GB RAM / 256 GB storage", "8 GB physical RAM / 256 GB storage", status="VERIFIED_SECONDARY", note="YugaTech's Philippine launch report and local review identify this exact Philippine launch configuration. HONOR's extra 5 GB RAM Turbo is virtual memory and is not added to physical RAM."),
        field("philippine_release_date", retail, "Official store availability began February 4, 2023", "2023-02-04", note="Contemporaneous local reporting says the handset officially hit stores on February 4, 2023. The source is dated February 5; this is a reported availability date, not proof of every store's stock."),
        field("official_launch_price_php", launch, "PHP 16,990 SRP for 8 GB / 256 GB, reported January 19, 2023", 16990, unit="PHP", note="Historical Philippine launch SRP for the documented 8 GB / 256 GB model. Do not present as current pricing."),
        field("current_price_php", price_history, "No current dated Philippine retail offer established; last verified YugaTech listing reviewed is February 7, 2023", None, status="PENDING_VERIFICATION", unit="PHP", note="Available price evidence is historical. The catalog current-price value remains blank pending a current exact-configuration seller observation."),
        field("display_size", official, "6.67 inches", 6.67, key="displayInches", unit="in", status="VERIFIED", note="HONOR's model-specific display specification."),
        field("display_technology", official, "Curved AMOLED", "Curved AMOLED", key="displayType", status="VERIFIED", note="HONOR Philippines describes the X9a as having a 120 Hz curved AMOLED display; the global spec sheet identifies AMOLED."),
        field("display_resolution", official, "1080 × 2400 pixels", "1080 x 2400", key="resolution", status="VERIFIED", note="HONOR's model-specific specification; local launch report gives the same FHD+ resolution."),
        field("display_refresh_rate", launch, "120 Hz refresh; 300 Hz touch sampling", 120, key="refreshHz", unit="Hz", note="The catalog refresh-rate field records the display refresh only. Touch sampling is retained in the source note."),
        field("display_brightness", ph_product, "800 nits full-screen brightness", 800, unit="nits", status="VERIFIED", note="HONOR Philippines labels 800 nits as full-screen brightness; it is not described as a peak HDR value."),
        field("display_protection", ph_product, "0.65 mm deeply reinforced glass; HONOR reports stress above 900 MPa", "Deeply reinforced display glass; 0.65 mm / over 900 MPa as reported by HONOR", status="VERIFIED", note="Manufacturer's lab statement is preserved as a manufacturer claim; no third-party drop rating or guaranteed outcome is inferred."),
        field("chipset", launch, "Qualcomm Snapdragon 695 5G", "Qualcomm Snapdragon 695 5G", key="chipset", note="Philippine launch report identifies this chipset."),
        field("process_node", qualcomm, "6 nm process technology", 6, unit="nm", status="VERIFIED", note="Qualcomm lists a 6 nm process for Snapdragon 695; the local launch source matches the phone to that platform."),
        field("cpu", official, "Octa-core: 2 × Cortex-A78 up to 2.2 GHz + 6 × Cortex-A55 up to 1.8 GHz", "Octa-core: 2x A78 up to 2.2 GHz + 6x A55 up to 1.8 GHz", key="cpu", status="VERIFIED", note="HONOR's model-specific X9a spec page lists this CPU layout; Qualcomm confirms the platform's peak clock up to 2.2 GHz."),
        field("gpu", official, "Adreno 619", "Adreno 619", key="gpu", status="VERIFIED", note="HONOR's X9a specifications and Qualcomm's Snapdragon 695 specifications identify Adreno 619."),
        field("operating_system", official, "MagicUI 6.1 based on Android 12", "MagicUI 6.1 (Android 12)", key="os", status="VERIFIED", note="Software version at the Philippine launch; subsequent update state is not implied."),
        field("os_support", launch, "No published Philippine OS/security update policy found in the reviewed model sources", None, status="PENDING_VERIFICATION", note="A current support policy was not established in this pass; no update duration is inferred."),
        field("ram_capacity", launch, "8 GB RAM; HONOR separately advertises up to 5 GB RAM Turbo extension", 8, key="ramGb", unit="GB", note="8 GB is physical RAM for the local configuration. RAM Turbo is storage-backed virtual memory and not included in the physical figure."),
        field("ram_type", official, "RAM technology not specified in the reviewed model-specific sources", None, status="NOT_DISCLOSED", unit="", note="No LPDDR generation or physical RAM type is stated in the reviewed HONOR and Philippine launch sources."),
        field("storage_capacity", launch, "256 GB storage", 256, key="storageGb", unit="GB", note="Exact Philippine launch configuration."),
        field("storage_type", official, "Storage technology not specified", None, status="NOT_DISCLOSED", note="The reviewed HONOR and Philippine launch specifications state capacity but not eMMC/UFS type."),
        field("storage_expansion", revu, "No microSD slot", "No microSD card slot", status="VERIFIED_SECONDARY", note="REVU's local hands-on review explicitly reports no microSD slot."),
        field("rear_camera_system", official, "64 MP f/1.8 main + 5 MP f/2.2 ultra-wide/depth + 2 MP f/2.4 macro", "64 MP main + 5 MP ultra-wide/depth + 2 MP macro", status="VERIFIED", note="HONOR's model-specific specification identifies the modules and apertures; local launch reporting independently lists the same camera configuration."),
        field("main_camera_sensor", official, "64 MP main camera; sensor make/model not stated", None, status="NOT_DISCLOSED", note="Camera resolution is not a sensor model; the reviewed sources do not name the sensor."),
        field("ultrawide_camera", official, "5 MP f/2.2 ultra-wide and depth camera", "5 MP ultra-wide/depth", note="HONOR describes this single module as Ultra Wide & Depth; it is not represented as a separate depth camera."),
        field("telephoto_camera", official, "No telephoto module in the manufacturer-listed triple-camera system", "No telephoto module listed", status="NOT_APPLICABLE", note="The model-specific manufacturer specification enumerates all three rear modules as main, ultra-wide/depth, and macro."),
        field("front_camera", official, "16 MP f/2.45", 16, key="frontCameraMp", unit="MP", status="VERIFIED", note="HONOR's model specification and local launch report agree."),
        field("video_recording", official, "Rear video up to 1080p; JamOnline reports front video up to 1080p/30 fps; REVU reports regular video 1080p/30 fps and Multi-video 720p/30 fps", "Up to 1080p/30 fps regular video; 720p/30 fps Multi-video reported", note="Mode details differ by camera/use; source-specific resolution and frame rate are kept explicit."),
        field("battery_capacity", ph_product, "5100 mAh typical; 4900 mAh rated", 5100, key="batteryMah", unit="mAh", status="VERIFIED", note="HONOR Philippines states both typical and rated capacity. The catalog value uses the typical capacity and the rated value remains in the note."),
        field("battery_technology", official, "Lithium polymer", "Lithium polymer", status="VERIFIED", note="HONOR's model-specific specifications list the battery type."),
        field("wired_charging", ph_product, "40 W HONOR SuperCharge", 40, key="chargingW", unit="W", status="VERIFIED", note="HONOR Philippines specifies a maximum wired charging power of 40 W with the original charger and cable."),
        field("wireless_charging", official, "Wireless charging not listed in the reviewed specifications", None, status="NOT_DISCLOSED", note="No wireless or reverse charging capability is claimed in the reviewed model specification pages."),
        field("dimensions", official, "161.6 × 73.9 × 7.9 mm", "161.6 x 73.9 x 7.9 mm", key="dimensions", unit="mm", status="VERIFIED", note="HONOR's model-specific specifications; depth is the stated body depth and excludes camera bump per manufacturer caveat."),
        field("weight", official, "Approximately 175 g including battery", 175, key="weightG", unit="g", status="VERIFIED", note="HONOR's model-specific specifications; actual weight can vary by configuration and measurement method."),
        field("materials", yuga_review, "YugaTech FAQ says frosted glass back; REVU describes a plastic rear and aluminum frame", None, status="PENDING_VERIFICATION", note="The two Philippine reviews conflict on rear-panel material. The catalog material field remains blank until the difference is resolved."),
        field("ingress_protection", official, "No IP rating stated in the reviewed HONOR model specifications", None, status="NOT_DISCLOSED", note="No IP dust/water rating is recorded; none is inferred from the display durability claims."),
        field("sim_esim", launch, "Dual SIM; official global specification specifies Nano-SIM slots. eSIM is not listed.", "Dual Nano-SIM; eSIM not recorded", note="YugaTech confirms dual SIM and HONOR's model specification lists two Nano card slots; eSIM support is not claimed."),
        field("cellular_bands", launch, "5G and 4G LTE; specific Philippine frequency bands not listed", "5G and 4G LTE; specific bands not recorded", key="cellular", note="Network generations are reported locally; no Philippine band list is inferred from chipset capability."),
        field("wifi", official, "802.11 a/b/g/n/ac; 2.4 GHz and 5 GHz", "Wi-Fi 5 (802.11 a/b/g/n/ac), 2.4/5 GHz", key="wifi", status="VERIFIED", note="HONOR's model-specific specification."),
        field("bluetooth", official, "Bluetooth 5.1", "Bluetooth 5.1", status="VERIFIED", note="HONOR's model-specific specifications and Philippine launch report agree."),
        field("usb", official, "USB Type-C, USB 2.0", "USB Type-C, USB 2.0", key="ports", status="VERIFIED", note="HONOR's model-specific specification; YugaTech's local report confirms USB Type-C connector."),
        field("nfc", launch, "NFC listed for Philippine model; HONOR global specification says NFC is supported only on RMO-NX1", "NFC supported on RMO-NX1", status="VERIFIED_SECONDARY", note="Philippine launch reporting lists NFC; HONOR's global specification limits NFC support to RMO-NX1, the model code on the exact X9a product page."),
        field("gnss", official, "GPS, A-GPS, GLONASS, BeiDou, Galileo", "GPS, A-GPS, GLONASS, BeiDou, Galileo", status="VERIFIED", note="HONOR's model-specific positioning list."),
        field("audio", revu, "Single downward-firing speaker; no 3.5 mm jack; USB-C audio", "Single speaker; no 3.5 mm jack; USB-C audio", status="VERIFIED_SECONDARY", note="REVU documents the single speaker and absent 3.5 mm jack; HONOR's global spec lists Type-C earphone output."),
        field("sensors", official, "Gravity, in-screen fingerprint, gyroscope, compass, ambient light, and proximity sensors", "Gravity; in-screen fingerprint; gyroscope; compass; ambient light; proximity", status="VERIFIED", note="HONOR's model-specific sensor list. Fingerprint sensor is included as a device sensor; NFC is recorded separately."),
    ]

    review = {
        "deviceId": DEVICE, "configurationId": CONFIG,
        "brand": "HONOR", "model": "X9a",
        "configuration": "8 GB physical RAM / 256 GB storage",
        "configurationLabel": "8 GB RAM / 256 GB storage",
        "sources": sources, "fields": fields,
        "replacementVariants": [{
            "id": CONFIG, "label": "8 GB RAM / 256 GB storage",
            "sku": None, "modelCode": "RMO-NX1",
            "notes": "YugaTech's contemporaneous Philippine launch reporting identifies the local 8 GB / 256 GB configuration. HONOR's global specifications identify RMO-NX1 and the same configuration; a separate Philippine retailer SKU is not stated. HONOR's 5 GB RAM Turbo is virtual memory, not additional physical RAM.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine retail availability was reported beginning February 4, 2023; present stock is not established.",
            "philippineAvailability": "Contemporaneous Philippine reporting states that the phone became available at HONOR kiosks, partner stores, and online channels from February 4, 2023.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "X Series",
            "philippineReleaseYear": 2023,
            "philippineDateLabel": "First reported Philippine retail availability",
            "researchNotes": "The workbook label HONOR X9a matches HONOR's Philippines X9a 5G product and the 2023 Philippine launch reports. The reported local launch configuration is 8 GB physical RAM / 256 GB storage. The PHP 16,990 SRP is historical; current price and stock are not established. The global spec page lists additional memory configurations, but no additional Philippine variant is added without local evidence.",
            "qualityFlag": "Current price and stock not verified; rear material conflict unresolved",
            "openIssues": [
                {"issue": "Current exact-configuration price and stock are not verified", "action": "Keep current price blank until a current Philippine offer matching the 8 GB / 256 GB model is observed."},
                {"issue": "Local reviewers conflict on rear-panel material", "action": "Keep material blank until manufacturer or variant-specific evidence resolves the glass-versus-plastic descriptions."},
                {"issue": "Published OS/security update policy not established", "action": "Keep support term unresolved; do not infer from the Android version at launch."},
                {"issue": "Exact local retail SKU and variant code are not documented", "action": "Retain RMO-NX1 as the official model code while leaving any Philippine-specific retailer SKU blank."},
                {"issue": "Reuse rights for the exact official product image are not established", "action": "Continue showing the neutral placeholder until image permission or a reusable license is documented."},
            ],
        },
    }

    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR X9a Emerald Green product image was identified on the official HONOR Philippines specification page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_HONOR_SPECS,
        "assetUrl": IMAGE_URL,
        "scope": "Exact HONOR X9a model and Emerald Green color variant; the 8 GB / 256 GB storage configuration is not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR X9a",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "X9a", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [{
            "device_id": DEVICE, "amount_php": 16990,
            "configuration_id": CONFIG, "configuration_match": "exact",
            "variant_ram_gb": 8, "variant_storage_gb": 256,
            "price_type": "independent_reported_historical_price",
            "source_published_at": "2023-01-19",
            "excerpt": "YugaTech's January 19, 2023 Philippine launch report identifies HONOR X9a 5G at 8 GB RAM / 256 GB storage and PHP 16,990 SRP, with preorder beginning January 20. Historical launch price, not current.",
            "source_url": URL_YUGA_LAUNCH, "source_kind": "independent_ph_reference",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
            "availability_status": "historical_launch_price",
        }],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "HONOR X9a inventory record matched to HONOR X9a 5G Philippine launch sources",
        "configuration": "8 GB / 256 GB",
        "reviewedFields": len(fields),
        "firstReportedRetailAvailability": "2023-02-04",
        "historicalLaunchPricePhp": 16990,
        "currentPriceLoaded": False,
        "unresolvedMaterials": "YugaTech and REVU disagree; kept blank",
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
