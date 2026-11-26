#!/usr/bin/env python3
"""Record source-backed Philippine research for TECNO CAMON 17P (CG7)."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/tecno-camon-17p-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_097c07418374a0"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-6gb-128gb-ph"

URL_TECNO_SPECS = "https://www.tecno-mobile.com/ph/phones/tech-specs/techspecs/camon-17p-12/"
URL_TECNO_PRODUCT = "https://www.tecno-mobile.com/ph/phones/product-detail/product/camon-17p-12/"
URL_YUGA = "https://www.yugatech.com/mobile/tecno-camon-17p-specs-price-philippines/"
URL_YUGA_PRICES = "https://www.yugatech.com/tecno-gadget-price-list-philippines/"
URL_NOYPI = "https://www.noypigeeks.com/android/tecno-camon-17p-philippines/"
URL_NTC = "https://region4b.ntc.gov.ph/wp-content/uploads/2022/01/GEC_12312021.pdf"
URL_GSMARENA = "https://www.gsmarena.com/tecno_camon_17p-10896.php"
URL_MEDIATEK = "https://www.mediatek.com/products/smartphones/mediatek-helio-g85"
URL_NANOREVIEW = "https://nanoreview.net/en/soc/mediatek-helio-g85"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-tecno-camon-17p"
URL_ECATALOG = "https://e-catalog.com/TECNO-CAMON-17P-128GB-6GB.htm"
URL_PTG = "https://www.pinoytechnoguide.com/pricelists/TECNO"
URL_TECNO_LAUNCH_VIDEO = "https://www.youtube.com/watch?v=AWwfCvAGR30"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("tecno_camon17p_ph_specs", "TECNO Mobile Philippines", URL_TECNO_SPECS,
           "Primary Philippine-market product specifications",
           "The manufacturer page identifies the PH CAMON 17P and lists 6 GB RAM, 128 GB ROM, Android 11, 6.8-inch 1080 x 2460 display, 5,000 mAh typical battery, 18 W charging, dimensions, cellular technologies, OTG, cameras, and sensors."),
    source("tecno_camon17p_ph_product", "TECNO Mobile Philippines", URL_TECNO_PRODUCT,
           "Primary product overview and display-brightness check",
           "The official product overview lists 500-nit display brightness and promotes 2K video. Its images match the exact model, but the page does not state reusable-image terms; no image is copied."),
    source("tecno_camon17p_yugatech", "YugaTech Philippines", URL_YUGA,
           "Philippine availability, dated launch price, and local specification cross-check",
           "Published June 30, 2021, the article says the phone was available in the Philippines for PHP 8,490 and links to Shopee. It lists the PH 6 GB / 128 GB configuration, cameras, connectivity, software, battery, dimensions, and colors." ,
           "2021-06-30"),
    source("tecno_camon17p_yugatech_price_index", "YugaTech Philippines", URL_YUGA_PRICES,
           "Historical Philippine price-list check",
           "The price index records the CAMON 17P at PHP 8,490 on June 30 and July 15, 2021. These are dated historical observations, not current offers."),
    source("tecno_camon17p_noypi", "NoypiGeeks Philippines", URL_NOYPI,
           "Independent Philippine launch and specification cross-check",
           "Published June 30, 2021, the report says TECNO Mobile Philippines launched the CAMON 17P and lists 6 GB / 128 GB, Helio G85, display, cameras, LTE, battery, and charging." ,
           "2021-06-30"),
    source("tecno_camon17p_ntc_gec", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and local model-code evidence",
           "The GEC record maps TECNO CG7 to TECNO CAMON 17P, applicant Twireless Inc., issued April 5, 2021. It supports Philippine registration and the code CG7; it does not establish retail eligibility by itself.",
           "2021-04-05"),
    source("tecno_camon17p_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-model global release and technical cross-check",
           "The exact-model page lists announced May 8, 2021 and released May 28, 2021; IPS LCD, 1080p30 video, dual Nano-SIM, 3.5 mm audio, NFC absent, and other global specifications. Model codes include CG7 and CG7n. Regional details are not treated as Philippine-specific unless corroborated."),
    source("tecno_camon17p_mediatek_g85", "MediaTek", URL_MEDIATEK,
           "Primary chipset CPU and GPU architecture reference",
           "MediaTek specifies two Cortex-A75 cores up to 2 GHz, six Cortex-A55 cores up to 1.8 GHz, and Mali-G52-class graphics. SoC capabilities are not used to infer installed RAM, storage, or connectivity beyond device-specific evidence."),
    source("tecno_camon17p_nanoreview_g85", "NanoReview", URL_NANOREVIEW,
           "Helio G85 process-node and chipset cross-check",
           "NanoReview lists the Helio G85 as an 8-core 12 nm SoC with the same A75/A55 layout and Mali-G52 MP2. This is chipset-level evidence; benchmark scores are not presented as CAMON 17P test results."),
    source("tecno_camon17p_kimovil_global", "Kimovil", URL_KIMOVIL,
           "Cross-market exact-model specification check, with configuration caveat",
           "The page is explicitly for a Global 4 GB / 128 GB version, not the Philippine 6 GB / 128 GB CG7. Its weight, materials, camera sensor, battery chemistry, USB, and regional connectivity claims are not promoted as verified PH-variant facts." ,
           "2024-04-04"),
    source("tecno_camon17p_ecatalog_global", "E-Catalog", URL_ECATALOG,
           "Cross-market 6 GB / 128 GB specification cross-check",
           "This page labels the product CAMON 17P 128 GB / 6 GB and code CG7N, while the Philippine NTC record uses CG7. It reports eMMC 5.1, Li-ion graphite, plastic construction, USB-C, and other details; the code/market difference leaves those fields pending for the PH CG7."),
    source("tecno_camon17p_ptg_price_index", "PinoyTechGuide", URL_PTG,
           "Current Philippine TECNO price-list review",
           "The current TECNO price index was checked for the CAMON 17P; the model is not listed there. This does not prove that no used or private sale exists, so no current Philippine price is assigned."),
    source("tecno_camon17p_official_launch_video", "TECNO Mobile Official", URL_TECNO_LAUNCH_VIDEO,
           "Official CAMON 17 series announcement context",
           "TECNO's verified channel published a CAMON 17 series launch video on May 3, 2021. It supports the series launch timeline but does not establish the first global sale date of the 17P.",
           "2021-05-03"),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, catalog_value=None,
          price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": "Exact Philippine TECNO CG7 CAMON 17P, 6 GB RAM / 128 GB storage unless noted"}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        item["unit"] = unit
    if price_type:
        item["priceType"] = price_type
    return item


def fields_for() -> list[dict]:
    rows = [
        field("model_number", "tecno_camon17p_ntc_gec", "NTC GEC maps TECNO CG7 to TECNO CAMON 17P", "CG7", status="VERIFIED", note="Use the locally registered CG7 code. GSMArena also lists CG7n among global model codes; the PH NTC row specifically identifies CG7."),
        field("global_release_date", "tecno_camon17p_gsmarena", "GSMArena lists announced 2021-05-08 and released 2021-05-28", "2021-05-28", note="The May 28 global release date is a secondary listing; the official May 3 series video is a launch promotion, not proof of first sale."),
        field("configuration", "tecno_camon17p_ph_specs", "6 GB RAM / 128 GB ROM", "6 GB RAM / 128 GB storage", status="VERIFIED", note="TECNO's Philippine specification page lists this local configuration; YugaTech independently reports the same single configuration."),
        field("philippine_release_date", "tecno_camon17p_yugatech", "YugaTech reported the CAMON 17P available in the Philippines on June 30, 2021", "2021-06-30", note="This is the dated Philippine availability report, not a transaction timestamp."),
        field("official_launch_price_php", "tecno_camon17p_yugatech", "PHP 8,490 launch-era price reported June 30, 2021 for the 6 GB / 128 GB PH model", 8490, unit="PHP", note="Historical price reported with a purchase link; not a current price. The manufacturer's page does not state a price.", price_type="historical_ph_launch_price"),
        field("current_price_php", "tecno_camon17p_ptg_price_index", "No current dated, orderable Philippine CAMON 17P offer was verified; the accessible YugaTech price-list entries are from 2021", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep the live catalog price blank. The 2021 PHP 8,490 amount remains a historical launch observation only.", price_type="no_current_offer_verified"),
        field("display_size", "tecno_camon17p_ph_specs", "6.8-inch display", 6.8, status="VERIFIED", key="displayInches", unit="in", note="TECNO PH and YugaTech list 6.8 inches."),
        field("display_technology", "tecno_camon17p_gsmarena", "IPS LCD; TECNO PH calls it a Dot-in display", "IPS LCD", key="displayType", note="GSMArena identifies IPS LCD; manufacturer and local launch sources confirm the centered Dot-in design."),
        field("display_resolution", "tecno_camon17p_ph_specs", "1080 x 2460 pixels (FHD+)", "1080 x 2460", status="VERIFIED", key="resolution", note="Manufacturer PH page states 1080 x 2460."),
        field("display_refresh_rate", "tecno_camon17p_ph_specs", "No refresh-rate value stated in the reviewed PH product specifications", None, status="NOT_DISCLOSED", key="refreshHz", unit="Hz", note="Do not infer 60 Hz from silence."),
        field("display_brightness", "tecno_camon17p_ph_product", "500 nit brightness", 500, status="VERIFIED", unit="nits", note="Official TECNO PH overview states 500 nits but does not specify whether typical, peak, or HBM."),
        field("display_protection", "tecno_camon17p_ph_specs", "No named cover-glass protection or scratch-resistance rating recorded", None, status="NOT_DISCLOSED", note="2.5D glass claims on a global page do not establish a protection rating for the PH model."),
        field("chipset", "tecno_camon17p_ph_specs", "MediaTek Helio G85", "MediaTek Helio G85", status="VERIFIED", key="chipset", note="Official TECNO PH overview and local YugaTech listing identify the G85."),
        field("process_node", "tecno_camon17p_nanoreview_g85", "Helio G85 manufactured on a 12 nm process", 12, unit="nm", note="SoC-level NanoReview value. It describes the confirmed chipset, not a separately measured phone process."),
        field("cpu", "tecno_camon17p_mediatek_g85", "2x Cortex-A75 up to 2.0 GHz + 6x Cortex-A55 up to 1.8 GHz", "2x Cortex-A75 2.0 GHz + 6x Cortex-A55 1.8 GHz", status="VERIFIED", key="cpu", note="MediaTek official G85 page lists the core arrangement and clocks."),
        field("gpu", "tecno_camon17p_ph_specs", "Arm Mali-G52 MC2", "Arm Mali-G52 MC2", status="VERIFIED", key="gpu", note="YugaTech identifies Mali-G52 MC2; MediaTek confirms Mali-G52-class graphics for the chipset."),
        field("operating_system", "tecno_camon17p_ph_specs", "Android 11 with HiOS 7.6", "HiOS 7.6 based on Android 11", status="VERIFIED", key="os", note="TECNO PH lists Android 11; contemporaneous local coverage names HiOS 7.6."),
        field("os_support", "tecno_camon17p_ph_specs", "No OS-upgrade or security-support policy found", None, status="NOT_DISCLOSED", note="No update count, end date, or support duration is inferred."),
        field("ram_capacity", "tecno_camon17p_ph_specs", "6 GB RAM", 6, status="VERIFIED", key="ramGb", unit="GB", note="Official Philippine product specification."),
        field("ram_type", "tecno_camon17p_ph_specs", "TECNO PH confirms 6 GB but does not identify the installed RAM type; Kimovil's LPDDR4X line is for its Global 4 GB version", None, status="NOT_DISCLOSED", note="Chipset memory support and the different global SKU do not establish the PH unit's installed RAM type."),
        field("storage_capacity", "tecno_camon17p_ph_specs", "128 GB ROM", 128, status="VERIFIED", key="storageGb", unit="GB", note="Official Philippine product specification."),
        field("storage_type", "tecno_camon17p_ecatalog_global", "E-Catalog reports eMMC 5.1 for CAMON 17P 6 GB / 128 GB code CG7N; local NTC registration uses CG7", None, status="PENDING_VERIFICATION", key="storageType", note="The cross-market code differs from the Philippine registration; keep the Philippine storage interface blank pending a CG7-specific source."),
        field("storage_expansion", "tecno_camon17p_yugatech", "Dedicated microSD slot; expansion up to 512 GB", "Dedicated microSD slot, up to 512 GB", note="YugaTech's local specification lists a dedicated slot and 512 GB maximum."),
        field("rear_camera_system", "tecno_camon17p_yugatech", "64 MP f/1.79 wide + 2 MP macro + 2 MP bokeh/depth + QVGA AI camera", "64 MP wide + 2 MP macro + 2 MP bokeh/depth + QVGA AI camera", key="rearCameraMp", unit="MP", note="The local source describes the third module as bokeh; NoypiGeeks describes depth. Catalog numeric value is the 64 MP main camera.", catalog_value=64),
        field("main_camera_sensor", "tecno_camon17p_kimovil_global", "Kimovil lists an OmniVision OV64B main sensor for its Global 4 GB / 128 GB page; PH CG7 sensor identity is not independently confirmed", None, status="PENDING_VERIFICATION", note="Do not transfer the unverified global variant's sensor identity to the PH 6 GB / 128 GB record."),
        field("ultrawide_camera", "tecno_camon17p_yugatech", "The complete local rear-camera list contains no ultrawide module", "No ultrawide camera listed", status="NOT_APPLICABLE", note="The four listed rear modules are main, macro, bokeh/depth, and QVGA AI; none is described as ultrawide."),
        field("telephoto_camera", "tecno_camon17p_yugatech", "The complete local rear-camera list contains no telephoto module", "No telephoto camera listed", status="NOT_APPLICABLE", note="No telephoto lens appears in the full local camera list."),
        field("front_camera", "tecno_camon17p_ph_specs", "16 MP front camera with dual flash", 16, status="VERIFIED", key="frontCameraMp", unit="MP", note="Official TECNO PH specification."),
        field("video_recording", "tecno_camon17p_ph_product", "Official TECNO overview advertises 2K video; GSMArena lists 1080p at 30 fps", None, status="CONFLICTING_INFORMATION", key="video", note="Published video-capability claims differ. Keep the catalog video mode blank pending model-specific recording evidence."),
        field("battery_capacity", "tecno_camon17p_ph_specs", "5,000 mAh typical", 5000, status="VERIFIED", key="batteryMah", unit="mAh", note="TECNO PH explicitly marks this typical capacity."),
        field("battery_technology", "tecno_camon17p_ecatalog_global", "E-Catalog describes Li-ion graphite for code CG7N; Kimovil's Global 4 GB / 128 GB page lists Li-Polymer", None, status="PENDING_VERIFICATION", note="These are cross-market pages and disagree on chemistry; do not assign a battery type to local CG7."),
        field("wired_charging", "tecno_camon17p_ph_specs", "18 W Flash Charge", 18, status="VERIFIED", key="chargingW", unit="W", note="Official TECNO PH specification."),
        field("wireless_charging", "tecno_camon17p_ph_specs", "Wireless and reverse charging are not stated in the reviewed PH specification", None, status="NOT_DISCLOSED", note="Do not infer lack of support from omission."),
        field("dimensions", "tecno_camon17p_ph_specs", "168.67 x 76.44 x 8.82 mm", "168.67 x 76.44 x 8.82 mm", status="VERIFIED", key="dimensions", unit="mm", note="Official TECNO PH page gives height, width, and thickness."),
        field("weight", "tecno_camon17p_kimovil_global", "Kimovil lists 215 g on a Global 4 GB / 128 GB page; TECNO PH does not publish a weight", None, status="PENDING_VERIFICATION", key="weightG", unit="g", note="Keep blank because the recorded weight is not confirmed for local CG7 6 GB / 128 GB."),
        field("materials", "tecno_camon17p_ecatalog_global", "E-Catalog reports plastic front/back for CG7N; Kimovil reports plastic for its Global 4 GB / 128 GB version", None, status="PENDING_VERIFICATION", note="Neither reviewed source confirms frame/back materials for Philippine CG7; do not transfer the cross-market claim."),
        field("ingress_protection", "tecno_camon17p_ph_specs", "No IP rating recorded in the reviewed manufacturer PH page", None, status="NOT_DISCLOSED", note="No water/dust rating is inferred."),
        field("sim_esim", "tecno_camon17p_yugatech", "Dual Nano-SIM; eSIM is not listed", "Dual Nano-SIM; eSIM not recorded", key="sim", note="YugaTech local spec and GSMArena confirm dual Nano-SIM; eSIM is not documented."),
        field("cellular_bands", "tecno_camon17p_ph_specs", "GSM, WCDMA, LTE (FDD/TDD); exact Philippine band list not stated", "GSM / WCDMA / LTE; exact PH bands not recorded", key="cellular", note="The local official page lists network technologies but not band numbers; the GEC RF list is not treated as a complete mobile-band map."),
        field("wifi", "tecno_camon17p_yugatech", "Wi-Fi support listed; standard and bands not specified for the PH configuration", "Wi-Fi; standard not recorded", key="wifi", note="Do not transfer Wi-Fi 5 / 802.11ac from the different Global page without a local-variant specification."),
        field("bluetooth", "tecno_camon17p_yugatech", "Bluetooth 5.0", "Bluetooth 5.0", note="YugaTech's Philippine launch specification lists Bluetooth 5.0; Kimovil also lists 5.0 for the global model."),
        field("usb", "tecno_camon17p_ph_specs", "TECNO PH confirms OTG but does not name the physical port or data generation; cross-market pages say USB-C", None, status="PENDING_VERIFICATION", key="ports", note="Keep the local connector and USB generation blank until a CG7-specific PH source confirms them."),
        field("nfc", "tecno_camon17p_gsmarena", "GSMArena and Kimovil list NFC as absent for the exact CAMON 17P family", False, note="Secondary exact-model references agree; the PH manufacturer specification does not separately mention NFC."),
        field("gnss", "tecno_camon17p_yugatech", "GPS, A-GPS, GLONASS, BeiDou, and Galileo", "GPS, A-GPS, GLONASS, BeiDou, Galileo", note="YugaTech's Philippine launch spec lists these positioning systems."),
        field("audio", "tecno_camon17p_gsmarena", "3.5 mm headphone jack: yes; speaker configuration not fully stated", "3.5 mm headphone jack", key="sound", note="GSMArena and Kimovil list the headphone jack for the exact model; no speaker count is inferred."),
        field("sensors", "tecno_camon17p_ph_specs", "G-sensor, ambient-light sensor, proximity sensor, and fingerprint sensor", "Accelerometer, ambient-light, proximity, fingerprint", status="VERIFIED", note="Official TECNO PH page lists these sensors; fingerprint location is separately described as side-mounted by YugaTech."),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field records, got {len(rows)}")
    source_ids = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in rows} - source_ids)
    if missing:
        raise ValueError(f"Fields reference undefined sources: {missing}")
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "The NTC GEC record maps model CG7 to CAMON 17P and the June 30, 2021 YugaTech report says TECNO Mobile's CAMON 17P was available in the Philippines. Workbook eligibility remains Pending.",
        "philippineAvailability": "TECNO's Philippine product page lists the CAMON 17P 6 GB / 128 GB specification. YugaTech reported it available in the Philippines on June 30, 2021 at PHP 8,490; the NTC GEC record maps TECNO CG7 to TECNO CAMON 17P. This establishes local registration and contemporaneous reported availability, not an exact first purchase timestamp.",
        "observedAt": OBSERVED,
        "manufacturer": "TECNO Mobile",
        "catalogModel": "Camon 17P",
        "productLine": "TECNO CAMON 17P",
        "modelNumber": "CG7",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Philippine launch report date",
        "researchNotes": "Workbook row 38 matched to TECNO CAMON 17P / NTC code CG7. The Philippine manufacturer page documents one 6 GB / 128 GB configuration. The PHP 8,490 price is historical (June 2021); no current orderable PH offer was verified. Global pages list memory and model-code variants that are not transferred into the local configuration. Workbook eligibility remains Pending.",
        "qualityFlag": "Philippine registration and reported availability verified; one 6 GB / 128 GB configuration; historical price only; current price and several variant-specific specifications remain unverified.",
        "openIssues": [
            {"issue": "No current dated and orderable Philippine offer was verified", "action": "Keep the live price blank; preserve PHP 8,490 as historical only."},
            {"issue": "GSMArena lists both CG7 and CG7n; local NTC registration specifically maps CG7 to CAMON 17P", "action": "Use CG7 for the PH record; do not merge CG7n as a local variant without evidence."},
            {"issue": "Several global pages describe 4 GB / 128 GB or code CG7N rather than PH code CG7", "action": "Do not transfer their RAM type, storage type, weight, materials, or unverified sensor details."},
            {"issue": "TECNO overview advertises 2K video while GSMArena lists 1080p30", "action": "Leave video modes unresolved pending exact PH unit evidence."},
            {"issue": "Cross-market sources disagree on battery chemistry", "action": "Leave battery technology unset for the PH code."},
            {"issue": "Official product images match the exact model, but reuse terms were not found", "action": "Continue using the neutral placeholder until image reuse permission is established."},
            {"issue": "Workbook eligibility status remains Pending", "action": "Preserve Pending and apply existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "tecno"
            or device.get("model", "").casefold() != "camon 17p"):
        raise ValueError("Inventory row no longer matches TECNO Camon 17P")
    current_ids = {variant.get("id") for variant in device.get("variants", [])}
    if current_ids - {OLD_CONFIG, CONFIG}:
        raise ValueError(f"Unexpected CAMON 17P configurations: {sorted(current_ids)}")

    variant = {
        "id": CONFIG,
        "label": "6 GB RAM / 128 GB storage",
        "sku": None,
        "modelCode": "CG7",
        "notes": "Frost Silver, Magnet Black, and Spruce Green are listed for the model; inventory does not tie each color to a separate SKU.",
        "workbookRow": 38,
    }
    record = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "TECNO",
        "model": "Camon 17P",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "modelCode": "CG7",
        "sources": SOURCES,
        "fields": fields_for(),
        "availabilityEvidence": availability_evidence(),
        "replacementVariants": [variant],
        "replaceUnrecordedPlaceholder": True,
    }
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].append(record)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "TECNO's official page contains exact CAMON 17P product images, but no reusable image license or permission to copy/embed was recorded. Keep the neutral placeholder.",
        "sourcePage": URL_TECNO_PRODUCT,
        "assetUrl": None,
        "scope": "TECNO CAMON 17P / Philippine CG7, 6 GB / 128 GB",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for TECNO Camon 17P",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "TECNO", "model_name": "Camon 17P", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech published June 30, 2021 and reports PHP 8,490 for the locally available 6 GB / 128 GB CAMON 17P."},
            {"device_id": DEVICE, "source_url": URL_YUGA_PRICES, "result": "YugaTech price index contains dated June 30 and July 15, 2021 entries at PHP 8,490; historical only."},
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "Current TECNO price index reviewed; CAMON 17P not listed. This does not prove no private or used sale exists."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Kimovil page is Global 4 GB / 128 GB and has no usable current Philippine price; no PH offer promoted."},
        ],
        "prices": [{
            "device_id": DEVICE,
            "amount_php": 8490,
            "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_6gb_128gb_configuration",
            "variant_ram_gb": 6,
            "variant_storage_gb": 128,
            "price_type": "historical_ph_launch_price",
            "source_published_at": "2021-06-30",
            "excerpt": "YugaTech reported the locally available 6 GB / 128 GB TECNO CAMON 17P at PHP 8,490 on June 30, 2021.",
            "source_url": URL_YUGA,
            "source_kind": "historical_local_launch_price",
            "observed_at": OBSERVED_AT,
            "local_availability_verified": True,
            "availability_status": "historical_launch_price_not_current",
        }],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 38 TECNO Camon 17P -> NTC-registered TECNO CG7 CAMON 17P",
        "configuration": variant["label"],
        "reviewedFields": len(record["fields"]),
        "philippineAvailabilityReportDate": "2021-06-30",
        "historicalLaunchPricePhp": 8490,
        "currentPrice": "not verified; left blank",
        "image": "neutral placeholder; reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
