#!/usr/bin/env python3
"""Review Philippine Galaxy Z Fold3 5G configurations from exact model sources."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_samsung_a_series_reviews import f, record, src  # noqa: E402
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"
DEVICE = "device_f6ce8c275dee32"
CONFIGS = [
    {"storage": 256, "price": 87990, "sku": None},
    {"storage": 512, "price": 95990, "sku": None},
]


def source(sid: str, publisher: str, url: str, _access_date: str,
           purpose: str, note: str, published: str | None = None) -> dict:
    return src(sid, publisher, url, purpose, note, published)


def sources() -> list[dict]:
    return [
        source(
            "samsung_fold3_ph_256_identity",
            "Samsung Business Philippines",
            "https://www.samsung.com/ph/business/smartphones/galaxy-z/galaxy-z-fold3-5g-phantom-green-256gb-sm-f926bzgdphl/buy/",
            OBSERVED,
            "Local product identity and supported memory choices",
            "Samsung Philippines identifies the Galaxy Z Fold3 5G and lists 12 GB/256 GB and 12 GB/512 GB choices. The cited Phantom Green order code is color-specific and is not assigned to the color-unspecified workbook configuration.",
        ),
        source(
            "samsung_fold3_ph_512_sku",
            "Samsung Philippines",
            "https://www.samsung.com/ph/support/model/SM-F926BZGGPHL/",
            OBSERVED,
            "Philippine 12 GB/512 GB support SKU and regional model code",
            "Samsung Philippines identifies local SKU SM-F926BZGGPHL and family model SM-F926B/DS. The local code is Phantom Green; because the workbook does not identify color, the SKU remains blank on the 12 GB/512 GB catalog variant.",
        ),
        source(
            "samsung_fold3_ph_preorder_2021",
            "Samsung Philippines",
            "https://www.samsung.com/ph/offer/offline/2021/galaxy-zseries3/samsung-care/",
            OBSERVED,
            "Official Philippine pre-order period",
            "Samsung Philippines' terms state that Galaxy Z Fold3 pre-orders ran 19 August–21 September 2021 through Samsung Online Store/pre-order portals, with separate operator windows. This confirms Philippine authorized-channel availability before general retail sale.",
            "2021-08-19",
        ),
        source(
            "samsung_fold3_ph_srp_2021",
            "Samsung Philippines",
            "https://www.samsung.com/ph/offer/offline/2021/galaxy-pnb/q3/",
            OBSERVED,
            "Dated Philippine SRP by 256 GB and 512 GB configurations",
            "Samsung Philippines lists PHP 87,990 for the Galaxy Z Fold3 5G 256 GB and PHP 95,990 for 512 GB. The offer page marks Fold3 prices as starting 13 September 2021; these are historical SRPs, not current prices.",
            "2021-09-13",
        ),
        source(
            "samsung_fold3_global_specs_2021",
            "Samsung Global Newsroom",
            "https://news.samsung.com/global/the-next-chapter-in-mobile-innovation-unfold-your-world-with-galaxy-z-fold3-5g-and-galaxy-z-flip3-5g",
            OBSERVED,
            "Manufacturer specifications at launch",
            "Samsung's launch specification table supplies the Fold3 display panels and resolutions, cameras, processor platform, RAM/storage types, battery, charging, water-resistance, operating system, connectivity, dimensions, and weight.",
            "2021-08-11",
        ),
        source(
            "samsung_fold3_ph_processor",
            "Samsung Philippines Support",
            "https://www.samsung.com/ph/support/mobile-devices/what-is-the-difference-between-galaxy-z-fold3-and-galaxy-z-fold4/",
            OBSERVED,
            "Exact Philippine model processor identification",
            "Samsung Philippines' comparison identifies Snapdragon 888 as the Galaxy Z Fold3 processor.",
        ),
        source(
            "samsung_fold3_ph_model_256",
            "Samsung Philippines Support",
            "https://www.samsung.com/ph/support/model/SM-F926BZSDPHL/",
            OBSERVED,
            "Philippine 12 GB/256 GB support SKU and regional model code",
            "Samsung Philippines identifies local SKU SM-F926BZSDPHL and family model SM-F926B/DS. This Phantom Silver order code is color-specific and is not assigned to the color-unspecified workbook configuration.",
        ),
        source(
            "samsung_fold3_global_3q_report_2021",
            "Samsung Electronics",
            "https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2021_3Q_Interim_Report_vF.pdf",
            OBSERVED,
            "Launch operating-system version and folded/unfolded hardware context",
            "Samsung's 2021 third-quarter report lists the Fold3 launch OS as Android 11 with One UI 3.1.1, along with foldable dimensions and model-level details.",
            "2021-11-15",
        ),
        source(
            "yugatech_fold3_ph_launch_2021",
            "YugaTech",
            "https://www.yugatech.com/mobile/samsung-galaxy-z-fold3-flip3-5g-specs-price-philippines/",
            OBSERVED,
            "Philippine launch prices, configuration details, and general-sale date",
            "YugaTech's 11 August 2021 Philippine launch report lists 12 GB/256 GB at PHP 87,990 and 12 GB/512 GB at PHP 95,990, gives model-specific specs, and reports general availability through Samsung and authorized partners from 22 September 2021. Prices are cross-checked against Samsung Philippines' dated SRP table.",
            "2021-08-11",
        ),
    ]


def shared_fields() -> list[dict]:
    official = "samsung_fold3_global_specs_2021"
    secondary = "yugatech_fold3_ph_launch_2021"
    return [
        f("model_number", "samsung_fold3_ph_model_256", "Philippine model family SM-F926B/DS", "SM-F926B/DS",
          note="The base family code applies to both capacities. Samsung Philippines' color-specific SKUs are retained as source evidence but not assigned to the color-unspecified workbook variants."),
        f("display_size", official, "Main display 7.6 in; cover display 6.2 in", 7.6,
          key="displayInches", unit="in", note="The public numeric display-size field stores the 7.6-inch main panel; the 6.2-inch cover panel remains in sourceValue."),
        f("display_technology", official, "Dynamic AMOLED 2X on the main and cover displays", "Dynamic AMOLED 2X", key="displayType"),
        f("display_resolution", official, "Main: 2208 x 1768; cover: 2268 x 832", "Main 2208 x 1768; cover 2268 x 832", key="resolution"),
        f("display_refresh_rate", official, "Both displays: adaptive refresh rate up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", official, "Main panel: 900 nits HBM / 1200 nits peak; cover: 1000 nits HBM / 1500 nits peak", "Main: 900 HBM / 1200 peak nits; cover: 1000 HBM / 1500 peak nits", unit="nits"),
        f("display_protection", "yugatech_fold3_ph_launch_2021", "Corning Gorilla Glass Victus is listed for the cover glass", "Corning Gorilla Glass Victus", status="VERIFIED_SECONDARY"),
        f("chipset", "samsung_fold3_ph_processor", "Qualcomm Snapdragon 888", "Qualcomm Snapdragon 888", key="chipset"),
        f("cpu", official, "5 nm 64-bit octa-core processor: up to 2.84 GHz + 2.4 GHz + 1.8 GHz", "Octa-core; 2.84 / 2.4 / 1.8 GHz", key="cpu"),
        f("process_node", official, "5 nm process", "5 nm"),
        f("operating_system", "samsung_fold3_global_3q_report_2021", "Android 11 with One UI 3.1.1 at launch", "Android 11 / One UI 3.1.1", key="os"),
        f("rear_camera_system", official, "12 MP wide/main with OIS + 12 MP ultra-wide + 12 MP telephoto with OIS", 12,
          key="rearCameraMp", unit="MP", note="The numeric public camera field stores the 12 MP wide/main camera; the sourceValue preserves all three rear modules."),
        f("main_camera_sensor", official, "12 MP wide-angle main; Dual Pixel AF, OIS, f/1.8", "12 MP; Dual Pixel AF; OIS; f/1.8"),
        f("ultrawide_camera", official, "12 MP ultra-wide, f/2.2", "12 MP; f/2.2"),
        f("telephoto_camera", official, "12 MP telephoto, OIS, f/2.4, 2x optical zoom", "12 MP; OIS; f/2.4; 2x optical zoom"),
        f("front_camera", official, "10 MP cover selfie camera plus 4 MP under-display camera, f/1.8", 10,
          key="frontCameraMp", unit="MP", note="The numeric public field stores the 10 MP cover camera; Samsung also lists a separate 4 MP under-display camera."),
        f("video_recording", official, "HDR10+ recording and Tracking AF; maximum recording mode not stated in this source table", "HDR10+ recording; Tracking AF", key="video"),
        f("storage_type", official, "256 GB / 512 GB UFS 3.1", "UFS 3.1", key="storageType"),
        f("battery_capacity", official, "4,400 mAh typical dual battery; 4,275 mAh rated minimum", 4400,
          key="batteryMah", unit="mAh", note="Samsung distinguishes the 4,400 mAh typical capacity from 4,275 mAh rated minimum; the catalog stores typical capacity."),
        f("wired_charging", official, "25 W wired fast charging", 25, key="chargingW", unit="W"),
        f("wireless_charging", official, "10 W fast wireless charging; 4.5 W reverse wireless charging", "10 W wireless; 4.5 W reverse"),
        f("dimensions", official, "Folded: 67.1 x 158.2 x 14.4–16.0 mm; unfolded: 128.1 x 158.2 x 6.4 mm", "Folded 67.1 x 158.2 x 14.4–16.0 mm; unfolded 128.1 x 158.2 x 6.4 mm", key="dimensions", unit="mm"),
        f("weight", official, "271 g", 271, key="weightG", unit="g"),
        f("materials", "yugatech_fold3_ph_launch_2021", "Armor Aluminum body; Corning Gorilla Glass Victus exterior glass", "Armor Aluminum; Gorilla Glass Victus", status="VERIFIED_SECONDARY"),
        f("ingress_protection", official, "IPX8 water resistance; Samsung states it is not dust-resistant", "IPX8; not dust-resistant"),
        f("cellular_bands", official, "5G and LTE; supported bands and speeds vary by market and carrier", "5G; LTE", key="cellular"),
        f("sim_esim", official, "Two Nano-SIM slots and one eSIM; eSIM availability varies by region/carrier", "2 Nano-SIM; eSIM support varies", key="sim"),
        f("wifi", official, "Wi-Fi 6E (802.11 a/b/g/n/ac/ax)", "Wi-Fi 6E", key="wifi"),
        f("bluetooth", official, "Bluetooth 5.2", "Bluetooth 5.2"),
        f("nfc", official, "NFC support listed", "Yes"),
        f("gnss", official, "GPS, Galileo, GLONASS, and BeiDou", "GPS; Galileo; GLONASS; BeiDou"),
        f("usb", official, "USB Type-C", "USB Type-C", key="ports"),
        f("audio", official, "Stereo speakers with Dolby Atmos", "Stereo speakers; Dolby Atmos", key="sound"),
    ]


def build_records() -> list[dict]:
    shared = shared_fields()
    source_rows = sources()
    variants = [
        {"id": f"{DEVICE}-samsung-12gb-{item['storage']}gb",
         "label": f"12 GB RAM / {item['storage']} GB storage",
         "modelCode": "SM-F926B/DS", "sku": None,
         "notes": "Color-specific Philippine Samsung SKU not recorded for the inventory configuration."}
        for item in CONFIGS
    ]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine pre-orders opened 19 August 2021; general sale reported from 22 September 2021",
        "philippineAvailability": (
            "Samsung Philippines' official terms document pre-orders from 19 August to 21 September 2021. "
            "YugaTech reported general availability through Samsung.com/ph, authorized Samsung stores, online partners, "
            "and telco partners beginning 22 September 2021. The catalog date is the reported general-sale start, "
            "not a first individual transaction timestamp."
        ),
        "observedAt": OBSERVED,
        "qualityFlag": "Official Philippine pre-order period and reported general-sale date documented",
    }
    result = []
    for index, item in enumerate(CONFIGS):
        storage = item["storage"]
        label = f"12 GB RAM / {storage} GB storage"
        config_id = f"{DEVICE}-samsung-12gb-{storage}gb"
        fields = [
            f("configuration", "samsung_fold3_ph_256_identity", label, label),
            f("ram_capacity", "samsung_fold3_ph_256_identity", "12 GB", 12, key="ramGb", unit="GB"),
            f("storage_capacity", "samsung_fold3_ph_256_identity", f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "yugatech_fold3_ph_launch_2021",
              "General Philippine availability reported beginning 22 September 2021; official Samsung pre-orders opened 19 August.",
              "2021-09-22", status="VERIFIED_SECONDARY",
              note="Records the reported general-sale date. Samsung Philippines' official pre-order terms independently document local authorized pre-orders beginning 19 August 2021."),
            f("official_launch_price_php", "yugatech_fold3_ph_launch_2021",
              f"Philippine launch coverage reports PHP {item['price']:,} for the {storage} GB configuration.", item["price"],
              status="VERIFIED_SECONDARY", unit="PHP",
              note="Launch-period Philippine price reported by YugaTech on 11 August 2021 and corroborated by Samsung Philippines' dated SRP table; not a current offer."),
            f("current_price_php", "samsung_fold3_ph_srp_2021",
              f"Historical Samsung Philippines SRP, effective 13 September 2021: PHP {item['price']:,}", item["price"],
              unit="PHP", note="Dated Samsung Philippines SRP effective 13 September 2021; not a current offer.",
              price_condition="new", price_type="Historical Samsung Philippines SRP (not a current offer)",
              price_observed="2021-09-13"),
            *shared,
        ]
        review = record(DEVICE, "Galaxy Z Fold3 5G", config_id, label, source_rows, fields,
                        model_code="SM-F926B/DS", availability=availability)
        if index == 0:
            review["replacementVariants"] = variants
        result.append(review)
    return result


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = build_records()
    for item in items:
        add_review(manual, catalog, item)
        if item.get("replacementVariants"):
            device = next(d for d in catalog if d["id"] == item["deviceId"])
            device["variants"] = [
                {"id": variant["id"], "label": variant["label"], "specs": {},
                 "sku": variant.get("sku"), "modelCode": variant.get("modelCode")}
                for variant in item["replacementVariants"]
            ]
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"models": 1, "reviewedConfigurations": len(items), "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
