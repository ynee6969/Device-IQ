#!/usr/bin/env python3
"""Research the Philippine ZTE Blade V41 Vita 5G configuration."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_bf5cf152c95ed1"
CONFIG = "device_bf5cf152c95ed1-6gb-128gb"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/zte-blade-v41-vita-ph-prices-2026-11-27.json"

URL_ZTE = "https://global.ztedevices.com/products/zte-blade-v41-vita-5g"
URL_ZTE_BLOG = "https://global.ztedevices.com/blogs/news/explore-the-sharp-camera-of-the-blade-v41-vita"
URL_ZTE_VIDEO = "https://www.youtube.com/watch?v=l8DhB-XHvpM"
URL_GIZ_LAUNCH = "https://www.gizguide.com/2023/02/zte-blade-v41-5g-specs-ph.html"
URL_YUGA_LAUNCH = "https://www.yugatech.com/news/zte-makes-philippine-comeback-with-blade-series-smartphones/"
URL_GADGETMATCH = "https://www.gadgetmatch.com/zte-blade-series-redmagic-8-pro-now-in-the-philippines/"
URL_TECHNOBABOY = "https://www.technobaboy.com/2023/02/22/zte-launches-the-blade-series-in-the-philippines/"
URL_YUGA_REVIEW = "https://www.yugatech.com/mobile/zte-blade-v41-vita-5g-review/"
URL_YUGA_SPEC = "https://www.yugatech.com/spec/zte-blade-v41-vita-5g/"
URL_TEKNO = "https://www.teknogadyet.com/2023/02/zte-blade-v41-vita-5g-specs-price-review-philippines.html"
URL_PROMO = "https://www.gizguide.com/2023/07/zte-first-kiosk-philippines.html"
URL_SINGTEL = "https://cdn1.singteldigital.com/content/dam/singtel/personal/products-services/mobile/pdf/list-of-5g-sa-handsets.pdf"
URL_ZTE_MODEL_NOTICE = "https://www.ztedevices.com/cn/notice/%E7%BB%88%E7%AB%AFzte-7531n%E7%AD%8913%E6%AC%BE%E4%BA%A7%E5%93%81%E5%81%9C%E6%AD%A2%E5%B8%82%E5%9C%BA%E6%8E%A8%E5%B9%BF%E3%80%81%E5%81%9C%E6%AD%A2%E7%89%88%E6%9C%AC%E6%9B%B4%E6%96%B0%E5%85%AC%E5%91%8A/"
URL_GSMARENA = "https://www.gsmarena.com/zte_blade_v41_vita-12018.php"
IMAGE_URL = "https://cdn.shopify.com/s/files/1/0513/2229/0361/products/BladeV41Vita5G-hero.png?v=1670581371"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("zte_v41_global_product", URL_ZTE, "ZTE Devices", "Manufacturer product page, global configuration and image source",
        "Official global product page lists Dimensity 810, 6GB+128GB, 11GB including dynamic RAM, 6.6-inch IPS FHD+ display described as 60Hz, triple camera, 7.98mm thickness, 4500mAh battery and 22.5W charging. Its USD price and Notify Me control do not establish a current Philippine price or stock."),
    src("zte_v41_global_camera_article", URL_ZTE_BLOG, "ZTE Devices", "Manufacturer product article and rear camera cross-check",
        "Official article dated 2022-12-23 describes the V41 Vita's 7.98mm body, 50MP main camera, 2MP depth camera and 2MP macro camera.", "2022-12-23"),
    src("zte_v41_official_video", URL_ZTE_VIDEO, "ZTE Devices (official channel)", "Manufacturer product introduction and global configuration",
        "ZTE's official product-introduction video, published 2022-12-12, names the V41 Vita 5G and lists Dimensity 810, 6GB RAM, 128GB ROM, 4500mAh and 22.5W charging.", "2022-12-12"),
    src("zte_v41_gsmarena_announce", URL_GSMARENA, "GSMArena", "Independent model announcement and release-date cross-check",
        "Reports the Blade V41 Vita was announced 2022-12-07 and released 2022-12-23. Used as release timing; exact first-sale transaction is not independently established.", "2022-12-07"),
    src("zte_v41_model_singtel", URL_SINGTEL, "Singtel", "Model-code and 5G-standards identity cross-check",
        "Singtel's 5G SA handset list explicitly pairs ZTE 8140N with V41 Vita 5G. This is model identity/network support evidence, not Philippine availability."),
    src("zte_v41_model_notice", URL_ZTE_MODEL_NOTICE, "ZTE Corporation", "Manufacturer model-code cross-check",
        "ZTE's own end-of-promotion/software-update notice lists external model ZTE 8140N. The marketing-name link is corroborated separately by Singtel's device list.", "2024-04-28"),
    src("zte_v41_gizguide_ph", URL_GIZ_LAUNCH, "GIZGUIDE", "Contemporaneous Philippine launch, price and specifications",
        "Local article dated 2023-02-21 reports ZTE's Philippine return, V41 Vita 5G, PHP 11,999, Dimensity 810, 6GB/128GB, cameras, 4500mAh and 22.5W charge.", "2023-02-21"),
    src("zte_v41_yugatech_ph", URL_YUGA_LAUNCH, "YugaTech", "Philippine launch and price",
        "Local article dated 2023-02-21 reports the V41 Vita 5G in the Philippine Blade-series introduction and lists PHP 11,999 for 6GB+128GB.", "2023-02-21"),
    src("zte_v41_gadgetmatch_ph", URL_GADGETMATCH, "GadgetMatch", "Philippine release and configuration cross-check",
        "Article dated 2023-02-22 reports the Blade V41 Vita 5G released in the Philippines at PHP 11,999, with 6GB RAM and 128GB storage. Its publication date follows the 2023-02-21 launch reports.", "2023-02-22"),
    src("zte_v41_technobaboy_ph", URL_TECHNOBABOY, "Technobaboy", "Philippine configuration/specification cross-check",
        "Local report dated 2023-02-22 lists 6GB+128GB, 2408×1080, 90Hz, Wi-Fi 6, NFC, 5G/4G, dual SIM and local PHP 11,999 pricing.", "2023-02-22"),
    src("zte_v41_yuga_review", URL_YUGA_REVIEW, "YugaTech", "Hands-on Philippine review and specification-conflict review",
        "Review of a local unit reports a 60Hz display and a frosted-glass back; its own specification summary later lists 90Hz. The refresh-rate discrepancy is preserved as unresolved."),
    src("zte_v41_yuga_spec", URL_YUGA_SPEC, "YugaTech", "Philippine specification database cross-check",
        "Lists 6GB RAM, 128GB storage, 1080×2408, 90Hz, Dimensity 810, 50+2+2 cameras, Wi-Fi, Bluetooth 5.0, NFC, 5G and MyOS 12/Android 12."),
    src("zte_v41_teknogadyet", URL_TEKNO, "TeknoGadyet", "Philippine configuration, camera, connectivity and historical launch-price cross-check",
        "Local coverage lists one 6GB/128GB configuration at PHP 11,999, 1080p/30 video, 1TB microSD, Wi-Fi 6, Bluetooth 5, NFC, 5G/4G, USB-C OTG, Li-Po 4500mAh battery and a July 2023 promotional price context."),
    src("zte_v41_promo", URL_PROMO, "GIZGUIDE", "Historical Philippine retail promotion",
        "ZTE kiosk opening story dated 2023-07-17 reports a temporary V41 Vita 5G reduction from PHP 11,999 SRP to PHP 9,999 through July 31, 2023.", "2023-07-17"),
    src("zte_v41_current_price_check", URL_ZTE, "ZTE Devices", "Current price research and stock limitation",
        "Checked 2026-11-27. The official global page displays USD 229 and a Notify Me control; it does not publish a PHP price or establish Philippine stock. YugaTech's Philippine price-list history for this model is dated 2023, so no current PHP price is asserted."),
]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      catalog_value=None, price_type: str | None = None,
      price_observed: str | None = None, price_condition: str | None = None,
      listing_status: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key,
                    "catalogValue": normalized if catalog_value is None else catalog_value})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    if price_type:
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed
        row["priceCondition"] = price_condition or "new"
    if listing_status:
        row["listingStatus"] = listing_status
    return row


def nd(fid: str, sid: str, description: str, note: str | None = None) -> dict:
    return f(fid, sid, description, None, status="NOT_DISCLOSED",
             note=note or "The reviewed sources do not publish this exact value; it remains blank rather than inferred.")


def na(fid: str, sid: str, description: str, note: str) -> dict:
    return f(fid, sid, description, None, status="NOT_APPLICABLE", note=note)


def conflict(fid: str, sid: str, description: str, evidence: list[dict], note: str,
             key: str | None = None) -> dict:
    row = f(fid, sid, description, None, status="CONFLICTING_INFORMATION",
            key=key, catalog_value=None, note=note)
    row["candidateEvidence"] = evidence
    return row


def ev(value: str, url: str, source_kind: str, excerpt: str, match: str) -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": match, "reviewStatus": "CONFLICTING_INFORMATION"}


def fields() -> list[dict]:
    refresh = conflict(
        "display_refresh_rate", "zte_v41_global_product",
        "ZTE's global product page and YugaTech's hands-on review say 60Hz; multiple Philippine launch/specification sources say 90Hz.",
        [ev("60 Hz", URL_ZTE, "manufacturer_primary_global", "IPS 6.6-inch FHD+ 60Hz Display", "ZTE Blade V41 Vita 5G 6GB/128GB global listing"),
         ev("60 Hz", URL_YUGA_REVIEW, "hands_on_philippines", "The review body describes the tested panel at 60 Hz.", "Philippine review unit"),
         ev("90 Hz", URL_GIZ_LAUNCH, "secondary_philippines", "Launch report describes a 90Hz display.", "Philippine launch record"),
         ev("90 Hz", URL_TECHNOBABOY, "secondary_philippines", "Display listed as 2408×1080, 90Hz.", "Philippine launch record"),
         ev("90 Hz", URL_YUGA_SPEC, "secondary_philippines", "Specification database lists 90Hz; the same publisher's hands-on body says 60Hz.", "Philippine device entry")],
        "The manufacturer global page, a hands-on PH review, and local launch/specification sheets disagree. No refresh rate is published until the regional hardware specification is resolved.",
        key="refreshHz")
    resolution = conflict(
        "display_resolution", "zte_v41_technobaboy_ph",
        "Local Philippine pages report both 2408×1080 and 2400×1080; ZTE's global page says FHD+ without the pixel dimensions.",
        [ev("2408 × 1080", URL_TECHNOBABOY, "secondary_philippines", "2408×1080", "Philippine launch listing"),
         ev("1080 × 2408", URL_YUGA_SPEC, "secondary_philippines", "1080 x 2408", "Philippine spec database"),
         ev("2400 × 1080", URL_GIZ_LAUNCH, "secondary_philippines", "2400 x 1080", "Philippine launch listing")],
        "The pixel-count mismatch is unresolved; retain FHD+ only in the display note, not as a fabricated exact pixel value.",
        key="resolution")
    sim = conflict(
        "sim_esim", "zte_v41_gadgetmatch_ph",
        "GadgetMatch reports two SIM slots plus a microSD slot; TeknoGadyet reports microSD uses SIM 2, implying a hybrid tray.",
        [ev("2 SIM slots + 1 microSD slot", URL_GADGETMATCH, "secondary_philippines", "Slots: 2x SIM card, 1x microSD", "Philippine launch article"),
         ev("microSD uses SIM 2 slot", URL_TEKNO, "secondary_philippines", "128GB expandable storage, expandable up to 1TB via microSD card, uses SIM 2 slot", "Philippine model listing")],
        "Sources disagree about whether the microSD card shares the second SIM tray. Keep the tray layout unresolved.",
        key="sim")
    rows = [
        f("model_number", "zte_v41_model_singtel", "ZTE 8140N V41 Vita 5G", "8140N", status="VERIFIED_SECONDARY",
          note="Singtel explicitly pairs model 8140N with V41 Vita 5G; a ZTE corporate notice also lists external model 8140N."),
        f("global_release_date", "zte_v41_gsmarena_announce", "GSMArena reports released 2022-12-23 (announced 2022-12-07); ZTE's own product introduction video followed on 2022-12-12", "2022-12-23", status="VERIFIED_SECONDARY",
          note="Independent exact-model listing reports 2022-12-23 as release; the product was announced 2022-12-07. ZTE's official introduction video was published 2022-12-12. Exact first-sale transaction is not established."),
        f("configuration", "zte_v41_gadgetmatch_ph", "Philippine V41 Vita 5G: 6GB RAM / 128GB storage; ZTE also advertises up to 5GB dynamic RAM", "6 GB RAM / 128 GB storage",
          note="The 5GB dynamic RAM is software memory, not a distinct physical-RAM configuration. PH sources identify one 6GB/128GB version; no extra variants are merged."),
        f("philippine_release_date", "zte_v41_yugatech_ph", "YugaTech reported ZTE's Philippine Blade-series introduction on 2023-02-21; follow-up coverage on Feb 22 reported the phones released locally", "2023-02-21", status="VERIFIED_SECONDARY",
          note="The earliest contemporaneous PH coverage dates the official local launch to Feb 21; Feb 22 sources report the same local release after the event."),
        f("official_launch_price_php", "zte_v41_gadgetmatch_ph", "PHP 11,999 Philippine suggested retail price for 6GB/128GB", 11999, status="VERIFIED_SECONDARY", unit="PHP",
          price_type="Historical Philippine launch suggested retail price", price_observed="2023-02-21",
          note="Contemporaneous local launch coverage reports PHP 11,999; YugaTech, GIZGUIDE and Technobaboy corroborate the launch price."),
        f("current_price_php", "zte_v41_current_price_check", "No current PHP price found for Philippine sale. ZTE global page lists USD 229 with a Notify Me control; PH price-list data is historical.", None,
          status="UNAVAILABLE_AFTER_RESEARCH", unit="PHP",
          note="No dated current Philippine retailer price was found. Historical PHP 11,999 launch and PHP 9,999 July 2023 promotion remain separate observations; no price is shown as current."),
        f("display_size", "zte_v41_global_product", "6.6-inch display; some local specification listings report 6.67 inches", 6.6, key="displayInches", unit="in",
          note="Manufacturer and local launch coverage use 6.6 inches; 6.67 inches is a more precise secondary database value and is not treated as a conflicting panel size."),
        f("display_technology", "zte_v41_global_product", "IPS display; Philippine launch references identify IPS LCD", "IPS LCD", key="displayType"),
        resolution,
        refresh,
        nd("display_brightness", "zte_v41_global_product", "No numeric brightness value is published in the reviewed manufacturer or Philippine launch sources."),
        nd("display_protection", "zte_v41_global_product", "Display cover-glass protection is not identified in the reviewed manufacturer or PH sources."),
        f("chipset", "zte_v41_global_product", "MediaTek Dimensity 810 8-core 5G processor", "MediaTek Dimensity 810 (6 nm)", key="chipset"),
        f("process_node", "zte_v41_gizguide_ph", "MediaTek Dimensity 810 manufactured on 6nm process", 6, unit="nm"),
        f("cpu", "zte_v41_gizguide_ph", "Octa-core: 2× Cortex-A76 up to 2.4 GHz + 6× Cortex-A55 up to 2.0 GHz", "2x Cortex-A76 @ 2.4GHz + 6x Cortex-A55 @ 2.0GHz", key="cpu", status="VERIFIED_SECONDARY"),
        f("gpu", "zte_v41_gizguide_ph", "ARM Mali-G57 MC2", "ARM Mali-G57 MC2", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", "zte_v41_global_product", "Android 12 with MyOS 12", "Android 12 with MyOS 12", key="os", status="VERIFIED_SECONDARY"),
        nd("os_support", "zte_v41_model_notice", "ZTE's notice says software version updates for external model 8140N ended on 2024-04-28, but no published OS/security support period or guaranteed update schedule was found."),
        f("ram_capacity", "zte_v41_global_product", "6 GB physical RAM plus up to 5 GB Dynamic RAM", 6, key="ramGb", unit="GB",
          note="Catalog RAM is 6GB physical RAM only. The advertised dynamic RAM is software-backed and not added to the installed capacity."),
        nd("ram_type", "zte_v41_global_product", "RAM type is not identified on ZTE's product page or the reviewed PH launch sources."),
        f("storage_capacity", "zte_v41_global_product", "128 GB ROM", 128, key="storageGb", unit="GB"),
        f("storage_type", "zte_v41_gizguide_ph", "128 GB UFS 2.2 storage", "UFS 2.2", status="VERIFIED_SECONDARY"),
        f("storage_expansion", "zte_v41_teknogadyet", "Expandable by microSD up to 1 TB; TeknoGadyet reports the card uses SIM 2", "microSD up to 1 TB", status="VERIFIED_SECONDARY",
          note="The capacity is reported by a local source; the tray-sharing detail remains unresolved in the separate SIM field."),
        f("rear_camera_system", "zte_v41_global_camera_article", "50 MP main + 2 MP macro + 2 MP depth cameras", "50 MP main + 2 MP macro + 2 MP depth", key="rearCameraMp", catalog_value=50, unit="MP"),
        nd("main_camera_sensor", "zte_v41_global_camera_article", "The exact image sensor supplier/model is not disclosed in the reviewed sources."),
        na("ultrawide_camera", "zte_v41_global_camera_article", "The documented rear-camera set is one main, one macro and one depth camera; no ultrawide module is listed.", "Not applicable to the documented triple-camera system; no ultrawide lens is listed."),
        na("telephoto_camera", "zte_v41_global_camera_article", "The documented rear-camera set is one main, one macro and one depth camera; no telephoto module is listed.", "Not applicable to the documented triple-camera system; no telephoto lens is listed."),
        f("front_camera", "zte_v41_gizguide_ph", "8 MP front camera", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", "zte_v41_teknogadyet", "Front and rear cameras record up to 1080p at 30fps", "1080p at 30fps", status="VERIFIED_SECONDARY", key="video"),
        f("battery_capacity", "zte_v41_global_product", "4500 mAh battery", 4500, key="batteryMah", unit="mAh"),
        f("battery_technology", "zte_v41_teknogadyet", "4500mAh non-removable lithium-ion polymer battery", "Li-Po; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", "zte_v41_global_product", "22.5 W charging", 22.5, key="chargingW", unit="W"),
        nd("wireless_charging", "zte_v41_global_product", "Wireless/reverse charging is not specified on the reviewed manufacturer page; no unsupported 0 W value is assigned."),
        f("dimensions", "zte_v41_global_product", "7.98 mm body thickness; length and width not recorded by the reviewed ZTE page", "7.98 mm thick; length/width not recorded", key="dimensions", unit="mm",
          note="Only the official manufacturer's thickness value is published here; no dimensions are inferred from unrelated market databases."),
        nd("weight", "zte_v41_global_product", "The reviewed manufacturer page does not publish a device weight."),
        f("materials", "zte_v41_yuga_review", "YugaTech's hands-on review describes a frosted-glass back; frame material is not confirmed", "Frosted-glass back; frame not recorded", status="VERIFIED_SECONDARY",
          note="This is a reviewer observation of a local unit; the reviewer says the frame appears plastic-metal, which is not treated as a confirmed material specification."),
        nd("ingress_protection", "zte_v41_global_product", "No IP ingress-protection rating is stated in the reviewed ZTE product page or PH launch sources."),
        sim,
        f("cellular_bands", "zte_v41_gadgetmatch_ph", "5G SA/NSA and 4G LTE; exact Philippine frequency bands are not stated in the reviewed local coverage", "5G SA/NSA; 4G LTE (frequency bands not recorded)", key="cellular", status="VERIFIED_SECONDARY",
          note="Singtel's model-code list corroborates the device as a 5G SA handset. No Philippine band list is inferred from other regional models."),
        f("wifi", "zte_v41_yuga_spec", "Wi-Fi 6 (dual-band; exact radio configuration not otherwise listed)", "Wi-Fi 6, dual-band", key="wifi", status="VERIFIED_SECONDARY"),
        f("bluetooth", "zte_v41_yuga_spec", "Bluetooth 5.0", "Bluetooth 5.0", status="VERIFIED_SECONDARY"),
        f("usb", "zte_v41_teknogadyet", "USB Type-C 2.0 with USB OTG", "USB Type-C 2.0; OTG", key="ports", status="VERIFIED_SECONDARY"),
        f("nfc", "zte_v41_technobaboy_ph", "NFC supported", "NFC supported", status="VERIFIED_SECONDARY"),
        f("gnss", "zte_v41_teknogadyet", "GPS with A-GPS, GLONASS, BeiDou and Galileo", "GPS, A-GPS, GLONASS, BeiDou, Galileo", status="VERIFIED_SECONDARY"),
        f("audio", "zte_v41_yuga_review", "3.5 mm headphone jack; single downward-firing loudspeaker", "3.5 mm headphone jack; mono bottom-firing speaker", status="VERIFIED_SECONDARY", key="sound"),
        f("sensors", "zte_v41_teknogadyet", "Side-mounted fingerprint, light, proximity, accelerometer and gyroscope sensors", "Side fingerprint; light; proximity; accelerometer; gyroscope", status="VERIFIED_SECONDARY"),
    ]
    if len(rows) != 46 or len({row["fieldId"] for row in rows}) != 46:
        raise ValueError(f"Expected 46 distinct field reviews, got {len(rows)}")
    return rows


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the workbook's pending Blade V41 record; refusing unexpected scope/device.")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != f"{DEVICE}-unrecorded":
        raise ValueError("Expected one unrecorded placeholder configuration; review before replacing it.")

    replacement = {"id": CONFIG, "label": "6 GB RAM / 128 GB storage (5G)",
                   "modelCode": "8140N", "notes": "Philippine launch sources identify one 6GB/128GB configuration; 5GB Dynamic RAM is software-backed and not a separate variant."}
    review = {
        "deviceId": DEVICE, "configurationId": CONFIG, "brand": "ZTE",
        "model": "Blade V41 Vita 5G", "configuration": "6 GB RAM / 128 GB storage",
        "configurationLabel": replacement["label"], "modelCode": "8140N",
        "replacementVariants": [replacement], "replaceUnrecordedPlaceholder": True,
        "sources": SOURCES, "fields": fields(),
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Verified historical Philippine availability: ZTE V41 Vita 5G, model 8140N, 6 GB / 128 GB; local Blade launch coverage dates the introduction to 2023-02-21 and reports PHP 11,999 launch pricing. Current Philippine stock/price is not verified.",
            "philippineAvailability": "Verified historical Philippine availability: ZTE Blade V41 Vita 5G, 6 GB / 128 GB, reported locally in February 2023.",
            "observedAt": OBSERVED,
            "qualityFlag": "Manually reviewed; one PH configuration matched; current price, display rate/resolution and SIM tray layout remain unresolved.",
            "catalogModel": "Blade V41 Vita 5G",
            "manufacturer": "ZTE",
            "productLine": "Blade V41",
            "modelNumber": "8140N",
            "philippineReleaseYear": 2023,
            "philippineDateLabel": "Reported Philippine launch date",
            "researchNotes": "Workbook row 167 is matched to ZTE model 8140N / Blade V41 Vita 5G and the sole PH launch configuration documented in local sources, 6 GB RAM / 128 GB storage. The 5 GB Dynamic RAM figure is software extension, not installed RAM. A licensed exact-model image was not located. The manufacturer product render is retained only as an identity/source reference because republishing permission is not documented. Study eligibility remains Pending.",
            "openIssues": [
                {"issue": "No current Philippine price or stock evidence was found", "action": "Keep current price blank; show only dated launch and promotional prices."},
                {"issue": "Refresh rate conflicts between the manufacturer global page and Philippine reports; even YugaTech's review body and spec summary disagree", "action": "Keep normalized refresh rate blank until the regional specification is resolved."},
                {"issue": "Pixel resolution and SIM/microSD tray layout conflict across local references", "action": "Keep both values unresolved and retain cited source evidence."},
                {"issue": "Study eligibility remains Pending", "action": "Keep workbook eligibility unchanged until the thesis screening rule is applied."},
                {"issue": "Manufacturer product image is exact-model, but reuse rights are not documented", "action": "Keep the neutral unavailable-image placeholder and preserve the source URL for future rights review."},
            ],
        },
    }
    add_review(manual, catalog, review)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    saved = next(row for row in manual["records"]
                 if row.get("deviceId") == DEVICE and row.get("configurationId") == CONFIG)
    saved.update({"model": "Blade V41 Vita 5G", "configuration": "6 GB RAM / 128 GB storage",
                  "configurationLabel": replacement["label"]})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact ZTE Blade V41 Vita 5G product image is shown on the manufacturer page, but no reuse license or permission to republish/hotlink the render was documented. Keep the neutral placeholder.",
        "sourcePage": URL_ZTE,
        "assetUrl": None,
        "candidateAssetUrl": IMAGE_URL,
        "scope": "Exact ZTE Blade V41 Vita 5G / 8140N model render; color/configuration not stated on the image itself.",
        "rightsTermsUrl": None,
        "rightsCheck": "Reviewed the ZTE global product page and its purchase information. No image reuse license was found. Do not download or hotlink; no access controls were bypassed.",
        "rightsCheckSourcePage": URL_ZTE,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for ZTE Blade V41 Vita 5G",
    }
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 11999, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_blade_v41_vita_5g_8140n_6gb_128gb",
         "variant_ram_gb": 6, "variant_storage_gb": 128,
         "price_type": "historical_ph_launch_suggested_retail_price",
         "source_published_at": "2023-02-21",
         "excerpt": "Contemporaneous Philippine launch coverage reports the 6GB/128GB Blade V41 Vita 5G at PHP 11,999.",
         "source_url": URL_GIZ_LAUNCH, "source_kind": "historical_local_launch_price_report",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 9999, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_blade_v41_vita_5g_8140n_6gb_128gb",
         "variant_ram_gb": 6, "variant_storage_gb": 128,
         "price_type": "historical_local_kiosk_promotion",
         "source_published_at": "2023-07-17",
         "excerpt": "GIZGUIDE reports a temporary July 2023 ZTE kiosk offer reducing V41 Vita 5G from PHP 11,999 SRP to PHP 9,999 through July 31.",
         "source_url": URL_PROMO, "source_kind": "historical_local_promotion",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_promotion_not_current"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "ZTE", "model_name": "Blade V41 Vita 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": item["url"], "source_kind": item["purpose"], "status": "reviewed", "result": item["note"]} for item in SOURCES],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = {}
    for row in review["fields"]:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"workbookRow": 167, "model": "ZTE Blade V41 Vita 5G", "modelNumber": "8140N",
                      "configuration": replacement["label"], "reviewedFields": len(review["fields"]),
                      "fieldStatuses": counts, "sources": len(SOURCES),
                      "philippineLaunchDate": "2023-02-21", "launchPricePhp": 11999,
                      "historicPromoPricePhp": 9999, "currentPhpPrice": "not found",
                      "image": "official exact-model render identified; reuse rights not established; placeholder retained",
                      "studyScope": "Pending"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
