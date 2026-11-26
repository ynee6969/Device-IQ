#!/usr/bin/env python3
"""Review the Philippine Samsung Galaxy Z Fold5 storage configurations."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-z-fold5-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_8b71a65802ab50"
CONFIGS = {
    256: f"{DEVICE}-ph-12gb-256gb",
    512: f"{DEVICE}-ph-12gb-512gb",
    1024: f"{DEVICE}-ph-12gb-1tb",
}

URL_PRODUCT_256 = "https://www.samsung.com/ph/smartphones/galaxy-z/galaxy-z-fold5-phantom-black-256gb-sm-f946bzkdphl/"
URL_PRODUCT_512 = "https://www.samsung.com/ph/smartphones/galaxy-z/galaxy-z-fold5-gray-512gb-sm-f946bzugphl/"
URL_PRODUCT_1TB = "https://www.samsung.com/ph/smartphones/galaxy-z/galaxy-z-fold5-cream-1tb-sm-f946bzehphl/buy/"
URL_PH_NEWS = "https://news.samsung.com/ph/samsung-galaxy-z-flip5-and-galaxy-z-fold5-delivering-flexibility-and-versatility-without-compromise"
URL_PH_PREORDER = "https://www.samsung.com/ph/offer/offline/2023/galaxy-z-flip5-fold5-preorder/"
URL_SUPPORT = "https://www.samsung.com/ph/support/model/SM-F946BZKDPHL/"
URL_GLOBAL_NEWS = "https://news.samsung.com/global/samsung-galaxy-z-flip5-and-galaxy-z-fold5-delivering-flexibility-and-versatility-without-compromise"
URL_YUGA = "https://www.yugatech.com/news/samsung-galaxy-z-flip5-fold5-priced-in-the-philippines-with-pre-order-details/"
URL_REVU = "https://www.revu.com.ph/2023/07/samsung-galaxy-z-flip5-fold5-price-ph/"
URL_GADGET_PH = "https://www.gadgetpilipinas.net/2023/07/samsung-galaxy-z-fold5-launched/"
URL_UNBOX = "https://www.youtube.com/watch?v=qV7Vl_SktTs"
URL_GSMARENA = "https://www.gsmarena.com/samsung_galaxy_z_fold5-review-2599.php"
URL_GSMARENA_RAM = "https://www.gsmarena.com/samsung_galaxy_z_fold5-review-2599p4.php"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/samsung-galaxy-z-fold-5"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-samsung-galaxy-z-fold5"
URL_SAMSUNG_RAM = "https://images.samsung.com/is/content/samsung/assets/pl/2307/mktpd/q5/Galaxy_Z_Fold5_spec.pdf"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("zfold5_ph_product_256", "Samsung Philippines (manufacturer)", URL_PRODUCT_256,
        "Exact local Phantom Black 12/256 product identity, specifications and sale status",
        "Samsung Philippines identifies Galaxy Z Fold5 Phantom Black 12GB/256GB as SM-F946BZKDPHL and publishes detailed local specifications. The product page showed Not for sale when checked on 26 November 2026."),
    src("zfold5_ph_product_512", "Samsung Philippines (manufacturer)", URL_PRODUCT_512,
        "Exact local online-exclusive Gray 12/512 product identity and sale status",
        "Samsung Philippines identifies Galaxy Z Fold5 Gray 12GB/512GB as SM-F946BZUGPHL. Gray is a Samsung.com-exclusive local color; the product page showed Not for sale when checked on 26 November 2026."),
    src("zfold5_ph_product_1tb", "Samsung Philippines (manufacturer)", URL_PRODUCT_1TB,
        "Exact local Cream 12/1TB product identity and sale status",
        "Samsung Philippines identifies Galaxy Z Fold5 Cream 12GB/1TB as SM-F946BZEHPHL. The product page showed Not for sale when checked on 26 November 2026."),
    src("zfold5_ph_news", "Samsung Newsroom Philippines (manufacturer)", URL_PH_NEWS,
        "Philippine launch, storage configurations, SRPs, availability date and model specifications",
        "Samsung Philippines gives 12GB/256GB, 12GB/512GB and 12GB/1TB SRPs of PHP 98,990, PHP 105,990 and PHP 119,990; general availability began 18 August 2023. It publishes displays, camera, processor, battery, charging and other specifications.", "2023-07-26"),
    src("zfold5_ph_preorder", "Samsung Philippines (manufacturer)", URL_PH_PREORDER,
        "Official preorder dates, 512GB storage upgrade and 1TB promotion price",
        "The official July 2023 campaign listed original SRPs of PHP 98,990/105,990/119,990 and preorder prices of PHP 98,990/98,990/112,990 for 256GB/512GB/1TB. The 512GB offer included a free upgrade from 256GB; 1TB received a PHP 7,000 discount.", "2023-07-26"),
    src("zfold5_ph_support", "Samsung Support Philippines (manufacturer)", URL_SUPPORT,
        "Philippine support model code and regional dual-SIM product identity",
        "Samsung Philippines support identifies the Galaxy Z Fold5 as model SM-F946B/DS and links to local product code SM-F946BZKDPHL."),
    src("zfold5_global_news", "Samsung Global Newsroom (manufacturer)", URL_GLOBAL_NEWS,
        "Global availability, design, build and software support",
        "Samsung announced the Z Fold5 on 26 July 2023 and states global general availability began 11 August 2023. It documents IPX8, Armor Aluminum, Victus 2 exterior glass and four OS upgrades with five years of security updates.", "2023-07-26"),
    src("zfold5_yugatech_ph", "YugaTech Philippines", URL_YUGA,
        "Independent Philippine release, configuration, SRP and specification cross-check",
        "YugaTech reports the local 12GB/256GB, 12GB/512GB and 12GB/1TB choices, PHP 98,990/105,990/119,990 prices and general availability on 18 August 2023.", "2023-07-26"),
    src("zfold5_revu_ph", "Revu Philippines", URL_REVU,
        "Independent Philippine preorder, availability and SRP cross-check",
        "Revu reports Philippine availability from 18 August 2023, preorders from 26 July, and PHP 98,990/105,990/119,990 prices for 256GB/512GB/1TB.", "2023-07-26"),
    src("zfold5_gadgetpilipinas", "Gadget Pilipinas", URL_GADGET_PH,
        "Independent Philippine configuration and launch-price cross-check",
        "Gadget Pilipinas reports all three 12GB local storage configurations, their PHP 98,990/105,990/119,990 launch prices and the 18 August 2023 general release date.", "2023-07-26"),
    src("zfold5_unbox_ph", "UNBOX PH (verified YouTube channel)", URL_UNBOX,
        "Philippine launch video cross-check for local configuration and SRP",
        "UNBOX PH's 26 July 2023 first-look video lists 12GB RAM, storage through 1TB and PHP 98,990/105,990/119,990 for 256GB/512GB/1TB.", "2023-07-26"),
    src("zfold5_gsmarena", "GSMArena", URL_GSMARENA,
        "Independent hands-on hardware, display, camera, battery and connectivity review",
        "The exact-model review checks the global SM-F946B Galaxy Z Fold5 hardware, but is not used for Philippine launch prices or local availability.", "2023-08-10"),
    src("zfold5_gsmarena_ram", "GSMArena", URL_GSMARENA_RAM,
        "Independent exact-model RAM-generation claim",
        "GSMArena identifies 12GB LPDDR5X RAM. Its claim conflicts with Samsung's Poland Galaxy Z Fold5 specification PDF, which says LPDDR5; leave RAM generation unresolved.", "2023-08-10"),
    src("zfold5_nanoreview", "NanoReview", URL_NANOREVIEW,
        "Independent chipset, camera, RAM/storage, battery and specification cross-check",
        "The exact-model profile reports LPDDR5X RAM, UFS 4.0, a 4nm Snapdragon 8 Gen 2 platform, Adreno 740, Samsung GN3 main sensor and other technical details. It does not establish Philippine price or release evidence."),
    src("zfold5_kimovil", "Kimovil", URL_KIMOVIL,
        "Global model and storage-configuration identity cross-check only",
        "Kimovil lists the global SM-F946B model separately with 12GB/256GB, 12GB/512GB and 12GB/1TB configurations. Global prices are not treated as Philippine prices."),
    src("zfold5_samsung_global_ram", "Samsung Poland (manufacturer specification PDF)", URL_SAMSUNG_RAM,
        "Manufacturer RAM-generation claim for the global Galaxy Z Fold5 family",
        "Samsung's Poland Galaxy Z Fold5 specification PDF lists 12GB LPDDR5 RAM. This differs from GSMArena and NanoReview, which say LPDDR5X; keep generation blank pending a Philippines-specific manufacturer specification.", "2023-07-26"),
]
S = {item["id"]: item["id"] for item in SOURCES}


def f(fid: str, sid: str, value, normalized=None, *, key: str | None = None,
      unit: str | None = None, status: str = "VERIFIED", note: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    return row


def price_observations(config: str, storage: int) -> list[dict]:
    srp = {256: 98990, 512: 105990, 1024: 119990}[storage]
    all_prices = [
        ("zfold5_ph_news", srp, "historical_ph_official_srp", "Samsung Philippines lists the local official launch SRP."),
        ("zfold5_yugatech_ph", srp, "historical_ph_launch_price", "YugaTech reports the same Philippine launch price."),
        ("zfold5_revu_ph", srp, "historical_ph_launch_price", "Revu reports the same Philippine launch price."),
        ("zfold5_gadgetpilipinas", srp, "historical_ph_launch_price", "Gadget Pilipinas reports the same Philippine launch price."),
        ("zfold5_unbox_ph", srp, "historical_ph_launch_video", "UNBOX PH's local launch video lists the same Philippine price."),
    ]
    if storage == 512:
        all_prices.append(("zfold5_ph_preorder", 98990, "historical_ph_preorder_storage_upgrade",
                          "Samsung's preorder promotion offered 12GB/512GB for the 12GB/256GB PHP 98,990 price through a free storage upgrade; original 512GB SRP remained PHP 105,990."))
    if storage == 1024:
        all_prices.append(("zfold5_ph_preorder", 112990, "historical_ph_preorder_discount",
                          "Samsung's preorder promotion reduced the 1TB configuration from PHP 119,990 SRP to PHP 112,990."))
    url_by_source = {source["id"]: source["url"] for source in SOURCES}
    publication = {source["id"]: source.get("publicationDate") for source in SOURCES}
    return [{
        "device_id": DEVICE, "amount_php": amount, "configuration_id": config,
        "configuration_match": "exact_philippine_storage_configuration",
        "variant_ram_gb": 12, "variant_storage_gb": storage,
        "price_type": price_type, "source_published_at": publication[source_id],
        "excerpt": excerpt, "source_url": url_by_source[source_id],
        "source_kind": "historical_local_price_observation",
        "observed_at": OBSERVED, "local_availability_verified": True,
        "availability_status": "historical_price_not_current",
    } for source_id, amount, price_type, excerpt in all_prices]


def fields(config: str, storage: int, label: str) -> list[dict]:
    product_source = {256: "zfold5_ph_product_256", 512: "zfold5_ph_product_512",
                      1024: "zfold5_ph_product_1tb"}[storage]
    srp = {256: 98990, 512: 105990, 1024: 119990}[storage]
    rows = [
        f("model_number", S["zfold5_ph_support"], "Samsung Philippines support lists model SM-F946B/DS; example local color and storage product codes differ by variant.", "SM-F946B/DS", note="Uses the Philippine regional model family; color-specific product codes are not stored as a configuration model number."),
        f("global_release_date", S["zfold5_global_news"], "Samsung global general availability began 11 August 2023; announcement was 26 July 2023.", "2023-08-11", note="Records global general availability rather than announcement date."),
        f("configuration", S["zfold5_ph_news"], f"12 GB memory / {storage if storage < 1024 else '1 TB'} internal storage", f"12 GB RAM / {storage} GB storage"),
        f("philippine_release_date", S["zfold5_ph_news"], "Samsung Philippines general availability began 18 August 2023; local preorders began 26 July.", "2023-08-18", note="Records official local general availability; preorder start is preserved separately."),
        f("official_launch_price_php", S["zfold5_ph_news"], f"Samsung Philippines official launch SRP: PHP {srp:,} for the {label} configuration.", srp, unit="PHP", note="Samsung's official local SRP is corroborated by YugaTech, Revu, Gadget Pilipinas and UNBOX PH. Preorder discounts are separate historical promotions."),
        f("current_price_php", S[product_source], f"Samsung Philippines product page showed Not for sale on {OBSERVED}; no current, dated, orderable local price was verified.", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep current catalog price blank; preserve official launch SRP and preorder pricing as historical evidence."),
        f("display_size", S["zfold5_ph_news"], "Main display 7.6 inches; cover display 6.2 inches", 7.6, key="displayInches", unit="in", note="Catalog primary size is the main display; the cover display is retained in the source value."),
        f("display_technology", S["zfold5_ph_news"], "7.6-inch Dynamic AMOLED 2X main display and 6.2-inch Dynamic AMOLED 2X cover display", "Dynamic AMOLED 2X main and cover", key="displayType"),
        f("display_resolution", S["zfold5_ph_news"], "Main 2176 x 1812; cover 2316 x 904", "Main 2176 x 1812; cover 2316 x 904", key="resolution"),
        f("display_refresh_rate", S["zfold5_ph_news"], "Main adaptive 1-120 Hz; cover adaptive 48-120 Hz", 120, key="refreshHz", unit="Hz", note="Catalog numeric field is the main display's 120 Hz maximum; cover range is kept in this field record."),
        f("display_brightness", S["zfold5_ph_news"], "Samsung states the main display reaches up to 1,750 nits peak brightness", 1750, unit="nits", note="Peak brightness claim; not a sustained full-screen brightness measurement."),
        f("display_protection", S["zfold5_global_news"], "Corning Gorilla Glass Victus 2 on cover display and rear; inner flexible screen has a shock-dispersion layer", "Victus 2 cover/back; inner screen shock-dispersion layer"),
        f("chipset", S["zfold5_ph_news"], "Qualcomm Snapdragon 8 Gen 2 Mobile Platform for Galaxy", "Qualcomm Snapdragon 8 Gen 2 for Galaxy", key="chipset"),
        f("process_node", S["zfold5_nanoreview"], "Snapdragon 8 Gen 2 for Galaxy uses a 4 nm process", 4, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", S["zfold5_ph_product_256"], "Octa-core CPU; listed cluster speeds 3.36 GHz, 2.8 GHz and 2.0 GHz", "Octa-core; up to 3.36 GHz, 2.8 GHz and 2.0 GHz"),
        f("gpu", S["zfold5_nanoreview"], "Qualcomm Adreno 740", "Adreno 740", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", S["zfold5_ph_news"], "Android 13 with One UI 5.1.1 at launch", "Android 13 with One UI 5.1.1", key="os"),
        f("os_support", S["zfold5_global_news"], "Four generations of Android OS upgrades and five years of security updates", "4 OS upgrades; 5 years security updates"),
        f("ram_capacity", S["zfold5_ph_news"], "12 GB memory across the 256GB, 512GB and 1TB storage configurations", 12, key="ramGb", unit="GB"),
        f("ram_type", S["zfold5_gsmarena_ram"], "Samsung Poland's manufacturer PDF lists LPDDR5; GSMArena and NanoReview list LPDDR5X. Samsung Philippines does not disclose RAM generation.", None, status="CONFLICTING_INFORMATION", note="Retain conflicting manufacturer and independent claims; do not normalize the memory generation without a Philippines-specific manufacturer record."),
        f("storage_capacity", S["zfold5_ph_news"], f"{storage if storage < 1024 else '1 TB'} internal storage; no microSD expansion", storage, key="storageGb", unit="GB"),
        f("storage_type", S["zfold5_gsmarena_ram"], "UFS 4.0", "UFS 4.0", key="storageType", status="VERIFIED_SECONDARY"),
        f("storage_expansion", S["zfold5_gsmarena"], "No microSD card slot", "No microSD slot", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", S["zfold5_ph_news"], "50 MP wide main camera with OIS + 12 MP ultra-wide + 10 MP telephoto with 3x optical zoom", "50 MP wide + 12 MP ultra-wide + 10 MP telephoto"),
        f("main_camera_sensor", S["zfold5_nanoreview"], "NanoReview identifies the 50 MP main camera sensor as Samsung GN3", "Samsung GN3", status="VERIFIED_SECONDARY"),
        f("ultrawide_camera", S["zfold5_ph_news"], "12 MP ultra-wide; f/2.2; 123-degree field of view", "12 MP; f/2.2; 123 degrees"),
        f("telephoto_camera", S["zfold5_ph_news"], "10 MP telephoto; f/2.4; 3x optical zoom and up to 30x digital Space Zoom", "10 MP; f/2.4; 3x optical, up to 30x digital"),
        f("front_camera", S["zfold5_ph_product_256"], "10 MP cover selfie camera and 4 MP under-display inner camera", 10, key="frontCameraMp", unit="MP", note="Catalog numeric field uses the cover selfie camera; the 4 MP under-display camera is retained here."),
        f("video_recording", S["zfold5_ph_product_256"], "Samsung Philippines lists UHD 8K (7680 x 4320) at 30 fps; GSMArena lists 8K at 24 fps and 4K at 60 fps.", None, status="CONFLICTING_INFORMATION", note="Recording modes disagree between the local product table and independent review; keep the normalized video field blank and retain both source claims."),
        f("battery_capacity", S["zfold5_ph_news"], "4,400 mAh typical dual battery; rated capacity 4,270 mAh", 4400, key="batteryMah", unit="mAh"),
        f("battery_technology", S["zfold5_nanoreview"], "NanoReview identifies a non-removable lithium-polymer battery", "Li-Po; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", S["zfold5_ph_news"], "25 W wired charging; Samsung says around 50% in 30 minutes with compatible adapter and cable", 25, key="chargingW", unit="W"),
        f("wireless_charging", S["zfold5_nanoreview"], "Fast Wireless Charging 2.0 and Wireless PowerShare; NanoReview lists up to 15 W wireless charging", "Fast Wireless Charging 2.0; up to 15 W; Wireless PowerShare", status="VERIFIED_SECONDARY"),
        f("dimensions", S["zfold5_ph_news"], "Unfolded 154.9 x 129.9 x 6.1 mm; folded 154.9 x 67.1 x 13.4 mm", "Unfolded 154.9 x 129.9 x 6.1 mm; folded 154.9 x 67.1 x 13.4 mm", key="dimensions", unit="mm"),
        f("weight", S["zfold5_ph_news"], "253 g", 253, key="weightG", unit="g"),
        f("materials", S["zfold5_global_news"], "Armor Aluminum frame; Gorilla Glass Victus 2 on cover and rear; flexible inner display with shock-dispersion layer", "Armor Aluminum; Victus 2 cover/back; flexible inner screen"),
        f("ingress_protection", S["zfold5_global_news"], "IPX8 water-resistance rating; the rating does not indicate dust protection", "IPX8 water resistance"),
        f("sim_esim", S["zfold5_ph_product_256"], "Dual SIM: two Nano-SIM slots or SIM 1 + SIM 2 / Embedded SIM", "Dual Nano-SIM or Nano-SIM + eSIM", key="sim"),
        f("cellular_bands", S["zfold5_ph_product_256"], "Samsung Philippines lists 2G GSM 850/900/1800/1900; 3G WCDMA B1/2/4/5/8; LTE FDD B1/2/3/4/5/7/8/12/13/17/18/19/20/25/26/28/66, TDD B38/39/40/41; 5G Sub6 FDD N1/2/3/5/7/8/12/20/25/28/66, TDD N38/40/41/77/78.", "Philippine model bands per Samsung Philippines", key="cellular"),
        f("wifi", S["zfold5_ph_product_256"], "Wi-Fi 802.11 a/b/g/n/ac/ax; 2.4/5/6 GHz Wi-Fi 6E", "Wi-Fi 6E; 2.4/5/6 GHz", key="wifi"),
        f("bluetooth", S["zfold5_ph_product_256"], "Bluetooth 5.3", "Bluetooth 5.3"),
        f("usb", S["zfold5_ph_product_256"], "USB Type-C 3.2 Gen 1; no 3.5 mm audio jack", "USB Type-C 3.2 Gen 1; no 3.5 mm jack", key="ports"),
        f("nfc", S["zfold5_ph_product_256"], "NFC: Yes", "Yes"),
        f("gnss", S["zfold5_ph_product_256"], "GPS, GLONASS, BeiDou, Galileo and QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS", key="gnss"),
        f("audio", S["zfold5_ph_product_256"], "Stereo speakers; audio over USB Type-C or Bluetooth; no 3.5 mm jack", "Stereo speakers; USB-C/Bluetooth audio", key="sound"),
        f("sensors", S["zfold5_ph_product_256"], "Accelerometer, barometer, side fingerprint sensor, gyroscope, geomagnetic sensor, Hall sensor, light sensor and proximity sensor", "Accelerometer; barometer; side fingerprint; gyro; geomagnetic; Hall; light; proximity"),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field assessments, got {len(rows)}")

    price_evidence = [{
        "value": f"PHP {price['amount_php']:,}", "sourceUrl": price["source_url"],
        "sourceKind": price["price_type"], "observedAt": OBSERVED,
        "excerpt": price["excerpt"], "configurationMatch": label,
        "reviewStatus": "VERIFIED", "localAvailabilityVerified": True,
    } for price in price_observations(config, storage)]
    rows[4]["candidateEvidence"] = price_evidence
    ram = next(row for row in rows if row["fieldId"] == "ram_type")
    ram["candidateEvidence"] = [
        {"value": "12 GB LPDDR5", "sourceUrl": URL_SAMSUNG_RAM,
         "sourceKind": "manufacturer_global_specification", "observedAt": OBSERVED,
         "excerpt": "Samsung Poland's Galaxy Z Fold5 specification PDF lists 12GB LPDDR5 RAM.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
        {"value": "12 GB LPDDR5X", "sourceUrl": URL_GSMARENA_RAM,
         "sourceKind": "independent_global_review", "observedAt": OBSERVED,
         "excerpt": "GSMArena identifies the Galaxy Z Fold5's 12GB RAM as LPDDR5X.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
        {"value": "12 GB LPDDR5X", "sourceUrl": URL_NANOREVIEW,
         "sourceKind": "independent_global_specification", "observedAt": OBSERVED,
         "excerpt": "NanoReview identifies 12GB LPDDR5X RAM on the exact Fold5 model profile.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
    ]
    video = next(row for row in rows if row["fieldId"] == "video_recording")
    video["candidateEvidence"] = [
        {"value": "UHD 8K at 30 fps", "sourceUrl": URL_PRODUCT_256,
         "sourceKind": "manufacturer_ph_product_specification", "observedAt": OBSERVED,
         "excerpt": "Samsung Philippines product specifications list UHD 8K at 30fps.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
        {"value": "8K at 24 fps and 4K at 60 fps", "sourceUrl": URL_GSMARENA,
         "sourceKind": "independent_global_review", "observedAt": OBSERVED,
         "excerpt": "GSMArena's exact-model review lists 8K@24fps and 4K@60fps capture modes.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": False},
    ]
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_OFFICIAL_LAUNCH",
        "availabilityStatus": "Samsung Philippines confirms the Galaxy Z Fold5's local launch in 12GB/256GB, 12GB/512GB and 12GB/1TB configurations, with general availability from 18 August 2023. Current local sale and price are not verified.",
        "philippineAvailability": "Samsung Newsroom Philippines lists local SRPs of PHP 98,990, PHP 105,990 and PHP 119,990 for 12GB/256GB, 12GB/512GB and 12GB/1TB and says general availability began 18 August 2023. Local product pages identify exact examples SM-F946BZKDPHL (Phantom Black 256GB), SM-F946BZUGPHL (Gray 512GB online-exclusive) and SM-F946BZEHPHL (Cream 1TB). Samsung Philippines support identifies the base regional model as SM-F946B/DS. Its three reviewed product pages showed Not for sale on 26 November 2026, so current prices remain blank. The July–August preorder campaign offered 512GB for the 256GB price and reduced the 1TB price to PHP 112,990; these are preserved as historical promotions, not current prices.",
        "observedAt": OBSERVED,
        "manufacturer": "Samsung Electronics",
        "catalogModel": "Z Fold5",
        "productLine": "Galaxy Z series",
        "modelNumber": "SM-F946B/DS",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "General availability began 18 August 2023; Philippine preorders began 26 July",
        "researchNotes": "Workbook row 164 Samsung Z Fold5 matches the Philippine Galaxy Z Fold5 family SM-F946B/DS in three separate 12GB configurations: 256GB, 512GB and 1TB. Samsung Philippines confirms the local model, official SRPs and 18 August 2023 general availability; the 512GB preorder upgrade and 1TB discount are stored separately. All three sampled official local product pages showed Not for sale, so current prices remain blank. RAM generation is withheld because Samsung Poland lists LPDDR5 while GSMArena and NanoReview say LPDDR5X. Video capture maximum is also withheld because the Philippines product page says 8K30 and GSMArena says 8K24/4K60. Image reuse rights were not established; study scope remains Pending.",
        "qualityFlag": "Official local launch and all three storage configurations verified; SRPs and preorder terms sourced; current price not for sale/unverified; RAM type and video modes conflict across sources; image reuse rights not established; study scope remains Pending.",
        "openIssues": [
            {"issue": "All reviewed Samsung Philippines product pages showed Not for sale", "action": "Leave current price blank until a dated, orderable local offer is found."},
            {"issue": "Manufacturer and independent sources disagree on LPDDR5 versus LPDDR5X", "action": "Keep RAM generation blank and preserve all source claims."},
            {"issue": "Samsung Philippines lists 8K30 while GSMArena lists 8K24/4K60 video modes", "action": "Keep normalized video recording blank pending a source-specific resolution."},
            {"issue": "Exact local product images are visible but reuse permission or a suitable license was not located", "action": "Keep the neutral placeholder and preserve source-page metadata."},
            {"issue": "Workbook study scope remains Pending", "action": "Preserve supplied scope status; verified launch does not change eligibility."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 164 or device.get("category") != "smartphones"
            or device.get("brand") != "Samsung" or device.get("model") != "Z Fold5"):
        raise ValueError("Workbook row 164 guard failed; expected Samsung Z Fold5 smartphone")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Samsung Z Fold5 already has manual-review rows; refusing duplicate replacement")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise ValueError("Expected the original unrecorded-configuration placeholder before review")

    variants = {
        256: {"id": CONFIGS[256], "label": "12 GB RAM / 256 GB storage", "sku": None,
              "modelCode": "SM-F946B/DS", "notes": "Samsung Philippines Phantom Black 12/256 product code SM-F946BZKDPHL. Official historical SRP PHP 98,990; current price not verified."},
        512: {"id": CONFIGS[512], "label": "12 GB RAM / 512 GB storage", "sku": None,
              "modelCode": "SM-F946B/DS", "notes": "Samsung Philippines online-exclusive Gray 12/512 product code SM-F946BZUGPHL. Official SRP PHP 105,990; preorder upgrade price PHP 98,990 is historical; current price not verified."},
        1024: {"id": CONFIGS[1024], "label": "12 GB RAM / 1 TB storage", "sku": None,
              "modelCode": "SM-F946B/DS", "notes": "Samsung Philippines Cream 12/1TB product code SM-F946BZEHPHL. Official SRP PHP 119,990; preorder promo price PHP 112,990 is historical; current price not verified."},
    }
    replacement_variants = [variants[n] for n in (256, 512, 1024)]
    for index, storage in enumerate((256, 512, 1024)):
        variant = variants[storage]
        item = {
            "deviceId": DEVICE, "configurationId": CONFIGS[storage],
            "brand": "Samsung", "model": "Galaxy Z Fold5",
            "configuration": variant["label"], "modelCode": "SM-F946B/DS", "sku": None,
            "sources": SOURCES, "fields": fields(CONFIGS[storage], storage, variant["label"]),
        }
        if index == 0:
            item["availabilityEvidence"] = availability_evidence()
            item["replacementVariants"] = replacement_variants
            item["replaceUnrecordedPlaceholder"] = True
        add_review(manual, catalog, item)
        device["variants"] = [{"id": v["id"], "specs": {}} for v in replacement_variants]
    deduplicate_target_reviews(manual, {(DEVICE, CONFIGS[n]) for n in (256, 512, 1024)})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Samsung Philippines product pages show exact Galaxy Z Fold5 images for the 12/256 Phantom Black, 12/512 Gray and 12/1TB Cream configurations, but no reusable image license or written permission to copy or hotlink was found. Keep the neutral placeholder.",
        "sourcePage": URL_PRODUCT_256, "assetUrl": None,
        "scope": "Samsung Galaxy Z Fold5; local 12 GB / 256 GB, 12 GB / 512 GB and 12 GB / 1 TB configurations",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Samsung Galaxy Z Fold5",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [price for storage in (256, 512, 1024) for price in price_observations(CONFIGS[storage], storage)]
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Samsung", "model_name": "Galaxy Z Fold5", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": source["url"], "result": source["note"]} for source in SOURCES],
        "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "workbookRow": 164, "device": "Samsung Galaxy Z Fold5",
        "configurations": [variants[n]["label"] for n in (256, 512, 1024)],
        "reviewedFields": 46, "reviewedConfigurationFieldRows": 138,
        "sources": len(SOURCES), "historicalPriceObservations": len(prices),
        "globalAvailability": "2023-08-11", "philippineAvailability": "2023-08-18",
        "launchSRPPhp": {"256GB": 98990, "512GB": 105990, "1TB": 119990},
        "currentPrices": None, "imageRights": "not established; placeholder retained",
        "scopeStatus": "Pending", "conflicts": ["RAM generation", "maximum video recording modes"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
