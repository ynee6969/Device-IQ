#!/usr/bin/env python3
"""Add source-backed Philippine configuration reviews for Galaxy Tab S9 FE+."""
from __future__ import annotations

import json
from pathlib import Path

import add_verified_samsung_tab_s9_fe_review as fe_template
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-tab-s9-fe-plus-ph-prices-2026-11-27.json"
IMAGE_SOURCES = ROOT / "research/catalog-image-sources.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-27"
DEVICE = "device_ca40d8c136e83b"
MODEL = "Galaxy Tab S9 FE+"
UNRECORDED = f"{DEVICE}-unrecorded"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = {
    "wifi": src(
        "samsung_tab_s9_fe_plus_ph_wifi_128_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-fe-plus-wifi-gray-128gb-sm-x610nzaaxtc/",
        "Samsung Philippines", "Exact Philippine Wi-Fi SKU and configuration specifications",
        "Samsung Philippines identifies the Gray Wi-Fi SKU SM-X610NZAAXTC, with 8 GB RAM and 128 GB storage, and lists its hardware specifications."),
    "5g": src(
        "samsung_tab_s9_fe_plus_ph_5g_128_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-fe-plus-5g-gray-128gb-sm-x616bzaaxtc/",
        "Samsung Philippines", "Exact Philippine 5G SKU and configuration specifications",
        "Samsung Philippines identifies the Gray 5G SKU SM-X616BZAA XTC, with 8 GB RAM and 128 GB storage, and lists its hardware and cellular-band specifications."),
    "wifi_buy": src(
        "samsung_tab_s9_fe_plus_ph_wifi_buy_tool",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s9-fe/buy/?modelCode=SM-X610NZAAXTC",
        "Samsung Philippines", "Local SKU and purchase-option cross-check for Wi-Fi model",
        "The Samsung Philippines buying tool is keyed to the local Wi-Fi SKU; it supports local SKU matching but currently exposes no numeric price."),
    "5g_buy": src(
        "samsung_tab_s9_fe_plus_ph_5g_buy_tool",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s9-fe/buy/?modelCode=SM-X616BZAAXTC",
        "Samsung Philippines", "Local SKU, purchase-option and in-box items cross-check for 5G model",
        "The Samsung Philippines buying tool identifies the 8 GB / 128 GB 5G Gray SKU, lists the tablet, S Pen, data cable and eject pin in the box, and states no travel adapter is included; it exposes no current numeric price."),
    "ph_launch": src(
        "samsung_tab_s9_fe_plus_ph_launch_availability",
        "https://news.samsung.com/ph/samsung-galaxy-s23-fe-galaxy-tab-s9-fe-and-galaxy-buds-fe-bring-standout-features-to-even-more-users",
        "Samsung Newsroom Philippines", "Official Philippine launch date for the Galaxy Tab S9 FE series",
        "Samsung Philippines announced that the Galaxy Tab S9 FE series, including FE+, would be available locally beginning October 20, 2023.",
        "2023-10-11"),
    "ph_prices_2023": src(
        "samsung_tab_s9_fe_plus_ph_2023_home_credit",
        "https://www.samsung.com/ph/offer/offline/2023/galaxy-fe-series-home-credit/",
        "Samsung Philippines", "Historical Philippine cash price for exact 8 GB / 128 GB 5G configuration",
        "The Home Credit cash-price table explicitly lists Galaxy Tab S9 FE+ 5G (8 GB + 128 GB) at PHP 39,990. The campaign ran October 1 to December 31, 2023; this is historical, not a current price.",
        None),
    "ph_prices_2023_online": src(
        "samsung_tab_s9_fe_plus_ph_2023_online_srp",
        "https://www.samsung.com/ph/offer/online/2023/galaxy-tab-s9-fe/",
        "Samsung Philippines", "Historical model/network-level SRP for FE+ Wi-Fi and 5G",
        "Samsung's expired October 20–December 31, 2023 promotion lists SRP PHP 34,990 for FE+ Wi-Fi and PHP 39,990 for FE+ 5G, but does not state RAM or storage; retained only as model/network-level price evidence.",
        None),
    "ph_prices_2024": src(
        "samsung_tab_s9_fe_plus_ph_2024_home_credit_prices",
        "https://www.samsung.com/ph/offer/offline/2024/galaxy-devices-home-credit-offer/",
        "Samsung Philippines", "Historical model/network-level 2024 price observations",
        "The Samsung Philippines Home Credit table lists PHP 34,990 for Galaxy Tab S9 FE+ Wi-Fi and PHP 39,990 for FE+ 5G, without RAM or storage details. These are historical model/network-level observations, not current prices."),
    "ph_prices_2025": src(
        "samsung_tab_s9_fe_plus_ph_2025_trade_in_prices",
        "https://www.samsung.com/ph/offer/offline/2025/galaxy-tab-trade-in/",
        "Samsung Philippines", "Expired model/network-level 2025 SRP and offer for FE+ 5G",
        "Samsung's expired trade-in page lists FE+ 5G SRP PHP 43,990 and offer PHP 39,990, valid July 9–September 30, 2025. The table does not specify RAM or storage; neither value is current or attached to an exact configuration.",
        None),
    "global_launch": src(
        "samsung_tab_s9_fe_plus_global_launch",
        "https://news.samsung.com/global/samsung-galaxy-s23-fe-galaxy-tab-s9-fe-and-galaxy-buds-fe-bring-standout-features-to-even-more-users",
        "Samsung Global Newsroom", "Global announcement and selected-market availability context",
        "Samsung announced the FE family on October 4, 2023 and stated selected-market availability from October 5. This is not a Philippine release date.",
        "2023-10-04"),
    "exynos": src(
        "samsung_exynos_1380_official_specs",
        "https://semiconductor.samsung.com/processor/mobile-processor/exynos-1380/",
        "Samsung Semiconductor", "Exynos 1380 CPU, process and GPU details",
        "Samsung lists the Exynos 1380 5 nm process, four Cortex-A78 cores up to 2.4 GHz, four Cortex-A55 cores up to 2.0 GHz and Mali-G68 graphics with five cores."),
    "us_specs": src(
        "samsung_tab_s9_fe_plus_us_launch_spec_sheet",
        "https://image-us.samsung.com/SamsungUS/home/my-assets/10-11-23/TabS9FE-Spec.pdf",
        "Samsung US", "Manufacturer cross-check for launch OS, speakers and wired-charger requirement",
        "Samsung's launch spec sheet covers the FE+ model family, lists Android 13, stereo speakers with Dolby Atmos and says a separately sold 45 W wall charger is required. This is not Philippine availability or pricing evidence.",
        "2023-10-11"),
    # Temporary key used by the older shared FE field template. The resulting
    # wireless-charge row is replaced with the direct NanoReview/Kimovil sources
    # and this placeholder is removed before the record is saved.
    "samsung_de": src(
        "samsung_tab_s9_fe_samsung_de_comparison",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-fe-plus-wifi-gray-128gb-sm-x610nzaaxtc/",
        "Samsung Philippines", "Temporary shared-template source key; not saved",
        "Replaced in the FE+ field review with FE+ secondary-source evidence."),
    "nanoreview": src(
        "nanoreview_tab_s9_fe_plus_specs",
        "https://nanoreview.net/en/tablet/samsung-galaxy-tab-s9-fe-plus",
        "NanoReview", "Secondary model-family specification cross-check",
        "NanoReview lists LPDDR4X, UFS 2.2, 90 Hz, Gorilla Glass 3, 45 W charging, no wireless charging and Li-Ion chemistry. The page's selected RAM detail defaults to 6 GB even though its selector lists 8/128 and 12/256; the RAM type is therefore not assigned to the local 8 GB SKU. Its battery chemistry conflicts with Kimovil."),
    "kimovil": src(
        "kimovil_tab_s9_fe_plus_specs",
        "https://www.kimovil.com/en/where-to-buy-samsung-galaxy-tab-s9-fe-plus-5g",
        "Kimovil", "Secondary 8 GB / 128 GB 5G model cross-check",
        "Kimovil lists the global 8 GB / 128 GB 5G model, dimensions, Exynos 1380, 10,090 mAh battery, 45 W charging and Li-Polymer chemistry. Its chemistry claim conflicts with NanoReview, and global configuration/pricing does not establish Philippine sale."),
    "gsmarena": src(
        "gsmarena_tab_s9_fe_plus_access_attempt",
        "https://www.gsmarena.com/samsung_galaxy_tab_s9_fe_plus-12609.php",
        "GSMArena", "Independent specification cross-check access attempt",
        "GSMArena search identifies model ID 12609. The direct specification page could not be fetched in this research session, and its comparison page returned HTTP 402. No specification values were copied from GSMArena."),
    "image_product": src(
        "samsung_tab_s9_fe_plus_ph_gray_product_image_candidate",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-fe-plus-5g-gray-128gb-sm-x616bzaaxtc/",
        "Samsung Philippines", "Exact-model product image candidate; not reused",
        "Samsung's exact Philippine Gray 5G product page shows the Galaxy Tab S9 FE+. Product art is a model match, but reuse rights were not cleared for this catalog."),
    "image_press": src(
        "samsung_mobile_press_tab_s9_fe_plus_gallery",
        "https://www.samsungmobilepress.com/media-assets/galaxy-tab-s9-fe-plus?tab=images",
        "Samsung Mobile Press", "Exact-model product-image gallery and usage-rights review",
        "The media gallery includes exact-model product assets. Samsung Mobile Press terms permit use only for personal, informational and non-commercial purposes and require proprietary notices to remain intact. The DeviceIQ thesis catalog is treated as informational and non-commercial; source credit and terms are preserved with the image."),
    "image_terms": src(
        "samsung_mobile_press_image_terms",
        "https://www.samsungmobilepress.com/terms",
        "Samsung Mobile Press", "Product-image reuse terms",
        "Samsung Mobile Press terms allow personal, informational and non-commercial use only; they do not grant commercial rights. Do not remove or alter any copyright, trademark or proprietary notice."),
    "commons": src(
        "commons_samsung_galaxy_tab_image_search",
        "https://commons.wikimedia.org/wiki/Category:Samsung_Galaxy_Tab",
        "Wikimedia Commons", "Search for exact-model reusable product photography",
        "A search for Galaxy Tab S9 FE+ exact-model product photography did not identify a suitable openly licensed product image. The broad Galaxy Tab category is not evidence of an exact-model photo or license."),
}

