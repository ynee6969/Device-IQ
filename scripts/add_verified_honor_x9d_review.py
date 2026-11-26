#!/usr/bin/env python3
"""Record the source-matched Philippine HONOR X9d 5G device review."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-x9d-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_efb3b8a0ab65ed"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-12gb-256gb-ph"

URL_HONOR = "https://www.honor.com/ph/phones/honor-x9d/"
URL_HONOR_SPECS = "https://www.honor.com/ph/phones/honor-x9d/spec/"
URL_HONOR_AE_SPECS = "https://www.honor.com/ae-en/phones/honor-x9d/spec/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/6-series/snapdragon-6-gen-4-mobile-platform"
URL_GADGETMATCH = "https://www.gadgetmatch.com/honor-x9d-5g-launches-in-the-philippines-price-preorder-availability/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/honor-x9d-5g"
URL_YUGA = "https://www.yugatech.com/news/honor-x9d-5g-now-official-specs-and-price-in-the-philippines/"
URL_BESTTECH = "https://besttechasia.com/honor-price-list-philippines/"
URL_BESTTECH_DEVICE = "https://besttechasia.com/honor-x9d-5g-full-specs-price-philippines/"
URL_JI = "https://jitelecom.store/product/honor-x9d-5g-12-256/"
IMAGE_URL = "https://www-file.honor.com/content/dam/honor/common/product-list/product-series/honor-x9d/honor-x9d-red-back.png"


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
            or device.get("model") != "X9d"):
        raise ValueError("The inventory record no longer matches the HONOR X9d model identity")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR X9d already has a manual review; inspect it before replacing")

    sources = [
        source("honor_x9d_ph_official_product", "HONOR Philippines", URL_HONOR,
               "Official Philippine model identity and model-level display, platform, battery, charging, durability, and color claims",
               "HONOR Philippines identifies HONOR X9d, Snapdragon 6 Gen 4, 4 nm process, 6.79-inch 1.5K OLED up to 120 Hz and 6,000-nit peak brightness, 8,300 mAh silicon-carbon battery, 66 W SuperCharge, and its durability claims. The same page explains that water/dust ratings are laboratory conditions and protection can decrease with wear."),
        source("honor_x9d_ph_official_specs", "HONOR Philippines", URL_HONOR_SPECS,
               "Official PH specifications page and exact Reddish Brown product-image source",
               "The PH specifications page identifies the X9d and the Reddish Brown, Midnight Black, and Sunrise Gold finishes. Its accessible text rendering omits many specification values. The exact Reddish Brown image asset is recorded separately; it is not copied because reuse rights are not stated."),
        source("honor_x9d_ae_official_specs", "HONOR", URL_HONOR_AE_SPECS,
               "Official regional specification cross-check for shared model features",
               "HONOR's regional product specification page identifies the X9d model family and lists battery, wired charging, water/dust rating nomenclature, dual nano-SIM, Wi-Fi 6, Bluetooth 5.2, and connectivity sections. Only features also supported for the Philippine model are carried into this catalog; regional colors and sales details are not used."),
        source("honor_x9d_qualcomm_platform", "Qualcomm", URL_QUALCOMM,
               "Primary source for Snapdragon 6 Gen 4 platform name, clock ceiling, and process node",
               "Qualcomm documents Snapdragon 6 Gen 4, 2.3 GHz CPU clock speed, and 4 nm process technology. Device-specific CPU cluster and GPU model are taken from the exact-model Philippine reference."),
        source("honor_x9d_ph_launch_gadgetmatch", "GadgetMatch", URL_GADGETMATCH,
               "Contemporaneous Philippine launch, local preorder dates, prices, configuration, and feature cross-check",
               "Published 2026-01-09. Reports Philippine preorders from January 9 through January 23 at PHP 17,999, PHP 18,999 from January 24, and one local configuration: 12 GB RAM plus 12 GB virtual expansion / 256 GB storage. Virtual expansion is not counted as physical RAM.",
               "2026-01-09"),
        source("honor_x9d_ph_ptg_specs", "Pinoy Techno Guide", URL_PTG,
               "Detailed Philippine specification reference and local launch-price cross-check",
               "Published 2026-01-09. Identifies a local 12 GB / 256 GB X9d, PHP 18,999 official price, 8,300 mAh battery, 66 W charging, cameras, software, dimensions, weight, and connectivity. Its processor row says Snapdragon 6s Gen 4, which conflicts with HONOR Philippines, Qualcomm, GadgetMatch, and YugaTech identifying Snapdragon 6 Gen 4; that PTG chipset string is retained as a source discrepancy and is not used as the normalized chipset.",
               "2026-01-09", "independent_ph_reference"),
        source("honor_x9d_ph_yugatech_launch", "YugaTech", URL_YUGA,
               "Independent local launch, 12/256 configuration, specification, and historical price cross-check",
               "Published 2026-01-09. Reports a PHP 18,999 SRP, PHP 17,999 preorder offer, Snapdragon 6 Gen 4, Android 15 with MagicOS 9, and local technical specifications. Its TL;DR contains a 2025 typo for the preorder year; the publication date and contemporaneous GadgetMatch and PTG reports establish the 2026 period.",
               "2026-01-09"),
        source("honor_x9d_ph_besttech_price_list", "Best Tech Asia", URL_BESTTECH,
               "Recent Philippine guide-price cross-check",
               "The 2026 guide reports the 12 GB / 256 GB model at PHP 18,999 and says prices were checked 2026-11-25. This is an editorial SRP/guide value, not a live exact-configuration checkout offer.",
               "2026-11-25", "independent_price_guide"),
        source("honor_x9d_ph_besttech_specs", "Best Tech Asia", URL_BESTTECH_DEVICE,
               "Detailed independent Philippine specifications and launch-price cross-check",
               "Updated 2026-11-16. Identifies the 12 GB / 256 GB Philippine model and PHP 18,999 SRP. The page directs buyers to official marketplace stores but does not establish a live, in-stock checkout price.",
               "2026-11-16", "independent_specification_database"),
        source("honor_x9d_ph_jitelecom_listing", "JI Telecom", URL_JI,
               "Exact-configuration Philippine retailer price candidate and branch-stock caveat",
               "The indexed product listing identifies HONOR X9d 5G 12 GB / 256 GB at PHP 22,999. It states stock may vary by branch and online checkout is unavailable; this is not evidence of a purchasable current offer.",
               source_kind="retailer_price_observation"),
    ]
    official = "honor_x9d_ph_official_product"
    official_specs = "honor_x9d_ph_official_specs"
    regional = "honor_x9d_ae_official_specs"
    qualcomm = "honor_x9d_qualcomm_platform"
    local = "honor_x9d_ph_launch_gadgetmatch"
    ptg = "honor_x9d_ph_ptg_specs"
    yuga = "honor_x9d_ph_yugatech_launch"
    ji = "honor_x9d_ph_jitelecom_listing"

    fields = [
        field("model_number", official_specs, "No model code is exposed on the reviewed HONOR Philippines product/specification pages or local launch reports", None, status="NOT_DISCLOSED", note="Do not infer a regional model code or retailer SKU for the Philippine unit."),
        field("configuration", local, "12 GB RAM (plus 12 GB virtual RAM expansion) / 256 GB storage; reported as the lone Philippine configuration", "12 GB physical RAM / 256 GB storage", status="VERIFIED_SECONDARY", note="GadgetMatch explicitly describes the lone Philippine configuration; PTG and YugaTech independently list 12/256. Virtual RAM is not added to physical memory."),
        field("philippine_release_date", local, "Philippine preorders opened January 9, 2026; reported at launch on January 9", "2026-01-09", status="VERIFIED_SECONDARY", note="First reviewed contemporaneous Philippine preorder date; it is not asserted as the first retail transaction date."),
        field("official_launch_price_php", local, "PHP 18,999 from January 24, 2026; preorder price PHP 17,999 from January 9 to 23", 18999, unit="PHP", status="VERIFIED_SECONDARY", note="Historical Philippine SRP; the lower preorder promotion is retained in the source note and price history, not treated as the standard launch SRP."),
        field("current_price_php", ji, "PHP 22,999 indexed for 12 GB / 256 GB; retailer says stock varies by branch and online checkout is unavailable", None, status="PENDING_VERIFICATION", unit="PHP", note="No current purchasable exact-configuration offer was established. Keep the catalog price blank; retain retailer and guide values as dated candidates."),
        field("display_size", official, "6.79 inches", 6.79, key="displayInches", unit="in", status="VERIFIED", note="HONOR Philippines product page identifies a 6.79-inch OLED display."),
        field("display_technology", official, "HONOR describes the panel as OLED; local launch sources call it AMOLED", "AMOLED", key="displayType", status="VERIFIED_SECONDARY", note="HONOR confirms an OLED panel and contemporaneous Philippine sources identify it as AMOLED, a specific OLED panel type."),
        field("display_resolution", ptg, "2640 × 1200 pixels (1.5K / FHD+ wording varies by source)", "2640 x 1200", key="resolution", status="VERIFIED_SECONDARY", note="PTG provides the pixel dimensions; HONOR PH and GadgetMatch describe the panel as 1.5K. The numeric dimensions are kept separate from marketing resolution labels."),
        field("display_refresh_rate", official, "Up to 120 Hz adaptive refresh rate", 120, key="refreshHz", unit="Hz", status="VERIFIED", note="HONOR Philippines lists an adaptive refresh rate up to 120 Hz."),
        field("display_brightness", official, "6,000 nits peak; PTG additionally lists 800 nits typical and 1,800 nits HBM", "6000 nits peak; 1800 nits HBM; 800 nits typical (PTG)", status="VERIFIED_SECONDARY", unit="nits", note="Only the clearly labeled peak figure is treated as the headline maximum; typical and HBM conditions are preserved separately from peak brightness."),
        field("display_protection", ptg, "Aluminosilicate glass", "Aluminosilicate glass", status="VERIFIED_SECONDARY", note="Reported in the Philippine specification listing and launch coverage."),
        field("chipset", official, "Snapdragon 6 Gen 4; PTG's table says Snapdragon 6s Gen 4", "Qualcomm Snapdragon 6 Gen 4", key="chipset", status="VERIFIED", note="HONOR Philippines, Qualcomm's platform documentation, GadgetMatch, and YugaTech identify Snapdragon 6 Gen 4. PTG alone lists '6s Gen 4'; that source discrepancy is noted and not normalized as the model chipset."),
        field("process_node", qualcomm, "4 nm", 4, unit="nm", status="VERIFIED", note="Qualcomm lists the Snapdragon 6 Gen 4 as a 4 nm platform; HONOR Philippines identifies that platform in the X9d."),
        field("cpu", ptg, "Octa-core: 1 × Cortex-A720 up to 2.3 GHz + 3 × Cortex-A720 up to 2.2 GHz + 4 × Cortex-A520 up to 1.8 GHz", "Octa-core: 1x Cortex-A720 up to 2.3 GHz + 3x Cortex-A720 up to 2.2 GHz + 4x Cortex-A520 up to 1.8 GHz", key="cpu", status="VERIFIED_SECONDARY", note="PTG lists the device-level core layout; Qualcomm independently gives the platform's maximum CPU clock as 2.3 GHz."),
        field("gpu", ptg, "Adreno 810", "Adreno 810", key="gpu", status="VERIFIED_SECONDARY", note="Device-level GPU model reported in PTG's Philippine model specification."),
        field("operating_system", ptg, "Android 15 with MagicOS 9.0 at launch", "MagicOS 9.0 (Android 15)", key="os", status="VERIFIED_SECONDARY", note="Launch-era software version; later upgrade status is not inferred."),
        field("os_support", official_specs, "No official Philippine OS/security update duration found in reviewed sources", None, status="PENDING_VERIFICATION", note="No update count, end date, or support promise is inferred."),
        field("ram_capacity", local, "12 GB physical RAM plus up to 12 GB virtual expansion", 12, key="ramGb", unit="GB", status="VERIFIED_SECONDARY", note="Only the physical 12 GB is recorded as RAM capacity."),
        field("ram_type", official_specs, "RAM generation/type not stated in reviewed sources", None, status="NOT_DISCLOSED", note="No LPDDR type is inferred."),
        field("storage_capacity", local, "256 GB for the sole reported Philippine configuration", 256, key="storageGb", unit="GB", status="VERIFIED_SECONDARY", note="The contemporaneous local launch report identifies 256 GB; no second Philippine storage configuration was established."),
        field("storage_type", official_specs, "Storage interface/type not stated in reviewed sources", None, status="NOT_DISCLOSED", note="No UFS generation is inferred."),
        field("storage_expansion", ptg, "Expansion: None", "No microSD expansion listed", status="VERIFIED_SECONDARY", note="PTG's exact-model specification lists no storage expansion."),
        field("rear_camera_system", ptg, "Dual rear cameras: 108 MP f/1.75 main with autofocus and OIS + 5 MP f/2.2 ultrawide; LED flash", "108 MP f/1.75 main with AF/OIS + 5 MP f/2.2 ultrawide", status="VERIFIED_SECONDARY", note="Local X9d specification and launch sources identify the same two-camera layout; no depth/macro lens is added."),
        field("main_camera_sensor", ptg, "108 MP f/1.75 main camera with autofocus and OIS; sensor manufacturer/model not stated", None, status="NOT_DISCLOSED", note="The sensor supplier/model remains unrecorded; the camera resolution and OIS are captured in the rear-camera field."),
        field("ultrawide_camera", ptg, "5 MP f/2.2 ultrawide", "5 MP f/2.2 ultrawide", status="VERIFIED_SECONDARY", note="Reported for the local model in PTG's specification table."),
        field("telephoto_camera", ptg, "No telephoto module listed in the dual-rear-camera specification", "No telephoto camera listed", status="NOT_APPLICABLE", note="The listed rear system contains main and ultrawide cameras only."),
        field("front_camera", ptg, "16 MP f/2.45", 16, key="frontCameraMp", unit="MP", status="VERIFIED_SECONDARY", note="PTG and local launch coverage identify a 16 MP front camera."),
        field("video_recording", ptg, "Rear: up to 4K at 30 fps or 1080p at 60 fps; front: up to 1080p at 30 fps", "Rear up to 4K/30 or 1080p/60; front up to 1080p/30", status="VERIFIED_SECONDARY", note="Recording modes from the Philippine model specification listing."),
        field("battery_capacity", official, "8,300 mAh typical capacity", 8300, key="batteryMah", unit="mAh", status="VERIFIED", note="HONOR Philippines lists 8,300 mAh; a typical-value qualifier is available in official regional specifications."),
        field("battery_technology", official, "Silicon-carbon battery", "Silicon-carbon", status="VERIFIED", note="HONOR Philippines explicitly describes the battery as silicon-carbon."),
        field("wired_charging", official, "66 W HONOR SuperCharge; actual charging power varies by scenario", 66, key="chargingW", unit="W", status="VERIFIED", note="HONOR Philippines lists 66 W and qualifies actual charging power by scenario."),
        field("wireless_charging", official_specs, "No wireless charging specification found in reviewed sources", None, status="NOT_DISCLOSED", note="No wireless charging capability is inferred."),
        field("dimensions", ptg, "161.9 × 76.1 × 7.76 mm", "161.9 x 76.1 x 7.76 mm", key="dimensions", unit="mm", status="VERIFIED_SECONDARY", note="Local model-specific dimensions; order is height × width × thickness."),
        field("weight", ptg, "193 g", 193, key="weightG", unit="g", status="VERIFIED_SECONDARY", note="Local model-specific weight listing."),
        field("materials", ptg, "Glass front, polycarbonate back", "Glass front; polycarbonate rear", status="VERIFIED_SECONDARY", note="PTG identifies the front and rear materials; color-specific finish differences are not inferred."),
        field("ingress_protection", official, "HONOR states IP69K under ISO 20653:2023 and IP66, IP68, IP69 under IEC 60529; these are controlled laboratory ratings", "IP66, IP68, IP69 (IEC 60529); IP69K (ISO 20653:2023)", status="VERIFIED", note="The official PH page explains the separate standards and warns that protection can decrease through wear. This records the ratings without implying permanent or unrestricted waterproofing."),
        field("sim_esim", ptg, "Dual SIM (Nano-SIM); eSIM support not stated", "Dual Nano-SIM; eSIM not recorded", status="VERIFIED_SECONDARY", note="Only the two physical Nano-SIM slots are recorded; absence of eSIM is not inferred."),
        field("cellular_bands", regional, "5G NR, 4G LTE, 3G WCDMA, and 2G GSM; exact Philippine band list not recorded", "5G NR / 4G LTE / 3G WCDMA / 2G GSM; band list not recorded", key="cellular", status="VERIFIED_SECONDARY", note="Network generations are reported for the model. No individual band coverage or carrier compatibility is inferred."),
        field("wifi", ptg, "Dual-band Wi-Fi 802.11 a/b/g/n/ac/ax (Wi-Fi 6)", "Wi-Fi 6 (802.11 a/b/g/n/ac/ax), dual band", key="wifi", status="VERIFIED_SECONDARY", note="PTG lists Wi-Fi 6 for the handset. Qualcomm platform capabilities are not substituted for the model-specific listing."),
        field("bluetooth", regional, "Bluetooth 5.2", "Bluetooth 5.2", status="VERIFIED", note="HONOR's official regional model specification lists BT 5.2; the local reference agrees."),
        field("usb", ptg, "USB Type-C; USB version/protocol not stated", "USB Type-C; protocol not recorded", key="ports", status="VERIFIED_SECONDARY", note="The connector is identified; transfer speed/version is left unrecorded."),
        field("nfc", ptg, "NFC: Yes", "NFC", status="VERIFIED_SECONDARY", note="NFC is listed for the Philippine X9d model."),
        field("gnss", ptg, "GPS, GLONASS, Galileo, BeiDou", "GPS, GLONASS, Galileo, BeiDou", status="VERIFIED_SECONDARY", note="Positioning systems listed in the local specification reference."),
        field("audio", ptg, "Dual speakers; USB Type-C audio output; FM radio: No", "Dual speakers; USB-C audio output; no FM radio listed", status="VERIFIED_SECONDARY", note="Audio details are from PTG's exact-model Philippine specification listing."),
        field("sensors", ptg, "Gyroscope, compass, ambient-light sensor, proximity sensor, accelerometer; optical under-display fingerprint reader", "Gyroscope, compass, ambient light, proximity, accelerometer; optical under-display fingerprint", status="VERIFIED_SECONDARY", note="Sensor and biometric details are transcribed from the local specification reference."),
    ]

    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "HONOR",
        "model": "X9d",
        "configuration": "12 GB physical RAM / 256 GB storage",
        "configurationLabel": "12 GB RAM / 256 GB storage",
        "replacementVariants": [{
            "id": CONFIG, "label": "12 GB RAM / 256 GB storage",
            "sku": None, "modelCode": None,
            "notes": "GadgetMatch describes this as the lone Philippine configuration; PTG and YugaTech also identify the local 12 GB / 256 GB version. The additional 12 GB HONOR RAM expansion is virtual and is not counted as physical RAM. Three Philippine launch colors are finishes, not distinct memory configurations. Global-region colors and any 512 GB option are not added without an exact Philippine SKU/offer.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "sources": sources,
        "fields": fields,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine preorder availability was reported from January 9, 2026; current stock is not established.",
            "philippineAvailability": "GadgetMatch reported Philippine preorders January 9–23, 2026 and standard pricing from January 24; PTG lists the Philippine model and local official-store links.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "X Series",
            "philippineReleaseYear": 2026,
            "philippineDateLabel": "First reported Philippine preorder date",
            "researchNotes": "The workbook's HONOR X9d record matches the Philippine-market X9d 5G. Local launch reporting identifies one 12 GB physical RAM / 256 GB storage configuration. The historical Philippine SRP is PHP 18,999; PHP 17,999 was the January preorder offer. No current in-stock checkout offer is confirmed. The PTG chipset row says Snapdragon 6s Gen 4, while HONOR Philippines, Qualcomm, GadgetMatch, and YugaTech identify Snapdragon 6 Gen 4; the manufacturer-supported name is used, with the discrepancy documented. The catalog's image remains the neutral placeholder because image reuse rights were not established.",
            "qualityFlag": "Current price and stock unverified; PTG chipset entry conflicts with HONOR and other launch sources",
            "openIssues": [
                {"issue": "No current purchasable exact-configuration retailer offer verified", "action": "Keep the catalog price blank; preserve retailer and guide prices only as dated candidates."},
                {"issue": "PTG lists Snapdragon 6s Gen 4 while HONOR PH, Qualcomm, GadgetMatch, and YugaTech list Snapdragon 6 Gen 4", "action": "Use the manufacturer-supported Snapdragon 6 Gen 4 name and retain the conflicting PTG text in source metadata."},
                {"issue": "Official image reuse terms are not stated", "action": "Continue showing the neutral placeholder until a reusable license or written permission is documented."},
                {"issue": "Official software-support duration was not found", "action": "Leave OS/security update duration unrecorded."},
            ],
        },
    }

    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR X9d Reddish Brown product image was identified on the official HONOR Philippines specifications page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_HONOR_SPECS,
        "assetUrl": IMAGE_URL,
        "scope": "Exact HONOR X9d model, Reddish Brown finish; image does not distinguish the 12 GB / 256 GB configuration",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR X9d 5G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "X9d", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [
            {
                "device_id": DEVICE, "amount_php": 22999,
                "configuration_id": CONFIG, "configuration_match": "exact",
                "variant_ram_gb": 12, "variant_storage_gb": 256,
                "price_type": "retailer_listed_price_stock_varies_by_branch_checkout_unavailable",
                "source_published_at": None,
                "excerpt": "JI Telecom's exact 12GB/256GB X9d listing shows PHP 22,999, but states stock varies by branch and online checkout is unavailable. Treat as a retailer price candidate, not an available offer.",
                "source_url": URL_JI, "source_kind": "retailer_price_observation",
                "observed_at": OBSERVED_AT, "local_availability_verified": False,
                "availability_status": "branch_stock_unconfirmed_online_checkout_unavailable",
            },
            {
                "device_id": DEVICE, "amount_php": 18999,
                "configuration_id": CONFIG, "configuration_match": "exact",
                "variant_ram_gb": 12, "variant_storage_gb": 256,
                "price_type": "independent_current_price_guide_candidate",
                "source_published_at": "2026-11-25",
                "excerpt": "Best Tech Asia's Philippines price list says it verified PHP 18,999 for HONOR X9d 12GB/256GB on 2026-11-25; this is an editorial guide/SRP, not a live in-stock exact-configuration checkout offer.",
                "source_url": URL_BESTTECH, "source_kind": "independent_price_guide",
                "observed_at": OBSERVED_AT, "local_availability_verified": False,
                "availability_status": "guide_price_candidate_no_live_checkout",
            },
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "HONOR X9d inventory record matched to HONOR Philippines X9d 5G and local launch coverage",
        "configuration": "12 GB physical RAM / 256 GB storage",
        "reviewedFields": len(fields),
        "preorderStart": "2026-01-09",
        "historicalLaunchPricePhp": 18999,
        "preorderPricePhp": 17999,
        "currentPublicPricePhp": None,
        "currentStock": "unverified; JI Telecom states branch stock varies and checkout is unavailable",
        "chipsetSourceConflict": "PTG lists 6s Gen 4; HONOR PH, Qualcomm, GadgetMatch and YugaTech identify 6 Gen 4",
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
