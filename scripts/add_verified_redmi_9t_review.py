#!/usr/bin/env python3
"""Record sourced Philippine configurations for Xiaomi Redmi 9T."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/redmi-9t-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_b52492e270dd1f"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG_4_64 = f"{DEVICE}-4gb-64gb-ph"
CONFIG_6_128 = f"{DEVICE}-6gb-128gb-ph"

URL_XIAOMI = "https://www.mi.com/global/product/redmi-9t/specs/"
URL_MANUAL = "https://alsgp0.fds.api.xiaomi.com/xiaomi-b2c-i18n-upload/user-guides/e56de73a0ee9963f98e3095146ed23cb.pdf"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/xiaomi-redmi-9t"
URL_REVU = "https://www.revu.com.ph/2021/01/xiaomi-redmi-9t-price-specs-philippines/"
URL_NOYPI = "https://www.noypigeeks.com/android/redmi-9t-price-philippines/"
URL_GADGET_PILIPINAS = "https://www.gadgetpilipinas.net/2021/01/redmi-9t-launches-in-ph-priced/"
URL_QUALCOMM = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/snapdragon-662-mobile-platform-product-brief.pdf"
URL_GSMARENA = "https://www.gsmarena.com/xiaomi_redmi_9t-pictures-10670.php"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("redmi_9t_xiaomi_specs", "Xiaomi Global", URL_XIAOMI,
           "Primary exact-model specifications and technical cross-check",
           "Xiaomi's Redmi 9T specification page lists 4 GB / 64 GB, 4 GB / 128 GB, and 6 GB / 128 GB global configurations, with LPDDR4X RAM, configuration-specific UFS storage, display, Snapdragon 662, cameras, battery, charging, radios, sensors, and dimensions. The Philippine launch sources identify only 4 GB / 64 GB and 6 GB / 128 GB locally; the 4 GB / 128 GB global option is not added as a Philippine variant. The page notes that availability varies by region and images are illustrations."),
    source("redmi_9t_xiaomi_manual", "Xiaomi", URL_MANUAL,
           "Primary user-guide identity reference",
           "The official Redmi 9T user guide identifies product model M2010J19SG. The reviewed Philippine launch articles do not tie that hardware code to the exact local SKU, so it is retained as a model-level observation and not asserted as a locally confirmed model number."),
    source("redmi_9t_ptg_ph", "PinoyTechGuide Philippines", URL_PTG,
           "Philippine configurations, launch prices, and specification cross-check",
           "Published January 27, 2021. Lists the local 4 GB / 64 GB and 6 GB / 128 GB configurations at PHP 6,990 and PHP 7,990; describes Redmi 9T as launched in the Philippines, with Android 10 / MIUI 12, Snapdragon 662, cameras, battery, connectivity, and other specifications. Its image is an exact-model product photograph, but no image reuse terms were recorded." ,
           "2021-01-27"),
    source("redmi_9t_revu_ph", "REVU Philippines", URL_REVU,
           "Contemporaneous Philippine launch date, local configuration, launch price, and availability",
           "Published January 27, 2021. Reports Xiaomi Philippines' Redmi 9T launch, local 4 GB / 64 GB at PHP 6,990 and 6 GB / 128 GB at PHP 7,990, non-NFC local versions, and availability at official Xiaomi stores and authorized retailers from January 29. A PHP 500 base-model discount was announced for January 29; the article does not give the resulting sale price as a printed amount, so no computed promotional price is recorded.",
           "2021-01-27"),
    source("redmi_9t_noypi_ph", "NoypiGeeks Philippines", URL_NOYPI,
           "Independent Philippine launch-price and exact-model specification cross-check",
           "Published January 27, 2021. Independently reports the same 4 GB / 64 GB and 6 GB / 128 GB launch prices and January 29 availability, and lists the display, chipset, cameras, battery, local connectivity, audio, and build dimensions.",
           "2021-01-27"),
    source("redmi_9t_gadgetpilipinas_ph", "Gadget Pilipinas", URL_GADGET_PILIPINAS,
           "Independent Philippine launch and configuration cross-check",
           "Published January 27, 2021. Confirms the local 4 GB / 64 GB and 6 GB / 128 GB pricing and availability from January 29. One sentence in the article incorrectly labels the 4 GB / 64 GB price configuration as 6 GB / 64 GB; the correctly tabulated configuration and the other launch sources agree on 4 GB / 64 GB, so the prose typo is not adopted.",
           "2021-01-27"),
    source("redmi_9t_qualcomm_662", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 662 platform architecture and capability reference",
           "Qualcomm documents the Snapdragon 662 as an 11 nm mobile platform with Kryo 260 octa-core CPU up to 2 GHz, Adreno 610 GPU, LTE platform, Wi-Fi and Bluetooth capabilities. Platform capabilities are not substituted for handset-specific implementation; device features are taken from Xiaomi and exact-model sources."),
    source("redmi_9t_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-model global release-date cross-check",
           "The exact Redmi 9T page is indexed as released on January 18, 2021. Xiaomi's January 8 global debut announcement is earlier than this release date; the date is global-market context, not Philippine availability."),
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
    config = f"Philippine Redmi 9T, {ram} GB physical RAM / {storage} GB storage"
    rows = [
        field("model_number", "redmi_9t_xiaomi_manual", "Official user guide identifies model M2010J19SG; local SKU mapping was not established", None, status="PENDING_VERIFICATION", note="Preserve the official model-level code in source metadata, but leave the public Philippine model-number field blank until the local SKU-to-code mapping is confirmed.", config_match="Redmi 9T model-level manual; Philippine configuration code not confirmed"),
        field("global_release_date", "redmi_9t_gsmarena", "GSMArena lists the Redmi 9T as released January 18, 2021; Xiaomi announced its global debut on January 8", "2021-01-18", status="VERIFIED_SECONDARY", note="Use the indexed release date, not the earlier announcement/debut date. This does not indicate Philippine sale availability.", config_match="Global model-level release information"),
        field("configuration", "redmi_9t_revu_ph", f"Philippine Redmi 9T: {ram} GB RAM / {storage} GB storage", f"{ram} GB RAM / {storage} GB storage", status="VERIFIED_SECONDARY", note="REVU and NoypiGeeks identify the Philippine 4 GB / 64 GB and 6 GB / 128 GB configurations. The global 4 GB / 128 GB option is not reported as a Philippine launch variant and is not added.", config_match=config),
        field("philippine_release_date", "redmi_9t_revu_ph", "Xiaomi's Philippine launch coverage says official-store and authorized-retailer availability began January 29, 2021", "2021-01-29", status="VERIFIED_SECONDARY", note="Use the reported retail availability date; January 27 is the announcement/publication date, not the sale date.", config_match="Philippine Redmi 9T launch; both documented configurations"),
        field("official_launch_price_php", "redmi_9t_revu_ph", f"Philippine launch price: PHP {launch_price:,} for {ram} GB / {storage} GB", launch_price, status="VERIFIED_SECONDARY", unit="PHP", note="Historical local launch price for this exact configuration. It is not a current price.", config_match=config, price_type="historical_ph_launch_price"),
        field("current_price_php", "redmi_9t_revu_ph", "Reviewed local prices are dated January 2021; no current dated, orderable Philippine offer was verified", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep catalog current price blank. Launch-day PHP 500 discount was reported for the 4 GB / 64 GB model, but no printed resulting sale amount is recorded.", config_match=config, price_type="no_current_offer_verified"),
        field("display_size", "redmi_9t_xiaomi_specs", "6.53-inch display", 6.53, status="VERIFIED", key="displayInches", unit="in", note="Xiaomi's exact-model specification; local launch sources corroborate 6.53 inches.", config_match=config),
        field("display_technology", "redmi_9t_ptg_ph", "IPS LCD", "IPS LCD", status="VERIFIED_SECONDARY", key="displayType", note="PinoyTechGuide identifies IPS LCD; local launch coverage identifies an LCD panel.", config_match=config),
        field("display_resolution", "redmi_9t_xiaomi_specs", "2340 x 1080 pixels (FHD+); PTG lists the same resolution. REVU has a conflicting 2400 x 1080 table entry.", "2340 x 1080", status="VERIFIED", key="resolution", note="The manufacturer and PTG agree at 2340 x 1080. REVU's 2400 x 1080 entry is retained as a source discrepancy and not preferred over Xiaomi's primary specification.", config_match=config),
        field("display_refresh_rate", "redmi_9t_revu_ph", "60 Hz", 60, status="VERIFIED_SECONDARY", key="refreshHz", unit="Hz", note="REVU lists the LCD as 60 Hz; the model is not advertised as a high-refresh-rate panel.", config_match=config),
        field("display_brightness", "redmi_9t_xiaomi_specs", "400 nits typical brightness", 400, status="VERIFIED", unit="nits", note="Xiaomi's exact-model specification identifies typical brightness.", config_match=config),
        field("display_protection", "redmi_9t_ptg_ph", "Corning Gorilla Glass 3", "Corning Gorilla Glass 3", status="VERIFIED_SECONDARY", note="PTG and NoypiGeeks list Gorilla Glass 3; Xiaomi's current global specification page does not name the cover glass.", config_match=config),
        field("chipset", "redmi_9t_xiaomi_specs", "Qualcomm Snapdragon 662", "Qualcomm Snapdragon 662", status="VERIFIED", key="chipset", note="Xiaomi's exact-model page and local launch reporting identify Snapdragon 662.", config_match=config),
        field("process_node", "redmi_9t_qualcomm_662", "11 nm process", 11, status="VERIFIED", unit="nm", note="Qualcomm platform product brief identifies the process node; Xiaomi also lists 11 nm for the Redmi 9T processor.", config_match=config),
        field("cpu", "redmi_9t_qualcomm_662", "Kryo 260 octa-core CPU, up to 2.0 GHz", "Kryo 260 octa-core, up to 2.0 GHz", status="VERIFIED", key="cpu", note="Qualcomm's platform brief gives the official family and maximum frequency; no handset benchmark score is inferred.", config_match=config),
        field("gpu", "redmi_9t_xiaomi_specs", "Qualcomm Adreno 610", "Qualcomm Adreno 610", status="VERIFIED", key="gpu", note="Xiaomi and Qualcomm identify Adreno 610 for the Snapdragon 662 platform.", config_match=config),
        field("operating_system", "redmi_9t_xiaomi_specs", "MIUI 12 based on Android 10 at launch", "MIUI 12 based on Android 10", status="VERIFIED", key="os", note="This is the documented launch software, not a claim about the latest installed update today.", config_match=config),
        field("os_support", "redmi_9t_xiaomi_specs", "No published update duration or end-of-support date was found in the reviewed sources", None, status="NOT_DISCLOSED", note="Keep update policy blank; do not infer support duration from later software versions.", config_match=config),
        field("ram_capacity", "redmi_9t_revu_ph", f"{ram} GB physical RAM", ram, status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="This is the exact Philippine storage/RAM variant; no virtual-memory expansion is added to physical RAM.", config_match=config),
        field("ram_type", "redmi_9t_xiaomi_specs", "LPDDR4X", "LPDDR4X", status="VERIFIED", note="Xiaomi lists LPDDR4X for the documented configuration family, including this RAM/storage combination.", config_match=config),
        field("storage_capacity", "redmi_9t_revu_ph", f"{storage} GB internal storage", storage, status="VERIFIED_SECONDARY", key="storageGb", unit="GB", note="The exact Philippine configuration is separately identified in contemporaneous launch coverage.", config_match=config),
        field("storage_type", "redmi_9t_xiaomi_specs", "UFS 2.1" if storage == 64 else "UFS 2.2", "UFS 2.1" if storage == 64 else "UFS 2.2", status="VERIFIED", key="storageType", note="Xiaomi lists UFS 2.1 for 64 GB and UFS 2.2 for its 128 GB options. The local 6 GB / 128 GB configuration matches the latter; no local 4 GB / 128 GB variant is inferred.", config_match=config),
        field("storage_expansion", "redmi_9t_xiaomi_specs", "Dedicated microSD expansion, up to 512 GB", "Dedicated microSD; up to 512 GB", status="VERIFIED", note="Xiaomi lists dual SIM plus a dedicated microSD slot and up to 512 GB expansion.", config_match=config),
        field("rear_camera_system", "redmi_9t_xiaomi_specs", "48 MP main + 8 MP 120-degree ultra-wide + 2 MP macro + 2 MP depth", "48 MP main + 8 MP ultra-wide + 2 MP macro + 2 MP depth", status="VERIFIED", key="rearCameraMp", unit="MP", note="Complete rear camera set from Xiaomi; catalog numeric value represents the main camera only.", config_match=config, catalog_value=48),
        field("main_camera_sensor", "redmi_9t_xiaomi_specs", "48 MP main camera, 1/2-inch sensor size, f/1.79, PDAF; sensor maker/model not named", "1/2-inch sensor size; maker/model not disclosed", status="VERIFIED", note="Record the published sensor size while leaving the sensor identity unspecified.", config_match=config),
        field("ultrawide_camera", "redmi_9t_xiaomi_specs", "8 MP ultra-wide camera, 120-degree field of view, f/2.2", "8 MP ultra-wide; 120-degree field of view", status="VERIFIED", note="Xiaomi's exact-model camera specification.", config_match=config),
        field("telephoto_camera", "redmi_9t_xiaomi_specs", "The complete listed rear system has main, ultra-wide, macro, and depth cameras; no telephoto camera is listed", "No telephoto camera listed", status="NOT_APPLICABLE", note="Based on Xiaomi's complete four-camera rear specification.", config_match=config),
        field("front_camera", "redmi_9t_xiaomi_specs", "8 MP front camera, f/2.05", 8, status="VERIFIED", key="frontCameraMp", unit="MP", note="Xiaomi's exact-model specification; local launch sources corroborate 8 MP.", config_match=config),
        field("video_recording", "redmi_9t_xiaomi_specs", "Rear and front video: 1080p at 30 fps and 720p at 30 fps; time-lapse also listed", "Front/rear 1080p30 and 720p30; time-lapse", status="VERIFIED", key="video", note="Record only modes listed on the product page; chipset video capability is not substituted.", config_match=config),
        field("battery_capacity", "redmi_9t_xiaomi_specs", "6000 mAh typical", 6000, status="VERIFIED", key="batteryMah", unit="mAh", note="Xiaomi's exact-model battery rating; local sources corroborate 6,000 mAh.", config_match=config),
        field("battery_technology", "redmi_9t_ptg_ph", "Li-Po, non-removable", "Li-Po; non-removable", status="VERIFIED_SECONDARY", note="PTG lists battery chemistry and non-removable construction; manufacturer page confirms capacity but not chemistry.", config_match=config),
        field("wired_charging", "redmi_9t_xiaomi_specs", "18 W wired charging; 22.5 W charger supplied in box", 18, status="VERIFIED", key="chargingW", unit="W", note="The phone's charging rate is 18 W; the included 22.5 W adapter rating is not reported as the phone's input rate.", config_match=config),
        field("wireless_charging", "redmi_9t_xiaomi_specs", "Wireless charging is not specified in the reviewed product page", None, status="NOT_DISCLOSED", note="Do not convert omission into a confirmed lack of support.", config_match=config),
        field("dimensions", "redmi_9t_xiaomi_specs", "162.3 x 77.3 x 9.6 mm", "162.3 x 77.3 x 9.6 mm", status="VERIFIED", key="dimensions", unit="mm", note="Xiaomi exact-model dimensions; NoypiGeeks reports the same values.", config_match=config),
        field("weight", "redmi_9t_xiaomi_specs", "198 g", 198, status="VERIFIED", key="weightG", unit="g", note="Xiaomi exact-model figure; NoypiGeeks reports the same weight.", config_match=config),
        field("materials", "redmi_9t_ptg_ph", "Plastic body", "Plastic body", status="VERIFIED_SECONDARY", note="PTG lists plastic build materials; no more detailed frame/back composition is asserted.", config_match=config),
        field("ingress_protection", "redmi_9t_noypi_ph", "No IP certification or formal ingress-protection rating was identified; local coverage mentions water-repellent/splash-resistant coating", None, status="NOT_DISCLOSED", note="A water-repellent design claim is not an IP rating. Keep the IP field blank.", config_match=config),
        field("sim_esim", "redmi_9t_xiaomi_specs", "Dual SIM with dedicated microSD tray; eSIM support is not stated", "Dual SIM; dedicated microSD; eSIM not recorded", status="VERIFIED", key="sim", note="Xiaomi confirms the dual-SIM and dedicated microSD arrangement. No eSIM claim is inferred.", config_match=config),
        field("cellular_bands", "redmi_9t_xiaomi_specs", "Global specification lists GSM B2/3/5/8; WCDMA B1/2/4/5/8; LTE FDD B1/2/3/4/5/7/8/20/28 and TDD B38/40/41. Philippine SKU band mapping was not separately published.", "Global Redmi 9T bands: GSM B2/3/5/8; WCDMA B1/2/4/5/8; LTE FDD B1/2/3/4/5/7/8/20/28; TDD B38/40/41", status="VERIFIED", key="cellular", note="This is the Xiaomi global model specification, not a carrier-compatibility guarantee for every Philippine SKU.", config_match="Global Redmi 9T model-level radio specification; local SKU band mapping not separately confirmed"),
        field("wifi", "redmi_9t_xiaomi_specs", "Dual-band 2.4 / 5 GHz Wi-Fi 802.11 a/b/g/n/ac", "Dual-band Wi-Fi 802.11 a/b/g/n/ac", status="VERIFIED", key="wifi", note="Xiaomi lists both frequency bands and supported protocols.", config_match=config),
        field("bluetooth", "redmi_9t_xiaomi_specs", "Bluetooth 5.0", "Bluetooth 5.0", status="VERIFIED", note="Xiaomi exact-model specification.", config_match=config),
        field("usb", "redmi_9t_xiaomi_specs", "USB Type-C; data-transfer generation not stated", "USB Type-C", status="VERIFIED", key="ports", note="Connector type is recorded; no USB data speed is inferred.", config_match=config),
        field("nfc", "redmi_9t_revu_ph", "Local launch coverage says only non-NFC variants would be sold in the Philippines; PTG lists NFC: No", False, status="VERIFIED_SECONDARY", note="Local-market-specific evidence is used because Xiaomi says NFC availability varies by market.", config_match="Philippine Redmi 9T variants; local launch sources report non-NFC models"),
        field("gnss", "redmi_9t_xiaomi_specs", "GPS/A-GPS, GLONASS, BeiDou, Galileo", "GPS/A-GPS, GLONASS, BeiDou, Galileo", status="VERIFIED", key="gnss", note="Xiaomi's exact-model navigation specification.", config_match=config),
        field("audio", "redmi_9t_xiaomi_specs", "Dual speakers, 3.5 mm headphone jack, Hi-Res Audio", "Dual speakers; 3.5 mm jack; Hi-Res Audio", status="VERIFIED", key="sound", note="Xiaomi's exact-model audio specification; NoypiGeeks also lists stereo speakers and a headphone jack.", config_match=config),
        field("sensors", "redmi_9t_xiaomi_specs", "Proximity, ambient light, accelerometer, electronic compass, vibration motor, IR blaster; side fingerprint sensor", "Proximity, ambient light, accelerometer, compass, vibration motor, IR blaster, side fingerprint", status="VERIFIED", note="Xiaomi lists the sensors and side fingerprint reader; keep the IR blaster as a model feature, not a separate sensor rating.", config_match=config),
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
        "availabilityStatus": "Contemporaneous Philippine launch reporting documents Xiaomi official-store and authorized-retailer availability from January 29, 2021. Workbook eligibility remains Pending.",
        "philippineAvailability": "Xiaomi Philippines launch coverage published January 27, 2021 states that the Redmi 9T would be sold by official Xiaomi online stores, authorized Mi Stores, and resellers from January 29. Two local configurations were listed: 4 GB / 64 GB at PHP 6,990 and 6 GB / 128 GB at PHP 7,990. This verifies reported local market availability, not current stock or orderability.",
        "observedAt": OBSERVED,
        "manufacturer": "Xiaomi Corporation",
        "catalogModel": "Redmi 9T",
        "productLine": "Redmi 9 series",
        "modelNumber": None,
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Reported Philippine retail availability date",
        "researchNotes": "Workbook row 47 'Redmi 9T' is matched to Xiaomi's Redmi 9T on the basis of exact-model Philippine launch coverage. Local sources agree on 4 GB / 64 GB and 6 GB / 128 GB variants; global 4 GB / 128 GB is not added as a local configuration. Official model guide lists M2010J19SG, but the reviewed Philippine sources do not map that code to the local SKU, so the catalog model-number field stays blank. January 2021 launch prices are historical; current price and image reuse rights are unverified. Workbook eligibility remains Pending.",
        "qualityFlag": "Philippine Redmi 9T launch and two local variants verified; hardware-code mapping, current price, and image reuse rights unresolved; workbook eligibility remains Pending.",
        "openIssues": [
            {"issue": "The official user guide gives hardware code M2010J19SG, but no reviewed Philippine launch source ties it to the exact local SKU", "action": "Leave the public model-number field blank pending local code confirmation."},
            {"issue": "Only January 2021 launch prices were verified; retailer links do not establish a current orderable offer", "action": "Keep current price blank and preserve the two launch MSRPs as historical price observations."},
            {"issue": "A January 29 PHP 500 discount is reported for the base variant, but the reviewed article does not print the resulting sale amount", "action": "Record the discount note only; do not calculate or publish a sale price."},
            {"issue": "Exact product photographs appear on Xiaomi and PTG pages without recorded reuse permission", "action": "Use the neutral image placeholder until image usage rights are established."},
            {"issue": "A source has a prose typo calling the 4 GB / 64 GB launch option 6 GB / 64 GB", "action": "Use the matching price table and multiple agreeing local launch reports; preserve the typo in source notes."},
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
            or device.get("model", "").casefold() != "9t"):
        raise ValueError("Inventory row no longer matches Redmi 9T")
    variant_ids = {variant.get("id") for variant in device.get("variants", [])}
    if variant_ids - {OLD_CONFIG, CONFIG_4_64, CONFIG_6_128}:
        raise ValueError(f"Unexpected Redmi 9T configurations: {sorted(variant_ids)}")

    variants = [
        {"id": CONFIG_4_64, "label": "4 GB RAM / 64 GB storage", "sku": None,
         "modelCode": None,
         "notes": "Philippine launch sources identify this as the base non-NFC configuration. Reported local colors include Carbon Gray, Twilight Blue, Ocean Green, and an orange color variously named Sunrise Orange / Sunset Orange; no color-to-storage mapping is documented.",
         "workbookRow": 47},
        {"id": CONFIG_6_128, "label": "6 GB RAM / 128 GB storage", "sku": None,
         "modelCode": None,
         "notes": "Philippine launch sources identify this as the higher-memory non-NFC configuration. Reported local colors include Carbon Gray, Twilight Blue, Ocean Green, and an orange color variously named Sunrise Orange / Sunset Orange; no color-to-storage mapping is documented.",
         "workbookRow": 47},
    ]
    records = []
    for index, (variant, ram, storage, price) in enumerate((
            (variants[0], 4, 64, 6990), (variants[1], 6, 128, 7990))):
        records.append({
            "deviceId": DEVICE,
            "configurationId": variant["id"],
            "brand": "Redmi",
            "model": "Redmi 9T",
            "configuration": variant["label"],
            "configurationLabel": variant["label"],
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
        "reason": "Exact Redmi 9T product photographs are present on Xiaomi's specification page and PinoyTechGuide, but no reusable image license or permission to copy/embed is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_XIAOMI,
        "assetUrl": None,
        "scope": "Redmi 9T; Philippine 4 GB / 64 GB and 6 GB / 128 GB variants",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Xiaomi Redmi 9T",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for variant, ram, storage, amount in (
            (variants[0], 4, 64, 6990), (variants[1], 6, 128, 7990)):
        prices.append({
            "device_id": DEVICE, "amount_php": amount, "configuration_id": variant["id"],
            "configuration_match": f"exact_philippine_{ram}gb_{storage}gb_configuration",
            "variant_ram_gb": ram, "variant_storage_gb": storage,
            "price_type": "historical_ph_launch_price", "source_published_at": "2021-01-27",
            "excerpt": f"Philippine Redmi 9T launch coverage lists PHP {amount:,} for the {ram} GB / {storage} GB configuration; reported availability began January 29, 2021.",
            "source_url": URL_REVU, "source_kind": "historical_local_launch_price",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
            "availability_status": "historical_launch_price_not_current",
        })
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Redmi", "model_name": "Redmi 9T", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_REVU, "result": "Philippine launch coverage lists 4 GB / 64 GB at PHP 6,990 and 6 GB / 128 GB at PHP 7,990; availability from January 29, 2021. A PHP 500 base-variant discount was announced for January 29, but the resulting price was not printed and is not calculated."},
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "PinoyTechGuide independently lists the same two Philippine configurations and launch MSRPs; its exact-model photograph has no recorded reuse license."},
            {"device_id": DEVICE, "source_url": URL_XIAOMI, "result": "Xiaomi global specs support 4 GB / 64 GB UFS 2.1 and 6 GB / 128 GB UFS 2.2. A separate 4 GB / 128 GB global configuration exists but is not added to the Philippine catalog because no local launch source lists it."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 47 Redmi 9T -> Philippine Xiaomi Redmi 9T",
        "configurations": [{"label": item["label"], "historicalLaunchPricePhp": price}
                           for item, price in zip(variants, (6990, 7990))],
        "reviewedFields": sum(len(item["fields"]) for item in records),
        "philippineAvailabilityDate": "2021-01-29",
        "currentPrices": "blank; no current orderable offer verified",
        "image": "neutral placeholder; reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
