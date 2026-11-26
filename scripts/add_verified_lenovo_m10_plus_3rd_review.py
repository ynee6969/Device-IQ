#!/usr/bin/env python3
"""Review Philippine Lenovo Tab M10 Plus (3rd Gen) configurations."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-26"
DEVICE = "device_d34ec0baa2b329"
G80_CONFIG = f"{DEVICE}-tb125fu-g80-3gb-32gb-wifi"
LTE_CONFIG = f"{DEVICE}-zaan0009ph-4gb-64gb-lte"

URL_PSREF = "https://psref.lenovo.com/Product/Lenovo_Tablets/Tab_M10_Plus_3rd_Gen?tab=spec"
URL_PSREF_G80 = "https://psref.lenovo.com/Detail/Lenovo_Tablets/Tab_M10_Plus_3rd_Gen?M=ZAAK0014US"
URL_LENOVO_DATASHEET = "https://psref.lenovo.com/syspool/Sys/PDF/datasheet/Lenovo_Tab-M10-Plus-3Gen_datasheet_EN.pdf"
URL_LENOVO_PH_FAQ = "https://support.lenovo.com/ph/en/solutions/ht513627-ht513574-lenovo-tab-m10-3rd-gen-tb328fu-tb328xu-frequently-asked-questions-faqs"
URL_YUGA = "https://www.yugatech.com/news/lenovo-tab-m10-and-m10-plus-priced-in-the-philippines/"
URL_GIZ = "https://www.gizguide.com/2022/11/lenovo-tab-m10-3rd-gen-ph-price-specs-official.html"
URL_ABENSON = "https://electroworld.abenson.com/lenovo-tab-m10-plus-3rd-gen-lte-zaan0009ph-storm-grey.html"
URL_VILLMAN = "https://villman.com/Product-Detail/lenovo_tab-m10-plus-gen-3lte-zaan0009ph1061inch-2k-ips-400nits-60hzsnapdragon-6804gb64gbqualcomm-adreno-610-android-12"
URL_DATABLITZ = "https://ecommerce.datablitz.com.ph/products/lenovo-tab-m10-plus-3rd-gen-10-61-2k-4gb-64gb-4g-lte-storm-grey-zaan0009ph"

SOURCES = [
    {"id": "lenovo_m10_plus_3rd_psref", "publisher": "Lenovo PSREF",
     "url": URL_PSREF, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Official model-family specification reference",
     "note": "Lenovo PSREF lists the Tab M10 Plus (3rd Gen) options, including 10.61-inch 2000 x 1200 IPS, 60 Hz, 400 nits, PC + metal, 7,500 mAh minimum / 7,700 mAh typical battery, cameras, sensors, ports, memory/storage types, and both processor families. It warns that options vary by model and region."},
    {"id": "lenovo_m10_plus_3rd_psref_g80", "publisher": "Lenovo PSREF",
     "url": URL_PSREF_G80, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Exact G80 3 GB / 32 GB Wi-Fi model cross-check",
     "note": "The specific Lenovo ZAAK0014US PSREF configuration maps TB125FU to MediaTek Helio G80, 3 GB LPDDR4x, 32 GB eMMC 5.1, and Wi-Fi-only connectivity. This is an official configuration reference; the local launch configuration is separately matched to Philippine sources."},
    {"id": "lenovo_m10_plus_3rd_datasheet", "publisher": "Lenovo",
     "url": URL_LENOVO_DATASHEET, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Official battery and charging capability reference",
     "note": "Lenovo's product datasheet states 7,700 mAh capacity and support for up to 20 W Quick Charge. The PSREF notes that supplied adapter wattage varies by country."},
    {"id": "lenovo_m10_plus_3rd_ph_support", "publisher": "Lenovo Support Philippines",
     "url": URL_LENOVO_PH_FAQ, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Philippine support model and Wi-Fi configuration cross-check",
     "note": "Lenovo Philippines support identifies the TB125FU Wi-Fi product family and lists 3 GB + 32 GB, 4 GB + 64 GB, and 4 GB + 128 GB configurations. This supports the Wi-Fi model family and capacity options but does not map every processor to each local option."},
    {"id": "yugatech_m10_plus_ph_launch", "publisher": "YugaTech",
     "url": URL_YUGA, "publicationDate": "2022-11-07", "accessDate": OBSERVED,
     "purpose": "Contemporaneous Philippine launch, configuration, price, and feature reference",
     "note": "YugaTech reports the Philippine launch of a 3 GB + 32 GB Helio G80 version at PHP 10,995 and a 4 GB + 64 GB Snapdragon 680 version at PHP 14,995, with authorized Lenovo stores and reseller channels. The article does not publish the exact Lenovo SKU or explicitly identify the first sale day."},
    {"id": "gizguide_m10_plus_ph_launch", "publisher": "GizGuide",
     "url": URL_GIZ, "publicationDate": "2022-11-08", "accessDate": OBSERVED,
     "purpose": "Independent Philippine launch cross-check and discrepancy record",
     "note": "GizGuide confirms Philippine availability and the two processor families. Its detail table lists 4 GB + 64 GB for Snapdragon 680, but its summary price line labels that option 4 GB + 32 GB; this storage inconsistency is retained rather than used to create a separate variant."},
    {"id": "abenson_m10_plus_lte", "publisher": "Abenson / Electroworld",
     "url": URL_ABENSON, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Philippine LTE SKU, configuration, and dated retailer price listing",
     "note": "The local retailer identifies a Tab M10 Plus 3rd Gen LTE with 4 GB + 64 GB, Snapdragon SDM680, and a ZAAN0009PH listing. Its page showed PHP 16,497 and a notify-me state when reviewed; this is not treated as a currently purchasable offer."},
    {"id": "villman_m10_plus_lte", "publisher": "VillMan Computers",
     "url": URL_VILLMAN, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Philippine LTE SKU technical cross-check",
     "note": "VillMan lists ZAAN0009PH / TB128XU with 4 GB + 64 GB, Snapdragon 680, UFS 2.2, LTE, Android 12, cameras, battery, and build details; its page says the product is phased out."},
    {"id": "datablitz_m10_plus_lte", "publisher": "DataBlitz",
     "url": URL_DATABLITZ, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Philippine LTE SKU listing and conflicting processor/price candidate",
     "note": "DataBlitz lists the same ZAAN0009PH 4 GB + 64 GB LTE product, but identifies the chipset as Helio G80 rather than Snapdragon 680 and showed PHP 10,995 with the product sold out. The conflict is retained and neither price is presented as a current purchasable offer."},
]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key=None, unit=None, note=None, price_condition=None, price_type=None,
      price_observed=None, candidates=None):
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    if price_condition:
        row.update({"priceCondition": price_condition, "priceType": price_type,
                    "priceObservedAt": price_observed})
    if candidates:
        row["candidateEvidence"] = candidates
    return row


def pending(fid: str, note: str, sid="lenovo_m10_plus_3rd_psref"):
    return f(fid, sid, "Not recorded for the exact Philippine configuration in the reviewed sources.", None,
             status="PENDING_VERIFICATION", note=note)


def undisclosed(fid: str, note: str, sid="lenovo_m10_plus_3rd_psref"):
    return f(fid, sid, "Not stated in the reviewed exact-model specifications.", None,
             status="NOT_DISCLOSED", note=note)


def price_candidates() -> list[dict]:
    return [
        {"value": 14995, "unit": "PHP", "sourceUrl": URL_YUGA, "sourceKind": "local_technology_publication",
         "observedAt": "2022-11-07", "excerpt": "4 GB + 64 GB Snapdragon 680 version priced at PHP 14,995.",
         "configurationMatch": "4 GB / 64 GB; exact LTE SKU not identified", "reviewStatus": "PENDING_VERIFICATION"},
        {"value": 16497, "unit": "PHP", "sourceUrl": URL_ABENSON, "sourceKind": "authorized_retailer_listing",
         "observedAt": OBSERVED, "excerpt": "ZAAN0009PH LTE 4 GB + 64 GB page showed PHP 16,497 and notify-me / unavailable state.",
         "configurationMatch": "exact retailer SKU ZAAN0009PH", "reviewStatus": "PENDING_VERIFICATION"},
        {"value": 10995, "unit": "PHP", "sourceUrl": URL_DATABLITZ, "sourceKind": "authorized_retailer_listing",
         "observedAt": OBSERVED, "excerpt": "ZAAN0009PH 4 GB + 64 GB LTE listing showed PHP 10,995 and Sold out.",
         "configurationMatch": "exact retailer SKU ZAAN0009PH", "reviewStatus": "PENDING_VERIFICATION"},
    ]


def common_fields(*, config: str, lte: bool, chip_conflict: bool = False) -> list[dict]:
    p = "lenovo_m10_plus_3rd_psref"
    local = "yugatech_m10_plus_ph_launch"
    fields = [
        f("model_number", "lenovo_m10_plus_3rd_ph_support" if not lte else "villman_m10_plus_lte",
          "TB125FU (Wi-Fi family)" if not lte else "TB128XU / ZAAN0009PH (local LTE listing)",
          "TB125FU" if not lte else "TB128XU / ZAAN0009PH", status="VERIFIED_SECONDARY",
          note="The Wi-Fi model family is named by Lenovo Support Philippines; the LTE retailer part number and TB128XU family are taken from Philippine retailer product records."),
        f("configuration", local,
          "3 GB RAM + 32 GB storage + MediaTek Helio G80; Philippine launch listing identifies TB125FU Wi-Fi family." if not lte else
          "4 GB RAM + 64 GB storage + LTE (ZAAN0009PH / TB128XU); processor differs across local retailer pages.",
          "3 GB RAM / 32 GB storage / MediaTek Helio G80 / Wi-Fi" if not lte else "4 GB RAM / 64 GB storage / LTE",
          status="VERIFIED_SECONDARY",
          note="YugaTech reports the 3 GB / 32 GB Helio G80 launch configuration; Lenovo Support Philippines identifies the matching TB125FU Wi-Fi family. For the LTE SKU, Philippine retailers agree on 4 GB / 64 GB and LTE, but disagree on chipset; it remains a separate configuration with chipset withheld." if lte else
               "YugaTech identifies this local launch configuration; Lenovo Support Philippines lists the same RAM/storage tier for its TB125FU Wi-Fi family."),
        f("philippine_release_date", local, "Lenovo Philippines introduced and listed the Tab M10 Plus 3rd Gen in November 2022; exact first-sale day not established.", "November 2022",
          status="VERIFIED_SECONDARY", note="Month-level local launch/availability evidence only; the article publication date is not treated as an exact first sale."),
        f("official_launch_price_php", local, "Official SRP not established; YugaTech reported the Philippine launch price shown below.", None,
          status="PENDING_VERIFICATION", unit="PHP", note="The local launch report gives a dated listing price but does not establish that it was a manufacturer SRP."),
        f("current_price_php", local, "YugaTech Philippine launch listing: PHP 10,995 for 3 GB / 32 GB Helio G80.", 10995,
          status="VERIFIED_SECONDARY", unit="PHP", note="Historical November 2022 Philippine launch-price observation; not a current offer.",
          price_condition="new", price_type="Historical Philippine launch listing (not current)", price_observed="2022-11-07") if not lte else
        f("current_price_php", "abenson_m10_plus_lte", "Retailer pages list different prices for ZAAN0009PH but both showed the product unavailable when checked.", None,
          status="PENDING_VERIFICATION", unit="PHP", note="Candidate prices are retained in the audit only: Abenson PHP 16,497 and DataBlitz PHP 10,995 (both sold out/unavailable); YugaTech's PHP 14,995 applies to a reported 4 GB / 64 GB Snapdragon 680 launch configuration but the exact LTE SKU match is not established.", candidates=price_candidates()),
        f("display_size", p, "10.61 inches", 10.61, key="displayInches", unit="in"),
        f("display_technology", p, "IPS", "IPS", key="displayType"),
        f("display_resolution", p, "2000 x 1200", "2000 x 1200", key="resolution"),
        f("display_refresh_rate", p, "60 Hz", 60, key="refreshHz", unit="Hz"),
        f("display_brightness", p, "400 nits", 400, unit="nits"),
        f("display_protection", p, "Anti-fingerprint surface; no strengthened cover-glass material is identified.", "Anti-fingerprint surface; cover-glass type not stated", status="VERIFIED_SECONDARY"),
        f("chipset", p if not chip_conflict else "datablitz_m10_plus_lte",
          "MediaTek Helio G80" if not chip_conflict else "Conflicting exact-SKU retailer listings: Helio G80 vs Qualcomm Snapdragon SDM680.",
          "MediaTek Helio G80" if not chip_conflict else None,
          status="VERIFIED" if not chip_conflict else "CONFLICTING_INFORMATION",
          key="chipset" if not chip_conflict else None,
          note="Exact G80 3 GB / 32 GB TB125FU configuration is documented by Lenovo PSREF and matched to the local launch listing." if not chip_conflict else
               "DataBlitz identifies ZAAN0009PH as Helio G80; Abenson and VillMan identify the same local LTE part number as Snapdragon SDM680. The manufacturer family supports both processors, but the exact ZAAN0009PH processor is withheld pending a primary SKU-level match.",
          candidates=None if not chip_conflict else [
              {"value": "MediaTek Helio G80", "sourceUrl": URL_DATABLITZ, "sourceKind": "authorized_retailer_listing", "observedAt": OBSERVED,
               "excerpt": "ZAAN0009PH 4 GB + 64 GB LTE product tech specifications list Helio G80.", "configurationMatch": "exact retailer part number", "reviewStatus": "CONFLICTING_INFORMATION"},
              {"value": "Qualcomm Snapdragon SDM680", "sourceUrl": URL_ABENSON, "sourceKind": "authorized_retailer_listing", "observedAt": OBSERVED,
               "excerpt": "ZAAN0009PH LTE product highlights list Snapdragon SDM680.", "configurationMatch": "exact retailer part number", "reviewStatus": "CONFLICTING_INFORMATION"},
              {"value": "Qualcomm Snapdragon SDM680", "sourceUrl": URL_VILLMAN, "sourceKind": "authorized_retailer_listing", "observedAt": OBSERVED,
               "excerpt": "ZAAN0009PH / TB128XU specification lists Snapdragon 680.", "configurationMatch": "exact retailer part number and model family", "reviewStatus": "CONFLICTING_INFORMATION"},
          ]),
        pending("process_node", "Lenovo's exact SKU specifications do not state a fabrication process."),
        f("cpu", p, "2 x Cortex-A75 up to 2.0 GHz + 6 x Cortex-A55 up to 1.8 GHz" if not chip_conflict else "Exact LTE SKU CPU withheld because its chipset is disputed.",
          "2x Cortex-A75 2.0 GHz + 6x Cortex-A55 1.8 GHz" if not chip_conflict else None,
          key="cpu" if not chip_conflict else None, status="VERIFIED" if not chip_conflict else "PENDING_VERIFICATION"),
        f("gpu", p, "Arm Mali-G52 MC2" if not chip_conflict else "Exact LTE SKU GPU withheld because its chipset is disputed.",
          "Arm Mali-G52 MC2" if not chip_conflict else None, key="gpu" if not chip_conflict else None,
          status="VERIFIED" if not chip_conflict else "PENDING_VERIFICATION"),
        f("operating_system", p, "Android 12 at launch; Lenovo PSREF lists Android 12 or later.", "Android 12 at launch", key="os"),
        f("os_support", local, "YugaTech reports three years of security updates at launch; Lenovo does not publish a PH-specific end date in the reviewed sources.", "3 years of security updates reported; exact support end date not recorded", status="VERIFIED_SECONDARY"),
        f("ram_capacity", "lenovo_m10_plus_3rd_ph_support" if not lte else "abenson_m10_plus_lte", "3 GB" if not lte else "4 GB", 3 if not lte else 4, key="ramGb", unit="GB", status="VERIFIED_SECONDARY" if lte else "VERIFIED"),
        f("ram_type", p, "LPDDR4x", "LPDDR4x", key="ramType"),
        f("storage_capacity", "lenovo_m10_plus_3rd_ph_support" if not lte else "abenson_m10_plus_lte", "32 GB" if not lte else "64 GB", 32 if not lte else 64, key="storageGb", unit="GB", status="VERIFIED_SECONDARY" if lte else "VERIFIED"),
        f("storage_type", "lenovo_m10_plus_3rd_psref_g80" if not lte else "datablitz_m10_plus_lte",
          "32 GB eMMC 5.1" if not lte else "Conflicting exact-SKU listings imply different storage types: eMMC 5.1 (G80 listing) vs UFS 2.2 (SDM680 listings).",
          "eMMC 5.1" if not lte else None, key="storageType" if not lte else None,
          status="VERIFIED" if not lte else "CONFLICTING_INFORMATION",
          note=None if not lte else "Exact SKU chipset and storage type conflict together: DataBlitz lists the G80 / eMMC 5.1 model; Abenson and VillMan list the SDM680 / UFS 2.2 model. Do not select one until a Lenovo configuration record for ZAAN0009PH is found.",
          candidates=None if not lte else [
              {"value": "eMMC 5.1", "sourceUrl": URL_DATABLITZ, "sourceKind": "authorized_retailer_listing", "observedAt": OBSERVED,
               "excerpt": "Retail listing identifies G80; Lenovo PSREF associates G80 configuration with eMMC 5.1.", "configurationMatch": "exact retailer part number; type association from manufacturer family spec", "reviewStatus": "CONFLICTING_INFORMATION"},
              {"value": "UFS 2.2", "sourceUrl": URL_VILLMAN, "sourceKind": "authorized_retailer_listing", "observedAt": OBSERVED,
               "excerpt": "ZAAN0009PH listing identifies 64 GB UFS 2.2 with Snapdragon 680.", "configurationMatch": "exact retailer part number", "reviewStatus": "CONFLICTING_INFORMATION"},
          ]),
        f("storage_expansion", p, "microSD card slot supports up to 1 TB", "microSD up to 1 TB"),
        f("rear_camera_system", p, "8 MP f/2.2 autofocus rear camera", "8 MP f/2.2 autofocus rear camera"),
        f("main_camera_sensor", p, "8 MP f/2.2 autofocus rear camera; sensor make/model not stated.", "8 MP f/2.2 autofocus; sensor make/model not disclosed"),
        f("ultrawide_camera", p, "The manufacturer lists one rear camera and no ultrawide module.", "No ultrawide camera listed", status="NOT_APPLICABLE"),
        f("telephoto_camera", p, "The manufacturer lists one rear camera and no telephoto module.", "No telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", p, "8 MP f/2.0 fixed-focus front camera", 8, key="frontCameraMp", unit="MP"),
        pending("video_recording", "The reviewed manufacturer specifications do not state camera video modes or frame rates."),
        f("battery_capacity", p, "7,700 mAh typical; 7,500 mAh minimum", 7700, key="batteryMah", unit="mAh",
          note="Catalog uses Lenovo's typical capacity; the manufacturer separately lists 7,500 mAh minimum."),
        f("battery_technology", p, "Integrated lithium-polymer battery", "Integrated lithium-polymer"),
        f("wired_charging", "lenovo_m10_plus_3rd_datasheet", "Lenovo lists 20 W Quick Charge; country-specific adapter offerings include 10 W and 20 W.", 20, key="chargingW", unit="W",
          note="This is the maximum supported charge figure. Lenovo says the bundled adapter depends on market; the exact Philippine adapter for each variant is not confirmed."),
        undisclosed("wireless_charging", "Wireless charging is not stated in the reviewed manufacturer specifications."),
        f("dimensions", p, "251.2 x 158.8 x 7.45 mm (W x D x H)", "251.2 x 158.8 x 7.45", key="dimensions", unit="mm"),
        f("weight", p, "Approximately 465 g", 465, key="weightG", unit="g"),
        f("materials", p, "PC + metal", "PC + metal"),
        undisclosed("ingress_protection", "No IP ingress-protection rating is stated in the reviewed specifications."),
        f("sim_esim", "lenovo_m10_plus_3rd_ph_support" if not lte else "abenson_m10_plus_lte",
          "TB125FU Wi-Fi configuration has no SIM/eSIM." if not lte else "Single nano-SIM LTE configuration; eSIM is not listed.",
          "Not applicable to Wi-Fi-only configuration" if not lte else "Single nano-SIM; eSIM not listed",
          status="NOT_APPLICABLE" if not lte else "VERIFIED_SECONDARY"),
        f("cellular_bands", "lenovo_m10_plus_3rd_ph_support" if not lte else "abenson_m10_plus_lte",
          "Wi-Fi-only; cellular bands not applicable." if not lte else "4G LTE; Philippine-supported bands not stated on the local retailer page.",
          "Not applicable to Wi-Fi-only configuration" if not lte else "4G LTE; bands not recorded", status="NOT_APPLICABLE" if not lte else "VERIFIED_SECONDARY"),
        f("wifi", p, "Wi-Fi 5; IEEE 802.11ac 1x1, 2.4 GHz and 5 GHz", "Wi-Fi 5, 802.11ac 1x1; 2.4/5 GHz", key="wifi"),
        f("bluetooth", p, "Bluetooth 5.0" if not lte else "Exact Bluetooth version withheld while chipset/retailer SKU specifications conflict.",
          "Bluetooth 5.0" if not lte else None, status="VERIFIED" if not lte else "PENDING_VERIFICATION"),
        f("usb", p, "USB-C 2.0 and 3.5 mm headphone/microphone combo jack", "USB-C 2.0; 3.5 mm combo jack", key="ports"),
        undisclosed("nfc", "NFC support is not stated in the reviewed manufacturer specifications."),
        f("gnss", p, "GPS, GLONASS, Galileo, and BeiDou" if not lte else "GPS, GLONASS, Galileo, BeiDou, and A-GPS listed for the LTE model family.",
          "GPS; GLONASS; Galileo; BeiDou" if not lte else "GPS; GLONASS; Galileo; BeiDou; A-GPS"),
        f("audio", p, "Four 1 W speakers with Dolby Atmos; one microphone", "Four 1 W Dolby Atmos speakers; mono microphone", key="sound"),
        f("sensors", p, "Accelerometer, ambient-light sensor, gyroscope, and Hall sensor", "Accelerometer; ambient light; gyroscope; Hall"),
        f("tablet_stylus", p, "Compatible with Lenovo Precision Pen 2; optional or bundled depending on configuration.", "Lenovo Precision Pen 2 compatible; bundle varies", key="stylus"),
        undisclosed("tablet_keyboard", "A compatible keyboard was not identified in the reviewed specifications."),
        f("tablet_cellular_variant", "lenovo_m10_plus_3rd_ph_support" if not lte else "abenson_m10_plus_lte",
          "TB125FU Wi-Fi only" if not lte else "4G LTE variant (ZAAN0009PH / TB128XU)",
          "Wi-Fi only" if not lte else "4G LTE", key="cellular", status="VERIFIED" if not lte else "VERIFIED_SECONDARY"),
    ]
    if chip_conflict:
        fields[2]["note"] += " The exact CPU/storage controller remains unresolved despite the capacity and LTE radio match."
    return fields


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    manual["records"] = [row for row in manual["records"] if not (
        row.get("deviceId") == DEVICE and row.get("configurationId") == f"{DEVICE}-unrecorded"
    )]
    for review in manual["records"]:
        if review.get("deviceId") != DEVICE:
            continue
        for source in review.get("sources", []):
            if source.get("id") == "lenovo_m10_plus_3rd_psref_g80":
                # The date on Lenovo's page is the model's announce date, not
                # a publication date for the PSREF document itself.
                source["publicationDate"] = None

    replacements = [
        {"id": G80_CONFIG, "label": "3 GB RAM / 32 GB storage / Wi-Fi / MediaTek Helio G80 (TB125FU)",
         "sku": None, "modelCode": "TB125FU",
         "notes": "Philippine launch configuration reported by YugaTech; the matching Lenovo TB125FU PSREF build is Wi-Fi, Helio G80, 3 GB / 32 GB."},
        {"id": LTE_CONFIG, "label": "4 GB RAM / 64 GB storage / 4G LTE (ZAAN0009PH / TB128XU; chipset unresolved)",
         "sku": "ZAAN0009PH", "modelCode": "TB128XU",
         "notes": "Local retailers agree on 4 GB / 64 GB LTE, but disagree on Helio G80 vs Snapdragon 680 and eMMC vs UFS. Chipset and storage type are withheld pending Lenovo's exact part-number configuration."},
    ]
    # The review helper validates each configuration against its in-memory
    # catalog. Seed both replacement IDs for review-time validation; the public
    # catalog builder still applies the replacement action only once, on the
    # first manual review row.
    target = next(device for device in catalog if device["id"] == DEVICE)
    target["variants"] = [{"id": item["id"], "label": item["label"], "specs": {}}
                          for item in replacements]
    common_availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine launch and authorized reseller availability reported in November 2022; exact first-sale day not established.",
        "philippineAvailability": "YugaTech reported Lenovo Philippines' Tab M10 Plus (3rd Gen) launch through Lenovo exclusive stores and authorized resellers. Exact first retail transaction date is not recorded.",
        "observedAt": OBSERVED,
        "qualityFlag": "ZAAN0009PH LTE listing has conflicting processor/storage details across Philippine retailers.",
        "manufacturer": "Lenovo",
        "productLine": "Tab M10 Plus",
        "modelNumber": "TB125FU (Wi-Fi) / TB128XU (LTE)",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Philippine launch month",
        "researchNotes": "Two Philippine launch configurations are documented. Lenovo's 3 GB / 32 GB Helio G80 Wi-Fi configuration is matched to the TB125FU family. Local retailers identify ZAAN0009PH / TB128XU as 4 GB / 64 GB LTE, but DataBlitz reports Helio G80 while Abenson and VillMan report Snapdragon SDM680; storage type also differs. Conflicting fields remain blank. Launch pricing is dated and the retailer pages checked were sold out/unavailable.",
        "openIssues": [
            {"issue": "Exact first-sale date is not recorded", "action": "Keep the Philippine launch month at November 2022; do not infer a sale date from article publication."},
            {"issue": "ZAAN0009PH processor and storage type conflict", "action": "Resolve against Lenovo PSREF or a manufacturer part-number record before publishing a chipset or storage type for the LTE SKU."},
            {"issue": "No currently purchasable retailer price confirmed", "action": "Keep sold-out retailer prices as dated audit candidates, not current offers."},
        ],
    }
    yuga_image = "https://www.yugatech.com/wp-content/uploads/2022/11/09_Lenovo_Tab_m10_Plus_G3_Service-720x405.jpg"
    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "A model-matched product image was found, but no reusable license or written permission is recorded for this site.",
        "sourcePage": URL_YUGA,
        "assetUrl": yuga_image,
        "scope": "Exact model; variant not distinguished",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Lenovo Tab M10 Plus (3rd Gen)",
    }

    records = [
        {"deviceId": DEVICE, "configurationId": G80_CONFIG,
         "brand": "Lenovo", "model": "Tab M10 Plus 3rd Gen",
         "configuration": replacements[0]["label"], "sources": SOURCES,
         "fields": common_fields(config="g80", lte=False),
         "replacementVariants": replacements, "availabilityEvidence": common_availability,
         "modelCode": "TB125FU"},
        {"deviceId": DEVICE, "configurationId": LTE_CONFIG,
         "brand": "Lenovo", "model": "Tab M10 Plus 3rd Gen",
         "configuration": replacements[1]["label"], "sources": SOURCES,
         "fields": common_fields(config="lte", lte=True, chip_conflict=True),
         "sku": "ZAAN0009PH", "modelCode": "TB128XU"},
    ]
    for row in records:
        add_review(manual, catalog, row)
        review = next(item for item in manual["records"] if
                      (item["deviceId"], item["configurationId"]) == (DEVICE, row["configurationId"]))
        review["configuration"] = row["configuration"]
        review["configurationLabel"] = row["configuration"]
    deduplicate_target_reviews(manual, {(DEVICE, G80_CONFIG), (DEVICE, LTE_CONFIG)})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "Tab M10 Plus 3rd Gen", "configurations": len(records),
                      "fields": sum(len(row["fields"]) for row in records),
                      "lteProcessorStatus": "CONFLICTING_INFORMATION",
                      "imageStatus": unavailable[DEVICE]["status"]}, indent=2))


if __name__ == "__main__":
    main()
