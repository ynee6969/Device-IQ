#!/usr/bin/env python3
"""Record sourced Philippine configurations for Xiaomi Redmi Note 10."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/redmi-note-10-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_91090601d354b8"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG_4_64 = f"{DEVICE}-4gb-64gb-ph"
CONFIG_6_128 = f"{DEVICE}-6gb-128gb-ph"

URL_XIAOMI = "https://www.mi.com/global/product/redmi-note-10/specs/"
URL_MANUAL = "https://alsgp0.fds.api.xiaomi.com/gl123/Redmi/Redmi%20Note%2010/%E9%87%8F%E4%BA%A7/K7A_%E8%8B%B1%E6%B3%B0%E5%8F%8C%E8%AF%AD%E7%89%88_V1%3DGUID-ECC851F1-4529-4207-AA02-87DAAA9A5B29%3D1%3Den%3D.pdf"
URL_XIAOMI_FAQ = "https://www.mi.com/uk/support/faq/details/KA-07683/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/xiaomi-redmi-note-10"
URL_YUGA = "https://www.yugatech.com/mobile/xiaomi-redmi-note-10-ph-price/"
URL_REVU = "https://www.revu.com.ph/2021/03/redmi-note-10-price-in-philippines-specs/"
URL_NTC = "https://region4b.ntc.gov.ph/wp-content/uploads/2022/01/GEC_12312021.pdf"
URL_QUALCOMM = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/prod_brief_qcom_sd678.pdf"
URL_NANOREVIEW = "https://nanoreview.net/en/soc/qualcomm-snapdragon-678"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-xiaomi-redmi-note-10"
URL_GSMARENA = "https://fo.gsmarena.com/xiaomi_redmi_note_10-10247.php"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("redmi_note_10_xiaomi_specs", "Xiaomi Global", URL_XIAOMI,
           "Primary exact-model specifications and regional configuration reference",
           "Xiaomi lists global 4 GB / 64 GB, 4 GB / 128 GB, and 6 GB / 128 GB configurations. Its local launch coverage supports only 4 GB / 64 GB and 6 GB / 128 GB for the Philippines, so 4 GB / 128 GB is not added as a local variant. The global page documents display, Snapdragon 678, LPDDR4X / UFS 2.2, cameras, battery, dimensions, and connectivity; it flags IP53 as TBD."),
    source("redmi_note_10_xiaomi_manual", "Xiaomi", URL_MANUAL,
           "Primary model identity and display-protection reference",
           "The official quick-start guide identifies Redmi model M2101K7AG and states that the phone uses Corning Gorilla Glass 3. The same code is listed in the Philippine NTC equipment register."),
    source("redmi_note_10_xiaomi_faq", "Xiaomi UK Support", URL_XIAOMI_FAQ,
           "Manufacturer support cross-check for regional capabilities and unresolved feature claims",
           "Xiaomi's exact-model FAQ states no NFC, no eSIM, 4G only, Bluetooth 5.0, IP53, dual SIM plus dedicated microSD, and MIUI 12 based on Android 11. Its IP53 statement is retained as a model-level claim because Xiaomi's global product page marks the rating TBD and GSMArena notes regional dependence; local IP53 applicability remains unresolved."),
    source("redmi_note_10_ptg_ph", "PinoyTechGuide Philippines", URL_PTG,
           "Philippine configurations, prices, launch promotion, and exact-model specs",
           "Published March 12, 2021. Lists local 4 GB / 64 GB at PHP 8,490, with a stated PHP 7,990 introductory price on March 13, and 6 GB / 128 GB at PHP 9,990. Its specifications cover display, build, cameras, battery, NFC, connectivity, and sensors. Exact-model product imagery is present, but reuse permission is not recorded.",
           "2021-03-12"),
    source("redmi_note_10_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine availability and independent launch configuration/specification cross-check",
           "Published March 12, 2021. Reports Xiaomi Philippines' launch, the 4 GB / 64 GB and 6 GB / 128 GB configurations, and availability from March 13 through Lazada, Authorized Mi Stores, and official offline channels. It agrees on most hardware specifications, but lists Bluetooth 5.1 while Xiaomi and PTG list 5.0; keep Bluetooth unresolved.",
           "2021-03-12"),
    source("redmi_note_10_revu_ph", "REVU Philippines", URL_REVU,
           "Contemporaneous local launch pricing and first-sale-day promotion cross-check",
           "Reports PHP 8,490 for 4 GB / 64 GB and PHP 9,990 for 6 GB / 128 GB, with the first-sale-day base-variant offer PHP 500 below its usual price. PTG gives the exact introductory amount of PHP 7,990 on March 13, 2021.",
           "2021-03-12"),
    source("redmi_note_10_ntc_gec", "National Telecommunications Commission Philippines", URL_NTC,
           "Local equipment-registration match for model M2101K7AG",
           "NTC GEC record ESD-GEC-2106586 lists Redmi M2101K7AG, applicant Xiaomi Communications Co Ltd, issued February 24, 2021. The frequency row includes 13.56 MHz but does not identify that entry as an NFC feature; it is not used to override direct Xiaomi and PTG statements that NFC is absent." ,
           "2021-02-24"),
    source("redmi_note_10_qualcomm_678", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 678 architecture and platform reference",
           "Qualcomm identifies the Snapdragon 678 as an 11 nm platform with Kryo 460 CPU up to 2.2 GHz and Adreno 612 graphics. Platform capabilities are not used as a substitute for handset-specific feature confirmation."),
    source("redmi_note_10_nanoreview_678", "NanoReview", URL_NANOREVIEW,
           "Independent Snapdragon 678 architecture cross-check",
           "NanoReview lists an 8-core Snapdragon 678 at 11 nm with two Kryo 460 Gold cores up to 2.2 GHz and six Kryo 460 Silver cores up to 1.7 GHz. Used as a chipset-level technical cross-check, not as a Redmi Note 10 benchmark or device measurement."),
    source("redmi_note_10_kimovil", "Kimovil", URL_KIMOVIL,
           "Exact-model global variant and identity cross-check",
           "The exact Redmi Note 10 page lists several global and India memory variants and an aggregate March 2021 release month. Its regional price listings and aliases are not used to assert Philippine prices, local configurations, or model-code identity."),
    source("redmi_note_10_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-model global release and technical cross-check",
           "The exact Redmi Note 10 page lists announcement on March 4 and release on March 16, 2021, plus the 4 GB / 64 GB and 6 GB / 128 GB variants. This global release date is kept separate from Philippine retail availability on March 13. GSMArena notes IP53 availability can vary by market."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, config_match: str,
          catalog_value=None, price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": config_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        item["unit"] = unit
    if price_type:
        item["priceType"] = price_type
    return item


def fields_for(ram: int, storage: int, launch_price: int) -> list[dict]:
    config = f"Philippine Redmi Note 10, {ram} GB RAM / {storage} GB storage"
    rows = [
        field("model_number", "redmi_note_10_ntc_gec", "NTC-registered Redmi model M2101K7AG; Xiaomi's official guide gives the same model code", "M2101K7AG", status="VERIFIED", note="The Philippine NTC register contains M2101K7AG and the exact-model Xiaomi guide confirms the code. Local launch sources identify the corresponding marketed handset as Redmi Note 10.", config_match="Philippine Redmi Note 10 model; local GEC code M2101K7AG"),
        field("global_release_date", "redmi_note_10_gsmarena", "GSMArena lists announcement on March 4, 2021 and release on March 16, 2021", "2021-03-16", status="VERIFIED_SECONDARY", note="Use the global availability/release date, not the March 4 announcement. The Philippine retail date is recorded separately.", config_match="Global Redmi Note 10 model-level release information"),
        field("configuration", "redmi_note_10_ptg_ph", f"Philippine Redmi Note 10: {ram} GB RAM / {storage} GB storage", f"{ram} GB RAM / {storage} GB storage", status="VERIFIED_SECONDARY", note="PTG and YugaTech identify the local 4 GB / 64 GB and 6 GB / 128 GB variants. Xiaomi lists an additional global 4 GB / 128 GB configuration, which is not added locally without Philippine launch evidence.", config_match=config),
        field("philippine_release_date", "redmi_note_10_yugatech_ph", "Xiaomi Philippines launch coverage says official online and authorized-store availability began March 13, 2021", "2021-03-13", status="VERIFIED_SECONDARY", note="The March 12 date is the announcement/publication date; March 13 is the reported local first-sale date.", config_match="Philippine Redmi Note 10 launch; both locally listed configurations"),
        field("official_launch_price_php", "redmi_note_10_ptg_ph", f"Philippine launch price: PHP {launch_price:,} for {ram} GB / {storage} GB", launch_price, status="VERIFIED_SECONDARY", unit="PHP", note="Historical Philippine launch price for this exact configuration. It is not a current price.", config_match=config, price_type="historical_ph_launch_price"),
        field("current_price_php", "redmi_note_10_ptg_ph", "Reviewed local offers and prices are from March 2021; no current dated and orderable Philippine offer was verified", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank. Preserve the March 13, 2021 PHP 7,990 introductory offer for the 4 GB / 64 GB configuration as historical only.", config_match=config, price_type="no_current_offer_verified"),
        field("display_size", "redmi_note_10_xiaomi_specs", "6.43-inch AMOLED DotDisplay", 6.43, status="VERIFIED", key="displayInches", unit="in", note="Xiaomi's exact-model specification; local launch coverage reports the same display size.", config_match=config),
        field("display_technology", "redmi_note_10_xiaomi_specs", "Super AMOLED", "Super AMOLED", status="VERIFIED", key="displayType", note="Xiaomi identifies an AMOLED DotDisplay; PTG describes it as Super AMOLED.", config_match=config),
        field("display_resolution", "redmi_note_10_xiaomi_specs", "2400 x 1080 pixels, 409 ppi", "2400 x 1080", status="VERIFIED", key="resolution", note="Xiaomi, PTG, and YugaTech agree on 2400 x 1080; no conflicting value was found.", config_match=config),
        field("display_refresh_rate", "redmi_note_10_xiaomi_specs", "Refresh-rate value not listed in the reviewed Xiaomi or Philippine launch specifications", None, status="NOT_DISCLOSED", unit="Hz", note="Do not infer 60 Hz from omission or chipset capability.", config_match=config),
        field("display_brightness", "redmi_note_10_xiaomi_specs", "700 nits HBM typical; 1100 nits peak typical", 700, status="VERIFIED", unit="nits", note="Record Xiaomi's HBM typical figure as the catalog numeric brightness; retain peak figure in the field text.", config_match=config),
        field("display_protection", "redmi_note_10_xiaomi_manual", "Corning Gorilla Glass 3", "Corning Gorilla Glass 3", status="VERIFIED", note="The exact-model Xiaomi quick-start guide identifies Gorilla Glass 3; PTG and YugaTech corroborate it.", config_match=config),
        field("chipset", "redmi_note_10_xiaomi_specs", "Qualcomm Snapdragon 678", "Qualcomm Snapdragon 678", status="VERIFIED", key="chipset", note="Xiaomi and local launch sources identify Snapdragon 678.", config_match=config),
        field("process_node", "redmi_note_10_qualcomm_678", "11 nm process", 11, status="VERIFIED", unit="nm", note="Qualcomm's product brief gives the Snapdragon 678 process node.", config_match=config),
        field("cpu", "redmi_note_10_nanoreview_678", "2x Kryo 460 Gold / Cortex-A76 up to 2.2 GHz + 6x Kryo 460 Silver / Cortex-A55 up to 1.7 GHz", "2x Cortex-A76 2.2 GHz + 6x Cortex-A55 1.7 GHz", status="VERIFIED_SECONDARY", key="cpu", note="NanoReview's chipset-level core breakdown; Qualcomm confirms Kryo 460 family and up to 2.2 GHz. This is CPU platform detail, not a handset performance score.", config_match=config),
        field("gpu", "redmi_note_10_xiaomi_specs", "Qualcomm Adreno 612", "Qualcomm Adreno 612", status="VERIFIED", key="gpu", note="Xiaomi and Qualcomm identify Adreno 612 for the Snapdragon 678.", config_match=config),
        field("operating_system", "redmi_note_10_xiaomi_specs", "MIUI 12 based on Android 11 at launch", "MIUI 12 based on Android 11", status="VERIFIED", key="os", note="Record the launch OS; later update versions are not substituted for factory software.", config_match=config),
        field("os_support", "redmi_note_10_xiaomi_faq", "No guaranteed update duration or end-of-support date stated in the reviewed manufacturer material", None, status="NOT_DISCLOSED", note="Later software releases do not establish a formal update-support commitment.", config_match=config),
        field("ram_capacity", "redmi_note_10_ptg_ph", f"{ram} GB RAM", ram, status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="The exact locally reported RAM/storage configuration; physical RAM only.", config_match=config),
        field("ram_type", "redmi_note_10_xiaomi_specs", "LPDDR4X", "LPDDR4X", status="VERIFIED", note="Xiaomi identifies LPDDR4X for the Redmi Note 10 configurations.", config_match=config),
        field("storage_capacity", "redmi_note_10_ptg_ph", f"{storage} GB internal storage", storage, status="VERIFIED_SECONDARY", key="storageGb", unit="GB", note="The exact Philippine configuration is separately identified in local launch coverage.", config_match=config),
        field("storage_type", "redmi_note_10_xiaomi_specs", "UFS 2.2", "UFS 2.2", status="VERIFIED", key="storageType", note="Xiaomi lists UFS 2.2 storage for the Redmi Note 10 family; the local launch sources confirm these capacities.", config_match=config),
        field("storage_expansion", "redmi_note_10_xiaomi_specs", "Dedicated microSD slot; maximum supported capacity not listed on the reviewed Xiaomi page", "Dedicated microSD slot; capacity limit not recorded", status="VERIFIED", note="Xiaomi and YugaTech confirm a dedicated slot. Do not infer a card-size limit.", config_match=config),
        field("rear_camera_system", "redmi_note_10_xiaomi_specs", "48 MP main + 8 MP 118-degree ultra-wide + 2 MP macro + 2 MP depth", "48 MP main + 8 MP ultra-wide + 2 MP macro + 2 MP depth", status="VERIFIED", key="rearCameraMp", unit="MP", note="Complete rear camera set from Xiaomi; catalog numeric value is the main sensor resolution.", config_match=config, catalog_value=48),
        field("main_camera_sensor", "redmi_note_10_xiaomi_specs", "48 MP main camera, 1/2-inch sensor size, 0.8 μm pixel size, f/1.79, PDAF; maker/model not named", "1/2-inch sensor size; maker/model not disclosed", status="VERIFIED", note="Record published sensor dimensions; do not infer a manufacturer or sensor part number.", config_match=config),
        field("ultrawide_camera", "redmi_note_10_xiaomi_specs", "8 MP ultra-wide camera, 118-degree field of view, f/2.2", "8 MP ultra-wide; 118-degree field of view", status="VERIFIED", note="Xiaomi's exact-model camera specification.", config_match=config),
        field("telephoto_camera", "redmi_note_10_xiaomi_specs", "The complete listed rear camera system has main, ultra-wide, macro, and depth modules; no telephoto module is listed", "No telephoto camera listed", status="NOT_APPLICABLE", note="Based on the complete manufacturer rear-camera specification.", config_match=config),
        field("front_camera", "redmi_note_10_xiaomi_specs", "13 MP front camera, f/2.45", 13, status="VERIFIED", key="frontCameraMp", unit="MP", note="Xiaomi's exact-model specification; local coverage corroborates 13 MP.", config_match=config),
        field("video_recording", "redmi_note_10_xiaomi_specs", "Rear: 4K at 30 fps, 1080p at 60/30 fps; front: 1080p at 30 fps and 720p at 30 fps", "Rear 4K30 and 1080p60/30; front 1080p30 and 720p30", status="VERIFIED", key="video", note="Record only manufacturer-listed modes; do not extend the front-camera capability based on SoC support.", config_match=config),
        field("battery_capacity", "redmi_note_10_xiaomi_specs", "5000 mAh typical", 5000, status="VERIFIED", key="batteryMah", unit="mAh", note="Xiaomi's exact-model typical capacity; local sources agree.", config_match=config),
        field("battery_technology", "redmi_note_10_ptg_ph", "Li-Po, non-removable", "Li-Po; non-removable", status="VERIFIED_SECONDARY", note="PTG specifies chemistry and construction; Xiaomi confirms the battery capacity.", config_match=config),
        field("wired_charging", "redmi_note_10_xiaomi_specs", "33 W wired fast charging", 33, status="VERIFIED", key="chargingW", unit="W", note="Xiaomi and Philippine launch coverage identify 33 W wired charging.", config_match=config),
        field("wireless_charging", "redmi_note_10_xiaomi_specs", "Wireless and reverse wireless charging are not listed in the reviewed specification", None, status="NOT_DISCLOSED", note="Do not convert omitted capability details into a confirmed negative.", config_match=config),
        field("dimensions", "redmi_note_10_xiaomi_specs", "160.46 x 74.5 x 8.29 mm", "160.46 x 74.5 x 8.29 mm", status="VERIFIED", key="dimensions", unit="mm", note="Xiaomi's exact-model dimensions; PTG agrees.", config_match=config),
        field("weight", "redmi_note_10_xiaomi_specs", "178.8 g", 178.8, status="VERIFIED", key="weightG", unit="g", note="Xiaomi's exact-model figure; PTG agrees.", config_match=config),
        field("materials", "redmi_note_10_gsmarena", "Glass front with Gorilla Glass 3; plastic back and plastic frame", "Gorilla Glass 3 front; plastic back and frame", status="VERIFIED_SECONDARY", note="Exact-model GSMArena build description; Xiaomi's user guide independently confirms the front glass. No additional material layer is inferred.", config_match=config),
        field("ingress_protection", "redmi_note_10_xiaomi_specs", "Xiaomi global spec page marks IP53 as TBD; Xiaomi UK FAQ says IP53; GSMArena notes market-dependent availability", None, status="CONFLICTING_INFORMATION", note="Do not publish IP53 as a confirmed Philippine-SKU rating until local applicability is established.", config_match="Model-level sources differ; PH configuration certification not resolved"),
        field("sim_esim", "redmi_note_10_xiaomi_faq", "Dual Nano-SIM plus dedicated microSD slot; eSIM unsupported", "Dual Nano-SIM; dedicated microSD; no eSIM", status="VERIFIED", key="sim", note="Xiaomi FAQ explicitly documents the physical SIM/card-slot layout and no eSIM.", config_match=config),
        field("cellular_bands", "redmi_note_10_xiaomi_specs", "Global model: GSM 850/900/1800/1900; WCDMA B1/2/4/5/8; LTE FDD B1/2/3/4/5/7/8/20/28; LTE TDD B38/40/41. No 5G.", "Global Redmi Note 10 4G bands: GSM 850/900/1800/1900; WCDMA B1/2/4/5/8; LTE FDD B1/2/3/4/5/7/8/20/28; LTE TDD B38/40/41", status="VERIFIED", key="cellular", note="Xiaomi global specification and support FAQ identify these 4G bands and no 5G. This is not a carrier-compatibility guarantee for every local network.", config_match=config),
        field("wifi", "redmi_note_10_ptg_ph", "Dual-band Wi-Fi 802.11 b/g/n/ac; Xiaomi confirms 2.4 GHz and 5 GHz operation", "Dual-band Wi-Fi 802.11 b/g/n/ac", status="VERIFIED_SECONDARY", key="wifi", note="PTG gives the protocol list; Xiaomi confirms both bands.", config_match=config),
        field("bluetooth", "redmi_note_10_xiaomi_specs", "Xiaomi global page and FAQ specify Bluetooth 5.0; YugaTech launch coverage reports 5.1", None, status="CONFLICTING_INFORMATION", note="Keep Bluetooth unset pending an exact Philippine unit or manufacturer clarification.", config_match=config),
        field("usb", "redmi_note_10_xiaomi_specs", "USB Type-C; interface generation not stated", "USB Type-C", status="VERIFIED", key="ports", note="Connector type only; no data-transfer rate inferred.", config_match=config),
        field("nfc", "redmi_note_10_xiaomi_faq", "Xiaomi FAQ and PTG say NFC is unsupported; NTC's M2101K7AG register line includes 13.56 MHz without labeling that entry as NFC", None, status="CONFLICTING_INFORMATION", note="Do not promote either presence or absence while the local certification line is ambiguous; the public NFC field remains blank.", config_match="Philippine M2101K7AG variant; local certification interpretation unresolved"),
        field("gnss", "redmi_note_10_xiaomi_specs", "GPS L1, Galileo E1, GLONASS G1, BeiDou", "GPS, Galileo, GLONASS, BeiDou", status="VERIFIED", key="gnss", note="Xiaomi's exact-model navigation specification; local PTG listing corroborates the named systems.", config_match=config),
        field("audio", "redmi_note_10_xiaomi_specs", "Dual speakers, 3.5 mm headphone jack, Hi-Res Audio certification", "Dual speakers; 3.5 mm jack; Hi-Res Audio", status="VERIFIED", key="sound", note="Xiaomi's exact-model audio specification; local coverage agrees.", config_match=config),
        field("sensors", "redmi_note_10_xiaomi_specs", "Proximity, ambient light, accelerometer, gyroscope, electronic compass, linear motor, IR blaster; side fingerprint sensor", "Proximity, ambient light, accelerometer, gyroscope, compass, linear motor, IR blaster, side fingerprint", status="VERIFIED", note="Xiaomi's exact-model sensor and side fingerprint specifications.", config_match=config),
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
        "availabilityStatus": "Xiaomi Philippines launch reporting identifies official online and authorized-store availability from March 13, 2021. Workbook eligibility remains Pending.",
        "philippineAvailability": "Xiaomi Philippines' March 12, 2021 launch coverage and independent Philippine sources report Redmi Note 10 retail availability from March 13 through the official online store, Authorized Mi Stores, and official offline channels. The locally documented configurations are 4 GB / 64 GB and 6 GB / 128 GB. This verifies reported local launch availability, not present-day stock or orderability.",
        "observedAt": OBSERVED,
        "manufacturer": "Xiaomi Corporation",
        "catalogModel": "Redmi Note 10",
        "productLine": "Redmi Note 10 series",
        "modelNumber": "M2101K7AG",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Reported Philippine retail availability date",
        "researchNotes": "Workbook row 48 'Redmi Note 10' matches Xiaomi's Redmi Note 10. Local launch reporting identifies two Philippine configurations: 4 GB / 64 GB and 6 GB / 128 GB; the global 4 GB / 128 GB option is not added locally. The Philippine NTC register and Xiaomi quick-start guide identify model M2101K7AG. Launch prices are historical, including a dated 4 GB / 64 GB introductory price of PHP 7,990 on March 13, 2021. Current price remains blank. Bluetooth version, NFC, and IP53 applicability retain unresolved source conflicts. Workbook eligibility remains Pending.",
        "qualityFlag": "Philippine release, M2101K7AG model code, and two local variants verified; current price is not verified; Bluetooth, NFC, and IP53 status retain evidence conflicts; eligibility remains Pending.",
        "openIssues": [
            {"issue": "Global Xiaomi specs and UK support FAQ do not agree on whether IP53 applies, and GSMArena notes market dependence", "action": "Keep IP rating blank for the Philippine configuration."},
            {"issue": "Xiaomi and PTG list Bluetooth 5.0 while YugaTech reports 5.1", "action": "Keep Bluetooth version blank pending an exact local hardware confirmation."},
            {"issue": "Xiaomi FAQ and PTG say NFC is absent, while the NTC register lists an unexplained 13.56 MHz entry for M2101K7AG", "action": "Keep NFC unresolved until the certification frequency field is authoritatively mapped."},
            {"issue": "Only 2021 launch MSRPs and a first-day introductory price were verified", "action": "Keep current price blank; preserve dated historical amounts."},
            {"issue": "Exact Redmi Note 10 photographs appear on Xiaomi and PTG pages without recorded reuse permission", "action": "Keep the neutral image placeholder until rights are established."},
            {"issue": "Workbook eligibility status remains Pending", "action": "Preserve Pending and follow existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "redmi"
            or device.get("model", "").casefold() != "note 10"):
        raise ValueError("Inventory row no longer matches Redmi Note 10")
    variant_ids = {variant.get("id") for variant in device.get("variants", [])}
    if variant_ids - {OLD_CONFIG, CONFIG_4_64, CONFIG_6_128}:
        raise ValueError(f"Unexpected Redmi Note 10 configurations: {sorted(variant_ids)}")

    variants = [
        {"id": CONFIG_4_64, "label": "4 GB RAM / 64 GB storage", "sku": None,
         "modelCode": "M2101K7AG",
         "notes": "Philippine launch sources document this configuration at PHP 8,490 MSRP and a historical PHP 7,990 introductory offer on March 13, 2021. Colors Onyx Gray, Pebble White, and Lake Green are listed at model level; no color-to-storage SKU mapping is documented.",
         "workbookRow": 48},
        {"id": CONFIG_6_128, "label": "6 GB RAM / 128 GB storage", "sku": None,
         "modelCode": "M2101K7AG",
         "notes": "Philippine launch sources document this higher-memory configuration at PHP 9,990. Colors Onyx Gray, Pebble White, and Lake Green are listed at model level; no color-to-storage SKU mapping is documented.",
         "workbookRow": 48},
    ]
    records = []
    for index, (variant, ram, storage, price) in enumerate((
            (variants[0], 4, 64, 8490), (variants[1], 6, 128, 9990))):
        records.append({
            "deviceId": DEVICE,
            "configurationId": variant["id"],
            "brand": "Redmi",
            "model": "Redmi Note 10",
            "configuration": variant["label"],
            "configurationLabel": variant["label"],
            "modelCode": "M2101K7AG",
            "sources": SOURCES,
            "fields": fields_for(ram, storage, price),
            "availabilityEvidence": availability_evidence(),
            **({"replacementVariants": variants,
                "replaceUnrecordedPlaceholder": True} if index == 0 else {}),
        })
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].extend(records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Exact Redmi Note 10 photographs are present on Xiaomi's specification page and PinoyTechGuide, but no reusable image license or permission to copy/embed is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_XIAOMI,
        "assetUrl": None,
        "scope": "Redmi Note 10; Philippine 4 GB / 64 GB and 6 GB / 128 GB variants",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Xiaomi Redmi Note 10",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 8490, "configuration_id": CONFIG_4_64,
         "configuration_match": "exact_philippine_4gb_64gb_configuration", "variant_ram_gb": 4,
         "variant_storage_gb": 64, "price_type": "historical_ph_launch_price",
         "source_published_at": "2021-03-12",
         "excerpt": "Philippine launch coverage lists PHP 8,490 for the Redmi Note 10 4 GB / 64 GB configuration.",
         "source_url": URL_PTG, "source_kind": "historical_local_launch_price",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 7990, "configuration_id": CONFIG_4_64,
         "configuration_match": "exact_philippine_4gb_64gb_configuration", "variant_ram_gb": 4,
         "variant_storage_gb": 64, "price_type": "historical_ph_introductory_price",
         "source_published_at": "2021-03-12",
         "excerpt": "PinoyTechGuide lists an introductory PHP 7,990 price for the 4 GB / 64 GB configuration on March 13, 2021; REVU independently reports a PHP 500 first-day reduction from PHP 8,490.",
         "source_url": URL_PTG, "source_kind": "dated_local_launch_promotion",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_introductory_price_not_current"},
        {"device_id": DEVICE, "amount_php": 9990, "configuration_id": CONFIG_6_128,
         "configuration_match": "exact_philippine_6gb_128gb_configuration", "variant_ram_gb": 6,
         "variant_storage_gb": 128, "price_type": "historical_ph_launch_price",
         "source_published_at": "2021-03-12",
         "excerpt": "Philippine launch coverage lists PHP 9,990 for the Redmi Note 10 6 GB / 128 GB configuration.",
         "source_url": URL_PTG, "source_kind": "historical_local_launch_price",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Redmi", "model_name": "Redmi Note 10", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "PTG lists the 4 GB / 64 GB configuration at PHP 8,490, with an explicit introductory price of PHP 7,990 on March 13, 2021, and 6 GB / 128 GB at PHP 9,990."},
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech reports official local availability of 4 GB / 64 GB and 6 GB / 128 GB configurations beginning March 13, 2021."},
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC GEC record ESD-GEC-2106586 lists model M2101K7AG for Xiaomi Communications Co Ltd; a 13.56 MHz entry is not assumed to prove NFC."},
            {"device_id": DEVICE, "source_url": URL_XIAOMI, "result": "Xiaomi's global specification includes 4 GB / 64 GB, 4 GB / 128 GB, and 6 GB / 128 GB; only two local launch configurations are added."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 48 Redmi Note 10 -> Philippine Xiaomi Redmi Note 10 / M2101K7AG",
        "configurations": [{"label": item["label"], "launchPricePhp": price}
                           for item, price in zip(variants, (8490, 9990))],
        "introductoryOffer": {"configuration": variants[0]["label"], "pricePhp": 7990, "date": "2021-03-13"},
        "reviewedFields": sum(len(item["fields"]) for item in records),
        "philippineAvailabilityDate": "2021-03-13",
        "currentPrices": "blank; no current orderable offer verified",
        "image": "neutral placeholder; reuse rights not established",
        "unresolved": ["Bluetooth version", "NFC capability", "local IP53 applicability"],
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
