#!/usr/bin/env python3
"""Record exact-SKU, source-backed reviews for Galaxy Tab S10 FE+ (PH)."""
from __future__ import annotations

import json
from pathlib import Path

import add_verified_samsung_tab_s9_fe_review as fe_template
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-tab-s10-fe-plus-ph-prices-2026-11-27.json"
IMAGE_SOURCES = ROOT / "research/catalog-image-sources.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-27"
DEVICE = "device_8a813e7f0aaaae"
MODEL = "Galaxy Tab S10 FE+"
UNRECORDED = f"{DEVICE}-unrecorded"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = {
    "wifi": src(
        "samsung_tab_s10_fe_plus_ph_wifi_128_specs",
        "https://www.samsung.com/ph/business/tablets/galaxy-tab-s/galaxy-tab-s10-fe-plus-gray-128gb-sm-x620nzaaxtc/",
        "Samsung Philippines", "Exact local Wi-Fi SKU and configuration specifications",
        "Samsung Philippines identifies Gray Wi-Fi SKU SM-X620NZAAXTC as 8 GB RAM / 128 GB storage and publishes its hardware details."),
    "5g": src(
        "samsung_tab_s10_fe_plus_ph_5g_128_specs",
        "https://www.samsung.com/ph/business/tablets/galaxy-tab-s/galaxy-tab-s10-fe-plus-gray-128gb-sm-x626bzaaxtc/",
        "Samsung Philippines", "Exact local 5G SKU and configuration specifications",
        "Samsung Philippines identifies Gray 5G SKU SM-X626BZAAXTC as 8 GB RAM / 128 GB storage and publishes its hardware, cellular-band and SIM/eSIM details."),
    "global_launch": src(
        "samsung_tab_s10_fe_plus_global_launch",
        "https://news.samsung.com/global/galaxy-tab-s10-fe-series-brings-intelligent-experiences-to-the-forefront-with-premium-versatile-design",
        "Samsung Global Newsroom", "Global launch date and model-family specifications",
        "Samsung announced the S10 FE family on 2025-04-02 and states availability in select markets beginning 2025-04-03. The story identifies FE+ display, cameras, chipset, memory options, battery, charging and launch OS; it is not Philippine-sale evidence.",
        "2025-04-02"),
    "ph_launch": src(
        "samsung_tab_s10_fe_plus_ph_launch",
        "https://news.samsung.com/ph/galaxy-tab-s10-fe-series-brings-intelligent-experiences-to-the-forefront-with-premium-versatile-design",
        "Samsung Newsroom Philippines", "Philippine launch announcement and local configuration availability",
        "Samsung Philippines announced local availability from 2025-05-15 for the Galaxy Tab S10 FE+ 5G (128 GB), in Gray and Blue. The announcement does not state the Wi-Fi FE+ first-sale date or RAM for the 5G launch option.",
        "2025-04-02"),
    "ph_launch_price": src(
        "samsung_tab_s10_fe_plus_ph_launch_price_story",
        "https://news.samsung.com/ph/bigger-screen-bigger-possibilities-three-reasons-why-the-galaxy-tab-s10-fe-series-is-the-perfect-campus-companion",
        "Samsung Newsroom Philippines", "Historical Philippine series price context",
        "Samsung's local story describes the FE+ 5G as available from PHP 39,990; RAM is not stated, so this is retained as model/network-level evidence only."),
    "ph_history_price": src(
        "samsung_tab_s10_fe_plus_ph_2025_trade_in_price",
        "https://www.samsung.com/ph/offer/offline/2025/galaxy-tab-trade-in/",
        "Samsung Philippines", "Historical exact-configuration SRP",
        "Samsung's expired July 2025 offer table lists FE+ 5G (8 GB + 128 GB) at SRP PHP 39,990, with trade-in savings available separately; campaign dates were July 1–September 30, 2025."),
    "ph_current_price": src(
        "samsung_tab_s10_fe_plus_ph_2026_current_srp",
        "https://www.samsung.com/ph/trade-in/",
        "Samsung Philippines", "Current local SRP for exact 8 GB / 128 GB Wi-Fi and 5G variants",
        "The live Samsung Philippines trade-in page, valid through 2026-11-30, lists SRP PHP 47,490 for Galaxy Tab S10 FE+ Wi-Fi (8 GB + 128 GB) and PHP 52,690 for 5G (8 GB + 128 GB). SRP excludes optional trade-in value; checkout stock was not checked."),
    "exynos": src(
        "samsung_exynos_1580_official_specs",
        "https://semiconductor.samsung.com/processor/mobile-processor/exynos-1580/",
        "Samsung Semiconductor", "Exynos 1580 process, CPU and GPU specifications",
        "Samsung lists third-generation 4 nm EUV FinFET and Xclipse 540 graphics. Its Exynos 1580 CPU specification lists Cortex-A720 at 2.9 and 2.6 GHz and Cortex-A520 at 1.95 GHz."),
    "security": src(
        "samsung_tab_s10_fe_plus_ph_security_support",
        "https://www.samsung.com/ph/business/tablets/galaxy-tab-s/galaxy-tab-s10-fe-plus-gray-128gb-sm-x626bzaaxtc/",
        "Samsung Philippines", "Published product support-period endpoint",
        "Samsung Philippines lists the security-update period as valid until 30 April 2032 on the exact local FE+ product pages; this is a support-period endpoint, not an OS-upgrade-count guarantee."),
    "nanoreview": src(
        "nanoreview_samsung_galaxy_tab_s10_fe_plus_specs",
        "https://nanoreview.net/en/tablet/samsung-galaxy-tab-s10-fe",
        "NanoReview", "Secondary technical cross-check for the Galaxy Tab S10 FE+",
        "NanoReview's FE+ page exposes 8/128 and 12/256 options and lists LPDDR5X, UFS 3.1, 4 speakers, Dolby Atmos, no wireless charging and Li-Ion chemistry. It reports 90 Hz and 800 nits maximum; the brightness measurement condition is unclear."),
    "kimovil": src(
        "kimovil_samsung_galaxy_tab_s10_fe_plus_specs",
        "https://www.kimovil.com/en/where-to-buy-samsung-galaxy-tab-s10-fe-plus",
        "Kimovil", "Secondary global model cross-check; conflicting claims are not promoted",
        "Kimovil lists global 8/128 Wi-Fi and 5G versions and LPDDR5X, but this page also reports 120 Hz and 1750 nits, contrary to Samsung's 90 Hz / 600 nits max and 800 nits HBM. Its conflicting panel data are not used as local product specifications; its Li-Polymer claim is retained only as unresolved chemistry evidence."),
    "annual_report": src(
        "samsung_2025_q3_report_tab_s10_fe_platform",
        "https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_3Q_Interim_Report.pdf",
        "Samsung Electronics", "Launch platform and OS confirmation",
        "Samsung's 2025 Q3 interim report labels Galaxy Tab S10 FE / FE+ (April 2025) and lists Exynos 1580, Android 15 and One UI 7.0."),
    "image_press": src(
        "samsung_mobile_press_tab_s10_fe_plus_gallery",
        "https://www.samsungmobilepress.com/media-assets/galaxy-tab-s10-fe-plus?tab=images",
        "Samsung Mobile Press", "Exact-model gray product image and usage-rights review",
        "The official gallery contains the exact Galaxy Tab S10 FE+ gray-front product image. Samsung Mobile Press terms restrict use to personal, informational, non-commercial purposes and require proprietary notices to remain intact; the DeviceIQ thesis catalog is treated as educational/non-commercial."),
    "image_terms": src(
        "samsung_mobile_press_image_terms",
        "https://www.samsungmobilepress.com/terms",
        "Samsung Mobile Press", "Product image reuse terms",
        "Terms permit personal, informational and non-commercial use only; no commercial rights are granted and copyright, trademark and proprietary notices must be preserved."),
}

