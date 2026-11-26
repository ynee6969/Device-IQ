#!/usr/bin/env python3
"""Review Samsung Galaxy A34, A54, and A36 Philippine configurations."""
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


def build_records():
    output = []

    # A34 5G
    device = "device_b1444d256c2933"
    product_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a34-5g-awesome-graphite-128gb-sm-a346ezkcphl/"
    product_256_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a34-5g-awesome-graphite-256gb-sm-a346ezkephl/"
    local_url = "https://news.samsung.com/ph/awesome-together-samsung-launches-the-new-galaxy-a-series-in-the-philippines-with-a-spectacular-launch-party"
    global_specs_url = "https://news.samsung.com/global/the-samsung-galaxy-a54-5g-and-galaxy-a34-5g-awesome-experiences-for-all"
    product = src("samsung_a34_ph_product_specs", "Samsung Philippines", product_url,
                  "Exact local Galaxy A34 5G model and specifications",
                  "Official Samsung Philippines product page for local SKU SM-A346EZKCPHL, an 8 GB/128 GB Galaxy A34 5G. The page also lists the 8 GB/256 GB option and detailed hardware specifications.")
    product_256 = src("samsung_a34_ph_256_sku", "Samsung Philippines", product_256_url,
                      "Exact local 8 GB/256 GB Galaxy A34 5G configuration",
                      "Samsung Philippines identifies the local SM-A346EZKEPHL 8 GB/256 GB configuration.")
    launch = src("samsung_a34_ph_price_availability", "Samsung Newsroom Philippines", local_url,
                 "Philippine availability, authorized channels, configuration prices, and processor",
                 "Samsung's 18 April 2023 Philippines launch coverage identifies the Galaxy A34 5G, MediaTek Dimensity 1080, authorized sales channels, and listed prices of PHP 19,990 for 8 GB/128 GB and PHP 21,990 for 8 GB/256 GB. It does not state the exact first sale date.",
                 "2023-04-18")
    global_specs = src("samsung_a34_a54_global_launch_specs", "Samsung Global Newsroom", global_specs_url,
                       "Galaxy A34 5G launch operating system",
                       "Samsung's global launch specifications identify Android 13 with One UI 5.1 at launch. Philippine RAM and storage are taken from Samsung Philippines sources.",
                       "2023-03-15")
    variants = [
        {"id": f"{device}-auto-8gb-128gb", "label": "8 GB RAM / 128 GB storage", "modelCode": "SM-A346E", "sku": "SM-A346EZKCPHL"},
        {"id": f"{device}-auto-8gb-256gb", "label": "8 GB RAM / 256 GB storage", "modelCode": "SM-A346E", "sku": "SM-A346EZKEPHL"},
    ]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Available",
        "philippineAvailability": "Samsung Philippines listed the Galaxy A34 5G through Samsung.com, Experience Stores, authorized stores, and partner retailers in April 2023; exact first-sale date is not recorded.",
        "observedAt": OBSERVED,
        "qualityFlag": "Philippine availability verified; exact first-sale date not recorded",
    }
    shared = [
        f("model_number", "samsung_a34_ph_product_specs", "SM-A346E Philippine model family; example local SKU SM-A346EZKEPHL.", "SM-A346E"),
        f("display_size", "samsung_a34_ph_product_specs", "6.6 inches (full rectangle)", 6.6, key="displayInches", unit="in"),
        f("display_technology", "samsung_a34_ph_product_specs", "Super AMOLED", "Super AMOLED", key="displayType"),
        f("display_resolution", "samsung_a34_ph_product_specs", "1080 x 2340 (FHD+)", "1080 x 2340", key="resolution"),
        f("display_refresh_rate", "samsung_a34_ph_product_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", "samsung_a34_ph_product_specs", "1,000 nits at High Brightness Mode", 1000, unit="nits"),
        f("chipset", "samsung_a34_ph_price_availability", "MediaTek Dimensity 1080", "MediaTek Dimensity 1080", key="chipset"),
        f("cpu", "samsung_a34_ph_product_specs", "Octa-core; 2.6 GHz and 2.0 GHz", "Octa-core 2.6 / 2.0 GHz"),
        f("rear_camera_system", "samsung_a34_ph_product_specs", "48 MP main + 8 MP ultra-wide + 5 MP macro rear cameras", 48, key="rearCameraMp", unit="MP",
          note="The numeric catalog field stores the main sensor; this source value retains all listed rear cameras."),
        f("main_camera_sensor", "samsung_a34_ph_product_specs", "48 MP main camera, f/1.8, autofocus, OIS", "48 MP; f/1.8; AF; OIS"),
        f("ultrawide_camera", "samsung_a34_ph_product_specs", "8 MP ultra-wide camera, f/2.2", "8 MP; f/2.2"),
        f("telephoto_camera", "samsung_a34_ph_product_specs", "No telephoto module is listed in Samsung's three-camera specification.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", "samsung_a34_ph_product_specs", "13 MP front camera, f/2.2", 13, key="frontCameraMp", unit="MP"),
        f("video_recording", "samsung_a34_ph_product_specs", "UHD 4K (3840 x 2160) at 30 fps", "UHD 4K/30 fps"),
        f("battery_capacity", "samsung_a34_ph_product_specs", "5,000 mAh typical; 4,905 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
          note="The catalog stores typical capacity; Samsung separately states rated minimum capacity."),
        f("wired_charging", "samsung_a34_ph_price_availability", "Samsung says Super Fast Charging but does not state wattage in the cited local sources.", None,
          status="NOT_DISCLOSED", note="No charging wattage is recorded from these Samsung Philippines sources."),
        f("dimensions", "samsung_a34_ph_product_specs", "161.3 x 78.1 x 8.2 mm", "161.3 x 78.1 x 8.2 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_a34_ph_product_specs", "199 g", 199, key="weightG", unit="g"),
        f("ingress_protection", "samsung_a34_ph_product_specs", "IP67", "IP67"),
        f("operating_system", "samsung_a34_a54_global_launch_specs", "Android 13 with One UI 5.1 at launch", "Android 13 / One UI 5.1", key="os"),
        f("storage_expansion", "samsung_a34_ph_product_specs", "microSD support up to 1 TB", "microSD up to 1 TB"),
        f("wifi", "samsung_a34_ph_product_specs", "802.11 a/b/g/n/ac, 2.4 GHz and 5 GHz", "802.11 a/b/g/n/ac", key="wifi"),
        f("bluetooth", "samsung_a34_ph_product_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
    ]
    for storage, price in [(128, 19990), (256, 21990)]:
        config = f"{device}-auto-8gb-{storage}gb"
        label = f"8 GB RAM / {storage} GB storage"
        config_source = "samsung_a34_ph_product_specs" if storage == 128 else "samsung_a34_ph_256_sku"
        config_sku = "SM-A346EZKCPHL" if storage == 128 else "SM-A346EZKEPHL"
        fields = [
            f("configuration", config_source, label, label),
            f("ram_capacity", config_source, "8 GB", 8, key="ramGb", unit="GB"),
            f("storage_capacity", config_source, f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "samsung_a34_ph_price_availability", "Exact first-sale date not stated in Samsung Philippines launch coverage.", None,
              status="NOT_DISCLOSED", note="Philippine availability is verified, but the cited source does not give the exact first-sale date."),
            f("official_launch_price_php", "samsung_a34_ph_price_availability", f"Samsung Philippines listed price: PHP {price:,}", price, unit="PHP",
              note="Official listed price in April 2023 Philippine launch coverage; not a current offer."),
            f("current_price_php", "samsung_a34_ph_price_availability", f"Historical Samsung Philippines listed price: PHP {price:,}", price, unit="PHP",
              note="Dated Samsung Philippines price observation from 18 April 2023; not a current offer.", price_condition="new",
              price_type="Historical Samsung Philippines listed price (not a current offer)", price_observed="2023-04-18"),
            *shared,
        ]
        output.append(record(device, "Galaxy A34 5G", config, label, [product, product_256, launch, global_specs], fields,
                             variants=variants, model_code="SM-A346E", sku=config_sku, availability=availability))

    # A54 5G
    device = "device_de761fe6bf288e"
    product_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a54-5g-awesome-graphite-128gb-sm-a546ezkcphl/"
    product_256_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a54-5g-awesome-graphite-256gb-sm-a546ezkdphl/"
    local_url = "https://news.samsung.com/ph/awesome-together-samsung-launches-the-new-galaxy-a-series-in-the-philippines-with-a-spectacular-launch-party"
    global_specs_url = "https://news.samsung.com/global/the-samsung-galaxy-a54-5g-and-galaxy-a34-5g-awesome-experiences-for-all"
    product = src("samsung_a54_ph_product_specs", "Samsung Philippines", product_url,
                  "Exact local Galaxy A54 5G model and specifications",
                  "Official Samsung Philippines page identifies the local SM-A546E Galaxy A54 5G and lists its 8 GB/128 GB configuration and detailed hardware specifications.")
    product_256 = src("samsung_a54_ph_256_sku", "Samsung Philippines", product_256_url,
                      "Exact local 8 GB/256 GB Galaxy A54 5G configuration",
                      "Samsung Philippines identifies the local SM-A546EZKDPHL 8 GB/256 GB configuration.")
    launch = src("samsung_a54_ph_price_availability", "Samsung Newsroom Philippines", local_url,
                 "Philippine availability, authorized channels, configuration prices, and processor",
                 "Samsung's 18 April 2023 Philippines launch coverage identifies the Galaxy A54 5G, Exynos 1380, authorized sales channels, and listed prices of PHP 24,990 for 8 GB/128 GB and PHP 26,990 for 8 GB/256 GB. It does not state the exact first sale date.",
                 "2023-04-18")
    global_specs = src("samsung_a34_a54_global_launch_specs", "Samsung Global Newsroom", global_specs_url,
                       "Galaxy A54 5G launch operating system",
                       "Samsung's global launch specifications identify Android 13 with One UI 5.1 at launch. Philippine RAM and storage are taken from Samsung Philippines sources.",
                       "2023-03-15")
    variants = [
        {"id": f"{device}-auto-8gb-128gb", "label": "8 GB RAM / 128 GB storage", "modelCode": "SM-A546E", "sku": "SM-A546EZKCPHL"},
        {"id": f"{device}-auto-8gb-256gb", "label": "8 GB RAM / 256 GB storage", "modelCode": "SM-A546E", "sku": "SM-A546EZKDPHL"},
    ]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Available",
        "philippineAvailability": "Samsung Philippines listed the Galaxy A54 5G through Samsung.com, Experience Stores, authorized stores, and partner retailers in April 2023; exact first-sale date is not recorded.",
        "observedAt": OBSERVED,
        "qualityFlag": "Philippine availability verified; exact first-sale date not recorded",
    }
    shared = [
        f("model_number", "samsung_a54_ph_product_specs", "SM-A546E Philippine model family; example local 8 GB/128 GB SKU SM-A546EZKCPHL.", "SM-A546E"),
        f("display_size", "samsung_a54_ph_product_specs", "6.4 inches (full rectangle)", 6.4, key="displayInches", unit="in"),
        f("display_technology", "samsung_a54_ph_product_specs", "Super AMOLED", "Super AMOLED", key="displayType"),
        f("display_resolution", "samsung_a54_ph_product_specs", "1080 x 2340 (FHD+)", "1080 x 2340", key="resolution"),
        f("display_refresh_rate", "samsung_a54_ph_product_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("chipset", "samsung_a54_ph_price_availability", "Samsung Exynos 1380", "Exynos 1380", key="chipset"),
        f("cpu", "samsung_a54_ph_product_specs", "Octa-core; 2.4 GHz and 2.0 GHz", "Octa-core 2.4 / 2.0 GHz"),
        f("rear_camera_system", "samsung_a54_ph_product_specs", "50 MP main + 12 MP ultra-wide + 5 MP macro rear cameras", 50, key="rearCameraMp", unit="MP",
          note="The numeric catalog field stores the main sensor; source value retains the complete camera array."),
        f("main_camera_sensor", "samsung_a54_ph_product_specs", "50 MP main camera, f/1.8, autofocus, OIS", "50 MP; f/1.8; AF; OIS"),
        f("ultrawide_camera", "samsung_a54_ph_product_specs", "12 MP ultra-wide camera, f/2.2", "12 MP; f/2.2"),
        f("telephoto_camera", "samsung_a54_ph_product_specs", "No telephoto module is listed in Samsung's three-camera specification.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", "samsung_a54_ph_product_specs", "32 MP front camera, f/2.2", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", "samsung_a54_ph_product_specs", "UHD 4K (3840 x 2160) at 30 fps", "UHD 4K/30 fps"),
        f("battery_capacity", "samsung_a54_ph_product_specs", "5,000 mAh typical; 4,905 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
          note="The catalog stores typical capacity; Samsung separately states rated minimum capacity."),
        f("wired_charging", "samsung_a54_ph_price_availability", "Samsung describes Super Fast Charging but does not state wattage in the cited local sources.", None,
          status="NOT_DISCLOSED", note="No charging wattage is recorded from these Samsung Philippines sources."),
        f("dimensions", "samsung_a54_ph_product_specs", "158.2 x 76.7 x 8.2 mm", "158.2 x 76.7 x 8.2 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_a54_ph_product_specs", "202 g", 202, key="weightG", unit="g"),
        f("ingress_protection", "samsung_a54_ph_product_specs", "IP67", "IP67"),
        f("operating_system", "samsung_a34_a54_global_launch_specs", "Android 13 with One UI 5.1 at launch", "Android 13 / One UI 5.1", key="os"),
        f("storage_expansion", "samsung_a54_ph_product_specs", "microSD support up to 1 TB", "microSD up to 1 TB"),
        f("wifi", "samsung_a54_ph_product_specs", "802.11 a/b/g/n/ac/ax, 2.4 GHz and 5 GHz", "Wi-Fi 6 (802.11ax)", key="wifi"),
        f("bluetooth", "samsung_a54_ph_product_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
    ]
    for storage, price in [(128, 24990), (256, 26990)]:
        config = f"{device}-auto-8gb-{storage}gb"
        label = f"8 GB RAM / {storage} GB storage"
        config_source = "samsung_a54_ph_product_specs" if storage == 128 else "samsung_a54_ph_256_sku"
        config_sku = "SM-A546EZKCPHL" if storage == 128 else "SM-A546EZKDPHL"
        fields = [
            f("configuration", config_source, label, label),
            f("ram_capacity", config_source, "8 GB", 8, key="ramGb", unit="GB"),
            f("storage_capacity", config_source, f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "samsung_a54_ph_price_availability", "Exact first-sale date not stated in Samsung Philippines launch coverage.", None,
              status="NOT_DISCLOSED", note="Philippine availability is verified, but the cited source does not give the exact first-sale date."),
            f("official_launch_price_php", "samsung_a54_ph_price_availability", f"Samsung Philippines listed price: PHP {price:,}", price, unit="PHP",
              note="Official listed price in April 2023 Philippine launch coverage; not a current offer."),
            f("current_price_php", "samsung_a54_ph_price_availability", f"Historical Samsung Philippines listed price: PHP {price:,}", price, unit="PHP",
              note="Dated Samsung Philippines price observation from 18 April 2023; not a current offer.", price_condition="new",
              price_type="Historical Samsung Philippines listed price (not a current offer)", price_observed="2023-04-18"),
            *shared,
        ]
        output.append(record(device, "Galaxy A54 5G", config, label, [product, product_256, launch, global_specs], fields,
                             variants=variants, model_code="SM-A546E", sku=config_sku, availability=availability))

    # A36 5G
    device = "device_6649cf0c87cf5f"
    product_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a36-5g-awesome-black-128gb-sm-a366bzksphl/"
    product_256_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a36-5g-awesome-lavender-256gb-sm-a366blvtphl/"
    launch_url = "https://news.samsung.com/ph/samsung-marks-a-step-forward-with-ai-for-everyone-by-introducing-new-galaxy-a56-5g-and-galaxy-a36-5g"
    global_launch_url = "https://news.samsung.com/us/samsung-new-galaxy-a56-a36-a26-5g-marks-step-forward-with-ai-for-everyone/"
    price_url = "https://news.samsung.com/ph/discover-awesome-intelligence-this-summer-with-samsung"
    product = src("samsung_a36_ph_product_specs", "Samsung Philippines", product_url,
                  "Exact local Galaxy A36 5G model, 8 GB/128 GB configuration, and specifications",
                  "Official Samsung Philippines page identifies the SM-A366B family and lists detailed display, camera, memory, connectivity, physical, and battery specifications.")
    product_256 = src("samsung_a36_ph_256_sku", "Samsung Philippines", product_256_url,
                      "Exact local 8 GB/256 GB Galaxy A36 5G configuration",
                      "Samsung Philippines links this Galaxy A36 5G 8 GB/256 GB Lavender model from its official local newsroom page.")
    launch = src("samsung_a36_ph_launch_specs", "Samsung Newsroom Philippines", launch_url,
                 "Philippine availability window and launch-level hardware specifications",
                 "Samsung stated availability by 17 March 2025 at Experience Stores and partner retailers and by 24 March online; these are by-date deadlines, not an exact first-sale date. The same source identifies the Snapdragon 6 Gen 3 platform, 45 W charging, IP67, One UI 7.0, and 5,000 mAh typical battery.",
                 "2025-03-02")
    global_launch = src("samsung_a36_global_launch_os", "Samsung Newsroom US", global_launch_url,
                        "Galaxy A36 5G launch operating system version",
                        "Samsung's global launch specification lists Android 15. The separate Philippines source is used for local availability and pricing.",
                        "2025-03-02")
    price_source = src("samsung_a36_ph_price_apr2025", "Samsung Newsroom Philippines", price_url,
                       "Dated Philippine A36 5G listed prices by exact configuration",
                       "Samsung lists PHP 19,990 for 8 GB/128 GB (online exclusive) and PHP 21,990 for 8 GB/256 GB. These are 16 April 2025 listed-price observations, not current offers or an asserted original MSRP.",
                       "2025-04-16")
    variants = [
        {"id": f"{device}-auto-8gb-128gb", "label": "8 GB RAM / 128 GB storage", "modelCode": "SM-A366B", "sku": "SM-A366BZKSPHL"},
        {"id": f"{device}-auto-8gb-256gb", "label": "8 GB RAM / 256 GB storage", "modelCode": "SM-A366B", "sku": "SM-A366BLVTPHL"},
    ]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Available",
        "philippineAvailability": "Samsung Philippines announced availability by 17 March 2025 at Experience Stores and partner retailers, and by 24 March online. The exact first-sale date is not recorded.",
        "observedAt": OBSERVED,
        "qualityFlag": "Local availability verified; exact first-sale date not disclosed",
    }
    shared = [
        f("model_number", "samsung_a36_ph_product_specs", "SM-A366B Philippine product family; example 8 GB/128 GB SKU SM-A366BZKSPHL.", "SM-A366B"),
        f("display_size", "samsung_a36_ph_product_specs", "6.7 inches (full rectangle)", 6.7, key="displayInches", unit="in"),
        f("display_technology", "samsung_a36_ph_product_specs", "Super AMOLED", "Super AMOLED", key="displayType"),
        f("display_resolution", "samsung_a36_ph_product_specs", "1080 x 2340 (FHD+)", "1080 x 2340", key="resolution"),
        f("display_refresh_rate", "samsung_a36_ph_product_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", "samsung_a36_ph_product_specs", "Up to 1,200 nits HBM", 1200, unit="nits"),
        f("chipset", "samsung_a36_ph_launch_specs", "Qualcomm Snapdragon 6 Gen 3 Mobile Platform", "Snapdragon 6 Gen 3", key="chipset"),
        f("cpu", "samsung_a36_ph_product_specs", "Octa-core; 2.4 GHz and 1.8 GHz", "Octa-core 2.4 / 1.8 GHz"),
        f("rear_camera_system", "samsung_a36_ph_product_specs", "50 MP main + 8 MP ultra-wide + 5 MP macro rear cameras", 50, key="rearCameraMp", unit="MP",
          note="The numeric catalog field stores the main sensor; source value retains the complete camera array."),
        f("main_camera_sensor", "samsung_a36_ph_product_specs", "50 MP main camera, f/1.8, autofocus, OIS", "50 MP; f/1.8; AF; OIS"),
        f("ultrawide_camera", "samsung_a36_ph_product_specs", "8 MP ultra-wide camera, f/2.2", "8 MP; f/2.2"),
        f("telephoto_camera", "samsung_a36_ph_product_specs", "No telephoto module is listed in Samsung's three-camera specification.", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", "samsung_a36_ph_product_specs", "12 MP front camera, f/2.2", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", "samsung_a36_ph_product_specs", "UHD 4K (3840 x 2160) at 30 fps", "UHD 4K/30 fps"),
        f("battery_capacity", "samsung_a36_ph_product_specs", "5,000 mAh typical", 5000, key="batteryMah", unit="mAh"),
        f("wired_charging", "samsung_a36_ph_launch_specs", "45 W Super Fast Charge 2.0", 45, key="chargingW", unit="W"),
        f("dimensions", "samsung_a36_ph_product_specs", "162.9 x 78.2 x 7.4 mm", "162.9 x 78.2 x 7.4 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_a36_ph_product_specs", "195 g", 195, key="weightG", unit="g"),
        f("ingress_protection", "samsung_a36_ph_launch_specs", "IP67", "IP67"),
        f("operating_system", "samsung_a36_global_launch_os", "Android 15 with One UI 7.0 at launch", "Android 15 / One UI 7.0", key="os"),
        f("wifi", "samsung_a36_ph_product_specs", "802.11a/b/g/n/ac/ax, 2.4 GHz and 5 GHz", "Wi-Fi 6 (802.11ax)", key="wifi"),
        f("bluetooth", "samsung_a36_ph_product_specs", "Bluetooth 5.4", "Bluetooth 5.4"),
    ]
    for storage, price in [(128, 19990), (256, 21990)]:
        config = f"{device}-auto-8gb-{storage}gb"
        label = f"8 GB RAM / {storage} GB storage"
        config_source = "samsung_a36_ph_product_specs" if storage == 128 else "samsung_a36_ph_256_sku"
        config_sku = "SM-A366BZKSPHL" if storage == 128 else "SM-A366BLVTPHL"
        fields = [
            f("configuration", config_source, label, label),
            f("ram_capacity", config_source, "8 GB", 8, key="ramGb", unit="GB"),
            f("storage_capacity", config_source, f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "samsung_a36_ph_launch_specs", "Samsung says availability by 17 March at physical retail and partner stores; exact first-sale date not stated.", None,
              status="NOT_DISCLOSED", note="The announcement uses a by-date deadline, not an exact first-sale date."),
            f("current_price_php", "samsung_a36_ph_price_apr2025", f"Historical Samsung Philippines listed price: PHP {price:,}", price, unit="PHP",
              note="Dated Samsung Philippines listed-price observation from 16 April 2025; not a current offer or an asserted original MSRP.",
              price_condition="new", price_type="Historical Samsung Philippines listed price (not a current offer)", price_observed="2025-04-16"),
            *shared,
        ]
        output.append(record(device, "Galaxy A36 5G", config, label,
                             [product, product_256, launch, price_source, global_launch], fields,
                             variants=variants, model_code="SM-A366B", sku=config_sku, availability=availability))
    return output


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = build_records()
    for item in items:
        add_review(manual, catalog, item)
    first_for_device = set()
    for item in items:
        review = next(r for r in manual["records"] if
                      (r["deviceId"], r["configurationId"]) ==
                      (item["deviceId"], item["configurationId"]))
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
