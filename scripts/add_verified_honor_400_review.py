#!/usr/bin/env python3
"""Record the exact Philippine HONOR 400 5G configuration and source conflicts."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-400-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_32de18b7c0de7e"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-12gb-512gb-ph"

URL_HONOR = "https://www.honor.com/ph/phones/honor-400/"
URL_HONOR_SPECS = "https://www.honor.com/ph/phones/honor-400/spec/"
URL_HONOR_REPORT = "https://www.honor.com/content/dam/honor/global/honor-esg/green_environmental_protection/1230pdf/phones/HONOR%20Environmental%20Report-HONOR%20400.pdf"
URL_YUGA = "https://www.yugatech.com/news/honor-400-5g-now-official-priced-specs-in-the-philippines/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/honor-400-5g"
URL_PTG_REVIEW = "https://www.pinoytechnoguide.com/reviews/honor-400-5g"
URL_GUANZON = "https://www.guanzongroup.com.ph/product/honor-400-5g/"
IMAGE_URL = "https://www-file.honor.com/content/dam/honor/common/product-list/product-series/honor-400/honor-400-id-gold-back.png"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None, source_kind: str | None = None) -> dict:
    result = {"id": sid, "publisher": publisher, "url": url,
              "publicationDate": publication_date, "accessDate": OBSERVED,
              "purpose": purpose, "note": note}
    if source_kind:
        result["sourceKind"] = source_kind
    return result


def field(fid: str, source_id: str, value, normalized_value, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, candidate_evidence=None,
          local_availability_verified=None,
          configuration_match="Exact Philippine 12 GB RAM / 512 GB storage configuration") -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": source_id,
           "sourceValue": value, "normalizedValue": normalized_value,
           "note": note, "configurationMatch": configuration_match}
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized_value
    if unit:
        row["unit"] = unit
    if candidate_evidence:
        row["candidateEvidence"] = candidate_evidence
    if local_availability_verified is not None:
        row["localAvailabilityVerified"] = local_availability_verified
    return row


def conflict(value, url, excerpt, *, source_kind="independent_ph_reference", observed_at="2026-11-26",
             configuration_match="Exact HONOR 400 5G model; local storage variant not distinguished"):
    return {"value": value, "unit": None, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": observed_at, "excerpt": excerpt,
            "configurationMatch": configuration_match, "reviewStatus": "CONFLICTING_INFORMATION",
            "localAvailabilityVerified": True}


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device or device.get("category") != "smartphones" or device.get("brand", "").casefold() != "honor" or device.get("model") != "400":
        raise ValueError("The source record no longer matches the HONOR 400 workbook identity")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR 400 already has a manual review; inspect it before replacing")

    sources = [
        source("honor_400_ph_official_product", "HONOR Philippines", URL_HONOR,
               "Official Philippine product identity, battery, display, camera, charging, and durability cross-check",
               "HONOR Philippines identifies the HONOR 400 and publishes 6000 mAh battery, 80 W maximum wired charging, 200 MP + 12 MP rear cameras, 50 MP front camera, 5000-nit peak display, 184 g weight, 7.3 mm thickness, IP66 resistance, and four local colors."),
        source("honor_400_ph_official_specs", "HONOR Philippines", URL_HONOR_SPECS,
               "Official Philippine detailed specifications",
               "The official Philippine HONOR 400 specification page identifies the exact model. Indexed page text lists display resolution, refresh rate, processor, GPU, memory, cameras, battery, cellular and connectivity details; specific values are cited in individual fields."),
        source("honor_400_official_product_report", "HONOR", URL_HONOR_REPORT,
               "Manufacturer environmental report for exact model dimensions and mass",
               "HONOR's product environmental report identifies the HONOR 400 and specifies a 6.55-inch display, 156.5 × 74.6 × 7.3 mm dimensions, and 184 g handset weight."),
        source("honor_400_ph_launch_yugatech", "YugaTech", URL_YUGA,
               "Contemporaneous Philippine launch, preorder window, configuration range, and technical cross-check",
               "Published 2025-06-17. Reports Philippine preorder dates June 18–27, 2025, a PHP 22,999 starting price, and multiple memory configurations. Its article reports 90 W charging and a 165.5 mm height; those two values conflict with HONOR's published 80 W maximum and 156.5 mm height, so the manufacturer values are retained and the conflict is preserved in the field audit.",
               "2025-06-17"),
        source("honor_400_ph_specs_ptg", "Pinoy Techno Guide", URL_PTG,
               "Exact Philippine model, 12 GB / 512 GB configuration, preorder date, price, and full specification cross-check",
               "Published 2025-06-17. The Philippine product entry identifies HONOR 400 5G with 12 GB RAM / 512 GB storage, PHP 22,999 official price, and preorders beginning June 18, 2025. It lists detailed specifications; isolated values that conflict with the manufacturer or PTG hands-on review are retained as candidate evidence.",
               "2025-06-17"),
        source("honor_400_ph_review_ptg", "Pinoy Techno Guide", URL_PTG_REVIEW,
               "Independent hands-on review, local availability, and field-level conflict review",
               "Published 2025-07-12. The review states the device was available through HONOR stores, authorized dealers, and official online stores. It identifies the 12 GB / 512 GB tested configuration and reports 80 W maximum phone charging, 156.7 mm height, and IP65; the height and ingress rating differ slightly from HONOR's official material, and are retained as candidate evidence.",
               "2025-07-12"),
        source("honor_400_current_price_guanzon", "Guanzon Merchandising Corporation", URL_GUANZON,
               "Current Philippine price-reference candidate for the exact 12 GB / 512 GB model",
               "The retailer product page lists HONOR 400 5G 12 GB + 512 GB at PHP 22,999 and explicitly warns that displayed prices are for reference, may vary by branch, and can change. It provides an inquiry button but does not confirm a currently available unit; retain as a price candidate, not a public current price.",
               source_kind="retailer_price_candidate"),
    ]
    honor_id = "honor_400_ph_official_product"
    specs_id = "honor_400_ph_official_specs"
    report_id = "honor_400_official_product_report"
    yuga_id = "honor_400_ph_launch_yugatech"
    ptg_id = "honor_400_ph_specs_ptg"
    review_id = "honor_400_ph_review_ptg"
    guanzon_id = "honor_400_current_price_guanzon"

    evidence_resolution = [conflict("1264 × 2780 pixels", URL_PTG,
                                    "The source's display table gives 1264 × 2780; HONOR's indexed Philippine specification gives 2736 × 1264." )]
    evidence_charging = [conflict("90 W charging support", URL_YUGA,
                                  "YugaTech's launch article states 90 W wired charging and separately lists a 100 W SuperCharge adapter."),
                         conflict("80 W maximum wired charging", URL_PTG_REVIEW,
                                  "PTG's hands-on review says the handset supports up to 80 W; this agrees with HONOR's 80 W maximum.",
                                  observed_at="2025-07-12"),
                         conflict("88 W fast charging", URL_GUANZON,
                                  "Guanzon's product summary says 88 W, while its specification table gives up to 20V/4A (80 W); HONOR's maximum is 80 W.",
                                  source_kind="retailer_product_page")]
    evidence_dimensions = [conflict("156.7 × 74.6 × 7.3 mm", URL_PTG_REVIEW,
                                    "PTG review specifications give 156.7 mm height; HONOR's product report gives 156.5 mm.",
                                    observed_at="2025-07-12"),
                          conflict("165.5 × 74.6 × 7.3 mm", URL_YUGA,
                                   "YugaTech's launch article lists 165.5 mm height; the HONOR environmental report gives 156.5 mm.")]
    evidence_ip = [conflict("IP65", URL_PTG_REVIEW,
                            "PTG hands-on review states IP65; HONOR product page and the PTG product specification list IP66.",
                            observed_at="2025-07-12")]

    fields = [
        field("model_number", yuga_id, "Philippine model code/SKU not listed", None, status="NOT_DISCLOSED", note="The reviewed official product and Philippine launch pages identify the marketing model but do not state the Philippine hardware SKU."),
        field("configuration", ptg_id, "12 GB RAM / 512 GB storage", "12 GB RAM / 512 GB storage", note="PTG's exact Philippine device entry and hands-on review identify the 12 GB / 512 GB configuration; YugaTech also lists 12 GB and 512 GB among the local options."),
        field("philippine_release_date", ptg_id, "Announced June 17, 2025; preorders June 18–27, 2025", "2025-06-18", note="Records the first documented Philippine preorder date, not a separately established first retail-sale date."),
        field("official_launch_price_php", ptg_id, "PHP 22,999 official price, published 2025-06-17", 22999, unit="PHP", note="Historical Philippine launch-era official price associated with the documented 12 GB / 512 GB configuration; not a current offer."),
        field("current_price_php", guanzon_id, "PHP 22,999 retailer price reference for 12 GB / 512 GB; current branch availability is not confirmed", 22999, status="PENDING_VERIFICATION", unit="PHP", local_availability_verified=False, note="A Philippine retailer page lists this exact configuration and price but calls prices reference-only and directs customers to inquire. Keep as a dated candidate until current stock/offer is confirmed."),
        field("display_size", specs_id, "6.55 inches", 6.55, key="displayInches", unit="in", status="VERIFIED", note="HONOR Philippines specification and PTG local product page."),
        field("display_technology", specs_id, "AMOLED", "AMOLED", key="displayType", status="VERIFIED", note="HONOR Philippines specification."),
        field("display_resolution", specs_id, "2736 × 1264 pixels", "2736 x 1264", key="resolution", status="VERIFIED", note="HONOR Philippines indexed specification is used. PTG's product table lists 1264 × 2780; this discrepancy is retained as candidate evidence rather than copied into the catalog.", candidate_evidence=evidence_resolution),
        field("display_refresh_rate", specs_id, "120 Hz", 120, key="refreshHz", unit="Hz", status="VERIFIED", note="HONOR Philippines specification."),
        field("display_brightness", honor_id, "5000 nits HDR peak brightness", 5000, unit="nits", status="VERIFIED", note="HONOR Philippines product page labels 5000 nits as HDR peak brightness."),
        field("display_protection", ptg_id, "Scratch-resistant glass", "Scratch-resistant glass", note="PTG's exact Philippine specification entry."),
        field("chipset", specs_id, "Qualcomm Snapdragon 7 Gen 3", "Qualcomm Snapdragon 7 Gen 3", key="chipset", status="VERIFIED", note="HONOR Philippines specification."),
        field("process_node", ptg_id, "4 nm", 4, unit="nm", note="PTG lists Snapdragon 7 Gen 3 (4 nm) for the Philippine model."),
        field("cpu", ptg_id, "Octa-core: 1 × Cortex-A715 at 2.63 GHz + 3 × Cortex-A715 at 2.4 GHz + 4 × Cortex-A510 at 1.8 GHz", "Octa-core 1+3+4; up to 2.63 GHz", key="cpu", note="PTG's Philippine device page lists the core families and frequencies."),
        field("gpu", specs_id, "Adreno 720", "Adreno 720", key="gpu", status="VERIFIED", note="HONOR Philippines specification."),
        field("operating_system", ptg_id, "Android 15 with MagicOS 9.0", "Android 15 / MagicOS 9.0", key="os", note="Software versions reported for the Philippine product; later update history is not inferred."),
        field("os_support", specs_id, "Published software support policy not listed", None, status="NOT_DISCLOSED", note="No duration or number of Android/security updates is stated in the reviewed official product specification."),
        field("ram_capacity", ptg_id, "12 GB physical RAM", 12, key="ramGb", unit="GB", note="PTG identifies 12 GB physical RAM for its exact Philippine 512 GB product entry."),
        field("ram_type", ptg_id, "RAM type not listed", None, status="NOT_DISCLOSED", note="The reviewed Philippine sources state capacity but do not identify RAM technology or speed."),
        field("storage_capacity", ptg_id, "512 GB", 512, key="storageGb", unit="GB", note="PTG's exact Philippine product entry identifies 512 GB internal storage."),
        field("storage_type", ptg_id, "Storage technology not listed", None, status="NOT_DISCLOSED", note="The reviewed local product sources do not identify the UFS generation."),
        field("storage_expansion", ptg_id, "No expansion listed", "No expansion listed", note="PTG's Philippine device specification lists storage expansion as none."),
        field("rear_camera_system", specs_id, "200 MP main camera with OIS + 12 MP 112° ultra-wide camera", "200 MP main + 12 MP ultra-wide", note="HONOR Philippines identifies the 200 MP main and 12 MP 112° ultra-wide camera system; PTG provides matching resolution and aperture details."),
        field("main_camera_sensor", honor_id, "200 MP main camera; 1/1.4-inch image sensor, sensor model not stated", "1/1.4-inch sensor; model not disclosed", status="VERIFIED", note="HONOR Philippines specifies 1/1.4-inch sensor size but does not name its manufacturer/model."),
        field("ultrawide_camera", ptg_id, "12 MP macro/ultra-wide camera, f/2.2, 112° field of view", "12 MP ultra-wide/macro; 112° FoV", note="PTG lists the local camera module as macro/ultra-wide; this does not establish a separate macro module."),
        field("telephoto_camera", review_id, "The rear camera system has main and ultra-wide modules; no dedicated telephoto camera", "No dedicated telephoto camera", status="NOT_APPLICABLE", note="PTG's hands-on review explicitly states there is no dedicated telephoto camera."),
        field("front_camera", ptg_id, "50 MP f/2.0", 50, key="frontCameraMp", unit="MP", note="PTG's Philippine specifications; also cross-checked against HONOR Philippines product page."),
        field("video_recording", ptg_id, "Rear up to 4K; front up to 4K", "Rear video up to 4K; front video up to 4K", key="video", note="PTG's Philippine specification entry lists up to 4K recording for rear and front cameras."),
        field("battery_capacity", honor_id, "Up to 6000 mAh silicon-carbon battery", 6000, key="batteryMah", unit="mAh", status="VERIFIED", note="HONOR Philippines states up to 6000 mAh; PTG reports a 6000 mAh high-density silicon-carbon battery."),
        field("battery_technology", honor_id, "Silicon-carbon battery; capacity stated as up to 6000 mAh", "Silicon-carbon", status="VERIFIED", note="HONOR Philippines product page identifies the silicon-carbon battery."),
        field("wired_charging", honor_id, "Maximum wired charging power 80 W", 80, key="chargingW", unit="W", status="VERIFIED", note="HONOR Philippines states that the handset supports a maximum 80 W wired charge. PTG review also reports the phone maxes at 80 W. YugaTech's launch article reports 90 W support and a 100 W adapter; that conflict is retained here, while the manufacturer maximum is used for the public value.", candidate_evidence=evidence_charging),
        field("wireless_charging", specs_id, "Wireless charging not listed", None, status="NOT_DISCLOSED", note="No wireless charging capability is stated in the reviewed local product specification."),
        field("dimensions", report_id, "156.5 × 74.6 × 7.3 mm", "156.5 x 74.6 x 7.3 mm", key="dimensions", unit="mm", status="VERIFIED", note="HONOR manufacturer environmental report gives these exact dimensions. PTG review lists 156.7 mm height and YugaTech lists 165.5 mm; both differences are preserved as source evidence, not silently substituted.", candidate_evidence=evidence_dimensions),
        field("weight", report_id, "184 g handset with battery", 184, key="weightG", unit="g", status="VERIFIED", note="HONOR manufacturer environmental report; PTG local page also reports 184 g."),
        field("materials", ptg_id, "Glass front and back; metal frame", "Glass front/back; metal frame", note="PTG's Philippine specification table describes these build materials."),
        field("ingress_protection", honor_id, "IP66 dust and water resistance", "IP66", status="VERIFIED", note="HONOR Philippines states IP66; the PTG local product specification also lists IP66. Its hands-on review separately says IP65, which is retained as conflicting candidate evidence.", candidate_evidence=evidence_ip),
        field("sim_esim", ptg_id, "Dual SIM: Nano-SIM plus eSIM", "Nano-SIM + eSIM", note="PTG's exact Philippine product specification; YugaTech also lists dual Nano-SIM and eSIM."),
        field("cellular_bands", ptg_id, "5G, 4G LTE, 3G HSPA+, 2G EDGE/GPRS; specific bands not listed", "5G, 4G LTE, 3G, 2G; bands not recorded", key="cellular", note="Generations are recorded without inferring exact Philippine band support."),
        field("wifi", ptg_id, "Wi-Fi 802.11 b/g/n/ac/6", "Wi-Fi 6", key="wifi", note="PTG's Philippine specification lists Wi-Fi 6. Exact band details are not recorded."),
        field("bluetooth", ptg_id, "Bluetooth 5.4", "Bluetooth 5.4", note="PTG's Philippine specification."),
        field("usb", ptg_id, "USB Type-C; data generation not listed", "USB Type-C", key="ports", note="PTG's Philippine specifications; data transfer speed is not stated."),
        field("nfc", ptg_id, "NFC support", "Yes", note="PTG's Philippine specification."),
        field("gnss", ptg_id, "GPS, GLONASS, Galileo, BeiDou, QZSS", "GPS, GLONASS, Galileo, BeiDou, QZSS", note="PTG's Philippine specification."),
        field("audio", ptg_id, "Stereo speakers; USB Type-C audio output", "Stereo speakers; USB Type-C audio", note="PTG's Philippine specification."),
        field("sensors", ptg_id, "Gyroscope, compass, ambient-light sensor, proximity sensor, accelerometer", "Gyroscope, compass, ambient light, proximity, accelerometer", note="PTG's Philippine specification; list is retained as published."),
    ]

    review = {
        "deviceId": DEVICE, "configurationId": CONFIG,
        "brand": "HONOR", "model": "400",
        "configuration": "12 GB RAM / 512 GB storage",
        "configurationLabel": "12 GB RAM / 512 GB storage",
        "sources": sources, "fields": fields,
        "replacementVariants": [{
            "id": CONFIG, "label": "12 GB RAM / 512 GB storage",
            "sku": None, "modelCode": None,
            "notes": "PTG identifies the Philippine HONOR 400 5G as 12 GB RAM / 512 GB storage. YugaTech lists multiple memory options but does not map every price/configuration pair. No local SKU is recorded.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine preorders were reported June 18–27, 2025; current stock is not established.",
            "philippineAvailability": "PTG's Philippine product page records preorders from June 18 to June 27, 2025; the 2025-07-12 hands-on review later states that the phone was available at HONOR stores, authorized dealers, and official online stores.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "N Series",
            "philippineReleaseYear": 2025,
            "philippineDateLabel": "Philippine preorder start",
            "researchNotes": "The workbook's HONOR 400 label matches the manufacturer HONOR 400 and Philippine HONOR 400 5G. PTG identifies the 12 GB / 512 GB configuration at PHP 22,999. The value is historical launch-era price evidence; no current retail price is verified. Conflicting YugaTech/PTG secondary specifications are preserved, with manufacturer values used for charging, dimensions, display resolution, and ingress rating where available.",
            "qualityFlag": "Launch price is historical; some secondary specifications conflict",
            "openIssues": [
                {"issue": "Exact Philippine SKU/model code is not recorded", "action": "Leave SKU/model code blank until a source names it."},
                {"issue": "Current retail availability is not verified", "action": "Keep the June 2025 price as historical and the Guanzon reference quote as a separate unverified candidate."},
                {"issue": "Guanzon's 2026 PHP 22,999 price is reference-only and has no confirmed in-stock checkout", "action": "Keep the exact-configuration price in the audit candidate queue; do not expose as a current offer yet."},
                {"issue": "YugaTech reports 90 W charging and 165.5 mm height, while Guanzon's summary says 88 W; HONOR publishes 80 W and 156.5 mm", "action": "Keep manufacturer values in the public catalog and preserve conflicting values in the field audit."},
                {"issue": "PTG's hands-on review lists IP65 and 156.7 mm height, while HONOR and PTG's product table list IP66 and the manufacturer report lists 156.5 mm", "action": "Preserve the review discrepancies as evidence; do not substitute them for manufacturer values."},
                {"issue": "Official image reuse terms are not established", "action": "Continue showing the neutral placeholder until rights are clear."},
            ],
        },
    }

    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR 400 Desert Gold product image was identified on the official HONOR Philippines specification page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_HONOR_SPECS,
        "assetUrl": IMAGE_URL,
        "scope": "Exact HONOR 400 model, Desert Gold color; RAM/storage configuration is not visually distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR 400",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "400", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [{
            "device_id": DEVICE, "amount_php": 22999,
            "configuration_id": CONFIG, "configuration_match": "exact",
            "variant_ram_gb": 12, "variant_storage_gb": 512,
            "price_type": "independent_reported_historical_price",
            "source_published_at": "2025-06-17",
            "excerpt": "PTG's Philippine HONOR 400 5G entry associates the 12 GB RAM / 512 GB configuration with a PHP 22,999 official price and preorders beginning June 18, 2025. Historical, not current.",
            "source_url": URL_PTG, "source_kind": "independent_ph_reference",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
        }, {
            "device_id": DEVICE, "amount_php": 22999,
            "configuration_id": CONFIG, "configuration_match": "exact",
            "variant_ram_gb": 12, "variant_storage_gb": 512,
            "price_type": "retailer_reference_pending_availability",
            "source_published_at": None,
            "excerpt": "Guanzon lists the exact 12 GB + 512 GB HONOR 400 5G configuration at PHP 22,999 but says prices are reference-only and branch-dependent; page does not establish current stock.",
            "source_url": URL_GUANZON, "source_kind": "retailer_price_candidate",
            "observed_at": OBSERVED_AT, "local_availability_verified": False,
            "availability_status": "pending_in_stock_confirmation",
        }],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "HONOR 400 inventory record matched to HONOR 400 5G Philippine product",
        "configuration": "12 GB / 512 GB",
        "reviewedFields": len(fields),
        "preorderStart": "2025-06-18",
        "historicalPricePhp": 22999,
        "priceLoadedAsCurrent": False,
        "conflictsPreserved": ["display_resolution", "wired_charging", "dimensions", "ingress_protection"],
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
