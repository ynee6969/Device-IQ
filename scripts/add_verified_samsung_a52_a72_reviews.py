#!/usr/bin/env python3
"""Record exact, source-backed Philippine reviews for Galaxy A52 LTE and A72."""
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


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           published: str | None = None) -> dict:
    return src(sid, publisher, url, purpose, note, published)


def model_sources(model: str) -> list[dict]:
    is_a52 = model == "Galaxy A52 LTE"
    local_url = (
        "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a52-5g/buy/"
        if is_a52 else "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a72/buy/"
    )
    local_note = (
        "Samsung Philippines' buying tool labels Galaxy A52 and Galaxy A52 5G separately and lists "
        "8 GB/128 GB and 8 GB/256 GB choices for the standard A52. The local black 8 GB/256 GB "
        "order code is SM-A525FZKIXTC. This review is for the LTE A52 (family SM-A525F), not A52 5G."
        if is_a52 else
        "Samsung Philippines' Galaxy A72 listing and 2021 local offer identify the Philippine A72 "
        "family. The black 8 GB/256 GB order code is SM-A725FZKHXTC; this color-specific code is "
        "not applied to the color-unspecified 8 GB/128 GB configuration."
    )
    official = source(
        f"samsung_{'a52' if is_a52 else 'a72'}_ph_product_identity",
        "Samsung Philippines", local_url,
        "Philippine model identity, network-family separation, and available memory choices",
        local_note,
    )
    price = source(
        "samsung_a52_a72_ph_prices_2021_05",
        "Samsung Philippines",
        "https://www.samsung.com/ph/offer/offline/2021/kumu-live-galaxy-a-series-promo/",
        "Dated Philippine Samsung SRP by exact memory configuration",
        "Samsung Philippines lists 8 GB/128 GB and 8 GB/256 GB prices separately for the Galaxy A52 "
        "and A72. The promotion was valid 25 May–3 June 2021; these are historical SRPs, not current prices.",
        "2021-05-25",
    )
    launch_promo = source(
        "samsung_a52_a72_ph_launch_promo_2021",
        "Samsung Philippines",
        "https://www.samsung.com/ph/offer/offline/2021/galaxy-a52-a72/launch-promo/",
        "Dated Philippine purchase availability through authorized Samsung dealers",
        "Samsung Philippines' launch promotion covers purchases of the Galaxy A52 and A72 from select "
        "authorized dealers nationwide during 26 March–4 April 2021. The period supports availability "
        "from 26 March, but does not identify the first transaction time.",
    )
    specs = source(
        "samsung_a52_a72_specs_2021_h1",
        "Samsung Electronics",
        "https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2021_Half_Year_Report.pdf",
        "Manufacturer specifications and LTE/5G platform distinction",
        "Samsung's 2021 half-year report identifies A52 LTE as SDM720G (separate from A52 5G's SDM750G) "
        "and lists display, refresh rate, dimensions, camera array, launch OS, and battery for the A52 LTE "
        "and A72 families.",
    )
    global_launch = source(
        "samsung_a52_a72_global_launch_2021",
        "Samsung Global Newsroom",
        "https://news.samsung.com/global/the-galaxy-a52-a52-5g-and-a72-make-innovation-accessible-to-all",
        "Model family and global launch announcement",
        "Samsung announced Galaxy A52, A52 5G, and A72 as distinct products on 17 March 2021. Global launch "
        "details are used only for model-family context; Philippine configuration and price evidence comes "
        "from Samsung Philippines.",
        "2021-03-17",
    )
    yugatech = source(
        f"yugatech_{'a52_a52_5g_a72' if is_a52 else 'a72_hands_on'}_2021",
        "YugaTech",
        ("https://www.yugatech.com/mobile/samsung-galaxy-a52-a52-5g-a72-specs-price-philippines/"
         if is_a52 else "https://www.yugatech.com/mobile/samsung-galaxy-a72-hands-on/"),
        "Philippine availability date and corroborating technical specifications",
        ("YugaTech's 17 March 2021 launch report distinguishes the standard Galaxy A52's 4G LTE/SDM720G "
         "from the A52 5G's 5G/SDM750G and reports nationwide availability beginning 26 March 2021. "
         "Its listed A52 specifications are used as secondary evidence where Samsung's report is silent."
         if is_a52 else
         "YugaTech's 18 March 2021 hands-on identifies the A72 as a 4G LTE model and supplies its launch "
         "configuration and secondary technical details. Its launch coverage reports nationwide availability "
         "beginning 26 March 2021."),
        "2021-03-17" if is_a52 else "2021-03-18",
    )
    sources = [official, price, launch_promo, specs, global_launch, yugatech]
    if is_a52:
        sources.append(source(
            "pinoytechnoguide_a52_specs_2021",
            "Pinoy Techno Guide",
            "https://www.pinoytechnoguide.com/smartphones/samsung-galaxy-a52",
            "Corroborating exact-model specifications and original Philippine listing context",
            "Pinoy Techno Guide's 17 March 2021 Galaxy A52 page lists the standard 4G LTE model and detailed "
            "camera, battery, charging, connectivity, and physical specifications. Its 8 GB/256 GB entry is "
            "not generalized to the separate 8 GB/128 GB configuration.",
            "2021-03-17",
        ))
    return sources


