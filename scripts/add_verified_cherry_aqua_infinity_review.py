#!/usr/bin/env python3
"""Record exact-model research for the Cherry Mobile Aqua Infinity."""
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
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/cherry-aqua-infinity-ph-prices-2026-11-27.json"
OBSERVED = "2026-11-27"
DEVICE = "device_5695810422dccc"
CONFIG = f"{DEVICE}-auto-8gb-128gb"

URL_CHERRY = "https://cherry.com.ph/products/cherry-mobile-aqua-infinity"
URL_IMAGE = "https://cherry.com.ph/cdn/shop/products/Aqua_S9_Infinity_Black_1.jpg?v=1773381391&width=416"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/cherry-mobile-aqua-infinity"
URL_UNBOX_LAUNCH = "https://unbox.ph/gadget/cherry-mobile-makes-the-aqua-infinity-official-on-christmas-eve/"
URL_UNBOX_REVIEW = "https://unbox.ph/gadget/cherry-mobile-aqua-infinity-unboxing-review-philippines/"
URL_YUGATECH = "https://www.yugatech.com/news/cherry-mobile-aqua-infinity-philippines-price/"
URL_GIZGUIDE = "https://www.gizguide.com/2021/02/cherry-mobile-aqua-infinity-.html"
URL_NOYPI = "https://www.noypigeeks.com/deal-alert/cherry-mobile-discounted-lazada-birthday-sale/"
URL_NTC = "https://region4b.ntc.gov.ph/wp-content/uploads/2022/01/GEC_12312021.pdf"
URL_MEDIATEK = "https://www.mediatek.com/products/smartphones/mediatek-helio-p60"
URL_GSMARENA = "https://www.gsmarena.com/"
URL_NANOREVIEW = "https://nanoreview.net/"
URL_KIMOVIL = "https://www.kimovil.com/"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("cherry_aqua_infinity_official_shop", "CHERRY Shop / Cosmic Technologies Incorporated", URL_CHERRY,
        "Manufacturer shop, exact product identity/configuration, current listed price, stock status and specifications",
        "Official Philippine CHERRY Shop page names Aqua Infinity, lists the single 8 GB + 128 GB configuration, core specifications, colors, PHP 5,999 sale price (reduced from PHP 7,999), and marks the listing sold out. The page promotes a free Bluetooth speaker and Helo LX fitness band. The page's product image was visually checked but is not republished because no reusable image license or permission was located."),
    src("cherry_aqua_infinity_ptg", "Pinoy Techno Guide", URL_PTG,
        "Exact-model Philippine announcement, availability, configuration, historical SRP and technical specifications",
        "Dated 2020-12-18. Records an announcement date of 2020-12-17, PHP 7,999 official price, one 8 GB / 128 GB configuration, specifications and says it was already available through local stores, authorized dealers and online shops. This differs in timing from coverage that describes the official promotion as starting December 24; exact first sale date remains unresolved.", "2020-12-18"),
    src("cherry_aqua_infinity_unbox_launch", "UNBOX PH", URL_UNBOX_LAUNCH,
        "Contemporaneous Philippine launch/promotion date and introductory price",
        "Published 2020-12-23. Calls the Aqua Infinity official on Christmas Eve and lists an introductory PHP 6,999 price beginning December 24, versus PHP 7,999 retail price. It documents a launch promotion, not the exact first transaction.", "2020-12-23"),
    src("cherry_aqua_infinity_unbox_review", "UNBOX PH", URL_UNBOX_REVIEW,
        "Independent exact-model hardware and configuration review",
        "Published 2021-01-20. Identifies 8 GB LPDDR4X RAM, 128 GB UFS 2.1 storage, 12 MP f/2.2 main camera and 20 MP f/2.4 depth camera, Full HD main-camera video, and 10 W USB-C charging for the Aqua Infinity.", "2021-01-20"),
    src("cherry_aqua_infinity_yugatech", "YugaTech Philippines", URL_YUGATECH,
        "Contemporaneous Philippine launch, local availability and price cross-check",
        "Published 2020-12-23. Reports the local Aqua Infinity, 8 GB/128 GB configuration, PHP 7,999 SRP, and a PHP 6,999 introductory Lazada offer on December 24. This supports a December 2020 local launch window; the exact first-sale date differs from PTG's report.", "2020-12-23"),
    src("cherry_aqua_infinity_gizguide", "Gizguide Philippines", URL_GIZGUIDE,
        "Historical Philippine promotion and model-level specification cross-check",
        "Published 2021-02-26. Reports a PHP 6,999 promotional price cut from PHP 7,999 and the same exact Aqua Infinity 8 GB/128 GB configuration, Helio P60, cameras, battery, Android 10 and local official-store channel.", "2021-02-26"),
    src("cherry_aqua_infinity_noypigeeks_sale", "NoypiGeeks Philippines", URL_NOYPI,
        "Dated historical Philippine sale-price observation",
        "Published 2021-03-25. Reports CHERRY's March 27 Lazada Birthday Sale listing the Aqua Infinity at PHP 5,999 from PHP 7,999. This is an expired sale snapshot, not a current purchasable offer.", "2021-03-25"),
    src("cherry_aqua_infinity_ntc", "National Telecommunications Commission (Philippines)", URL_NTC,
        "Regulatory identity and equipment-certification record",
        "The NTC GEC list identifies CHERRY MOBILE AQUA INFINITY under certification ESD-GEC-2006347, applicant Cosmic Technologies Incorporated, issued 2020-10-27. The GEC number is a certification identifier, not a device SKU/model code; the combined radio-frequency column is not treated as a definitive cellular-band specification.", "2020-10-27"),
    src("mediatek_helio_p60", "MediaTek", URL_MEDIATEK,
        "Chipset manufacturer specifications",
        "MediaTek identifies Helio P60's Cortex-A73 big cores, Mali-G72 GPU family, LPDDR4X capability and TSMC 12 nm process. Phone-specific clock values are sourced from the exact-model PTG page."),
    src("cherry_aqua_infinity_image_rights", "CHERRY Shop / Cosmic Technologies Incorporated", URL_CHERRY,
        "Exact-model product-image match and rights review",
        f"The official product page image {URL_IMAGE} was visually checked against the CHERRY Aqua Infinity listing; it depicts the black Aqua Infinity with the circular rear-camera assembly. The page footer says © Cosmic Technologies Incorporated; no open license or written reuse permission for the image was found. The catalog retains its neutral placeholder."),
    src("cherry_aqua_infinity_gsmarena_search", "GSMArena", URL_GSMARENA,
        "Exact-model source discovery",
        "Searched for an exact Aqua Infinity model page; no matching GSMArena profile or article was located in this pass. No data is inferred from a similarly named device."),
    src("cherry_aqua_infinity_nanoreview_search", "NanoReview", URL_NANOREVIEW,
        "Exact-model source discovery",
        "Searched for an exact Aqua Infinity profile; no matching NanoReview page was located in this pass. No data is inferred from another Aqua model."),
    src("cherry_aqua_infinity_kimovil_search", "Kimovil", URL_KIMOVIL,
        "Exact-model source discovery",
        "Searched for an exact Aqua Infinity profile; no matching Kimovil model page was located in this pass. Global database values are not substituted."),
]