CONFIGS = [
    {"id": f"{DEVICE}-sm-x620n-8gb-128gb-wifi-ph", "key": "wifi",
     "modelCode": "SM-X620N", "sku": "SM-X620NZAAXTC", "ram": 8,
     "storage": 128, "network": "Wi-Fi", "weight": 664, "launch": 0},
    {"id": f"{DEVICE}-sm-x626b-8gb-128gb-5g-ph", "key": "5g",
     "modelCode": "SM-X626B", "sku": "SM-X626BZAAXTC", "ram": 8,
     "storage": 128, "network": "5G", "weight": 668, "launch": 39990},
]

CELLULAR_BANDS = (
    "2G GSM 850/900/1800/1900; 3G UMTS B1 (2100)/B2 (1900)/B4 (AWS)/B5 (850)/B8 (900); "
    "4G FDD LTE B1 (2100)/B2 (1900)/B3 (1800)/B4 (AWS)/B5 (850)/B7 (2600)/B8 (900)/"
    "B12 (700)/B13 (700)/B17 (700)/B20 (800)/B25 (1900)/B26 (850)/B28 (700)/B32 (1500)/B66 (AWS-3); "
    "4G TDD LTE B38 (2600)/B40 (2300)/B41 (2500); "
    "5G FDD Sub-6 n1 (2100)/n3 (1800)/n5 (850)/n7 (2600)/n8 (900)/n20 (800)/n26 (850)/n28 (700)/n66 (AWS-3)/n71 (600); "
    "5G TDD Sub-6 n38 (2600)/n40 (2300)/n41 (2500)/n77 (3700)/n78 (3500)"
)


