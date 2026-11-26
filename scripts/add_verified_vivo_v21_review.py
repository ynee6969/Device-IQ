#!/usr/bin/env python3
"""Record source-backed Philippine research for vivo V21 5G (V2050)."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/vivo-v21-5g-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_09d07effbd7687"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-8gb-128gb-ph"

URL_VIVO_STORE = "https://shop.vivo.com/ph/product/2022?skuId=8046"
URL_VIVO_LAUNCH = "https://www.vivoglobal.ph/vivo-launches-v21-series-phone/"
URL_VIVO_PREORDER = "https://www.vivoglobal.ph/pre-order-vivo-v21-series-get-premium-freebies/"
URL_VIVO_PRICE_DROP = "https://www.vivoglobal.ph/vivo-v21-price-drops-equip-influencer-in-you/"
URL_YUGA = "https://www.yugatech.com/mobile/vivo-v21-5g-v21e-4g-specs-price-philippines/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/vivo-v21-5g"
URL_NTC = "https://region4b.ntc.gov.ph/wp-content/uploads/2022/01/GEC_12312021.pdf"
URL_GSMARENA = "https://www.gsmarena.com/vivo_v21_5g-10879.php"
URL_GSMARENA_REVIEW = "https://www.gsmarena.com/vivo_v21_5g-review-2273.php"
URL_GSMARENA_RELEASE = "https://www.gsmarena.com/vivo_v21_5g_india_price_sale_date-news-48891.php"
URL_MEDIATEK = "https://i.mediatek.com/dimensity-800u"
URL_NANOREVIEW = "https://nanoreview.net/en/soc/mediatek-dimensity-800u"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("vivo_v21_ph_store", "vivo Philippines Official Store", URL_VIVO_STORE,
           "Primary local product page, configuration, specification, and price-page review",
           "The Philippine store page identifies V21 5G Dusk Blue 8 GB / 128 GB, the second color, full product specifications, and a displayed PHP 23,999 amount. The page did not expose a current stock or checkout state in the reviewed content, so that displayed amount is not treated as a verified current offer. It also lists 2404 x 1080 resolution and 7.39 mm / 177 g, which conflict with other model-level published values and are retained for review."),
    source("vivo_v21_ph_launch", "vivo Philippines", URL_VIVO_LAUNCH,
           "Primary Philippine launch date and launch feature evidence",
           "Published May 27, 2021. vivo states pre-orders ran June 1-4 and the final product release date was June 5. It describes the Philippine V21 5G separately from V21e 4G and documents the 44 MP front OIS, 64 MP main camera, 90 Hz display, colors, and launch design.",
           "2021-05-27"),
    source("vivo_v21_ph_preorder", "vivo Philippines", URL_VIVO_PREORDER,
           "Primary Philippine MSRP and authorized local availability",
           "Published May 31, 2021. vivo reports V21 5G pre-orders June 1-4, an official SRP of PHP 23,999, and retail availability beginning June 5 through vivo stores and official online stores.",
           "2021-05-31"),
    source("vivo_v21_ph_price_reduction", "vivo Philippines", URL_VIVO_PRICE_DROP,
           "Dated historical Philippine price change",
           "Published August 3, 2021. vivo states the V21 5G price decreased from PHP 23,999 to PHP 21,999 at its kiosks and stores. This is a dated historical promotion/price change, not a current offer.",
           "2021-08-03"),
    source("vivo_v21_yugatech", "YugaTech Philippines", URL_YUGA,
           "Independent Philippine launch and configuration cross-check",
           "Published May 31, 2021. Distinguishes V21 5G from V21e 4G; lists 8 GB + 3 GB extended RAM, 128 GB storage, hybrid microSD slot, processor, camera set, software, charging, connectivity, and June 5 local availability. It reports color-dependent ranges for thickness and weight."),
    source("vivo_v21_ptg", "PinoyTechGuide", URL_PTG,
           "Philippine device-specific specification cross-check",
           "Published May 31, 2021. Lists V21 5G specifications and its PHP 23,999 official launch price. Its page states 256 GB storage, while vivo Philippines' exact local 8 GB / 128 GB store SKU and YugaTech's launch report say 128 GB; the manufacturer's exact local configuration is retained and the PTG storage discrepancy is not promoted."),
    source("vivo_v21_ntc_gec", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and exact model-code match",
           "The NTC GEC register maps vivo V2050 to marketing name V21 5G, applicant vivo Mobile Tech Inc., issued April 29, 2021. The record distinguishes this from the V21e (V2061)."),
    source("vivo_v21_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-model global release and technical cross-check",
           "The exact V21 5G listing records release on May 6, 2021. Its specification set covers multiple regional storage/RAM variants; it is used only for model-level characteristics and not to add non-Philippine configurations."),
    source("vivo_v21_gsmarena_review", "GSMArena", URL_GSMARENA_REVIEW,
           "Exact-model independent technical review",
           "The review identifies V21 5G and provides panel brightness, processor, storage interface, and global build observations. The review's build-material description conflicts with vivo's local 'matte glass' design wording, so no single body-material claim is promoted."),
    source("vivo_v21_gsmarena_release", "GSMArena", URL_GSMARENA_RELEASE,
           "Contemporaneous global-market release context",
           "GSMArena reports the V21 5G sale date in India as May 6, 2021, supporting the earliest reviewed global market release date, not a simultaneous worldwide launch."),
    source("vivo_v21_mediatek_800u", "MediaTek", URL_MEDIATEK,
           "Primary chipset CPU, GPU, and manufacturing-process reference",
           "MediaTek specifies a 7 nm Dimensity 800U, 2 Cortex-A76 cores up to 2.4 GHz, 6 Cortex-A55 cores up to 2 GHz, and Mali-G57 MC3 GPU. Chipset-level memory, storage, and connectivity capabilities are not substituted for device-specific implementation."),
    source("vivo_v21_nanoreview_800u", "NanoReview", URL_NANOREVIEW,
           "Independent chipset architecture cross-check",
           "NanoReview independently lists the Dimensity 800U at 7 nm with two Cortex-A76 and six Cortex-A55 cores and Mali-G57 MP3-class graphics. It is used only as a chipset-level cross-check; scores are not presented as handset measurements."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, catalog_value=None,
          price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note,
            "configurationMatch": "Exact Philippine vivo V21 5G / V2050, 8 GB physical RAM / 128 GB storage unless a model-level chipset or GSMArena specification is noted"}
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
        field("model_number", "vivo_v21_ntc_gec", "NTC maps model V2050 to vivo V21 5G", "V2050", status="VERIFIED", note="Exact model-code/marketing-name match in the Philippine NTC GEC register; V21e is separately registered as V2061."),
        field("global_release_date", "vivo_v21_gsmarena", "GSMArena lists release on May 6, 2021; its report identifies India sale beginning that day", "2021-05-06", note="Earliest reviewed market release date; does not imply a worldwide simultaneous release or Philippine availability."),
        field("configuration", "vivo_v21_ph_store", "V21 5G 8 GB + 128 GB (5G); 3 GB Extended RAM is software-managed expansion", "8 GB physical RAM / 128 GB storage", status="VERIFIED", note="The exact Philippine official-store SKU and YugaTech identify 8 GB / 128 GB. The additional 3 GB is extended/virtual RAM, not a separate physical memory configuration. No 256 GB local variant is added."),
        field("philippine_release_date", "vivo_v21_ph_launch", "vivo says final product release date in the Philippines was June 5, 2021", "2021-06-05", status="VERIFIED", note="Manufacturer's Philippine launch announcement gives June 5 as product release after June 1-4 pre-orders; this is not an exact first transaction time."),
        field("official_launch_price_php", "vivo_v21_ph_preorder", "Official Philippine SRP PHP 23,999 for V21 5G 8 GB / 128 GB", 23999, status="VERIFIED", unit="PHP", note="Manufacturer's Philippine preorder announcement states the SRP; record as launch-era price only.", price_type="historical_ph_launch_price"),
        field("current_price_php", "vivo_v21_ph_store", "Official store page displays PHP 23,999 but does not expose a current orderable/stock state; the page path is a 2022 product listing", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep the current live price blank until an active, dated, purchasable offer is verified. The August 2021 PHP 21,999 reduction and launch SRP are historical observations.", price_type="current_offer_orderability_unverified"),
        field("display_size", "vivo_v21_ph_store", "6.44-inch display", 6.44, status="VERIFIED", key="displayInches", unit="in", note="Official Philippine store and local launch coverage agree on 6.44 inches."),
        field("display_technology", "vivo_v21_ph_store", "AMOLED", "AMOLED", status="VERIFIED", key="displayType", note="Official Philippine product specification."),
        field("display_resolution", "vivo_v21_ph_store", "Official store specifies 2404 x 1080; YugaTech, PTG, and GSMArena list 2400 x 1080", None, status="CONFLICTING_INFORMATION", key="resolution", note="Published model specifications differ by four vertical pixels. Leave the catalog resolution blank until the official spec discrepancy is resolved."),
        field("display_refresh_rate", "vivo_v21_ph_launch", "90 Hz display refresh rate", 90, status="VERIFIED", key="refreshHz", unit="Hz", note="vivo Philippines launch communication and YugaTech identify the 90 Hz panel."),
        field("display_brightness", "vivo_v21_gsmarena_review", "GSMArena lists 500 nits typical and independently measured 467 nits in its test", 500, status="VERIFIED_SECONDARY", unit="nits", note="The 500-nit typical rating is a model-level published figure; GSMArena's 467-nit lab reading is its own review measurement and is not substituted for the typical specification."),
        field("display_protection", "vivo_v21_ph_launch", "Local manufacturer says the matte-glass design is scratch-resistant but gives no named front-glass protection rating", None, status="NOT_DISCLOSED", note="A scratch-resistance statement is not converted into a Gorilla Glass or other protection rating."),
        field("chipset", "vivo_v21_ph_store", "MediaTek Dimensity 800U", "MediaTek Dimensity 800U", status="VERIFIED", key="chipset", note="Official Philippine store and vivo Philippines launch materials identify this chipset."),
        field("process_node", "vivo_v21_mediatek_800u", "MediaTek specifies the Dimensity 800U as a 7 nm SoC", 7, unit="nm", note="Chipset-level process node, not a separate handset measurement."),
        field("cpu", "vivo_v21_mediatek_800u", "2x Cortex-A76 up to 2.4 GHz + 6x Cortex-A55 up to 2.0 GHz", "2x Cortex-A76 2.4 GHz + 6x Cortex-A55 2.0 GHz", status="VERIFIED", key="cpu", note="MediaTek's official chipset architecture page."),
        field("gpu", "vivo_v21_mediatek_800u", "Arm Mali-G57 MC3", "Arm Mali-G57 MC3", status="VERIFIED", key="gpu", note="MediaTek's official specification; local YugaTech and PTG coverage also names Mali-G57 MC3."),
        field("operating_system", "vivo_v21_yugatech", "Android 11 with Funtouch OS 11.1", "Funtouch OS 11.1 based on Android 11", status="VERIFIED_SECONDARY", key="os", note="YugaTech identifies the Philippine launch software; vivo's local store lists Funtouch OS 11.1."),
        field("os_support", "vivo_v21_ph_store", "No OS upgrade or security-support policy found in reviewed manufacturer pages", None, status="NOT_DISCLOSED", note="No update count, end date, or support duration is inferred."),
        field("ram_capacity", "vivo_v21_ph_store", "8 GB physical RAM plus 3 GB Extended RAM", 8, status="VERIFIED", key="ramGb", unit="GB", note="Catalog RAM records the installed physical capacity; the 3 GB extended-memory feature is not added to that number."),
        field("ram_type", "vivo_v21_ph_store", "Manufacturer confirms 8 GB but does not state the installed memory type for the Philippine SKU", None, status="NOT_DISCLOSED", note="Dimensity 800U LPDDR4x support alone does not prove the installed RAM type."),
        field("storage_capacity", "vivo_v21_ph_store", "8 GB / 128 GB (5G) exact Philippine official-store SKU", 128, status="VERIFIED", key="storageGb", unit="GB", note="Official store and YugaTech document the local 128 GB configuration. PTG's page lists 256 GB, which conflicts with the exact local manufacturer SKU and is not promoted."),
        field("storage_type", "vivo_v21_gsmarena_review", "GSMArena identifies UFS 2.2 for V21 5G storage; the exact local store page does not identify the interface", "UFS 2.2", status="VERIFIED_SECONDARY", key="storageType", note="Exact-model global listing reports UFS 2.2 across its memory configurations. This interface is not separately stated on the Philippine store page."),
        field("storage_expansion", "vivo_v21_ph_store", "Hybrid slot: 1 Nano-SIM + 1 Nano-SIM or 1 microSD; maximum microSD capacity not stated", "Hybrid microSD slot; maximum capacity not recorded", status="VERIFIED", note="Official Philippine store specifies the hybrid slot. No maximum card capacity is inferred."),
        field("rear_camera_system", "vivo_v21_ph_store", "64 MP OIS AF main + 8 MP wide-angle + 2 MP macro, with rear flash", "64 MP OIS main + 8 MP ultra-wide + 2 MP macro", status="VERIFIED", key="rearCameraMp", unit="MP", note="Official local store and YugaTech identify the same three-module arrangement; catalog numeric value represents the main camera only.", catalog_value=64),
        field("main_camera_sensor", "vivo_v21_ph_store", "No main sensor manufacturer or sensor model identified in reviewed local product specifications", None, status="NOT_DISCLOSED", note="The 64 MP resolution and OIS do not identify the sensor model."),
        field("ultrawide_camera", "vivo_v21_ph_store", "8 MP wide-angle rear camera", "8 MP ultra-wide camera", status="VERIFIED", note="The local manufacturer store and local launch spec identify an 8 MP wide-angle module."),
        field("telephoto_camera", "vivo_v21_ph_store", "The complete three-camera rear specification is 64 MP main, 8 MP wide-angle, and 2 MP macro; no telephoto module listed", "No telephoto camera listed", status="NOT_APPLICABLE", note="No telephoto lens appears in the complete official rear-camera specification."),
        field("front_camera", "vivo_v21_ph_store", "44 MP front autofocus camera with OIS", 44, status="VERIFIED", key="frontCameraMp", unit="MP", note="Official Philippine store specification; local launch sources corroborate the 44 MP OIS front camera."),
        field("video_recording", "vivo_v21_ph_store", "Front and rear cameras support 4K video; Dual-View Video is listed; frame rate is not stated", "Front/rear 4K video; Dual-View Video; frame rate not recorded", status="VERIFIED", key="video", note="Record only the local store's named capabilities; do not infer a 30 fps rate from chipset support."),
        field("battery_capacity", "vivo_v21_ph_store", "4,000 mAh battery", 4000, status="VERIFIED", key="batteryMah", unit="mAh", note="Official Philippine product page states the capacity; local sources corroborate it."),
        field("battery_technology", "vivo_v21_ptg", "Li-Po battery, non-removable", "Li-Po; non-removable", status="VERIFIED_SECONDARY", note="PinoyTechGuide reports chemistry and non-removable construction for the exact V21 5G model; official local store confirms capacity but omits chemistry."),
        field("wired_charging", "vivo_v21_ph_store", "33 W (11 V / 3 A) FlashCharge", 33, status="VERIFIED", key="chargingW", unit="W", note="Official Philippine store specification."),
        field("wireless_charging", "vivo_v21_ph_store", "Wireless and reverse wireless charging are not listed in the reviewed Philippine specification", None, status="NOT_DISCLOSED", note="No wireless charging absence is inferred from omission."),
        field("dimensions", "vivo_v21_yugatech", "Published thickness values range from 7.29 to 7.39 mm; official local store lists 159.68 x 73.90 x 7.39 mm for its Dusk Blue listing while vivo launch material says 7.29 mm", None, status="CONFLICTING_INFORMATION", key="dimensions", unit="mm", note="The manufacturer and local source pages do not consistently map color to thickness. Keep scalar dimensions blank pending resolution."),
        field("weight", "vivo_v21_yugatech", "Published weight values range from 176 to 177 g; local launch material says 176 g and official store listing says 177 g", None, status="CONFLICTING_INFORMATION", key="weightG", unit="g", note="Conflicting official/local values may be color-dependent, but the exact color mapping is inconsistent. Keep a single numeric catalog weight blank."),
        field("materials", "vivo_v21_ph_launch", "vivo Philippines describes anti-glare matte glass; GSMArena describes glass front with plastic back and frame", None, status="CONFLICTING_INFORMATION", note="The descriptions conflict on back/frame material. Do not promote one composition into the catalog."),
        field("ingress_protection", "vivo_v21_ph_store", "No IP rating recorded in the reviewed Philippine specification", None, status="NOT_DISCLOSED", note="No water/dust rating is inferred."),
        field("sim_esim", "vivo_v21_ph_store", "Two Nano-SIMs, with the second slot shared with microSD; eSIM is not stated", "Dual Nano-SIM; second slot shared with microSD; eSIM not recorded", status="VERIFIED", key="sim", note="Official Philippine store specifies two Nano-SIM positions and the hybrid second slot. No eSIM status is inferred."),
        field("cellular_bands", "vivo_v21_ph_store", "5G supported (5G bands not listed); GSM B2/B3/B5/B8; WCDMA B1/B2/B4/B5/B8; LTE FDD B1/B2/B3/B4/B5/B7/B8/B20/B28; LTE TDD B38/B39/B40/B41F", "5G supported (bands not listed); GSM B2/B3/B5/B8; WCDMA B1/B2/B4/B5/B8; LTE FDD B1/B2/B3/B4/B5/B7/B8/B20/B28; LTE TDD B38/B39/B40/B41F", status="VERIFIED", key="cellular", note="Use the Philippine manufacturer store's published radio bands. The exact 5G bands are not disclosed on that page."),
        field("wifi", "vivo_v21_yugatech", "Dual-band Wi-Fi; local launch reporting gives Wi-Fi support but not protocol, with the matching model listing 802.11 a/b/g/n/ac", "Dual-band Wi-Fi 802.11 a/b/g/n/ac", status="VERIFIED_SECONDARY", key="wifi", note="YugaTech identifies the Philippine model; GSMArena exact-model reference supports 802.11 a/b/g/n/ac. The Philippine manufacturer store confirms 2.4 and 5 GHz operation."),
        field("bluetooth", "vivo_v21_ph_store", "Bluetooth 5.1", "Bluetooth 5.1", status="VERIFIED", note="Official Philippine store specification."),
        field("usb", "vivo_v21_ph_store", "USB Type-C; OTG supported", "USB Type-C; OTG", status="VERIFIED", key="ports", note="Official Philippine store specification; data-generation speed is not stated."),
        field("nfc", "vivo_v21_ph_store", "NFC not supported", False, status="VERIFIED", note="Official Philippine store explicitly lists NFC as not supported."),
        field("gnss", "vivo_v21_ph_store", "GPS, BeiDou, Galileo, GLONASS", "GPS, BeiDou, Galileo, GLONASS", status="VERIFIED", key="gnss", note="Official Philippine store's location technology list."),
        field("audio", "vivo_v21_ph_store", "Hi-Fi not supported; store box includes an earphone-jack adapter; a built-in 3.5 mm jack and speaker layout are not specified", "Audio playback; adapter in box; jack/speaker details not recorded", status="VERIFIED_SECONDARY", key="sound", note="Store documentation lists audio playback support and an earphone-jack adapter. Do not infer a built-in 3.5 mm jack or stereo speaker count."),
        field("sensors", "vivo_v21_ph_store", "In-display fingerprint, accelerometer, proximity, ambient-light sensor, e-compass, gyroscope", "In-display fingerprint, accelerometer, proximity, ambient light, e-compass, gyroscope", status="VERIFIED", note="Official Philippine store enumerates these sensors."),
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
        "availabilityStatus": "vivo Philippines identifies the local model as V21 5G, announces June 5, 2021 local release, and registers model V2050 with the NTC. Workbook eligibility remains Pending.",
        "philippineAvailability": "vivo Philippines announced the V21 5G for June 5, 2021 retail release after June 1-4 pre-orders. The official local store identifies the 8 GB / 128 GB product and NTC maps V2050 to V21 5G. This is a manufacturer-reported local release date, not an exact first transaction timestamp.",
        "observedAt": OBSERVED,
        "manufacturer": "vivo",
        "catalogModel": "V21 5G",
        "productLine": "vivo V21 series",
        "modelNumber": "V2050",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Philippine product release date",
        "researchNotes": "Workbook row 44 'vivo V21' matched to the Philippine V21 5G / NTC code V2050, distinct from V21e / V2061. The manufacturer store and YugaTech document the local 8 GB physical RAM / 128 GB storage configuration; the additional 3 GB is virtual/extended RAM. Official May 31 SRP was PHP 23,999 and vivo announced a dated reduction to PHP 21,999 on August 3, 2021. The store's displayed price has no confirmed live stock/checkout state, so current price remains blank. Display resolution and body dimensions/weight/material descriptions have published discrepancies and remain visibly unresolved. Workbook eligibility remains Pending.",
        "qualityFlag": "Philippine V21 5G / V2050 availability and 8 GB / 128 GB configuration verified; current offer not verified; resolution and body details retain source discrepancies; image reuse rights not established.",
        "openIssues": [
            {"issue": "Official store page shows PHP 23,999 but does not establish current stock or checkout availability", "action": "Keep the live price blank; preserve PHP 23,999 and PHP 21,999 as dated historical price records."},
            {"issue": "The official store lists 2404 x 1080 while local and global references list 2400 x 1080", "action": "Leave catalog resolution blank until the published specification conflict is resolved."},
            {"issue": "Thickness and weight vary in published sources; store Dusk Blue values do not align with the local marketing values", "action": "Leave scalar dimensions and weight blank; preserve both source claims in the field audit."},
            {"issue": "Manufacturer describes matte glass while GSMArena describes a plastic back/frame", "action": "Leave body-material field unresolved."},
            {"issue": "PTG lists 256 GB storage while the exact local official-store SKU and YugaTech report 128 GB", "action": "Keep only the manufacturer-confirmed local 8 GB / 128 GB configuration."},
            {"issue": "Official product imagery is exact but reuse rights are not published in the reviewed page", "action": "Use the neutral unavailable-image placeholder until reuse permission is established."},
            {"issue": "Workbook eligibility status remains Pending", "action": "Preserve Pending and apply existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "vivo"
            or device.get("model", "").casefold() != "v21"):
        raise ValueError("Inventory row no longer matches vivo V21")
    current_ids = {variant.get("id") for variant in device.get("variants", [])}
    if current_ids - {OLD_CONFIG, CONFIG}:
        raise ValueError(f"Unexpected V21 configurations: {sorted(current_ids)}")

    variant = {
        "id": CONFIG,
        "label": "8 GB RAM / 128 GB storage (V21 5G)",
        "sku": None,
        "modelCode": "V2050",
        "notes": "Philippine manufacturer store and YugaTech report 8 GB physical RAM / 128 GB storage; vivo's 3 GB Extended RAM is virtual memory. Colors Dusk Blue and Sunset Dazzle are listed, but no separate storage configuration is documented locally. Do not merge V21e 4G / V2061.",
        "workbookRow": 44,
    }
    record = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "vivo",
        "model": "V21 5G",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "modelCode": "V2050",
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
        "reason": "vivo's Philippine store page displays exact V21 5G product images, but no reusable image license or permission to copy/embed was recorded. Keep the neutral placeholder.",
        "sourcePage": URL_VIVO_STORE,
        "assetUrl": None,
        "scope": "vivo V21 5G / Philippine V2050, 8 GB RAM / 128 GB storage",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for vivo V21 5G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "vivo", "model_name": "V21 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_VIVO_PREORDER, "result": "vivo Philippines set the official local V21 5G 8 GB / 128 GB SRP at PHP 23,999 and announced store availability from June 5, 2021."},
            {"device_id": DEVICE, "source_url": URL_VIVO_PRICE_DROP, "result": "vivo Philippines documented the dated August 3, 2021 price reduction from PHP 23,999 to PHP 21,999; historical only."},
            {"device_id": DEVICE, "source_url": URL_VIVO_STORE, "result": "Official store page displays PHP 23,999 for 8 GB / 128 GB, but the page does not expose a current stock or checkout status; not promoted as a live price."},
        ],
        "prices": [
            {
                "device_id": DEVICE, "amount_php": 23999,
                "configuration_id": CONFIG,
                "configuration_match": "exact_philippine_8gb_128gb_configuration",
                "variant_ram_gb": 8, "variant_storage_gb": 128,
                "price_type": "historical_ph_launch_price",
                "source_published_at": "2021-05-31",
                "excerpt": "vivo Philippines announced a Philippine SRP of PHP 23,999 for the V21 5G, with pre-orders June 1-4 and store availability from June 5.",
                "source_url": URL_VIVO_PREORDER,
                "source_kind": "manufacturer_historical_local_price",
                "observed_at": OBSERVED_AT,
                "local_availability_verified": True,
                "availability_status": "historical_launch_price_not_current",
            },
            {
                "device_id": DEVICE, "amount_php": 21999,
                "configuration_id": CONFIG,
                "configuration_match": "exact_philippine_8gb_128gb_configuration",
                "variant_ram_gb": 8, "variant_storage_gb": 128,
                "price_type": "historical_ph_price_reduction",
                "source_published_at": "2021-08-03",
                "excerpt": "vivo Philippines announced the V21 5G price reduction from PHP 23,999 to PHP 21,999 on August 3, 2021.",
                "source_url": URL_VIVO_PRICE_DROP,
                "source_kind": "manufacturer_historical_local_price",
                "observed_at": OBSERVED_AT,
                "local_availability_verified": True,
                "availability_status": "historical_price_change_not_current",
            },
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 44 vivo V21 -> Philippine V21 5G / NTC V2050",
        "configuration": variant["label"],
        "reviewedFields": len(record["fields"]),
        "philippineReleaseDate": "2021-06-05",
        "historicalLaunchPricePhp": 23999,
        "historicalPriceReductionPhp": 21999,
        "currentPrice": "not orderability-verified; left blank",
        "image": "neutral placeholder; reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
