#!/usr/bin/env python3
"""Record source-backed review for exact Philippine Galaxy Tab S9 configurations."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-tab-s9-ph-prices-2026-11-27.json"
IMAGE_SOURCES = ROOT / "research/catalog-image-sources.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-27"
DEVICE = "device_7867f6ebccc2fa"
MODEL = "Galaxy Tab S9"
UNRECORDED = f"{DEVICE}-unrecorded"
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/5/59/20230729_%EC%82%BC%EC%84%B1_%EA%B0%A4%EB%9F%AD%EC%8B%9C_%ED%83%AD_S9.jpg?utm_campaign=index&utm_content=original&utm_source=commons.wikimedia.org"
IMAGE_PAGE = "https://commons.wikimedia.org/wiki/File:20230729_%EC%82%BC%EC%84%B1_%EA%B0%A4%EB%9F%AD%EC%8B%9C_%ED%83%AD_S9.jpg"


def src(sid: str, url: str, publisher: str, purpose: str, note: str, published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = {
    "wifi_128": src(
        "samsung_tab_s9_ph_wifi_128_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-wi-fi-graphite-128gb-sm-x710nzaaxtc/",
        "Samsung Philippines", "Exact 8 GB / 128 GB Wi-Fi Philippine SKU and product specifications",
        "Official Philippine product page for Graphite SKU SM-X710NZAA XTC. Product specifications identify the 8 GB / 128 GB Wi-Fi variant and model-family technical details."),
    "wifi_256": src(
        "samsung_tab_s9_ph_wifi_256_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-wi-fi-graphite-256gb-sm-x710nzaextc/",
        "Samsung Philippines", "Exact 12 GB / 256 GB Wi-Fi Philippine SKU and product specifications",
        "Official Philippine product page for Graphite SKU SM-X710NZAE XTC. Samsung Philippines newsroom separately lists the local 12 GB / 256 GB Wi-Fi configuration."),
    "5g_128": src(
        "samsung_tab_s9_ph_5g_128_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-5g-graphite-128gb-sm-x716bzaaxtc/",
        "Samsung Philippines", "Exact 8 GB / 128 GB 5G Philippine SKU and product specifications",
        "Official Philippine product page for Graphite SKU SM-X716BZAA XTC. Detailed table lists the local 5G model specifications, network bands, memory and storage."),
    "5g_256": src(
        "samsung_tab_s9_ph_5g_256_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-5g-graphite-256gb-sm-x716bzaextc/",
        "Samsung Philippines", "Exact 12 GB / 256 GB 5G Philippine SKU and product specifications",
        "Official Philippine product page for Graphite SKU SM-X716BZAE XTC. Samsung Philippines newsroom separately lists the local 12 GB / 256 GB 5G configuration."),
    "ph_launch_specs": src(
        "samsung_tab_s9_ph_newsroom_specs",
        "https://news.samsung.com/ph/samsung-galaxy-tab-s9-sets-the-new-standard-to-bring-galaxys-premium-experience-to-a-tablet",
        "Samsung Newsroom Philippines", "Local configuration table and launch specifications",
        "Samsung Philippines lists Android 13.0, an 11-inch Dynamic AMOLED 2X display, 60–120 Hz refresh rate, dimensions, Wi-Fi/5G weights, cameras, 8/128 and 12/256 GB versions, processor and 8,400 mAh typical battery.",
        "2023-09-06"),
    "ph_pricing": src(
        "samsung_tab_s9_ph_preorder_terms",
        "https://www.samsung.com/ph/offer/offline/2023/galaxy-tab-s9-preorder/",
        "Samsung Philippines", "Authorized local preorder window, pickup timing, SRPs and preorder offers",
        "Official terms show the July 26–August 17, 2023 local preorder period; customers could get preorder units as early as August 11. They list device SRPs and the 256 GB preorder prices with a free within-series storage upgrade.",
        "2023-07-26"),
    "ph_availability": src(
        "samsung_tab_s9_ph_local_availability",
        "https://news.samsung.com/ph/galaxy-tab-s9-series-the-ultimate-entertainment-experience-that-takes-you-places",
        "Samsung Newsroom Philippines", "Dated confirmation of Philippine store and online availability",
        "Samsung Philippines reported the series available through participating local stores and online channels by September 6, 2023. This confirms local availability but not the exact first general-sale transaction.",
        "2023-09-06"),
    "ph_pricing_release": src(
        "samsung_tab_s9_ph_launch_prices",
        "https://news.samsung.com/ph/bring-your-ideas-to-life-everywhere-with-the-samsung-galaxy-tab-s9-series",
        "Samsung Newsroom Philippines", "Dated Philippine launch price cross-check",
        "Samsung Newsroom Philippines published variant SRPs on September 8, 2023: Wi-Fi 8/128 PHP 47,990, Wi-Fi 12/256 PHP 54,990, 5G 8/128 PHP 56,990, and 5G 12/256 PHP 63,990.",
        "2023-09-08"),
    "global_launch": src(
        "samsung_tab_s9_global_launch",
        "https://news.samsung.com/global/samsung-galaxy-tab-s9-sets-the-new-standard-to-bring-galaxys-premium-experience-to-a-tablet",
        "Samsung Global Newsroom", "Global announcement, availability timing, support policy and shared model specifications",
        "Samsung announced the Tab S9 series July 26, 2023 and said general availability in select markets began August 11, 2023. The global launch material identifies the Snapdragon 8 Gen 2 for Galaxy, IP68, included S Pen, Armor Aluminum and four OS generations plus five years of security updates.",
        "2023-07-26"),
    "global_availability": src(
        "samsung_tab_s9_global_availability",
        "https://news.samsung.com/global/samsung-announces-global-launch-of-galaxy-z-flip5-galaxy-z-fold5-galaxy-watch6-series-and-galaxy-tab-s9-series",
        "Samsung Global Newsroom", "Global market availability start date",
        "Samsung says the Galaxy Tab S9 series launched in selected markets on August 11, 2023; additional markets followed later.",
        "2023-08-11"),
    "charge_specs": src(
        "samsung_tab_s9_45w_charging_support",
        "https://www.samsung.com/us/support/answer/ANS10003691/",
        "Samsung Support US", "Manufacturer charging capability",
        "Samsung support states that Galaxy Tab S9 models support 45 W Fast Charging 2.0 with a compatible charger and cable. This does not imply the charger is included."),
    "sim_specs": src(
        "samsung_tab_s9_5g_sim_esim_specs",
        "https://www.samsung.com/ch/support/mobile-devices/vergleich-galaxy-tab-s9-serie/",
        "Samsung Switzerland Support", "Manufacturer SIM capability for model codes SM-X716B / SM-X710",
        "Samsung's model-family table maps SM-X716B to the cellular model and identifies Nano-SIM (4FF) plus eSIM. The Wi-Fi-only SM-X710 does not take a SIM."),
    "processor_specs": src(
        "qualcomm_snapdragon_8_gen_2_specs",
        "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-gen-2-mobile-platform",
        "Qualcomm", "Chip process and platform-level technical details",
        "Qualcomm lists the Snapdragon 8 Gen 2 at 4 nm and a maximum CPU frequency up to 3.36 GHz; Samsung's exact Galaxy Tab S9 local product pages identify the Snapdragon 8 Gen 2 for Galaxy."),
    "gsmarena": src(
        "gsmarena_tab_s9_specs",
        "https://www.gsmarena.com/compare.php3?idPhone1=12439",
        "GSMArena", "Independent exact-model specification cross-check",
        "GSMArena's Galaxy Tab S9 specification table reports the octa-core CPU layout, Adreno 740 graphics, UFS storage, Corning Gorilla Glass without a revision, SIM/eSIM on cellular models, cameras, dimensions and other model-family details."),
    "nanoreview": src(
        "nanoreview_tab_s9_specs",
        "https://nanoreview.net/en/tablet/samsung-galaxy-tab-s9",
        "NanoReview", "Secondary technical specifications and measurement references",
        "NanoReview lists LPDDR5X memory, screen brightness, storage and battery data for the Tab S9 family. Its page attributes measured display data to NotebookCheck; Samsung's Philippine product pages remain the primary source where available."),
    "os_support": src(
        "samsung_tab_s9_environment_report",
        "https://www.samsung.com/global/sustainability/landing_hub-file/AY_wCQf6BaEALYNu/Galaxy_Tab_S9_Environmental_Report_EN_2503.pdf",
        "Samsung Electronics", "Manufacturer software support commitment",
        "Samsung's Galaxy Tab S9 product environmental report says four generations of OS upgrades and five years of security updates."),
    "ph_2025_promo": src(
        "samsung_tab_s9_ph_2025_promo",
        "https://www.samsung.com/ph/offer/offline/2025/galaxy-tab-home-credit/",
        "Samsung Philippines", "Dated official local discount terms by storage and connectivity variant",
        "Expired offer valid June 1–30, 2025. Samsung's table lists each Tab S9 Wi-Fi/5G 128/256 GB SRP and PHP 8,000 discount. Dated promo prices are calculated from those explicit SRPs and discount amounts; they are not current offers.",
        "2025-06-01"),
    "yugatech_prices": src(
        "yugatech_tab_s9_ph_prices",
        "https://www.yugatech.com/news/samsung-galaxy-tab-s9-series-priced-in-the-philippines/",
        "YugaTech", "Independent local launch SRP and configuration cross-check",
        "YugaTech's August 3, 2023 report lists the same three Tab S9 SRPs as Samsung, but reports PHP 64,990 for 12/256 GB 5G while Samsung's preorder terms and September 8 Newsroom article list PHP 63,990. Both dated values are retained.",
        "2023-08-03"),
    "lazmall_price": src(
        "baratobot_tab_s9_5g_128_lazmall_price",
        "https://baratobot.com/p/samsung-galaxy-tab-s9-5g-114759?v=6999",
        "BaratoBot price tracker; seller shown as Samsung on LazMall", "Recent dated Philippine retail listing for 8 GB / 128 GB 5G",
        "BaratoBot reported the Graphite 128 GB Samsung LazMall offer at PHP 50,990 and in stock on November 17, 2026. This is the tracker’s last observed date, not a November 27 checkout guarantee.",
        "2026-11-17"),
    "price_me_5g256": src(
        "priceme_tab_s9_5g_256_current_listing",
        "https://ph.priceme.com/Samsung-Galaxy-Tab-S9-SM-X716-11in-5G-256GB/p-916292358.aspx",
        "PriceMe Philippines; retailer offer shown as Anson's", "Current comparator listing and price history for 12 GB / 256 GB 5G",
        "PriceMe's page observed November 27, 2026 shows an in-stock Anson's offer at PHP 52,990. Its price history lists August 7, 2026 as the last price change, so direct checkout availability and condition remain unconfirmed.",
        "2026-08-07"),
    "commons_image": src(
        "commons_tab_s9_exact_model_image",
        IMAGE_PAGE,
        "Striker9498 / Wikimedia Commons", "Licensed exact-model photograph and attribution record",
        "The photo is captioned Samsung Galaxy Tab S9, dated July 29, 2023, and shows the device information screen naming Galaxy Tab S9 and model SM-X710. Used as a model-identification image; the exact storage configuration is not visible. Creator is Striker9498; CC BY-SA 4.0. Catalog asset will be resized and converted to WebP without cropping or subject edits."),
}

CONFIGS = [
    {"id": f"{DEVICE}-sm-x710-8gb-128gb-wifi-ph", "key": "wifi_128", "modelCode": "SM-X710", "sku": "SM-X710NZAA XTC", "ram": 8, "storage": 128, "network": "Wi-Fi", "weight": 498, "launch": 47990},
    {"id": f"{DEVICE}-sm-x710-12gb-256gb-wifi-ph", "key": "wifi_256", "modelCode": "SM-X710", "sku": "SM-X710NZAE XTC", "ram": 12, "storage": 256, "network": "Wi-Fi", "weight": 498, "launch": 54990, "preorder": 47990},
    {"id": f"{DEVICE}-sm-x716b-8gb-128gb-5g-ph", "key": "5g_128", "modelCode": "SM-X716B", "sku": "SM-X716BZAA XTC", "ram": 8, "storage": 128, "network": "5G", "weight": 500, "launch": 56990, "current": 50990, "currentDate": "2026-11-17"},
    {"id": f"{DEVICE}-sm-x716b-12gb-256gb-5g-ph", "key": "5g_256", "modelCode": "SM-X716B", "sku": "SM-X716BZAE XTC", "ram": 12, "storage": 256, "network": "5G", "weight": 500, "launch": 63990, "preorder": 56990, "candidateCurrent": 52990},
]


def field(fid: str, sid: str, source_value, normalized=None, *, status="VERIFIED", key=None,
          unit=None, note=None, candidate_evidence=None, price_condition=None,
          price_type=None, price_observed=None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": source_value, "normalizedValue": normalized,
           "note": note or "Exact local model and configuration checked against the cited source."}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if candidate_evidence:
        row["candidateEvidence"] = candidate_evidence
    if price_condition is not None:
        row["priceCondition"] = price_condition
    if price_type is not None:
        row["priceType"] = price_type
    if price_observed is not None:
        row["priceObservedAt"] = price_observed
    return row


def missing(fid: str, sid: str, value: str, note: str, *, status="NOT_DISCLOSED", unit=None) -> dict:
    return field(fid, sid, value, None, status=status, unit=unit, note=note)


def evidence(value: str, url: str, source_kind: str, excerpt: str, *, status="CONFLICTING_INFORMATION") -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": "Galaxy Tab S9 model family; exact local memory variant not stated",
            "reviewStatus": status, "localAvailabilityVerified": False}


CELLULAR_BANDS = (
    "2G GSM 850/900/1800/1900; 3G UMTS B1/B2/B4/B5/B8; "
    "4G FDD LTE B1/B2/B3/B4/B5/B7/B8/B12/B13/B17/B20/B25/B26/B28/B32/B66; "
    "4G TDD LTE B38/B40/B41; 5G FDD Sub-6 n1/n3/n5/n7/n8/n20/n28/n66; "
    "5G TDD Sub-6 n38/n40/n41/n77/n78"
)


def make_review(config: dict) -> dict:
    sid = config["key"]
    network = config["network"]
    wifi_only = network == "Wi-Fi"
    label = f"{config['ram']} GB RAM / {config['storage']} GB storage · {network}"
    local_config_note = "Exact Samsung Philippines model code and RAM/storage variant matched to its local SKU page and the Philippines newsroom configuration table."
    notes: list[dict] = []
    fields: list[dict] = []

    def add(fid, source_key, value, normalized=None, **kwargs):
        fields.append(field(fid, SOURCES[source_key]["id"], value, normalized, **kwargs))

    def unavailable(fid, source_key, value, note, *, status="NOT_DISCLOSED", unit=None):
        fields.append(missing(fid, SOURCES[source_key]["id"], value, note, status=status, unit=unit))

    price_conflict = None
    if config["key"] == "5g_256":
        price_conflict = [evidence(
            "PHP 64,990 for Galaxy Tab S9 5G 12GB / 256GB",
            SOURCES["yugatech_prices"]["url"], "independent_ph_launch_report",
            "YugaTech published PHP 64,990 on August 3, 2023; Samsung Philippines lists PHP 63,990 in its July 2023 preorder terms and September 8, 2023 newsroom price table.",
            status="PENDING_VERIFICATION")]

    add("model_number", sid, config["modelCode"], config["modelCode"], note=local_config_note)
    add("global_release_date", "global_availability", "General availability in selected global markets began 2023-08-11", "2023-08-11",
        note="Samsung's global newsroom identifies August 11, 2023 as the selected-market general availability date. The series was announced July 26; this is not a claim that every market released it on the same day.")
    add("configuration", sid, label, label, note=local_config_note)
    add("philippine_release_date", "ph_pricing", "Samsung says preorder units could be collected as early as 2023-08-11", "2023-08-11",
        note="This is the earliest local preorder-unit pickup date documented by Samsung Philippines, not a verified date of the first general retail sale. Samsung later reported local store and online availability by September 6, 2023.")
    add("official_launch_price_php", "ph_pricing_release", f"PHP {config['launch']:,} official Philippine SRP for {label}", config["launch"], unit="PHP",
        note=("Samsung Philippines lists PHP 63,990 as SRP for 12GB / 256GB 5G. YugaTech reported PHP 64,990 on August 3, 2023; the one-thousand-peso discrepancy is retained as unresolved secondary evidence."
              if price_conflict else "Historical Philippine SRP in Samsung Philippines' dated product/preorder price table. This is a launch-era price, not a current offer."),
        candidate_evidence=price_conflict)
    if config.get("current"):
        add("current_price_php", "lazmall_price", "BaratoBot reports an in-stock Samsung LazMall listing at PHP 50,990, last checked 2026-11-17", config["current"],
            status="VERIFIED_SECONDARY", unit="PHP", note="Recent dated listing from Samsung's LazMall store, as reported by BaratoBot on November 17, 2026. Its date is shown with the price; stock and price may have changed since that check.",
            price_condition="new", price_type="dated_official_lazmall_listing", price_observed=config["currentDate"])
    elif config.get("candidateCurrent"):
        add("current_price_php", "price_me_5g256", "PriceMe shows PHP 52,990 at Anson's and marks the offer in stock; last recorded price change was 2026-08-07", None,
            status="PENDING_VERIFICATION", unit="PHP", note="A price comparator currently shows an in-stock offer, but its price history has no update after August 7, 2026 and the retailer checkout, stock and item condition were not independently confirmed. Keep the catalog's current price blank pending a fresh direct listing.")
    else:
        unavailable("current_price_php", "ph_2025_promo", "No sufficiently recent, directly confirmed exact-configuration Philippine selling price was found for this Wi-Fi variant.",
                    "Historical SRPs and dated promotions are recorded separately. No current price is inferred from a stale product page or expired promotion.", status="PENDING_VERIFICATION", unit="PHP")

    add("display_size", sid, "11.0 inches (full rectangle)", 11, key="displayInches", unit="in",
        note="Samsung lists an 11-inch full-rectangle measurement and 10.9 inches accounting for rounded corners.")
    add("display_technology", sid, "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType")
    add("display_resolution", sid, "2560 x 1600 (WQXGA)", "2560 x 1600", key="resolution")
    add("display_refresh_rate", "ph_launch_specs", "Dynamic refresh rate from 60 to 120 Hz", 120, key="refreshHz", unit="Hz",
        note="Samsung says the panel dynamically adjusts from 60 to 120 Hz; catalog numeric value records the maximum refresh rate.")
    add("display_brightness", "nanoreview", "NanoReview lists 600 nits maximum rated brightness and attributes measured data to NotebookCheck", 600,
        status="VERIFIED_SECONDARY", unit="nits", note="Secondary specification/measurement. Samsung Philippines does not publish a brightness rating for this model.")
    add("display_protection", "gsmarena", "Corning Gorilla Glass; revision not specified", "Corning Gorilla Glass (revision unspecified)",
        status="VERIFIED_SECONDARY", note="GSMArena identifies Corning Gorilla Glass but does not specify the revision. Samsung's Philippine specifications do not name a glass version.")
    add("chipset", sid, "Qualcomm Snapdragon 8 Gen 2 for Galaxy", "Qualcomm Snapdragon 8 Gen 2 for Galaxy", key="chipset")
    add("process_node", "processor_specs", "Snapdragon 8 Gen 2 is a 4 nm platform", 4, status="VERIFIED_SECONDARY", unit="nm",
        note="Qualcomm lists the Snapdragon 8 Gen 2 mobile platform as 4 nm; Samsung identifies the Galaxy Tab S9's chip as Snapdragon 8 Gen 2 for Galaxy.")
    add("cpu", sid, "Octa-core; CPU speed groups 3.36 GHz, 2.8 GHz and 2.0 GHz", "Octa-core; 3.36 GHz / 2.8 GHz / 2.0 GHz",
        note="Samsung Philippines lists these CPU speeds and an octa-core CPU on the exact local SKU page.")
    add("gpu", "gsmarena", "Adreno 740", "Adreno 740", status="VERIFIED_SECONDARY")
    add("operating_system", "ph_launch_specs", "Android 13.0 at launch", "Android 13", key="os",
        note="Samsung Philippines lists Android 13.0 in the local launch specification table; later updates are not substituted for launch software.")
    add("os_support", "os_support", "Four generations of One UI and Android OS upgrades; five years of security updates", "Up to 4 OS generations; 5 years of security updates",
        note="Manufacturer support commitment from Samsung's Galaxy Tab S9 product environmental report. This is the launch policy, not a statement that future updates remain available indefinitely.")
    add("ram_capacity", sid, f"{config['ram']} GB", config["ram"], key="ramGb", unit="GB")
    add("ram_type", "nanoreview", "LPDDR5X", "LPDDR5X", status="VERIFIED_SECONDARY",
        note="NanoReview lists LPDDR5X for the Galaxy Tab S9 model family; Samsung Philippines does not state RAM type on the product page.")
    add("storage_capacity", sid, f"{config['storage']} GB", config["storage"], key="storageGb", unit="GB")
    add("storage_type", "gsmarena", "UFS; revision not specified", "UFS (revision unspecified)", status="VERIFIED_SECONDARY",
        note="GSMArena lists UFS storage without a version. A faster UFS revision is not inferred for a local configuration from an unsourced family-level claim.")
    add("storage_expansion", sid, "MicroSD card support up to 1 TB", "microSD supported up to 1 TB")
    add("rear_camera_system", sid, "13 MP autofocus rear camera", "13 MP autofocus rear camera", key="rearCameraMp",
        note="Samsung's exact Philippine SKU specifications list a single 13 MP autofocus rear camera.")
    unavailable("main_camera_sensor", "gsmarena", "No exact image-sensor component name was disclosed in the reviewed manufacturer or independent specifications.",
                "Megapixel count and autofocus are documented; the sensor part number is not. No sensor model is inferred.")
    add("ultrawide_camera", sid, "The Tab S9 rear-camera specification lists one 13 MP camera and no rear ultra-wide module", "No rear ultra-wide camera", status="NOT_APPLICABLE")
    add("telephoto_camera", sid, "The Tab S9 rear-camera specification lists one 13 MP camera and no telephoto module", "No telephoto camera", status="NOT_APPLICABLE")
    add("front_camera", "ph_launch_specs", "12 MP ultra-wide front camera", "12 MP ultra-wide", key="frontCameraMp", unit="MP")
    add("video_recording", sid, "Rear video: UHD 4K (3840 x 2160) at 30 fps", "Rear video up to 4K / 30 fps", key="video")
    add("battery_capacity", sid, "8,400 mAh typical; Samsung lists 8,160 mAh rated/minimum", 8400, key="batteryMah", unit="mAh",
        note="Samsung's 8,400 mAh figure is typical capacity; the manufacturer's footnote states rated/minimum capacity is 8,160 mAh.")
    battery_evidence = [
        evidence("Li-Po", SOURCES["gsmarena"]["url"], "independent_specification", "GSMArena lists Li-Po battery chemistry."),
        evidence("Li-Ion", SOURCES["nanoreview"]["url"], "independent_specification", "NanoReview lists Li-Ion battery chemistry."),
    ]
    fields.append(field("battery_technology", SOURCES["gsmarena"]["id"],
                        "GSMArena reports Li-Po; NanoReview reports Li-Ion; Samsung does not specify chemistry.", None,
                        status="CONFLICTING_INFORMATION", note="Independent sources disagree on battery chemistry, and Samsung's local specification page does not identify it. Chemistry is withheld.", candidate_evidence=battery_evidence))
    add("wired_charging", "charge_specs", "45 W Fast Charging 2.0 with a compatible adapter and cable", 45, key="chargingW", unit="W",
        note="Samsung support lists 45 W capability. A compatible charger and cable are required; this does not state they are included.")
    add("wireless_charging", "nanoreview", "Not supported", "Not supported", status="VERIFIED_SECONDARY",
        note="NanoReview marks wireless charging as unsupported. Samsung's specifications do not list wireless charging.")
    add("dimensions", sid, "165.8 x 254.3 x 5.9 mm", "165.8 x 254.3 x 5.9 mm", key="dimensions", unit="mm")
    add("weight", sid, f"{config['weight']} g ({network} model)", config["weight"], key="weightG", unit="g",
        note="Samsung lists 498 g for Wi-Fi and 500 g for 5G models.")
    add("materials", "global_launch", "Armor Aluminum frame", "Armor Aluminum frame")
    add("ingress_protection", sid, "IP68", "IP68")
    if wifi_only:
        add("sim_esim", "sim_specs", "Wi-Fi-only SKU; no SIM or eSIM", "No SIM; Wi-Fi only", key="sim")
        unavailable("cellular_bands", sid, "Not applicable: this local SKU is Wi-Fi-only.",
                    "No cellular modem is included in the SM-X710 Wi-Fi configuration.", status="NOT_APPLICABLE")
        add("tablet_cellular_variant", sid, "Wi-Fi-only model", "Wi-Fi only", key="cellular")
    else:
        add("sim_esim", "sim_specs", "Nano-SIM (4FF) and eSIM", "Nano-SIM + eSIM", key="sim",
            note="Samsung documents Nano-SIM + eSIM for model code SM-X716B; the local SKU page identifies this 5G model code.")
        add("cellular_bands", sid, CELLULAR_BANDS, CELLULAR_BANDS)
        add("tablet_cellular_variant", sid, "5G cellular model", "5G cellular", key="cellular")
    add("wifi", sid, "802.11 a/b/g/n/ac/ax on 2.4, 5 and 6 GHz; Wi-Fi 6E", "Wi-Fi 6E", key="wifi")
    add("bluetooth", sid, "Bluetooth 5.3", "Bluetooth 5.3", key="bluetooth")
    add("usb", sid, "USB Type-C; USB 3.2 Gen 1", "USB Type-C; USB 3.2 Gen 1", key="ports")
    add("nfc", sid, "NFC: No", "No NFC")
    add("gnss", sid, "GPS, GLONASS, BeiDou, Galileo and QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS")
    add("audio", "ph_launch_specs", "Quad speakers with AKG tuning and Dolby Atmos", "Quad speakers; AKG tuning; Dolby Atmos", key="sound")
    add("sensors", sid, "Accelerometer, fingerprint, gyroscope, geomagnetic, Hall and RGB light sensors", "Accelerometer; fingerprint; gyroscope; geomagnetic; Hall; RGB light")
    add("tablet_stylus", "global_launch", "IP68-rated S Pen included in the box", "S Pen included", key="stylus")
    add("tablet_keyboard", sid, "Book Cover Keyboard supported; sold separately", "Book Cover Keyboard supported; sold separately", key="keyboard",
        note="Accessory support is separate from time-limited 2023 preorder keyboard offers.")

    if len(fields) != 49:
        raise ValueError(f"Expected 49 field reviews for {label}, found {len(fields)}")
    sources = list(SOURCES.values())
    variants = [{"id": c["id"], "label": f"{c['ram']} GB RAM / {c['storage']} GB storage · {c['network']}",
                 "sku": c["sku"], "modelCode": c["modelCode"],
                 "notes": "Exact Samsung Philippines SKU verified from the local product page."}
                for c in CONFIGS]
    item = {"deviceId": DEVICE, "configurationId": config["id"], "brand": "Samsung", "model": MODEL,
            "configuration": label, "modelCode": config["modelCode"], "sku": config["sku"],
            "sources": sources, "fields": fields,
            "availabilityEvidence": {
                "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                "availabilityStatus": "Authorized Philippine preorder pickup documented from 2023-08-11; local stores and online availability reported by 2023-09-06.",
                "philippineAvailabilityDate": "2023-08-11",
                "philippineDateLabel": "Earliest preorder pickup",
                "philippineAvailability": "Samsung Philippines' authorized preorder terms say units could be collected as early as August 11, 2023; its September 6 newsroom article reports availability through participating local stores and online channels. Exact first general-sale date remains unresolved.",
                "observedAt": "2023-09-06", "philippineReleaseYear": 2023,
                "catalogModel": MODEL,
                "qualityFlag": "Earliest preorder pickup documented; exact first general-sale date unresolved.",
                "openIssues": [{"issue": "Exact date of first general retail sale was not found.",
                                "action": "Retain August 11, 2023 as earliest documented preorder pickup; do not label it the first retail sale."}],
            }}
    # The merge helper validates each reviewed configuration against either an
    # existing catalog variant or its review's explicit replacement set. Keep
    # this declaration on every in-memory review; main() stores it only on the
    # first manual review so a workbook rebuild replaces the placeholder once.
    item["replacementVariants"] = variants
    return item


def price_rows() -> list[dict]:
    rows = []
    promo_source = SOURCES["ph_2025_promo"]["url"]
    official_price_source = SOURCES["ph_pricing_release"]["url"]
    launch_source = SOURCES["ph_pricing"]["url"]
    for config in CONFIGS:
        common = {"device_id": DEVICE, "configuration_id": config["id"],
                  "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
                  "variant_connectivity": config["network"],
                  "configuration_match": f"exact_{config['ram']}gb_{config['storage']}gb_{config['network'].lower().replace('-', '')}"}
        rows.append({**common, "amount_php": config["launch"],
                     "price_type": "historical_ph_official_srp", "source_published_at": "2023-09-08",
                     "observed_at": OBSERVED, "source_url": official_price_source,
                     "source_kind": "official_samsung_ph_launch_price", "local_availability_verified": True,
                     "availability_status": "historical_launch_srp_not_current", "review_status": "VERIFIED",
                     "excerpt": f"Samsung Philippines lists PHP {config['launch']:,} SRP for {config['ram']} GB / {config['storage']} GB {config['network']} Galaxy Tab S9."})
        discount_price = config["launch"] - 8000
        rows.append({**common, "amount_php": discount_price,
                     "price_type": "historical_2025_promo_price_calculated_from_published_srp_and_discount",
                     "source_published_at": "2025-06-01", "observed_at": OBSERVED,
                     "source_url": promo_source, "source_kind": "official_samsung_ph_discount_terms_arithmetic",
                     "local_availability_verified": True,
                     "availability_status": "expired_2025_06_01_to_2025_06_30_offer_not_current",
                     "review_status": "VERIFIED",
                     "excerpt": f"Samsung Philippines' June 1–30, 2025 offer listed the PHP {config['launch']:,} SRP and PHP 8,000 off; PHP {discount_price:,} is the subtraction of those two published amounts, not a current offer."})
        if config.get("preorder"):
            rows.append({**common, "amount_php": config["preorder"],
                         "price_type": "historical_2023_preorder_price_with_free_storage_upgrade",
                         "source_published_at": "2023-07-26", "observed_at": OBSERVED,
                         "source_url": launch_source, "source_kind": "official_samsung_ph_preorder_price",
                         "local_availability_verified": True,
                         "availability_status": "expired_2023_preorder_offer_256gb_upgrade_price_not_current",
                         "review_status": "VERIFIED",
                         "excerpt": f"Samsung Philippines listed PHP {config['preorder']:,} preorder price for the exact 12 GB / 256 GB {config['network']} configuration as part of a 128 GB to 256 GB free storage upgrade; the offer ran July 26–August 17, 2023."})
    # YugaTech's competing 5G 12/256 launch figure is retained instead of silently overwritten.
    config = next(c for c in CONFIGS if c["key"] == "5g_256")
    rows.append({"device_id": DEVICE, "configuration_id": config["id"], "amount_php": 64990,
                 "variant_ram_gb": 12, "variant_storage_gb": 256, "variant_connectivity": "5G",
                 "configuration_match": "exact_12gb_256gb_5g", "price_type": "historical_secondary_launch_srp_conflicts_with_samsung_ph",
                 "source_published_at": "2023-08-03", "observed_at": OBSERVED,
                 "source_url": SOURCES["yugatech_prices"]["url"], "source_kind": "independent_ph_launch_price_report",
                 "local_availability_verified": True, "availability_status": "historical_reported_price_conflicts_with_official_srp",
                 "review_status": "PENDING_VERIFICATION",
                 "excerpt": "YugaTech reported PHP 64,990 on August 3, 2023; Samsung Philippines terms and its September 8 newsroom price list show PHP 63,990. The discrepancy is retained; no single value is inferred from the secondary report."})
    # Recent offers have explicit dates and source-reported stock caveats.
    c128 = next(c for c in CONFIGS if c["key"] == "5g_128")
    rows.append({"device_id": DEVICE, "configuration_id": c128["id"], "amount_php": 50990,
                 "variant_ram_gb": 8, "variant_storage_gb": 128, "variant_connectivity": "5G",
                 "configuration_match": "exact_8gb_128gb_5g", "price_type": "dated_samsung_lazmall_listing",
                 "source_published_at": None, "observed_at": "2026-11-17", "source_url": SOURCES["lazmall_price"]["url"],
                 "source_kind": "price_tracker_reports_official_samsung_lazmall_listing",
                 "local_availability_verified": True, "availability_status": "reported_in_stock_on_2026_11_17_not_rechecked_at_checkout",
                 "review_status": "VERIFIED_SECONDARY",
                 "excerpt": "BaratoBot records a PHP 50,990 Graphite 8/128 GB offer from Samsung on LazMall, in stock when checked November 17, 2026. Price and stock may have changed since."})
    c256 = next(c for c in CONFIGS if c["key"] == "5g_256")
    rows.append({"device_id": DEVICE, "configuration_id": c256["id"], "amount_php": 52990,
                 "variant_ram_gb": 12, "variant_storage_gb": 256, "variant_connectivity": "5G",
                 "configuration_match": "exact_12gb_256gb_5g", "price_type": "comparator_listed_current_offer_condition_and_checkout_pending",
                 "source_published_at": None, "observed_at": OBSERVED, "source_url": SOURCES["price_me_5g256"]["url"],
                 "source_kind": "price_comparator_ansons_offer", "local_availability_verified": False,
                 "availability_status": "priceme_marks_offer_in_stock_last_recorded_price_change_2026_08_07_direct_stock_not_checked",
                 "review_status": "PENDING_VERIFICATION",
                 "excerpt": "PriceMe shows an in-stock Anson's offer at PHP 52,990 on the page accessed November 27, 2026; its price history says the price last changed August 7, 2026. Direct stock and condition were not confirmed."})
    return rows


def update_image_sources() -> None:
    sources = json.loads(IMAGE_SOURCES.read_text(encoding="utf-8"))
    source = {
        "deviceId": DEVICE, "method": "direct", "pageUrl": IMAGE_PAGE, "assetUrl": IMAGE_URL,
        "scope": "Exact Galaxy Tab S9 model; photographed display identifies model SM-X710; memory/storage configuration is not visible.",
        "rightsStatus": "LICENSED", "credit": "Striker9498 (Wikimedia Commons)",
        "usageTerms": "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
        "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0/",
        "rightsCheckedAt": OBSERVED,
        "changes": "Converted from JPEG to WebP and resized for catalog delivery; no crop or subject edits.",
    }
    source_index = next((index for index, row in enumerate(sources) if row.get("deviceId") == DEVICE), None)
    if source_index is None:
        sources.append(source)
    else:
        sources[source_index] = source
    IMAGE_SOURCES.write_text("[\n" + ",\n".join(
        "  " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in sources
    ) + "\n]\n", encoding="utf-8")
    unavailable = json.loads(IMAGE_UNAVAILABLE.read_text(encoding="utf-8"))
    unavailable.pop(DEVICE, None)
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Included":
        raise ValueError("Expected the Included workbook Galaxy Tab S9 record; refusing unexpected scope/device.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {v["id"] for v in CONFIGS}
    replacing = current_ids == {UNRECORDED}
    already_integrated = current_ids == expected_ids
    if not (replacing or already_integrated):
        raise ValueError(f"Unexpected Galaxy Tab S9 configurations; refusing: {sorted(current_ids)}")

    for index, config in enumerate(CONFIGS):
        add_review(manual, catalog, make_review(config))
    deduplicate_target_reviews(manual, {(DEVICE, config["id"]) for config in CONFIGS})
    source_updates = {s["id"]: s for s in SOURCES.values()}
    for config in CONFIGS:
        saved = next(r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == config["id"])
        if config["id"] != CONFIGS[0]["id"]:
            for key in ("replacementVariants", "replaceUnrecordedPlaceholder", "additionalVariants"):
                saved.pop(key, None)
        saved.update({"brand": "Samsung", "model": MODEL,
                      "configuration": f"{config['ram']} GB RAM / {config['storage']} GB storage · {config['network']}",
                      "configurationLabel": f"{config['ram']} GB RAM / {config['storage']} GB storage · {config['network']}"})
        saved["sources"] = [source_updates.get(s["id"], s) for s in saved.get("sources", [])]
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    update_image_sources()
    prices = price_rows()
    snapshot = {"run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
                "models": [{"device_id": DEVICE, "brand": "Samsung", "model_name": MODEL,
                            "category": "tablets", "status": "manually_reviewed"}],
                "fetches": [], "observations": [],
                "discovery": [{"device_id": DEVICE, "source_url": source["url"],
                               "source_kind": source["purpose"], "status": "reviewed", "result": source["note"]}
                              for source in SOURCES.values()],
                "prices": prices}
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    model = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if model:
        model["status"] = "manually_reviewed"
    known = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type"),
              p.get("source_url"), p.get("configuration_match")) for p in latest.get("prices", [])}
    for price in prices:
        key = (price["device_id"], price["configuration_id"], price["price_type"],
               price["source_url"], price["configuration_match"])
        if key in known:
            existing = next(row for row in latest["prices"] if (
                row.get("device_id"), row.get("configuration_id"), row.get("price_type"),
                row.get("source_url"), row.get("configuration_match")) == key)
            existing.update(price)
        else:
            latest.setdefault("prices", []).append(price)
            known.add(key)
    latest["run_at"] = OBSERVED
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"model": MODEL, "configurations": [
        {"configuration": f"{c['ram']} GB RAM / {c['storage']} GB storage · {c['network']}",
         "sku": c["sku"], "launchSrpPhp": c["launch"], "currentListedPricePhp": c.get("current"),
         "currentPriceObservedAt": c.get("currentDate"), "scope": "Included"} for c in CONFIGS],
        "reviewedConfigurations": len(CONFIGS), "reviewedFieldsPerConfiguration": 49,
        "availability": "Authorized PH preorder pickup from 2023-08-11; first general-sale date unresolved",
        "image": "exact model photograph; CC BY-SA 4.0 with credit; model code SM-X710 is visible",
        "launchPriceConflict": "YugaTech 5G 12/256 PHP 64,990 vs Samsung PH PHP 63,990 retained",
        "priceObservations": len(prices)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
