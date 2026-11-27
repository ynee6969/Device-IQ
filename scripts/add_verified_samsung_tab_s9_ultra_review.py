#!/usr/bin/env python3
"""Record source-backed review for exact Philippine Galaxy Tab S9 Ultra configurations."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-tab-s9-ultra-ph-prices-2026-11-27.json"
IMAGE_SOURCES = ROOT / "research/catalog-image-sources.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-27"
DEVICE = "device_82e9616b879292"
MODEL = "Galaxy Tab S9 Ultra"
UNRECORDED = f"{DEVICE}-unrecorded"


def src(sid: str, url: str, publisher: str, purpose: str, note: str, published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = {
    "5g_256": src(
        "samsung_tab_s9_ultra_ph_5g_256_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-ultra-5g-graphite-256gb-sm-x916bzaaxtc/",
        "Samsung Philippines", "Exact 12 GB / 256 GB 5G Graphite SKU, technical specifications and current sales-page status",
        "Official Philippine product page identifies SKU SM-X916BZAAXTC, 12 GB / 256 GB and Galaxy Tab S9 Ultra 5G; its live page showed no current price and was labeled Not for sale."),
    "5g_512": src(
        "samsung_tab_s9_ultra_ph_5g_512_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-ultra-5g-graphite-512gb-sm-x916bzaextc/",
        "Samsung Philippines", "Exact 12 GB / 512 GB 5G Graphite SKU and technical specifications",
        "Official Philippine product page identifies SKU SM-X916BZAEXTC and the 12 GB / 512 GB 5G configuration. The page did not provide a currently available PHP offer during review."),
    "5g_1tb": src(
        "samsung_tab_s9_ultra_ph_5g_1tb_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-ultra-5g-graphite-1tb-sm-x916bzaixtc/",
        "Samsung Philippines", "Exact 16 GB / 1 TB 5G Graphite SKU and technical specifications",
        "Official Philippine product page identifies SKU SM-X916BZAIXTC and the 16 GB / 1 TB 5G configuration; its live page reported Out of Stock and no current numeric price."),
    "ph_launch_specs": src(
        "samsung_tab_s9_ph_newsroom_specs",
        "https://news.samsung.com/ph/samsung-galaxy-tab-s9-sets-the-new-standard-to-bring-galaxys-premium-experience-to-a-tablet",
        "Samsung Newsroom Philippines", "Philippine launch specification table and shared model specifications",
        "Samsung Philippines gives the S9 Ultra's 14.6-inch 2960 x 1848 display, 60-120 Hz refresh, configurations, cameras, processor, and 11,200 mAh typical battery.",
        "2023-08-02"),
    "ph_availability": src(
        "samsung_tab_s9_ph_local_availability",
        "https://news.samsung.com/ph/galaxy-tab-s9-series-the-ultimate-entertainment-experience-that-takes-you-places",
        "Samsung Newsroom Philippines", "Dated confirmation of local store and online availability",
        "Samsung Philippines reported Galaxy Tab S9 series availability through participating Philippine stores and online channels by September 6, 2023. This confirms local presence but not the date of the first general-sale transaction.",
        "2023-09-06"),
    "ph_pricing_release": src(
        "samsung_tab_s9_ph_launch_prices",
        "https://news.samsung.com/ph/bring-your-ideas-to-life-everywhere-with-the-samsung-galaxy-tab-s9-series",
        "Samsung Newsroom Philippines", "Dated Philippine official SRPs for Galaxy Tab S9 Ultra 5G storage configurations",
        "Samsung Philippines lists 5G Galaxy Tab S9 Ultra SRPs: PHP 85,990 for 12/256 GB, PHP 93,990 for 12/512 GB and PHP 112,990 for 16 GB/1 TB.",
        "2023-09-08"),
    "ph_pricing": src(
        "samsung_tab_s9_ph_preorder_terms",
        "https://www.samsung.com/ph/offer/offline/2023/galaxy-tab-s9-preorder/",
        "Samsung Philippines", "Preorder dates, early pickup window, official SRPs and exact 5G preorder offers",
        "Official preorder terms ran July 26-August 17, 2023 and allow early claims beginning August 11. The 12/512 GB 5G model had a free storage-upgrade preorder price of PHP 85,990; the 16 GB/1 TB 5G model had a PHP 9,500 discount to PHP 103,490. The 12/256 GB 5G listing had no separate preorder price.",
        "2023-07-26"),
    "global_launch": src(
        "samsung_tab_s9_global_specs",
        "https://news.samsung.com/global/samsung-galaxy-tab-s9-sets-the-new-standard-to-bring-galaxys-premium-experience-to-a-tablet",
        "Samsung Global Newsroom", "Global model launch, shared hardware features and support policy",
        "Samsung announced the Tab S9 series on July 26, 2023, naming Snapdragon 8 Gen 2 for Galaxy, IP68, Armor Aluminum and the in-box S Pen.",
        "2023-07-26"),
    "global_availability": src(
        "samsung_tab_s9_global_availability",
        "https://news.samsung.com/global/samsung-announces-global-launch-of-galaxy-z-flip5-galaxy-z-fold5-galaxy-watch6-series-and-galaxy-tab-s9-series",
        "Samsung Global Newsroom", "Dated selected-market general availability",
        "Samsung said general availability in selected markets began August 11, 2023; this is a global market date and does not imply Philippine sale.",
        "2023-08-11"),
    "charge_specs": src(
        "samsung_tab_s9_45w_charging_support",
        "https://www.samsung.com/us/support/answer/ANS10003691/",
        "Samsung Support US", "Manufacturer charging capability",
        "Samsung support states compatible Galaxy Tab S9 models support 45 W Fast Charging 2.0 with a compatible adapter and cable; this does not imply that a charger is included."),
    "sim_specs": src(
        "samsung_tab_s9_ultra_sim_and_wireless_specs",
        "https://www.samsung.com/ch/support/mobile-devices/vergleich-galaxy-tab-s9-serie/",
        "Samsung Switzerland Support", "Samsung model-family SIM and wireless-charging specifications for SM-X916B",
        "Samsung's comparison maps SM-X916B to the Tab S9 Ultra 5G and lists Nano-SIM/eSIM. Its charging table states inductive charging is not supported."),
    "processor_specs": src(
        "qualcomm_snapdragon_8_gen_2_specs",
        "https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-gen-2-mobile-platform",
        "Qualcomm", "Processor platform process and GPU specifications",
        "Qualcomm lists the Snapdragon 8 Gen 2 platform at 4 nm, up to 3.36 GHz and Adreno 740; Samsung Philippines identifies the Tab S9 Ultra's Snapdragon 8 Gen 2 for Galaxy."),
    "os_support": src(
        "samsung_tab_s9_environment_report",
        "https://www.samsung.com/global/sustainability/landing_hub-file/AY_wCQf6BaEALYNu/Galaxy_Tab_S9_Environmental_Report_EN_2503.pdf",
        "Samsung Electronics", "Manufacturer software-support commitment",
        "Samsung's Tab S9 environmental report states four generations of OS upgrades and five years of security updates."),
    "ph_2025_promo": src(
        "samsung_tab_s9_ultra_ph_2025_promo",
        "https://www.samsung.com/ph/offer/offline/2025/galaxy-tab-home-credit/",
        "Samsung Philippines", "Expired local price promotion by Tab S9 Ultra storage and model name",
        "Samsung lists S9 Ultra 256/512 GB and 1 TB SRPs and PHP 4,000 off plus a keyboard bundle for June 1-30, 2025. The source does not specify 5G/Wi-Fi by configuration, so these price observations are kept at model/storage level and not attached to a 5G variant.",
        "2025-06-01"),
    "image_rights": src(
        "samsung_tab_s9_ultra_mobile_press_terms",
        "https://www.samsungmobilepress.com/terms",
        "Samsung Mobile Press", "Product-image reuse rights review",
        "Samsung Mobile Press terms restrict copying or using site materials to personal, informational and non-commercial use and prohibit other exploitation without authorization. The Commons category reviewed contains photos taken with the tablet rather than product photographs; no exact-model product image with a reusable license was identified."),
}

CONFIGS = [
    {"id": f"{DEVICE}-sm-x916b-12gb-256gb-5g-ph", "key": "5g_256", "modelCode": "SM-X916B", "sku": "SM-X916BZAAXTC", "ram": 12, "storage": 256, "storageText": "256 GB", "network": "5G", "color": "Graphite", "weight": 737, "launch": 85990},
    {"id": f"{DEVICE}-sm-x916b-12gb-512gb-5g-ph", "key": "5g_512", "modelCode": "SM-X916B", "sku": "SM-X916BZAEXTC", "ram": 12, "storage": 512, "storageText": "512 GB", "network": "5G", "color": "Graphite", "weight": 737, "launch": 93990, "preorder": 85990, "preorderType": "historical_2023_preorder_free_storage_upgrade"},
    {"id": f"{DEVICE}-sm-x916b-16gb-1tb-5g-ph", "key": "5g_1tb", "modelCode": "SM-X916B", "sku": "SM-X916BZAIXTC", "ram": 16, "storage": 1024, "storageText": "1 TB", "network": "5G", "color": "Graphite", "weight": 737, "launch": 112990, "preorder": 103490, "preorderType": "historical_2023_preorder_discount"},
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
    label = f"{config['ram']} GB RAM / {config['storageText']} storage · 5G · Graphite"
    local_config_note = "Exact Samsung Philippines model code, color and RAM/storage configuration matched to the official SKU page and Philippine launch/preorder sources."
    fields: list[dict] = []

    def add(fid, source_key, value, normalized=None, **kwargs):
        fields.append(field(fid, SOURCES[source_key]["id"], value, normalized, **kwargs))

    def unavailable(fid, source_key, value, note, *, status="NOT_DISCLOSED", unit=None):
        fields.append(missing(fid, SOURCES[source_key]["id"], value, note, status=status, unit=unit))

    add("model_number", sid, config["modelCode"], config["modelCode"], note=local_config_note)
    add("global_release_date", "global_availability", "Samsung selected-market general availability began 2023-08-11", "2023-08-11",
        note="Samsung names August 11, 2023 for selected global markets. This does not establish the first general sale in every market.")
    add("configuration", sid, label, label, note=local_config_note)
    add("philippine_release_date", "ph_pricing", "Preordered Tab S9 units could be claimed from 2023-08-11", "2023-08-11",
        note="August 11 is the earliest local preorder claim date documented in Samsung Philippines' terms, not a verified date of first general retail sale. Samsung later reported local store and online availability by September 6, 2023.")
    add("official_launch_price_php", "ph_pricing_release", f"PHP {config['launch']:,} official Philippine SRP for {label}", config["launch"], unit="PHP",
        note="Historical 2023 Philippine SRP explicitly listed for this exact 5G RAM/storage configuration; it is not a current offer.")
    unavailable("current_price_php", sid,
                "No current exact-SKU PHP sale price was verifiable on November 27, 2026.",
                "Samsung Philippines' 256 GB product page showed Not for sale and its 1 TB page showed Out of Stock; the official 512 GB page did not provide a current numeric PHP offer in the reviewed page. Historical launch and expired promotion prices are not current prices.",
                status="PENDING_VERIFICATION", unit="PHP")

    add("display_size", sid, "14.6 inches (full rectangle)", 14.6, key="displayInches", unit="in",
        note="Samsung lists 14.6 inches measured diagonally across the full rectangle.")
    add("display_technology", sid, "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType")
    add("display_resolution", sid, "2960 x 1848 (WQXGA+)", "2960 x 1848", key="resolution")
    add("display_refresh_rate", "ph_launch_specs", "Dynamic refresh rate from 60 to 120 Hz", 120, key="refreshHz", unit="Hz",
        note="Samsung describes a dynamic refresh rate up to 120 Hz; catalog numeric field stores the maximum refresh rate.")
    unavailable("display_brightness", sid, "Samsung does not publish a numeric brightness rating on the reviewed local SKU pages.",
                "No peak or typical nit value is inferred.", unit="nits")
    unavailable("display_protection", sid, "The reviewed Samsung Philippines specifications do not identify a display-glass protection material or version.",
                "No Gorilla Glass generation or other protection type is inferred.")
    add("chipset", sid, "Qualcomm Snapdragon 8 Gen 2 for Galaxy", "Qualcomm Snapdragon 8 Gen 2 for Galaxy", key="chipset")
    add("process_node", "processor_specs", "Qualcomm lists Snapdragon 8 Gen 2 at 4 nm", 4, unit="nm",
        note="Qualcomm is the platform manufacturer; Samsung's exact Philippine SKU pages identify Snapdragon 8 Gen 2 for Galaxy.")
    add("cpu", sid, "Octa-core; CPU speed groups 3.36 GHz, 2.8 GHz and 2.0 GHz", "Octa-core; 3.36 GHz / 2.8 GHz / 2.0 GHz",
        note="Samsung Philippines lists these CPU frequencies and an octa-core CPU on the exact local product page.")
    add("gpu", "processor_specs", "Qualcomm lists Adreno 740 for Snapdragon 8 Gen 2", "Adreno 740",
        note="Qualcomm's platform specification identifies Adreno 740; Samsung identifies the same Snapdragon 8 Gen 2 platform in this device.")
    add("operating_system", "sim_specs", "Android 13.0 with One UI 5.1.1 at launch", "Android 13", key="os",
        note="Samsung's model-family comparison lists Android 13.0 / One UI 5.1.1 as the factory OS for model family SM-X916B/SM-X910.")
    add("os_support", "os_support", "Four generations of One UI and Android OS upgrades; five years of security updates", "Up to 4 OS generations; 5 years of security updates",
        note="Samsung's launch-era product environmental report states the support commitment; this is not a claim that all future support remains active indefinitely.")
    add("ram_capacity", sid, f"{config['ram']} GB", config["ram"], key="ramGb", unit="GB")
    unavailable("ram_type", sid, "Samsung does not state the RAM technology type on the reviewed official specifications.",
                "The exact capacity is recorded; RAM type is not inferred.")
    add("storage_capacity", sid, config["storageText"], config["storage"], key="storageGb", unit="GB",
        note="Samsung's official 5G SKU page identifies the exact internal storage configuration.")
    unavailable("storage_type", sid, "Samsung does not identify the internal storage technology on the reviewed local SKU page.",
                "No UFS generation is inferred.")
    add("storage_expansion", sid, "MicroSD card support up to 1 TB", "microSD supported up to 1 TB")
    add("rear_camera_system", sid, "13 MP autofocus main wide + 8 MP rear ultra-wide", 13, key="rearCameraMp", unit="MP",
        note="Samsung lists both a 13 MP autofocus main camera and an 8 MP rear ultra-wide camera.")
    unavailable("main_camera_sensor", sid, "Samsung does not identify the image-sensor part numbers in its specifications.",
                "Camera roles and resolution are documented; no sensor part number is inferred.")
    add("ultrawide_camera", sid, "8 MP rear ultra-wide camera", "8 MP rear ultra-wide")
    add("telephoto_camera", sid, "Samsung lists two rear cameras (wide and ultra-wide) and no telephoto module", "No telephoto camera", status="NOT_APPLICABLE")
    add("front_camera", sid, "12 MP wide + 12 MP ultra-wide front cameras", "12 MP wide + 12 MP ultra-wide", key="frontCameraMp", unit="MP")
    add("video_recording", sid, "Rear video: UHD 4K (3840 x 2160) at 30 fps", "Rear video up to 4K / 30 fps", key="video")
    add("battery_capacity", sid, "11,200 mAh typical; 10,880 mAh rated/minimum", 11200, key="batteryMah", unit="mAh",
        note="Samsung's Philippine specification page lists 11,200 mAh typical and 10,880 mAh rated/minimum capacity.")
    unavailable("battery_technology", sid, "Samsung does not state battery cell chemistry in the reviewed specifications.",
                "Only published capacity is recorded; cell chemistry is not inferred.")
    add("wired_charging", "charge_specs", "45 W Fast Charging 2.0 with a compatible adapter and cable", 45, key="chargingW", unit="W",
        note="Samsung specifies 45 W charging capability; a compatible adapter and cable are required and may not be included.")
    add("wireless_charging", "sim_specs", "Samsung lists inductive/wireless charging as unsupported", "No wireless charging",
        note="Samsung Switzerland's Tab S9 model-family comparison explicitly says inductive charging is not supported.")
    add("dimensions", sid, "208.6 x 326.4 x 5.5 mm", "208.6 x 326.4 x 5.5 mm", key="dimensions", unit="mm")
    add("weight", sid, "737 g (5G model)", 737, key="weightG", unit="g",
        note="Samsung Philippines specifies 737 g for this 5G SKU; the distinct Wi-Fi model is listed at 732 g but is not treated as a local SKU here.")
    add("materials", "global_launch", "Armor Aluminum frame", "Armor Aluminum frame")
    add("ingress_protection", sid, "IP68", "IP68")
    add("sim_esim", "sim_specs", "Nano-SIM (4FF) + eSIM for SM-X916B 5G", "Nano-SIM + eSIM", key="sim",
        note="Samsung's manufacturer comparison maps SM-X916B to the 5G model and lists a Nano-SIM and eSIM.")
    add("cellular_bands", sid, CELLULAR_BANDS, CELLULAR_BANDS,
        note="Band list is from the Samsung Philippines SM-X916B product specification page.")
    add("tablet_cellular_variant", sid, "5G cellular model", "5G cellular", key="cellular")
    add("wifi", sid, "802.11 a/b/g/n/ac/ax across 2.4, 5 and 6 GHz; Wi-Fi 6E", "Wi-Fi 6E", key="wifi")
    add("bluetooth", sid, "Bluetooth 5.3", "Bluetooth 5.3", key="bluetooth")
    add("usb", sid, "USB Type-C; USB 3.2 Gen 1", "USB Type-C; USB 3.2 Gen 1", key="ports")
    add("nfc", sid, "NFC: No", "No NFC")
    add("gnss", sid, "GPS, GLONASS, BeiDou, Galileo and QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS")
    add("audio", "ph_launch_specs", "Quad speakers with AKG tuning and Dolby Atmos", "Quad speakers; AKG tuning; Dolby Atmos", key="sound")
    add("sensors", sid, "Accelerometer, fingerprint, gyroscope, geomagnetic, Hall and light sensors", "Accelerometer; fingerprint; gyroscope; geomagnetic; Hall; light")
    add("tablet_stylus", "global_launch", "IP68-rated S Pen included in the box", "S Pen included", key="stylus")
    add("tablet_keyboard", sid, "Book Cover Keyboard supported; sold separately", "Book Cover Keyboard supported; sold separately", key="keyboard",
        note="Keyboard support is a model feature; historical promotion bundles are recorded separately and do not make the keyboard an included accessory for every sale.")

    if len(fields) != 49:
        raise ValueError(f"Expected 49 reviewed fields for {label}, found {len(fields)}")
    sources = list(SOURCES.values())
    variants = [{"id": c["id"], "label": f"{c['ram']} GB RAM / {c['storageText']} storage · 5G · Graphite",
                 "sku": c["sku"], "modelCode": c["modelCode"],
                 "notes": "Exact Samsung Philippines 5G SKU verified on the local product page."}
                for c in CONFIGS]
    item = {"deviceId": DEVICE, "configurationId": config["id"], "brand": "Samsung", "model": MODEL,
            "configuration": label, "modelCode": config["modelCode"], "sku": config["sku"],
            "sources": sources, "fields": fields,
            "availabilityEvidence": {
                "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                "availabilityStatus": "Authorized PH preorder claim from 2023-08-11; local store and online availability reported by 2023-09-06.",
                "philippineAvailabilityDate": "2023-08-11",
                "philippineDateLabel": "Earliest preorder pickup",
                "philippineAvailability": "Samsung Philippines preorder terms allow Tab S9 series preorder claims beginning August 11, 2023; Samsung's September 6, 2023 newsroom article reports local store and online availability. Exact first general-sale date unresolved.",
                "observedAt": "2023-09-06", "philippineReleaseYear": 2023,
                "catalogModel": MODEL,
                "qualityFlag": "Earliest preorder pickup documented; exact first general-sale date unresolved.",
                "openIssues": [{"issue": "Exact date of first general retail sale was not found.",
                                "action": "Retain August 11, 2023 as earliest documented preorder pickup; do not label it the first retail sale."}],
            }}
    item["replacementVariants"] = variants
    return item


def price_rows() -> list[dict]:
    rows = []
    for config in CONFIGS:
        common = {"device_id": DEVICE, "configuration_id": config["id"],
                  "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
                  "variant_connectivity": "5G",
                  "configuration_match": f"exact_{config['ram']}gb_{config['storage']}gb_5g"}
        rows.append({**common, "amount_php": config["launch"],
                     "price_type": "historical_ph_official_srp", "source_published_at": "2023-09-08",
                     "observed_at": OBSERVED, "source_url": SOURCES["ph_pricing_release"]["url"],
                     "source_kind": "official_samsung_ph_launch_price", "local_availability_verified": True,
                     "availability_status": "historical_launch_srp_not_current", "review_status": "VERIFIED",
                     "excerpt": f"Samsung Philippines lists PHP {config['launch']:,} SRP for the exact {config['ram']} GB / {config['storageText']} 5G Galaxy Tab S9 Ultra configuration."})
        if config.get("preorder"):
            offer_type = config["preorderType"]
            if offer_type == "historical_2023_preorder_free_storage_upgrade":
                offer_note = "after a free upgrade from the 256 GB configuration"
                status = "expired_2023_preorder_256gb_base_upgraded_to_512gb_offer_not_current"
            else:
                offer_note = "after the published PHP 9,500 discount on the 1 TB model"
                status = "expired_2023_preorder_9500_discount_not_current"
            rows.append({**common, "amount_php": config["preorder"],
                         "price_type": offer_type,
                         "source_published_at": "2023-07-26", "observed_at": OBSERVED,
                         "source_url": SOURCES["ph_pricing"]["url"], "source_kind": "official_samsung_ph_preorder_price",
                         "local_availability_verified": True, "availability_status": status,
                         "review_status": "VERIFIED",
                         "excerpt": f"Samsung Philippines listed PHP {config['preorder']:,} for the exact {config['ram']} GB / {config['storageText']} 5G Tab S9 Ultra preorder {offer_note}; offer period July 26-August 17, 2023."})

    # The 2025 Samsung promotion names model and storage price rows but omits
    # connectivity, so retain those observations at model/storage level only.
    for config in CONFIGS:
        srp = config["launch"]
        rows.append({"device_id": DEVICE, "configuration_id": None,
                     "variant_ram_gb": None, "variant_storage_gb": config["storage"],
                     "variant_connectivity": None,
                     "configuration_match": f"exact_model_{config['storageText'].lower().replace(' ', '')}_storage_connectivity_unspecified",
                     "amount_php": srp - 4000,
                     "price_type": "historical_2025_promo_price_arithmetic_connectivity_unspecified",
                     "source_published_at": "2025-06-01", "observed_at": OBSERVED,
                     "source_url": SOURCES["ph_2025_promo"]["url"],
                     "source_kind": "official_samsung_ph_discount_terms_arithmetic",
                     "local_availability_verified": True,
                     "availability_status": "expired_2025_06_01_to_2025_06_30_offer_not_current",
                     "review_status": "VERIFIED",
                     "excerpt": f"Samsung Philippines' June 2025 offer lists Galaxy Tab S9 Ultra {config['storageText']} SRP PHP {srp:,} and PHP 4,000 off plus a keyboard bundle. Calculated PHP {srp - 4000:,}; source does not specify Wi-Fi or 5G, so this model/storage price is not linked to an exact variant."})
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
        "reason": "No exact-model device product photo with a reusable license was found. The Wikimedia Commons category reviewed contains photographs taken with the Tab S9 Ultra, not product images. Samsung Mobile Press terms restrict site material to personal, informational, non-commercial use and do not grant reuse for a public product catalog.",
        "sourcePage": SOURCES["5g_256"]["url"],
        "assetUrl": "https://images.samsung.com/is/image/samsung/p6pim/ph/sm-x916bzaaxtc/gallery/ph-galaxy-tab-s9-ultra-5g-x916-sm-x916bzaaxtc-thumb-538124151",
        "scope": "Galaxy Tab S9 Ultra model family; no image reused because exact-model product-image rights were not cleared.",
        "rightsTermsUrl": SOURCES["image_rights"]["url"],
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Samsung Galaxy Tab S9 Ultra",
    }
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Included":
        raise ValueError("Expected the Included workbook Galaxy Tab S9 Ultra record; refusing unexpected scope/device.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {v["id"] for v in CONFIGS}
    replacing = current_ids == {UNRECORDED}
    already_integrated = current_ids == expected_ids
    if not (replacing or already_integrated):
        raise ValueError(f"Unexpected Galaxy Tab S9 Ultra configurations; refusing: {sorted(current_ids)}")

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
                      "configuration": f"{config['ram']} GB RAM / {config['storageText']} storage · {config['network']} · {config['color']}",
                      "configurationLabel": f"{config['ram']} GB RAM / {config['storageText']} storage · {config['network']} · {config['color']}"})
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
        {"configuration": f"{c['ram']} GB RAM / {c['storageText']} storage · {c['network']} · {c['color']}",
         "sku": c["sku"], "launchSrpPhp": c["launch"], "currentListedPricePhp": c.get("current"),
         "currentPriceObservedAt": c.get("currentDate"), "scope": "Included"} for c in CONFIGS],
        "reviewedConfigurations": len(CONFIGS), "reviewedFieldsPerConfiguration": 49,
        "availability": "Authorized PH preorder pickup from 2023-08-11; first general-sale date unresolved",
        "image": "Unavailable: no exact-model reusable image rights found; neutral placeholder retained",
        "launchPriceConflict": "No conflict found among the reviewed official Philippine launch SRPs",
        "priceObservations": len(prices)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
