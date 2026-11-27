#!/usr/bin/env python3
"""Record source-backed model and Philippine configuration review for DOOGEE T10."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/doogee-t10-ph-prices-2026-11-27.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
OBSERVED = "2026-11-27"
DEVICE = "device_6d0aa2c52b2ae3"
CONFIG = f"{DEVICE}-ph-8gb-128gb-4g"
MODEL = "T10"

URL_DOOGEE = "https://www.doogee.co.za/tablets/doogee-t10.html"
URL_TERMS = "https://www.doogee.com/policies/terms-of-service"
URL_YUGATECH = "https://www.yugatech.com/toys-gadgets/doogee-philippines-relaunched/"
URL_GADGETMATCH = "https://www.gadgetmatch.com/doogee-enters-the-philippines-with-t-series-tablets/"
URL_HUNGRYGEEKS = "https://hungrygeeks.com.ph/doogee-philippines-officially-launches-t10-t10s-and-t30-pro-tablets-starts-at-php7399/"
URL_GSMARENA = "https://www.gsmarena.com/doogee_to_enter_the_tablet_market_with_the_t10-news-56254.php"
URL_GIZMOCHINA = "https://www.gizmochina.com/2022/11/01/doogee-enters-the-tablet-industry-with-the-launch-of-the-doogee-t10-tablet-specs-price-availability/"
URL_HARTWARE = "https://www.hartware.de/2022/11/01/doogees-first-tablet-t10-will-refresh-you-with-ultimate-entertainment/"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-doogee-t10"
URL_NOTEBOOKCHECK = "https://www.notebookcheck.net/Doogee-T10-Tab.685999.0.html"
URL_YUGATECH_PRICES = "https://www.yugatech.com/doogee-gadget-price-list-philippines"
URL_MOBILEMALL = "https://philippines.mobilemall.co/doogee-t10"
URL_PTG = "https://www.pinoytechnoguide.com/"
URL_NANOREVIEW = "https://nanoreview.net/"
IMAGE_URL = "https://www.doogee.co.za/assets/t10/t10-slate.png"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("doogee_t10_official_specs", "DOOGEE South Africa (manufacturer regional site)", URL_DOOGEE,
        "Exact-model manufacturer product page and hardware specifications",
        "DOOGEE's T10 page identifies the exact model and gives the product's display, T606 processor, memory, storage, battery, camera, connectivity, build, accessory support, and Android 12 details. It is a regional/global technical source, not proof of Philippine sale or a regional SKU."),
    src("doogee_t10_ph_yugatech", "YugaTech Philippines", URL_YUGATECH,
        "Philippine launch, local 8 GB / 128 GB configuration, local specifications and launch SRP",
        "Published 2023-09-01. Names the DOOGEE T10 at the Philippine launch, links to its DOOGEE Lazada listing, reports 8 GB physical plus 7 GB virtual RAM / 128 GB, and lists PHP 9,499 SRP / PHP 8,399 introductory price. Its spec table differs from DOOGEE on A55 clock and does not identify a regional SKU." , "2023-09-01"),
    src("doogee_t10_ph_gadgetmatch", "GadgetMatch Philippines", URL_GADGETMATCH,
        "Independent Philippine model/configuration and price cross-check",
        "Published 2023-09-04. Separately lists T10 8 GB RAM / 128 GB storage, LTE capability, Android 12, 13 MP rear / 8 MP front cameras, 8,300 mAh, PHP 8,399 promo and PHP 9,499 SRP. It does not identify a numeric local SKU or current price.", "2023-09-04"),
    src("doogee_t10_ph_hungrygeeks", "Hungry Geeks Philippines", URL_HUNGRYGEEKS,
        "Local launch campaign dates and DOOGEE official-store availability",
        "Published 2023-09-01. Reports the official DOOGEE Lazada store was open for purchase at launch, gives the T10 PHP 9,499 SRP and PHP 8,399 introductory offer through September 13, 2023, and says offline partner stores would start September 28. This is launch-era reporting, not present stock evidence.", "2023-09-01"),
    src("doogee_t10_gsmarena_prelaunch", "GSMArena", URL_GSMARENA,
        "Pre-launch exact-model reporting and discrepancy review",
        "Published 2022-10-22, before the T10's reported global launch. GSMArena previewed the T10 and said November 1 was planned; some preview values (430 g and UFS storage) differ from final DOOGEE product specifications. Pre-launch values are not promoted as final hardware.", "2022-10-22"),
    src("doogee_t10_gizmochina_launch", "Gizmochina", URL_GIZMOCHINA,
        "Global release date and exact-model launch cross-check",
        "Published 2022-11-01. Reports that DOOGEE launched the exact T10 globally on November 1, 2022. This establishes a reported global date only; it is not Philippine-sale evidence.", "2022-11-01"),
    src("doogee_t10_hartware_launch", "Hartware", URL_HARTWARE,
        "Independent exact-model launch and configuration cross-check",
        "Published 2022-11-01. Reports global T10 release, 8 GB physical plus extended RAM, 128 GB storage, 8,300 mAh and 18 W charging. It is a secondary model-level source.", "2022-11-01"),
    src("doogee_t10_kimovil", "Kimovil", URL_KIMOVIL,
        "Secondary exact-model global specification cross-check",
        "The exact T10 profile lists Global 8 GB / 128 GB; its global price feed is not a Philippine price. It reports eMMC storage, dimensions, 570 g, display and camera details, but differs from DOOGEE on LPDDR4X versus LPDDR4 and does not verify a local SKU."),
    src("doogee_t10_notebookcheck", "Notebookcheck", URL_NOTEBOOKCHECK,
        "Independent exact-model technical cross-check",
        "The exact T10 model page lists 60 Hz display, Mali-G57 MP1, eMMC storage, 3.5 mm audio, LTE/Wi-Fi 5, Bluetooth 5.0, 570 g, 8,300 mAh Li-polymer battery and Android 12. It is not Philippine variant, sale, or price evidence."),
    src("doogee_t10_yugatech_current_index", "YugaTech Philippines", URL_YUGATECH_PRICES,
        "Current Philippine price search as of 2026-11-27",
        "The YugaTech Philippine price index was updated 2026-11-26 and its current DOOGEE rows do not list the T10. This absence is not proof that no seller has stock; it supplies no current T10 price." , "2026-11-26"),
    src("doogee_t10_mobilemall_candidate", "MobileMall Philippines", URL_MOBILEMALL,
        "Review and rejection of an estimated PH price candidate",
        "The current search result labels the T10 discontinued and marks its PHP amount as estimated/converted rather than an observed authorized Philippine offer. That estimate is not used as a current price."),
    src("doogee_t10_image_rights", "DOOGEE", URL_TERMS,
        "Image reuse terms for the exact-model official product image",
        "DOOGEE's site terms say website images/materials may not be used for business use without written permission and describe unauthorized reproduction/distribution as prohibited. No reuse permission or open license was located; the exact image is therefore not republished."),
]
SOURCE_BY_ID = {row["id"]: row for row in SOURCES}


def f(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
      key=None, unit=None, note=None, candidate_evidence=None,
      price_condition=None, price_type=None, price_observed=None):
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized,
           "note": note or "Exact DOOGEE T10 model reviewed against the cited source; this does not imply that every global option was sold in the Philippines."}
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized
    if unit:
        row["unit"] = unit
    if candidate_evidence:
        row["candidateEvidence"] = candidate_evidence
    if price_condition:
        row["priceCondition"] = price_condition
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed
    return row


def not_disclosed(fid: str, sid: str, explanation: str):
    return f(fid, sid, explanation, None, status="NOT_DISCLOSED", note=explanation)


def candidate(value, url, kind, excerpt, *, match="exact DOOGEE T10 model"):
    return {"value": value, "sourceUrl": url, "sourceKind": kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": match, "reviewStatus": "CONFLICTING_INFORMATION",
            "localAvailabilityVerified": False}


def fields() -> list[dict]:
    cpu_candidates = [
        candidate("2 x 1.6 GHz Cortex-A75 + 6 x up to 1.6 GHz Cortex-A55",
                  URL_DOOGEE, "manufacturer_regional_product_page",
                  "DOOGEE states two Cortex-A75 and six Cortex-A55 cores at up to 1.6 GHz."),
        candidate("2 x 1.6 GHz Cortex-A75 + 6 x 1.4 GHz Cortex-A55",
                  URL_YUGATECH, "independent_ph_launch_source",
                  "YugaTech's T10 specification table gives 2 x 1.6 GHz A75 + 6 x 1.4 GHz A55.",
                  match="exact model in Philippine launch coverage"),
    ]
    ram_type_candidates = [
        candidate("LPDDR4", URL_DOOGEE, "manufacturer_regional_product_page",
                  "DOOGEE labels the 8+7 GB memory as LPDDR4."),
        candidate("LPDDR4X", URL_KIMOVIL, "secondary_model_database",
                  "Kimovil labels the T10's physical memory LPDDR4X."),
    ]
    return [
        f("model_number", "doogee_t10_official_specs",
          "Product name is DOOGEE T10; the reviewed sources do not state a distinct Philippine model code or SKU.",
          "DOOGEE T10; regional model code/SKU not recorded", status="VERIFIED"),
        f("global_release_date", "doogee_t10_gizmochina_launch",
          "Gizmochina reports the T10 global launch on 2022-11-01; Hartware also reports release on that date.",
          "2022-11-01", status="VERIFIED_SECONDARY", note="Reported global launch date, cross-checked against two dated independent reports. GSMArena's earlier 2022-10-22 article says November 1 was planned. This is not Philippine availability evidence."),
        f("configuration", "doogee_t10_ph_yugatech",
          "Philippine launch coverage identifies 8 GB physical RAM + 7 GB virtual/extended RAM and 128 GB storage; the T10 is LTE-capable. The numeric Philippine SKU is not listed.",
          "8 GB physical RAM / 128 GB storage / 4G LTE; 7 GB extended RAM is virtual", note="YugaTech and GadgetMatch identify the same local model/configuration. The 7 GB extended amount is not counted as physical RAM; no regional model code or color-specific SKU is inferred."),
        f("philippine_release_date", "doogee_t10_ph_hungrygeeks",
          "DOOGEE Philippines launch and official online-store availability reported 2023-09-01; offline partners were scheduled from 2023-09-28.",
          "2023-09-01", status="VERIFIED_SECONDARY", note="Reported Philippine launch/online availability date. This is not an exact first transaction timestamp; offline partners had a later start date."),
        f("official_launch_price_php", "doogee_t10_ph_hungrygeeks",
          "Philippine launch SRP PHP 9,499; introductory offer PHP 8,399 through 2023-09-13.",
          9499, status="VERIFIED_SECONDARY", unit="PHP", note="Historical launch SRP for the locally reported DOOGEE T10 8/128 LTE configuration. The separate PHP 8,399 introductory offer ran 2023-09-01 through 2023-09-13; neither amount is a current price.", price_condition="new", price_type="historical_ph_launch_srp", price_observed="2023-09-01"),
        f("current_price_php", "doogee_t10_yugatech_current_index",
          "No current exact-model Philippine price was found in the reviewed current price index; the separate MobileMall amount is marked estimated/discontinued and was rejected.",
          None, status="UNAVAILABLE_AFTER_RESEARCH", unit="PHP", note="No dated current authorized Philippine price observation was located as of 2026-11-27. YugaTech's index updated 2026-11-26 does not list T10; MobileMall's converted estimate is not a current local offer. Keep blank; this does not prove that no seller has stock."),
        f("display_size", "doogee_t10_official_specs", "10.1-inch display", 10.1, status="VERIFIED", key="displayInches", unit="in"),
        f("display_technology", "doogee_t10_official_specs", "10.1-inch IPS display", "IPS LCD", status="VERIFIED", key="displayType"),
        f("display_resolution", "doogee_t10_official_specs", "1920 x 1200 pixels (FHD+)", "1920 x 1200", status="VERIFIED", key="resolution"),
        f("display_refresh_rate", "doogee_t10_notebookcheck", "60 Hz", 60, key="refreshHz", unit="Hz", note="Notebookcheck's exact T10 technical table lists 60 Hz; the manufacturer page does not specify refresh rate."),
        f("display_brightness", "doogee_t10_official_specs", "300 nits", 300, status="VERIFIED", unit="nits"),
        not_disclosed("display_protection", "doogee_t10_official_specs", "TÜV Rheinland low-blue-light/eye-comfort certification is listed, but the display cover-glass material or scratch-protection rating is not recorded."),
        f("chipset", "doogee_t10_official_specs", "Unisoc T606 octa-core processor", "Unisoc T606", status="VERIFIED", key="chipset"),
        f("process_node", "doogee_t10_official_specs", "12 nm processor", 12, status="VERIFIED", unit="nm"),
        f("cpu", "doogee_t10_official_specs",
          "DOOGEE and Philippine launch coverage differ on the Cortex-A55 maximum clock: up to 1.6 GHz on DOOGEE's product page versus 1.4 GHz in YugaTech's table.",
          None, status="CONFLICTING_INFORMATION", key="cpu", note="The T606 chipset match is confirmed, but the exact A55 cluster clock is disputed by the manufacturer regional page and local launch source. The CPU field is withheld pending a source that resolves the discrepancy.", candidate_evidence=cpu_candidates),
        f("gpu", "doogee_t10_notebookcheck", "ARM Mali-G57 MP1", "ARM Mali-G57 MP1", key="gpu", note="Exact-model Notebookcheck technical specification; YugaTech's Philippine T10 table independently lists Mali-G57 MP1."),
        f("operating_system", "doogee_t10_ph_yugatech", "Android 12 at launch", "Android 12", status="VERIFIED_SECONDARY", key="os", note="Philippine launch coverage and DOOGEE's product page state Android 12 out of the box."),
        f("os_support", "doogee_t10_ph_yugatech", "YugaTech reported Android 13 upgrade availability; no duration or security-update policy was found.", "Android 13 upgrade reported; update duration/policy not recorded", status="VERIFIED_SECONDARY", note="This records a reported version upgrade only, not a continuing OS or security-support commitment."),
        f("ram_capacity", "doogee_t10_ph_yugatech", "8 GB physical RAM plus up to 7 GB extended/virtual RAM", 8, status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="The local T10 launch configuration and DOOGEE page identify 8 GB physical RAM. The extra 7 GB is virtual/extended memory and is not added to the physical RAM value."),
        f("ram_type", "doogee_t10_official_specs", "DOOGEE says LPDDR4; Kimovil says LPDDR4X for the exact-model profile.", None, status="CONFLICTING_INFORMATION", key="ramType", note="The manufacturer page and secondary database differ on the memory generation suffix. Do not present LPDDR4X as established for the local configuration.", candidate_evidence=ram_type_candidates),
        f("storage_capacity", "doogee_t10_ph_yugatech", "128 GB internal storage", 128, status="VERIFIED_SECONDARY", key="storageGb", unit="GB"),
        f("storage_type", "doogee_t10_official_specs", "Final DOOGEE product specifications list 128 GB eMMC; Kimovil and Notebookcheck also list eMMC. GSMArena's October 2022 pre-launch preview said UFS.", "eMMC; generation not stated by DOOGEE", status="VERIFIED", key="storageType", note="Use the final manufacturer specification, cross-checked against later exact-model references. GSMArena's UFS claim was published before global release and is treated as a superseded pre-launch discrepancy, not final hardware."),
        f("storage_expansion", "doogee_t10_official_specs", "TF/microSD expansion up to 1 TB", "microSD/TF card supported up to 1 TB", status="VERIFIED", note="DOOGEE's product page gives expansion up to 1 TB; YugaTech says microSDXC shares the SIM tray."),
        f("rear_camera_system", "doogee_t10_ph_yugatech", "13 MP main rear camera; YugaTech lists an additional secondary camera without its resolution or role.", "13 MP main rear camera + secondary module (details not recorded)", status="VERIFIED_SECONDARY", note="Do not infer a depth, ultrawide, or telephoto role for the unspecified second module."),
        f("main_camera_sensor", "doogee_t10_kimovil", "13 MP main, f/2.2, CMOS; sensor make/model not identified", "13 MP main, f/2.2; sensor model not recorded", status="VERIFIED_SECONDARY", note="Kimovil's exact-model entry provides lens/aperture and sensor type but no sensor identity; no sensor manufacturer or model is inferred."),
        not_disclosed("ultrawide_camera", "doogee_t10_official_specs", "No separate ultrawide camera is identified in the reviewed DOOGEE or local launch specifications; its presence is not explicitly ruled out."),
        not_disclosed("telephoto_camera", "doogee_t10_official_specs", "No separate telephoto camera is identified in the reviewed DOOGEE or local launch specifications; its presence is not explicitly ruled out."),
        f("front_camera", "doogee_t10_official_specs", "8 MP front camera", 8, status="VERIFIED", key="frontCameraMp", unit="MP"),
        not_disclosed("video_recording", "doogee_t10_ph_yugatech", "The reviewed manufacturer product page and Philippine launch specification do not state supported video resolutions or frame rates."),
        f("battery_capacity", "doogee_t10_official_specs", "8,300 mAh typical capacity", 8300, status="VERIFIED", key="batteryMah", unit="mAh", note="DOOGEE labels 8,300 mAh as typical capacity; Philippine launch coverage also lists 8,300 mAh."),
        f("battery_technology", "doogee_t10_notebookcheck", "Lithium-polymer battery; YugaTech also lists Li-Po. DOOGEE says only high-density lithium.", "Lithium-polymer (secondary-source classification)", status="VERIFIED_SECONDARY", note="Two exact-model secondary sources identify Li-Po/polymer chemistry. DOOGEE's page does not specify the cell subtype; treat this as secondary-source evidence."),
        f("wired_charging", "doogee_t10_official_specs", "18 W wired charging", 18, status="VERIFIED", key="chargingW", unit="W"),
        not_disclosed("wireless_charging", "doogee_t10_official_specs", "Wireless and reverse charging are not stated in the reviewed manufacturer specification."),
        f("dimensions", "doogee_t10_ph_yugatech", "242.3 x 161.1 x 7.5 mm", "242.3 x 161.1 x 7.5 mm", status="VERIFIED_SECONDARY", key="dimensions", unit="mm", note="YugaTech gives the exact T10 dimensions; manufacturer page independently confirms 7.5 mm thickness. Stored as height x width x depth."),
        f("weight", "doogee_t10_official_specs", "570 g", 570, status="VERIFIED", key="weightG", unit="g", note="DOOGEE's final product page and later Kimovil/Notebookcheck model profiles list 570 g. GSMArena's October 2022 pre-launch preview listed 430 g; the later final product specification resolves that early preview discrepancy."),
        f("materials", "doogee_t10_official_specs", "Aviation-grade aluminum integrated/unibody construction", "Aluminum alloy unibody", status="VERIFIED"),
        not_disclosed("ingress_protection", "doogee_t10_official_specs", "No IP or ingress-protection rating is stated in the reviewed product specification."),
        f("sim_esim", "doogee_t10_ph_yugatech", "Dual SIM; microSDXC uses a shared SIM slot. eSIM is not recorded.", "Dual SIM; shared SIM/microSD tray; eSIM not recorded", status="VERIFIED_SECONDARY", key="sim"),
        f("cellular_bands", "doogee_t10_ph_yugatech", "GSM / HSPA / LTE; exact local frequency bands are not listed.", "GSM / HSPA / 4G LTE; exact Philippine bands not recorded", status="VERIFIED_SECONDARY", key="cellular", note="Record only the reported radio generations. Do not infer Philippine carrier-band compatibility from the chipset or a global Kimovil profile."),
        f("wifi", "doogee_t10_official_specs", "802.11ac dual-band Wi-Fi (2.4 GHz and 5 GHz)", "Wi-Fi 5 (802.11ac), dual-band", status="VERIFIED", key="wifi"),
        f("bluetooth", "doogee_t10_official_specs", "Bluetooth 5.0", "Bluetooth 5.0", status="VERIFIED"),
        f("usb", "doogee_t10_ph_yugatech", "USB Type-C 2.0", "USB Type-C; USB 2.0", status="VERIFIED_SECONDARY", key="ports"),
        not_disclosed("nfc", "doogee_t10_official_specs", "NFC support is not stated in the reviewed manufacturer or Philippine launch sources; no unsupported 'No NFC' claim is made."),
        f("gnss", "doogee_t10_official_specs", "GPS, BeiDou, GLONASS, Galileo and A-GPS", "GPS; BeiDou; GLONASS; Galileo; A-GPS", status="VERIFIED"),
        f("audio", "doogee_t10_notebookcheck", "Dual stereo speakers and a 3.5 mm audio connection", "Dual stereo speakers; 3.5 mm audio jack", status="VERIFIED_SECONDARY", key="sound", note="Exact-model Notebookcheck specification; DOOGEE independently identifies dual stereo speakers."),
        f("sensors", "doogee_t10_kimovil", "Accelerometer and proximity sensor; Notebookcheck lists a gyroscope. Other sensors are not recorded.", "Accelerometer; proximity sensor; gyroscope (documented sensors only)", status="VERIFIED_SECONDARY", note="Combines explicitly listed exact-model secondary references; an omitted sensor is not treated as absent."),
        f("tablet_stylus", "doogee_t10_official_specs", "DOOGEE describes stylus support/compatibility; exact stylus model and package inclusion are not stated.", "Stylus supported; model/package inclusion not recorded", status="VERIFIED", key="stylus"),
        f("tablet_keyboard", "doogee_t10_official_specs", "Detachable full-size keyboard supported as an optional, separately purchased accessory.", "Detachable keyboard supported; sold separately", status="VERIFIED", key="keyboard"),
        f("tablet_cellular_variant", "doogee_t10_ph_yugatech", "The Philippine T10 launch configuration is the LTE-capable model; DOOGEE lists dual 4G LTE.", "GSM / HSPA / 4G LTE; exact Philippine bands not recorded", status="VERIFIED_SECONDARY", key="cellular"),
    ]


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("workbookRow") != 172 or device.get("brand") != "DOOGEE" or device.get("model") != MODEL:
        raise SystemExit("Catalog target guard failed for workbook row 172 DOOGEE T10")
    if device.get("scopeStatus") != "Pending":
        raise SystemExit("Expected supplied workbook scope Pending; refusing to change eligibility")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise SystemExit("Expected one unrecorded configuration placeholder before exact-model review")
    if any(row.get("deviceId") == DEVICE for row in manual["records"]):
        raise SystemExit("DOOGEE T10 already has a manual review; refusing duplicate replacement")

    label = "8 GB RAM / 128 GB storage · 4G LTE (Philippine configuration; SKU not recorded)"
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Dated Philippine launch coverage identifies DOOGEE T10 availability through the official online store from 2023-09-01. Historical introductory pricing ended 2023-09-13. No current price or stock observation was found.",
        "philippineAvailability": "YugaTech and GadgetMatch identify DOOGEE T10 at the Philippine launch with 8 GB physical RAM / 128 GB storage; YugaTech links to the local DOOGEE Lazada listing, and Hungry Geeks reports the official Lazada store open for purchase. This supports Philippine availability for the reported 8/128 LTE model in September 2023, but no numeric local SKU or exact first transaction time is documented. It does not verify current stock.",
        "observedAt": OBSERVED,
        "productLine": "DOOGEE T-series tablets",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Reported Philippine launch/online availability date",
        "researchNotes": "Workbook row 172 matches the exact DOOGEE T10 model, not the similar T10S, T10 Pro, or T30 Pro. Philippine launch sources identify one local 8 GB physical / 128 GB LTE configuration, with no numeric SKU. The 7 GB memory extension is virtual and not counted as physical RAM. The global launch is reported as 2022-11-01; Philippine launch coverage is dated 2023-09-01. Current Philippine price/stock, exact regional SKU, CPU cluster clock, and RAM generation suffix remain unresolved. The workbook eligibility value remains Pending.",
        "qualityFlag": "Exact DOOGEE T10 and PH 8/128 LTE model match supported by manufacturer and Philippine launch sources; current price, numeric PH SKU and several technical details unresolved; workbook scope remains Pending.",
        "openIssues": [
            {"issue": "No numeric Philippine model code or authorized local SKU was found", "action": "Keep modelCode and SKU blank; retain only the source-backed 8/128 LTE configuration."},
            {"issue": "No current exact-model Philippine price or stock observation was located", "action": "Keep current price blank; do not use the discontinued/estimated currency-converted listing."},
            {"issue": "DOOGEE and YugaTech differ on Cortex-A55 maximum clock; DOOGEE and Kimovil differ on LPDDR4 versus LPDDR4X", "action": "Keep CPU cluster-clock and RAM-type fields in CONFLICTING_INFORMATION until exact local evidence resolves them."},
            {"issue": "Some published preview specifications differ from the final manufacturer page", "action": "Use final DOOGEE eMMC / 570 g values and retain the pre-launch GSMArena discrepancy in source notes."},
            {"issue": "Display cover material, video modes, NFC, exact LTE bands, eSIM and ingress rating are not disclosed in reviewed sources", "action": "Leave those claims blank or marked Not disclosed; do not infer from similar models or the chipset."},
            {"issue": "DOOGEE product imagery is exact but reuse terms require written permission for business use", "action": "Keep the neutral placeholder unless reusable permission or a license is obtained."},
            {"issue": "Study eligibility remains Pending in the supplied workbook", "action": "Preserve the workbook's scope status; research verification does not change eligibility."},
        ],
    }
    variant = {"id": CONFIG, "label": label, "modelCode": None, "sku": None,
               "notes": "Philippine launch reporting identifies 8 GB physical RAM / 128 GB storage and LTE; a numeric local SKU is not recorded."}
    item = {
        "deviceId": DEVICE, "configurationId": CONFIG, "brand": "DOOGEE", "model": MODEL,
        "configuration": label, "sources": SOURCES, "fields": fields(),
        "replacementVariants": [variant], "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": availability,
    }
    if len(item["fields"]) != 49 or {row["fieldId"] for row in item["fields"]} != {
        "model_number", "global_release_date", "configuration", "philippine_release_date", "official_launch_price_php", "current_price_php",
        "display_size", "display_technology", "display_resolution", "display_refresh_rate", "display_brightness", "display_protection",
        "chipset", "process_node", "cpu", "gpu", "operating_system", "os_support", "ram_capacity", "ram_type", "storage_capacity",
        "storage_type", "storage_expansion", "rear_camera_system", "main_camera_sensor", "ultrawide_camera", "telephoto_camera",
        "front_camera", "video_recording", "battery_capacity", "battery_technology", "wired_charging", "wireless_charging",
        "dimensions", "weight", "materials", "ingress_protection", "sim_esim", "cellular_bands", "wifi", "bluetooth", "usb",
        "nfc", "gnss", "audio", "sensors", "tablet_stylus", "tablet_keyboard", "tablet_cellular_variant",
    }:
        raise SystemExit("DOOGEE T10 review does not cover the complete 49-field tablet audit schema")

    add_review(manual, catalog, item)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    manual["reviewedAt"] = OBSERVED

    images[DEVICE] = {
        "status": "REUSE_PERMISSION_REQUIRED",
        "reason": "DOOGEE's exact-model product page shows the DOOGEE T10. The brand's terms prohibit copying/reproducing site content or using product images for business use without written permission; no reusable license or permission was found. Keep the neutral placeholder.",
        "sourcePage": URL_DOOGEE,
        "assetUrl": IMAGE_URL,
        "scope": "DOOGEE T10 Space Gray product image; image is model-level and does not identify a local numeric SKU.",
        "rightsTermsUrl": URL_TERMS,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for DOOGEE T10",
    }

    prices = [
        {
            "device_id": DEVICE, "configuration_id": CONFIG, "variant_ram_gb": 8,
            "variant_storage_gb": 128, "variant_connectivity": "4G LTE",
            "configuration_match": "ph_8gb_physical_128gb_4g_lte_model_match_sku_unlisted",
            "amount_php": 9499, "price_type": "historical_ph_launch_srp",
            "source_published_at": "2023-09-01", "observed_at": OBSERVED,
            "source_url": URL_HUNGRYGEEKS, "source_kind": "historical_ph_launch_price",
            "local_availability_verified": True,
            "availability_status": "reported_launch_srp; not_current_price",
            "review_status": "VERIFIED_SECONDARY",
            "excerpt": "Philippine launch reporting lists DOOGEE T10 SRP PHP 9,499 for the local model/configuration; numeric SKU was not stated.",
        },
        {
            "device_id": DEVICE, "configuration_id": CONFIG, "variant_ram_gb": 8,
            "variant_storage_gb": 128, "variant_connectivity": "4G LTE",
            "configuration_match": "ph_8gb_physical_128gb_4g_lte_model_match_sku_unlisted",
            "amount_php": 8399, "price_type": "historical_ph_introductory_promo_2023-09-01_to_13",
            "source_published_at": "2023-09-01", "observed_at": OBSERVED,
            "source_url": URL_HUNGRYGEEKS, "source_kind": "historical_ph_launch_promotion",
            "local_availability_verified": True,
            "availability_status": "expired_2023-09-13; not_current_price",
            "review_status": "VERIFIED_SECONDARY",
            "excerpt": "Launch report lists the introductory PHP 8,399 price through September 13, 2023; this is a historical promotion, not a current offer.",
        },
    ]
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "DOOGEE", "model_name": MODEL,
                    "category": "tablets", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_DOOGEE, "result": "Exact DOOGEE T10 manufacturer product page reviewed for final model specifications."},
            {"device_id": DEVICE, "source_url": URL_YUGATECH, "result": "Philippine launch coverage names T10 and reports local 8/128 configuration and PHP 9,499 SRP / PHP 8,399 promo."},
            {"device_id": DEVICE, "source_url": URL_GADGETMATCH, "result": "Independent Philippine T10 launch/configuration and price cross-check."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "Exact-model pre-launch article; planned 2022-11-01 launch but early 430 g/UFS values differ from final manufacturer specs."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Exact model profile reviewed; global-only information, with LPDDR4X conflict retained and no PH price inferred."},
            {"device_id": DEVICE, "source_url": URL_NOTEBOOKCHECK, "result": "Exact-model technical table reviewed for 60 Hz, GPU, audio, dimensions, battery and final 570 g weight."},
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "Pinoy Techno Guide reference site searched for the exact DOOGEE T10; no exact model article was located in this pass."},
            {"device_id": DEVICE, "source_url": URL_NANOREVIEW, "result": "NanoReview reference site searched for the exact DOOGEE T10; no exact model profile was located in this pass."},
            {"device_id": DEVICE, "source_url": URL_YUGATECH_PRICES, "result": "Current YugaTech price index dated 2026-11-26 has no exact T10 price row; no current price inferred."},
            {"device_id": DEVICE, "source_url": URL_TERMS, "result": "Official DOOGEE terms do not grant reuse of product images for business use without written permission; exact T10 image left unavailable."},
        ],
        "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    model = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if model:
        model["status"] = "manually_reviewed"
    known = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type"), p.get("source_url"), p.get("configuration_match")) for p in latest.get("prices", [])}
    for price in prices:
        key = (price["device_id"], price["configuration_id"], price["price_type"], price["source_url"], price["configuration_match"])
        if key not in known:
            latest.setdefault("prices", []).append(price)
            known.add(key)
    latest["run_at"] = OBSERVED
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "DOOGEE T10", "workbookRow": 172, "configuration": label,
                      "reviewedFields": len(item["fields"]),
                      "verified": sum(r["status"] in {"VERIFIED", "VERIFIED_SECONDARY"} for r in item["fields"]),
                      "conflicts": [r["fieldId"] for r in item["fields"] if r["status"] == "CONFLICTING_INFORMATION"],
                      "notDisclosed": sum(r["status"] == "NOT_DISCLOSED" for r in item["fields"]),
                      "currentPrice": None, "historicalPrices": [9499, 8399],
                      "image": "exact manufacturer image found; reuse permission required; placeholder retained",
                      "scopeStatus": "Pending (preserved)"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