def patch_field(item: dict, field_id: str, source_key: str, source_value,
                normalized=None, *, status="VERIFIED", key=None, unit=None,
                note: str, candidate_evidence=None, price_type=None,
                price_observed=None) -> None:
    row = next((entry for entry in item["fields"] if entry["fieldId"] == field_id), None)
    if row is None:
        raise ValueError(f"Missing expected field {field_id}")
    row.update({"sourceId": SOURCES[source_key]["id"], "sourceValue": source_value,
                "normalizedValue": normalized, "status": status, "note": note})
    row.pop("catalogKey", None)
    row.pop("catalogValue", None)
    row.pop("candidateEvidence", None)
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    else:
        row.pop("unit", None)
    if candidate_evidence:
        row["candidateEvidence"] = candidate_evidence
    if price_type:
        row["priceCondition"] = "new"
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed or OBSERVED


def review(config: dict) -> dict:
    item = fe_template.make_review(config)
    wifi = config["network"] == "Wi-Fi"
    product = config["key"]
    exact = (f"Exact local Samsung Philippines Gray SKU {config['sku']} ({config['modelCode']}) "
             f"is listed as 8 GB RAM / 128 GB storage, {config['network']}.")

    patch_field(item, "model_number", product, config["modelCode"], config["modelCode"], note=exact)
    patch_field(item, "configuration", product,
                f"8 GB RAM / 128 GB storage · {config['network']} · Gray",
                f"8 GB RAM / 128 GB storage · {config['network']} · Gray", note=exact)
    patch_field(item, "global_release_date", "global_launch",
                "Samsung announced the series on 2025-04-02; select-market availability began 2025-04-03",
                "2025-04-03", note="Select-market global availability only; Philippine availability is sourced separately.")
    if wifi:
        patch_field(item, "philippine_release_date", "ph_launch",
                    "Samsung PH announced the 5G FE+ 128 GB variant for 2025-05-15; the Wi-Fi SKU's first-sale date is not stated.",
                    status="PENDING_VERIFICATION", note="The local exact Wi-Fi product page confirms the SKU exists, but the dated local announcement names only the FE+ 5G variant.")
        launch_value = "Samsung Newsroom Philippines states FE+ 5G available from PHP 39,990; RAM/storage are not stated in this price story."
        patch_field(item, "official_launch_price_php", "ph_launch_price", launch_value,
                    status="PENDING_VERIFICATION", unit="PHP",
                    note="Historical model/network price context only. The exact initial price for this Wi-Fi 8/128 configuration is not documented.")
    else:
        patch_field(item, "philippine_release_date", "ph_launch",
                    "Samsung Philippines announced Galaxy Tab S10 FE+ 5G (128 GB) availability starting 2025-05-15; RAM is not specified.",
                    "2025-05-15", note="Official local announcement dates the FE+ 5G 128 GB launch. The exact SM-X626B 8/128 SKU is independently listed on Samsung PH.")
        launch_value = "Samsung Newsroom Philippines states FE+ 5G available from PHP 39,990; RAM/storage are not stated in this price story."
        patch_field(item, "official_launch_price_php", "ph_launch_price", launch_value,
                    status="PENDING_VERIFICATION", unit="PHP",
                    note="The local story gives a model/network starting price without RAM/storage; the launch-price field stays blank for this exact SKU.")

    current_price = 47490 if wifi else 52690
    patch_field(item, "current_price_php", "ph_current_price",
                f"Samsung Philippines current SRP for Galaxy Tab S10 FE+ {'Wi-Fi' if wifi else '5G'} (8 GB + 128 GB): PHP {current_price:,}.",
                current_price, unit="PHP", status="VERIFIED",
                price_type="official_current_ph_srp", note="Current exact-configuration manufacturer SRP, observed during the official offer period ending 2026-11-30; not reduced by optional trade-in value.")

    patch_field(item, "display_size", product, "13.1 in (332.8 mm) full rectangle; 13.0 in (330.5 mm) rounded corners", 13.1, key="displayInches", unit="in", note="Samsung Philippines exact-SKU spec page lists 13.1 inches full rectangle and 13.0 inches at rounded corners.")
    patch_field(item, "display_technology", product, "TFT display", "TFT", key="displayType", note="Samsung Philippines lists TFT; secondary IPS-LCD labeling is not substituted for the local manufacturer term.")
    patch_field(item, "display_resolution", product, "2880 x 1800 (WQXGA+)", "2880 x 1800", key="resolution", note="Samsung Philippines exact-SKU specification.")
    patch_field(item, "display_refresh_rate", "global_launch", "LCD, refresh rate up to 90 Hz", 90, key="refreshHz", unit="Hz", note="Samsung's launch specification lists up to 90 Hz; the conflicting 120 Hz claim on Kimovil is not used.")
    patch_field(item, "display_brightness", product, "600 nits maximum; 800 nits outdoor High Brightness Mode", 600, unit="nits", note="Samsung Philippines specifies 600 nits maximum and 800 nits outdoor HBM; the two modes are kept distinct.")
    patch_field(item, "display_protection", product, "Samsung Philippines does not identify a screen-cover glass material or version.", status="NOT_DISCLOSED", note="No Gorilla Glass generation or other panel-cover material is inferred from secondary listings, which conflict.")
    patch_field(item, "chipset", "global_launch", "Samsung Exynos 1580", "Samsung Exynos 1580", key="chipset", note="Samsung's launch table identifies Exynos 1580 for the FE+ model family.")
    patch_field(item, "process_node", "exynos", "Samsung Exynos 1580, third-generation 4 nm EUV FinFET", 4, unit="nm", note="Samsung Semiconductor specifies its 4 nm EUV FinFET process.")
    patch_field(item, "cpu", "exynos", "1 x Cortex-A720 up to 2.9 GHz; 3 x Cortex-A720 up to 2.6 GHz; 4 x Cortex-A520 up to 1.95 GHz", "Octa-core: 1 x Cortex-A720 2.9 GHz + 3 x Cortex-A720 2.6 GHz + 4 x Cortex-A520 1.95 GHz", key="cpu", note="Samsung Exynos 1580 architecture; the Samsung PH device page also lists CPU clocks 2.9/2.6/1.9 GHz.")
    patch_field(item, "gpu", "exynos", "Samsung Xclipse 540 GPU", "Samsung Xclipse 540", key="gpu", note="Samsung Semiconductor identifies Xclipse 540 graphics for Exynos 1580.")
    patch_field(item, "operating_system", "annual_report", "Android 15, One UI 7.0 at launch", "Android 15", key="os", note="Samsung Electronics' 2025 report lists Android 15 / One UI 7.0 for Tab S10 FE and FE+ at launch; later OS versions are not substituted.")
    patch_field(item, "os_support", "security", "Samsung lists security-update period valid until 30 April 2032", "Security updates listed through 2032-04-30", note="Manufacturer support-period endpoint; no OS-generation count is inferred.")
    patch_field(item, "ram_capacity", product, "8 GB", 8, key="ramGb", unit="GB", note=exact)
    patch_field(item, "ram_type", "nanoreview", "LPDDR5X; NanoReview displays the 8 GB / 128 GB option", "LPDDR5X", status="VERIFIED_SECONDARY", note="Secondary model-family data matches the selected 8/128 configuration; Samsung PH does not publish RAM technology.")
    patch_field(item, "storage_capacity", product, "128 GB internal storage", 128, key="storageGb", unit="GB", note=exact)
    patch_field(item, "storage_type", "nanoreview", "UFS 3.1; NanoReview displays the 8 GB / 128 GB option", "UFS 3.1", status="VERIFIED_SECONDARY", note="Secondary model-family data for the selected 8/128 configuration; Samsung PH does not publish storage-interface type.")
    patch_field(item, "storage_expansion", product, "MicroSD card support up to 2 TB", "microSD up to 2 TB", note="Samsung Philippines and Samsung's global launch materials list expansion up to 2 TB.")
    patch_field(item, "rear_camera_system", product, "Single 13 MP autofocus rear camera", 13, key="rearCameraMp", unit="MP", note="Samsung Philippines lists a 13 MP rear camera with autofocus; Samsung's launch table lists one rear camera.")
    patch_field(item, "main_camera_sensor", product, "Samsung does not disclose the rear-camera sensor component.", status="NOT_DISCLOSED", note="No sensor part number, type or aperture is inferred from camera resolution.")
    patch_field(item, "ultrawide_camera", "global_launch", "Samsung lists one 13 MP rear camera and no rear ultra-wide module.", "No rear ultra-wide camera", status="NOT_APPLICABLE", note="Samsung's FE+ launch specification names a single rear camera; no rear ultra-wide camera is listed.")
    patch_field(item, "telephoto_camera", "global_launch", "Samsung lists one 13 MP rear camera and no telephoto module.", "No telephoto camera", status="NOT_APPLICABLE", note="Samsung's FE+ launch specification names a single rear camera; no telephoto camera is listed.")
    patch_field(item, "front_camera", "global_launch", "12 MP ultra-wide front camera", 12, key="frontCameraMp", unit="MP", note="Samsung's global launch table identifies the front module as 12 MP ultra-wide.")
    patch_field(item, "video_recording", product, "Rear video recording up to UHD 4K (3840 x 2160) at 30 fps", "Rear video up to 4K / 30 fps", key="video", note="Samsung Philippines exact-SKU specification.")
    patch_field(item, "battery_capacity", product, "10,090 mAh typical capacity", 10090, key="batteryMah", unit="mAh", note="Samsung Philippines labels 10,090 mAh as typical capacity; a rated/minimum capacity is not supplied.")
    chemistry_evidence = [
        {"value": "Li-Ion", "sourceUrl": SOURCES["nanoreview"]["url"], "sourceKind": "secondary_specification", "observedAt": OBSERVED,
         "excerpt": "NanoReview lists battery type Li-Ion.", "configurationMatch": "Galaxy Tab S10 FE+ model-level; chemistry/sample not stated by Samsung", "reviewStatus": "CONFLICTING_INFORMATION"},
        {"value": "Li-Polymer", "sourceUrl": SOURCES["kimovil"]["url"], "sourceKind": "secondary_specification", "observedAt": OBSERVED,
         "excerpt": "Kimovil lists battery type Li-Polymer.", "configurationMatch": "Global Galaxy Tab S10 FE+ model page; no local battery variant identified", "reviewStatus": "CONFLICTING_INFORMATION"},
    ]
    patch_field(item, "battery_technology", "nanoreview", "NanoReview says Li-Ion; Kimovil says Li-Polymer; Samsung does not disclose chemistry.", status="CONFLICTING_INFORMATION", note="Secondary sources conflict, and Samsung does not identify cell chemistry. Value withheld.", candidate_evidence=chemistry_evidence)
    patch_field(item, "wired_charging", "global_launch", "45 W wired charging; compatible 45 W power adapter sold separately", 45, key="chargingW", unit="W", note="Samsung global launch specification lists 45 W and says the adapter is sold separately.")
    patch_field(item, "wireless_charging", "nanoreview", "NanoReview lists no wireless charging.", "No wireless charging", status="VERIFIED_SECONDARY", note="Samsung PH does not enumerate this feature; secondary specification only, not presented as a manufacturer claim.")
    patch_field(item, "dimensions", product, "194.7 x 300.6 x 6.0 mm (H x W x D)", "194.7 x 300.6 x 6.0 mm", key="dimensions", unit="mm", note="Samsung Philippines physical specification.")
    patch_field(item, "weight", product, f"{config['weight']} g ({config['network']} model)", config["weight"], key="weightG", unit="g", note="Samsung Philippines lists 664 g for Wi-Fi and 668 g for the 5G model.")
    patch_field(item, "materials", "nanoreview", "Metal rear body and metal frame; Kimovil describes an aluminium-alloy frame.", "Metal body/frame", status="VERIFIED_SECONDARY", note="Two secondary descriptions support metal construction; exact alloy composition is not assigned from these sources.")
    patch_field(item, "ingress_protection", product, "IP68; lab submersion up to 1.5 m freshwater for up to 30 minutes", "IP68", note="Samsung Philippines states IP68 and its stated laboratory conditions.")
    if wifi:
        patch_field(item, "sim_esim", product, "Exact SM-X620N SKU is Wi-Fi only; no SIM/eSIM.", "No SIM; Wi-Fi only", key="sim", note=exact)
        patch_field(item, "cellular_bands", product, "Not applicable to the Wi-Fi-only SM-X620N SKU.", status="NOT_APPLICABLE", note="Samsung identifies this exact SKU as Wi-Fi-only; no cellular bands are assigned.")
        patch_field(item, "tablet_cellular_variant", product, "Wi-Fi-only variant", "Wi-Fi only", key="cellular", note=exact)
    else:
        patch_field(item, "sim_esim", product, "Dual-SIM: SIM 1 + embedded SIM + MicroSD; availability may vary by country/carrier.", "Nano-SIM + eSIM", key="sim", note="Samsung Philippines exact 5G SKU page lists Dual-SIM, SIM 1 + embedded SIM + MicroSD.")
        patch_field(item, "cellular_bands", product, CELLULAR_BANDS, CELLULAR_BANDS, note="Bands transcribed from Samsung Philippines' SM-X626B 5G specification page.")
        patch_field(item, "tablet_cellular_variant", product, "5G cellular variant", "5G cellular", key="cellular", note=exact)
    patch_field(item, "wifi", product, "802.11a/b/g/n/ac/ax, 2.4 GHz + 5 GHz, HE80, MIMO, 1024-QAM (Wi-Fi 6)", "Wi-Fi 6", key="wifi", note="Samsung Philippines lists 802.11ax; do not upgrade to Wi-Fi 6E based on a secondary global listing.")
    patch_field(item, "bluetooth", product, "Bluetooth 5.3", "Bluetooth 5.3", note="Samsung Philippines exact-SKU specification.")
    patch_field(item, "usb", product, "USB Type-C, USB 2.0", "USB Type-C; USB 2.0", key="ports", note="Samsung Philippines lists USB 2.0 and USB Type-C.")
    patch_field(item, "nfc", product, "NFC: No", "No NFC", note="Samsung Philippines exact-SKU specification.")
    patch_field(item, "gnss", product, "GPS, GLONASS, BeiDou, Galileo and QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS", note="Samsung Philippines lists location technologies.")
    patch_field(item, "audio", "nanoreview", "Four-speaker audio and Dolby Atmos; Kimovil also lists stereo speakers and Dolby Atmos.", "4 speakers; Dolby Atmos", status="VERIFIED_SECONDARY", key="sound", note="Secondary model-level cross-check; Samsung PH product page does not specify speaker count.")
    patch_field(item, "sensors", product, "Accelerometer, fingerprint sensor, gyroscope, geomagnetic sensor, Hall sensor and light sensor", "Accelerometer; fingerprint; gyroscope; geomagnetic; Hall; light", note="Samsung Philippines exact-SKU sensor list.")
    patch_field(item, "tablet_stylus", product, "S Pen included with the Galaxy Tab S10 FE+", "S Pen included", key="stylus", note="Samsung Philippines lists the tablet with S Pen; S Pen is included with the product.")
    patch_field(item, "tablet_keyboard", product, "Book Cover Keyboard and Book Cover Keyboard Slim supported; sold separately", "Book Cover Keyboard supported; sold separately", key="keyboard", note="Samsung Philippines product page lists both keyboard accessories as sold separately.")

    # This generic FE template carries Samsung S9 FE source references; replace
    # them with the exact S10 FE+ evidence set before saving.
    item["sources"] = list(SOURCES.values())
    item["availabilityEvidence"] = {
        "verificationStatus": "VERIFIED_OFFICIAL_LAUNCH",
        "availabilityStatus": "Samsung Philippines announced FE+ 5G 128 GB availability beginning 2025-05-15 and now lists exact 8/128 Gray Wi-Fi and 5G product SKUs. Current official SRP is listed through 2026-11-30; checkout stock was not checked.",
        "philippineAvailabilityDate": "2025-05-15", "philippineDateLabel": "Philippine launch date",
        "philippineAvailability": "Samsung Philippines announced local availability for Galaxy Tab S10 FE+ 5G (128 GB) from 2025-05-15. Current Samsung Philippines product pages identify Gray 8/128 Wi-Fi (SM-X620NZAAXTC) and 5G (SM-X626BZAAXTC) SKUs. The first local sale date for the Wi-Fi SKU and exact Philippine 12/256 SKUs were not verified.",
        "observedAt": OBSERVED, "philippineReleaseYear": 2025, "catalogModel": MODEL,
        "qualityFlag": "Two exact local 8/128 SKUs reviewed; Wi-Fi first-sale date, exact launch prices, PH 12/256 availability and battery chemistry remain unresolved.",
        "openIssues": [
            {"issue": "Samsung's dated local availability announcement names the FE+ 5G 128 GB variant; an exact first-sale date for Wi-Fi is not documented.", "action": "Keep the Wi-Fi configuration date blank until dated local availability evidence is found."},
            {"issue": "Global materials mention 12 GB / 256 GB, but explicitly warn memory options vary by market; no exact PH 12/256 SKU was located.", "action": "Do not add the 12/256 configuration to the Philippine catalog without local SKU or authorized local listing evidence."},
            {"issue": "Samsung Newsroom gives FE+ 5G from PHP 39,990 without RAM/storage; an exact initial launch price for each 8/128 SKU remains unverified. A July 2025 exact 5G 8/128 SRP and current 2026 SRPs are separately sourced.", "action": "Keep exact-configuration launch-price fields blank; retain dated exact and model/network price observations."},
            {"issue": "Samsung does not identify display cover glass or battery chemistry. NanoReview and Kimovil disagree on battery chemistry; Kimovil also reports refresh/brightness values inconsistent with Samsung's exact local specifications.", "action": "Leave the screen-cover material undisclosed and battery chemistry unresolved; prefer Samsung's local display measurements."},
        ],
    }
    item["replacementVariants"] = [
        {"id": c["id"], "label": f"{c['ram']} GB RAM / {c['storage']} GB storage · {c['network']} · Gray",
         "sku": c["sku"], "modelCode": c["modelCode"],
         "notes": f"Exact local Gray {c['network']} 8/128 SKU listed by Samsung Philippines."}
        for c in CONFIGS
    ]
    return item