CONFIGS = [
    {"id": f"{DEVICE}-sm-x610n-8gb-128gb-wifi-ph", "key": "wifi",
     "modelCode": "SM-X610N", "sku": "SM-X610NZAAXTC", "ram": 8,
     "storage": 128, "network": "Wi-Fi", "weight": 627, "launch": 34990},
    {"id": f"{DEVICE}-sm-x616b-8gb-128gb-5g-ph", "key": "5g",
     "modelCode": "SM-X616B", "sku": "SM-X616BZAAXTC", "ram": 8,
     "storage": 128, "network": "5G", "weight": 628, "launch": 39990},
]

CELLULAR_BANDS = (
    "2G GSM 850/900/1800/1900; 3G UMTS B1/B2/B4/B5/B8; "
    "4G FDD LTE B1/B2/B3/B4/B5/B7/B8/B12/B13/B17/B20/B26/B28/B32/B66; "
    "4G TDD LTE B38/B40/B41; 5G FDD Sub-6 n1/n3/n5/n7/n8/n20/n28/n66; "
    "5G TDD Sub-6 n38/n40/n41/n77/n78"
)


def patch_field(item: dict, field_id: str, source_key: str, source_value,
                normalized=None, *, status="VERIFIED", key=None, unit=None,
                note: str, candidate_evidence=None) -> None:
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


