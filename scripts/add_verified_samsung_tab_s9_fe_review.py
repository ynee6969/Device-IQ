#!/usr/bin/env python3
"""Record source-backed review for exact Philippine Galaxy Tab S9 FE SKUs."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-tab-s9-fe-ph-prices-2026-11-27.json"
IMAGE_SOURCES = ROOT / "research/catalog-image-sources.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-27"
DEVICE = "device_33bf4ec88cc229"
MODEL = "Galaxy Tab S9 FE"
UNRECORDED = f"{DEVICE}-unrecorded"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = {
    "wifi": src(
        "samsung_tab_s9_fe_ph_wifi_128_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-fe-wifi-gray-128gb-sm-x510nzaaxtc/",
        "Samsung Philippines", "Exact Wi-Fi 6 GB / 128 GB Philippine SKU, product features and specifications",
        "Official Philippine page identifies Gray Wi-Fi SKU SM-X510NZAAXTC and lists its 6 GB RAM, 128 GB storage, dimensions, display, cameras, Wi-Fi, USB, battery, weight and sensors."),
    "5g": src(
        "samsung_tab_s9_fe_ph_5g_128_specs",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-fe-5g-gray-128gb-sm-x516bzaaxtc/",
        "Samsung Philippines", "Exact 5G 6 GB / 128 GB Philippine SKU, product features and specifications",
        "Official Philippine page identifies Gray 5G SKU SM-X516BZAA XTC and lists its 6 GB RAM, 128 GB storage, cellular bands, dimensions, display, cameras, Wi-Fi, USB, battery, weight and sensors."),
    "ph_launch": src(
        "samsung_tab_s9_fe_ph_launch_availability",
        "https://news.samsung.com/ph/samsung-galaxy-s23-fe-galaxy-tab-s9-fe-and-galaxy-buds-fe-bring-standout-features-to-even-more-users",
        "Samsung Newsroom Philippines", "Dated Philippine launch and availability of the Galaxy Tab S9 FE series",
        "Samsung Philippines announced local availability beginning October 20, 2023, and stated the series started at PHP 26,990. The launch statement is series-level; exact SKU pricing comes from Samsung's own offer listing.",
        "2023-10-11"),
    "ph_prices_2023": src(
        "samsung_tab_s9_fe_ph_2023_cash_prices",
        "https://www.samsung.com/ph/offer/offline/2023/galaxy-fe-series-home-credit/",
        "Samsung Philippines", "Dated official Philippine cash price for exact 6 GB / 128 GB Wi-Fi and 5G configurations",
        "Samsung Philippines' 2023 campaign table lists PHP 26,990 for the Galaxy Tab S9 FE Wi-Fi 6 GB + 128 GB and PHP 31,990 for the 5G 6 GB + 128 GB. Campaign page does not expose an exact publication day.",
        None),
    "ph_prices_2025": src(
        "samsung_tab_s9_fe_ph_2025_trade_in_prices",
        "https://www.samsung.com/ph/offer/offline/2025/galaxy-tab-trade-in/",
        "Samsung Philippines", "Expired 2025 Philippine network-level SRP and promotional price observations",
        "Samsung listed Wi-Fi SRP PHP 28,990 / offer PHP 26,990 and 5G SRP PHP 33,990 / offer PHP 31,990, with the offer period July 11–September 30, 2025. This table does not identify RAM/storage, so these observations are model/network-level only and are not attached to a configuration.",
        "2025-07-11"),
    "global_launch": src(
        "samsung_tab_s9_fe_global_launch",
        "https://news.samsung.com/global/samsung-galaxy-s23-fe-galaxy-tab-s9-fe-and-galaxy-buds-fe-bring-standout-features-to-even-more-users",
        "Samsung Global Newsroom", "Global announcement and selected-market general availability date",
        "Samsung announced the FE series on October 4, 2023 and said the Tab S9 FE series would be available in selected markets starting October 5, 2023. The latter is a global selected-market date, not a Philippine release date.",
        "2023-10-04"),
    "exynos": src(
        "samsung_exynos_1380_official_specs",
        "https://semiconductor.samsung.com/processor/mobile-processor/exynos-1380/",
        "Samsung Semiconductor", "Exynos 1380 process node, CPU architecture and GPU specifications",
        "Samsung lists 5 nm process, four Cortex-A78 cores at 2.4 GHz, four Cortex-A55 cores at 2.0 GHz and Mali-G68 graphics with five cores. The Tab S9 FE manufacturer pages identify Exynos 1380."),
    "us_specs": src(
        "samsung_tab_s9_fe_us_launch_specs",
        "https://news.samsung.com/us/samsung-galaxy-s23-fe-galaxy-tab-s9-fe-galaxy-buds-fe-bring-standout-features-to-even-more-users/",
        "Samsung Newsroom US", "Manufacturer model-family cross-check for launch OS, stereo speakers, memory options and 45 W charging",
        "Samsung lists Android 13, 6/128 and 8/256 memory options, two FE cameras, 8,000 mAh battery, Wi-Fi 6, Bluetooth 5.3 and wired charging requiring a separately sold 45 W wall charger. US carrier and availability notes are not treated as Philippine evidence."),
    "samsung_de": src(
        "samsung_tab_s9_fe_samsung_de_comparison",
        "https://www.samsung.com/de/support/mobile-devices/vergleich-galaxy-tab-s9-vs-galaxy-tab-s9fe/",
        "Samsung Germany Support", "Manufacturer model-family comparison for SM-X510N / SM-X516B, charging and wireless-charging capability",
        "Samsung's comparison identifies SM-X510N as Wi-Fi and SM-X516B as cellular; it lists 45 W Super Fast Charging and states inductive charging is unsupported. Regional source is used only for shared model-family hardware, not local sale or price."),
    "nanoreview": src(
        "nanoreview_tab_s9_fe_specs",
        "https://nanoreview.net/en/tablet/samsung-galaxy-tab-s9-fe",
        "NanoReview", "Secondary specification cross-check for display protection, RAM/storage type, charging and battery chemistry",
        "NanoReview lists Corning Gorilla Glass 3, LPDDR4X, UFS 2.2, 45 W charging, no wireless charging and Li-Ion chemistry. These are secondary claims; the Li-Ion battery chemistry conflicts with Kimovil and is withheld."),
    "kimovil": src(
        "kimovil_tab_s9_fe_specs",
        "https://www.kimovil.com/en/where-to-buy-samsung-galaxy-tab-s9-fe",
        "Kimovil", "Secondary specification and configuration cross-check",
        "Kimovil lists 6/128 Wi-Fi, 8/256 Wi-Fi, 6/128 5G and 8/256 5G variants and reports Li-Polymer battery chemistry. Its battery chemistry conflicts with NanoReview; global configuration listings do not establish Philippine sales."),
    "gsmarena": src(
        "gsmarena_tab_s9_fe_specs_access_attempt",
        "https://www.gsmarena.com/samsung_galaxy_tab_s9_fe-12517.php",
        "GSMArena", "Attempted independent specification cross-check",
        "Direct access returned HTTP 402 Payment Required. No protection was bypassed and no specification values were copied from this page."),
    "image_product": src(
        "samsung_tab_s9_fe_ph_product_image_candidate",
        "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s9-fe-5g-gray-128gb-sm-x516bzaaxtc/",
        "Samsung Philippines", "Exact-model product-image match and source page reviewed; asset not reused",
        "Samsung product imagery depicts the Galaxy Tab S9 FE, but the page does not grant reuse permission for the public catalog."),
    "image_terms": src(
        "samsung_mobile_press_image_terms",
        "https://www.samsungmobilepress.com/terms",
        "Samsung Mobile Press", "Product-image reuse rights review",
        "Samsung Mobile Press terms identify images as Samsung or licensor property and limit copying/downloading to personal, informational and non-commercial use. The terms do not authorize reuse in this public product catalog."),
    "commons_taken_with": src(
        "commons_tab_s9_fe_taken_with_category",
        "https://commons.wikimedia.org/wiki/Category:Taken_with_Samsung_Galaxy_Tab_S9_FE",
        "Wikimedia Commons", "Search for reusable exact-model product photography",
        "The reviewed category contains scene photographs taken with a Galaxy Tab S9 FE, not product photographs of the device. No suitable exact-model openly licensed product image was found."),
}

CELLULAR_BANDS = (
    "2G GSM 850/900/1800/1900; 3G UMTS B1/B2/B4/B5/B8; "
    "4G FDD LTE B1/B2/B3/B4/B5/B7/B8/B12/B13/B17/B20/B26/B28/B32/B66; "
    "4G TDD LTE B38/B40/B41; 5G FDD Sub-6 n1/n3/n5/n7/n8/n20/n28/n66; "
    "5G TDD Sub-6 n38/n40/n41/n77/n78"
)

CONFIGS = [
    {"id": f"{DEVICE}-sm-x510n-6gb-128gb-wifi-ph", "key": "wifi",
     "modelCode": "SM-X510N", "sku": "SM-X510NZAAXTC", "ram": 6,
     "storage": 128, "network": "Wi-Fi", "weight": 523, "launch": 26990},
    {"id": f"{DEVICE}-sm-x516b-6gb-128gb-5g-ph", "key": "5g",
     "modelCode": "SM-X516B", "sku": "SM-X516BZAA XTC", "ram": 6,
     "storage": 128, "network": "5G", "weight": 524, "launch": 31990},
]


def field(fid: str, sid: str, source_value, normalized=None, *, status="VERIFIED",
          key=None, unit=None, note=None, candidate_evidence=None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": source_value, "normalizedValue": normalized,
           "note": note or "Exact Philippine product model and 6 GB / 128 GB configuration checked against the cited source."}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if candidate_evidence:
        row["candidateEvidence"] = candidate_evidence
    return row


def missing(fid: str, sid: str, value: str, note: str, *, status="NOT_DISCLOSED", unit=None) -> dict:
    return field(fid, sid, value, None, status=status, unit=unit, note=note)


def evidence(value: str, url: str, source_kind: str, excerpt: str) -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": "Galaxy Tab S9 FE model family; exact battery sample/configuration not independently stated",
            "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False}


def make_review(config: dict) -> dict:
    sid = config["key"]
    wifi_only = config["network"] == "Wi-Fi"
    label = f"{config['ram']} GB RAM / {config['storage']} GB storage · {config['network']} · Gray"
    exact_note = f"Exact Samsung Philippines Gray SKU {config['sku']} identifies model {config['modelCode']} and 6 GB / 128 GB; this is the locally evidenced configuration."
    fields: list[dict] = []

    def add(fid, source_key, value, normalized=None, **kwargs):
        fields.append(field(fid, SOURCES[source_key]["id"], value, normalized, **kwargs))

    def unavailable(fid, source_key, value, note, *, status="NOT_DISCLOSED", unit=None):
        fields.append(missing(fid, SOURCES[source_key]["id"], value, note, status=status, unit=unit))

    add("model_number", sid, config["modelCode"], config["modelCode"], note=exact_note)
    add("global_release_date", "global_launch",
        "Samsung announced the FE series 2023-10-04; selected-market availability began 2023-10-05",
        "2023-10-05", note="October 5, 2023 is Samsung's selected-market availability date. It is not used as the Philippine launch date.")
    add("configuration", sid, label, label, note=exact_note)
    add("philippine_release_date", "ph_launch",
        "Samsung Philippines stated the Galaxy Tab S9 FE series would be available locally starting 2023-10-20",
        "2023-10-20", note="Samsung Philippines gave October 20, 2023 as the start of local availability; this is the official series launch date, not an inference from global release timing.")
    add("official_launch_price_php", "ph_prices_2023",
        f"Samsung Philippines lists PHP {config['launch']:,} cash price for Galaxy Tab S9 FE {config['ram']} GB / {config['storage']} GB {config['network']}",
        config["launch"], unit="PHP", note="Historical local price from Samsung's 2023 campaign table for this exact 6 GB / 128 GB configuration; not a current offer.")
    unavailable("current_price_php", sid,
                "No current exact-SKU Philippine cash price was verifiable on 2026-11-27.",
                "The Samsung Philippines product page supplies specifications but no current numeric offer. The dated 2023 prices and expired 2025 promotion are kept as history, not treated as current.",
                status="PENDING_VERIFICATION", unit="PHP")

    add("display_size", sid, "10.9 inches full rectangle (10.8 inches accounting for rounded corners)", 10.9, key="displayInches", unit="in",
        note="Samsung measures the panel at 10.9 inches diagonally across the full rectangle; rounded-corner measurement is 10.8 inches.")
    add("display_technology", sid, "TFT display", "TFT", key="displayType")
    add("display_resolution", sid, "2304 x 1440 (WUXGA+)", "2304 x 1440", key="resolution")
    add("display_refresh_rate", sid, "Adaptive refresh rate up to 90 Hz", 90, key="refreshHz", unit="Hz")
    add("display_brightness", sid, "Maximum brightness 600 nits; outdoor brightness 720 nits in High Brightness Mode", 600, unit="nits",
        note="Samsung Philippines states a 600-nit maximum and 720-nit outdoor High Brightness Mode; the catalog value records maximum brightness.")
    add("display_protection", "nanoreview", "Corning Gorilla Glass 3", "Corning Gorilla Glass 3", status="VERIFIED_SECONDARY",
        note="NanoReview lists Gorilla Glass 3; Samsung's Philippine specification page does not name a display-glass revision. Secondary-source claim only.")
    add("chipset", sid, "Samsung Exynos 1380", "Samsung Exynos 1380", key="chipset")
    add("process_node", "exynos", "Samsung Semiconductor lists Exynos 1380 on 5 nm FinFET", 5, unit="nm")
    add("cpu", "exynos", "4 x Arm Cortex-A78 up to 2.4 GHz + 4 x Arm Cortex-A55 up to 2.0 GHz",
        "Octa-core: 4 x Cortex-A78 up to 2.4 GHz + 4 x Cortex-A55 up to 2.0 GHz", key="cpu")
    add("gpu", "exynos", "Arm Mali-G68 GPU with five cores", "Arm Mali-G68 MP5", key="gpu")
    add("operating_system", "us_specs", "Android 13 at launch", "Android 13", key="os",
        note="Samsung's launch specification table lists Android 13; later installed versions are not substituted for launch OS.")
    add("os_support", "global_launch", "Four generations of Android OS upgrades and five years of security updates",
        "Up to 4 OS generations; 5 years of security updates",
        note="Samsung's launch-era policy; this does not claim that all future updates remain active indefinitely.")
    add("ram_capacity", sid, "6 GB", 6, key="ramGb", unit="GB")
    add("ram_type", "nanoreview", "LPDDR4X", "LPDDR4X", status="VERIFIED_SECONDARY",
        note="NanoReview lists LPDDR4X; Samsung's local SKU specification page does not publish RAM technology type.")
    add("storage_capacity", sid, "128 GB internal storage", 128, key="storageGb", unit="GB")
    add("storage_type", "nanoreview", "UFS 2.2", "UFS 2.2", status="VERIFIED_SECONDARY",
        note="NanoReview lists UFS 2.2; Samsung's local SKU specification page does not identify the storage interface.")
    add("storage_expansion", sid, "MicroSD card support up to 1 TB", "microSD up to 1 TB")
    add("rear_camera_system", sid, "Single 8 MP autofocus rear camera", 8, key="rearCameraMp", unit="MP")
    unavailable("main_camera_sensor", sid,
                "Samsung does not identify the camera sensor component in the reviewed specifications.",
                "Resolution and autofocus are documented; no sensor part number or lens aperture is inferred.")
    add("ultrawide_camera", sid, "Samsung lists one 8 MP rear camera and no rear ultra-wide module", "No rear ultra-wide camera", status="NOT_APPLICABLE")
    add("telephoto_camera", sid, "Samsung lists one 8 MP rear camera and no telephoto module", "No telephoto camera", status="NOT_APPLICABLE")
    add("front_camera", sid, "12 MP front ultra-wide camera", 12, key="frontCameraMp", unit="MP",
        note="Samsung identifies the 12 MP front camera; the FE model-family launch specification identifies it as ultra-wide.")
    add("video_recording", sid, "Rear video up to UHD 4K (3840 x 2160) at 30 fps", "Rear video up to 4K / 30 fps", key="video")
    add("battery_capacity", sid, "8,000 mAh typical capacity", 8000, key="batteryMah", unit="mAh",
        note="Samsung labels 8,000 mAh as typical capacity; a rated/minimum value is not supplied in the reviewed Philippine page.")
    chemistry_evidence = [
        evidence("Li-Ion", SOURCES["nanoreview"]["url"], "independent_specification",
                 "NanoReview lists Li-Ion battery chemistry."),
        evidence("Li-Polymer", SOURCES["kimovil"]["url"], "independent_specification",
                 "Kimovil lists Li-Polymer battery chemistry."),
    ]
    fields.append(field("battery_technology", SOURCES["nanoreview"]["id"],
                        "NanoReview says Li-Ion; Kimovil says Li-Polymer; Samsung does not disclose cell chemistry.",
                        None, status="CONFLICTING_INFORMATION",
                        note="The two secondary sources disagree and Samsung does not specify chemistry. No battery chemistry is selected.",
                        candidate_evidence=chemistry_evidence))
    add("wired_charging", "us_specs", "Wired charging supported with a separately sold 45 W wall charger", 45,
        key="chargingW", unit="W", note="Samsung's launch materials require a 45 W wall charger, sold separately; the adapter is not asserted to be in-box.")
    add("wireless_charging", "samsung_de", "Samsung states inductive charging is not supported", "No wireless charging",
        note="Samsung's model-family comparison identifies SM-X510N and SM-X516B and states inductive charging is unsupported.")
    add("dimensions", sid, "165.8 x 254.3 x 6.5 mm", "165.8 x 254.3 x 6.5 mm", key="dimensions", unit="mm")
    add("weight", sid, f"{config['weight']} g ({config['network']} model)", config["weight"], key="weightG", unit="g",
        note="Samsung's Philippines SKU pages list 523 g for Wi-Fi and 524 g for 5G.")
    add("materials", sid, "Full-metal frame", "Full-metal frame")
    add("ingress_protection", sid, "IP68", "IP68")
    if wifi_only:
        add("sim_esim", sid, "Wi-Fi-only model; no SIM or eSIM", "No SIM; Wi-Fi only", key="sim")
        unavailable("cellular_bands", sid, "Not applicable: this exact SM-X510N SKU is Wi-Fi-only.",
                    "No cellular modem or cellular frequency bands are specified for the Wi-Fi-only model.", status="NOT_APPLICABLE")
        add("tablet_cellular_variant", sid, "Wi-Fi-only variant", "Wi-Fi only", key="cellular")
    else:
        add("sim_esim", sid, "Samsung Philippines advertises Dual SIM with eSIM on the Tab S9 FE cellular model family", "Nano-SIM + eSIM", key="sim",
            note="Samsung's local 5G product page advertises eSIM/Dual SIM. Function availability may vary by country, region or carrier.")
        add("cellular_bands", sid, CELLULAR_BANDS, CELLULAR_BANDS,
            note="Band list copied from the exact Samsung Philippines SM-X516B 5G product specification page.")
        add("tablet_cellular_variant", sid, "5G cellular variant", "5G cellular", key="cellular")
    add("wifi", sid, "Wi-Fi 6 (802.11 a/b/g/n/ac/ax), 2.4 GHz and 5 GHz", "Wi-Fi 6", key="wifi")
    add("bluetooth", sid, "Bluetooth 5.3", "Bluetooth 5.3")
    add("usb", sid, "USB Type-C, USB 2.0", "USB Type-C; USB 2.0", key="ports")
    add("nfc", sid, "NFC: No", "No NFC")
    add("gnss", sid, "GPS, GLONASS, BeiDou, Galileo and QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS")
    add("audio", "us_specs", "Dual stereo speakers with Dolby Atmos", "Dual stereo speakers; Dolby Atmos", key="sound",
        note="Samsung's model-family launch specification lists dual stereo speakers and Dolby Atmos.")
    add("sensors", sid, "Accelerometer, fingerprint sensor, gyroscope, geomagnetic sensor, Hall sensor and light sensor",
        "Accelerometer; fingerprint; gyroscope; geomagnetic; Hall; light")
    add("tablet_stylus", "ph_launch", "S Pen included in the box; S Pen Creator Edition sold separately", "S Pen included", key="stylus")
    add("tablet_keyboard", sid, "Book Cover Keyboard supported and sold separately", "Book Cover Keyboard supported; sold separately", key="keyboard")

    if len(fields) != 49:
        raise ValueError(f"Expected 49 field reviews for {label}, found {len(fields)}")
    variants = [{"id": c["id"], "label": f"{c['ram']} GB RAM / {c['storage']} GB storage · {c['network']} · Gray",
                 "sku": c["sku"], "modelCode": c["modelCode"],
                 "notes": f"Exact Gray {c['network']} SKU identified on Samsung Philippines' local product page."}
                for c in CONFIGS]
    item = {"deviceId": DEVICE, "configurationId": config["id"], "brand": "Samsung", "model": MODEL,
            "configuration": label, "modelCode": config["modelCode"], "sku": config["sku"],
            "sources": list(SOURCES.values()), "fields": fields,
            "availabilityEvidence": {
                "verificationStatus": "VERIFIED_OFFICIAL_LAUNCH",
                "availabilityStatus": "Philippine availability officially announced from 2023-10-20; exact 6/128 Wi-Fi and 6/128 5G SKUs listed locally.",
                "philippineAvailabilityDate": "2023-10-20",
                "philippineDateLabel": "Philippine launch date",
                "philippineAvailability": "Samsung Philippines announced availability beginning October 20, 2023. Exact local Samsung SKU pages and 2023 Samsung campaign pricing were found for 6 GB / 128 GB Wi-Fi (SM-X510NZAAXTC) and 6 GB / 128 GB 5G (SM-X516BZAA XTC). Samsung's PH product page mentions up to 256 GB but explicitly warns that 256 GB availability varies by region; no exact PH 8/256 SKU or local price was verified, so it is not added as a confirmed local configuration.",
                "observedAt": OBSERVED, "philippineReleaseYear": 2023,
                "catalogModel": MODEL,
                "qualityFlag": "Two exact 6/128 Philippine SKUs verified; local 8/256 availability and current price remain unresolved.",
                "openIssues": [
                    {"issue": "Samsung Philippines describes an option up to 256 GB but warns that its availability varies by country, region or carrier; no exact local 8 GB / 256 GB SKU or price was found.",
                     "action": "Do not list 8/256 as a verified Philippine SKU until an exact local SKU, authorized local listing or dated local configuration-specific price is found."},
                    {"issue": "No current numeric price for either exact 6/128 SKU was exposed by Samsung Philippines on the review date.",
                     "action": "Keep current price blank; retain historical local prices and dated expired promotions separately."},
                ],
            }}
    item["replacementVariants"] = variants
    return item


def price_rows() -> list[dict]:
    rows = []
    for config in CONFIGS:
        rows.append({
            "device_id": DEVICE, "configuration_id": config["id"], "variant_ram_gb": 6,
            "variant_storage_gb": 128, "variant_connectivity": config["network"],
            "configuration_match": f"exact_6gb_128gb_{config['network'].lower().replace('-', '')}",
            "amount_php": config["launch"], "price_type": "historical_ph_official_2023_cash_price_exact_configuration",
            "source_published_at": None, "observed_at": OBSERVED,
            "source_url": SOURCES["ph_prices_2023"]["url"],
            "source_kind": "official_samsung_ph_2023_campaign_cash_price",
            "local_availability_verified": True,
            "availability_status": "historical_2023_campaign_cash_price_not_current",
            "review_status": "VERIFIED",
            "excerpt": f"Samsung Philippines' 2023 campaign lists PHP {config['launch']:,} for the Galaxy Tab S9 FE 6 GB / 128 GB {config['network']} configuration. This is a historical campaign cash price, not a current offer.",
        })

    # Samsung's 2025 page omits RAM/storage. Preserve these as network-level
    # observations so that a model-level price never looks like an exact SKU.
    for network, srp, offer in [("Wi-Fi", 28990, 26990), ("5G", 33990, 31990)]:
        common = {"device_id": DEVICE, "configuration_id": None, "variant_ram_gb": None,
                  "variant_storage_gb": None, "variant_connectivity": network,
                  "configuration_match": f"model_network_{network.lower().replace('-', '')}_ram_storage_unspecified"}
        rows.append({**common, "amount_php": srp,
                     "price_type": "historical_2025_ph_official_srp_network_configuration_unspecified",
                     "source_published_at": "2025-07-11", "observed_at": OBSERVED,
                     "source_url": SOURCES["ph_prices_2025"]["url"],
                     "source_kind": "official_samsung_ph_2025_srp",
                     "local_availability_verified": True,
                     "availability_status": "historical_network_level_srp_not_current",
                     "review_status": "VERIFIED",
                     "excerpt": f"Samsung Philippines listed PHP {srp:,} SRP for Galaxy Tab S9 FE {network} during its 2025 trade-in promotion; RAM/storage not specified."})
        rows.append({**common, "amount_php": offer,
                     "price_type": "expired_2025_ph_official_promo_network_configuration_unspecified",
                     "source_published_at": "2025-07-11", "observed_at": OBSERVED,
                     "source_url": SOURCES["ph_prices_2025"]["url"],
                     "source_kind": "official_samsung_ph_2025_expired_offer",
                     "local_availability_verified": True,
                     "availability_status": "expired_2025_07_11_to_2025_09_30_not_current",
                     "review_status": "VERIFIED",
                     "excerpt": f"Samsung Philippines listed PHP {offer:,} promotional price for Galaxy Tab S9 FE {network}, valid July 11–September 30, 2025; RAM/storage not specified and the offer is expired."})
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
        "reason": "No exact-model product image with reuse permission was identified. Samsung Mobile Press terms restrict site materials to personal, informational and non-commercial use; Wikimedia Commons search results were photographs taken with the Tab S9 FE rather than product photos.",
        "sourcePage": SOURCES["image_product"]["url"],
        "assetUrl": "https://images.samsung.com/is/image/samsung/p6pim/ph/sm-x516bzaaxtc/gallery/ph-galaxy-tab-s9-fe-sm-x516-sm-x516bzaaxtc-thumb-538474968",
        "scope": "Samsung Galaxy Tab S9 FE; no image reused because an exact-model product-image license was not cleared.",
        "rightsTermsUrl": SOURCES["image_terms"]["url"],
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Samsung Galaxy Tab S9 FE",
    }
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Included":
        raise ValueError("Expected the Included workbook Galaxy Tab S9 FE record; refusing unexpected scope/device.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {v["id"] for v in CONFIGS}
    replacing = current_ids == {UNRECORDED}
    already_integrated = current_ids == expected_ids
    if not (replacing or already_integrated):
        raise ValueError(f"Unexpected Galaxy Tab S9 FE configurations; refusing: {sorted(current_ids)}")

    for config in CONFIGS:
        add_review(manual, catalog, make_review(config))
    deduplicate_target_reviews(manual, {(DEVICE, config["id"]) for config in CONFIGS})
    source_updates = {s["id"]: s for s in SOURCES.values()}
    for config in CONFIGS:
        saved = next(r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == config["id"])
        if config["id"] != CONFIGS[0]["id"]:
            for key in ("replacementVariants", "replaceUnrecordedPlaceholder", "additionalVariants"):
                saved.pop(key, None)
        saved.update({"brand": "Samsung", "model": MODEL,
                      "configuration": f"{config['ram']} GB RAM / {config['storage']} GB storage · {config['network']} · Gray",
                      "configurationLabel": f"{config['ram']} GB RAM / {config['storage']} GB storage · {config['network']} · Gray"})
        saved["sources"] = [source_updates.get(s["id"], s) for s in saved.get("sources", [])]
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    update_image_sources()
    prices = price_rows()
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Samsung", "model_name": MODEL,
                    "category": "tablets", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": s["url"],
                       "source_kind": s["purpose"], "status": "reviewed", "result": s["note"]}
                      for s in SOURCES.values()],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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

    print(json.dumps({
        "model": MODEL,
        "configurations": [{"id": c["id"], "sku": c["sku"], "modelCode": c["modelCode"],
                            "configuration": f"{c['ram']} GB / {c['storage']} GB · {c['network']}",
                            "historicalPhPricePhp": c["launch"], "currentPricePhp": None}
                           for c in CONFIGS],
        "reviewedConfigurations": len(CONFIGS), "reviewedFieldsPerConfiguration": 49,
        "availability": "Philippine launch documented 2023-10-20; local 8/256 availability unresolved",
        "image": "Unavailable: Samsung reuse terms do not permit use; neutral placeholder retained",
        "conflicts": ["Battery chemistry: NanoReview Li-Ion vs Kimovil Li-Polymer"],
        "priceObservations": len(prices),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