def price_rows() -> list[dict]:
    rows = []
    for c in CONFIGS:
        amount = 47490 if c["network"] == "Wi-Fi" else 52690
        rows.append({
            "device_id": DEVICE, "configuration_id": c["id"], "variant_ram_gb": 8,
            "variant_storage_gb": 128, "variant_connectivity": c["network"],
            "configuration_match": f"exact_8gb_128gb_{'wifi' if c['network'] == 'Wi-Fi' else '5g'}",
            "amount_php": amount, "price_type": "current_official_ph_srp_2026-11",
            "source_published_at": None, "observed_at": OBSERVED,
            "source_url": SOURCES["ph_current_price"]["url"],
            "source_kind": "official_samsung_ph_current_srp",
            "local_availability_verified": True,
            "availability_status": "current_official_srp_listed_through_2026-11-30; stock_not_checked",
            "review_status": "VERIFIED",
            "excerpt": f"Samsung Philippines lists Galaxy Tab S10 FE+ {c['network']} (8 GB + 128 GB) at SRP PHP {amount:,}; the page lists maximum trade-in offer separately.",
        })
    rows.extend([
        {
            "device_id": DEVICE, "configuration_id": CONFIGS[1]["id"], "variant_ram_gb": 8,
            "variant_storage_gb": 128, "variant_connectivity": "5G",
            "configuration_match": "exact_8gb_128gb_5g",
            "amount_php": 39990, "price_type": "historical_ph_official_srp_exact_configuration_2025-07_to_09",
            "source_published_at": None, "observed_at": OBSERVED,
            "source_url": SOURCES["ph_history_price"]["url"],
            "source_kind": "official_samsung_ph_historical_srp",
            "local_availability_verified": True,
            "availability_status": "expired_campaign_2025-07-01_to_2025-09-30_not_current",
            "review_status": "VERIFIED",
            "excerpt": "Samsung Philippines' expired offer table explicitly lists Galaxy Tab S10 FE+ 5G (8 GB + 128 GB) SRP PHP 39,990. Trade-in savings are separate; this is not a current price.",
        },
        {
            "device_id": DEVICE, "configuration_id": None, "variant_ram_gb": None,
            "variant_storage_gb": 128, "variant_connectivity": "5G",
            "configuration_match": "model_network_5g_storage_128_ram_unspecified",
            "amount_php": 39990, "price_type": "historical_ph_launch_story_starting_price_ram_unspecified",
            "source_published_at": None, "observed_at": OBSERVED,
            "source_url": SOURCES["ph_launch_price"]["url"],
            "source_kind": "official_samsung_ph_news_price_context",
            "local_availability_verified": True,
            "availability_status": "historical_model_network_price_context_not_exact_ram",
            "review_status": "VERIFIED",
            "excerpt": "Samsung Newsroom Philippines reported the FE+ 5G as available from PHP 39,990; the story does not state RAM/storage, so it is model/network context only.",
        },
    ])
    return rows