def review(config: dict) -> dict:
    item = fe_template.make_review(config)
    wifi = config["network"] == "Wi-Fi"
    product_source = config["key"]
    buy_source = "wifi_buy" if wifi else "5g_buy"
    exact = f"Exact local Samsung Philippines SKU {config['sku']} ({config['modelCode']}) is listed as Gray, 8 GB RAM / 128 GB storage, {config['network']}."

    # The shared FE tablet template supplies the complete tablet audit field set.
    # Override every value that differs on the FE+ and keep the template limited
    # to structure only.
    patch_field(item, "model_number", product_source, config["modelCode"], config["modelCode"], note=exact)
    patch_field(item, "configuration", product_source,
                f"8 GB RAM / 128 GB storage · {config['network']} · Gray",
                f"8 GB RAM / 128 GB storage · {config['network']} · Gray", note=exact)
    patch_field(item, "global_release_date", "global_launch",
                "Samsung announced the FE family 2023-10-04; selected-market availability began 2023-10-05",
                "2023-10-05", note="Selected-market availability only; not the Philippine launch date.")
    patch_field(item, "philippine_release_date", "ph_launch",
                "Samsung Philippines announced FE series availability starting 2023-10-20",
                "2023-10-20", note="Official Samsung Philippines series launch date; not an inferred global date.")
    if wifi:
        patch_field(item, "official_launch_price_php", "ph_prices_2023_online",
                    "Samsung Philippines listed PHP 34,990 SRP for Galaxy Tab S9 FE+ Wi-Fi; RAM/storage are not stated in this price table.",
                    status="PENDING_VERIFICATION", unit="PHP",
                    note="Model/network-level historical SRP only. The official product page lists a local 8/128 SKU, but the price table does not connect its amount to a memory configuration; do not present this as an exact-config launch price.")
    else:
        patch_field(item, "official_launch_price_php", "ph_prices_2023",
                    "Samsung Philippines lists PHP 39,990 cash price for Galaxy Tab S9 FE+ 5G (8 GB + 128 GB)",
                    39990, unit="PHP",
                    note="Historical 2023 local campaign cash price explicitly tied to the 8 GB / 128 GB 5G configuration; not a current offer.")
    patch_field(item, "current_price_php", product_source,
                "No current numeric exact-SKU Philippine cash price was verifiable on 2026-11-27.",
                status="PENDING_VERIFICATION", unit="PHP",
                note="Samsung's current Philippines product/buy pages identify the SKU but expose no numeric price. Historical campaign prices are retained separately.")

    patch_field(item, "display_size", product_source,
                "12.4 inches (315.0 mm), full rectangle; 12.4 inches accounting for rounded corners",
                12.4, key="displayInches", unit="in",
                note="Samsung Philippines lists 12.4 inches; its page says 12.4 inches both for the full rectangle and rounded-corner measurement.")
    patch_field(item, "display_technology", product_source, "TFT display", "TFT", key="displayType", note="Samsung Philippines lists TFT technology.")
    patch_field(item, "display_resolution", product_source, "2560 x 1600 (WQXGA)", "2560 x 1600", key="resolution", note="Samsung Philippines specification for the 12.4-inch FE+ panel.")
    patch_field(item, "display_refresh_rate", product_source, "Refresh rate up to 90 Hz", 90, key="refreshHz", unit="Hz", note="Samsung Philippines advertises a 90 Hz display for the FE+ model family.")
    brightness_evidence = [
        {"value": "600 nits maximum; 720 nits outdoor High Brightness Mode", "unit": "nits",
         "sourceUrl": SOURCES[product_source]["url"], "sourceKind": "official_manufacturer",
         "observedAt": OBSERVED, "excerpt": "Samsung Philippines lists maximum brightness of 600 nits and outdoor brightness of 720 nits in High Brightness Mode.",
         "configurationMatch": "Exact Galaxy Tab S9 FE+ local SKU family; brightness-mode definition stated", "reviewStatus": "CONFLICTING_INFORMATION"},
        {"value": "800 nits max rated brightness", "unit": "nits",
         "sourceUrl": SOURCES["nanoreview"]["url"], "sourceKind": "secondary_specification",
         "observedAt": OBSERVED, "excerpt": "NanoReview lists 800 nits max rated brightness and cites NotebookCheck elsewhere on its page.",
         "configurationMatch": "Galaxy Tab S9 FE+ model level; test/mode definition differs or is unspecified", "reviewStatus": "CONFLICTING_INFORMATION"},
    ]
    patch_field(item, "display_brightness", product_source,
                "Samsung Philippines: 600 nits maximum / 720 nits outdoor HBM; NanoReview: 800 nits max-rated",
                status="CONFLICTING_INFORMATION", unit="nits",
                note="Withheld because Samsung's manufacturer brightness modes and NanoReview's max-rated figure are not reconciled to the same test condition.",
                candidate_evidence=brightness_evidence)
    patch_field(item, "display_protection", "nanoreview", "Corning Gorilla Glass 3", "Corning Gorilla Glass 3",
                status="VERIFIED_SECONDARY", note="NanoReview lists Gorilla Glass 3; Samsung Philippines does not name the glass version on its local specifications page.")
    patch_field(item, "chipset", product_source, "Samsung Exynos 1380", "Samsung Exynos 1380", key="chipset", note="Samsung Philippines identifies Exynos 1380 for the FE+ family.")
    patch_field(item, "process_node", "exynos", "Samsung Exynos 1380, 5 nm FinFET", 5, unit="nm", note="Samsung Semiconductor's Exynos 1380 specification.")
    patch_field(item, "cpu", "exynos", "4 x Cortex-A78 up to 2.4 GHz + 4 x Cortex-A55 up to 2.0 GHz",
                "Octa-core: 4 x Cortex-A78 up to 2.4 GHz + 4 x Cortex-A55 up to 2.0 GHz", key="cpu", note="Samsung Semiconductor CPU configuration for Exynos 1380.")
    patch_field(item, "gpu", "exynos", "Arm Mali-G68 GPU, five cores", "Arm Mali-G68 MP5", key="gpu", note="Samsung Semiconductor identifies the Exynos 1380 GPU as Mali-G68 with five cores.")
    patch_field(item, "operating_system", "us_specs", "Android 13 at launch", "Android 13", key="os", note="Samsung launch specification; current OS versions are not substituted for launch OS.")
    patch_field(item, "os_support", "global_launch", "Four generations of Android OS upgrades and five years of security updates",
                "Up to 4 OS generations; 5 years of security updates", note="Samsung's launch-era support commitment; not a claim that updates remain active indefinitely.")
    patch_field(item, "ram_capacity", product_source, "8 GB", 8, key="ramGb", unit="GB", note=exact)
    patch_field(item, "ram_type", "nanoreview", "NanoReview lists LPDDR4X but its selected configuration is 6 GB; the local SKU is 8 GB.",
                status="PENDING_VERIFICATION", note="The secondary source does not unambiguously attach this memory type to the locally verified 8 GB configuration; left unassigned.")
    patch_field(item, "storage_capacity", product_source, "128 GB internal storage", 128, key="storageGb", unit="GB", note=exact)
    patch_field(item, "storage_type", "nanoreview", "UFS 2.2", "UFS 2.2", status="VERIFIED_SECONDARY",
                note="NanoReview lists UFS 2.2 at model level and exposes an 8/128 option; Samsung's local page does not publish storage-interface type.")
    patch_field(item, "storage_expansion", product_source, "microSD card support up to 1 TB", "microSD up to 1 TB", note="Samsung Philippines lists microSD expansion up to 1 TB.")
    patch_field(item, "rear_camera_system", product_source, "Dual rear camera: 8 MP main autofocus + 8 MP ultra-wide", 8,
                key="rearCameraMp", unit="MP", note="Samsung lists 8 MP + 8 MP rear resolution; the 8 MP main sensor value is the catalog's primary-camera field.")
    patch_field(item, "main_camera_sensor", product_source, "Samsung does not identify the rear camera sensor component.",
                status="NOT_DISCLOSED", note="No sensor part number or aperture is inferred from resolution alone.")
    patch_field(item, "ultrawide_camera", product_source, "8 MP rear ultra-wide camera", 8, unit="MP", note="Samsung Philippines lists two rear cameras; the FE+ launch materials identify the second as ultra-wide.")
    patch_field(item, "telephoto_camera", product_source, "Samsung lists two rear cameras and no telephoto module", "No telephoto camera",
                status="NOT_APPLICABLE", note="No telephoto camera appears in the manufacturer's listed rear-camera system.")
    patch_field(item, "front_camera", product_source, "12 MP front camera", 12, key="frontCameraMp", unit="MP", note="Samsung Philippines lists a 12 MP front camera; no sensor part number inferred.")
    patch_field(item, "video_recording", product_source, "Rear video up to UHD 4K (3840 x 2160) at 30 fps", "Rear video up to 4K / 30 fps", key="video", note="Samsung Philippines lists UHD 4K at 30 fps.")
    patch_field(item, "battery_capacity", product_source, "10,090 mAh typical capacity", 10090, key="batteryMah", unit="mAh",
                note="Samsung labels 10,090 mAh as typical capacity; a rated/minimum capacity is not supplied.")
    chemistry_evidence = [
        {"value": "Li-Ion", "sourceUrl": SOURCES["nanoreview"]["url"], "sourceKind": "secondary_specification",
         "observedAt": OBSERVED, "excerpt": "NanoReview lists Li-Ion battery chemistry.",
         "configurationMatch": "Galaxy Tab S9 FE+ model level; battery sample/configuration unspecified", "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
        {"value": "Li-Polymer", "sourceUrl": SOURCES["kimovil"]["url"], "sourceKind": "secondary_specification",
         "observedAt": OBSERVED, "excerpt": "Kimovil lists Li-Polymer battery chemistry.",
         "configurationMatch": "Global Galaxy Tab S9 FE+ 8/128 5G listing; battery sample not stated", "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
    ]
    patch_field(item, "battery_technology", "nanoreview",
                "NanoReview says Li-Ion; Kimovil says Li-Polymer; Samsung does not disclose cell chemistry.",
                status="CONFLICTING_INFORMATION", note="The secondary sources disagree and Samsung does not specify chemistry. No battery chemistry is selected.", candidate_evidence=chemistry_evidence)
    patch_field(item, "wired_charging", "us_specs", "Requires separately sold 45 W wall charger", 45, key="chargingW", unit="W",
                note="Samsung's spec sheet requires a 45 W charger sold separately; the Philippine buy page also states no travel adapter is included.")
    patch_field(item, "wireless_charging", "nanoreview", "NanoReview and Kimovil report no wireless charging", "No wireless charging",
                status="VERIFIED_SECONDARY", note="No wireless charging is stated by two secondary specifications; Samsung's local page does not enumerate this feature.")
    patch_field(item, "dimensions", product_source, "185.4 x 285.4 x 6.5 mm", "185.4 x 285.4 x 6.5 mm", key="dimensions", unit="mm", note="Samsung Philippines physical specification.")
    patch_field(item, "weight", product_source, f"{config['weight']} g ({config['network']} model)", config["weight"], key="weightG", unit="g",
                note="Samsung Philippines lists 627 g for Wi-Fi and 628 g for the 5G configuration.")
    patch_field(item, "materials", product_source, "Metal body/frame", "Metal", note="Samsung product materials describe a metal body; exact alloy composition is not stated.")
    patch_field(item, "ingress_protection", product_source, "IP68", "IP68", note="Samsung Philippines identifies the FE+ as IP68 rated.")
    if wifi:
        patch_field(item, "sim_esim", product_source, "Wi-Fi-only SKU; no SIM/eSIM", "No SIM; Wi-Fi only", key="sim", note="Exact SM-X610N is the Wi-Fi-only variant.")
        patch_field(item, "cellular_bands", product_source, "Not applicable to Wi-Fi-only SKU", status="NOT_APPLICABLE", note="The exact Wi-Fi SKU has no cellular modem or mobile-network bands.")
        patch_field(item, "tablet_cellular_variant", product_source, "Wi-Fi-only variant", "Wi-Fi only", key="cellular", note="Exact SM-X610N is listed as Wi-Fi by Samsung Philippines.")
    else:
        patch_field(item, "sim_esim", product_source, "Samsung Philippines describes Dual SIM with eSIM; function availability varies by country, region or carrier.",
                    "Nano-SIM + eSIM", key="sim", note="Samsung's local FE+ page advertises eSIM/Dual SIM and warns functionality varies by market or carrier.")
        patch_field(item, "cellular_bands", product_source, CELLULAR_BANDS, CELLULAR_BANDS,
                    note="Band list transcribed from the Samsung Philippines SM-X616B 5G specification page.")
        patch_field(item, "tablet_cellular_variant", product_source, "5G cellular variant", "5G cellular", key="cellular", note="Exact SM-X616B is the Samsung Philippines 5G variant.")
    patch_field(item, "wifi", product_source, "Wi-Fi 6 (802.11 a/b/g/n/ac/ax), 2.4 GHz and 5 GHz", "Wi-Fi 6", key="wifi", note="Samsung Philippines lists 802.11 a/b/g/n/ac/ax, 2.4 GHz and 5 GHz.")
    patch_field(item, "bluetooth", product_source, "Bluetooth 5.3", "Bluetooth 5.3", note="Samsung Philippines specification.")
    patch_field(item, "usb", product_source, "USB Type-C, USB 2.0", "USB Type-C; USB 2.0", key="ports", note="Samsung Philippines lists USB 2.0 and USB Type-C.")
    patch_field(item, "nfc", product_source, "NFC: No", "No NFC", note="Samsung Philippines lists NFC as unavailable.")
    patch_field(item, "gnss", product_source, "GPS, GLONASS, BeiDou and Galileo; Samsung also lists QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS", note="Samsung Philippines connectivity specification.")
    patch_field(item, "audio", "us_specs", "Stereo speakers with Dolby Atmos", "Stereo speakers; Dolby Atmos", key="sound", note="Samsung launch specification sheet for the FE+ model family.")
    patch_field(item, "sensors", product_source, "Accelerometer, fingerprint sensor, gyroscope, geomagnetic sensor, Hall sensor and light sensor",
                "Accelerometer; fingerprint; gyroscope; geomagnetic; Hall; light", note="Samsung Philippines sensor list.")
    patch_field(item, "tablet_stylus", buy_source, "S Pen is included in the box; Creator Edition sold separately", "S Pen included", key="stylus",
                note="Samsung Philippines purchase page lists the S Pen in the box.")
    patch_field(item, "tablet_keyboard", product_source, "Book Cover Keyboard supported and sold separately", "Book Cover Keyboard supported; sold separately", key="keyboard",
                note="Samsung lists keyboard compatibility and labels the accessory as sold separately.")

    item["sources"] = [s for s in item["sources"] if s["id"] != "samsung_tab_s9_fe_samsung_de_comparison"]
    item["sources"] = list({s["id"]: s for s in [*item["sources"], *SOURCES.values()]}.values())
    item["availabilityEvidence"] = {
        "verificationStatus": "VERIFIED_OFFICIAL_LAUNCH",
        "availabilityStatus": "Philippine series availability officially announced from 2023-10-20; exact 8/128 Wi-Fi and 8/128 5G local SKUs identified.",
        "philippineAvailabilityDate": "2023-10-20", "philippineDateLabel": "Philippine launch date",
        "philippineAvailability": "Samsung Philippines announced FE-series local availability from October 20, 2023. Its local pages identify Galaxy Tab S9 FE+ Gray Wi-Fi 8/128 (SM-X610NZAAXTC) and 5G 8/128 (SM-X616BZAA XTC). Samsung PH mentions storage up to 256 GB with regional availability caveats, but no exact local 12/256 SKU and configuration-specific local price were verified; non-PH regional SKU codes were not treated as local evidence.",
        "observedAt": OBSERVED, "philippineReleaseYear": 2023, "catalogModel": MODEL,
        "qualityFlag": "Two exact local 8/128 SKUs identified; current price, exact 12/256 Philippine SKU, display peak brightness condition and battery chemistry remain unresolved.",
        "openIssues": [
            {"issue": "Samsung Philippines mentions up to 256 GB, with availability varying by market; no exact PH 12 GB / 256 GB SKU or local configuration-specific price was verified.",
             "action": "Do not list 12/256 as a confirmed Philippine variant until a Samsung Philippines SKU or authorized local configuration-level listing is found."},
            {"issue": "Samsung Philippines did not expose a current numeric price for either exact 8/128 SKU on the review date.",
             "action": "Keep current price blank and retain dated historical local prices separately."},
            {"issue": "Samsung Philippines states 600 nits maximum and 720 nits outdoor HBM; NanoReview gives 800 nits max-rated without a matching test-mode definition.",
             "action": "Keep peak brightness unresolved until comparable measurement conditions are documented."},
            {"issue": "NanoReview reports Li-Ion battery chemistry while Kimovil reports Li-Polymer; Samsung does not disclose chemistry.",
             "action": "Keep battery chemistry unselected unless manufacturer evidence or reconciled tests resolve the conflict."},
        ],
    }
    item["replacementVariants"] = [
        {"id": c["id"], "label": f"{c['ram']} GB RAM / {c['storage']} GB storage · {c['network']} · Gray",
         "sku": c["sku"], "modelCode": c["modelCode"],
         "notes": f"Exact Gray {c['network']} 8/128 SKU identified on Samsung Philippines' local product page."}
        for c in CONFIGS
    ]
    return item


def price_rows() -> list[dict]:
    rows = [{
        "device_id": DEVICE, "configuration_id": CONFIGS[1]["id"], "variant_ram_gb": 8,
        "variant_storage_gb": 128, "variant_connectivity": "5G",
        "configuration_match": "exact_8gb_128gb_5g",
        "amount_php": 39990, "price_type": "historical_ph_official_2023_cash_price_exact_configuration",
        "source_published_at": None, "observed_at": OBSERVED,
        "source_url": SOURCES["ph_prices_2023"]["url"],
        "source_kind": "official_samsung_ph_2023_home_credit_cash_price",
        "local_availability_verified": True,
        "availability_status": "historical_2023_campaign_cash_price_not_current",
        "review_status": "VERIFIED",
        "excerpt": "Samsung Philippines' Home Credit cash-price table explicitly lists Galaxy Tab S9 FE+ 5G (8 GB + 128 GB) at PHP 39,990 during the October 1–December 31, 2023 campaign. Historical, not current.",
    }]
    network_prices = [
        ("Wi-Fi", 34990, "2023", "ph_prices_2023_online", "historical_2023_ph_official_srp_model_network_configuration_unspecified", "Samsung's Oct 20–Dec 31, 2023 Philippines promotion lists FE+ Wi-Fi SRP PHP 34,990; RAM/storage not stated."),
        ("Wi-Fi", 34990, "2024", "ph_prices_2024", "historical_2024_ph_official_home_credit_model_network_configuration_unspecified", "Samsung Philippines' 2024 Home Credit table lists FE+ Wi-Fi at PHP 34,990; RAM/storage not stated."),
        ("5G", 39990, "2024", "ph_prices_2024", "historical_2024_ph_official_home_credit_model_network_configuration_unspecified", "Samsung Philippines' 2024 Home Credit table lists FE+ 5G at PHP 39,990; RAM/storage not stated."),
        ("5G", 43990, "2025", "ph_prices_2025", "historical_2025_ph_official_srp_model_network_configuration_unspecified", "Samsung Philippines' expired 2025 trade-in campaign lists FE+ 5G SRP PHP 43,990; RAM/storage not stated."),
        ("5G", 39990, "2025", "ph_prices_2025", "expired_2025_ph_official_promo_model_network_configuration_unspecified", "Samsung Philippines' expired 2025 trade-in campaign lists FE+ 5G offer PHP 39,990, valid July 9–September 30, 2025; RAM/storage not stated."),
    ]
    for network, amount, effective, source_key, price_type, excerpt in network_prices:
        rows.append({
            "device_id": DEVICE, "configuration_id": None, "variant_ram_gb": None,
            "variant_storage_gb": None, "variant_connectivity": network,
            "configuration_match": f"model_network_{network.lower()}_ram_storage_unspecified",
            "amount_php": amount, "price_type": price_type,
            "source_published_at": None, "observed_at": OBSERVED,
            "source_url": SOURCES[source_key]["url"],
            "source_kind": "official_samsung_ph_historical_campaign_price",
            "local_availability_verified": True,
            "availability_status": "expired_2025_campaign_not_current" if effective == "2025" else "historical_campaign_price_not_current",
            "review_status": "VERIFIED", "excerpt": excerpt,
        })
    return rows


def update_image_review() -> None:
    sources = json.loads(IMAGE_SOURCES.read_text(encoding="utf-8"))
    sources = [row for row in sources if row.get("deviceId") != DEVICE]
    sources.append({
        "deviceId": DEVICE,
        "pageUrl": SOURCES["image_press"]["url"],
        "method": "direct",
        "assetUrl": "https://api.samsungmobilepress.com/file/846B6641975DCE08D456B6A54BD37D5386EEE0954A92A835344B5C14F6FC5574D361A54E4FAA211D9F4A08ED3D68C0A9A22A8526E61F7E3BFC73E2D79C7552FA1A2517C53F7F89D3AF06AC60E10882C73A08C95625F87A102DAF86601A4494D9C61F02325BC2A1EA4E3158CDA50AC6CFEC56475CF9CAA37D334DA8A2F9BEADDF05B05381491F6914ED641E1C8CEE6D66BF02FBE24415EFB1CDE4ED9BDC9E7776",
        "rightsStatus": "LICENSED",
        "licenseUrl": SOURCES["image_terms"]["url"],
        "usageTerms": "Samsung Mobile Press Terms of Use: personal, informational and non-commercial use only; preserve copyright, trademark and proprietary notices; no commercial use is granted.",
        "credit": "Samsung Electronics Co., Ltd. via Samsung Mobile Press",
        "scope": "Exact Galaxy Tab S9 FE+ model; Samsung's product image does not identify the pictured color or local network configuration.",
        "changes": "Converted to WebP and resized to fit the catalog image area without cropping; no product edits or notice removal.",
        "rightsCheckedAt": OBSERVED,
    })
    IMAGE_SOURCES.write_text("[\n" + ",\n".join(
        "  " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in sources
    ) + "\n]\n", encoding="utf-8")
    unavailable = json.loads(IMAGE_UNAVAILABLE.read_text(encoding="utf-8"))
    unavailable.pop(DEVICE, None)
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    # Reuse the previously reviewed FE model's 49-field structure, while
    # overriding all FE+-specific data and source rows above.
    fe_template.DEVICE = DEVICE
    fe_template.MODEL = MODEL
    fe_template.OBSERVED = OBSERVED
    fe_template.UNRECORDED = UNRECORDED
    fe_template.SOURCES = SOURCES
    fe_template.CONFIGS = CONFIGS
    fe_template.CELLULAR_BANDS = CELLULAR_BANDS

    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Included" or device.get("workbookRow") != 439:
        raise ValueError("Expected the Included workbook row 439 Galaxy Tab S9 FE+ record; refusing unexpected target.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {c["id"] for c in CONFIGS}
    if current_ids not in ({UNRECORDED}, expected_ids):
        raise ValueError(f"Unexpected FE+ configurations; refusing to overwrite: {sorted(current_ids)}")

    targets = {(DEVICE, c["id"]) for c in CONFIGS}
    for config in CONFIGS:
        add_review(manual, catalog, review(config))
    deduplicate_target_reviews(manual, targets)
    by_source = {s["id"]: s for s in SOURCES.values()}
    for index, config in enumerate(CONFIGS):
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, config["id"]))
        if index:
            for key in ("replacementVariants", "replaceUnrecordedPlaceholder", "additionalVariants"):
                saved.pop(key, None)
        label = f"{config['ram']} GB RAM / {config['storage']} GB storage · {config['network']} · Gray"
        saved.update({"brand": "Samsung", "model": MODEL, "configuration": label, "configurationLabel": label})
        saved["sources"] = [by_source.get(s["id"], s) for s in saved.get("sources", [])]
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
        "model": MODEL, "workbookRow": 439,
        "configurations": [{"sku": c["sku"], "modelCode": c["modelCode"], "ramGb": c["ram"],
                            "storageGb": c["storage"], "network": c["network"],
                            "exactConfigHistoricalPricePhp": 39990 if c["network"] == "5G" else None}
                           for c in CONFIGS],
        "reviewedConfigurations": len(CONFIGS), "reviewedFieldsPerConfiguration": 49,
        "unresolved": ["current prices", "12/256 Philippine configuration", "display peak brightness conditions", "battery chemistry"],
        "image": "Samsung Mobile Press exact-model image cached with informational, non-commercial usage terms and attribution",
        "priceObservations": len(prices),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
