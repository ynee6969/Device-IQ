#!/usr/bin/env python3
"""Record the source-matched Philippine HONOR X9c 5G configuration."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-x9c-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_bd830ce3628852"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-12gb-256gb-ph"

URL_HONOR = "https://www.honor.com/ph/phones/honor-x9c/"
URL_HONOR_SPECS = "https://www.honor.com/ph/phones/honor-x9c/spec/"
URL_HONOR_SUPPORT = "https://www.honor.com/sa-en/support/phones/honor-x9c/"
URL_HONOR_SG_SPECS = "https://www.honor.com/sg/phones/honor-x9c/spec/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/6-series/snapdragon-6-gen-1-mobile-platform"
URL_YUGA_LAUNCH = "https://www.yugatech.com/news/honor-x9c-5g-specs-price-philippines/"
URL_YUGA_SPECS = "https://www.yugatech.com/spec/honor-x9c-5g-2/"
URL_YUGA_PRICE_LIST = "https://www.yugatech.com/honor-gadget-price-list-philippines/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/honor-x9c-5g"
URL_PTG_REVIEW = "https://www.pinoytechnoguide.com/reviews/honor-x9c-5g"
URL_REVU = "https://www.revu.com.ph/2025/01/honor-x9c-5g-review-price-specs/"
URL_OCTAGON = "https://www.octagon.com.ph/products/honor-x9c-12gb-256gb-jade-cyan"
URL_BESTTECH = "https://besttechasia.com/honor-x9c-5g-full-specs-price-philippines/"
IMAGE_URL = "https://www-file.honor.com/content/dam/honor/ph/specs/smartphone/honor-x9c/honor-x9c-cyan.png"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None, source_kind: str | None = None) -> dict:
    item = {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}
    if source_kind:
        item["sourceKind"] = source_kind
    return item


def field(fid: str, source_id: str, value, normalized_value, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str,
          configuration_match="Philippine 12 GB physical RAM / 256 GB storage configuration") -> dict:
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
            or device.get("model") != "X9c"):
        raise ValueError("The source record no longer matches the HONOR X9c workbook identity")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR X9c already has a manual review; inspect it before replacing")

    sources = [
        source("honor_x9c_ph_official_product", "HONOR Philippines", URL_HONOR,
               "Official Philippines model identity, display, battery, charging, durability, and colorways",
               "HONOR Philippines identifies HONOR X9c, 6600 mAh silicon-carbon battery, 66 W SuperCharge, 189 g weight, 7.98 mm thickness, Ultra-Bounce Anti-Drop Technology 2.0, and IP65M marketing language."),
        source("honor_x9c_ph_official_specs", "HONOR Philippines", URL_HONOR_SPECS,
               "Official Philippine model specification page and exact product-image source",
               "The official Philippines specifications page identifies HONOR X9c and Titanium Purple, Titanium Black, and Jade Cyan. Its text-rendered spec table omits most values; no image asset is copied because reuse rights are not stated."),
        source("honor_x9c_official_support", "HONOR", URL_HONOR_SUPPORT,
               "Manufacturer support page identifying model code and physical configurations",
               "HONOR support identifies HONOR X9c as model BRP-NX1 and lists physical 8 GB / 256 GB and 12 GB / 256 GB versions. This is model-code evidence, not a Philippine-specific retail SKU statement."),
        source("honor_x9c_sg_official_specs", "HONOR Singapore", URL_HONOR_SG_SPECS,
               "Official regional technical specification cross-check",
               "HONOR Singapore's model-specific specifications list display, CPU layout, GPU, MagicOS/Android version, cameras, 6600 mAh battery, charging, connectivity, and sensors. Region-only variants are not imported into the Philippine catalog."),
        source("honor_x9c_qualcomm_platform", "Qualcomm", URL_QUALCOMM,
               "Primary source for Snapdragon 6 Gen 1 process technology and platform specifications",
               "Qualcomm specifies Snapdragon 6 Gen 1 as a 4 nm platform with CPU up to 2.2 GHz. Device-specific CPU layout is taken from HONOR's model specification."),
        source("honor_x9c_ph_launch_yugatech", "YugaTech", URL_YUGA_LAUNCH,
               "Contemporaneous Philippine launch, local pricing, market availability, and feature specifications",
               "Published 2025-01-11. Reports the HONOR X9c 5G launched in the Philippines at PHP 16,999, available through HONOR's official online stores, and provides a detailed local specification list. It mentions 256 GB and 512 GB storage options but gives a single price without a distinct 512 GB local SKU offer.",
               "2025-01-11"),
        source("honor_x9c_ph_price_history_yugatech", "YugaTech", URL_YUGA_PRICE_LIST,
               "Dated Philippine launch-price history cross-check",
               "YugaTech records HONOR X9c 5G at PHP 16,999, verified January 11, 2025; this is launch-era history, not a present offer.",
               "2025-01-11"),
        source("honor_x9c_ph_ptg_product", "Pinoy Techno Guide", URL_PTG,
               "Philippine price, pre-order, and local configuration cross-check",
               "Published 2025-01-10. PTG identifies the 12 GB / 256 GB HONOR X9c 5G at PHP 16,999 and reports it available for preorder through HONOR stores, kiosks, and official online stores.",
               "2025-01-10"),
        source("honor_x9c_ph_ptg_review", "Pinoy Techno Guide", URL_PTG_REVIEW,
               "Independent Philippine hands-on review and local 12 GB / 256 GB configuration cross-check",
               "The local review documents the X9c 5G tested with 12 GB physical RAM and 256 GB storage, the Snapdragon 6 Gen 1, 6600 mAh Si/C battery, and 66 W charging.",
               "2025-01-10"),
        source("honor_x9c_ph_revu_review", "REVU Philippines", URL_REVU,
               "Independent Philippine review and source for build, screen, materials, and feature conflicts",
               "Published 2025-01-10. REVU identifies its exact 12 GB / 256 GB review unit, polycarbonate rear, 120 Hz curved display, 4,000-nit peak brightness, IP65M, 4K rear video, 16 MP front camera, and 66 W charging.",
               "2025-01-10"),
        source("honor_x9c_ph_octagon_listing", "Octagon Computer Superstore", URL_OCTAGON,
               "Exact-configuration Philippine retailer price and stock-status observation",
               "At access on 2026-11-26, the exact HONOR X9c 12 GB / 256 GB Jade Cyan listing displayed PHP 16,999 but was marked Out of stock. This is a price observation, not an available offer.",
               source_kind="retailer_price_observation"),
        source("honor_x9c_ph_besttech_price_guide", "Best Tech Asia", URL_BESTTECH,
               "Recent independent Philippine guide-price cross-check",
               "The 2026 Philippine guide lists the 12 GB / 256 GB model at PHP 16,999 and was updated 2026-11-16. It links to official marketplace stores but does not establish a live, in-stock exact-configuration checkout price.",
               "2026-11-16", source_kind="independent_price_guide"),
        source("honor_x9c_yugatech_specs", "YugaTech", URL_YUGA_SPECS,
               "Detailed secondary specification cross-check",
               "YugaTech's specification database identifies processor, CPU layout, GPU, camera, IP rating, and other technical fields. It lists 8/12 GB RAM and 256/512 GB storage generally; those additional combinations are not treated as Philippine configurations without local variant-specific sale evidence.",
               source_kind="independent_specification_database"),
    ]
    official = "honor_x9c_sg_official_specs"
    ph_product = "honor_x9c_ph_official_product"
    launch = "honor_x9c_ph_launch_yugatech"
    ptg = "honor_x9c_ph_ptg_product"
    ptg_review = "honor_x9c_ph_ptg_review"
    revu = "honor_x9c_ph_revu_review"
    octagon = "honor_x9c_ph_octagon_listing"
    qualcomm = "honor_x9c_qualcomm_platform"

    fields = [
        field("model_number", "honor_x9c_official_support", "BRP-NX1 (manufacturer support model code); Philippine retailer SKU not stated", "BRP-NX1 (manufacturer model code)", status="VERIFIED", note="HONOR's official support page identifies the X9c as BRP-NX1. Local Philippine sources do not state a separate retail SKU."),
        field("configuration", ptg, "12 GB RAM / 256 GB storage", "12 GB physical RAM / 256 GB storage", status="VERIFIED_SECONDARY", note="PTG and the Philippine Octagon listing identify this exact local configuration; HONOR's support page lists the same 12/256 model. HONOR RAM Turbo is virtual memory and is not counted as physical RAM."),
        field("philippine_release_date", ptg, "HONOR X9c 5G pre-order was reported on January 10, 2025", "2025-01-10", note="The first reviewed Philippine preorder report is dated January 10, 2025. YugaTech reports official online purchase availability on January 11; neither date proves a first retail transaction."),
        field("official_launch_price_php", launch, "PHP 16,999 for the Philippine launch model, reported January 11, 2025", 16999, unit="PHP", note="Historical launch SRP. YugaTech lists storage capacities 256 GB and 512 GB but provides no separate local 512 GB price/configuration evidence in the launch article; the exact supported Philippine retail listing found is 12/256."),
        field("current_price_php", octagon, "PHP 16,999 listed for exact 12 GB / 256 GB Jade Cyan; Octagon marked the item Out of stock at access on 2026-11-26", None, status="PENDING_VERIFICATION", unit="PHP", note="The dated retailer amount is preserved in the price snapshot, but the page marked the item Out of stock; it is not a purchasable current offer. The catalog price remains blank until a current in-stock exact-configuration offer is verified."),
        field("display_size", official, "6.78 inches", 6.78, key="displayInches", unit="in", status="VERIFIED", note="HONOR's model-specific display specification."),
        field("display_technology", official, "Curved AMOLED", "Curved AMOLED", key="displayType", status="VERIFIED", note="HONOR's regional model-specific spec page and Philippine reviews identify a curved AMOLED display."),
        field("display_resolution", official, "2700 × 1224 pixels", "2700 x 1224", key="resolution", status="VERIFIED", note="HONOR's model-specific specification; local reporting gives the same resolution."),
        field("display_refresh_rate", official, "Up to 120 Hz adjustable refresh rate", 120, key="refreshHz", unit="Hz", status="VERIFIED", note="HONOR's specification lists 120 Hz; actual app refresh may vary."),
        field("display_brightness", ph_product, "HONOR Philippines says 4000 nits typical brightness; YugaTech and REVU call 4000 nits peak/HDR brightness", None, status="CONFLICTING_INFORMATION", unit="nits", note="The number is consistent but the manufacturer and local sources use different brightness qualifiers (typical versus peak/HDR). The field is left blank until the measurement condition is reconciled."),
        field("display_protection", ph_product, "HONOR Ultra-Bounce Anti-Drop Technology 2.0; manufacturer reports a 2 m drop test", "HONOR Ultra-Bounce Anti-Drop Technology 2.0; 2 m manufacturer drop-test claim", status="VERIFIED", note="This records HONOR's stated technology and test claim without implying guaranteed damage prevention or substituting a third-party rating."),
        field("chipset", launch, "Qualcomm Snapdragon 6 Gen 1", "Qualcomm Snapdragon 6 Gen 1", key="chipset", note="Philippine launch report and HONOR model specification identify this chipset."),
        field("process_node", qualcomm, "4 nm", 4, unit="nm", status="VERIFIED", note="Qualcomm identifies Snapdragon 6 Gen 1 as a 4 nm platform; local and manufacturer sources match the X9c to this chipset."),
        field("cpu", official, "Octa-core: 4 × Cortex-A78 up to 2.2 GHz + 4 × Cortex-A55 up to 1.8 GHz", "Octa-core: 4x A78 up to 2.2 GHz + 4x A55 up to 1.8 GHz", key="cpu", status="VERIFIED", note="HONOR's model-specific specification."),
        field("gpu", official, "Adreno A710", "Adreno A710", key="gpu", status="VERIFIED", note="HONOR's model-specific specification."),
        field("operating_system", official, "MagicOS 8.0 based on Android 14", "MagicOS 8.0 (Android 14)", key="os", status="VERIFIED", note="Software version at the Philippine launch; later update status is not inferred."),
        field("os_support", launch, "No official Philippine OS/security update duration established in the reviewed sources", None, status="PENDING_VERIFICATION", note="A support-duration policy was not found in this research pass; no update count or support end date is inferred."),
        field("ram_capacity", ptg, "12 GB physical RAM; HONOR RAM Turbo adds up to 12 GB virtual extension", 12, key="ramGb", unit="GB", note="Only the 12 GB physical RAM is counted. Virtual RAM is not added to the hardware capacity."),
        field("ram_type", official, "RAM technology not specified in reviewed manufacturer and Philippine sources", None, status="NOT_DISCLOSED", note="The sources state capacity but not LPDDR generation."),
        field("storage_capacity", ptg, "256 GB internal storage for the reported Philippine 12 GB configuration", 256, key="storageGb", unit="GB", note="PTG and the exact local retailer product page identify 256 GB. Although YugaTech mentions 512 GB in a general spec list, no matching Philippine 512 GB stock/SKU was established."),
        field("storage_type", official, "Storage technology not stated in the reviewed model specifications", None, status="NOT_DISCLOSED", note="No storage bus/type is recorded."),
        field("storage_expansion", octagon, "Card slot: No", "No microSD card slot", status="VERIFIED_SECONDARY", note="Octagon's exact local 12 GB / 256 GB product listing specifies no card slot."),
        field("rear_camera_system", official, "108 MP f/1.75 main with OIS and EIS + 5 MP f/2.2 wide/ultra-wide", "108 MP main with OIS/EIS + 5 MP ultra-wide", status="VERIFIED", note="HONOR's model specification and Philippine launch report list a two-camera rear system; there is no macro module in the reported system."),
        field("main_camera_sensor", ph_product, "108 MP main camera; 1/1.67-inch sensor size; sensor manufacturer/model not named", None, status="NOT_DISCLOSED", note="The physical sensor supplier/model is not recorded. Sensor format is not used to infer a model number."),
        field("ultrawide_camera", official, "5 MP f/2.2 wide camera", "5 MP ultra-wide", note="The second rear module is described as wide/ultra-wide; a dedicated depth or macro camera is not listed."),
        field("telephoto_camera", official, "No telephoto camera in the manufacturer-listed dual rear camera system", "No telephoto module listed", status="NOT_APPLICABLE", note="HONOR's exact model specification enumerates only the main and wide rear modules."),
        field("front_camera", official, "16 MP f/2.45", 16, key="frontCameraMp", unit="MP", status="VERIFIED", note="HONOR's model-specific specification and Philippine review sources agree."),
        field("video_recording", official, "Rear video up to 4K; front video up to 1080p", "Rear up to 4K; front up to 1080p", note="HONOR's model-specific camera specification lists these recording ceilings; frame rate for all modes is not promoted here."),
        field("battery_capacity", ph_product, "6600 mAh silicon-carbon battery", 6600, key="batteryMah", unit="mAh", status="VERIFIED", note="HONOR Philippines product information and Philippine launch reports agree."),
        field("battery_technology", ph_product, "Silicon-carbon", "Silicon-carbon", status="VERIFIED", note="HONOR Philippines explicitly describes the battery as silicon-carbon."),
        field("wired_charging", ph_product, "66 W HONOR SuperCharge", 66, key="chargingW", unit="W", status="VERIFIED", note="HONOR Philippines states 66 W wired charging; actual power can vary with charger and operating conditions."),
        field("wireless_charging", official, "Wireless charging not listed in reviewed X9c model specifications", None, status="NOT_DISCLOSED", note="No wireless or reverse charging capability is claimed in the reviewed manufacturer pages."),
        field("dimensions", official, "162.8 × 75.5 × 7.98 mm", "162.8 x 75.5 x 7.98 mm", key="dimensions", unit="mm", status="VERIFIED", note="HONOR's model-specific dimensions; measurements can vary slightly by configuration and process."),
        field("weight", ph_product, "189 g", 189, key="weightG", unit="g", status="VERIFIED", note="HONOR Philippines lists 189 g; the manufacturer includes a caveat for configuration and measurement variation."),
        field("materials", revu, "REVU's Jade Cyan review unit has a polycarbonate laminate rear; manufacturer marketing calls the design titanium-finish but does not identify it as titanium metal", "Jade Cyan review unit: polycarbonate laminate rear; frame material not established", status="VERIFIED_SECONDARY", note="This is the reviewer's color-specific observation, not generalized to every color or a material claim about the frame."),
        field("ingress_protection", ph_product, "HONOR Philippines: IP65M; YugaTech launch: IP65", None, status="CONFLICTING_INFORMATION", note="The manufacturer product page and local launch report use different rating strings. Both source claims are retained; no IP value is promoted to the catalog pending clarification."),
        field("sim_esim", official, "Dual Nano-SIM; eSIM not listed", "Dual Nano-SIM; eSIM not recorded", status="VERIFIED", note="HONOR's model-specific specs and local launch report identify dual Nano-SIM; eSIM support is not stated."),
        field("cellular_bands", launch, "5G and 4G LTE; exact Philippine frequency bands not listed", "5G and 4G LTE; specific bands not recorded", key="cellular", note="The local report lists network generations but no exact Philippine band mapping."),
        field("wifi", official, "Wi-Fi 5, 802.11 a/b/g/n/ac; dual band", "Wi-Fi 5 (802.11 a/b/g/n/ac), dual band", key="wifi", status="VERIFIED", note="HONOR's model-specific specification and launch reporting agree."),
        field("bluetooth", official, "Bluetooth 5.1", "Bluetooth 5.1", status="VERIFIED", note="HONOR's model-specific specification."),
        field("usb", official, "USB Type-C, USB 2.0", "USB Type-C, USB 2.0", key="ports", status="VERIFIED", note="HONOR's model-specific spec and local launch reporting identify USB-C 2.0."),
        field("nfc", official, "NFC", "Yes", status="VERIFIED", note="HONOR's model-specific spec and the exact local retailer specification identify NFC support."),
        field("gnss", official, "GPS, A-GPS, GLONASS, BeiDou, Galileo", "GPS, A-GPS, GLONASS, BeiDou, Galileo", status="VERIFIED", note="HONOR's model-specific positioning specification."),
        field("audio", official, "Dual stereo speakers; no 3.5 mm audio jack", "Dual stereo speakers; no 3.5 mm jack", status="VERIFIED", note="HONOR Philippines confirms dual stereo speakers; the exact local retailer spec says no analog audio jack. USB-C audio output is not assumed unless a source names it."),
        field("sensors", official, "Under-display fingerprint sensor, accelerometer/gravity, gyroscope, proximity, compass, ambient light", "Under-display fingerprint; gravity/accelerometer; gyroscope; proximity; compass; ambient light", status="VERIFIED", note="HONOR's model-specific sensor list; no additional sensor is inferred."),
    ]

    review = {
        "deviceId": DEVICE, "configurationId": CONFIG,
        "brand": "HONOR", "model": "X9c",
        "configuration": "12 GB physical RAM / 256 GB storage",
        "configurationLabel": "12 GB RAM / 256 GB storage",
        "sources": sources, "fields": fields,
        "replacementVariants": [{
            "id": CONFIG, "label": "12 GB RAM / 256 GB storage",
            "sku": None, "modelCode": "BRP-NX1",
            "notes": "The 12 GB / 256 GB configuration is established by Philippine preorder reporting, independent local reviews, HONOR support, and an exact Philippine retailer listing. YugaTech's general spec page also mentions 512 GB storage, but no exact 512 GB local sales SKU/offer was verified, so no second Philippine variant is created. HONOR RAM Turbo is virtual memory, not additional physical RAM.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine preorders were reported starting January 10, 2025; current stock is not established.",
            "philippineAvailability": "PTG reported preorders through HONOR stores, kiosks, and official online shops on January 10, 2025; YugaTech reported official online purchase availability January 11, 2025.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "X Series",
            "philippineReleaseYear": 2025,
            "philippineDateLabel": "First reported Philippine preorder date",
            "researchNotes": "The workbook label HONOR X9c matches HONOR's Philippine X9c 5G product, not the separately marketed X9c Smart. The local configuration established by preorder sources and retailer listing is 12 GB physical RAM / 256 GB storage. PHP 16,999 is the launch SRP; the exact-configuration Octagon listing still shows PHP 16,999 but was out of stock at review time. Current availability is not verified. A general YugaTech specification list mentions 512 GB, but no local 512 GB configuration was confirmed.",
            "qualityFlag": "Current stock unverified; IP rating and brightness qualifiers conflict across sources",
            "openIssues": [
                {"issue": "Retailer price observation is out of stock", "action": "Keep public purchasable price blank and retain the out-of-stock listing only as a dated observation."},
                {"issue": "YugaTech lists 512 GB storage generally, but no exact local 512 GB sale listing was found", "action": "Do not add the 512 GB Philippine variant unless an exact local configuration and offer are verified."},
                {"issue": "Manufacturer uses IP65M while YugaTech launch report says IP65", "action": "Preserve both labels and leave the catalog IP field unresolved until the rating nomenclature is confirmed."},
                {"issue": "HONOR labels 4000 nits typical brightness; local sources call it peak/HDR", "action": "Keep brightness value unresolved until the measurement qualifier is reconciled."},
                {"issue": "No official software support duration found", "action": "Keep OS/security update support period blank."},
                {"issue": "Official product image reuse rights are not established", "action": "Continue showing the neutral placeholder until written permission or a reusable license is documented."},
            ],
        },
    }

    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR X9c Jade Cyan image was identified on the official HONOR Philippines specifications page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_HONOR_SPECS,
        "assetUrl": IMAGE_URL,
        "scope": "Exact HONOR X9c model, Jade Cyan colorway; the 12 GB / 256 GB configuration is not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR X9c",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "X9c", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [
            {
                "device_id": DEVICE, "amount_php": 16999,
                "configuration_id": CONFIG, "configuration_match": "exact",
                "variant_ram_gb": 12, "variant_storage_gb": 256,
                "price_type": "retailer_listed_price_out_of_stock",
                "source_published_at": None,
                "excerpt": "Octagon's exact HONOR X9c 12GB/256GB Jade Cyan listing showed PHP 16,999 at access on 2026-11-26 and was marked Out of stock. It is not an available offer and is not loaded as the catalog price.",
                "source_url": URL_OCTAGON, "source_kind": "retailer_price_observation",
                "observed_at": OBSERVED_AT, "local_availability_verified": False,
                "availability_status": "out_of_stock",
            },
            {
                "device_id": DEVICE, "amount_php": 16999,
                "configuration_id": CONFIG, "configuration_match": "exact",
                "variant_ram_gb": 12, "variant_storage_gb": 256,
                "price_type": "independent_current_price_guide_candidate",
                "source_published_at": "2026-11-16",
                "excerpt": "Best Tech Asia's Philippine guide updated 2026-11-16 lists the 12GB/256GB HONOR X9c 5G at PHP 16,999 and links to official stores, but does not establish live stock or checkout price.",
                "source_url": URL_BESTTECH, "source_kind": "independent_price_guide",
                "observed_at": OBSERVED_AT, "local_availability_verified": False,
                "availability_status": "candidate_current_price_stock_unverified",
            },
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "HONOR X9c inventory record matched to HONOR X9c 5G Philippine launch and retailer sources; X9c Smart kept distinct",
        "configuration": "12 GB / 256 GB",
        "reviewedFields": len(fields),
        "preorderStart": "2025-01-10",
        "historicalLaunchPricePhp": 16999,
        "currentListedPricePhp": 16999,
        "currentStock": "Octagon listing out of stock; no purchasable offer set",
        "no512GbVariantAdded": True,
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