def update_image_review() -> None:
    sources = json.loads(IMAGE_SOURCES.read_text(encoding="utf-8"))
    sources = [row for row in sources if row.get("deviceId") != DEVICE]
    sources.append({
        "deviceId": DEVICE,
        "pageUrl": SOURCES["image_press"]["url"],
        "method": "direct",
        "assetUrl": "https://api.samsungmobilepress.com/file/EB6857FDFA1B6B9982B8D02D52E9D86D89786A4BD56539C90499353889BE4DBAE0D08FE9DE370AF57182E01450A1E6B4DDF6E44FDD3477FEF9ACE2C8C9A512C8ECBAF76F8224BFAA856AD6AF3A8DB2F487EC68CB22CAC28E422E6663CE635A077B6149229543867DF10BC3C7B86BC0FF7F07E96B3BBE6DBEC7B987A99C4EBB2401F5801CAFE687AA0865B5F66281D364",
        "rightsStatus": "LICENSED",
        "licenseUrl": SOURCES["image_terms"]["url"],
        "usageTerms": "Samsung Mobile Press Terms of Use: personal, informational and non-commercial use only; preserve copyright, trademark and proprietary notices; no commercial use is granted.",
        "credit": "Samsung Electronics Co., Ltd. via Samsung Mobile Press",
        "scope": "Exact Galaxy Tab S10 FE+ Gray front product image; memory/storage and Wi-Fi/5G configuration are not visually distinguishable.",
        "changes": "Converted to WebP and resized for catalog display without cropping; no product edits or notice removal.",
        "rightsCheckedAt": OBSERVED,
    })
    IMAGE_SOURCES.write_text("[\n" + ",\n".join(
        "  " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in sources
    ) + "\n]\n", encoding="utf-8")
    unavailable = json.loads(IMAGE_UNAVAILABLE.read_text(encoding="utf-8"))
    unavailable.pop(DEVICE, None)
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    fe_template.DEVICE = DEVICE
    fe_template.MODEL = MODEL
    fe_template.OBSERVED = OBSERVED
    fe_template.UNRECORDED = UNRECORDED
    fe_template.CONFIGS = CONFIGS
    fe_template.CELLULAR_BANDS = CELLULAR_BANDS

    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Included" or device.get("workbookRow") != 443:
        raise ValueError("Expected the Included workbook row 443 Galaxy Tab S10 FE+ record; refusing unexpected target.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {c["id"] for c in CONFIGS}
    if current_ids not in ({UNRECORDED}, expected_ids):
        raise ValueError(f"Unexpected S10 FE+ configurations; refusing to overwrite: {sorted(current_ids)}")

    targets = {(DEVICE, c["id"]) for c in CONFIGS}
    for config in CONFIGS:
        add_review(manual, catalog, review(config))
    deduplicate_target_reviews(manual, targets)
    for index, config in enumerate(CONFIGS):
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, config["id"]))
        if index:
            for key in ("replacementVariants", "replaceUnrecordedPlaceholder", "additionalVariants"):
                saved.pop(key, None)
        label = f"8 GB RAM / 128 GB storage · {config['network']} · Gray"
        saved.update({"brand": "Samsung", "model": MODEL, "configuration": label, "configurationLabel": label,
                      "sources": list(SOURCES.values())})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    update_image_review()
    prices = price_rows()
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Samsung", "model_name": MODEL,
                    "category": "tablets", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": s["url"], "source_kind": s["purpose"],
                       "status": "reviewed", "result": s["note"]} for s in SOURCES.values()],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    model = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if model:
        model["status"] = "manually_reviewed"
    known = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type"), p.get("source_url"), p.get("configuration_match")) for p in latest.get("prices", [])}
    for price in prices:
        key = (price["device_id"], price["configuration_id"], price["price_type"], price["source_url"], price["configuration_match"])
        if key in known:
            next(p for p in latest["prices"] if (p.get("device_id"), p.get("configuration_id"), p.get("price_type"), p.get("source_url"), p.get("configuration_match")) == key).update(price)
        else:
            latest.setdefault("prices", []).append(price)
            known.add(key)
    latest["run_at"] = OBSERVED
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "model": MODEL, "workbookRow": 443,
        "configurations": [{"sku": c["sku"], "modelCode": c["modelCode"], "ramGb": c["ram"],
                            "storageGb": c["storage"], "network": c["network"],
                            "currentSrpPhp": 47490 if c["network"] == "Wi-Fi" else 52690}
                           for c in CONFIGS],
        "reviewedConfigurations": len(CONFIGS), "reviewedFieldsPerConfiguration": 49,
        "unresolved": ["Wi-Fi first-sale date", "exact 8/128 launch prices", "12/256 PH SKU", "screen-cover glass", "battery chemistry"],
        "image": "Samsung Mobile Press exact-model Gray product image; educational non-commercial use terms and credit recorded",
        "priceObservations": len(prices),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
