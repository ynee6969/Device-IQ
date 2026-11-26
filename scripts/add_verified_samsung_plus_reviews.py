#!/usr/bin/env python3
"""Add manufacturer-backed configuration reviews for Samsung Galaxy Plus phones."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"


def src(sid, publisher, url, purpose, note, published=None):
    return {
        "id": sid,
        "publisher": publisher,
        "url": url,
        "publicationDate": published,
        "accessDate": OBSERVED,
        "purpose": purpose,
        "note": note,
    }


def f(fid, sid, value, normalized=None, *, key=None, unit=None, status="VERIFIED",
      note=None, price_condition=None, price_type=None, price_observed=None,
      replace_existing=False):
    row = {
        "fieldId": fid,
        "status": status,
        "sourceId": sid,
        "sourceValue": value,
        "normalizedValue": normalized,
    }
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    if replace_existing:
        row["replaceExisting"] = True
    if price_condition:
        row.update({
            "priceCondition": price_condition,
            "priceType": price_type,
            "priceObservedAt": price_observed,
        })
    return row


def config_review(device_id, model, config_id, label, variants, sources, fields,
                  *, model_code=None, sku=None):
    return {
        "deviceId": device_id,
        "configurationId": config_id,
        "brand": "Samsung",
        "model": model,
        "configuration": label,
        "sources": sources,
        "fields": fields,
        "replacementVariants": variants,
        "modelCode": model_code,
        "sku": sku,
    }


def records():
    out = []

    # Galaxy S23+: the official Philippine spec page ties the exact 8/512 SKU
    # to this model; Samsung's PH launch table establishes the 8/256 and 8/512
    # options and their original Philippine SRPs.
    device = "device_9b51cd23075357"
    s23_specs_url = "https://www.samsung.com/ph/smartphones/galaxy-s/galaxy-s23-plus-cream-512gb-sm-s916bzecphl/"
    s23_news_url = "https://news.samsung.com/ph/take-your-passions-further-with-the-new-samsung-galaxy-s23-series-designed-for-a-premium-experience-today-and-beyond"
    s23_specs = src(
        "samsung_s23plus_ph_specs", "Samsung Philippines", s23_specs_url,
        "Exact local model SKU and Galaxy S23+ hardware specifications",
        "Samsung Philippines identifies an SM-S916BZECPHL 8 GB/512 GB Galaxy S23+ SKU and lists the model-specific display, camera, processor, storage, connectivity, dimensions, and battery specifications.",
    )
    s23_launch = src(
        "samsung_s23plus_ph_launch", "Samsung Newsroom Philippines", s23_news_url,
        "Philippine launch configurations, original SRPs, and model specifications",
        "Samsung's Philippine newsroom lists Galaxy S23+ configurations at 8 GB/256 GB and 8 GB/512 GB, their PHP 68,990 and PHP 76,990 SRPs, and the model-level specification table. Its local preorder window began 2 February 2023.",
        "2023-02-02",
    )
    s23_variants = [
        {"id": f"{device}-auto-8gb-256gb", "label": "8 GB RAM / 256 GB storage", "modelCode": "SM-S916B"},
        {"id": f"{device}-auto-8gb-512gb", "label": "8 GB RAM / 512 GB storage", "modelCode": "SM-S916B"},
    ]
    s23_shared = [
        f("model_number", "samsung_s23plus_ph_specs", "SM-S916B model family; Samsung Philippines retail SKU SM-S916BZECPHL is the Cream 8 GB/512 GB example.", "SM-S916B",
          note="The model family is verified. The color-specific retail SKU is not assigned to the inventory configuration."),
        f("display_size", "samsung_s23plus_ph_specs", "6.6 inches (full rectangle)", 6.6, key="displayInches", unit="in"),
        f("display_technology", "samsung_s23plus_ph_specs", "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType"),
        f("display_resolution", "samsung_s23plus_ph_specs", "2340 x 1080 (FHD+)", "2340 x 1080", key="resolution"),
        f("display_refresh_rate", "samsung_s23plus_ph_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("chipset", "samsung_s23plus_ph_launch", "Snapdragon 8 Gen 2 Mobile Platform for Galaxy", "Snapdragon 8 Gen 2 for Galaxy", key="chipset"),
        f("cpu", "samsung_s23plus_ph_specs", "Octa-core; 3.36 GHz, 2.8 GHz, and 2 GHz", "Octa-core 3.36 / 2.8 / 2.0 GHz"),
        f("rear_camera_system", "samsung_s23plus_ph_specs", "50 MP wide + 10 MP 3x telephoto + 12 MP ultra-wide rear cameras", 50,
          key="rearCameraMp", unit="MP", note="Catalog's numeric rear-camera field stores the 50 MP main camera; the source value retains the full triple-camera array."),
        f("main_camera_sensor", "samsung_s23plus_ph_specs", "50 MP wide camera, f/1.8, with optical image stabilization", "50 MP; f/1.8; OIS"),
        f("ultrawide_camera", "samsung_s23plus_ph_specs", "12 MP ultra-wide camera, f/2.2", "12 MP; f/2.2"),
        f("telephoto_camera", "samsung_s23plus_ph_specs", "10 MP telephoto camera with 3x optical zoom, f/2.4", "10 MP; 3x optical zoom; f/2.4"),
        f("front_camera", "samsung_s23plus_ph_specs", "12 MP front camera", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", "samsung_s23plus_ph_specs", "Rear video up to UHD 8K at 30 fps", "Rear up to 8K/30 fps"),
        f("battery_capacity", "samsung_s23plus_ph_launch", "4,700 mAh typical; 4,563 mAh rated minimum", 4700, key="batteryMah", unit="mAh",
          note="Samsung separately states the 4,563 mAh rated minimum; the catalog value uses typical capacity."),
        f("wired_charging", "samsung_s23plus_ph_launch", "45 W wired charging; adapter sold separately", 45, key="chargingW", unit="W"),
        f("wireless_charging", "samsung_s23plus_ph_launch", "Fast Wireless Charging 2.0 and Wireless PowerShare", "Fast Wireless Charging 2.0; Wireless PowerShare"),
        f("dimensions", "samsung_s23plus_ph_specs", "157.8 x 76.2 x 7.6 mm (H x W x D)", "157.8 x 76.2 x 7.6 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_s23plus_ph_specs", "195 g", 195, key="weightG", unit="g"),
        f("wifi", "samsung_s23plus_ph_specs", "Wi-Fi 6E (802.11 a/b/g/n/ac/ax; 2.4, 5, and 6 GHz)", "Wi-Fi 6E", key="wifi"),
        f("bluetooth", "samsung_s23plus_ph_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
        f("ingress_protection", "samsung_s23plus_ph_launch", "IP68", "IP68"),
        f("operating_system", "samsung_s23plus_ph_launch", "Android 13 with One UI 5.1", "Android 13 / One UI 5.1", key="os"),
    ]
    for config_id, label, storage, price in [
        (s23_variants[0]["id"], s23_variants[0]["label"], 256, 68990),
        (s23_variants[1]["id"], s23_variants[1]["label"], 512, 76990),
    ]:
        fields = [
            f("configuration", "samsung_s23plus_ph_launch", f"8 GB RAM / {storage} GB storage", f"8 GB RAM / {storage} GB storage"),
            f("ram_capacity", "samsung_s23plus_ph_launch", "8 GB", 8, key="ramGb", unit="GB"),
            f("storage_capacity", "samsung_s23plus_ph_launch", f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("official_launch_price_php", "samsung_s23plus_ph_launch", f"Original Philippine SRP: PHP {price:,} for {storage} GB", price, unit="PHP",
              note="Manufacturer launch SRP reported by Samsung Newsroom Philippines; not a current offer."),
            f("current_price_php", "samsung_s23plus_ph_launch", f"Historical Philippine launch SRP: PHP {price:,} ({storage} GB)", price, unit="PHP",
              note="Dated launch-price observation from the Philippine Samsung newsroom; not a current selling offer.",
              price_condition="new", price_type="Historical official Philippine launch SRP (not a current offer)", price_observed="2023-02-02"),
            *s23_shared,
        ]
        out.append(config_review(device, "Galaxy S23+", config_id, label, s23_variants,
                                 [s23_specs, s23_launch], fields, model_code="SM-S916B"))

    # Galaxy S24+: Samsung's Philippine SKU page identifies 12/256 hardware;
    # Samsung's local preorder price table lists the 12/256 and 12/512 options.
    device = "device_af72f6e6d0b475"
    s24_specs_url = "https://www.samsung.com/ph/business/smartphones/galaxy-s/galaxy-s24-plus-onyx-black-256gb-sm-s926bzkbphl/"
    s24_price_url = "https://www.samsung.com/ph/offer/offline/2024/galaxy-s24-home-credit/"
    s24_launch_url = "https://www.samsung.com/ph/offer/offline/2024/galaxy-s24-preorder/"
    s24_news_url = "https://news.samsung.com/ph/enter-the-new-era-of-mobile-ai-with-samsung-galaxy-s24-series"
    s24_specs = src(
        "samsung_s24plus_ph_specs", "Samsung Philippines", s24_specs_url,
        "Philippine 12 GB/256 GB retail SKU and technical specifications",
        "Samsung Philippines lists local SKU SM-S926BZKBPHL as a 12 GB/256 GB Galaxy S24+ and provides the model's processor, display, cameras, connectivity, dimensions, weight, and typical battery specifications.",
    )
    s24_prices = src(
        "samsung_s24plus_ph_launch_price", "Samsung Philippines", s24_price_url,
        "Philippine launch SRPs by Galaxy S24+ storage configuration",
        "Samsung's Philippine offer table lists the original Galaxy S24+ SRP as PHP 68,990 for 12 GB/256 GB and PHP 76,990 for 12 GB/512 GB. These are historical launch SRPs, not current offers.",
        "2024-01-18",
    )
    s24_launch = src(
        "samsung_s24plus_ph_preorder", "Samsung Philippines", s24_launch_url,
        "Dated Philippine preorder campaign",
        "Samsung Philippines identifies the local Galaxy S24 preorder period; the cited price table is used separately for the configuration-specific SRPs.",
        "2024-01-18",
    )
    s24_news = src(
        "samsung_s24plus_ph_newsroom_specs", "Samsung Newsroom Philippines", s24_news_url,
        "Official model introduction, launch software, processor, and connectivity",
        "Samsung Newsroom Philippines' 18 January 2024 S24-series announcement lists the S24+ with Exynos 2400 for Galaxy, Android 14/One UI 6.1, Wi-Fi 6E, Bluetooth 5.3, and IP68.",
        "2024-01-18",
    )
    s24_variants = [
        {"id": f"{device}-auto-12gb-256gb", "label": "12 GB RAM / 256 GB storage", "modelCode": "SM-S926B"},
        {"id": f"{device}-auto-12gb-512gb", "label": "12 GB RAM / 512 GB storage", "modelCode": "SM-S926B"},
    ]
    s24_shared = [
        f("model_number", "samsung_s24plus_ph_specs", "SM-S926B model family; local example SKU SM-S926BZKBPHL is Onyx Black 12 GB/256 GB.", "SM-S926B",
          note="The local model family is verified. The color-specific order code is not assigned to the inventory configuration."),
        f("display_size", "samsung_s24plus_ph_specs", "6.7 inches (full rectangle)", 6.7, key="displayInches", unit="in"),
        f("display_technology", "samsung_s24plus_ph_specs", "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType"),
        f("display_resolution", "samsung_s24plus_ph_specs", "3120 x 1440 (QHD+)", "3120 x 1440", key="resolution"),
        f("display_refresh_rate", "samsung_s24plus_ph_specs", "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("chipset", "samsung_s24plus_ph_newsroom_specs", "Exynos 2400 for Galaxy", "Exynos 2400 for Galaxy", key="chipset", replace_existing=True),
        f("cpu", "samsung_s24plus_ph_specs", "Deca-core; 3.2, 2.9, 2.6, and 1.95 GHz", "Deca-core 3.2 / 2.9 / 2.6 / 1.95 GHz"),
        f("rear_camera_system", "samsung_s24plus_ph_specs", "50 MP wide + 10 MP telephoto + 12 MP ultra-wide rear cameras", 50,
          key="rearCameraMp", unit="MP", note="Catalog's numeric rear-camera field stores the 50 MP main camera; the source value retains the full triple-camera array."),
        f("main_camera_sensor", "samsung_s24plus_ph_specs", "50 MP wide camera, f/1.8, with optical image stabilization", "50 MP; f/1.8; OIS"),
        f("ultrawide_camera", "samsung_s24plus_ph_specs", "12 MP ultra-wide camera, f/2.2", "12 MP; f/2.2"),
        f("telephoto_camera", "samsung_s24plus_ph_specs", "10 MP telephoto with 3x optical zoom, f/2.4", "10 MP; 3x optical zoom; f/2.4"),
        f("front_camera", "samsung_s24plus_ph_specs", "12 MP front camera", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", "samsung_s24plus_ph_specs", "Rear video up to UHD 8K at 30 fps", "Rear up to 8K/30 fps"),
        f("battery_capacity", "samsung_s24plus_ph_specs", "4,900 mAh typical; 4,755 mAh rated minimum", 4900, key="batteryMah", unit="mAh",
          note="Samsung separately states the rated minimum; the catalog value uses typical capacity."),
        f("wired_charging", "samsung_s24plus_ph_specs", "45 W wired charging; adapter sold separately", 45, key="chargingW", unit="W"),
        f("wireless_charging", "samsung_s24plus_ph_specs", "Fast Wireless Charging 2.0 and Wireless PowerShare", "Fast Wireless Charging 2.0; Wireless PowerShare"),
        f("dimensions", "samsung_s24plus_ph_specs", "158.5 x 75.9 x 7.7 mm (H x W x D)", "158.5 x 75.9 x 7.7 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_s24plus_ph_specs", "196 g", 196, key="weightG", unit="g"),
        f("wifi", "samsung_s24plus_ph_specs", "Wi-Fi 6E (2.4, 5, and 6 GHz)", "Wi-Fi 6E", key="wifi"),
        f("bluetooth", "samsung_s24plus_ph_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
        f("ingress_protection", "samsung_s24plus_ph_specs", "IP68", "IP68"),
        f("operating_system", "samsung_s24plus_ph_newsroom_specs", "Android 14 with One UI 6.1", "Android 14 / One UI 6.1", key="os",
          note="Initial launch software as listed in Samsung's Galaxy S24 series announcement.", replace_existing=True),
    ]
    for config_id, label, storage, price in [
        (s24_variants[0]["id"], s24_variants[0]["label"], 256, 68990),
        (s24_variants[1]["id"], s24_variants[1]["label"], 512, 76990),
    ]:
        fields = [
            f("configuration", "samsung_s24plus_ph_launch_price", f"12 GB RAM / {storage} GB storage", f"12 GB RAM / {storage} GB storage"),
            f("ram_capacity", "samsung_s24plus_ph_launch_price", "12 GB", 12, key="ramGb", unit="GB"),
            f("storage_capacity", "samsung_s24plus_ph_launch_price", f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("official_launch_price_php", "samsung_s24plus_ph_launch_price", f"Original Philippine SRP: PHP {price:,} for {storage} GB", price, unit="PHP",
              note="Official Samsung Philippines launch SRP; not a current offer."),
            f("current_price_php", "samsung_s24plus_ph_launch_price", f"Historical Philippine launch SRP: PHP {price:,} ({storage} GB)", price, unit="PHP",
              note="Dated launch-price observation from Samsung Philippines; not a current selling offer.",
              price_condition="new", price_type="Historical official Philippine launch SRP (not a current offer)", price_observed="2024-01-18"),
            *s24_shared,
        ]
        out.append(config_review(device, "Galaxy S24+", config_id, label, s24_variants,
                                 [s24_specs, s24_prices, s24_launch, s24_news], fields, model_code="SM-S926B"))

    # Galaxy S26+: local product pages and the specification table confirm
    # 12/256 and 12/512, but current Samsung PH price references disagree.
    # Keep the launch SRPs and surface the conflict rather than publish a
    # potentially stale/current selling price as settled.
    device = "device_f7d2b14d45c9bb"
    s26_specs_url = "https://www.samsung.com/ph/smartphones/galaxy-s26/specs/"
    s26_buy_url = "https://www.samsung.com/ph/smartphones/galaxy-s26/buy/?modelCode=SM-S947BLBBPHL"
    s26_order_url = "https://www.samsung.com/ph/offer/galaxy-s26-series/preorder-in-store/"
    s26_tradein_url = "https://www.samsung.com/ph/trade-in/"
    s26_specs = src(
        "samsung_s26plus_ph_specs", "Samsung Philippines", s26_specs_url,
        "Galaxy S26+ technical specifications and storage choices",
        "Samsung Philippines' spec table lists Galaxy S26+ storage choices, display, Exynos 2600, camera system, battery, charging, connectivity, dimensions, and weight.",
    )
    s26_buy = src(
        "samsung_s26plus_ph_product", "Samsung Philippines", s26_buy_url,
        "Local Galaxy S26+ product family, configurations, and price reference",
        "Samsung Philippines' product page identifies the SM-S947B local model family and 12 GB/256 GB and 12 GB/512 GB options. Its price FAQ currently states PHP 74,990 and PHP 88,990, respectively; other Samsung price references differ.",
    )
    s26_order = src(
        "samsung_s26plus_ph_preorder", "Samsung Philippines", s26_order_url,
        "Local preorder start and original SRPs",
        "Samsung Philippines states that authorized dealers and Samsung Experience Stores accepted Galaxy S26+ preorders from 26 February to 17 March 2026. Its table lists original SRPs of PHP 74,990 (12/256) and PHP 88,990 (12/512), plus a limited pre-order price for the 12/512 configuration.",
        "2026-02-26",
    )
    s26_tradein = src(
        "samsung_s26plus_ph_price_conflict", "Samsung Philippines", s26_tradein_url,
        "Samsung's latest Philippine SRP reference for price cross-checking",
        "The Galaxy S26+ entries on Samsung Philippines' trade-in reference list SRPs of PHP 88,990 (12/256) and PHP 102,990 (12/512); this differs from the Samsung product-page FAQ's PHP 74,990 and PHP 88,990. It is an SRP reference, not a confirmed in-stock retail offer.",
    )
    s26_variants = [
        {"id": f"{device}-auto-12gb-256gb", "label": "12 GB RAM / 256 GB storage", "modelCode": "SM-S947B"},
        {"id": f"{device}-auto-12gb-512gb", "label": "12 GB RAM / 512 GB storage", "modelCode": "SM-S947B"},
    ]
    s26_shared = [
        f("model_number", "samsung_s26plus_ph_product", "SM-S947B Philippine model family; full product order code varies by color and storage.", "SM-S947B",
          note="The model family is derived from Samsung Philippines' exact local SM-S947B…PHL product code; no color-specific code is assigned."),
        f("display_size", "samsung_s26plus_ph_specs", "6.7 inches (full rectangle)", 6.7, key="displayInches", unit="in"),
        f("display_technology", "samsung_s26plus_ph_specs", "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType"),
        f("display_resolution", "samsung_s26plus_ph_specs", "QHD+", "QHD+", key="resolution"),
        f("display_refresh_rate", "samsung_s26plus_ph_specs", "Adaptive 1–120 Hz", 120, key="refreshHz", unit="Hz"),
        f("chipset", "samsung_s26plus_ph_specs", "Exynos 2600", "Exynos 2600", key="chipset",
          note="Samsung says application processor may vary by device and market; this entry reflects the Philippine-market specification table and local newsroom."),
        f("rear_camera_system", "samsung_s26plus_ph_specs", "50 MP wide + 10 MP telephoto + 12 MP ultra-wide rear cameras", 50,
          key="rearCameraMp", unit="MP", note="Catalog's numeric rear-camera field stores the 50 MP main camera; the source value retains the full triple-camera array."),
        f("main_camera_sensor", "samsung_s26plus_ph_specs", "50 MP wide camera, f/1.8, with 2x optical-quality zoom", "50 MP; f/1.8; 2x optical-quality zoom"),
        f("ultrawide_camera", "samsung_s26plus_ph_specs", "12 MP ultra-wide camera, f/2.2", "12 MP; f/2.2"),
        f("telephoto_camera", "samsung_s26plus_ph_specs", "10 MP telephoto with 3x optical zoom, f/2.4", "10 MP; 3x optical zoom; f/2.4"),
        f("front_camera", "samsung_s26plus_ph_specs", "12 MP front camera", 12, key="frontCameraMp", unit="MP"),
        f("battery_capacity", "samsung_s26plus_ph_specs", "4,900 mAh typical; 4,755 mAh rated minimum", 4900, key="batteryMah", unit="mAh",
          note="Samsung separately states the rated minimum; catalog value uses typical capacity."),
        f("wired_charging", "samsung_s26plus_ph_specs", "Samsung recommends a 45 W adapter; adapter sold separately", 45, key="chargingW", unit="W"),
        f("dimensions", "samsung_s26plus_ph_specs", "158.4 x 75.8 x 7.3 mm (H x W x D)", "158.4 x 75.8 x 7.3 mm", key="dimensions", unit="mm"),
        f("weight", "samsung_s26plus_ph_specs", "190 g (weight may vary by country or region)", 190, key="weightG", unit="g"),
        f("operating_system", "samsung_s26plus_ph_specs", "Android 16 with One UI 8.5", "Android 16 / One UI 8.5", key="os"),
        f("wifi", "samsung_s26plus_ph_specs", "Wi-Fi 7", "Wi-Fi 7", key="wifi"),
        f("bluetooth", "samsung_s26plus_ph_specs", "Bluetooth 6.0", "Bluetooth 6.0"),
        f("ingress_protection", "samsung_s26plus_ph_specs", "IP68", "IP68"),
    ]
    for index, (config_id, label, storage, launch_price, current_ref) in enumerate([
        (s26_variants[0]["id"], s26_variants[0]["label"], 256, 74990, 88990),
        (s26_variants[1]["id"], s26_variants[1]["label"], 512, 88990, 102990),
    ]):
        fields = [
            f("configuration", "samsung_s26plus_ph_specs", f"12 GB RAM / {storage} GB storage", f"12 GB RAM / {storage} GB storage"),
            f("ram_capacity", "samsung_s26plus_ph_specs", "12 GB", 12, key="ramGb", unit="GB"),
            f("storage_capacity", "samsung_s26plus_ph_specs", f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "samsung_s26plus_ph_preorder", "Philippine authorized-channel preorders opened 26 February 2026.", "2026-02-26",
              note="This is the documented preorder start, not a claim about first retail shipment."),
            f("official_launch_price_php", "samsung_s26plus_ph_preorder", f"Original Philippine SRP: PHP {launch_price:,} for {storage} GB", launch_price, unit="PHP",
              note="Samsung Philippines' dated preorder table labels this the SRP. The separate limited-time preorder price is not treated as the device's launch SRP."),
            f("current_price_php", "samsung_s26plus_ph_price_conflict",
              f"Samsung PH trade-in reference SRP PHP {current_ref:,}; product-page FAQ states PHP {launch_price:,}.", None,
              status="CONFLICTING_INFORMATION",
              note="Current price is withheld because two current Samsung Philippines references disagree. The trade-in page lists a higher SRP, while the product page FAQ lists the lower price; neither value is treated as a confirmed in-stock purchase offer."),
            *s26_shared,
        ]
        out.append(config_review(device, "Galaxy S26+", config_id, label, s26_variants,
                                 [s26_specs, s26_buy, s26_order, s26_tradein], fields, model_code="SM-S947B"))
    return out


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = records()
    for item in items:
        add_review(manual, catalog, item)
    # The catalog builder applies a replacement variant list once per model.
    # Keep it on the first field-review record; each add_review call still
    # needed the list to recognize its configuration against the placeholder.
    first_review_for_device = set()
    for item in items:
        review = next(r for r in manual["records"] if
                      (r["deviceId"], r["configurationId"]) ==
                      (item["deviceId"], item["configurationId"]))
        if item["deviceId"] in first_review_for_device:
            review.pop("replacementVariants", None)
        else:
            first_review_for_device.add(item["deviceId"])
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewedConfigurations": len(items), "models": 3, "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
