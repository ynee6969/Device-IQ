#!/usr/bin/env python3
"""Record source-backed review for exact Philippine Galaxy Tab S9+ configurations."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-tab-s9-plus-ph-prices-2026-11-27.json"
IMAGE_SOURCES = ROOT / "research/catalog-image-sources.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-27"
DEVICE = "device_3bdcbc7b1b3d1b"
MODEL = "Galaxy Tab S9+"
UNRECORDED = f"{DEVICE}-unrecorded"


def src(sid: str, url: str, publisher: str, purpose: str, note: str, published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = {
    "wifi_256": src(
        "samsung_tab_s9_plus_ph_wifi_256_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-plus-wi-fi-graphite-256gb-sm-x810nzaaxtc/",
        "Samsung Philippines", "Exact 12 GB / 256 GB Wi-Fi Philippine SKU and product specifications",
        "Official Philippine product page identifies Graphite SKU SM-X810NZAA XTC and the 12 GB / 256 GB Wi-Fi configuration."),
    "wifi_512": src(
        "samsung_tab_s9_plus_ph_wifi_512_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-plus-wi-fi-graphite-512gb-sm-x810nzaextc/",
        "Samsung Philippines", "Exact 12 GB / 512 GB Wi-Fi Philippine SKU and product specifications",
        "Official Philippine product page identifies Graphite SKU SM-X810NZAE XTC and the 12 GB / 512 GB Wi-Fi configuration."),
    "5g_256": src(
        "samsung_tab_s9_plus_ph_5g_256_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-plus-5g-graphite-256gb-sm-x816bzaaxtc/",
        "Samsung Philippines", "Exact 12 GB / 256 GB 5G Philippine SKU and product specifications",
        "Official Philippine product page identifies Graphite SKU SM-X816BZAA XTC and the 12 GB / 256 GB 5G configuration. Its specifications page includes local cellular bands."),
    "5g_512": src(
        "samsung_tab_s9_plus_ph_5g_512_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-plus-5g-graphite-512gb-sm-x816bzaextc/",
        "Samsung Philippines", "Exact 12 GB / 512 GB 5G Philippine SKU and product specifications",
        "Official Philippine product page identifies Graphite SKU SM-X816BZAE XTC and the 12 GB / 512 GB 5G configuration."),
    "ph_launch_specs": src(
        "samsung_tab_s9_ph_newsroom_specs",
        "https://news.samsung.com/ph/samsung-galaxy-tab-s9-sets-the-new-standard-to-bring-galaxys-premium-experience-to-a-tablet",
        "Samsung Newsroom Philippines", "Local configuration table and launch specifications",
        "Samsung Philippines lists the 12.4-inch Dynamic AMOLED 2X display, 60–120 Hz refresh rate, dimensions, Wi-Fi/5G weights, dual rear cameras, 12/256 and 12/512 GB versions, processor and 10,090 mAh typical battery.",
        "2023-09-06"),
    "ph_pricing": src(
        "samsung_tab_s9_ph_preorder_terms",
        "https://www.samsung.com/ph/offer/offline/2023/galaxy-tab-s9-preorder/",
        "Samsung Philippines", "Authorized local preorder window, pickup timing, SRPs and preorder offers",
        "Official terms show the July 26–August 17, 2023 local preorder period; customers could get preorder units as early as August 11. Tab S9+ 256 GB preorders qualified for a free upgrade to 512 GB; the listed 512 GB preorder price was PHP 61,990 Wi-Fi or PHP 70,990 5G.",
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
        "Samsung Newsroom Philippines published Tab S9+ SRPs on September 8, 2023: Wi-Fi 12/256 PHP 61,990, Wi-Fi 12/512 PHP 69,990, 5G 12/256 PHP 70,990, and 5G 12/512 PHP 78,990.",
        "2023-09-08"),
    "global_launch": src(
        "samsung_tab_s9_global_launch",
        "https://news.samsung.com/global/samsung-galaxy-tab-s9-sets-the-new-standard-to-bring-galaxys-premium-experience-to-a-tablet",
        "Samsung Global Newsroom", "Global announcement, availability timing, support policy and shared model specifications",
        "Samsung announced the Tab S9 series July 26, 2023. It identifies the Snapdragon 8 Gen 2 for Galaxy, IP68, included S Pen, Armor Aluminum and four OS generations plus five years of security updates.",
        "2023-07-26"),
    "global_availability": src(
        "samsung_tab_s9_global_availability",
        "https://news.samsung.com/global/samsung-announces-global-launch-of-galaxy-z-flip5-galaxy-z-fold5-galaxy-watch6-series-and-galaxy-tab-s9-series",
        "Samsung Global Newsroom", "Global market availability start date",
        "Samsung says general availability in selected markets began August 11, 2023; additional markets followed later.",
        "2023-08-11"),
    "charge_specs": src(
        "samsung_tab_s9_45w_charging_support",
        "https://www.samsung.com/us/support/answer/ANS10003691/",
        "Samsung Support US", "Manufacturer charging capability",
        "Samsung support states that Galaxy Tab S9 models support 45 W Fast Charging 2.0 with a compatible charger and cable. This does not imply the charger is included."),
    "sim_specs": src(
        "samsung_tab_s9_5g_sim_esim_specs",
        "https://www.samsung.com/ch/support/mobile-devices/vergleich-galaxy-tab-s9-serie/",
        "Samsung Switzerland Support", "Manufacturer SIM capability for model codes SM-X816B / SM-X810",
        "Samsung's model-family table maps SM-X816B to the cellular model and identifies Nano-SIM (4FF) plus eSIM. The Wi-Fi-only SM-X810 does not take a SIM."),
    "processor_specs": src(
        "qualcomm_snapdragon_8_gen_2_specs",
        "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-gen-2-mobile-platform",
        "Qualcomm", "Chip process and platform-level technical details",
        "Qualcomm lists the Snapdragon 8 Gen 2 at 4 nm and a maximum CPU frequency up to 3.36 GHz; Samsung's exact Galaxy Tab S9+ local product pages identify the Snapdragon 8 Gen 2 for Galaxy."),
    "os_support": src(
        "samsung_tab_s9_environment_report",
        "https://www.samsung.com/global/sustainability/landing_hub-file/AY_wCQf6BaEALYNu/Galaxy_Tab_S9_Environmental_Report_EN_2503.pdf",
        "Samsung Electronics", "Manufacturer software support commitment",
        "Samsung's Galaxy Tab S9 product environmental report says four generations of OS upgrades and five years of security updates."),
    "ph_2025_promo": src(
        "samsung_tab_s9_ph_2025_promo",
        "https://www.samsung.com/ph/offer/offline/2025/galaxy-tab-home-credit/",
        "Samsung Philippines", "Dated official local discount terms by storage and connectivity variant",
        "Expired offer valid June 1–30, 2025. Samsung's terms list the exact Tab S9+ Wi-Fi/5G 256/512 GB SRPs and PHP 4,000 discounts; arithmetic prices are historical and not current offers.",
        "2025-06-01"),
    "price_shopee": src(
        "shopee_kimstore_s9_plus_5g_256_price",
        "https://shopee.ph/Samsung-Galaxy-Tab-S9-5G-X816-(12GB-256GB)-i.80090165.22581857040",
        "Shopee Philippines; seller shown as Kimstore", "Dated sold-out listing for exact Tab S9+ 5G 12 GB / 256 GB price observation",
        "Shopee displays PHP 70,985 and marks this exact Galaxy Tab S9+ 5G X816 12 GB / 256 GB listing Sold Out. Kimstore is the named seller; item condition and a usable current offer were not verified."),
    "image_rights": src(
        "samsung_tab_s9_plus_image_reuse_terms",
        "https://www.samsung.com/ph/business/info/legal/",
        "Samsung Philippines", "Rights review for official product image",
        "Samsung's site legal notice says Samsung or its licensors own site content and does not grant a reusable license for the product photograph. No exact-model openly licensed image was located in the reviewed Commons search; the public catalog keeps the neutral placeholder."),
}

CONFIGS = [
    {"id": f"{DEVICE}-sm-x810-12gb-256gb-wifi-ph", "key": "wifi_256", "modelCode": "SM-X810", "sku": "SM-X810NZAA XTC", "ram": 12, "storage": 256, "network": "Wi-Fi", "weight": 581, "launch": 61990, "promoDiscount": 4000},
    {"id": f"{DEVICE}-sm-x810-12gb-512gb-wifi-ph", "key": "wifi_512", "modelCode": "SM-X810", "sku": "SM-X810NZAE XTC", "ram": 12, "storage": 512, "network": "Wi-Fi", "weight": 581, "launch": 69990, "promoDiscount": 4000, "preorder": 61990},
    {"id": f"{DEVICE}-sm-x816b-12gb-256gb-5g-ph", "key": "5g_256", "modelCode": "SM-X816B", "sku": "SM-X816BZAA XTC", "ram": 12, "storage": 256, "network": "5G", "weight": 586, "launch": 70990, "promoDiscount": 4000},
    {"id": f"{DEVICE}-sm-x816b-12gb-512gb-5g-ph", "key": "5g_512", "modelCode": "SM-X816B", "sku": "SM-X816BZAE XTC", "ram": 12, "storage": 512, "network": "5G", "weight": 586, "launch": 78990, "promoDiscount": 4000, "preorder": 70990},
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

    add("model_number", sid, config["modelCode"], config["modelCode"], note=local_config_note)
    add("global_release_date", "global_availability", "General availability in selected global markets began 2023-08-11", "2023-08-11",
        note="Samsung identifies August 11, 2023 as the start of availability in selected global markets. Another Samsung announcement refers to broader general availability from August 17; this date does not imply release in every market.")
    add("configuration", sid, label, label, note=local_config_note)
    add("philippine_release_date", "ph_pricing", "Samsung says preorder units could be collected as early as 2023-08-11", "2023-08-11",
        note="This is the earliest local preorder-unit pickup date documented by Samsung Philippines, not a verified date of the first general retail sale. Samsung later reported local store and online availability by September 6, 2023.")
    add("official_launch_price_php", "ph_pricing_release", f"PHP {config['launch']:,} official Philippine SRP for {label}", config["launch"], unit="PHP",
        note="Historical Philippine SRP in Samsung Philippines' dated local price table. This launch-era value is not a current offer.")
    unavailable("current_price_php", "ph_2025_promo",
                "No exact-configuration Philippine offer was verified as currently available on November 27, 2026.",
                "The latest reviewed official offer is dated June 2025 and expired. A sold-out 5G 12 GB / 256 GB Shopee listing is retained separately as a dated price observation; it is not promoted as an available price.",
                status="PENDING_VERIFICATION", unit="PHP")

    add("display_size", sid, "12.4 inches (full rectangle)", 12.4, key="displayInches", unit="in",
        note="Samsung lists a 12.4-inch full-rectangle display size.")
    add("display_technology", sid, "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType")
    add("display_resolution", sid, "2800 x 1752 (WQXGA+)", "2800 x 1752", key="resolution")
    add("display_refresh_rate", "ph_launch_specs", "Dynamic refresh rate from 60 to 120 Hz", 120, key="refreshHz", unit="Hz",
        note="Samsung says the panel dynamically adjusts from 60 to 120 Hz; the catalog numeric value records the maximum refresh rate.")
    unavailable("display_brightness", sid, "Samsung Philippines does not publish a numeric brightness rating for this model.",
                "No peak or typical nits value is inferred.", status="NOT_DISCLOSED", unit="nits")
    unavailable("display_protection", sid, "The reviewed Samsung Philippines product specifications do not name a display-glass protection material or version.",
                "No Gorilla Glass generation or other display-protection type is inferred.")
    add("chipset", sid, "Qualcomm Snapdragon 8 Gen 2 for Galaxy", "Qualcomm Snapdragon 8 Gen 2 for Galaxy", key="chipset")
    add("process_node", "processor_specs", "Qualcomm lists the Snapdragon 8 Gen 2 platform at 4 nm", 4, unit="nm",
        note="Qualcomm is the chip platform manufacturer; Samsung's local product pages name the Snapdragon 8 Gen 2 for Galaxy.")
    add("cpu", sid, "Octa-core; CPU speed groups 3.36 GHz, 2.8 GHz and 2.0 GHz", "Octa-core; 3.36 GHz / 2.8 GHz / 2.0 GHz",
        note="Samsung Philippines lists these CPU speeds and an octa-core CPU on the exact local SKU page.")
    add("gpu", "processor_specs", "Qualcomm Snapdragon 8 Gen 2 platform GPU: Adreno 740", "Adreno 740",
        note="Qualcomm's platform page lists the Adreno 740 GPU for Snapdragon 8 Gen 2.")
    add("operating_system", "ph_launch_specs", "Android 13.0 at launch", "Android 13", key="os",
        note="Samsung Philippines lists Android 13.0 in the local launch specification table; later updates are not substituted for launch software.")
    add("os_support", "os_support", "Four generations of One UI and Android OS upgrades; five years of security updates", "Up to 4 OS generations; 5 years of security updates",
        note="Manufacturer support commitment from Samsung's Galaxy Tab S9 product environmental report. This is the launch policy, not a statement that future updates remain available indefinitely.")
    add("ram_capacity", sid, f"{config['ram']} GB", config["ram"], key="ramGb", unit="GB")
    unavailable("ram_type", sid, "RAM technology is not stated on the reviewed Samsung Philippines product pages.",
                "The verified 12 GB capacity is retained; RAM type is not inferred.")
    add("storage_capacity", sid, f"{config['storage']} GB", config["storage"], key="storageGb", unit="GB")
    unavailable("storage_type", sid, "The reviewed Samsung Philippines product pages do not identify the internal storage technology.",
                "No UFS generation is inferred.")
    add("storage_expansion", sid, "MicroSD card support up to 1 TB", "microSD supported up to 1 TB")
    add("rear_camera_system", sid, "13 MP autofocus main wide + 8 MP rear ultra-wide", 13, key="rearCameraMp", unit="MP",
        note="Samsung Philippines lists a 13 MP autofocus main rear camera and a separate 8 MP ultra-wide rear camera.")
    unavailable("main_camera_sensor", sid, "Samsung does not identify the exact image sensor component in its reviewed specifications.",
                "The lens role and megapixel resolution are documented; a sensor part number is not inferred.")
    add("ultrawide_camera", sid, "8 MP rear ultra-wide camera", "8 MP rear ultra-wide", status="VERIFIED")
    add("telephoto_camera", sid, "The official rear-camera specification lists main wide and ultra-wide cameras and no telephoto module", "No telephoto camera", status="NOT_APPLICABLE")
    add("front_camera", "ph_launch_specs", "12 MP ultra-wide front camera", "12 MP ultra-wide", key="frontCameraMp", unit="MP")
    add("video_recording", sid, "Rear video: UHD 4K (3840 x 2160) at 30 fps", "Rear video up to 4K / 30 fps", key="video")
    add("battery_capacity", sid, "10,090 mAh typical; 9,800 mAh rated/minimum", 10090, key="batteryMah", unit="mAh",
        note="Samsung states 10,090 mAh typical capacity and 9,800 mAh rated/minimum capacity.")
    unavailable("battery_technology", sid, "Samsung does not disclose the battery chemistry in the reviewed model specifications.",
                "The capacity and rated minimum are documented; cell chemistry is not inferred.")
    add("wired_charging", "charge_specs", "45 W Fast Charging 2.0 with a compatible adapter and cable", 45, key="chargingW", unit="W",
        note="Samsung support lists 45 W capability. A compatible charger and cable are required; this does not state they are included.")
    unavailable("wireless_charging", sid, "Wireless charging capability is not stated on the reviewed manufacturer pages.",
                "Samsung's specification table does not list wireless charging, so absence is not asserted as a confirmed unsupported feature.", status="PENDING_VERIFICATION")
    add("dimensions", sid, "185.4 x 285.4 x 5.7 mm", "185.4 x 285.4 x 5.7 mm", key="dimensions", unit="mm")
    add("weight", sid, f"{config['weight']} g ({network} model)", config["weight"], key="weightG", unit="g",
        note="Samsung lists 581 g for Wi-Fi and 586 g for 5G models.")
    add("materials", "global_launch", "Armor Aluminum frame", "Armor Aluminum frame")
    add("ingress_protection", sid, "IP68", "IP68")
    if wifi_only:
        add("sim_esim", "sim_specs", "SM-X810 Wi-Fi-only SKU; no SIM or eSIM", "No SIM; Wi-Fi only", key="sim")
        unavailable("cellular_bands", sid, "Not applicable: this local SKU is Wi-Fi-only.",
                    "No cellular modem is included in the SM-X810 Wi-Fi configuration.", status="NOT_APPLICABLE")
        add("tablet_cellular_variant", sid, "Wi-Fi-only model", "Wi-Fi only", key="cellular")
    else:
        add("sim_esim", "sim_specs", "Nano-SIM (4FF) and eSIM", "Nano-SIM + eSIM", key="sim",
            note="Samsung Switzerland documents Nano-SIM + eSIM for model code SM-X816B; the exact Philippine SKU page identifies this 5G model code.")
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
                     "excerpt": f"Samsung Philippines lists PHP {config['launch']:,} SRP for {config['ram']} GB / {config['storage']} GB {config['network']} Galaxy Tab S9+."})
        discount_price = config["launch"] - config["promoDiscount"]
        rows.append({**common, "amount_php": discount_price,
                     "price_type": "historical_2025_promo_price_calculated_from_published_srp_and_discount",
                     "source_published_at": "2025-06-01", "observed_at": OBSERVED,
                     "source_url": promo_source, "source_kind": "official_samsung_ph_discount_terms_arithmetic",
                     "local_availability_verified": True,
                     "availability_status": "expired_2025_06_01_to_2025_06_30_offer_not_current",
                     "review_status": "VERIFIED",
                     "excerpt": f"Samsung Philippines' June 1–30, 2025 terms list PHP {config['launch']:,} SRP and PHP {config['promoDiscount']:,} off for this exact Tab S9+ configuration; PHP {discount_price:,} is calculated arithmetic and is not a current offer."})
        if config.get("preorder"):
            rows.append({**common, "amount_php": config["preorder"],
                         "price_type": "historical_2023_preorder_price_with_free_storage_upgrade",
                         "source_published_at": "2023-07-26", "observed_at": OBSERVED,
                         "source_url": launch_source, "source_kind": "official_samsung_ph_preorder_price",
                         "local_availability_verified": True,
                         "availability_status": "expired_2023_preorder_256gb_base_upgraded_to_512gb_offer_not_current",
                         "review_status": "VERIFIED",
                         "excerpt": f"Samsung Philippines listed PHP {config['preorder']:,} for the 12 GB / 512 GB {config['network']} Tab S9+ preorder configuration after a free upgrade from the 256 GB model; the offer ran July 26–August 17, 2023."})
    c256 = next(c for c in CONFIGS if c["key"] == "5g_256")
    rows.append({"device_id": DEVICE, "configuration_id": c256["id"], "amount_php": 70985,
                 "variant_ram_gb": 12, "variant_storage_gb": 256, "variant_connectivity": "5G",
                 "configuration_match": "exact_12gb_256gb_5g", "price_type": "dated_sold_out_retailer_listing_not_current_price",
                 "source_published_at": None, "observed_at": OBSERVED, "source_url": SOURCES["price_shopee"]["url"],
                 "source_kind": "shopee_ph_sold_out_kimstore_listing", "local_availability_verified": False,
                 "availability_status": "sold_out_when_page_accessed_2026_11_27_item_condition_not_stated",
                 "review_status": "PENDING_VERIFICATION",
                 "excerpt": "Shopee displayed PHP 70,985 for the exact Galaxy Tab S9+ 5G X816 12 GB / 256 GB listing by Kimstore but marked it Sold Out. The item condition was not stated; do not treat this as an available current price."})
    return rows


def update_image_sources() -> None:
    sources = json.loads(IMAGE_SOURCES.read_text(encoding="utf-8"))
    sources = [row for row in sources if row.get("deviceId") != DEVICE]
    IMAGE_SOURCES.write_text("[\n" + ",\n".join(
        "  " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in sources
    ) + "\n]\n", encoding="utf-8")
    unavailable = json.loads(IMAGE_UNAVAILABLE.read_text(encoding="utf-8"))
    unavailable[DEVICE] = {
        "status": "REUSE_PERMISSION_REQUIRED",
        "reason": "Samsung owns or licenses its product-site images and does not grant reuse permission for this product photograph; no exact-model openly licensed image was located in the reviewed Wikimedia Commons search.",
        "sourcePage": SOURCES["5g_256"]["url"],
        "scope": "Galaxy Tab S9+ model family; no image reused because exact-model product-image rights were not cleared.",
        "rightsTermsUrl": SOURCES["image_rights"]["url"],
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Samsung Galaxy Tab S9+",
    }
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Included":
        raise ValueError("Expected the Included workbook Galaxy Tab S9+ record; refusing unexpected scope/device.")
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
        "image": "Unavailable: no exact-model reusable image rights found; neutral placeholder retained",
        "launchPriceConflict": "No conflict found among the reviewed official Philippine launch SRPs",
        "priceObservations": len(prices)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
