#!/usr/bin/env python3
"""Review the Philippine Samsung Galaxy Z Flip5 storage configurations."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-z-flip5-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_8d098d93ab5f47"
CONFIG_256 = f"{DEVICE}-ph-8gb-256gb"
CONFIG_512 = f"{DEVICE}-ph-8gb-512gb"

URL_PRODUCT_256 = "https://www.samsung.com/ph/smartphones/galaxy-z/galaxy-z-flip5-cream-256gb-sm-f731bzeaphl/"
URL_PRODUCT_512 = "https://www.samsung.com/ph/smartphones/galaxy-z/galaxy-z-flip5-graphite-512gb-sm-f731bzaephl/buy/"
URL_PH_NEWS = "https://news.samsung.com/ph/samsung-galaxy-z-flip5-and-galaxy-z-fold5-delivering-flexibility-and-versatility-without-compromise"
URL_PH_PREORDER = "https://www.samsung.com/ph/offer/offline/2023/galaxy-z-flip5-fold5-preorder/"
URL_PH_DATES = "https://www.samsung.com/ph/mobile/mobile-phone-buying-guide/launch-dates/"
URL_GLOBAL_NEWS = "https://news.samsung.com/global/samsung-galaxy-z-flip5-and-galaxy-z-fold5-delivering-flexibility-and-versatility-without-compromise"
URL_YUGA = "https://www.yugatech.com/news/samsung-galaxy-z-flip5-fold5-priced-in-the-philippines-with-pre-order-details/"
URL_REVU = "https://www.revu.com.ph/2023/07/samsung-galaxy-z-flip5-fold5-price-ph/"
URL_UNBOX = "https://www.youtube.com/watch?v=u8H_EM3pr8I"
URL_GSMARENA = "https://www.gsmarena.com/samsung_galaxy_z_flip5-review-2597.php"
URL_GSMARENA_RAM = "https://www.gsmarena.com/samsung_galaxy_z_flip5-review-2597p4.php"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/samsung-galaxy-z-flip-5"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-samsung-galaxy-z-flip5"
URL_YUGA_SPECS = "https://www.yugatech.com/spec/samsung-galaxy-z-flip5/"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("zflip5_ph_product_256", "Samsung Philippines (manufacturer)", URL_PRODUCT_256,
        "Exact local 8/256 product identity, model code, specifications and current listing state",
        "Samsung Philippines product page identifies Galaxy Z Flip5 Cream 8GB/256GB as product code SM-F731BZEAPHL, publishes detailed specifications and showed Not for sale when checked on 26 November 2026."),
    src("zflip5_ph_product_512", "Samsung Philippines (manufacturer)", URL_PRODUCT_512,
        "Exact local 8/512 product identity and color-specific product code",
        "Samsung Philippines lists the Graphite 8GB/512GB variant as SM-F731BZAEPHL and offers 256GB/512GB storage choices on the product page. The page showed Not for sale when checked on 26 November 2026."),
    src("zflip5_ph_news", "Samsung Newsroom Philippines (manufacturer)", URL_PH_NEWS,
        "Philippine launch, general availability date, local SRPs and full model specifications",
        "Samsung Philippines states 256GB PHP 64,990 and 512GB PHP 71,990; pre-orders ran 26 July–17 August 2023 and general availability began 18 August. It lists both displays, camera, battery, charging, network and launch software.", "2023-07-26"),
    src("zflip5_ph_preorder", "Samsung Philippines (manufacturer)", URL_PH_PREORDER,
        "Official preorder dates and 512GB storage-upgrade promotion",
        "The official promotion ran 26 July–17 August 2023 and shows original SRPs of PHP 64,990 (256GB) and PHP 71,990 (512GB). Eligible preorder customers received 512GB for the 256GB price; the campaign amount is historical promo pricing, not the 512GB SRP.", "2023-07-26"),
    src("zflip5_ph_dates", "Samsung Philippines (manufacturer)", URL_PH_DATES,
        "Local launch event timing",
        "Samsung Philippines identifies the Galaxy Z Flip5 as launched at Galaxy Unpacked on 26 July 2023. The separate local newsroom announcement sets general availability on 18 August 2023."),
    src("zflip5_global_news", "Samsung Global Newsroom (manufacturer)", URL_GLOBAL_NEWS,
        "Global announcement, specifications, durability and software-support policy",
        "Samsung announced the Z Flip5 on 26 July 2023 and says general global availability started 11 August 2023. It documents IPX8, Armor Aluminum, Victus 2 on the cover window/back, Android 13/One UI 5.1.1 at launch, four OS upgrades and five years of security updates.", "2023-07-26"),
    src("zflip5_yugatech_ph", "YugaTech Philippines", URL_YUGA,
        "Independent Philippine launch-price and specification cross-check",
        "YugaTech reports local 8/256 and 8/512 storage options, PHP 64,990 and PHP 71,990 launch prices, main/cover displays, Snapdragon 8 Gen 2 for Galaxy and core camera/connectivity details.", "2023-07-26"),
    src("zflip5_revu_ph", "Revu Philippines", URL_REVU,
        "Independent local pre-order, availability and price cross-check",
        "Revu reports Philippine general availability on 18 August 2023, preorders from 26 July, and PHP 64,990/71,990 prices for 256GB/512GB.", "2023-07-26"),
    src("zflip5_unbox_ph", "UNBOX PH (verified YouTube channel)", URL_UNBOX,
        "Philippine launch-video price cross-check and alternate 256GB amount",
        "The 26 July 2023 video describes the Z Flip5 and lists 256GB at PHP 65,990 and 512GB at PHP 71,990. The 256GB figure differs from Samsung's official Philippine newsroom and other local reporting; it is retained as an alternate historical claim, not used as the catalog SRP.", "2023-07-26"),
    src("zflip5_gsmarena", "GSMArena", URL_GSMARENA,
        "Independent hardware, display, performance and battery review",
        "The exact Galaxy Z Flip5 review provides independent hands-on checks for the Snapdragon 8 Gen 2 for Galaxy, displays, battery, camera and connectivity. It is not used for Philippine model identity, price or availability.", "2023-08-05"),
    src("zflip5_gsmarena_ram", "GSMArena", URL_GSMARENA_RAM,
        "Independent RAM type claim for exact Galaxy Z Flip5",
        "The performance section describes the 8GB memory as LPDDR5X. This conflicts with YugaTech's Philippine product specification page, which lists LPDDR5; memory type is therefore withheld as conflicting.", "2023-08-05"),
    src("zflip5_yuga_specs_ph", "YugaTech Philippines", URL_YUGA_SPECS,
        "Philippine specification cross-check including RAM type",
        "YugaTech's Galaxy Z Flip5 spec page lists 8GB LPDDR5 RAM and both 256GB and 512GB storage options. Its RAM type claim conflicts with GSMArena's LPDDR5X label.", "2023-07-26"),
    src("zflip5_nanoreview", "NanoReview", URL_NANOREVIEW,
        "Independent chipset and specification cross-check",
        "Exact-model profile cross-checks chipset architecture, process node, GPU, memory/storage technology, camera and charging. Its current OS version is not treated as launch software or Philippine market evidence."),
    src("zflip5_kimovil", "Kimovil", URL_KIMOVIL,
        "Global model and memory-configuration cross-check only",
        "Kimovil distinguishes Global SM-F731B 8/256 and 8/512 configurations from North American SM-F731U and Canadian SM-F731W versions. Global price listings are not treated as Philippine prices."),
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


def price_observations(config: str) -> list[dict]:
    all_prices = [
        (CONFIG_256, 256, 64990, "2023-07-26", URL_PH_NEWS, "historical_ph_official_srp", "Samsung Philippines launch release gives PHP 64,990 SRP for the 256GB model."),
        (CONFIG_256, 256, 64990, "2023-07-26", URL_YUGA, "historical_ph_launch_price", "YugaTech reports the Philippine 256GB launch price as PHP 64,990."),
        (CONFIG_256, 256, 64990, "2023-07-26", URL_REVU, "historical_ph_launch_price", "Revu reports the Philippine 256GB launch price as PHP 64,990."),
        (CONFIG_256, 256, 65990, "2023-07-26", URL_UNBOX, "historical_ph_alternate_price_claim", "UNBOX PH's 26 July launch video lists PHP 65,990 for 256GB; this differs from Samsung Philippines, YugaTech and Revu."),
        (CONFIG_512, 512, 71990, "2023-07-26", URL_PH_NEWS, "historical_ph_official_srp", "Samsung Philippines launch release gives PHP 71,990 SRP for the 512GB model."),
        (CONFIG_512, 512, 71990, "2023-07-26", URL_YUGA, "historical_ph_launch_price", "YugaTech reports the Philippine 512GB launch price as PHP 71,990."),
        (CONFIG_512, 512, 71990, "2023-07-26", URL_REVU, "historical_ph_launch_price", "Revu reports the Philippine 512GB launch price as PHP 71,990."),
        (CONFIG_512, 512, 64990, "2023-07-26", URL_PH_PREORDER, "historical_ph_preorder_promo", "Samsung's 26 July–17 August 2023 preorder promotion offered the 512GB configuration at PHP 64,990 through a free double-storage upgrade; this is promotional pricing, not its PHP 71,990 SRP."),
    ]
    return [{
        "device_id": DEVICE, "amount_php": amount, "configuration_id": cid,
        "configuration_match": "exact_philippine_storage_configuration",
        "variant_ram_gb": 8, "variant_storage_gb": storage,
        "price_type": price_type, "source_published_at": published,
        "excerpt": excerpt, "source_url": url,
        "source_kind": "historical_local_price_observation",
        "observed_at": OBSERVED, "local_availability_verified": True,
        "availability_status": "historical_price_not_current",
    } for cid, storage, amount, published, url, price_type, excerpt in all_prices if cid == config]


def fields(config: str, storage: int, label: str) -> list[dict]:
    prices = price_observations(config)
    rows = [
        f("model_number", S["zflip5_ph_product_256"],
          "Samsung Philippines product code uses model family SM-F731B (example 256GB Cream SKU SM-F731BZEAPHL; 512GB Graphite SKU SM-F731BZAEPHL).",
          "SM-F731B", note="Color-specific product codes differ; SM-F731B is the base model family code."),
        f("global_release_date", S["zflip5_global_news"],
          "Samsung global availability began 11 August 2023; announcement was 26 July 2023.", "2023-08-11",
          note="Uses the first global general-availability date, not the announcement date."),
        f("configuration", S["zflip5_ph_news"], f"8 GB memory / {storage} GB internal storage", f"8 GB RAM / {storage} GB storage"),
        f("philippine_release_date", S["zflip5_ph_news"],
          "Samsung Philippines general availability began 18 August 2023; local preorders started 26 July.", "2023-08-18",
          note="Records the official general-availability date; preorder start is preserved separately."),
        f("official_launch_price_php", S["zflip5_ph_news"],
          f"Samsung Philippines official launch SRP: PHP {64990 if storage == 256 else 71990:,} for the {storage}GB configuration.",
          64990 if storage == 256 else 71990, unit="PHP",
          note="For 256GB, Samsung's SRP is corroborated by YugaTech and Revu; UNBOX PH's video lists PHP 65,990 and is preserved as a conflicting alternate claim. For 512GB, the official SRP was PHP 71,990; the time-limited preorder double-storage promotion is recorded separately."),
        f("current_price_php", S["zflip5_ph_product_256" if storage == 256 else "zflip5_ph_product_512"],
          "Samsung Philippines product pages showed Not for sale on 26 November 2026; no current dated, orderable local price was verified.",
          None, status="PENDING_VERIFICATION", unit="PHP",
          note="Keep catalog current price blank; launch SRP and preorder promo remain historical observations."),
        f("display_size", S["zflip5_ph_product_256"], "Main display 6.7 inches; cover display 3.4 inches", 6.7, key="displayInches", unit="in"),
        f("display_technology", S["zflip5_ph_news"], "6.7-inch Dynamic AMOLED 2X main display; 3.4-inch Super AMOLED Flex Window", "Dynamic AMOLED 2X main; Super AMOLED cover", key="displayType"),
        f("display_resolution", S["zflip5_ph_news"], "Main 2640 x 1080; cover 720 x 748", "Main 2640 x 1080; cover 720 x 748", key="resolution"),
        f("display_refresh_rate", S["zflip5_ph_news"], "Main adaptive 1-120 Hz; cover display 60 Hz", 120, key="refreshHz", unit="Hz", note="Catalog field reports the main display maximum; the 60 Hz cover display is specified in this review record."),
        f("display_brightness", S["zflip5_ph_news"], "Maximum brightness not recorded on the reviewed Philippine manufacturer specification pages.", None, status="NOT_DISCLOSED"),
        f("display_protection", S["zflip5_global_news"], "Armor Aluminum frame; Corning Gorilla Glass Victus 2 on Flex Window and back cover; main flexible display uses a shock-dispersion layer.", "Victus 2 on cover window/back; flexible main screen shock-dispersion layer"),
        f("chipset", S["zflip5_ph_news"], "Qualcomm Snapdragon 8 Gen 2 Mobile Platform for Galaxy", "Qualcomm Snapdragon 8 Gen 2 for Galaxy", key="chipset"),
        f("process_node", S["zflip5_nanoreview"], "Snapdragon 8 Gen 2 for Galaxy is based on a 4 nm process", 4, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", S["zflip5_ph_product_256"], "Octa-core CPU; listed cluster speeds 3.36 GHz, 2.8 GHz and 2.0 GHz", "Octa-core; up to 3.36 GHz, 2.8 GHz and 2.0 GHz", status="VERIFIED_SECONDARY"),
        f("gpu", S["zflip5_nanoreview"], "Qualcomm Adreno 740", "Adreno 740", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", S["zflip5_ph_news"], "Android 13 with One UI 5.1.1 at launch", "Android 13 with One UI 5.1.1", key="os"),
        f("os_support", S["zflip5_global_news"], "Four generations of Android OS upgrades and five years of security updates", "4 OS upgrades; 5 years security updates"),
        f("ram_capacity", S["zflip5_ph_product_256"], "8 GB memory for both Philippine storage variants", 8, key="ramGb", unit="GB"),
        f("ram_type", S["zflip5_gsmarena_ram"], "YugaTech Philippines lists 8 GB LPDDR5; GSMArena identifies 8 GB LPDDR5X. Samsung Philippines does not specify memory generation.", None, status="CONFLICTING_INFORMATION",
          note="Secondary specifications conflict on LPDDR5 versus LPDDR5X; keep this field blank pending a matching manufacturer disclosure or exact local-unit teardown."),
        f("storage_capacity", S["zflip5_ph_product_256"], f"{storage} GB internal storage; no microSD expansion", storage, key="storageGb", unit="GB"),
        f("storage_type", S["zflip5_nanoreview"], "UFS 4.0", "UFS 4.0", key="storageType", status="VERIFIED_SECONDARY"),
        f("storage_expansion", S["zflip5_ph_product_256"], "No microSD expansion slot is listed; Samsung product specs list internal storage only", "No microSD slot listed", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", S["zflip5_ph_product_256"], "12 MP wide main camera with OIS and Dual Pixel AF + 12 MP ultra-wide rear camera", "12 MP wide main + 12 MP ultra-wide"),
        f("main_camera_sensor", S["zflip5_ph_product_256"], "Samsung product specification does not disclose a sensor part number", None, status="NOT_DISCLOSED"),
        f("ultrawide_camera", S["zflip5_ph_news"], "12 MP ultra-wide; f/2.2; 123-degree field of view", "12 MP; f/2.2; 123 degrees"),
        f("telephoto_camera", S["zflip5_ph_product_256"], "Manufacturer lists only wide and ultra-wide rear modules", "No telephoto module listed", status="NOT_APPLICABLE"),
        f("front_camera", S["zflip5_ph_news"], "10 MP selfie camera, f/2.2, 85-degree field of view", 10, key="frontCameraMp", unit="MP"),
        f("video_recording", S["zflip5_ph_product_256"], "UHD 4K (3840 x 2160) at up to 60 fps; slow motion 960 fps at FHD and 240 fps at FHD", "UHD 4K/60; FHD slow motion/960 or 240 fps", key="video"),
        f("battery_capacity", S["zflip5_ph_news"], "3,700 mAh typical dual battery; rated capacity 3,591 mAh", 3700, key="batteryMah", unit="mAh"),
        f("battery_technology", S["zflip5_ph_news"], "Dual-battery assembly; cell chemistry is not specified in the reviewed Philippine manufacturer page", "Dual battery; chemistry not recorded", status="NOT_DISCLOSED"),
        f("wired_charging", S["zflip5_ph_news"], "25 W wired charging; Samsung says about 50% in 30 minutes with a compatible 25 W adapter sold separately", 25, key="chargingW", unit="W"),
        f("wireless_charging", S["zflip5_ph_news"], "Fast Wireless Charging 2.0 and Wireless PowerShare; NanoReview lists 15 W but Samsung PH does not publish a wattage on the reviewed page", "Fast Wireless Charging 2.0; Wireless PowerShare"),
        f("dimensions", S["zflip5_ph_news"], "Unfolded 165.1 x 71.9 x 6.9 mm; folded 85.1 x 71.9 x 15.1 mm", "Unfolded 165.1 x 71.9 x 6.9 mm; folded 85.1 x 71.9 x 15.1 mm", key="dimensions", unit="mm"),
        f("weight", S["zflip5_ph_news"], "187 g", 187, key="weightG", unit="g"),
        f("materials", S["zflip5_global_news"], "Armor Aluminum frame; Gorilla Glass Victus 2 on cover window and rear; flexible inner panel with shock-dispersion layer", "Armor Aluminum; Victus 2 cover/back; flexible inner screen"),
        f("ingress_protection", S["zflip5_global_news"], "IPX8 water-resistance rating; no dust-ingress rating indicated by IPX8", "IPX8 water resistance"),
        f("sim_esim", S["zflip5_ph_product_256"], "Dual-SIM: one nano-SIM plus embedded SIM (eSIM)", "Nano-SIM + eSIM", key="sim"),
        f("cellular_bands", S["zflip5_ph_product_256"], "Local Samsung Philippines specifications list 2G GSM 850/900/1800/1900; 3G WCDMA B1/2/4/5/8; LTE FDD B1/2/3/4/5/7/8/12/13/17/18/19/20/25/26/28/66, TDD B38/39/40/41; 5G Sub6 FDD N1/2/3/5/7/8/12/20/25/28/66, TDD N38/40/41/77/78.", "Philippine model bands per Samsung Philippines", key="cellular"),
        f("wifi", S["zflip5_ph_product_256"], "Wi-Fi 802.11 a/b/g/n/ac/ax; 2.4/5/6 GHz Wi-Fi 6E", "Wi-Fi 6E; 2.4/5/6 GHz", key="wifi"),
        f("bluetooth", S["zflip5_ph_product_256"], "Bluetooth 5.3", "Bluetooth 5.3"),
        f("usb", S["zflip5_ph_product_256"], "USB Type-C 3.2 Gen 1; no 3.5 mm audio jack", "USB Type-C 3.2 Gen 1; no 3.5 mm jack", key="ports"),
        f("nfc", S["zflip5_ph_product_256"], "NFC: Yes", "Yes"),
        f("gnss", S["zflip5_ph_product_256"], "GPS, GLONASS, BeiDou, Galileo and QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS", key="gnss"),
        f("audio", S["zflip5_ph_product_256"], "Stereo support; audio output through USB Type-C or Bluetooth; no 3.5 mm jack", "Stereo speakers; USB-C/Bluetooth audio", key="sound"),
        f("sensors", S["zflip5_ph_product_256"], "Accelerometer, barometer, fingerprint sensor, gyroscope, geomagnetic sensor, Hall sensor, light sensor and proximity sensor", "Accelerometer; barometer; fingerprint; gyro; geomagnetic; Hall; light; proximity"),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field assessments, got {len(rows)}")
    if storage == 256:
        rows[4]["candidateEvidence"] = [{
            "value": "PHP 65,990", "sourceUrl": URL_UNBOX,
            "sourceKind": "independent_ph_launch_video", "observedAt": OBSERVED,
            "excerpt": "UNBOX PH's 26 July 2023 launch video lists PHP 65,990 for 256GB.",
            "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION",
            "localAvailabilityVerified": True,
        }, {
            "value": "PHP 64,990", "sourceUrl": URL_PH_NEWS,
            "sourceKind": "manufacturer_ph_launch_srp", "observedAt": OBSERVED,
            "excerpt": "Samsung Philippines launch release lists PHP 64,990 for 256GB; YugaTech and Revu report the same amount.",
            "configurationMatch": label, "reviewStatus": "VERIFIED",
            "localAvailabilityVerified": True,
        }]
    else:
        rows[4]["candidateEvidence"] = [{
            "value": "PHP 64,990 promotional offer", "sourceUrl": URL_PH_PREORDER,
            "sourceKind": "manufacturer_ph_preorder_promotion", "observedAt": OBSERVED,
            "excerpt": "During the 26 July–17 August 2023 preorder promotion, eligible buyers received 512GB for the 256GB price through a free storage upgrade; original 512GB SRP remained PHP 71,990.",
            "configurationMatch": label, "reviewStatus": "VERIFIED",
            "localAvailabilityVerified": True,
        }]
    rows[19]["candidateEvidence"] = [{
        "value": "8 GB LPDDR5", "sourceUrl": URL_YUGA_SPECS,
        "sourceKind": "independent_ph_specification", "observedAt": OBSERVED,
        "excerpt": "YugaTech's exact Galaxy Z Flip5 specifications list 8 GB LPDDR5 RAM.",
        "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION",
        "localAvailabilityVerified": True,
    }, {
        "value": "8 GB LPDDR5X", "sourceUrl": URL_GSMARENA_RAM,
        "sourceKind": "independent_global_review", "observedAt": OBSERVED,
        "excerpt": "GSMArena's exact Galaxy Z Flip5 performance section describes 8 GB LPDDR5X RAM.",
        "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION",
        "localAvailabilityVerified": False,
    }]
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_OFFICIAL_LAUNCH",
        "availabilityStatus": "Samsung Philippines confirms the Galaxy Z Flip5's local launch; preorders ran 26 July–17 August 2023 and general availability began 18 August 2023. Current local sale and price are not verified.",
        "philippineAvailability": "Samsung Newsroom Philippines identifies the Galaxy Z Flip5 as a Philippine-market model with 8GB/256GB and 8GB/512GB storage, official SRPs of PHP 64,990 and PHP 71,990, and general availability beginning 18 August 2023. Samsung Philippines product pages identify local product codes SM-F731BZEAPHL (Cream 256GB) and SM-F731BZAEPHL (Graphite 512GB); the base model family is SM-F731B. The 512GB configuration was included in a time-limited free double-storage preorder offer at the 256GB price. Samsung product pages showed Not for sale on 26 November 2026; no current price is recorded. One UNBOX PH video lists PHP 65,990 for 256GB, differing from Samsung's official PHP 64,990 SRP and other local reporting; the official value is retained with the alternate claim in the field audit.",
        "observedAt": OBSERVED,
        "manufacturer": "Samsung Electronics",
        "catalogModel": "Z Flip5",
        "productLine": "Galaxy Z series",
        "modelNumber": "SM-F731B",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "General availability began 18 August 2023; Philippine preorders began 26 July",
        "researchNotes": "Workbook row 163 Samsung Z Flip5 matches the Philippine Galaxy Z Flip5 (SM-F731B) in distinct 8GB/256GB and 8GB/512GB configurations. Samsung Philippines lists official launch SRPs of PHP 64,990 and PHP 71,990 and states general availability began 18 August 2023. Eligible preorders from 26 July through 17 August received a free storage upgrade, allowing 512GB at the 256GB price; this campaign is recorded separately from SRP. Samsung product pages now display Not for sale, so current price remains blank. An UNBOX PH launch video lists PHP 65,990 for 256GB; Samsung's official release, YugaTech and Revu report PHP 64,990, so the manufacturer price is used and the alternate claim retained. YugaTech labels RAM as LPDDR5 while GSMArena says LPDDR5X; the memory-generation field is left unresolved. Workbook study scope remains Pending.",
        "qualityFlag": "Samsung Philippines launch and both 8/256 and 8/512 configurations verified; historical SRPs and preorder terms recorded; alternate 256GB price and conflicting LPDDR5/LPDDR5X claims preserved; current local price not for sale/unverified; image reuse rights not established; study scope remains Pending.",
        "openIssues": [
            {"issue": "A Philippine launch video reports PHP 65,990 for 256GB, while Samsung, YugaTech and Revu report PHP 64,990", "action": "Use Samsung's official SRP as the catalog historical launch value and retain the alternate claim in evidence; do not treat either as a current price."},
            {"issue": "Samsung product pages showed Not for sale when reviewed", "action": "Leave current price blank until an exact, dated, orderable Philippine offer is found."},
            {"issue": "YugaTech lists LPDDR5 RAM while GSMArena lists LPDDR5X, and Samsung's local specification page omits RAM generation", "action": "Keep the RAM-type value blank and record both exact-model claims until a source resolves the discrepancy."},
            {"issue": "Samsung product images are exact-model images but reusable terms or permission were not found", "action": "Keep the neutral placeholder and record the official source pages."},
            {"issue": "Workbook study scope is Pending", "action": "Preserve the supplied study-scope status; verified launch availability does not change eligibility."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 163 or device.get("category") != "smartphones"
            or device.get("brand") != "Samsung" or device.get("model") != "Z Flip5"):
        raise ValueError("Workbook row 163 guard failed; expected Samsung Z Flip5 smartphone")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Samsung Z Flip5 already has manual-review rows; refusing duplicate replacement")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise ValueError("Expected the original unrecorded-configuration placeholder before review")

    variant_256 = {"id": CONFIG_256, "label": "8 GB RAM / 256 GB storage",
                   "sku": None, "modelCode": "SM-F731B",
                   "notes": "Samsung Philippines Cream product code SM-F731BZEAPHL confirms a local 8/256 SKU. Official historical SRP PHP 64,990; a launch video gives a conflicting PHP 65,990. Current price not verified."}
    variant_512 = {"id": CONFIG_512, "label": "8 GB RAM / 512 GB storage",
                   "sku": None, "modelCode": "SM-F731B",
                   "notes": "Samsung Philippines Graphite product code SM-F731BZAEPHL confirms a local 8/512 SKU. Official SRP PHP 71,990; preorder free-storage offer temporarily gave 512GB for PHP 64,990. Current price not verified."}
    add_review(manual, catalog, {
        "deviceId": DEVICE, "configurationId": CONFIG_256, "brand": "Samsung", "model": "Galaxy Z Flip5",
        "configuration": variant_256["label"], "modelCode": "SM-F731B", "sku": None,
        "sources": SOURCES, "fields": fields(CONFIG_256, 256, variant_256["label"]),
        "availabilityEvidence": availability_evidence(),
        "replacementVariants": [variant_256, variant_512], "replaceUnrecordedPlaceholder": True,
    })
    device["variants"] = [{"id": CONFIG_256, "specs": {}}, {"id": CONFIG_512, "specs": {}}]
    add_review(manual, catalog, {
        "deviceId": DEVICE, "configurationId": CONFIG_512, "brand": "Samsung", "model": "Galaxy Z Flip5",
        "configuration": variant_512["label"], "modelCode": "SM-F731B", "sku": None,
        "sources": SOURCES, "fields": fields(CONFIG_512, 512, variant_512["label"]),
    })
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG_256), (DEVICE, CONFIG_512)})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Samsung Philippines product pages show exact Galaxy Z Flip5 images for the local Cream 8/256 and Graphite 8/512 configurations, but no reusable image license or written permission to copy or hotlink was found. Keep the neutral placeholder.",
        "sourcePage": URL_PRODUCT_256, "assetUrl": None,
        "scope": "Samsung Galaxy Z Flip5; local 8 GB / 256 GB and 8 GB / 512 GB configurations",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Samsung Galaxy Z Flip5",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [*price_observations(CONFIG_256), *price_observations(CONFIG_512)]
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Samsung", "model_name": "Galaxy Z Flip5", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_PRODUCT_256, "result": "Official Samsung Philippines Cream 8/256 product code and specs verified; page currently says Not for sale."},
            {"device_id": DEVICE, "source_url": URL_PRODUCT_512, "result": "Official Samsung Philippines Graphite 8/512 product code verified; page currently says Not for sale."},
            {"device_id": DEVICE, "source_url": URL_PH_NEWS, "result": "Samsung Philippines confirms official local launch SRPs, specs and 18 August 2023 general availability."},
            {"device_id": DEVICE, "source_url": URL_PH_PREORDER, "result": "Official 26 July–17 August 2023 campaign offered the 512GB model at the 256GB price through free double storage."},
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech corroborates 8/256 and 8/512 local configurations and Samsung launch prices."},
            {"device_id": DEVICE, "source_url": URL_REVU, "result": "Revu corroborates local 18 August availability and 64,990/71,990 historical SRPs."},
            {"device_id": DEVICE, "source_url": URL_UNBOX, "result": "UNBOX PH video lists PHP 65,990 for 256GB, conflicting with the official Samsung SRP and other local reports; alternate value retained."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "Exact model review cross-checks hardware; not used for Philippine price or local model proof."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA_RAM, "result": "Exact-model RAM claim is LPDDR5X; conflicts with YugaTech's LPDDR5 claim, so memory type remains unresolved."},
            {"device_id": DEVICE, "source_url": URL_YUGA_SPECS, "result": "Philippine model spec page supports both storage options and lists LPDDR5, conflicting with GSMArena's LPDDR5X claim."},
            {"device_id": DEVICE, "source_url": URL_NANOREVIEW, "result": "Exact model profile cross-checks processor architecture, display, memory/storage type and battery; current software version not treated as launch OS."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Global SM-F731B 8/256 and 8/512 listed separately from North American and Canadian model codes."},
            {"device_id": DEVICE, "source_url": URL_GLOBAL_NEWS, "result": "Samsung global newsroom states 11 August global availability, IPX8, Victus 2, Android 13/One UI 5.1.1 and 4 OS upgrades/5 years security updates."},
        ],
        "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "workbookRow": 163, "device": "Samsung Galaxy Z Flip5",
        "configurations": [variant_256["label"], variant_512["label"]],
        "reviewedFields": 46, "reviewedConfigurationFieldRows": 92,
        "sources": len(SOURCES), "historicalPriceObservations": len(prices),
        "globalAvailability": "2023-08-11", "philippineAvailability": "2023-08-18",
        "launchSRPPhp": {"256GB": 64990, "512GB": 71990},
        "currentPrice": None, "alternate256GbPriceClaim": 65990,
        "imageRights": "not established; placeholder retained", "scopeStatus": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