def f(fid: str, sid: str, source_value, normalized, *, status="VERIFIED",
      key=None, unit=None, note=None, price_type=None, price_observed=None,
      price_condition=None, listing_status=None, candidates=None,
      replace_existing=True):
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": source_value, "normalizedValue": normalized,
           "note": note or "Exact Cherry Mobile Aqua Infinity model reviewed; source and configuration limitations are recorded explicitly."}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if price_type:
        row.update({"priceType": price_type, "priceObservedAt": price_observed,
                    "priceCondition": price_condition or "new"})
    if listing_status:
        row["listingStatus"] = listing_status
    if candidates:
        row["candidateEvidence"] = candidates
    if replace_existing:
        row["replaceExisting"] = True
    return row


def nd(fid: str, sid: str, explanation: str, *, note=None):
    return f(fid, sid, explanation, None, status="NOT_DISCLOSED", note=note or explanation)


def unavailable(fid: str, sid: str, explanation: str):
    return f(fid, sid, explanation, None, status="UNAVAILABLE_AFTER_RESEARCH", note=explanation)


def candidate(value: str, url: str, source_kind: str, excerpt: str, match: str):
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": match,
            "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True}


def fields() -> list[dict]:
    date_candidates = [
        candidate("2020-12-18", URL_PTG, "independent_ph_reference",
                  "The exact PTG product page published 2020-12-18 says the Aqua Infinity is now available through stores, authorized dealers and online shops.",
                  "Exact Cherry Mobile Aqua Infinity; PTG publication date"),
        candidate("2020-12-24", URL_UNBOX_LAUNCH, "independent_ph_launch_report",
                  "Contemporaneous UNBOX coverage calls the phone official on Christmas Eve and says the introductory Lazada offer begins Dec 24.",
                  "Exact Cherry Mobile Aqua Infinity; official promotion/launch report"),
        candidate("2020-12-24", URL_YUGATECH, "independent_ph_launch_report",
                  "YugaTech's Dec 23 report gives the Dec 24 introductory offer and local official-store availability.",
                  "Exact Cherry Mobile Aqua Infinity; local promo availability"),
    ]
    return [
        nd("model_number", "cherry_aqua_infinity_ntc", "The exact marketing model is CHERRY / Cherry Mobile Aqua Infinity; no separate hardware model number or retail SKU was found. NTC ESD-GEC-2006347 is a regulatory certification ID, not a device model code.", note="Do not put the NTC certificate number in the model-number or SKU field."),
        unavailable("global_release_date", "cherry_aqua_infinity_ptg", "PTG records a December 17, 2020 announcement, but the reviewed sources do not establish a distinct worldwide release date; the local announcement is not treated as a global release date."),
        f("configuration", "cherry_aqua_infinity_official_shop", "CHERRY Shop lists the Aqua Infinity as 8 GB RAM + 128 GB storage; no other local memory/storage configuration was found.", "8 GB RAM / 128 GB storage", status="VERIFIED", note="The official product listing and local launch/review sources identify this same single configuration; no other capacity is merged into it."),
        f("philippine_release_date", "cherry_aqua_infinity_ptg", "PTG (published Dec 18, 2020) says the phone was already available; UNBOX and YugaTech describe the official launch/introductory offer as beginning Dec 24, 2020.", None, status="CONFLICTING_INFORMATION", note="Contemporaneous local reports disagree on whether availability began by Dec 18 or the official launch/promo began Dec 24. Keep the exact first-sale date blank; the Philippine availability year is 2020.", candidates=date_candidates),
        f("official_launch_price_php", "cherry_aqua_infinity_ptg", "PHP 7,999 official Philippine price for 8 GB / 128 GB; contemporaneous launch sources report a PHP 6,999 introductory offer on Dec 24, 2020.", 7999, status="VERIFIED_SECONDARY", unit="PHP", note="Historical launch SRP; the separate PHP 6,999 introductory promotion is recorded in dated price history and is not the SRP or a current price.", price_type="historical_ph_launch_srp", price_observed="2020-12-18", price_condition="new"),
        f("current_price_php", "cherry_aqua_infinity_official_shop", "Official CHERRY Shop listed PHP 5,999 sale price, reduced from PHP 7,999, on 2026-11-27; product listing status is Sold out and it promotes a free Bluetooth speaker and Helo LX fitness band.", 5999, status="VERIFIED", unit="PHP", note="Dated official-store page price for the promoted package; the exact listing is marked Sold out, so this is not a purchasable current offer or a claim of stock.", price_type="Official CHERRY Shop sale listing · sold out", price_observed=OBSERVED, price_condition="new", listing_status="Out of stock"),
        f("display_size", "cherry_aqua_infinity_official_shop", "6.52-inch HD+ TrueView display", 6.52, key="displayInches", unit="in"),
        f("display_technology", "cherry_aqua_infinity_ptg", "6.52-inch HD+ IPS LCD TrueView display", "IPS LCD", status="VERIFIED_SECONDARY", key="displayType"),
        f("display_resolution", "cherry_aqua_infinity_official_shop", "720 x 1600 pixels", "720 x 1600", key="resolution"),
        unavailable("display_refresh_rate", "cherry_aqua_infinity_official_shop", "The reviewed exact-model manufacturer, launch and review sources do not publish a refresh-rate value; it remains unrecorded."),
        nd("display_brightness", "cherry_aqua_infinity_official_shop", "No numeric display brightness or measurement standard is stated in the reviewed exact-model sources."),
        nd("display_protection", "cherry_aqua_infinity_official_shop", "No display-glass protection material or scratch-resistance rating is stated in the reviewed exact-model sources."),
        f("chipset", "cherry_aqua_infinity_official_shop", "MediaTek Helio P60 processor", "MediaTek Helio P60", key="chipset"),
        f("process_node", "mediatek_helio_p60", "TSMC 12 nm FinFET process", 12, status="VERIFIED", unit="nm", note="Chipset-maker process specification for Helio P60, not a phone-level performance estimate."),
        f("cpu", "cherry_aqua_infinity_ptg", "Octa-core: 4 x Cortex-A73 at 2.0 GHz + 4 x Cortex-A53 at 2.0 GHz.", "Octa-core: 4 x Cortex-A73 @ 2.0 GHz + 4 x Cortex-A53 @ 2.0 GHz", status="VERIFIED_SECONDARY", key="cpu"),
        f("gpu", "mediatek_helio_p60", "Arm Mali-G72 GPU; exact model specification identifies Mali-G72 MP3.", "Arm Mali-G72 MP3", status="VERIFIED_SECONDARY", key="gpu", note="MediaTek identifies the P60's Mali-G72 family; PTG's exact Aqua Infinity specification gives the MP3 variant."),
        f("operating_system", "cherry_aqua_infinity_official_shop", "Android 10", "Android 10", key="os"),
        unavailable("os_support", "cherry_aqua_infinity_official_shop", "No model-specific OS upgrade or security-update commitment was found in the reviewed official and exact-model sources."),
        f("ram_capacity", "cherry_aqua_infinity_official_shop", "8 GB memory", 8, key="ramGb", unit="GB"),
        f("ram_type", "mediatek_helio_p60", "MediaTek Helio P60 supports LPDDR4X; UNBOX's exact Aqua Infinity review identifies 8 GB LPDDR4X.", "LPDDR4X", status="VERIFIED_SECONDARY", key="ramType", note="Exact-model UNBOX review supplies the configured RAM type; MediaTek chipset page confirms platform support."),
        f("storage_capacity", "cherry_aqua_infinity_official_shop", "128 GB internal storage", 128, key="storageGb", unit="GB"),
        f("storage_type", "cherry_aqua_infinity_unbox_review", "128 GB UFS 2.1 storage", "UFS 2.1", status="VERIFIED_SECONDARY", key="storageType"),
        f("storage_expansion", "cherry_aqua_infinity_official_shop", "Expandable storage up to 256 GB; triple-card tray.", "microSD expansion up to 256 GB; separate triple-card tray"),
        f("rear_camera_system", "cherry_aqua_infinity_ptg", "Quad rear cameras: 12 MP main, 20 MP depth, 2 MP monochrome and 2 MP AI camera.", "12 MP main + 20 MP depth + 2 MP monochrome + 2 MP AI rear-camera system"),
        f("main_camera_sensor", "cherry_aqua_infinity_unbox_review", "12 MP main camera, f/2.2, autofocus; sensor make/model not identified.", "12 MP main; f/2.2; autofocus; sensor model not recorded", status="VERIFIED_SECONDARY"),
        f("ultrawide_camera", "cherry_aqua_infinity_ptg", "The exact-model four-camera list consists of main, depth, monochrome and AI modules; no separate ultrawide camera is listed.", None, status="NOT_APPLICABLE", note="The exact local camera list identifies all four modules and none is ultrawide."),
        f("telephoto_camera", "cherry_aqua_infinity_ptg", "The exact-model four-camera list contains no telephoto module.", None, status="NOT_APPLICABLE", note="The product's reported camera modules are main, depth, monochrome and AI; none is a telephoto camera."),
        f("front_camera", "cherry_aqua_infinity_official_shop", "8 MP front camera", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", "cherry_aqua_infinity_unbox_review", "Main rear camera records Full HD video; the source does not state frame rates.", "Main rear video up to Full HD; frame rate not recorded", status="VERIFIED_SECONDARY"),
        f("battery_capacity", "cherry_aqua_infinity_official_shop", "4000 mAh removable battery", 4000, key="batteryMah", unit="mAh"),
        f("battery_technology", "cherry_aqua_infinity_ptg", "4000 mAh Li-ion removable battery", "Lithium-ion; removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", "cherry_aqua_infinity_unbox_review", "10 W USB-C charging", 10, status="VERIFIED_SECONDARY", key="chargingW", unit="W"),
        nd("wireless_charging", "cherry_aqua_infinity_official_shop", "Wireless and reverse charging are not stated in the reviewed exact-model sources."),
        f("dimensions", "cherry_aqua_infinity_official_shop", "162 x 75 x 9.3 mm", "162 x 75 x 9.3 mm", key="dimensions", unit="mm"),
        f("weight", "cherry_aqua_infinity_official_shop", "192 g", 192, key="weightG", unit="g"),
        f("materials", "cherry_aqua_infinity_ptg", "Plastic build", "Plastic", status="VERIFIED_SECONDARY"),
        nd("ingress_protection", "cherry_aqua_infinity_official_shop", "No IP or ingress-protection rating is stated by the manufacturer page or reviewed exact-model launch sources."),
        f("sim_esim", "cherry_aqua_infinity_official_shop", "Dual SIM dual standby; triple-card tray. eSIM is not documented.", "Dual SIM dual standby; separate triple-card tray; eSIM not recorded", key="sim"),
        f("cellular_bands", "cherry_aqua_infinity_ptg", "4G LTE, 3G HSPA+, 2G EDGE/GPRS; exact cellular frequency bands are not documented by the local product specification.", "4G LTE; 3G HSPA+; 2G EDGE/GPRS; exact cellular bands not recorded", status="VERIFIED_SECONDARY", key="cellular"),
        f("wifi", "cherry_aqua_infinity_ptg", "Wi-Fi 802.11 b/g/n; supported frequency bands are not stated.", "Wi-Fi 802.11 b/g/n; band support not recorded", status="VERIFIED_SECONDARY", key="wifi"),
        f("bluetooth", "cherry_aqua_infinity_ptg", "Bluetooth is listed; version is not stated.", "Bluetooth supported; version not recorded", status="VERIFIED_SECONDARY"),
        f("usb", "cherry_aqua_infinity_official_shop", "USB Type-C charging; data protocol/speed is not stated.", "USB Type-C; data protocol not recorded", key="ports"),
        f("nfc", "cherry_aqua_infinity_ptg", "PTG's exact-model specification lists NFC: No.", "No NFC", status="VERIFIED_SECONDARY"),
        f("gnss", "cherry_aqua_infinity_ptg", "A-GPS listed; other satellite constellations are not stated.", "A-GPS; other constellations not recorded", status="VERIFIED_SECONDARY"),
        f("audio", "cherry_aqua_infinity_ptg", "3.5 mm audio jack; speaker count/type is not specified.", "3.5 mm audio jack; speaker configuration not recorded", status="VERIFIED_SECONDARY", key="sound"),
        f("sensors", "cherry_aqua_infinity_ptg", "Gyroscope, compass, ambient-light sensor, proximity sensor and accelerometer.", "Gyroscope; compass; ambient-light sensor; proximity sensor; accelerometer", status="VERIFIED_SECONDARY"),
    ]


def date_availability() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Exact CHERRY Aqua Infinity 8 GB / 128 GB model is documented in Philippine launch coverage and on CHERRY Shop. The exact first-sale day is unresolved; the current official shop page is marked Sold out as of 2026-11-27.",
        "philippineAvailability": "Philippine availability is verified for the Cherry Mobile Aqua Infinity 8 GB / 128 GB model. PTG reported it available by its 2020-12-18 page date; UNBOX and YugaTech describe the official launch/introductory offer on 2020-12-24. The first-sale date remains unresolved. CHERRY Shop's 2026-11-27 page is sold out.",
        "observedAt": OBSERVED,
        "manufacturer": "Cosmic Technologies Incorporated",
        "productLine": "Aqua",
        "catalogModel": "Aqua Infinity",
        "philippineReleaseYear": 2020,
        "philippineDateLabel": "Philippine availability documented in December 2020; exact first-sale date unresolved",
        "researchNotes": "Workbook row 5's Cherry Mobile Aqua Infinity is matched to the exact CHERRY Aqua Infinity product listing, one 8 GB / 128 GB configuration. NTC GEC ESD-GEC-2006347 is an equipment-certification identifier, not a device model/SKU. PTG's Dec 18, 2020 page says it was already available; contemporaneous launch reports place official launch/promotion on Dec 24, so no exact first-sale date is selected. The current official price page shows PHP 5,999 but is marked sold out and promotes a speaker/fitness-band bundle. The exact official product image is not reused because image rights were not established. Workbook eligibility remains Pending.",
        "qualityFlag": "Exact model/configuration and PH availability verified; December first-sale date unresolved; official current page is sold out; product-image reuse rights not established; study scope remains Pending.",
        "openIssues": [
            {"issue": "Local sources differ on availability by 2020-12-18 versus official promo/launch on 2020-12-24", "action": "Keep the exact first-sale date blank and retain both dated sources."},
            {"issue": "CHERRY Shop lists PHP 5,999 but marks the listing Sold out", "action": "Show it only as a dated official-store price snapshot with sold-out status."},
            {"issue": "The exact-model official product photo has no reusable license or permission on record", "action": "Keep the neutral image placeholder."},
            {"issue": "The workbook lists 2021 while local launch coverage dates the model to December 2020", "action": "Keep the source workbook claim unchanged and show sourced announcement/availability dates separately."},
            {"issue": "Study scope remains Pending", "action": "Preserve workbook eligibility."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable_images = json.loads(IMAGE_UNAVAILABLE.read_text(encoding="utf-8"))
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("workbookRow") != 5 or device.get("brand") != "Cherry Mobile" or device.get("model") != "Aqua Infinity":
        raise SystemExit("Catalog target guard failed for workbook row 5 Cherry Mobile Aqua Infinity")
    if device.get("scopeStatus") != "Pending":
        raise SystemExit("Expected workbook scope Pending; refusing to change eligibility")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != CONFIG:
        raise SystemExit("Expected the single exact 8 GB / 128 GB Aqua Infinity configuration")
    if any(r.get("deviceId") == DEVICE and r.get("configurationId") != CONFIG for r in manual["records"]):
        raise SystemExit("Unexpected Aqua Infinity configuration review exists; inspect model match first")

    definitions = json.loads((ROOT / "research/enrichment/specification-fields.json").read_text(encoding="utf-8"))["smartphones"]
    expected_fields = {definition["id"] for definition in definitions}
    reviewed_fields = fields()
    actual_fields = {row["fieldId"] for row in reviewed_fields}
    if actual_fields != expected_fields or len(reviewed_fields) != len(expected_fields):
        raise SystemExit(f"Phone field set is incomplete/duplicated: missing={expected_fields - actual_fields}, extra={actual_fields - expected_fields}")
    item = {
        "deviceId": DEVICE, "configurationId": CONFIG,
        "brand": "Cherry Mobile", "model": "Aqua Infinity",
        "configuration": "8 GB RAM / 128 GB storage",
        "configurationLabel": "8 GB RAM / 128 GB storage",
        "sources": SOURCES, "fields": reviewed_fields,
        "availabilityEvidence": date_availability(),
    }
    add_review(manual, catalog, item)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    saved = next(r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == CONFIG)
    saved.update({"brand": "Cherry Mobile", "model": "Aqua Infinity",
                  "configuration": "8 GB RAM / 128 GB storage",
                  "configurationLabel": "8 GB RAM / 128 GB storage",
                  "modelCode": None, "sku": None})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable_images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact black CHERRY Aqua Infinity image is present on the official CHERRY Shop product page and was visually checked against the named product, including its circular rear-camera module. The page footer credits Cosmic Technologies Incorporated, but no open reuse license or written permission was found; do not republish it.",
        "sourcePage": URL_CHERRY,
        "assetUrl": URL_IMAGE,
        "scope": "Exact black Aqua Infinity model-level product image; it does not distinguish memory/storage beyond the exact product listing.",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Cherry Mobile Aqua Infinity",
    }
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable_images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "configuration_id": CONFIG, "variant_ram_gb": 8, "variant_storage_gb": 128,
         "configuration_match": "exact_ph_aqua_infinity_8gb_128gb", "amount_php": 7999,
         "price_type": "historical_ph_launch_srp", "source_published_at": "2020-12-18", "observed_at": OBSERVED,
         "source_url": URL_PTG, "source_kind": "historical_ph_launch_srp_report",
         "local_availability_verified": True, "availability_status": "historical_srp_not_current",
         "review_status": "VERIFIED_SECONDARY",
         "excerpt": "PTG's 2020-12-18 exact-model listing reports PHP 7,999 official price for Aqua Infinity 8 GB / 128 GB."},
        {"device_id": DEVICE, "configuration_id": CONFIG, "variant_ram_gb": 8, "variant_storage_gb": 128,
         "configuration_match": "exact_ph_aqua_infinity_8gb_128gb_launch_promo", "amount_php": 6999,
         "price_type": "historical_ph_introductory_price", "source_published_at": "2020-12-23", "observed_at": OBSERVED,
         "source_url": URL_UNBOX_LAUNCH, "source_kind": "historical_ph_launch_promotion",
         "local_availability_verified": True, "availability_status": "promo_from_2020-12-24_not_current",
         "review_status": "VERIFIED_SECONDARY",
         "excerpt": "UNBOX reports the PHP 6,999 introductory offer beginning Dec 24, 2020, compared with PHP 7,999 retail SRP."},
        {"device_id": DEVICE, "configuration_id": CONFIG, "variant_ram_gb": 8, "variant_storage_gb": 128,
         "configuration_match": "exact_ph_aqua_infinity_8gb_128gb_feb_2021_promo", "amount_php": 6999,
         "price_type": "historical_ph_promotion_bundle", "source_published_at": "2021-02-26", "observed_at": OBSERVED,
         "source_url": URL_GIZGUIDE, "source_kind": "historical_ph_promotion_report",
         "local_availability_verified": True, "availability_status": "dated_2021_promo_not_current",
         "review_status": "VERIFIED_SECONDARY",
         "excerpt": "Gizguide reports a PHP 6,999 sale and freebies in February 2021; not the launch SRP or a current offer."},
        {"device_id": DEVICE, "configuration_id": CONFIG, "variant_ram_gb": 8, "variant_storage_gb": 128,
         "configuration_match": "exact_ph_aqua_infinity_8gb_128gb_march_2021_sale", "amount_php": 5999,
         "price_type": "historical_lazada_sale_price", "source_published_at": "2021-03-25", "observed_at": OBSERVED,
         "source_url": URL_NOYPI, "source_kind": "historical_ph_sale_report",
         "local_availability_verified": True, "availability_status": "sale_on_2021-03-27_expired",
         "review_status": "VERIFIED_SECONDARY",
         "excerpt": "NoypiGeeks reports a PHP 5,999 Cherry Mobile Lazada Birthday Sale price for March 27, 2021; this promotion has expired."},
        {"device_id": DEVICE, "configuration_id": CONFIG, "variant_ram_gb": 8, "variant_storage_gb": 128,
         "configuration_match": "exact_official_cherry_shop_listing_8gb_128gb_sold_out", "amount_php": 5999,
         "price_type": "current_official_store_listing_sold_out_bundle", "source_published_at": None, "observed_at": OBSERVED,
         "source_url": URL_CHERRY, "source_kind": "official_ph_store_page_price_snapshot",
         "local_availability_verified": True, "availability_status": "listed_but_sold_out; free_speaker_and_helo_lx_band_promotion",
         "review_status": "VERIFIED",
         "excerpt": "Official CHERRY Shop page lists Aqua Infinity at PHP 5,999 reduced from PHP 7,999, promotes a free speaker and Helo LX band, and marks it Sold out as observed 2026-11-27."},
    ]
    discovery = [
        {"device_id": DEVICE, "source_url": URL_CHERRY, "result": "Official CHERRY Shop confirms exact name, 8/128 config, core specs, colors, current page price and sold-out listing."},
        {"device_id": DEVICE, "source_url": URL_PTG, "result": "Exact local page supports announcement date, launch SRP, availability by page date and broad specifications; date differs from Dec 24 launch coverage."},
        {"device_id": DEVICE, "source_url": URL_UNBOX_LAUNCH, "result": "Contemporaneous official-launch and introductory-price date cross-check."},
        {"device_id": DEVICE, "source_url": URL_UNBOX_REVIEW, "result": "Exact-model review cross-checks RAM/storage types, cameras, Full HD video and 10 W charging."},
        {"device_id": DEVICE, "source_url": URL_YUGATECH, "result": "Local launch and Dec 24 promo cross-check; page fetch returned 403 in this pass, search-index excerpt used."},
        {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "Dated 2021 promotion snapshot and exact-model configuration cross-check."},
        {"device_id": DEVICE, "source_url": URL_NOYPI, "result": "Dated March 2021 official-store sale-price observation."},
        {"device_id": DEVICE, "source_url": URL_NTC, "result": "Official GEC confirms exact marketing model and certification ID issued 2020-10-27; GEC ID not used as a SKU."},
        {"device_id": DEVICE, "source_url": URL_MEDIATEK, "result": "Chipset source confirms Helio P60 architecture family and 12 nm node."},
        {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "No exact-model profile located."},
        {"device_id": DEVICE, "source_url": URL_NANOREVIEW, "result": "No exact-model profile located."},
        {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "No exact-model profile located."},
        {"device_id": DEVICE, "source_url": URL_IMAGE, "result": "Official exact-model photo visually checked; reuse rights not established; neutral placeholder retained."},
    ]
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Cherry Mobile", "model_name": "Aqua Infinity", "category": "smartphones", "status": "manually_reviewed"}],
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

    summaries = {status: sum(row["status"] == status for row in reviewed_fields)
                 for status in sorted({row["status"] for row in reviewed_fields})}
    print(json.dumps({
        "workbookRow": 5, "model": "Cherry Mobile Aqua Infinity",
        "configuration": "8 GB RAM / 128 GB storage",
        "reviewedFields": len(reviewed_fields), "statuses": summaries,
        "announcementDate": "2020-12-17", "philippineReleaseDate": "unresolved within December 2020",
        "launchSrpPhp": 7999, "latestOfficialListedPricePhp": 5999,
        "officialStoreStock": "Sold out", "image": "exact official photo found; rights not established; placeholder retained",
        "studyScope": "Pending (preserved)",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
