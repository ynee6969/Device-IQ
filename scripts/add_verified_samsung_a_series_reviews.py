#!/usr/bin/env python3
"""Manually review Samsung Galaxy A55 and A56 Philippine configurations."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"


def src(sid, publisher, url, purpose, note, published=None):
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid, sid, value, normalized=None, *, key=None, unit=None, status="VERIFIED",
      note=None, price_condition=None, price_type=None, price_observed=None,
      replace_existing=False):
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    if price_condition:
        row.update({"priceCondition": price_condition, "priceType": price_type,
                    "priceObservedAt": price_observed})
    if replace_existing:
        row["replaceExisting"] = True
    return row


def record(device_id, model, config_id, label, sources, fields, *, variants=None,
           model_code=None, sku=None, availability=None):
    row = {"deviceId": device_id, "configurationId": config_id,
           "brand": "Samsung", "model": model,
           "configuration": label, "sources": sources, "fields": fields}
    if variants:
        row["replacementVariants"] = variants
    if model_code:
        row["modelCode"] = model_code
    if sku:
        row["sku"] = sku
    if availability:
        row["availabilityEvidence"] = availability
    return row


def records():
    out = []

    # Galaxy A56 5G: replace a crawler's corrupted resolution and dimensions,
    # then use Samsung's own dated local price table for each exact storage tier.
    device = "device_28ca17138af731"
    product_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a56-5g-awesome-graphite-128gb-sm-a566bzksphl/"
    launch_url = "https://news.samsung.com/ph/samsung-marks-a-step-forward-with-ai-for-everyone-by-introducing-new-galaxy-a56-5g-and-galaxy-a36-5g"
    price_url = "https://news.samsung.com/ph/discover-awesome-intelligence-this-summer-with-samsung"
    a56_product = src(
        "samsung_a56_ph_product_specs", "Samsung Philippines", product_url,
        "Local Galaxy A56 5G product identity and hardware specifications",
        "Samsung Philippines identifies the SM-A566B Galaxy A56 5G family and provides exact local product configuration, display resolution, camera, connectivity, and physical specifications.",
    )
    a56_launch = src(
        "samsung_a56_ph_launch_specs", "Samsung Newsroom Philippines", launch_url,
        "Philippine availability window and model-level launch specifications",
        "Samsung states the Galaxy A56 5G would be available in the Philippines by 17 March 2025 at Samsung Experience Stores and partner retailers, and in the Samsung Online Store by 24 March. Its 2 March 2025 specification table lists launch OS, processor, cameras, battery, charging, and IP rating; it gives a by-date, not the exact first sale timestamp.",
        "2025-03-02",
    )
    a56_price = src(
        "samsung_a56_ph_price_apr2025", "Samsung Newsroom Philippines", price_url,
        "Dated Philippine prices by exact Galaxy A56 5G configuration",
        "Samsung Newsroom Philippines lists PHP 23,990 for 8 GB/128 GB (online exclusive) and PHP 25,990 for 8 GB/256 GB. These are price observations published 16 April 2025, not current offers.",
        "2025-04-16",
    )
    a56_availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Available",
        "philippineAvailability": "Samsung Philippines announced availability by 17 March 2025 at Samsung Experience Stores and partner retailers, and by 24 March in its online store. The exact first-sale date is not recorded.",
        "observedAt": OBSERVED,
        "qualityFlag": "Local availability verified; exact first-sale date not disclosed",
    }
    a56_configs = [
        ("config_663b8685d47596", "8 GB RAM / 128 GB storage", 128, 23990, "SM-A566BZKSPHL"),
        (device + "-8gb-256gb", "8 GB RAM / 256 GB storage", 256, 25990, None),
    ]
    a56_shared = [
        f("model_number", "samsung_a56_ph_product_specs", "SM-A566B local model family; the 8 GB/128 GB product page uses color-specific SKU SM-A566BZKSPHL.", "SM-A566B",
          note="The model family is recorded; the Graphite color-specific order code is not applied to the color-unspecified 8 GB/256 GB variant."),
        f("display_size", "samsung_a56_ph_product_specs", "6.7 inches (full rectangle)", 6.7, key="displayInches", unit="in"),
        f("display_technology", "samsung_a56_ph_product_specs", "Super AMOLED", "Super AMOLED", key="displayType"),
        f("display_resolution", "samsung_a56_ph_product_specs", "1080 x 2340 (FHD+)", "1080 x 2340", key="resolution", replace_existing=True),
        f("display_refresh_rate", "samsung_a56_ph_product_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("chipset", "samsung_a56_ph_launch_specs", "Exynos 1580", "Exynos 1580", key="chipset"),
        f("rear_camera_system", "samsung_a56_ph_launch_specs", "50 MP main + 12 MP ultra-wide + 5 MP macro rear cameras", 50,
          key="rearCameraMp", unit="MP", note="The catalog's numeric rear-camera value is the 50 MP main sensor; the source value retains the complete camera array."),
        f("main_camera_sensor", "samsung_a56_ph_launch_specs", "50 MP main camera, f/1.8, autofocus, OIS, HDR", "50 MP; f/1.8; AF; OIS; HDR"),
        f("ultrawide_camera", "samsung_a56_ph_launch_specs", "12 MP ultra-wide camera, f/2.2", "12 MP; f/2.2"),
        f("telephoto_camera", "samsung_a56_ph_launch_specs", "No dedicated telephoto camera listed in Samsung's Galaxy A56 5G specification table.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", "samsung_a56_ph_launch_specs", "12 MP front camera, f/2.2", 12, key="frontCameraMp", unit="MP"),
        f("battery_capacity", "samsung_a56_ph_launch_specs", "5,000 mAh typical; 4,905 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
          note="Samsung separately states the 4,905 mAh rated minimum; the catalog stores typical capacity."),
        f("wired_charging", "samsung_a56_ph_launch_specs", "45 W Super Fast Charge 2.0", 45, key="chargingW", unit="W"),
        f("dimensions", "samsung_a56_ph_product_specs", "162.2 x 77.5 x 7.4 mm", "162.2 x 77.5 x 7.4 mm", key="dimensions", unit="mm", replace_existing=True),
        f("weight", "samsung_a56_ph_product_specs", "198 g; weight may vary by market", 198, key="weightG", unit="g"),
        f("ingress_protection", "samsung_a56_ph_launch_specs", "IP67", "IP67"),
        f("operating_system", "samsung_a56_ph_launch_specs", "Android 15 with One UI 7.0 at launch", "Android 15 / One UI 7.0", key="os",
          note="Samsung's launch specification; later software updates may change the installed version."),
        f("wifi", "samsung_a56_ph_product_specs", "Wi-Fi 6", "Wi-Fi 6", key="wifi"),
        f("bluetooth", "samsung_a56_ph_product_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
    ]
    for config, label, storage, price, sku in a56_configs:
        fields = [
            f("configuration", "samsung_a56_ph_price_apr2025", label, label),
            f("ram_capacity", "samsung_a56_ph_price_apr2025", "8 GB", 8, key="ramGb", unit="GB"),
            f("storage_capacity", "samsung_a56_ph_price_apr2025", f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("current_price_php", "samsung_a56_ph_price_apr2025", f"Historical Samsung Philippines listed price: PHP {price:,}", price, unit="PHP",
              note="Dated Samsung Philippines price observation from 16 April 2025; not a current offer.", price_condition="new",
              price_type="Historical Samsung Philippines listed price (not a current offer)", price_observed="2025-04-16",
              replace_existing=True),
            *a56_shared,
        ]
        out.append(record(device, "Galaxy A56 5G", config, label,
                          [a56_product, a56_launch, a56_price], fields,
                          model_code="SM-A566B", sku=sku, availability=a56_availability))

    # The workbook contains a second shorthand A56 record separate from the
    # exact Galaxy A56 5G entry. Keep both inventory IDs, but apply the same
    # model match and source-backed configurations to the shorthand row.
    alias_id = "device_183607a456844b"
    alias_variants = [
        {"id": f"{alias_id}-auto-8gb-{storage}gb", "label": label,
         "sku": sku, "modelCode": "SM-A566B"}
        for _config, label, storage, _price, sku in a56_configs
    ]
    for original, alias_variant in zip(out[-len(a56_configs):], alias_variants):
        cloned = deepcopy(original)
        cloned["deviceId"] = alias_id
        cloned["configurationId"] = alias_variant["id"]
        cloned["configuration"] = alias_variant["label"]
        cloned["replacementVariants"] = alias_variants
        out.append(cloned)

    # Galaxy A55 inventory shorthand is matched to Samsung's exact local A55
    # 5G product family. The operator storage option stays separate, with its
    # documented 8 GB memory from Smart and no invented retail price.
    device = "device_8a8a8e9ba58d74"
    a55_product_url = "https://www.samsung.com/ph/business/smartphones/galaxy-a/galaxy-a55-5g-awesome-iceblue-256gb-sm-a556elbcphl/"
    a55_news_url = "https://news.samsung.com/ph/samsung-galaxy-a55-5g-and-galaxy-a35-5g-awesome-innovations-and-security-engineered-for-everyone"
    a55_smart_url = "https://store.smart.com.ph/samsung/samsung-galaxy-a55-5g/1602411721.html"
    a55_globe_url = "https://new.globe.com.ph/deals/prepaid-promos/devices/samsung/smartphones"
    a55_product = src(
        "samsung_a55_ph_product_specs", "Samsung Philippines", a55_product_url,
        "Exact local Galaxy A55 5G 8 GB/256 GB SKU and model hardware",
        "Samsung Philippines lists local SKU SM-A556ELBCPHL as Awesome Iceblue, 8 GB/256 GB and provides detailed A55 5G specifications. The color-specific SKU is not assigned to the color-unspecified inventory variants.",
    )
    a55_news = src(
        "samsung_a55_ph_launch_price", "Samsung Newsroom Philippines", a55_news_url,
        "Philippine availability start, launch price, local operator option, and model specifications",
        "Samsung Philippines states Galaxy A55 5G availability starting 18 March 2024, an 8 GB/256 GB Philippine launch price of PHP 24,990, and a 128 GB storage option through Globe and Smart. The announcement does not state the RAM or price for the 128 GB option.",
        "2024-03-12",
    )
    a55_smart = src(
        "smart_a55_128_config", "Smart Communications", a55_smart_url,
        "Philippine operator configuration for Galaxy A55 5G",
        "Smart's online catalog identifies Galaxy A55 5G with 8 GB RAM and 128 GB storage. Its displayed PHP 13,000 is a plan cash-out/starting amount, not the device's full retail price, so no 128 GB device price is recorded.",
    )
    a55_globe = src(
        "globe_a55_128_price", "Globe Online Prepaid", a55_globe_url,
        "Exact A55 5G 128 GB operator configuration and listed price",
        "Globe's official Samsung smartphone listing identifies Galaxy A55 5G, 128 GB, and a PHP 23,990 prepaid purchase price. The adjacent Smart product page independently confirms 8 GB RAM for its 128 GB option; the model and storage match. This is a dated operator listing, not the Samsung 256 GB launch SRP.",
    )
    a55_variants = [
        {"id": f"{device}-auto-8gb-256gb", "label": "8 GB RAM / 256 GB storage", "modelCode": "SM-A556E"},
        {"id": f"{device}-auto-8gb-128gb", "label": "8 GB RAM / 128 GB storage · operator variant", "modelCode": "SM-A556E"},
    ]
    a55_availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Available",
        "philippineAvailability": "Samsung Philippines states authorized-channel availability starting 18 March 2024; its announcement identifies the 8 GB/256 GB retail configuration and a separate 128 GB operator option.",
        "observedAt": OBSERVED,
        "qualityFlag": "128 GB variant has no recorded full retail price; Smart's plan cash-out is not treated as a device price",
    }
    a55_shared = [
        f("model_number", "samsung_a55_ph_product_specs", "SM-A556E Philippine model family; example local 8 GB/256 GB SKU SM-A556ELBCPHL.", "SM-A556E",
          note="Model family is verified; the color-specific Samsung SKU is not assigned to the inventory configuration."),
        f("display_size", "samsung_a55_ph_product_specs", "6.6 inches (full rectangle)", 6.6, key="displayInches", unit="in"),
        f("display_technology", "samsung_a55_ph_product_specs", "Super AMOLED", "Super AMOLED", key="displayType"),
        f("display_resolution", "samsung_a55_ph_product_specs", "1080 x 2340 (FHD+)", "1080 x 2340", key="resolution"),
        f("display_refresh_rate", "samsung_a55_ph_product_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("chipset", "samsung_a55_ph_product_specs", "Exynos 1480 (model processor family)", "Exynos 1480", key="chipset"),
        f("cpu", "samsung_a55_ph_product_specs", "Octa-core; 2.75 GHz and 2.0 GHz", "Octa-core 2.75 / 2.0 GHz"),
        f("rear_camera_system", "samsung_a55_ph_product_specs", "50 MP wide + 12 MP ultra-wide + 5 MP macro rear cameras", 50,
          key="rearCameraMp", unit="MP", note="Catalog's numeric rear-camera field stores the 50 MP main sensor; source value retains the complete camera array."),
        f("main_camera_sensor", "samsung_a55_ph_product_specs", "50 MP wide camera, f/1.8, with OIS", "50 MP; f/1.8; OIS"),
        f("ultrawide_camera", "samsung_a55_ph_product_specs", "12 MP ultra-wide camera, f/2.2", "12 MP; f/2.2"),
        f("telephoto_camera", "samsung_a55_ph_product_specs", "No dedicated telephoto camera listed; 5 MP macro module is separate.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", "samsung_a55_ph_product_specs", "32 MP front camera, f/2.2", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", "samsung_a55_ph_product_specs", "Rear video up to UHD 4K at 30 fps", "Rear up to 4K/30 fps"),
        f("battery_capacity", "samsung_a55_ph_product_specs", "5,000 mAh typical; 4,905 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
          note="Samsung separately states the rated minimum; catalog value uses typical capacity."),
        f("wired_charging", "smart_a55_128_config", "Smart lists 25 W fast charging", 25, key="chargingW", unit="W", status="VERIFIED_SECONDARY",
          note="Operator source; Samsung's cited local spec page does not provide a charging wattage."),
        f("dimensions", "samsung_a55_ph_product_specs", "161.1 x 77.4 x 8.2 mm", "161.1 x 77.4 x 8.2 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_a55_ph_product_specs", "213 g", 213, key="weightG", unit="g"),
        f("ingress_protection", "samsung_a55_ph_product_specs", "IP67", "IP67"),
        f("operating_system", "samsung_a55_ph_launch_price", "Android 14 with One UI 6.1 at launch", "Android 14 / One UI 6.1", key="os",
          note="Initial launch software; subsequent updates may change installed OS."),
        f("wifi", "samsung_a55_ph_product_specs", "Wi-Fi 6 (802.11ax)", "Wi-Fi 6", key="wifi"),
        f("bluetooth", "samsung_a55_ph_product_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
    ]
    for config, label, storage, price, src_id in [
        (a55_variants[0]["id"], a55_variants[0]["label"], 256, 24990, "samsung_a55_ph_launch_price"),
        (a55_variants[1]["id"], a55_variants[1]["label"], 128, None, "smart_a55_128_config"),
    ]:
        fields = [
            f("configuration", src_id, label, label),
            f("ram_capacity", src_id, "8 GB", 8, key="ramGb", unit="GB"),
            f("storage_capacity", src_id, f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "samsung_a55_ph_launch_price", "Authorized retail availability began 18 March 2024.", "2024-03-18",
              note="Samsung Philippines states these devices were available starting 18 March 2024."),
            *a55_shared,
        ]
        if price is not None:
            fields.extend([
                f("official_launch_price_php", "samsung_a55_ph_launch_price", "Original Philippine SRP: PHP 24,990 for 8 GB/256 GB", price, unit="PHP"),
                f("current_price_php", "samsung_a55_ph_launch_price", "Historical Philippine launch SRP: PHP 24,990", price, unit="PHP",
                  note="Dated manufacturer launch-price observation; not a current selling offer.", price_condition="new",
                  price_type="Historical official Philippine launch SRP (not a current offer)", price_observed="2024-03-18"),
            ])
        else:
            fields.append(f("current_price_php", "globe_a55_128_price",
                             "Globe Prepaid listed price: PHP 23,990 for Galaxy A55 5G 128 GB", 23990, unit="PHP",
                             status="VERIFIED_SECONDARY", note="Observed on Globe's official online prepaid device listing on 26 November 2026; not the 2024 Samsung launch SRP.",
                             price_condition="new", price_type="Globe Prepaid listed price", price_observed=OBSERVED,
                             replace_existing=True))
        out.append(record(device, "Galaxy A55 5G", config, label,
                          [a55_product, a55_news, a55_smart, a55_globe], fields,
                          variants=a55_variants, model_code="SM-A556E",
                          availability=a55_availability))

    # Galaxy A35 5G: the 8/256 local retail SKU and price are documented by
    # Samsung; Globe separately lists the 128 GB operator model and price but
    # does not disclose its RAM, which stays blank in this record.
    device = "device_45c7e8bb258a1d"
    a35_product_url = "https://www.samsung.com/ph/business/smartphones/galaxy-a/galaxy-a35-5g-awesome-navy-256gb-sm-a356ezkgphl/"
    a35_news_url = a55_news_url
    a35_globe_url = "https://new.globe.com.ph/deals/prepaid-promos/devices/samsung/smartphones/galaxy-a35-5g-128gb-awesome-lilac"
    a35_product = src(
        "samsung_a35_ph_product_specs", "Samsung Philippines", a35_product_url,
        "Exact local Galaxy A35 5G model, 8 GB/256 GB configuration, and hardware specifications",
        "Samsung Philippines identifies the local SM-A356E SKU and lists 8 GB RAM/256 GB storage with detailed display, camera, processor, battery, connectivity, and dimensions.",
    )
    a35_news = src(
        "samsung_a35_ph_launch_price", "Samsung Newsroom Philippines", a35_news_url,
        "Philippine launch availability, 8 GB/256 GB price, and operator-only 128 GB option",
        "Samsung states Galaxy A35 5G was available in the Philippines starting 18 March 2024 at PHP 20,990 for 8 GB/256 GB. A 128 GB option was offered only through Globe and Smart; the release announcement does not disclose RAM for that option.",
        "2024-03-12",
    )
    a35_globe = src(
        "globe_a35_128_price_specs", "Globe Online Prepaid", a35_globe_url,
        "Exact Galaxy A35 5G 128 GB Globe prepaid variant, listed price, and specifications",
        "Globe lists Galaxy A35 5G 128 GB in Awesome Lilac at PHP 19,990 and publishes display, processor, camera, battery, network, and storage specifications. The page does not state RAM, so RAM is left unrecorded.",
    )
    a35_variants = [
        {"id": f"{device}-auto-8gb-256gb", "label": "8 GB RAM / 256 GB storage", "modelCode": "SM-A356E"},
        {"id": f"{device}-auto-ram-unrecorded-128gb", "label": "RAM not recorded / 128 GB storage · Globe Prepaid variant", "modelCode": "SM-A356E"},
    ]
    a35_availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Available",
        "philippineAvailability": "Samsung Philippines states authorized retail availability starting 18 March 2024; its launch source distinguishes the 8 GB/256 GB retail tier and a 128 GB operator option.",
        "observedAt": OBSERVED,
        "qualityFlag": "128 GB Globe variant has no published RAM value; RAM is not inferred",
    }
    a35_shared = [
        f("model_number", "samsung_a35_ph_product_specs", "SM-A356E Philippine model family; example local Navy 8 GB/256 GB SKU SM-A356EZKGPHL.", "SM-A356E"),
        f("display_size", "samsung_a35_ph_product_specs", "6.6 inches (full rectangle)", 6.6, key="displayInches", unit="in"),
        f("display_technology", "samsung_a35_ph_product_specs", "Super AMOLED", "Super AMOLED", key="displayType"),
        f("display_resolution", "samsung_a35_ph_product_specs", "1080 x 2340 (FHD+)", "1080 x 2340", key="resolution"),
        f("display_refresh_rate", "samsung_a35_ph_product_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("chipset", "samsung_a35_ph_product_specs", "Samsung Exynos 1380 (S5E8835)", "Exynos 1380", key="chipset"),
        f("cpu", "samsung_a35_ph_product_specs", "Octa-core; 2.4 GHz and 2.0 GHz", "Octa-core 2.4 / 2.0 GHz"),
        f("rear_camera_system", "samsung_a35_ph_product_specs", "50 MP wide + 8 MP ultra-wide + 5 MP macro rear cameras", 50, key="rearCameraMp", unit="MP",
          note="Catalog numeric rear-camera value is the 50 MP main sensor; source value retains the complete array."),
        f("main_camera_sensor", "samsung_a35_ph_product_specs", "50 MP wide camera, f/1.8, with autofocus and OIS", "50 MP; f/1.8; AF; OIS"),
        f("ultrawide_camera", "samsung_a35_ph_product_specs", "8 MP ultra-wide camera, f/2.2", "8 MP; f/2.2"),
        f("telephoto_camera", "samsung_a35_ph_product_specs", "No dedicated telephoto camera listed; 5 MP macro module is separate.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", "samsung_a35_ph_product_specs", "13 MP front camera, f/2.2", 13, key="frontCameraMp", unit="MP"),
        f("video_recording", "samsung_a35_ph_product_specs", "Rear video up to UHD 4K at 30 fps", "Rear up to 4K/30 fps"),
        f("battery_capacity", "samsung_a35_ph_product_specs", "5,000 mAh typical; 4,905 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
          note="Samsung states 4,905 mAh rated minimum; catalog value is typical capacity."),
        f("wired_charging", "samsung_a35_ph_launch_price", "Super Fast Charging; Samsung page does not state wattage.", None,
          status="NOT_DISCLOSED", note="Charging wattage is not stated on the cited Samsung Philippines product and launch pages."),
        f("dimensions", "samsung_a35_ph_product_specs", "161.7 x 78.0 x 8.2 mm", "161.7 x 78.0 x 8.2 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_a35_ph_product_specs", "209 g", 209, key="weightG", unit="g"),
        f("ingress_protection", "samsung_a35_ph_product_specs", "IP67", "IP67"),
        f("wifi", "samsung_a35_ph_product_specs", "Wi-Fi 6 (802.11ax)", "Wi-Fi 6", key="wifi"),
        f("bluetooth", "samsung_a35_ph_product_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
    ]
    for config, label, storage, ram, price, price_source in [
        (a35_variants[0]["id"], a35_variants[0]["label"], 256, 8, 20990, "samsung_a35_ph_launch_price"),
        (a35_variants[1]["id"], a35_variants[1]["label"], 128, None, 19990, "globe_a35_128_price_specs"),
    ]:
        config_source = "samsung_a35_ph_launch_price" if storage == 256 else "globe_a35_128_price_specs"
        fields = [
            f("configuration", config_source, label, label),
            f("storage_capacity", config_source, f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "samsung_a35_ph_launch_price", "Authorized Philippine availability started 18 March 2024.", "2024-03-18",
              note="Samsung Philippines launch announcement gives the availability start date."),
            *a35_shared,
            f("current_price_php", price_source,
              (f"Historical official Philippine launch SRP: PHP {price:,} for 8 GB/256 GB" if storage == 256 else f"Globe Prepaid listed price: PHP {price:,} for Galaxy A35 5G 128 GB"),
              price, unit="PHP", status=("VERIFIED" if storage == 256 else "VERIFIED_SECONDARY"),
              note=("Dated Samsung Philippines launch price; not a current offer." if storage == 256 else "Observed on Globe's official prepaid product page on 26 November 2026; RAM is not disclosed."),
              price_condition="new",
              price_type=("Historical official Philippine launch SRP (not a current offer)" if storage == 256 else "Globe Prepaid listed price"),
              price_observed=("2024-03-18" if storage == 256 else OBSERVED)),
        ]
        if ram is not None:
            fields.insert(2, f("ram_capacity", "samsung_a35_ph_launch_price", "8 GB", 8, key="ramGb", unit="GB"))
        else:
            fields.insert(2, f("ram_capacity", "globe_a35_128_price_specs", "RAM not stated on the Globe listing.", None,
                               status="PENDING_VERIFICATION", note="No numeric RAM value is published in the cited local operator listing."))
        out.append(record(device, "Galaxy A35 5G", config, label,
                          [a35_product, a35_news, a35_globe], fields,
                          variants=a35_variants, model_code="SM-A356E",
                          availability=a35_availability))
    return out


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = records()
    for item in items:
        add_review(manual, catalog, item)
    # Samsung gives A56's local partner-store availability as "by 17 March",
    # which is a deadline, not an exact first-sale date. Keep the text evidence
    # while clearing the misleading normalized date from the catalog.
    for review in manual["records"]:
        if review.get("deviceId") not in {"device_28ca17138af731", "device_183607a456844b"}:
            continue
        for field in review.get("fields", []):
            if field.get("fieldId") == "philippine_release_date":
                field.update({
                    "status": "NOT_DISCLOSED",
                    "sourceValue": "Samsung states availability by 17 March 2025 at stores and partner retailers; this does not identify the exact first sale date.",
                    "normalizedValue": None,
                    "note": "The source provides a by-date deadline, not an exact local first-sale date.",
                    "clearDeviceAvailabilityDate": True,
                })
    # A variant replacement is model-scoped and must be applied once by the
    # catalog builder, even though each configuration needs the list to be
    # recognized by the review helper above.
    first_for_device = set()
    for item in items:
        review = next(r for r in manual["records"] if
                      (r["deviceId"], r["configurationId"]) ==
                      (item["deviceId"], item["configurationId"]))
        if item["deviceId"] == "device_28ca17138af731":
            # These two exact configurations already exist in the workbook.
            review.pop("replacementVariants", None)
        if item["deviceId"] in first_for_device:
            review.pop("replacementVariants", None)
        else:
            first_for_device.add(item["deviceId"])
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewedConfigurations": len(items),
                      "models": len({item["deviceId"] for item in items}),
                      "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