def specs_for(model: str) -> list[dict]:
    is_a52 = model == "Galaxy A52 LTE"
    family = "samsung_a52_ph_product_identity" if is_a52 else "samsung_a72_ph_product_identity"
    official_specs = "samsung_a52_a72_specs_2021_h1"
    secondary = "pinoytechnoguide_a52_specs_2021" if is_a52 else "yugatech_a72_hands_on_2021"
    online_article = "yugatech_a52_a52_5g_a72_2021" if is_a52 else secondary
    model_code = "SM-A525F" if is_a52 else "SM-A725F"
    display = 6.5 if is_a52 else 6.7
    battery = 4500 if is_a52 else 5000
    width, height, thickness = (75.1, 159.9, 8.4) if is_a52 else (77.4, 165.0, 8.4)
    rear = (
        "64 MP main with OIS + 12 MP ultra-wide + 5 MP depth + 5 MP macro"
        if is_a52 else
        "64 MP main with OIS + 12 MP ultra-wide + 8 MP telephoto + 5 MP macro"
    )
    rows = [
        f("model_number", family, f"Samsung Philippines model family {model_code}", model_code,
          note="Model-family code only. A color-specific order code is retained only when the cited Samsung Philippines source identifies it."),
        f("display_size", official_specs, f"{display:.1f}-inch display", display, key="displayInches", unit="in"),
        f("display_technology", official_specs, "Super AMOLED", "Super AMOLED", key="displayType"),
        f("display_resolution", official_specs, "FHD+ (2,400 x 1,080 pixels)", "1080 x 2400", key="resolution"),
        f("display_refresh_rate", official_specs, "90 Hz (LTE model)", 90, key="refreshHz", unit="Hz"),
        f("display_brightness", official_specs, "Up to 800 nits", 800, unit="nits"),
        f("chipset", official_specs, "Qualcomm SDM720G platform", "Qualcomm Snapdragon 720G", key="chipset"),
        f("cpu", secondary, "Octa-core Qualcomm Snapdragon 720G CPU", "Octa-core Snapdragon 720G", key="cpu", status="VERIFIED_SECONDARY"),
        f("gpu", secondary, "Adreno 618 GPU", "Adreno 618", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", official_specs, "Android 11 with One UI 3.1 at launch", "Android 11 / One UI 3.1", key="os"),
        f("rear_camera_system", official_specs, rear, 64, key="rearCameraMp", unit="MP",
          note="The numeric catalog field stores the 64 MP main sensor; the source value preserves the full rear-camera array."),
        f("main_camera_sensor", secondary, "64 MP main camera, f/1.8, autofocus, optical image stabilization", "64 MP; f/1.8; AF; OIS", status="VERIFIED_SECONDARY"),
        f("ultrawide_camera", secondary, "12 MP ultra-wide camera, f/2.2", "12 MP; f/2.2", status="VERIFIED_SECONDARY"),
        f("front_camera", secondary, "32 MP front camera, f/2.2", 32, key="frontCameraMp", unit="MP", status="VERIFIED_SECONDARY"),
        f("video_recording", secondary, "4K video recording at 30 fps", "4K/30 fps", key="video", status="VERIFIED_SECONDARY"),
        f("battery_capacity", official_specs, f"{battery:,} mAh", battery, key="batteryMah", unit="mAh"),
        f("wired_charging", secondary, "Up to 25 W wired fast charging", 25, key="chargingW", unit="W", status="VERIFIED_SECONDARY"),
        f("dimensions", official_specs, f"{height:.1f} x {width:.1f} x {thickness:.1f} mm (H x W x D)",
          f"{height:.1f} x {width:.1f} x {thickness:.1f} mm", key="dimensions", unit="mm"),
        f("weight", secondary, "189 g" if is_a52 else "203 g", 189 if is_a52 else 203,
          key="weightG", unit="g", status="VERIFIED_SECONDARY"),
        f("ingress_protection", "samsung_a52_a72_global_launch_2021", "IP67 water and dust resistance", "IP67",
          replace_existing=True),
        f("cellular_bands", online_article, "4G LTE, 3G HSPA+, 2G EDGE/GPRS; individual LTE bands not recorded",
          "4G LTE, 3G HSPA+, 2G EDGE/GPRS", key="cellular", status="VERIFIED_SECONDARY"),
        f("sim_esim", secondary, "Dual Nano-SIM; hybrid SIM/microSD slot", "Dual Nano-SIM; hybrid SIM/microSD", key="sim", status="VERIFIED_SECONDARY"),
        f("wifi", secondary, "Wi-Fi 802.11 a/b/g/n/ac (dual-band)", "Wi-Fi 5 (802.11 a/b/g/n/ac)", key="wifi", status="VERIFIED_SECONDARY"),
        f("bluetooth", secondary, "Bluetooth 5.0", "Bluetooth 5.0", status="VERIFIED_SECONDARY"),
        f("nfc", secondary, "NFC supported", "Yes", status="VERIFIED_SECONDARY"),
        f("gnss", secondary, "GPS, A-GPS, GLONASS, BeiDou, and Galileo", "GPS; A-GPS; GLONASS; BeiDou; Galileo", status="VERIFIED_SECONDARY"),
        f("usb", secondary, "USB Type-C", "USB Type-C", key="ports", status="VERIFIED_SECONDARY"),
        f("audio", secondary, "Stereo loudspeakers and Dolby Atmos; 3.5 mm audio jack",
          "Stereo speakers; Dolby Atmos; 3.5 mm jack", key="sound", status="VERIFIED_SECONDARY"),
        f("storage_expansion", secondary, "microSD expansion up to 1 TB", "microSD up to 1 TB", status="VERIFIED_SECONDARY"),
    ]
    if is_a52:
        rows.append(f("telephoto_camera", official_specs,
                       "No telephoto camera; Samsung lists main, ultra-wide, depth, and macro rear modules.",
                       "Not applicable", status="NOT_APPLICABLE"))
    else:
        rows.append(f("telephoto_camera", secondary, "8 MP telephoto camera with OIS, f/2.4, 3x optical zoom",
                       "8 MP; f/2.4; OIS; 3x optical zoom", status="VERIFIED_SECONDARY"))
    return rows


def build_records() -> list[dict]:
    output = []
    price_source_id = "samsung_a52_a72_ph_prices_2021_05"
    launch_source_id = "samsung_a52_a72_ph_launch_promo_2021"
    model_data = [
        {
            "deviceId": "device_edb8f688862988", "model": "Galaxy A52 LTE", "isA52": True,
            "code": "SM-A525F", "sku256": "SM-A525FZKIXTC",
            "configs": [(128, 17490), (256, 18990)],
            "launch_price_source": "pinoytechnoguide_a52_specs_2021",
            "launch_price": {256: 18990},
        },
        {
            "deviceId": "device_528380ceb337d2", "model": "Galaxy A72", "isA52": False,
            "code": "SM-A725F", "sku256": "SM-A725FZKHXTC",
            "configs": [(128, 22490), (256, 23990)],
            "launch_price_source": "yugatech_a72_hands_on_2021",
            "launch_price": {256: 23990},
        },
    ]
    for model_info in model_data:
        device_id = model_info["deviceId"]
        model = model_info["model"]
        sources = model_sources(model)
        variants = [
            {
                "id": f"{device_id}-samsung-8gb-{storage}gb",
                "label": f"8 GB RAM / {storage} GB storage",
                "sku": model_info["sku256"] if storage == 256 else None,
                "modelCode": model_info["code"],
                "notes": ("Exact Philippine color-specific SKU is not recorded for this configuration."
                          if storage == 128 else None),
            }
            for storage, _price in model_info["configs"]
        ]
        availability = {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine availability documented from 26 March 2021; exact first transaction time not recorded",
            "philippineAvailability": (
                "Samsung Philippines' launch promotion covered purchases through select authorized dealers "
                "from 26 March 2021, and YugaTech reported nationwide availability beginning that date. "
                "The date records reported nationwide availability; the exact first transaction time is not stated."
            ),
            "observedAt": OBSERVED,
            "qualityFlag": "Philippine availability dated; exact first-sale transaction time not disclosed",
        }
        for index, (storage, price_php) in enumerate(model_info["configs"]):
            configuration = f"8 GB RAM / {storage} GB storage"
            config_id = f"{device_id}-samsung-8gb-{storage}gb"
            fields = [
                f("configuration", price_source_id, configuration, configuration),
                f("ram_capacity", price_source_id, "8 GB", 8, key="ramGb", unit="GB"),
                f("storage_capacity", price_source_id, f"{storage} GB", storage, key="storageGb", unit="GB"),
                f("philippine_release_date", launch_source_id,
                  "Samsung Philippines' launch promotion covered authorized dealer purchases beginning 26 March 2021.",
                  "2021-03-26", status="VERIFIED",
                  note="Records the official Philippine promo start and documented authorized-sale availability, not the first individual transaction time."),
                f("official_launch_price_php", model_info["launch_price_source"],
                  (f"Philippine launch coverage reports PHP {model_info['launch_price'][storage]:,} for the {storage} GB configuration."
                   if storage in model_info["launch_price"] else
                   "The launch coverage does not unambiguously tie its single quoted price to this configuration."),
                  model_info["launch_price"].get(storage),
                  status="VERIFIED_SECONDARY" if storage in model_info["launch_price"] else "PENDING_VERIFICATION",
                  unit="PHP",
                  note=("Launch-period Philippine price reported by secondary coverage and corroborated by the later Samsung Philippines SRP table; not a current offer."
                        if storage in model_info["launch_price"] else
                        "A launch article quotes one model price without tying it unambiguously to this configuration; no launch price is assigned.")),
                f("current_price_php", price_source_id,
                  f"Historical Samsung Philippines SRP, 25 May 2021: PHP {price_php:,}", price_php,
                  unit="PHP", note="Historical Samsung Philippines SRP observed in a promotion valid 25 May–3 June 2021; not a current offer.",
                  price_condition="new", price_type="Historical Samsung Philippines SRP (not a current offer)",
                  price_observed="2021-05-25"),
                *specs_for(model),
            ]
            item = record(device_id, model, config_id, configuration, sources, fields,
                          model_code=model_info["code"],
                          sku=model_info["sku256"] if storage == 256 else None,
                          availability=availability)
            if index == 0:
                item["replacementVariants"] = variants
            output.append(item)
    return output


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = build_records()
    for item in items:
        add_review(manual, catalog, item)
        if item.get("replacementVariants"):
            device = next(d for d in catalog if d["id"] == item["deviceId"])
            device["variants"] = [
                {"id": variant["id"], "label": variant["label"], "specs": {}, "sku": variant.get("sku"), "modelCode": variant.get("modelCode")}
                for variant in item["replacementVariants"]
            ]
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "reviewedConfigurations": len(items),
        "models": len({item["deviceId"] for item in items}),
        "reviewedAt": OBSERVED,
    }, indent=2))


if __name__ == "__main__":
    main()
