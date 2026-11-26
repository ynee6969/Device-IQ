#!/usr/bin/env python3
"""Upgrade Galaxy S24 and S24 Ultra inventory evidence to Samsung PH sources."""
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


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid: str, sid: str, value, normalized=None, *, key: str | None = None,
      unit: str | None = None, status: str = "VERIFIED", note: str | None = None,
      price_condition: str | None = None, price_type: str | None = None,
      price_observed: str | None = None) -> dict:
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
    return row


def records():
    out = []
    preorder_url = "https://www.samsung.com/ph/offer/offline/2024/galaxy-s24-preorder/"
    s24_news_url = "https://news.samsung.com/ph/enter-the-new-era-of-mobile-ai-with-samsung-galaxy-s24-series"
    s24_spec_url = "https://www.samsung.com/ph/smartphones/galaxy-s24/specs/"
    s24_buy_url = "https://www.samsung.com/ph/smartphones/galaxy-s24/buy/"
    ultra_spec_url = "https://www.samsung.com/ph/smartphones/galaxy-s24-ultra/specs/"
    ultra_buy_url = "https://www.samsung.com/ph/smartphones/galaxy-s24-ultra/buy/"

    launch_source = src(
        "galaxy_s24_ph_preorder_srp", "Samsung Philippines", preorder_url,
        "Philippine preorder window, original SRP, and authorized sale timing",
        "Samsung Philippines lists the preorder campaign starting 18 January 2024, with the original SRP by storage configuration. The dates and prices are retained as historical launch observations, not current offers.",
        "2024-01-18")
    buy_source = src(
        "galaxy_s24_ph_product_config", "Samsung Philippines", s24_buy_url,
        "Philippine product configurations and model-family codes",
        "Samsung Philippines product tooling identifies the 8 GB / 256 GB and 8 GB / 512 GB configurations; full order codes vary by color and configuration.")
    s24_specs_source = src(
        "galaxy_s24_ph_specs", "Samsung Philippines", s24_spec_url,
        "Official Philippine hardware specifications",
        "Samsung Philippines lists local display, camera, processor, protection, battery, dimensions, weight, and color details for Galaxy S24.")
    s24_news_source = src(
        "galaxy_s24_ph_newsroom_specs", "Samsung Newsroom Philippines", s24_news_url,
        "Dated official launch, operating system, and connectivity specifications",
        "Samsung Newsroom's 18 January 2024 announcement includes model-specific hardware tables and the local campaign schedule.",
        "2024-01-18")

    s24_device = "device_f1fa8c58ea3104"
    s24_configs = [
        (s24_device + "-auto-8gb-256gb", "8 GB RAM / 256 GB storage", 256, 53990),
        (s24_device + "-auto-8gb-512gb", "8 GB RAM / 512 GB storage", 512, 61990),
    ]
    for config, label, storage, price in s24_configs:
        fields = [
            f("model_number", "galaxy_s24_ph_product_config", "SM-S921B Philippine model family; full PHL order code varies by color and storage.", "SM-S921B",
              note="The cited Samsung Philippines SKU pages show SM-S921B…PHL codes; this is the shared model family, not a color-specific order code."),
            f("configuration", "galaxy_s24_ph_product_config", f"8 GB RAM / {storage} GB storage", f"8 GB RAM / {storage} GB storage"),
            f("ram_capacity", "galaxy_s24_ph_product_config", "8 GB", 8, key="ramGb", unit="GB"),
            f("storage_capacity", "galaxy_s24_ph_product_config", f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "galaxy_s24_ph_preorder_srp", "Samsung Philippines preorder sales began 18 January 2024.", "2024-01-18",
              note="This is the documented start of authorized preorder sales, not the date devices first shipped to every customer."),
            f("official_launch_price_php", "galaxy_s24_ph_preorder_srp", f"Original Philippine SRP: PHP {price:,} for {storage} GB", price, unit="PHP",
              note="Official Samsung Philippines original SRP from the January 2024 preorder table; its preorder discount is not used as the launch SRP."),
            f("current_price_php", "galaxy_s24_ph_preorder_srp", f"Historical dated Philippine price observation: PHP {price:,} ({storage} GB)", price, unit="PHP",
              note="Historical manufacturer SRP snapshot dated 18 January 2024; not a current selling offer.", price_condition="new",
              price_type="Official Philippine launch SRP; historical dated snapshot, not a current offer", price_observed="2024-01-18"),
            f("display_size", "galaxy_s24_ph_specs", "6.2 inches", 6.2, key="displayInches", unit="in"),
            f("display_technology", "galaxy_s24_ph_specs", "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType"),
            f("display_resolution", "galaxy_s24_ph_specs", "2340 x 1080 (FHD+)", "2340 x 1080", key="resolution"),
            f("display_refresh_rate", "galaxy_s24_ph_specs", "120 Hz", 120, key="refreshHz", unit="Hz"),
            f("display_brightness", "galaxy_s24_ph_specs", "Up to 2,600 nits peak brightness", "Up to 2,600 nits peak", unit="nits"),
            f("display_protection", "galaxy_s24_ph_specs", "Corning Gorilla Glass Victus 2", "Corning Gorilla Glass Victus 2"),
            f("chipset", "galaxy_s24_ph_specs", "Exynos 2400", "Exynos 2400", key="chipset"),
            f("cpu", "galaxy_s24_ph_specs", "Samsung's cited Philippine specification does not list CPU core layout or clock rates.", None,
              status="NOT_DISCLOSED", note="The chipset is documented; core arrangement and clocks are not disclosed by the cited local specification."),
            f("gpu", "galaxy_s24_ph_specs", "Samsung's cited Philippine specification does not name the GPU.", None,
              status="NOT_DISCLOSED", note="No GPU is inferred from the chipset."),
            f("operating_system", "galaxy_s24_ph_newsroom_specs", "Android 14 with One UI 6.1", "Android 14 / One UI 6.1", key="os"),
            f("rear_camera_system", "galaxy_s24_ph_specs", "50 MP main (OIS) + 10 MP 3x telephoto + 12 MP ultra-wide rear cameras", "50 MP main + 10 MP telephoto + 12 MP ultra-wide"),
            f("ultrawide_camera", "galaxy_s24_ph_specs", "12 MP ultra-wide, f/2.2", "12 MP, f/2.2"),
            f("telephoto_camera", "galaxy_s24_ph_specs", "10 MP telephoto with 3x optical zoom, f/2.4", "10 MP, 3x optical zoom, f/2.4"),
            f("front_camera", "galaxy_s24_ph_specs", "12 MP", 12, key="frontCameraMp", unit="MP"),
            f("battery_capacity", "galaxy_s24_ph_newsroom_specs", "4,000 mAh typical; 3,880 mAh rated minimum", 4000, key="batteryMah", unit="mAh",
              note="Catalog value uses Samsung's typical capacity; Samsung separately states the rated minimum."),
            f("wired_charging", "galaxy_s24_ph_newsroom_specs", "25 W wired charging; adapter sold separately", 25, key="chargingW", unit="W"),
            f("wireless_charging", "galaxy_s24_ph_newsroom_specs", "Fast Wireless Charging 2.0; Wireless PowerShare", "Fast Wireless Charging 2.0; Wireless PowerShare"),
            f("dimensions", "galaxy_s24_ph_specs", "147.0 x 70.6 x 7.6 mm (H x W x D)", "147.0 x 70.6 x 7.6 mm", key="dimensions", unit="mm"),
            f("weight", "galaxy_s24_ph_specs", "167 g", 167, key="weightG", unit="g"),
            f("ingress_protection", "galaxy_s24_ph_specs", "IP68 water resistance", "IP68"),
            f("wifi", "galaxy_s24_ph_newsroom_specs", "Wi-Fi 6E", "Wi-Fi 6E", key="wifi"),
            f("bluetooth", "galaxy_s24_ph_newsroom_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
        ]
        out.append({"deviceId": s24_device, "configurationId": config, "brand": "Samsung",
                    "model": "Galaxy S24", "configuration": label, "sources":
                    [launch_source, buy_source, s24_specs_source, s24_news_source], "fields": fields})

    ultra_source = src(
        "galaxy_s24_ultra_ph_specs", "Samsung Philippines", ultra_spec_url,
        "Official Philippine hardware specifications",
        "Samsung's Philippine Galaxy S24 Ultra specification page lists model-specific camera, display, chipset, battery, charging, connectivity, and durability specifications.")
    ultra_buy_source = src(
        "galaxy_s24_ultra_ph_config", "Samsung Philippines", ultra_buy_url,
        "Philippine product configurations and model-family codes",
        "Samsung Philippines product tooling lists local 12 GB / 256 GB and 12 GB / 512 GB configurations; full order codes vary by color and storage.")
    ultra_resolution_source = src(
        "galaxy_s24_ultra_samsung_resolution", "Samsung Gulf Support",
        "https://www.samsung.com/ae/support/mobile-devices/what-are-the-sizes-and-the-resolution-of-the-new-s24-series/",
        "Official manufacturer display-resolution reference",
        "Samsung's official regional support article gives the Galaxy S24 Ultra display resolution as 3120 x 1440 (QHD+). This is a model-level display specification; the local configuration list remains from Samsung Philippines.",
        "2026-06-30")
    ultra_device = "device_32624044543da4"
    ultra_configs = [
        (ultra_device + "-auto-12gb-256gb", "12 GB RAM / 256 GB storage", 256, 84990),
        (ultra_device + "-auto-12gb-512gb", "12 GB RAM / 512 GB storage", 512, 92990),
    ]
    for config, label, storage, price in ultra_configs:
        fields = [
            f("model_number", "galaxy_s24_ultra_ph_config", "SM-S928B Philippine model family; full PHL order code varies by color and storage.", "SM-S928B",
              note="Samsung Philippines' local product codes use the SM-S928B family; this is not a color-specific retail order code."),
            f("configuration", "galaxy_s24_ultra_ph_config", f"12 GB RAM / {storage} GB storage", f"12 GB RAM / {storage} GB storage"),
            f("ram_capacity", "galaxy_s24_ultra_ph_config", "12 GB", 12, key="ramGb", unit="GB"),
            f("storage_capacity", "galaxy_s24_ultra_ph_config", f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("philippine_release_date", "galaxy_s24_ph_preorder_srp", "Samsung Philippines preorder sales began 18 January 2024.", "2024-01-18",
              note="This is the documented start of authorized preorder sales, not the date devices first shipped to every customer."),
            f("official_launch_price_php", "galaxy_s24_ph_preorder_srp", f"Original Philippine SRP: PHP {price:,} for {storage} GB", price, unit="PHP",
              note="Official Samsung Philippines original SRP from the January 2024 preorder table; the model's 1 TB listing is outside this workbook configuration."),
            f("current_price_php", "galaxy_s24_ph_preorder_srp", f"Historical dated Philippine price observation: PHP {price:,} ({storage} GB)", price, unit="PHP",
              note="Historical manufacturer SRP snapshot dated 18 January 2024; not a current selling offer.", price_condition="new",
              price_type="Official Philippine launch SRP; historical dated snapshot, not a current offer", price_observed="2024-01-18"),
            f("display_size", "galaxy_s24_ultra_ph_specs", "6.8 inches", 6.8, key="displayInches", unit="in"),
            f("display_technology", "galaxy_s24_ultra_ph_specs", "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType"),
            f("display_resolution", "galaxy_s24_ultra_samsung_resolution", "3120 x 1440 (QHD+)", "3120 x 1440", key="resolution"),
            f("display_refresh_rate", "galaxy_s24_ultra_ph_specs", "Adaptive 1–120 Hz", 120, key="refreshHz", unit="Hz"),
            f("display_brightness", "galaxy_s24_ultra_ph_specs", "Up to 2,600 nits peak brightness", "Up to 2,600 nits peak", unit="nits"),
            f("display_protection", "galaxy_s24_ultra_ph_specs", "Corning Gorilla Armor", "Corning Gorilla Armor"),
            f("chipset", "galaxy_s24_ultra_ph_specs", "Snapdragon 8 Gen 3 Mobile Platform for Galaxy", "Snapdragon 8 Gen 3 for Galaxy", key="chipset"),
            f("cpu", "galaxy_s24_ultra_ph_specs", "CPU speed up to 3.39 GHz; core layout not stated on cited specification page", "Up to 3.39 GHz; core layout not stated"),
            f("gpu", "galaxy_s24_ultra_ph_specs", "Samsung's cited Philippine specification does not name the GPU.", None,
              status="NOT_DISCLOSED", note="No GPU is inferred from the chipset."),
            f("operating_system", "galaxy_s24_ph_newsroom_specs", "Android 14 with One UI 6.1", "Android 14 / One UI 6.1", key="os"),
            f("rear_camera_system", "galaxy_s24_ultra_ph_specs", "200 MP wide + 50 MP 5x telephoto + 10 MP 3x telephoto + 12 MP ultra-wide rear cameras", "200 MP main + 50 MP 5x telephoto + 10 MP 3x telephoto + 12 MP ultra-wide"),
            f("ultrawide_camera", "galaxy_s24_ultra_ph_specs", "12 MP ultra-wide, f/2.2", "12 MP, f/2.2"),
            f("telephoto_camera", "galaxy_s24_ultra_ph_specs", "50 MP 5x optical telephoto and 10 MP 3x optical telephoto", "50 MP 5x + 10 MP 3x optical telephoto"),
            f("front_camera", "galaxy_s24_ultra_ph_specs", "12 MP", 12, key="frontCameraMp", unit="MP"),
            f("video_recording", "galaxy_s24_ultra_ph_specs", "Rear UHD 8K (7680 x 4320) at 30 fps; slow motion 240 fps FHD and 120 fps UHD", "Rear up to 8K/30 fps; slow motion 240 fps FHD / 120 fps UHD"),
            f("battery_capacity", "galaxy_s24_ph_newsroom_specs", "5,000 mAh typical; 4,855 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
              note="Catalog value uses Samsung's typical capacity; Samsung separately states the rated minimum."),
            f("wired_charging", "galaxy_s24_ph_newsroom_specs", "45 W wired charging; adapter sold separately", 45, key="chargingW", unit="W"),
            f("wireless_charging", "galaxy_s24_ph_newsroom_specs", "Fast Wireless Charging 2.0; Wireless PowerShare", "Fast Wireless Charging 2.0; Wireless PowerShare"),
            f("dimensions", "galaxy_s24_ultra_ph_specs", "162.3 x 79.0 x 8.6 mm (H x W x D)", "162.3 x 79.0 x 8.6 mm", key="dimensions", unit="mm"),
            f("weight", "galaxy_s24_ultra_ph_specs", "232 g (Sub6); 233 g (mmWave)", "232 g (Sub6) / 233 g (mmWave)",
              note="Samsung notes the weight varies by market; no single local-radio variant is assigned."),
            f("ingress_protection", "galaxy_s24_ultra_ph_specs", "IP68 water and dust resistance", "IP68"),
            f("wifi", "galaxy_s24_ph_newsroom_specs", "Wi-Fi 7", "Wi-Fi 7", key="wifi"),
            f("bluetooth", "galaxy_s24_ph_newsroom_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
        ]
        out.append({"deviceId": ultra_device, "configurationId": config, "brand": "Samsung",
                    "model": "Galaxy S24 Ultra", "configuration": label, "sources":
                    [launch_source, ultra_buy_source, ultra_source, ultra_resolution_source, s24_news_source], "fields": fields})
    return out


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = records()
    for item in items:
        add_review(manual, catalog, item)
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewedConfigurations": len(items), "models": 2,
                      "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
