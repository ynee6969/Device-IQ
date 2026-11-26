#!/usr/bin/env python3
"""Record the source-matched Philippine HONOR Play20A device review."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/honor-play20a-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_111b3317778f61"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-4gb-64gb-ph"

URL_HONOR_GLOBAL = "https://www.honor.com/global/phones/honor-play20-a/"
URL_HONOR_IMAGE_PAGE = "https://www.honor.com/global/phones/honor-play20-a/"
URL_HONOR_IMAGE = "https://www.honor.com/content/dam/honor/common/product-list/product-series/honor-play20-a/honor-play20-a-blue-list.png"
URL_MEDIA_TEK = "https://www.mediatek.com/products/smartphones/mediatek-helio-g81"
URL_NANOREVIEW = "https://nanoreview.net/en/soc/mediatek-helio-g81"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/honor-play20a"
URL_JAM_LAUNCH = "https://jamonline.ph/tech-news/honor-play-20a-philippines-price-specs-promo/"
URL_JAM_AVAIL = "https://jamonline.ph/tech-news/honor-play-20a-pad-x7b-philippines-price/"
URL_NOYPI = "https://www.noypigeeks.com/android/honor-play-20a-philippines/"
URL_REVU = "https://www.revu.com.ph/2026/11/honor-play-20a-review-price-specs/"
URL_BESTTECH = "https://besttechasia.com/honor-play20a-full-specs-price-philippines/"
URL_IWAREHOUSE = "https://iwarehouse.ph/products/3134-honor-play-20a"
URL_PHILNEWS = "https://philnews.ph/2026/11/11/honor-play-20a-2026-full-specs-features-price-in-philippines/"


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
          configuration_match="Philippine 4 GB physical RAM / 64 GB storage configuration") -> dict:
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
            or device.get("model") != "Play 20A"):
        raise ValueError("The inventory record no longer matches the 2026 HONOR Play 20A model identity")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("HONOR Play 20A already has a manual review; inspect it before replacing")

    sources = [
        source("honor_play20a_global_official_product", "HONOR Global", URL_HONOR_GLOBAL,
               "Manufacturer model identity and shared rear-screen, battery, display, storage expansion, color, and chipset features",
               "HONOR Global identifies the 2026 HONOR Play20A, the 2-inch Smart Rear Screen, 6.9-inch main display, 90 Hz, MediaTek G81, 6,000 mAh typical / 5,850 mAh rated battery, and a three-card slot. This global marketing page mentions 128 GB storage and is not used to infer a Philippine memory variant."),
        source("honor_play20a_global_image", "HONOR Global", URL_HONOR_IMAGE_PAGE,
               "Exact-model official image source page and Reddish/Light Blue product image provenance",
               "The manufacturer product page displays the Play20A in its official finishes. The linked Light Blue product-list image is recorded separately; reuse rights are not stated, so it is not copied into the site."),
        source("mediatek_helio_g81_official", "MediaTek", URL_MEDIA_TEK,
               "Primary source for Helio G81 CPU/GPU/platform feature cross-check",
               "MediaTek's official G81 page documents the octa-core Cortex-A75/A55 CPU, Mali-G52 MC2 GPU, Wi-Fi 5, Bluetooth capabilities, FM radio capability, and positioning support. The handset's own feature list is still used for device-level values."),
        source("nanoreview_helio_g81", "NanoReview", URL_NANOREVIEW,
               "Independent technical source for Helio G81 process node",
               "NanoReview lists the Helio G81 as a 12 nm platform. This is chipset process information, not a Philippine availability or device-SKU source.",
               source_kind="independent_chipset_reference"),
        source("honor_play20a_ph_ptg", "Pinoy Techno Guide", URL_PTG,
               "Philippine model page, features, price-history, and technical cross-check",
               "Published 2026-11-07. The page identifies the 2026 Philippine Play20A and many device features, but is internally inconsistent: its overview says 3 GB RAM / 128 GB storage, its specification table says 3 GB / 64 GB, and its promo text labels the November 11 promotion as 2025. The exact local 4 GB / 64 GB configuration and 2026 promo window are verified from other local sources and retailer evidence; PTG's disputed RAM, storage, and promo-year values are not used." ,
               "2026-11-07", "independent_ph_reference"),
        source("honor_play20a_ph_jam_launch", "JamOnline", URL_JAM_LAUNCH,
               "Contemporaneous Philippine launch and online early-access offer dates",
               "Published 2026-11-07. Reports HONOR Philippines introducing the Play 20A for a Shopee 11.11 early-access deal at PHP 8,099 from a PHP 8,999 SRP, before nationwide store release on November 28, 2026.",
               "2026-11-07"),
        source("honor_play20a_ph_jam_availability", "JamOnline", URL_JAM_AVAIL,
               "Philippine online availability, launch SRP, and Smart Rear Screen cross-check",
               "Published 2026-11-13. Reports that the Play 20A was available exclusively on Shopee for PHP 8,099 against an PHP 8,999 SRP, and describes the 2-inch rear display, 6.9-inch 90 Hz main display, and 6,000 mAh battery.",
               "2026-11-13"),
        source("honor_play20a_ph_noypigeeks", "NoypiGeeks", URL_NOYPI,
               "Philippine launch, exact 4 GB / 64 GB configuration, local price, and specifications",
               "Published 2026-11-06. Identifies the Philippine Play 20A with Helio G81, 4 GB RAM / 64 GB storage, PHP 8,999 SRP, 6,000 mAh battery and 15 W wired charging, Android 16 Go, IP52, and local feature specifications.",
               "2026-11-06"),
        source("honor_play20a_ph_revu_review", "REVU Philippines", URL_REVU,
               "Independent hands-on review and exact tested 4 GB / 64 GB configuration",
               "Published in November 2026. REVU's reviewed unit has 4 GB physical RAM and 64 GB storage; it confirms the Helio G81, Android 16 Go, 6.9-inch 90 Hz LCD, 13 MP and 5 MP cameras, 6,000 mAh battery, 15 W charging, and physical design. Its hands-on measurements and descriptions remain distinct from manufacturer claims." ,
               "2026-11", "independent_ph_review"),
        source("honor_play20a_ph_besttech", "Best Tech Asia", URL_BESTTECH,
               "Recent Philippine guide-price and specification cross-check",
               "Last updated 2026-11-16. Lists the Philippine 4 GB / 64 GB version at PHP 8,999 SRP and the PHP 8,099 11.11 Shopee launch price, with nationwide retail availability expected from November 28. It is an editorial guide, not a checkout offer.",
               "2026-11-16", "independent_price_guide"),
        source("honor_play20a_ph_iwarehouse", "iWarehouse", URL_IWAREHOUSE,
               "Exact-configuration Philippine retailer cash price and branch-stock observation",
               "At access on 2026-11-26, the exact new HONOR Play 20A 4 GB / 64 GB was listed from PHP 8,999 cash and shown at five store locations. The retailer warns that stock information is not reserved and asks buyers to call before visiting; the price is recorded with that availability caveat.",
               source_kind="retailer_price_observation"),
        source("honor_play20a_ph_price_specs_crosscheck", "PhilNews", URL_PHILNEWS,
               "Local 4 GB / 64 GB variant and price comparison cross-check",
               "Published 2026-11-11. Reports the Philippine 4 GB / 64 GB model at PHP 8,999 SRP, PHP 8,099 Shopee launch price, Android 16 Go, Helio G81, 6,000 mAh battery, and local launch/retail dates. Used as a cross-check rather than the primary device-spec source.",
               "2026-11-11", "independent_ph_reference"),
    ]
    official = "honor_play20a_global_official_product"
    ptg = "honor_play20a_ph_ptg"
    jam = "honor_play20a_ph_jam_launch"
    jam_current = "honor_play20a_ph_jam_availability"
    noypi = "honor_play20a_ph_noypigeeks"
    revu = "honor_play20a_ph_revu_review"
    mediatek = "mediatek_helio_g81_official"
    nano = "nanoreview_helio_g81"
    retailer = "honor_play20a_ph_iwarehouse"

    fields = [
        field("model_number", official, "No model code or Philippine SKU code stated in the reviewed manufacturer, launch, and retailer sources", None, status="NOT_DISCLOSED", note="No regional model code is inferred from the product name."),
        field("configuration", noypi, "Philippine model: 4 GB RAM / 64 GB storage; PTG page separately lists 3 GB and conflicting storage values", "4 GB physical RAM / 64 GB storage", status="VERIFIED_SECONDARY", note="NoypiGeeks, REVU's tested unit, PhilNews, and the exact iWarehouse listing all identify 4 GB / 64 GB. PTG's overview/table disagree internally on RAM and storage; the manufacturer global page's 128 GB marketing value is not treated as a Philippine variant."),
        field("philippine_release_date", jam, "Shopee early-access release reported for November 11, 2026; nationwide store release scheduled November 28, 2026", "2026-11-11", status="VERIFIED_SECONDARY", note="This records the first reported Philippine online availability date. Nationwide retail was scheduled for November 28; iWarehouse lists branch availability earlier but warns that stock is informational."),
        field("official_launch_price_php", jam, "PHP 8,999 SRP; PHP 8,099 Shopee 11.11 promotional price", 8999, unit="PHP", status="VERIFIED_SECONDARY", note="PHP 8,999 is the Philippine SRP. PHP 8,099 was a dated 11.11 launch promotion, not the standard price."),
        field("current_price_php", retailer, "PHP 8,999 cash price for the exact 4 GB / 64 GB model; retailer lists it at five locations but says stock is informational and not reserved", 8999, status="VERIFIED_SECONDARY", unit="PHP", note="Current new-retail cash listing observed 2026-11-26. The retailer lists five locations but says inventory is not reserved; call to confirm before travel. The PHP 8,099 Shopee offer was a dated 11.11 promotion and is not presented as current.", configuration_match="Exact Philippine HONOR Play 20A 4 GB RAM / 64 GB storage retailer configuration") | {"priceCondition": "new", "priceType": "Philippine retailer cash price PHP 8,999 observed 2026-11-26; branch stock informational and not reserved", "priceObservedAt": OBSERVED},
        field("display_size", official, "6.9-inch main display plus 2.0-inch Smart Rear Screen (240 × 296 pixels)", 6.9, key="displayInches", unit="in", status="VERIFIED", note="HONOR Global confirms the main display size and Smart Rear Screen; local sources specify the secondary display resolution."),
        field("display_technology", ptg, "Main 6.9-inch IPS LCD; secondary 2-inch Smart Rear LCD", "IPS LCD", key="displayType", status="VERIFIED_SECONDARY", note="Local model sources identify the main screen as LCD/IPS LCD. The 2-inch rear display is recorded in the display-size field and source notes, not merged into the main-panel type."),
        field("display_resolution", noypi, "Main: 720 × 1600 pixels (HD+); rear: 240 × 296 pixels", "720 x 1600", key="resolution", status="VERIFIED_SECONDARY", note="The main-panel resolution is the catalog value; the smaller rear-display resolution is retained in the source value."),
        field("display_refresh_rate", official, "Main display supports up to 90 Hz", 90, key="refreshHz", unit="Hz", status="VERIFIED", note="HONOR Global states up to 90 Hz and notes that actual refresh varies by app and scene."),
        field("display_brightness", revu, "REVU reports typical brightness around 600 nits; manufacturer page does not provide a matching measured-condition figure", "Approximately 600 nits typical (review report)", status="VERIFIED_SECONDARY", unit="nits", note="This is retained as a secondary review figure with its typical-brightness qualifier, not presented as a manufacturer-certified peak value."),
        field("display_protection", ptg, "Aluminosilicate glass on the main display", "Aluminosilicate glass", status="VERIFIED_SECONDARY", note="PTG lists aluminosilicate cover glass; REVU independently describes the front glass as scratch-resistant."),
        field("chipset", official, "MediaTek G81 / Helio G81", "MediaTek Helio G81", key="chipset", status="VERIFIED", note="HONOR's official product page says MediaTek G81; Philippine sources identify it as Helio G81."),
        field("process_node", nano, "12 nm", 12, unit="nm", status="VERIFIED_SECONDARY", note="NanoReview lists the Helio G81 process node as 12 nm; this is chipset-level information."),
        field("cpu", mediatek, "Octa-core: 2 × Cortex-A75 up to 2.0 GHz + 6 × Cortex-A55 up to 1.7 GHz", "Octa-core: 2x Cortex-A75 up to 2.0 GHz + 6x Cortex-A55 up to 1.7 GHz", key="cpu", status="VERIFIED", note="MediaTek's official Helio G81 page specifies the same CPU cluster and clock ceiling."),
        field("gpu", mediatek, "Arm Mali-G52 MC2", "Arm Mali-G52 MC2", key="gpu", status="VERIFIED", note="MediaTek's official Helio G81 specifications identify Mali-G52 MC2."),
        field("operating_system", noypi, "Android 16 Go Edition at Philippine launch", "Android 16 Go Edition", key="os", status="VERIFIED_SECONDARY", note="Local launch and review sources report Android 16 Go. No later operating-system upgrade is inferred."),
        field("os_support", official, "No official Philippine OS/security update duration found in reviewed sources", None, status="PENDING_VERIFICATION", note="No update count or end-of-support date is inferred."),
        field("ram_capacity", noypi, "4 GB physical RAM in the Philippine 4 GB / 64 GB configuration", 4, key="ramGb", unit="GB", status="VERIFIED_SECONDARY", note="Exact local 4 GB configuration is supported by NoypiGeeks, REVU's tested unit, PhilNews, and the retailer listing. PTG's page gives an inconsistent 3 GB figure; it is not adopted."),
        field("ram_type", mediatek, "Device-specific RAM generation not stated; platform supports LPDDR4x", None, status="NOT_DISCLOSED", note="A chipset-supported memory type does not establish the exact phone's installed RAM type."),
        field("storage_capacity", noypi, "64 GB internal storage in the Philippine configuration", 64, key="storageGb", unit="GB", status="VERIFIED_SECONDARY", note="NoypiGeeks, REVU, PhilNews, and iWarehouse identify the local 64 GB version. Global 128 GB and other-market configurations are not added as Philippine variants."),
        field("storage_type", mediatek, "Device-specific storage interface not stated; platform supports eMMC 5.1", None, status="NOT_DISCLOSED", note="The chipset's maximum supported interface is not taken as proof of the installed storage interface."),
        field("storage_expansion", official, "HONOR says storage can be expanded up to 1 TB using a three-card slot", "Dedicated microSD expansion up to 1 TB", status="VERIFIED", note="The official product page describes a three-card slot and expansion up to 1 TB; local spec pages also identify microSD expansion."),
        field("rear_camera_system", noypi, "Single 13 MP f/2.2 autofocus main camera with LED flash; Smart Rear Screen can be used as its selfie viewfinder", "13 MP f/2.2 main camera with autofocus and LED flash", status="VERIFIED_SECONDARY", note="The handset has one listed rear imaging camera; the rear display is a viewfinder feature, not another camera."),
        field("main_camera_sensor", noypi, "13 MP f/2.2 autofocus main camera; sensor maker/model not disclosed", None, status="NOT_DISCLOSED", note="The sensor vendor and sensor model are not named in the reviewed sources."),
        field("ultrawide_camera", noypi, "No ultrawide camera listed", "No ultrawide module listed", status="NOT_APPLICABLE", note="The local model sources list a single rear camera."),
        field("telephoto_camera", noypi, "No telephoto camera listed", "No telephoto module listed", status="NOT_APPLICABLE", note="The local model sources list a single rear camera."),
        field("front_camera", noypi, "5 MP f/2.2 front camera", 5, key="frontCameraMp", unit="MP", status="VERIFIED_SECONDARY", note="Local model and review sources report a 5 MP front camera."),
        field("video_recording", ptg, "Rear video up to 1080p at 30 fps; front video up to 1080p at 30 fps", "Rear up to 1080p/30; front up to 1080p/30", status="VERIFIED_SECONDARY", note="Maximum listed recording modes in the local specification reference."),
        field("battery_capacity", official, "6,000 mAh typical capacity; 5,850 mAh rated capacity", 6000, key="batteryMah", unit="mAh", status="VERIFIED", note="HONOR Global explicitly distinguishes typical and rated capacities; the catalog numeric value is the typical figure."),
        field("battery_technology", ptg, "Lithium-ion polymer (non-removable)", "Lithium-ion polymer", status="VERIFIED_SECONDARY", note="Battery chemistry is listed in the local specification reference; the battery is not user-removable."),
        field("wired_charging", noypi, "15 W wired charging", 15, key="chargingW", unit="W", status="VERIFIED_SECONDARY", note="Local launch specification reports 15 W wired charging."),
        field("wireless_charging", official, "No wireless charging support listed in reviewed sources", None, status="NOT_DISCLOSED", note="No wireless charging capability is inferred."),
        field("dimensions", noypi, "171.1 × 79.0 × 8.4 mm", "171.1 x 79 x 8.4 mm", key="dimensions", unit="mm", status="VERIFIED_SECONDARY", note="Local model-specific dimensions, ordered height × width × thickness."),
        field("weight", revu, "206.5 g", 206.5, key="weightG", unit="g", status="VERIFIED_SECONDARY", note="REVU's hands-on review reports the same model's weight."),
        field("materials", ptg, "Glass front, plastic back", "Glass front; plastic rear", status="VERIFIED_SECONDARY", note="Local specification listing; finish material is not generalized beyond this statement."),
        field("ingress_protection", noypi, "IP52 dust and splash resistance", "IP52", status="VERIFIED_SECONDARY", note="Local source lists IP52. This is not described as waterproof or suitable for immersion."),
        field("sim_esim", noypi, "Dual Nano-SIM; eSIM support not stated", "Dual Nano-SIM; eSIM not recorded", status="VERIFIED_SECONDARY", note="Only physical SIM slots are recorded; lack of eSIM support is not inferred."),
        field("cellular_bands", noypi, "2G GSM, 3G HSPA+, and 4G LTE; no 5G; exact Philippine band list not recorded", "2G / 3G / 4G LTE; no 5G; band list not recorded", key="cellular", status="VERIFIED_SECONDARY", note="Local references identify this as a 4G LTE handset. No carrier-specific band compatibility is inferred."),
        field("wifi", noypi, "Dual-band Wi-Fi 802.11 a/b/g/n/ac (Wi-Fi 5)", "Wi-Fi 5 (802.11 a/b/g/n/ac), dual band", key="wifi", status="VERIFIED_SECONDARY", note="Local device listing identifies Wi-Fi 5; MediaTek's G81 platform source also lists 802.11ac support."),
        field("bluetooth", noypi, "Bluetooth 5.1", "Bluetooth 5.1", status="VERIFIED_SECONDARY", note="Reported in the local specification reference."),
        field("usb", noypi, "USB Type-C; transfer protocol/version not stated", "USB Type-C; protocol not recorded", key="ports", status="VERIFIED_SECONDARY", note="Connector type is recorded without inferring USB data speed."),
        field("nfc", ptg, "NFC: No", "No NFC", status="VERIFIED_SECONDARY", note="PTG's device specification explicitly lists NFC as unavailable."),
        field("gnss", noypi, "GPS, A-GPS, GLONASS, Galileo, BeiDou", "GPS, A-GPS, GLONASS, Galileo, BeiDou", status="VERIFIED_SECONDARY", note="Local model sources list these navigation systems."),
        field("audio", noypi, "3.5 mm headphone jack; single loudspeaker; FM radio listed", "3.5 mm headphone jack; single loudspeaker; FM radio", status="VERIFIED_SECONDARY", note="Audio details from Philippine launch/specification references."),
        field("sensors", noypi, "Accelerometer, ambient-light sensor, proximity sensor; side-mounted fingerprint reader and face unlock", "Accelerometer, ambient light, proximity; side fingerprint reader; face unlock", status="VERIFIED_SECONDARY", note="Sensors and biometrics from local model-specific references."),
    ]

    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "HONOR",
        "model": "Play 20A",
        "configuration": "4 GB physical RAM / 64 GB storage",
        "configurationLabel": "4 GB RAM / 64 GB storage",
        "replacementVariants": [{
            "id": CONFIG, "label": "4 GB RAM / 64 GB storage",
            "sku": None, "modelCode": None,
            "notes": "The exact Philippine 4 GB / 64 GB configuration is identified by local launch coverage, REVU's 4/64 review unit, and the iWarehouse listing. PTG's page has incompatible 3 GB RAM and 64/128 GB statements; the 2026 Philippine unit is not merged with older devices or other-market memory configurations. The Smart Rear Screen is a display feature, not a second device variant.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "sources": sources,
        "fields": fields,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "HONOR Play20A Shopee early access was reported from November 11, 2026; nationwide store release was scheduled for November 28. iWarehouse lists branch availability but says stock is informational and not reserved.",
            "philippineAvailability": "JamOnline reports HONOR Philippines' exclusive Shopee early-access sale from November 11 and nationwide store release on November 28, 2026; iWarehouse lists the exact local 4 GB / 64 GB model at several branches with a call-to-confirm stock warning.",
            "observedAt": OBSERVED,
            "manufacturer": "HONOR",
            "productLine": "Play Series",
            "philippineReleaseYear": 2026,
            "philippineDateLabel": "First reported Philippine online early-access date",
            "researchNotes": "The workbook's HONOR Play 20A record matches the 2026 HONOR Play20A with a Smart Rear Screen, not an older reused Play 20A name or a different Play-series model. The confirmed Philippine configuration is 4 GB physical RAM / 64 GB storage. Local coverage and an exact retailer list PHP 8,999; PHP 8,099 was a dated 11.11 online promotion. PTG's page has conflicting memory values and incorrectly dates the promotion as 2025; those disputed values are not used. The official manufacturer image URL is recorded, but reuse terms are unstated and the neutral catalog placeholder remains.",
            "qualityFlag": "PTG memory and promo-date inconsistencies; retailer stock is informational and not reserved",
            "openIssues": [
                {"issue": "PTG's page conflicts internally on RAM/storage and gives a 2025 promo year", "action": "Use the corroborated local 4 GB / 64 GB configuration and 2026 promotion dates; preserve PTG's inconsistency in source notes."},
                {"issue": "Current retailer stock is not reserved", "action": "The listed PHP 8,999 cash price is shown with the observed date; advise checking the branch before purchase."},
                {"issue": "Official product image reuse terms are not stated", "action": "Continue showing the neutral placeholder until reusable licensing or written permission is documented."},
                {"issue": "Official OS/security update duration not found", "action": "Leave support duration unrecorded."},
            ],
        },
    }

    if len(fields) != 45:
        raise ValueError(f"Expected 45 standard phone fields, got {len(fields)}")
    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact HONOR Play20A Light Blue product-list image was identified on the official HONOR Global product page, but no reusable license or written permission is recorded.",
        "sourcePage": URL_HONOR_IMAGE_PAGE,
        "assetUrl": URL_HONOR_IMAGE,
        "scope": "Exact 2026 HONOR Play20A, Light Blue finish; product image does not distinguish the Philippine 4 GB / 64 GB configuration",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for HONOR Play20A",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "HONOR", "model_name": "Play 20A", "category": "smartphones", "status": "source_queued"}],
        "fetches": [], "observations": [], "discovery": [],
        "prices": [
            {
                "device_id": DEVICE, "amount_php": 8999,
                "configuration_id": CONFIG, "configuration_match": "exact",
                "variant_ram_gb": 4, "variant_storage_gb": 64,
                "price_type": "retailer_cash_price_stock_information_not_reserved",
                "source_published_at": None,
                "excerpt": "iWarehouse listed the exact new 4GB/64GB HONOR Play 20A at PHP 8,999 cash and showed five locations; it warns that stock information is not reserved and asks customers to call before visiting.",
                "source_url": URL_IWAREHOUSE, "source_kind": "retailer_price_observation",
                "observed_at": OBSERVED_AT, "local_availability_verified": False,
                "availability_status": "branch_stock_listed_not_reserved_call_to_confirm",
            },
            {
                "device_id": DEVICE, "amount_php": 8099,
                "configuration_id": CONFIG, "configuration_match": "exact",
                "variant_ram_gb": 4, "variant_storage_gb": 64,
                "price_type": "historical_philippine_online_launch_promotion",
                "source_published_at": "2026-11-07",
                "excerpt": "HONOR Philippines' 11.11 Shopee early-access promotion was reported at PHP 8,099 against PHP 8,999 SRP. This dated November 11, 2026 offer is historical and not treated as the current price.",
                "source_url": URL_JAM_LAUNCH, "source_kind": "official_campaign_report",
                "observed_at": OBSERVED_AT, "local_availability_verified": False,
                "availability_status": "dated_2026_11_11_campaign_not_current",
            },
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "2026 HONOR Play20A inventory record matched to Philippine launch, review, and exact retailer evidence",
        "configuration": "4 GB physical RAM / 64 GB storage",
        "reviewedFields": len(fields),
        "firstOnlineAccess": "2026-11-11",
        "nationwideRetailDate": "2026-11-28",
        "historicalSrPPhp": 8999,
        "historicalShopeePromoPhp": 8099,
        "currentRetailerCashPricePhp": 8999,
        "currentStock": "iWarehouse lists five locations; stock is informational and not reserved",
        "ptgInconsistencies": ["RAM/storage disagree within page", "11.11 promotion year shown as 2025"],
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
