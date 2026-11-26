#!/usr/bin/env python3
"""Add a source-backed Philippine review for the Motorola Edge 20 Pro row."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/motorola-edge-20-pro-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = "2026-11-26T15:15:13+08:00"
DEVICE = "device_cef4dc913ac418"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_GLOBAL = "https://motorolanews.com/its-time-to-find-your-edge-new-motorola-edge-20-pro-motorola-edge-20-motorola-edge-20-lite/"
URL_MOTO_DOC = "https://en-us.support.motorola.com/app/answers/detail/a_id/167829/p/11070"
URL_NTC_GEC = "https://region7.ntc.gov.ph/wp-content/uploads/2024/01/GEC_08312021.pdf"
URL_YUGA = "https://www.yugatech.com/news/motorola-edge-20-pro-specs-price-philippines/"
URL_REVU = "https://www.revu.com.ph/2021/10/motorola-edge-20-pro-fusion-price-ph/"
URL_VILLMAN = "https://villman.com/Product-Detail/motorola_moto-edge-20-pro-pany0015ph--67in-oled-hdr10--snapdragon-870--12gb-ram--256gb-rom-"
URL_IMAGE = "https://villman.com/product_photos/moto-edge-20-pro-gif-300px-102821_245k5.gif"
URL_QUALCOMM = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/prod_brief_qcom_sd870_5g.pdf"
URL_MANUAL = "https://help.motorola.com/hc/7120/12/pdf/help-motorola-edge-20-pro-12-global-en-us.pdf"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("edge20pro_motorola_global", "Motorola News", URL_GLOBAL,
           "Manufacturer global introduction date and product-family specifications",
           "Motorola's July 29, 2021 introduction identifies the Edge 20 Pro camera system, 6.7-inch OLED/144 Hz display, Wi-Fi 6, Snapdragon 870, 12 GB memory, 256 GB storage, 8K video, and Android 11. It describes the main sensor as 1/1.5-inch optical format; it does not identify a sensor part number or RAM type.",
           "2021-07-29"),
    source("edge20pro_motorola_doc", "Motorola Support", URL_MOTO_DOC,
           "Manufacturer mapping between XT2153-1 and motorola edge 20 pro",
           "Motorola's model-code table explicitly maps XT2153-1 / MC3A8 to motorola edge 20 pro. This is the exact model-code crosswalk, not Philippine retail evidence."),
    source("edge20pro_ntc_gec", "National Telecommunications Commission (NTC)", URL_NTC_GEC,
           "Philippine GEC model-code confirmation",
           "The NTC GEC table lists Motorola XT2153-1 as a smartphone under Motorola Mobility LLC, record ESD-GEC-2106870 dated July 29, 2021. The GEC corroborates the local regulatory model code; it is not treated alone as proof of consumer sales."),
    source("edge20pro_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine model launch reporting, configuration, price, and local technical specification cross-check",
           "Published October 21, 2021. YugaTech reports the Edge 20 Pro's Philippine unveiling, 12 GB/256 GB configuration, PHP 29,995 standard price and PHP 27,995 promotion, and local display, chipset, camera, battery, charging, connectivity, and software details. Its narrative paragraph contains camera transcription errors; this review uses its detailed specification list only where corroborated by Motorola or the exact local listing."),
    source("edge20pro_revu_ph", "REVU Philippines", URL_REVU,
           "Contemporaneous Philippine launch date, exact local configuration, list price, preorder price, and camera/video cross-check",
           "Published October 15, 2021. REVU says Motorola Philippines introduced the Edge 20 series that day and specifically lists the Edge 20 Pro 12 GB/256 GB at PHP 29,995, with a PHP 27,995 preorder price. It also reports 8K video and the 108 MP main / 8 MP periscope / 16 MP ultrawide arrangement. REVU explicitly says the article's feature image depicts the Edge 20 Fusion, so that image is not used for this record.",
           "2021-10-15"),
    source("edge20pro_villman_ph", "VillMan Computers Philippines", URL_VILLMAN,
           "Exact local part number, color, selected configuration, dated listed price, and local product page cross-check",
           "Observed November 26, 2026. The product page is titled for Motorola Moto Edge 20 Pro part number PANY0015PH, Thunder Black, 12 GB RAM/256 GB ROM, and lists PHP 29,995 with an Add to cart control. Stock status and item condition are not stated. Its specification table says Wi-Fi AC, conflicting with Motorola's Wi-Fi 6 statement; the catalog uses Motorola's manufacturer specification and preserves the discrepancy as an open issue. The page's exact-model-labeled image is not embedded because reuse terms are absent and the image target could not be visually inspected here."),
    source("edge20pro_qualcomm", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 870 platform CPU, GPU, and process-node specifications",
           "Qualcomm identifies Kryo 585 octa-core CPU up to 3.2 GHz, Adreno 650 graphics, and 7 nm process technology for the Snapdragon 870 5G Mobile Platform. These are platform specifications, not a separate Philippine SKU claim."),
    source("edge20pro_motorola_manual", "Motorola Support", URL_MANUAL,
           "Manufacturer's model-specific user guide",
           "Motorola's Edge 20 Pro guide is used for model-specific hardware/use context. Its illustration includes example imagery; no image is copied from the guide."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, catalog_value="__normalized__", unit=None, note: str,
          configuration_match: str,
          price_condition="__absent__", price_type=None,
          price_observed_at=None, listing_status=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": configuration_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value == "__normalized__" else catalog_value
    if unit:
        item["unit"] = unit
    if price_condition != "__absent__":
        item["priceCondition"] = price_condition
    if price_type is not None:
        item["priceType"] = price_type
    if price_observed_at is not None:
        item["priceObservedAt"] = price_observed_at
    if listing_status is not None:
        item["listingStatus"] = listing_status
    return item


def fields_for() -> list[dict]:
    match = "Philippine Motorola Edge 20 Pro PANY0015PH / XT2153-1: 12 GB RAM / 256 GB storage"
    out = []

    def add(fid, sid, value, normalized, **kwargs):
        out.append(field(fid, sid, value, normalized,
                         configuration_match=match, **kwargs))

    add("model_number", "edge20pro_ntc_gec", "NTC GEC Motorola XT2153-1; Motorola DoC maps XT2153-1 to motorola edge 20 pro", "XT2153-1", status="VERIFIED", note="The Philippine NTC record and Motorola model-code table agree on XT2153-1; VillMan separately identifies the local part number PANY0015PH.")
    add("global_release_date", "edge20pro_motorola_global", "Motorola global announcement dated July 29, 2021", "2021-07-29", status="VERIFIED", note="Global announcement date; distinct from the Philippine launch on October 15, 2021.")
    add("configuration", "edge20pro_revu_ph", "Philippine launch model: 12 GB RAM / 256 GB storage; VillMan part number PANY0015PH", "12 GB RAM / 256 GB storage", status="VERIFIED_SECONDARY", note="Philippine sources identify one local configuration. Global variants not evidenced in the Philippine launch sources are not added as local variants.")
    add("philippine_release_date", "edge20pro_revu_ph", "Motorola Philippines introduced/launched the Edge 20 Pro locally on October 15, 2021", "2021-10-15", status="VERIFIED_SECONDARY", note="Contemporaneous Philippine launch report. It is not a claim about the first individual retail transaction.")
    add("official_launch_price_php", "edge20pro_revu_ph", "Regular Philippine price PHP 29,995; preorder price PHP 27,995 for 12 GB / 256 GB", 29995, unit="PHP", status="VERIFIED_SECONDARY", note="The normalized value is the regular launch price. The lower preorder promotion is retained separately in price history and is not treated as the permanent list price.")
    add("current_price_php", "edge20pro_villman_ph", "VillMan product page lists PHP 29,995 for PANY0015PH 12 GB / 256 GB; stock status and condition not stated", 29995, unit="PHP", status="VERIFIED_SECONDARY", price_condition=None, price_type=f"VillMan exact local SKU listing observed {OBSERVED}; stock status and item condition not stated", price_observed_at=OBSERVED, listing_status="Not verified", note="Dated displayed local list price for the exact SKU/configuration. The page has an Add to cart control but no explicit stock or condition statement; no in-stock or new-condition claim is made.")
    add("display_size", "edge20pro_yugatech_ph", "6.7-inch Max Vision display", 6.7, key="displayInches", unit="in", note="Motorola and Philippine launch sources identify the 6.7-inch panel.")
    add("display_technology", "edge20pro_motorola_global", "OLED display", "OLED", key="displayType", status="VERIFIED", note="Manufacturer identifies OLED display technology.")
    add("display_resolution", "edge20pro_villman_ph", "1080 x 2400 pixels", "1080 x 2400", key="resolution", note="The exact local product page lists FHD+ 1080 x 2400 pixels.")
    add("display_refresh_rate", "edge20pro_motorola_global", "144 Hz refresh rate", 144, key="refreshHz", unit="Hz", status="VERIFIED", note="Manufacturer specification corroborated by Philippine launch reporting.")
    add("display_brightness", "edge20pro_motorola_global", "No numeric peak or typical brightness value found in reviewed sources", None, status="NOT_DISCLOSED", note="A marketing description such as bright or vivid is not converted into a numeric brightness value.")
    add("display_protection", "edge20pro_revu_ph", "Corning Gorilla Glass 5", "Corning Gorilla Glass 5", status="VERIFIED_SECONDARY", note="Contemporaneous Philippine specification lists Gorilla Glass 5; the exact protected surfaces are not asserted here.")
    add("chipset", "edge20pro_yugatech_ph", "Qualcomm Snapdragon 870 5G Mobile Platform", "Qualcomm Snapdragon 870", key="chipset", note="Local launch sources identify Snapdragon 870 for the Philippine Edge 20 Pro.")
    add("process_node", "edge20pro_qualcomm", "7 nm process technology", "7 nm", status="VERIFIED", unit="nm", note="Qualcomm platform property, not a claim about the handset's manufacturing process.")
    add("cpu", "edge20pro_qualcomm", "Kryo 585 octa-core CPU up to 3.2 GHz", "Kryo 585 octa-core up to 3.2 GHz", key="cpu", status="VERIFIED", note="Qualcomm's primary Snapdragon 870 product brief.")
    add("gpu", "edge20pro_qualcomm", "Adreno 650 GPU", "Adreno 650", key="gpu", status="VERIFIED", note="Qualcomm's primary Snapdragon 870 product brief.")
    add("operating_system", "edge20pro_motorola_global", "Android 11 at product introduction", "Android 11", key="os", status="VERIFIED", note="Motorola's global launch release identifies Android 11.")
    add("os_support", "edge20pro_motorola_global", "Motorola said the Edge 20 Pro would receive at least two major Android OS upgrades and two years of bi-monthly security updates; rollout was subject to change", "Launch plan: at least 2 major Android upgrades and 2 years of bi-monthly security updates", status="VERIFIED", note="This records Motorola's published launch plan, not a guarantee that all updates were delivered or remain available today.")
    add("ram_capacity", "edge20pro_revu_ph", "12 GB RAM", 12, key="ramGb", unit="GB", note="Exact Philippine launch configuration.")
    add("ram_type", "edge20pro_motorola_global", "Memory generation/type is not specified in the reviewed manufacturer or Philippine launch sources", None, status="NOT_DISCLOSED", note="No LPDDR type is inferred from the platform or product tier.")
    add("storage_capacity", "edge20pro_revu_ph", "256 GB built-in storage", 256, key="storageGb", unit="GB", note="Exact Philippine launch configuration.")
    add("storage_type", "edge20pro_yugatech_ph", "UFS 3.1 storage", "UFS 3.1", status="VERIFIED_SECONDARY", note="Philippine launch specification identifies UFS 3.1.")
    add("storage_expansion", "edge20pro_villman_ph", "Memory expansion listed as not applicable for PANY0015PH", "No memory expansion listed", status="VERIFIED_SECONDARY", note="The local part-number page explicitly lists Memory Expansion N/A; this is not a claim about cloud or USB storage.")
    add("rear_camera_system", "edge20pro_revu_ph", "108 MP main + 8 MP periscope telephoto + 16 MP ultrawide", "108 MP main + 8 MP periscope telephoto + 16 MP ultrawide", key="rearCameraMp", catalog_value=108, note="Detailed Philippine launch specifications and Motorola's product description support the three camera roles. YugaTech's narrative has a 1080 MP typo and a mislabeled camera; its detailed list, REVU, and VillMan support the values used here.")
    add("main_camera_sensor", "edge20pro_motorola_global", "Motorola describes the 108 MP main sensor as 1/1.5-inch optical format; sensor part number not stated", "108 MP; 1/1.5-inch optical format; sensor part number not recorded", status="VERIFIED", note="Manufacturer-stated optical format. VillMan lists 1/1.52-inch; the small notation difference is retained as a source discrepancy rather than treated as a distinct sensor identity.")
    add("ultrawide_camera", "edge20pro_revu_ph", "16 MP ultrawide camera with Macro Vision", "16 MP ultrawide with Macro Vision", status="VERIFIED_SECONDARY", note="Philippine launch source identifies the ultrawide camera; Motorola describes Macro Vision on the ultrawide lens.")
    add("telephoto_camera", "edge20pro_revu_ph", "8 MP periscope telephoto camera; up to 5x optical magnification and 50x digital Super Zoom", "8 MP periscope telephoto; 5x optical / up to 50x digital zoom", status="VERIFIED_SECONDARY", note="Periscope telephoto role and zoom specifications are reported in contemporaneous launch sources and Motorola's product release.")
    add("front_camera", "edge20pro_yugatech_ph", "32 MP front camera", 32, key="frontCameraMp", unit="MP", note="Philippine launch specification; the source also lists f/2.25, not normalized into this numeric catalog field.")
    add("video_recording", "edge20pro_motorola_global", "Motorola states Edge 20 Pro can record 8K video; detailed mode/frame-rate combinations not recorded", "8K video recording; frame rates/mode details not recorded", status="VERIFIED", note="Manufacturer launch statement; no 8K frame rate or front-camera recording modes are inferred.")
    add("battery_capacity", "edge20pro_yugatech_ph", "4,500 mAh battery", 4500, key="batteryMah", unit="mAh", note="Philippine launch specification corroborated by the exact local product listing.")
    add("battery_technology", "edge20pro_motorola_global", "Cell chemistry and internal battery construction not stated in reviewed sources", None, status="NOT_DISCLOSED", note="No lithium-polymer or cell-layout detail is inferred.")
    add("wired_charging", "edge20pro_motorola_global", "TurboPower 30 wired charging", 30, key="chargingW", unit="W", status="VERIFIED", note="Motorola names TurboPower 30; Philippine sources list 30 W.")
    add("wireless_charging", "edge20pro_motorola_manual", "Wireless or reverse charging support not established in reviewed sources", None, status="NOT_DISCLOSED", note="No support or absence is inferred from silence in the reviewed materials.")
    add("dimensions", "edge20pro_villman_ph", "163.26 x 74.55 x 7.99 mm", "163.26 x 74.55 x 7.99 mm", key="dimensions", unit="mm", note="Exact dimensions shown for local part number PANY0015PH. Some Philippine summaries round these values.")
    add("weight", "edge20pro_villman_ph", "190 g", 190, key="weightG", unit="g", note="Exact local listing specification.")
    add("materials", "edge20pro_villman_ph", "Gorilla Glass 5 listed under build; specific front/back/frame material breakdown not recorded", "Gorilla Glass 5; full material breakdown not recorded", status="VERIFIED_SECONDARY", note="Only the material entry stated by the exact local listing is recorded; no frame material is inferred.")
    add("ingress_protection", "edge20pro_villman_ph", "Water-repellent design; no formal IP rating listed", "Water-repellent design; IP rating not recorded", status="VERIFIED_SECONDARY", note="Water-repellent wording is not treated as an IP certification.")
    add("sim_esim", "edge20pro_yugatech_ph", "Dual Nano-SIM; eSIM support not stated in reviewed local sources", "Dual Nano-SIM; eSIM not recorded", key="sim", note="Local launch specification reports dual nano-SIM; no eSIM support is inferred.")
    add("cellular_bands", "edge20pro_yugatech_ph", "4G LTE and 5G; exact Philippine XT2153-1 band set not established", "4G LTE / 5G; exact local bands not recorded", key="cellular", note="Local sources confirm network generations. The NTC GEC radio ranges are not substituted for a full handset band specification.")
    add("wifi", "edge20pro_motorola_global", "Wi-Fi 6", "Wi-Fi 6", key="wifi", status="VERIFIED", note="Manufacturer states Wi-Fi 6. VillMan's local specification table says Wi-Fi AC; this conflict is flagged, and the manufacturer value is used.")
    add("bluetooth", "edge20pro_yugatech_ph", "Bluetooth 5.1", "Bluetooth 5.1", status="VERIFIED_SECONDARY", note="Philippine launch reporting; exact local product listing also names Bluetooth 5.1.")
    add("usb", "edge20pro_villman_ph", "USB Type-C 3.1 with DisplayPort 1.4 listed", "USB-C; USB 3.1 / DisplayPort 1.4 per local listing", key="ports", status="VERIFIED_SECONDARY", note="Exact local part-number page supplies the detailed port claim; no accessory or cable guarantee is implied.")
    add("nfc", "edge20pro_yugatech_ph", "NFC listed", "Yes", status="VERIFIED_SECONDARY", note="Philippine launch specification.")
    add("gnss", "edge20pro_yugatech_ph", "GPS, A-GPS, GLONASS, BeiDou, Galileo", "GPS, A-GPS, GLONASS, BeiDou, Galileo", status="VERIFIED_SECONDARY", note="Only the location systems listed in the Philippine launch specification are recorded.")
    add("audio", "edge20pro_motorola_manual", "Audio hardware details not fully established from reviewed manufacturer sources", None, status="NOT_DISCLOSED", note="No speaker count, tuning brand, or headphone-jack claim is inferred from incomplete product pages.")
    add("sensors", "edge20pro_motorola_global", "Side-mounted fingerprint reader; complete sensor list not recorded", "Side-mounted fingerprint reader; other sensors not recorded", status="VERIFIED", note="Motorola identifies the fingerprint reader integrated with the power key. No complete sensor suite is inferred.")

    if len(out) != 46:
        raise ValueError(f"Expected 46 reviewed phone fields, got {len(out)}")
    return out


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "motorola"
            or device.get("model") != "Edge 20 Pro"):
        raise ValueError("Inventory row no longer matches Motorola Edge 20 Pro")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Motorola Edge 20 Pro already has a manual review; inspect before replacing")

    config_id = f"{DEVICE}-12gb-256gb-ph"
    label = "12 GB RAM / 256 GB storage"
    review = {
        "deviceId": DEVICE, "configurationId": config_id,
        "brand": "Motorola", "model": "Edge 20 Pro",
        "configuration": label, "configurationLabel": label,
        "sources": SOURCES, "fields": fields_for(),
        "replacementVariants": [{
            "id": config_id, "label": label, "sku": "PANY0015PH",
            "modelCode": "XT2153-1",
            "notes": "Philippine Edge 20 Pro configuration and VillMan part number PANY0015PH; Motorola model code XT2153-1. Only the locally evidenced 12 GB / 256 GB configuration is represented.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine launch reported October 15, 2021; a local VillMan page lists part number PANY0015PH and PHP 29,995 as observed November 26, 2026. Current stock and item condition are not stated.",
            "philippineAvailability": "REVU reports that Motorola Philippines introduced and launched the Edge 20 Pro locally on October 15, 2021, as a 12 GB / 256 GB device priced at PHP 29,995 with a PHP 27,995 preorder offer. YugaTech independently reports the Philippine unveiling, configuration, and launch pricing. Motorola's model-code table maps XT2153-1 to motorola edge 20 pro, and the Philippine NTC GEC records XT2153-1. VillMan's exact local part number PANY0015PH page currently displays PHP 29,995; its stock status and item condition are not stated. Workbook scope remains Pending.",
            "observedAt": OBSERVED,
            "manufacturer": "Motorola Mobility",
            "productLine": "Motorola Edge 20 Pro",
            "modelNumber": "XT2153-1",
            "philippineReleaseYear": 2021,
            "philippineDateLabel": "Reported Philippine launch date",
            "researchNotes": "The workbook's Motorola Edge 20 Pro row matches the Philippine market model XT2153-1 / local part number PANY0015PH. Motorola's model-code table and the NTC GEC support the identity match. Motorola announced the model globally July 29, 2021; Philippine reporting places its local launch on October 15, 2021. Local evidence identifies the 12 GB / 256 GB configuration at a regular launch price of PHP 29,995, with a temporary preorder offer of PHP 27,995. On November 26, 2026, VillMan's exact PANY0015PH page displayed PHP 29,995, but it did not state stock or condition. Field conflicts are retained: Motorola specifies Wi-Fi 6 while VillMan's table says Wi-Fi AC; Motorola's camera sensor format is shown as 1/1.5-inch while VillMan lists 1/1.52-inch. The exact variant remains 12/256 GB. YugaTech's narrative contains camera transcription errors, so its detailed specifications are only used when corroborated by Motorola, REVU, or the exact local listing. REVU says its feature image shows the Edge 20 Fusion, so that image is excluded. VillMan links an Edge 20 Pro-labeled image, but the GIF could not be visually inspected here and reuse rights are not stated; the neutral placeholder remains. Workbook scope remains Pending.",
            "qualityFlag": "Philippine model matched to XT2153-1 / PANY0015PH 12 GB / 256 GB; retailer stock and price condition not stated; image not reused; workbook scope remains Pending",
            "openIssues": [
                {"issue": "Workbook eligibility/scope is still Pending", "action": "Preserve Pending and keep the record out of recommendation-eligible results according to current study rules."},
                {"issue": "VillMan's page displays PHP 29,995 but does not state stock status or item condition", "action": "Show the dated listed price with stock/condition as not recorded; do not label the item in stock or new."},
                {"issue": "Motorola states Wi-Fi 6 while VillMan's local table says Wi-Fi AC", "action": "Use the manufacturer specification and retain the exact local listing discrepancy for future review."},
                {"issue": "Motorola gives main sensor optical format as 1/1.5-inch; VillMan lists 1/1.52-inch", "action": "Retain both source statements; avoid asserting an exact sensor part number."},
                {"issue": "YugaTech's narrative paragraph contains camera transcription errors", "action": "Use its detailed list only where corroborated; do not use the incorrect 1080 MP or depth-camera labels."},
                {"issue": "REVU explicitly identifies its feature image as the Edge 20 Fusion; VillMan's product image target could not be visually inspected and has no stated reuse terms", "action": "Keep the neutral placeholder until an exact Edge 20 Pro image is visually verified and reuse permission is documented."},
                {"issue": "Full local cellular-band set, RAM type, display brightness, and complete sensor/audio suite were not established", "action": "Leave those values unrecorded rather than substituting regional details or guesses."},
            ],
        },
    }
    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "VillMan links an Edge 20 Pro-labeled GIF from the exact PANY0015PH page, but the image could not be visually inspected here and no reusable image license or permission is stated. REVU explicitly says its feature image shows the Edge 20 Fusion. No image is embedded.",
        "sourcePage": URL_VILLMAN, "assetUrl": URL_IMAGE,
        "scope": "Retailer image linked from the exact Motorola Edge 20 Pro PANY0015PH product page; exact visual match not independently confirmed",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Motorola Edge 20 Pro",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 29995,
         "configuration_id": config_id, "configuration_match": "exact",
         "variant_ram_gb": 12, "variant_storage_gb": 256,
         "price_type": "historical_ph_launch_list_price",
         "source_published_at": "2021-10-15",
         "excerpt": "Philippine launch regular price PHP 29,995 for the 12 GB / 256 GB Edge 20 Pro.",
         "source_url": URL_REVU, "source_kind": "historical_ph_launch_price_report",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_ph_launch_list_price_not_current"},
        {"device_id": DEVICE, "amount_php": 27995,
         "configuration_id": config_id, "configuration_match": "exact",
         "variant_ram_gb": 12, "variant_storage_gb": 256,
         "price_type": "historical_ph_preorder_price",
         "source_published_at": "2021-10-15",
         "excerpt": "Philippine Edge 20 Pro 12 GB / 256 GB preorder offer PHP 27,995; temporary launch promotion, not the regular list price.",
         "source_url": URL_REVU, "source_kind": "historical_ph_preorder_price_report",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_preorder_offer_not_current"},
        {"device_id": DEVICE, "amount_php": 29995,
         "configuration_id": config_id, "configuration_match": "exact",
         "variant_ram_gb": 12, "variant_storage_gb": 256,
         "price_type": "current_ph_retailer_listing_stock_and_condition_not_stated",
         "source_published_at": None,
         "excerpt": "VillMan exact PANY0015PH page displayed PHP 29,995; Add to cart control visible, stock status and condition not stated.",
         "source_url": URL_VILLMAN, "source_kind": "exact_variant_ph_retailer_price_observation",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "listed_price_stock_status_not_stated"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Motorola", "model_name": "Edge 20 Pro", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [], "discovery": [], "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "modelMatch": "Motorola Edge 20 Pro -> XT2153-1 / PANY0015PH",
        "configuration": "12/256 GB",
        "reviewedFields": len(review["fields"]),
        "globalAnnouncement": "2021-07-29",
        "philippineLaunch": "2021-10-15",
        "launchPricePhp": 29995,
        "preorderPricePhp": 27995,
        "currentListedPricePhp": 29995,
        "currentListingStockAndCondition": "not stated",
        "image": unavailable[DEVICE]["status"],
        "scopeStatus": "Pending",
    }, indent=2))


if __name__ == "__main__":
    main()
