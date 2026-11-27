#!/usr/bin/env python3
"""Complete the source-backed ASUS Zenfone 8 PH configuration review."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGE_SOURCES = ROOT / "research/catalog-image-sources.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/asus-zenfone-8-ph-prices-2026-11-27.json"
OBSERVED = "2026-11-27"
DEVICE = "device_bfb5e856a9a659"
CONFIG_8 = f"{DEVICE}-auto-8gb-128gb"
CONFIG_16 = f"{DEVICE}-auto-16gb-256gb"

URL_ASUS = "https://www.asus.com/mobile-handhelds/phones/zenfone/zenfone-8/techspec/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/asus-zenfone-8"
URL_LAUNCH = "https://2ndopinion.ph/asus-zenfone-returns-to-ph-shores-pre-orders-begin-may-14/"
URL_TECHNO = "https://www.technobaboy.com/2021/05/14/asus-zenfone-8-5g-zenfone-8-flip-pre-order-price-philippines/"
URL_MODEL_CODE = "https://rog.asus.com/us/support/faq/1014441/"
URL_SUPPORT = "https://rog.asus.com/ph/support/faq/1056885/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-888-5g-mobile-platform"
URL_GLOBAL_LAUNCH = "https://www.youtube.com/watch?v=OP7S32a4ohw"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-asus-zenfone-8"
URL_GSMARENA = "https://www.gsmarena.com/asus_zenfone_8-10893.php"
URL_NANOREVIEW = "https://nanoreview.net/"
URL_COMMONS = "https://commons.wikimedia.org/wiki/File:Zenfone_8.jpg"
URL_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/5/5d/Zenfone_8.jpg"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("asus_zenfone8_global_specs", "ASUS", URL_ASUS,
        "Manufacturer technical specifications for Zenfone 8",
        "The ASUS global specifications identify the Zenfone 8 and publish its display, Snapdragon 888, LPDDR5 and UFS 3.1 options, camera modules, battery, dimensions, weight, audio and connectivity. ASUS warns that Wi-Fi 6E and cellular-band compatibility vary by region; global bands are not assigned to the Philippine configurations."),
    src("asus_zenfone8_ph_ptg", "Pinoy Techno Guide", URL_PTG,
        "Exact-model Philippine launch, configuration, launch price and local specification report",
        "Dated 2021-05-14. Reports ASUS stores, authorized dealers and online availability; separately identifies 8 GB/128 GB at PHP 34,995 and 16 GB/256 GB at PHP 39,995. The page is a historical launch report and supplies no current price." , "2021-05-14"),
    src("asus_zenfone8_ph_launch", "2nd Opinion (ASUS Philippines launch information)", URL_LAUNCH,
        "Philippine preorder date, local configuration/price table and launch specifications",
        "Published 2021-05-15 and reports ASUS Philippines preorders began May 14 at ASUS Concept Stores and accredited online/offline shops. Its product table separately lists 16/256 at PHP 39,995 and 8/128 at PHP 34,995, with May 2021 ETA and May 14–25 preorder window. It establishes reported preorder availability, not an exact first retail transaction." , "2021-05-15"),
    src("asus_zenfone8_ph_technobaboy", "Technobaboy Philippines", URL_TECHNO,
        "Independent Philippine preorder, configuration and price cross-check",
        "Published 2021-05-14. Reports local preorder from that date and the same two Zenfone 8 configurations and launch prices. It calls local Wi-Fi 6, while PTG lists Wi-Fi 6E; the local standard remains unresolved." , "2021-05-14"),
    src("asus_zenfone8_model_code", "ASUS ROG Support", URL_MODEL_CODE,
        "Manufacturer model-name and model-number lookup",
        "ASUS support maps Zenfone 8 to marketing model I006D and model number ZS590KS. This does not identify a local color-specific or retail SKU."),
    src("asus_zenfone8_support_policy", "ROG Philippines / ASUS Support", URL_SUPPORT,
        "Manufacturer-published hardware and software support policy",
        "ASUS lists Zenfone 8 hardware support through 2024, two OS upgrades, and security updates through 2023. This is the published support commitment, not a claim that every regional firmware received an update on the same date."),
    src("qualcomm_snapdragon888", "Qualcomm", URL_QUALCOMM,
        "Chipset manufacturer specifications",
        "Qualcomm identifies Snapdragon 888, Kryo 680 CPU, Adreno 660 GPU and the 5 nm process node. Device-specific frequencies and radio bands are taken only from device/regional sources."),
    src("asus_zenfone8_global_launch", "ASUS (verified YouTube channel)", URL_GLOBAL_LAUNCH,
        "Official global product announcement date",
        "ASUS published its Zenfone 8 introduction on 2021-05-12. This is the manufacturer announcement date, not the Philippine preorder date.", "2021-05-12"),
    src("asus_zenfone8_kimovil", "Kimovil", URL_KIMOVIL,
        "Secondary exact-model identity and global configuration cross-check",
        "The exact Zenfone 8 profile includes global memory/storage options. It is not used as Philippine availability or price evidence; configurations not documented in local launch sources are not added."),
    src("asus_zenfone8_gsmarena_access", "GSMArena", URL_GSMARENA,
        "Exact-model source discovery and access result",
        "The exact Zenfone 8 page was queried, but its full page returned HTTP 402 during this review. No blocked content was bypassed and no field value is attributed to that page."),
    src("asus_zenfone8_nanoreview_search", "NanoReview", URL_NANOREVIEW,
        "Exact-model source discovery",
        "The site was searched for an exact Zenfone 8 profile; no exact-model profile was located in this pass. No NanoReview value is inferred."),
    src("asus_zenfone8_commons_image", "Wikimedia Commons / ROC-C.Z", URL_COMMONS,
        "Exact-model image identity and reuse license",
        "The file caption and description identify ASUS Zenfone 8 / ZS590KS. The Commons file page attributes the image to ROC-C.Z and declares CC BY-SA 4.0. The photo is a model-level front view; it does not distinguish RAM/storage or color variants. Catalog delivery converts/resizes the image without subject edits."),
]


def f(fid: str, sid: str, source_value, normalized, *, status="VERIFIED",
      key=None, unit=None, note=None, price_type=None, price_observed=None,
      price_condition=None, replace_existing=True, candidates=None):
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": source_value, "normalizedValue": normalized,
           "note": note or "Exact ASUS Zenfone 8 model reviewed. Philippine availability and configuration are asserted only where the cited local source identifies them."}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if price_type:
        row.update({"priceType": price_type, "priceObservedAt": price_observed,
                    "priceCondition": price_condition or "new"})
    if replace_existing:
        row["replaceExisting"] = True
    if candidates:
        row["candidateEvidence"] = candidates
    return row


def nd(fid: str, sid: str, explanation: str, *, note=None):
    return f(fid, sid, explanation, None, status="NOT_DISCLOSED", note=note or explanation)


def not_found(fid: str, sid: str, explanation: str):
    return f(fid, sid, explanation, None, status="UNAVAILABLE_AFTER_RESEARCH", note=explanation)


def fields(ram: int, storage: int, price: int) -> list[dict]:
    wifi_candidates = [
        {"value": "Wi-Fi 6E", "sourceUrl": URL_PTG, "sourceKind": "independent_ph_launch_source",
         "observedAt": OBSERVED, "excerpt": "PTG's Zenfone 8 specification table lists Wi-Fi 6E.",
         "configurationMatch": "Philippine Zenfone 8 launch page; both local configurations share the model-level specification",
         "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
        {"value": "Wi-Fi 6", "sourceUrl": URL_TECHNO, "sourceKind": "independent_ph_launch_source",
         "observedAt": OBSERVED, "excerpt": "Technobaboy's Philippine preorder report lists Wi-Fi 6.",
         "configurationMatch": "Philippine Zenfone 8 launch report; does not identify a different Wi-Fi hardware revision",
         "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
        {"value": "Integrated Wi-Fi 6/6E; availability/features depend on regulatory limitations",
         "sourceUrl": URL_ASUS, "sourceKind": "manufacturer_global_specification",
         "observedAt": OBSERVED, "excerpt": "ASUS lists Wi-Fi 6/6E and says Wi-Fi 6E availability/features depend on regional limits.",
         "configurationMatch": "global model-level spec; Philippine mode not isolated",
         "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
    ]
    config = f"{ram} GB RAM / {storage} GB storage"
    price_note = (f"Historical Philippine launch SRP for the locally documented {config} configuration. "
                  "This is the May 2021 launch price, not a current offer.")
    rows = [
        f("model_number", "asus_zenfone8_model_code", "ASUS maps Zenfone 8 to I006D / ZS590KS; no Philippine retail SKU is stated.", "ZS590KS; Philippine retail SKU not recorded", status="VERIFIED", note="The ASUS support lookup identifies the exact model number. Do not infer a local SKU or regional band set."),
        f("global_release_date", "asus_zenfone8_global_launch", "ASUS published its Zenfone 8 introduction on 2021-05-12.", "2021-05-12", status="VERIFIED", note="Manufacturer global announcement date; distinct from Philippine preorder timing."),
        f("configuration", "asus_zenfone8_ph_launch", f"ASUS Philippines preorder coverage lists Zenfone 8 {config}; no numeric color-specific SKU is stated.", config + "; local SKU not recorded", status="VERIFIED_SECONDARY", note="Exact Philippine launch configuration documented in the local preorder table. The other locally documented configuration remains a separate record."),
        f("philippine_release_date", "asus_zenfone8_ph_launch", "ASUS Philippines preorder period began 2021-05-14; local sources do not establish the first completed retail sale.", "2021-05-14", status="VERIFIED_SECONDARY", note="Reported Philippine preorder start date, not an exact first-sale date."),
        f("official_launch_price_php", "asus_zenfone8_ph_ptg", f"PHP {price:,} official price for {config} on the 2021-05-14 Philippine listing.", price, status="VERIFIED_SECONDARY", unit="PHP", note=price_note, price_type="historical_ph_launch_srp", price_observed="2021-05-14", price_condition="new"),
        not_found("current_price_php", "asus_zenfone8_ph_ptg", "No dated current Philippine offer for this exact configuration was found as of 2026-11-27. PTG's exact-model page records 2021 launch SRPs only; the launch price is not reused as a current price."),
        f("display_size", "asus_zenfone8_global_specs", "5.9-inch display", 5.9, key="displayInches", unit="in"),
        f("display_technology", "asus_zenfone8_global_specs", "Samsung AMOLED display", "Samsung AMOLED", key="displayType", note="ASUS calls the panel Samsung AMOLED; PTG uses the marketing label Super AMOLED."),
        f("display_resolution", "asus_zenfone8_global_specs", "2400 x 1080 pixels (ASUS lists vertical x horizontal)", "1080 x 2400", key="resolution", note="Stored in conventional width x height order; ASUS source prints the panel dimensions as 2400 x 1080."),
        f("display_refresh_rate", "asus_zenfone8_global_specs", "120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", "asus_zenfone8_global_specs", "ASUS lists 1100 nits peak; local launch coverage lists 1000 nits without a matching measurement label.", None, status="CONFLICTING_INFORMATION", note="The global manufacturer page reports 1100 nits peak while Philippine launch coverage reports 1000 nits. The source excerpts do not establish comparable measurement conditions, so no brightness value is selected.", candidates=[
            {"value": "1100 nits peak", "sourceUrl": URL_ASUS, "sourceKind": "manufacturer_global_specification", "observedAt": OBSERVED, "excerpt": "ASUS lists 1100 nits peak brightness.", "configurationMatch": "exact Zenfone 8 global model specification", "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
            {"value": "1000 nits", "sourceUrl": URL_LAUNCH, "sourceKind": "independent_ph_launch_source", "observedAt": OBSERVED, "excerpt": "Local launch report describes a 1000-nit Zenfone 8 display.", "configurationMatch": "Philippine Zenfone 8; exact configuration not differentiated", "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
        ]),
        f("display_protection", "asus_zenfone8_global_specs", "Corning Gorilla Glass Victus", "Corning Gorilla Glass Victus"),
        f("chipset", "asus_zenfone8_global_specs", "Qualcomm Snapdragon 888 5G Mobile Platform", "Qualcomm Snapdragon 888", key="chipset"),
        f("process_node", "qualcomm_snapdragon888", "5 nm process node", 5, status="VERIFIED", unit="nm", note="Chipset manufacturer product comparison identifies Snapdragon 888 at 5 nm; this is a SoC fabrication process claim."),
        f("cpu", "qualcomm_snapdragon888", "Qualcomm Kryo 680, octa-core; device clock configuration 1 x 2.84 GHz + 3 x 2.42 GHz + 4 x 1.8 GHz per local exact-model specification.", "Octa-core Kryo 680: 1 x 2.84 GHz + 3 x 2.42 GHz + 4 x 1.8 GHz", status="VERIFIED_SECONDARY", key="cpu", note="Qualcomm confirms the Kryo 680 CPU family; PTG publishes the exact Zenfone 8 cluster clocks."),
        f("gpu", "asus_zenfone8_global_specs", "Qualcomm Adreno 660", "Adreno 660", key="gpu"),
        f("operating_system", "asus_zenfone8_ph_ptg", "Android 11 with ZenUI 8", "Android 11 with ZenUI 8", status="VERIFIED_SECONDARY", key="os"),
        f("os_support", "asus_zenfone8_support_policy", "ASUS lists two OS upgrades and security updates through 2023; hardware support through 2024.", "Two OS upgrades; security updates through 2023; hardware support through 2024", status="VERIFIED", note="Manufacturer-published support policy; the field records the commitment and does not imply continued current updates."),
        f("ram_capacity", "asus_zenfone8_ph_launch", f"{ram} GB LPDDR5 RAM for the Philippine {config} listing", ram, status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="This exact local configuration is separated from the Zenfone 8's other RAM/storage option."),
        f("ram_type", "asus_zenfone8_global_specs", "LPDDR5", "LPDDR5", key="ramType"),
        f("storage_capacity", "asus_zenfone8_ph_launch", f"{storage} GB internal storage for the Philippine {config} listing", storage, status="VERIFIED_SECONDARY", key="storageGb", unit="GB"),
        f("storage_type", "asus_zenfone8_global_specs", "UFS 3.1", "UFS 3.1", key="storageType"),
        f("storage_expansion", "asus_zenfone8_ph_ptg", "No expandable storage listed; PTG says expansion: none.", "No microSD storage expansion", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", "asus_zenfone8_global_specs", "Dual rear cameras: 64 MP main and 12 MP ultrawide.", "64 MP main + 12 MP ultrawide dual rear-camera system"),
        f("main_camera_sensor", "asus_zenfone8_global_specs", "Sony IMX686 64 MP main sensor; f/1.8; 26.6 mm equivalent; phase-detection autofocus; optical image stabilization.", "64 MP Sony IMX686; f/1.8; PDAF; OIS"),
        f("ultrawide_camera", "asus_zenfone8_global_specs", "12 MP Sony IMX363 ultrawide; f/2.2; 14.3 mm equivalent; supports 4 cm macro.", "12 MP Sony IMX363 ultrawide; f/2.2; 4 cm macro"),
        f("telephoto_camera", "asus_zenfone8_global_specs", "Manufacturer specifies a fixed dual rear-camera system consisting of main and ultrawide cameras; no telephoto module is part of this model.", None, status="NOT_APPLICABLE", note="ASUS specifies two fixed rear cameras and identifies both as main and ultrawide. Do not confuse this model with Zenfone 8 Flip."),
        f("front_camera", "asus_zenfone8_ph_launch", "12 MP Sony IMX663 punch-hole front camera with dual-pixel autofocus.", 12, status="VERIFIED_SECONDARY", key="frontCameraMp", unit="MP"),
        f("video_recording", "asus_zenfone8_global_specs", "Main camera up to 8K UHD at 24 fps; secondary camera 4K UHD at 30/60 fps; 1080p at 30/60 fps; additional motion tracking and slow-motion modes.", "Main: 8K/24 fps; secondary: 4K/30 or 60 fps; 1080p/30 or 60 fps; other modes listed by ASUS"),
        f("battery_capacity", "asus_zenfone8_global_specs", "4000 mAh battery", 4000, key="batteryMah", unit="mAh"),
        f("battery_technology", "asus_zenfone8_ph_ptg", "Li-Po battery; non-removable", "Lithium-polymer; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", "asus_zenfone8_global_specs", "30 W wired charging", 30, key="chargingW", unit="W"),
        nd("wireless_charging", "asus_zenfone8_global_specs", "The reviewed ASUS specification and Philippine launch sources do not state wireless or reverse wireless charging support; no unsupported absence claim is made."),
        f("dimensions", "asus_zenfone8_global_specs", "148 x 68.5 x 8.9 mm", "148 x 68.5 x 8.9 mm", key="dimensions", unit="mm"),
        f("weight", "asus_zenfone8_global_specs", "169 g", 169, key="weightG", unit="g"),
        f("materials", "asus_zenfone8_ph_ptg", "Gorilla Glass Victus front, Gorilla Glass 3 back and aluminum frame.", "Gorilla Glass Victus front; Gorilla Glass 3 back; aluminum frame", status="VERIFIED_SECONDARY"),
        f("ingress_protection", "asus_zenfone8_ph_ptg", "IP68 water and dust resistance", "IP68", status="VERIFIED_SECONDARY"),
        f("sim_esim", "asus_zenfone8_global_specs", "Two nano-SIM slots; eSIM capability not stated.", "Dual nano-SIM; eSIM not recorded", key="sim", note="ASUS lists two physical nano-SIM slots. eSIM is left unrecorded because the source does not document it."),
        f("cellular_bands", "asus_zenfone8_ph_ptg", "5G, 4G LTE with VoLTE, 3G HSPA+, 2G EDGE/GPRS; exact Philippine frequency bands are not stated.", "5G; 4G LTE/VoLTE; 3G HSPA+; 2G EDGE/GPRS; exact PH bands not recorded", status="VERIFIED_SECONDARY", key="cellular", note="Local launch specifications support these network generations. ASUS says frequency bands vary by region; exact PH band compatibility is not inferred from a global variant."),
        f("wifi", "asus_zenfone8_global_specs", "Philippine sources disagree: PTG lists Wi-Fi 6E while Technobaboy lists Wi-Fi 6; ASUS says 6E availability depends on regional limits.", None, status="CONFLICTING_INFORMATION", key="wifi", note="Exact Philippine Wi-Fi mode remains unresolved. Candidate values are retained; no single Wi-Fi standard is shown for either local configuration.", candidates=wifi_candidates),
        f("bluetooth", "asus_zenfone8_global_specs", "Bluetooth 5.2", "Bluetooth 5.2"),
        f("usb", "asus_zenfone8_ph_ptg", "USB Type-C connector; exact USB data-generation/speed is not stated in the reviewed local source.", "USB Type-C; data standard not recorded", status="VERIFIED_SECONDARY", key="ports"),
        f("nfc", "asus_zenfone8_global_specs", "NFC supported", "NFC supported"),
        f("gnss", "asus_zenfone8_global_specs", "GPS L1/L5, GLONASS, BeiDou, Galileo, QZSS and NavIC", "GPS dual-band; GLONASS; BeiDou; Galileo; QZSS; NavIC"),
        f("audio", "asus_zenfone8_global_specs", "Dual stereo speakers with Dirac HD Sound; Hi-Res Audio via 3.5 mm output.", "Dual stereo speakers with Dirac HD; Hi-Res 3.5 mm audio output", key="sound"),
        f("sensors", "asus_zenfone8_ph_ptg", "Gyroscope, compass, ambient light sensor, proximity sensor and accelerometer.", "Gyroscope; compass; ambient-light sensor; proximity sensor; accelerometer", status="VERIFIED_SECONDARY"),
    ]
    return rows


def availability(config: str) -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Reported Philippine preorder availability from 2021-05-14 through the local ASUS launch channel; historical local configuration and SRP are documented. Current stock and price are not verified.",
        "philippineAvailability": f"ASUS Philippines launch coverage identifies the Zenfone 8 {config} for preorder through ASUS Concept Stores and accredited online/offline shops from 2021-05-14. Local sources distinguish it from Zenfone 8 Flip. This establishes reported preorder availability, not an exact first completed retail sale or current stock.",
        "observedAt": OBSERVED,
        "manufacturer": "ASUSTeK Computer Inc.",
        "productLine": "Zenfone",
        "modelNumber": "ZS590KS",
        "catalogModel": "Zenfone 8",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Reported Philippine preorder start date",
        "researchNotes": "Exact ASUS Zenfone 8 (ZS590KS) match. Only the two configurations identified in Philippine launch sources (8/128 and 16/256) are retained as separate records. The 8/256 global option shown by some global databases is not added as a local variant. Historical launch SRPs are not current prices. Regional Wi-Fi mode, exact PH frequency bands, and retail SKU remain unresolved. Workbook study scope remains Pending.",
        "qualityFlag": "Exact model, two local configurations, launch dates and historical SRPs manually reviewed; current price, exact regional SKU/bands and Wi-Fi mode unresolved; study scope remains Pending.",
        "openIssues": [
            {"issue": "No current price or stock observation for either exact configuration", "action": "Keep current price blank and preserve the May 2021 SRP as a dated historical launch price."},
            {"issue": "Philippine sources disagree on Wi-Fi 6 versus Wi-Fi 6E", "action": "Keep the Wi-Fi field unresolved and retain both cited candidates."},
            {"issue": "The manufacturer lists region-specific cellular bands but the local launch sources do not identify the exact PH band set", "action": "Show network generations only; do not claim specific Philippine frequency-band compatibility."},
            {"issue": "No exact local retail SKU is documented", "action": "Keep SKU blank; retain ASUS model number ZS590KS."},
            {"issue": "Workbook scope status is Pending", "action": "Do not change study eligibility as a side effect of technical enrichment."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    image_sources = json.loads(IMAGE_SOURCES.read_text(encoding="utf-8"))
    unavailable = json.loads(IMAGE_UNAVAILABLE.read_text(encoding="utf-8"))
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("workbookRow") != 3 or device.get("brand") != "ASUS" or device.get("model") != "Zenfone 8":
        raise SystemExit("Catalog target guard failed for workbook row 3 ASUS Zenfone 8")
    if device.get("scopeStatus") != "Pending":
        raise SystemExit("Expected workbook scope Pending; refusing to change eligibility")
    if {v.get("id") for v in device.get("variants", [])} != {CONFIG_8, CONFIG_16}:
        raise SystemExit("Expected the two locally documented 8/128 and 16/256 variants")
    if any(r.get("deviceId") == DEVICE and r.get("configurationId") not in {CONFIG_8, CONFIG_16} for r in manual["records"]):
        raise SystemExit("Unexpected Zenfone 8 configuration review exists; inspect exact model matching first")

    definitions = json.loads((ROOT / "research/enrichment/specification-fields.json").read_text(encoding="utf-8"))["smartphones"]
    expected_fields = {definition["id"] for definition in definitions}
    replacement_variants = [
        {"id": CONFIG_8, "label": "8 GB RAM / 128 GB storage", "sku": None,
         "modelCode": "ZS590KS", "pricePhp": 34995, "priceCondition": "new",
         "priceType": "Historical Philippine launch SRP", "priceObservedAt": "2021-05-14",
         "priceSourceUrl": URL_PTG, "listingStatus": "Not verified",
         "notes": "Historical launch SRP observed 2021-05-14; not a current offer. Philippine retail SKU not recorded."},
        {"id": CONFIG_16, "label": "16 GB RAM / 256 GB storage", "sku": None,
         "modelCode": "ZS590KS", "pricePhp": 39995, "priceCondition": "new",
         "priceType": "Historical Philippine launch SRP", "priceObservedAt": "2021-05-14",
         "priceSourceUrl": URL_PTG, "listingStatus": "Not verified",
         "notes": "Historical launch SRP observed 2021-05-14; not a current offer. Philippine retail SKU not recorded."},
    ]
    for config_id, ram, storage, price in ((CONFIG_8, 8, 128, 34995), (CONFIG_16, 16, 256, 39995)):
        rows = fields(ram, storage, price)
        actual = {row["fieldId"] for row in rows}
        if actual != expected_fields or len(rows) != len(expected_fields):
            raise SystemExit(f"The phone field set is incomplete/duplicated: missing={expected_fields - actual}, extra={actual - expected_fields}")
        item = {
            "deviceId": DEVICE, "configurationId": config_id,
            "brand": "ASUS", "model": "Zenfone 8",
            "configuration": f"{ram} GB RAM / {storage} GB storage",
            "configurationLabel": f"{ram} GB RAM / {storage} GB storage",
            "modelCode": "ZS590KS", "sources": SOURCES, "fields": rows,
            "availabilityEvidence": availability(f"{ram} GB RAM / {storage} GB storage"),
        }
        if config_id == CONFIG_8:
            item["replacementVariants"] = replacement_variants
        add_review(manual, catalog, item)
        deduplicate_target_reviews(manual, {(DEVICE, config_id)})
        saved = next(r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == config_id)
        saved["brand"] = "ASUS"
        saved["model"] = "Zenfone 8"
        saved["configuration"] = item["configuration"]
        saved["configurationLabel"] = item["configurationLabel"]
        saved["modelCode"] = "ZS590KS"
        saved["sku"] = None

    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    image_entry = {
        "deviceId": DEVICE, "method": "direct", "pageUrl": URL_COMMONS,
        "assetUrl": URL_IMAGE,
        "scope": "Exact Zenfone 8 ZS590KS model-level front view; the photo does not distinguish RAM/storage or color variants.",
        "rightsStatus": "LICENSED", "credit": "ROC-C.Z (Wikimedia Commons)",
        "usageTerms": "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
        "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0/",
        "rightsCheckedAt": OBSERVED,
        "changes": "Converted from JPEG to WebP and resized for catalog delivery; no crop or subject edits.",
    }
    image_sources = [row for row in image_sources if row.get("deviceId") != DEVICE]
    image_sources.append(image_entry)
    IMAGE_SOURCES.write_text(json.dumps(image_sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for config_id, ram, storage, price in ((CONFIG_8, 8, 128, 34995), (CONFIG_16, 16, 256, 39995)):
        prices.append({
            "device_id": DEVICE, "configuration_id": config_id,
            "variant_ram_gb": ram, "variant_storage_gb": storage,
            "configuration_match": f"ph_zenfone8_zs590ks_{ram}gb_{storage}gb_exact_local_launch_configuration",
            "amount_php": price, "price_type": "historical_ph_launch_srp",
            "source_published_at": "2021-05-14", "observed_at": OBSERVED,
            "source_url": URL_PTG, "source_kind": "historical_ph_launch_price_report",
            "local_availability_verified": True,
            "availability_status": "historical_launch_srp_not_current_price",
            "review_status": "VERIFIED_SECONDARY",
            "excerpt": f"Philippine launch report lists PHP {price:,} for ASUS Zenfone 8 {ram} GB / {storage} GB; dated May 14, 2021 and not a current offer.",
        })
    discovery = [
        {"device_id": DEVICE, "source_url": URL_ASUS, "result": "ASUS global exact-model specifications reviewed; regional bands/Wi-Fi caveats retained."},
        {"device_id": DEVICE, "source_url": URL_PTG, "result": "Exact PH page confirms 8/128 and 16/256 configurations, historical SRPs and local launch specifications."},
        {"device_id": DEVICE, "source_url": URL_LAUNCH, "result": "Contemporaneous ASUS Philippines launch coverage identifies May 14 preorder start and the two local configurations/SRPs."},
        {"device_id": DEVICE, "source_url": URL_TECHNO, "result": "Independent Philippine launch and price cross-check; Wi-Fi mode conflicts with PTG."},
        {"device_id": DEVICE, "source_url": URL_MODEL_CODE, "result": "ASUS maps Zenfone 8 to model number ZS590KS; no local numeric SKU identified."},
        {"device_id": DEVICE, "source_url": URL_SUPPORT, "result": "Official ASUS support page lists two OS upgrades, security updates through 2023, and hardware support through 2024."},
        {"device_id": DEVICE, "source_url": URL_QUALCOMM, "result": "Chipset manufacturer confirms Snapdragon 888 platform, Kryo 680, Adreno 660 and 5 nm node."},
        {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Exact global model profile used for identity/configuration cross-check only; no global option promoted to PH inventory."},
        {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "Exact page returned HTTP 402; no restricted content accessed or bypassed."},
        {"device_id": DEVICE, "source_url": URL_NANOREVIEW, "result": "No exact Zenfone 8 profile located in this pass."},
        {"device_id": DEVICE, "source_url": URL_COMMONS, "result": "Exact ZS590KS image visually reviewed; CC BY-SA 4.0 attribution and share-alike metadata recorded."},
    ]
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "ASUS", "model_name": "Zenfone 8", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [], "discovery": discovery, "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    model = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if model:
        model["status"] = "manually_reviewed"
    else:
        latest.setdefault("models", []).append(snapshot["models"][0])
    known = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type"), p.get("source_url"), p.get("configuration_match")) for p in latest.get("prices", [])}
    for price in prices:
        key = (price["device_id"], price["configuration_id"], price["price_type"], price["source_url"], price["configuration_match"])
        if key not in known:
            latest.setdefault("prices", []).append(price)
            known.add(key)
    latest["run_at"] = OBSERVED
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summaries = []
    for config_id, ram, storage, price in ((CONFIG_8, 8, 128, 34995), (CONFIG_16, 16, 256, 39995)):
        rows = fields(ram, storage, price)
        summaries.append({
            "configuration": f"{ram} GB / {storage} GB",
            "reviewedFields": len(rows),
            "statuses": dict(Counter(row["status"] for row in rows)),
            "historicalLaunchPricePhp": price,
            "currentPricePhp": None,
        })
    unavailable.pop(DEVICE, None)
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "workbookRow": 3, "model": "ASUS Zenfone 8", "modelNumber": "ZS590KS",
        "configurations": summaries, "sources": len(SOURCES),
        "philippinePreorderStart": "2021-05-14",
        "image": "exact model, visually reviewed, CC BY-SA 4.0; ready for catalog caching",
        "studyScope": "Pending (preserved)",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
