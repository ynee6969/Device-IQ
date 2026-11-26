#!/usr/bin/env python3
"""Record sourced Philippine configuration evidence for OnePlus 10 Pro."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/oneplus-10-pro-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_63c58f9b94a470"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-12gb-256gb-ph"

URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_ONEPLUS_SPECS = "https://www.oneplus.com/global/10-pro/specs"
URL_ONEPLUS_GLOBAL_EVENT = "https://www.youtube.com/watch?v=nKSOPsG0ma8"
URL_UNBOX = "https://unbox.ph/gadget/oneplus-10-pro-now-available-for-pre-order-in-the-philippines/"
URL_GIZGUIDE = "https://www.gizguide.com/2022/04/oneplus-10-pro-price-specs-official-philippines.html"
URL_YUGA = "https://www.yugatech.com/mobile/oneplus-10-pro-price-philippines/"
URL_YUGA_LOCAL = "https://www.yugatech.com/mobile/oneplus-10-pro-now-official-coming-to-ph/"
URL_NOYPI = "https://www.noypigeeks.com/android/oneplus-10-pro-specs-price-availability/"
URL_MANILASHAKER = "https://manilashaker.com/oneplus-10-pro-now-available-via-digital-walker-stores/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-gen-1-mobile-platform"
URL_QUALCOMM_BRIEF = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/snapdragon-8-gen-1-mobile-platform-product-brief.pdf"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/oneplus-10-pro"
URL_NANOREVIEW_SOC = "https://nanoreview.net/en/soc/qualcomm-snapdragon-8-gen-1"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-oneplus-10-pro"
URL_GSMARENA = "https://www.gsmarena.com/oneplus_10_pro-11234.php"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("oneplus_10_pro_ntc", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and model-code match",
           "The NTC 2022 GEC lists ONEPLUS model NE2213 as OnePlus 10 Pro 5G. This supports the Philippine model identity; it does not independently establish the retail configuration."),
    source("oneplus_10_pro_specs", "OnePlus Global", URL_ONEPLUS_SPECS,
           "Primary exact-model-family hardware, configuration, color, and connectivity specifications",
           "OnePlus lists the global model's 12 GB LPDDR5 / 256 GB UFS 3.1 option, Emerald Forest and Volcanic Black colors, display, cameras, battery, 80 W wired and 50 W wireless charging, connectivity, ports, sensors, and dimensions. It is a global specification page; Philippine channel and variant evidence is established separately."),
    source("oneplus_10_pro_global_event", "OnePlus Official", URL_ONEPLUS_GLOBAL_EVENT,
           "Manufacturer global launch event date",
           "OnePlus's verified global launch-event video was published March 31, 2022. The Chinese announcement was earlier; this field uses the global event date.",
           "2022-03-31"),
    source("oneplus_10_pro_unbox_ph", "Unbox Philippines", URL_UNBOX,
           "Philippine Digital Walker preorder date, exact local configuration, SRP, preorder discount, and local hardware",
           "Published April 2, 2022. Reports preorder through Digital Walker beginning April 2, ending April 6, for the 12 GB / 256 GB configuration. It gives PHP 52,990 SRP and PHP 4,000 off during preorder (PHP 48,990), and describes 80 W wired / 50 W wireless charging. This is dated local launch evidence, not a current offer.",
           "2022-04-02"),
    source("oneplus_10_pro_gizguide_ph", "GIZGUIDE Philippines", URL_GIZGUIDE,
           "Local official SRP, preorder window, color options, and Philippine hardware specifications",
           "Published April 1, 2022 and attributes the local SRP to Digital Walker. Identifies Volcanic Black and Emerald Forest colors, 12 GB / 256 GB local retail configuration, PHP 52,990 SRP, PHP 48,990 preorder, and 80 W / 50 W charging. It reports LPDDR5X whereas OnePlus's global spec page says LPDDR5; retain that memory-type discrepancy." ,
           "2022-04-01"),
    source("oneplus_10_pro_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Local SRP and preorder offer cross-check",
           "Published April 1, 2022. Reports Digital Walker's 12 GB / 256 GB listing at PHP 48,990 during the April 2-6 preorder, lists IP68 in its specification summary, and identifies local color/configuration details. This is a historical promotional price, not the SRP or a current offer.",
           "2022-04-01"),
    source("oneplus_10_pro_yugatech_announcement", "YugaTech Philippines", URL_YUGA_LOCAL,
           "Philippine market announcement cross-check",
           "Published April 1, 2022. Reports OnePlus confirmed the 10 Pro 5G was coming to the Philippines. It supports local launch context but does not alone establish completed sale or exact distributor stock.",
           "2022-04-01"),
    source("oneplus_10_pro_noypi_ph", "NoypiGeeks Philippines", URL_NOYPI,
           "Local authorized-channel availability, price, and regional hardware cross-check",
           "Published April 21, 2022. Reports OnePlus 10 Pro available at Digital Walker, identified as OnePlus's official Philippine distributor, and PHP 52,990. Its article says 65 W wired charging and 800-nit peak brightness; both are retained as source conflicts against the manufacturer/global and other local launch specifications.",
           "2022-04-21"),
    source("oneplus_10_pro_manilashaker_ph", "ManilaShaker Philippines", URL_MANILASHAKER,
           "Independent Digital Walker availability and local configuration cross-check",
           "Published April 21, 2022. Identifies Digital Walker as official distributor, says the phone is available nationwide, lists 12 GB / 256 GB at PHP 52,990 and the two local color names. It also reports 65 W wired charging, conflicting with the OnePlus global specification and preorder reporting.",
           "2022-04-21"),
    source("oneplus_10_pro_qualcomm", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 8 Gen 1 platform reference",
           "Qualcomm's product page documents the chipset family and Adreno graphics platform; platform capabilities are not substituted for handset-specific details."),
    source("oneplus_10_pro_qualcomm_brief", "Qualcomm", URL_QUALCOMM_BRIEF,
           "Primary chipset process and CPU capability reference",
           "Qualcomm's product brief specifies the 4 nm Snapdragon 8 Gen 1 process and CPU capability up to 3.0 GHz with Cortex-X2 technology. Core-cluster detail is cross-checked with NanoReview."),
    source("oneplus_10_pro_nanoreview", "NanoReview", URL_NANOREVIEW,
           "Exact-model secondary technical cross-check",
           "Exact OnePlus 10 Pro page used for chipset architecture, display, camera, battery, connectivity, and build cross-checks. Benchmark scores are not copied into the catalog; regional details are checked against OnePlus and local sources."),
    source("oneplus_10_pro_nanoreview_soc", "NanoReview", URL_NANOREVIEW_SOC,
           "Independent Snapdragon 8 Gen 1 architecture cross-check",
           "Used for CPU cluster details only; chipset benchmarks are not treated as phone specifications."),
    source("oneplus_10_pro_kimovil", "Kimovil", URL_KIMOVIL,
           "Global model/configuration and secondary technical cross-check",
           "The exact model page distinguishes global and regional variants and corroborates the 12 GB / 256 GB global configuration. Price listings are not treated as current Philippine prices."),
    source("oneplus_10_pro_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact model-number family, regional hardware, and secondary specification cross-check",
           "Exact OnePlus 10 Pro listing includes models NE2210/NE2211/NE2213/NE2215/NE2217 and distinguishes international 80 W charging from North American 65 W. NTC model NE2213 is locally registered, but local coverage still disagrees on charging; do not assume the region-specific hardware solely from a shared family listing."),
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
    if unit is not None:
        item["unit"] = unit
    if price_type is not None:
        item["priceType"] = price_type
    return item


def fields_for() -> list[dict]:
    config = "Philippine OnePlus 10 Pro NE2213: 12 GB RAM / 256 GB storage; Volcanic Black or Emerald Forest"
    rows = [
        field("model_number", "oneplus_10_pro_ntc", "NTC 2022 GEC lists ONEPLUS model NE2213 as OnePlus 10 Pro 5G", "NE2213", status="VERIFIED", note="Exact Philippine model-code and marketed-name match.", config_match="OnePlus 10 Pro 5G registered model NE2213"),
        field("global_release_date", "oneplus_10_pro_global_event", "OnePlus official global launch event published March 31, 2022", "2022-03-31", status="VERIFIED", note="Uses the global launch date, distinct from the earlier China announcement and Philippine preorder date.", config_match="OnePlus 10 Pro global version"),
        field("configuration", "oneplus_10_pro_unbox_ph", "Philippine preorder listing identifies 12 GB RAM / 256 GB storage; local reports list Volcanic Black and Emerald Forest colors", "12 GB RAM / 256 GB storage; Volcanic Black and Emerald Forest", status="VERIFIED_SECONDARY", note="The two color choices share the same reported 12/256 hardware; they are recorded as colors of one configuration, not duplicate configurations.", config_match=config),
        field("philippine_release_date", "oneplus_10_pro_unbox_ph", "Digital Walker Philippine preorder opened April 2, 2022; nationwide store availability was reported April 21", "2022-04-02", status="VERIFIED_SECONDARY", note="Date label is the first dated official-channel preorder, not a claim that all preorder units were delivered that day.", config_match="Philippine OnePlus 10 Pro launch; 12/256 local configuration"),
        field("official_launch_price_php", "oneplus_10_pro_unbox_ph", "Official SRP PHP 52,990 for 12 GB / 256 GB; preorder promotion PHP 48,990 from April 2-6, 2022", 52990, status="VERIFIED_SECONDARY", unit="PHP", note="Unbox and GIZGUIDE report PHP 52,990 SRP and PHP 48,990 dated preorder price; YugaTech corroborates the promotional price. Store PHP 52,990 as launch SRP and retain PHP 48,990 as a separate historical promotion.", config_match=config, price_type="historical_ph_launch_srp"),
        field("current_price_php", "oneplus_10_pro_kimovil", "No current dated, orderable Philippine offer was verified; global price comparison is not a Philippine listing", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank. The 2022 SRP and preorder promotion remain historical only.", config_match=config, price_type="no_current_offer_verified"),
        field("display_size", "oneplus_10_pro_specs", "6.7-inch display", 6.7, status="VERIFIED", key="displayInches", unit="in", note="OnePlus and Philippine launch reports agree.", config_match=config),
        field("display_technology", "oneplus_10_pro_specs", "Fluid AMOLED with LTPO 2.0", "Fluid AMOLED LTPO 2.0", status="VERIFIED", key="displayType", note="OnePlus and Philippine launch coverage identify the AMOLED LTPO 2.0 panel.", config_match=config),
        field("display_resolution", "oneplus_10_pro_specs", "3216 x 1440 pixels (QHD+)", "3216 x 1440", status="VERIFIED", key="resolution", note="Manufacturer specifications give 3216 x 1440; local reports agree.", config_match=config),
        field("display_refresh_rate", "oneplus_10_pro_specs", "Adaptive refresh rate up to 120 Hz", 120, status="VERIFIED", key="refreshHz", unit="Hz", note="OnePlus and local sources identify adaptive LTPO refresh up to 120 Hz.", config_match=config),
        field("display_brightness", "oneplus_10_pro_noypi_ph", "Local source reports 800-nit peak, while other launch specifications report 1300-nit peak/HDR brightness", None, status="CONFLICTING_INFORMATION", unit="nits", note="Brightness values differ and may use different measurement conventions. Leave the normalized value blank.", config_match=config),
        field("display_protection", "oneplus_10_pro_specs", "Corning Gorilla Glass Victus", "Corning Gorilla Glass Victus", status="VERIFIED_SECONDARY", note="Local launch sources identify Gorilla Glass Victus; OnePlus's spec page names Corning Gorilla Glass without generation.", config_match=config),
        field("chipset", "oneplus_10_pro_specs", "Qualcomm Snapdragon 8 Gen 1 (SM8450)", "Qualcomm Snapdragon 8 Gen 1", status="VERIFIED", key="chipset", note="OnePlus and Philippine launch sources agree on the Snapdragon 8 Gen 1 platform.", config_match=config),
        field("process_node", "oneplus_10_pro_qualcomm_brief", "4 nm process technology", 4, status="VERIFIED", unit="nm", note="Qualcomm identifies the Snapdragon 8 Gen 1 as a 4 nm platform.", config_match=config),
        field("cpu", "oneplus_10_pro_nanoreview_soc", "1x Cortex-X2 up to 3.0 GHz + 3x Cortex-A710 up to 2.5 GHz + 4x Cortex-A510 up to 1.8 GHz", "1x Cortex-X2 3.0 GHz + 3x Cortex-A710 2.5 GHz + 4x Cortex-A510 1.8 GHz", status="VERIFIED_SECONDARY", key="cpu", note="NanoReview's Snapdragon 8 Gen 1 core details; Qualcomm confirms the 3.0 GHz Cortex-X2-class platform. This is chipset architecture, not handset benchmark performance.", config_match=config),
        field("gpu", "oneplus_10_pro_specs", "Qualcomm Adreno 730", "Qualcomm Adreno 730", status="VERIFIED", key="gpu", note="OnePlus lists Adreno 730 for the 10 Pro; Qualcomm platform materials corroborate the GPU family.", config_match=config),
        field("operating_system", "oneplus_10_pro_unbox_ph", "OxygenOS 12.1 based on Android 12 at Philippine launch", "OxygenOS 12.1 based on Android 12", status="VERIFIED_SECONDARY", key="os", note="OnePlus's global page says OxygenOS based on Android 12; local launch reporting identifies OxygenOS 12.1. Later installed versions are not substituted.", config_match=config),
        field("os_support", "oneplus_10_pro_specs", "No model-specific guaranteed OS-upgrade or security-support duration found in the reviewed manufacturer launch/specification sources", None, status="NOT_DISCLOSED", note="Do not infer an update promise from later device software releases.", config_match=config),
        field("ram_capacity", "oneplus_10_pro_unbox_ph", "12 GB RAM", 12, status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="Exact Philippine preorder configuration; both local color options use the same capacity.", config_match=config),
        field("ram_type", "oneplus_10_pro_specs", "OnePlus global specifications say LPDDR5; GIZGUIDE and ManilaShaker report LPDDR5X", None, status="CONFLICTING_INFORMATION", note="Memory generation wording conflicts across the manufacturer page and Philippine secondary coverage. Leave the normalized RAM type blank until a hardware-specific NE2213 document resolves it.", config_match=config),
        field("storage_capacity", "oneplus_10_pro_unbox_ph", "256 GB internal storage", 256, status="VERIFIED_SECONDARY", key="storageGb", unit="GB", note="The exact Philippine 12/256 preorder configuration is corroborated by local launch reports and OnePlus's global variant list.", config_match=config),
        field("storage_type", "oneplus_10_pro_specs", "UFS 3.1 2-lane storage", "UFS 3.1", status="VERIFIED", note="OnePlus global and Philippine sources identify UFS 3.1 storage.", config_match=config),
        field("storage_expansion", "oneplus_10_pro_gsmarena", "No microSD card slot listed", "No microSD slot", status="VERIFIED_SECONDARY", note="Exact-model technical references list fixed internal storage and no memory-card slot.", config_match=config),
        field("rear_camera_system", "oneplus_10_pro_specs", "48 MP main + 50 MP 150-degree ultrawide + 8 MP telephoto with 3.3x optical zoom", "48 MP main + 50 MP ultrawide + 8 MP telephoto", status="VERIFIED", note="OnePlus and Philippine coverage agree on the three rear cameras; manufacturer model page is used for module layout.", config_match=config),
        field("main_camera_sensor", "oneplus_10_pro_specs", "Sony IMX789, 48 MP, f/1.8, OIS", "Sony IMX789 48 MP f/1.8 with OIS", status="VERIFIED", note="OnePlus identifies the sensor and optical stabilization.", config_match=config),
        field("ultrawide_camera", "oneplus_10_pro_specs", "Samsung JN1, 50 MP, 150-degree field of view", "Samsung JN1 50 MP, 150-degree FOV", status="VERIFIED_SECONDARY", note="OnePlus specifies JN1, 50 MP, and 150-degree FOV; local reports identify Samsung ISOCELL JN1.", config_match=config),
        field("telephoto_camera", "oneplus_10_pro_specs", "8 MP telephoto with OIS and 3.3x optical zoom", "8 MP telephoto; OIS; 3.3x optical zoom", status="VERIFIED", note="OnePlus and Philippine launch sources agree on telephoto resolution, optical stabilization, and 3.3x zoom.", config_match=config),
        field("front_camera", "oneplus_10_pro_specs", "Sony IMX615 32 MP front camera", 32, status="VERIFIED", key="frontCameraMp", unit="MP", note="OnePlus identifies the IMX615 sensor and 32 MP resolution; local aperture figures vary and are not asserted.", config_match=config),
        field("video_recording", "oneplus_10_pro_specs", "Rear video up to 8K/24 fps and 4K/120 fps; front video up to 1080p/30 fps", "Rear up to 8K/24 fps and 4K/120 fps; front up to 1080p/30 fps", status="VERIFIED", note="Maximum modes published on OnePlus's exact product specifications page.", config_match=config),
        field("battery_capacity", "oneplus_10_pro_specs", "5,000 mAh typical capacity", 5000, status="VERIFIED", key="batteryMah", unit="mAh", note="OnePlus and Philippine launch coverage agree on typical 5,000 mAh capacity.", config_match=config),
        field("battery_technology", "oneplus_10_pro_specs", "Non-removable lithium-polymer battery", "Li-Po; non-removable", status="VERIFIED_SECONDARY", note="OnePlus states the battery is non-removable; exact-model technical references identify Li-Po chemistry.", config_match=config),
        field("wired_charging", "oneplus_10_pro_manilashaker_ph", "OnePlus global specs and April 2 local preorder coverage report 80 W; April 21 Philippine availability reporting says 65 W", None, status="CONFLICTING_INFORMATION", unit="W", note="The manufacturer global specification and April 2 local preorder page list 80 W, while April 21 local availability reporting lists 65 W. Because the conflict concerns the Philippine retail unit, leave normalized charging power blank pending a package/model-specific local specification.", config_match=config),
        field("wireless_charging", "oneplus_10_pro_specs", "50 W AIRVOOC wireless charging", 50, status="VERIFIED", key="wirelessChargingW", unit="W", note="OnePlus and multiple Philippine sources identify 50 W wireless charging.", config_match=config),
        field("dimensions", "oneplus_10_pro_specs", "163.0 x 73.9 x 8.55 mm", "163.0 x 73.9 x 8.55 mm", status="VERIFIED", key="dimensions", unit="mm", note="OnePlus's exact product page gives these dimensions; local values are rounded versions.", config_match=config),
        field("weight", "oneplus_10_pro_specs", "200.5 g", 200.5, status="VERIFIED", key="weightG", unit="g", note="Manufacturer page gives 200.5 g; local coverage rounds to 200 or 201 g.", config_match=config),
        field("materials", "oneplus_10_pro_gsmarena", "Glass front with Gorilla Glass Victus, glass back, aluminum frame", "Gorilla Glass Victus front; glass back; aluminum frame", status="VERIFIED_SECONDARY", note="Exact-model build cross-check; OnePlus's product page confirms the cover glass family but not the frame material.", config_match=config),
        field("ingress_protection", "oneplus_10_pro_yugatech_ph", "YugaTech lists IP68, while OnePlus's global specification page does not assign an IP rating to the registered NE2213 Philippine unit", None, status="CONFLICTING_INFORMATION", note="IP protection is region/operator-specific in some OnePlus 10 Pro references. Do not apply a US/T-Mobile IP68 claim to the Philippine NE2213 without exact local documentation.", config_match=config),
        field("sim_esim", "oneplus_10_pro_specs", "Dual Nano-SIM; eSIM support not stated for the Philippine configuration", "Dual Nano-SIM; eSIM not recorded", status="VERIFIED", key="sim", note="OnePlus specifications list two Nano-SIM slots. The reviewed local/official material does not establish eSIM support for NE2213.", config_match=config),
        field("cellular_bands", "oneplus_10_pro_specs", "Global NE2213 family page lists GSM B2/3/5/8; WCDMA B1/2/4/5/8/19; LTE FDD B1/2/3/4/5/7/8/12/13/17/18/19/20/25/26/28/30/32/66/71; LTE TDD B38/39/40/41/46/48; 5G NSA/SA n1/2/3/5/7/8/20/25/28/30/38/40/41/48/66/71/77/78", "Manufacturer-published global 2G/3G/4G/5G bands; Philippine carrier compatibility not independently tested", status="VERIFIED_SECONDARY", key="cellular", note="Band list is from OnePlus's global page for the model family. This records supported bands; it is not a claim of certification on every Philippine carrier or active 5G band combination.", config_match="NE2213 global family; Philippine retail configuration identity established separately"),
        field("wifi", "oneplus_10_pro_specs", "Dual-band 2.4/5 GHz Wi-Fi 802.11 a/b/g/n/ac/ax (Wi-Fi 6)", "Wi-Fi 6, dual-band", status="VERIFIED", key="wifi", note="OnePlus global specifications list 802.11ax and dual-band Wi-Fi; Philippine coverage also identifies Wi-Fi 6.", config_match=config),
        field("bluetooth", "oneplus_10_pro_specs", "Bluetooth 5.2 with aptX, aptX HD, LDAC, and AAC support", "Bluetooth 5.2", status="VERIFIED", note="OnePlus's exact model family specification and local reports list Bluetooth 5.2.", config_match=config),
        field("usb", "oneplus_10_pro_specs", "USB Type-C 3.1 Gen 1; USB 3.1 data speed requires a compatible cable", "USB Type-C 3.1 Gen 1; OTG", status="VERIFIED", key="ports", note="OnePlus specifies USB 3.1 Gen 1 and Type-C; it notes the supplied standard cable supports USB 2.0 data speed.", config_match=config),
        field("nfc", "oneplus_10_pro_specs", "NFC enabled", "Yes", status="VERIFIED", note="OnePlus specification page lists NFC enabled.", config_match=config),
        field("gnss", "oneplus_10_pro_specs", "Dual-band GPS (L1+L5), GLONASS, Galileo (E1+E5a), BeiDou, A-GPS", "Dual-band GPS, GLONASS, Galileo, BeiDou, A-GPS", status="VERIFIED", key="gnss", note="OnePlus's global specification page lists the named systems; no additional GNSS support is inferred.", config_match=config),
        field("audio", "oneplus_10_pro_specs", "Dual stereo speakers with Dolby Atmos; no 3.5 mm headphone jack", "Dual stereo speakers; Dolby Atmos; no 3.5 mm jack", status="VERIFIED_SECONDARY", key="sound", note="OnePlus confirms stereo speakers and Dolby Atmos; exact-model technical reference confirms no 3.5 mm jack.", config_match=config),
        field("sensors", "oneplus_10_pro_specs", "In-display fingerprint, accelerometer, electronic compass, gyroscope, ambient-light, proximity, sensor core, flicker-detect, and front RGB sensors", "In-display fingerprint; accelerometer; compass; gyroscope; ambient light; proximity; sensor core; flicker detect; front RGB", status="VERIFIED", note="Sensor list as specified by OnePlus for the global model family.", config_match=config),
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
        "availabilityStatus": "Philippine preorder coverage identifies Digital Walker, later reported as OnePlus's official Philippine distributor, with NTC GEC listing NE2213 as OnePlus 10 Pro 5G. Workbook eligibility remains Pending.",
        "philippineAvailability": "The OnePlus 10 Pro 5G was announced for the Philippines in April 2022 and offered for preorder through Digital Walker from April 2 to April 6. Later reports say it was available nationwide through Digital Walker. The documented Philippine configuration is 12 GB / 256 GB in Volcanic Black and Emerald Forest, with PHP 52,990 SRP and PHP 48,990 preorder promotion. Current stock and price are not verified.",
        "observedAt": OBSERVED,
        "manufacturer": "OnePlus Technology (Shenzhen) Co., Ltd.",
        "catalogModel": "OnePlus 10 Pro",
        "productLine": "OnePlus 10 Series",
        "modelNumber": "NE2213",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Philippine preorder start date",
        "researchNotes": "Workbook row 86 OnePlus 10 Pro matches NTC model NE2213 / OnePlus 10 Pro 5G. Philippine preorder reporting identifies one local hardware configuration, 12 GB / 256 GB, offered in Volcanic Black and Emerald Forest. The colors share identical memory/storage and remain one configuration. Local SRP is PHP 52,990; PHP 48,990 was a dated April 2-6 preorder offer. The OnePlus global specification lists LPDDR5 and 80 W wired charging, while Philippine secondary sources disagree on LPDDR5X versus LPDDR5 and 65 W versus 80 W; the catalog leaves those fields unresolved. Some sources claim IP68 but exact NE2213 coverage is not consistent, so ingress protection remains blank. Current local price is blank. Exact official product images are available but reuse rights are not stated, so the neutral placeholder remains. Workbook eligibility is Pending.",
        "qualityFlag": "NE2213 model match, local 12/256 configuration, colors, SRP, and preorder price verified; current price unavailable; RAM type, wired charging, display brightness, and IP rating conflicts preserved; workbook eligibility remains Pending.",
        "openIssues": [
            {"issue": "OnePlus lists LPDDR5, while GIZGUIDE and ManilaShaker list LPDDR5X", "action": "Keep RAM type blank until hardware-specific Philippine NE2213 documentation resolves the difference."},
            {"issue": "OnePlus and April 2 preorder coverage list 80 W wired charging, while April 21 local availability reports list 65 W", "action": "Keep wired charging power blank pending confirmation for the local NE2213 retail unit."},
            {"issue": "Display brightness reports vary between 800 nits and 1300 nits", "action": "Keep normalized brightness blank."},
            {"issue": "IP68 claims may apply to region/operator-specific variants and are not established for the Philippine NE2213 unit", "action": "Keep the ingress-protection rating blank unless exact local documentation is found."},
            {"issue": "No current dated, orderable Philippine offer was verified", "action": "Keep current price blank and retain 2022 prices as historical only."},
            {"issue": "Exact OnePlus product images are available, but reuse terms or permission are not recorded", "action": "Keep the neutral placeholder until image rights are documented."},
            {"issue": "Workbook eligibility is Pending", "action": "Preserve the study's Pending status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 86 or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "oneplus"
            or device.get("model", "").casefold() not in {"10 pro", "oneplus 10 pro"}):
        raise ValueError("Workbook row 86 no longer matches OnePlus 10 Pro")
    variant_ids = {variant.get("id") for variant in device.get("variants", [])}
    if variant_ids - {OLD_CONFIG, CONFIG}:
        raise ValueError(f"Unexpected OnePlus 10 Pro configurations: {sorted(variant_ids)}")
    existing = [row for row in manual.get("records", []) if row.get("deviceId") == DEVICE]
    if any(row.get("configurationId") != CONFIG for row in existing):
        raise ValueError("Unexpected existing OnePlus 10 Pro review configuration; inspect before replacing")

    variant = {
        "id": CONFIG,
        "label": "12 GB RAM / 256 GB storage (Volcanic Black / Emerald Forest)",
        "sku": None,
        "modelCode": "NE2213",
        "notes": "Philippine preorder and local availability sources identify 12 GB / 256 GB in Volcanic Black and Emerald Forest. The colors share one hardware configuration. Historical SRP PHP 52,990; April 2-6, 2022 preorder promotion PHP 48,990. Current price not verified.",
        "workbookRow": 86,
    }
    record = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "OnePlus",
        "model": "10 Pro",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "modelCode": "NE2213",
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
        "reason": "OnePlus's official 10 Pro specification page shows exact product images for Emerald Forest and Volcanic Black, but no reusable license or permission to copy/embed is stated. Keep the neutral placeholder.",
        "sourcePage": URL_ONEPLUS_SPECS,
        "assetUrl": None,
        "scope": "OnePlus 10 Pro NE2213; Philippine 12 GB / 256 GB configuration in Volcanic Black or Emerald Forest",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for OnePlus 10 Pro",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    price_events = [
        ("oneplus_10_pro_unbox_ph", "2022-04-02", 52990, "historical local launch SRP"),
        ("oneplus_10_pro_gizguide_ph", "2022-04-01", 52990, "Digital Walker-attributed Philippine SRP"),
        ("oneplus_10_pro_noypi_ph", "2022-04-21", 52990, "historical local authorized-channel price"),
        ("oneplus_10_pro_manilashaker_ph", "2022-04-21", 52990, "historical local distributor retail price"),
        ("oneplus_10_pro_unbox_ph", "2022-04-02", 48990, "April 2-6 preorder promotion"),
        ("oneplus_10_pro_gizguide_ph", "2022-04-01", 48990, "April 2-6 preorder promotion"),
        ("oneplus_10_pro_yugatech_ph", "2022-04-01", 48990, "Digital Walker preorder promotion announced April 1; order window began April 2"),
    ]
    for sid, published, amount, kind in price_events:
        prices.append({
            "device_id": DEVICE,
            "amount_php": amount,
            "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_ne2213_12gb_256gb_configuration",
            "variant_ram_gb": 12,
            "variant_storage_gb": 256,
            "price_type": "historical_ph_launch_srp" if amount == 52990 else "historical_ph_preorder_promotion",
            "source_published_at": published,
            "excerpt": f"{kind}: OnePlus 10 Pro NE2213 12 GB / 256 GB listed at PHP {amount:,}; historical price observation, not current.",
            "source_url": next(item["url"] for item in SOURCES if item["id"] == sid),
            "source_kind": "historical_local_price_candidate",
            "observed_at": OBSERVED_AT,
            "local_availability_verified": True,
            "availability_status": "historical_price_not_current",
        })
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "OnePlus", "model_name": "10 Pro", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC 2022 GEC lists OnePlus model NE2213 as OnePlus 10 Pro 5G."},
            {"device_id": DEVICE, "source_url": URL_UNBOX, "result": "Digital Walker's April 2-6 Philippine preorder documents 12/256 configuration, PHP 52,990 SRP, PHP 48,990 promotion, and local 80W/50W charging specs."},
            {"device_id": DEVICE, "source_url": URL_MANILASHAKER, "result": "Digital Walker nationwide availability reported April 21; local reports disagree on wired charging power and RAM type."},
            {"device_id": DEVICE, "source_url": URL_ONEPLUS_SPECS, "result": "Manufacturer global specifications confirm the OnePlus 10 Pro hardware family, colors, and exact global specifications; region-specific claims are kept distinct."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 86 OnePlus 10 Pro -> NTC model NE2213 / global version",
        "configuration": variant["label"],
        "colors": ["Volcanic Black", "Emerald Forest"],
        "philippinePreorderStart": "2022-04-02",
        "launchSrpPhp": 52990,
        "preorderPromotionPhp": 48990,
        "reviewedFields": len(record["fields"]),
        "currentPrice": "blank; no current dated local offer verified",
        "image": "neutral placeholder; reuse rights not established",
        "unresolved": ["LPDDR5 vs LPDDR5X", "65W vs 80W wired charging", "display brightness", "local IP rating"],
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
        "historicalPriceCandidates": len(prices),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
