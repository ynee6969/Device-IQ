#!/usr/bin/env python3
"""Review additional ASUS ROG phone records against official PH pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_asus_rog_reviews import f, make, src  # noqa: E402
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"


def records():
    out = []

    # The PH spec comparison identifies 12/256 and 16/512, but the PH product
    # page only prices/lists 8/256 and 16/512. Thus 12/256 specs are reviewed,
    # while its local sale and price remain pending.
    device = "device_67c3c6cf323fd4"
    product_url = "https://rog.asus.com/ph/phones/rog-phone-6-model/"
    spec_url = "https://rog.asus.com/ph/phones/rog-phone-6-model/spec/?config=90AI00B2-M001A0"
    product_id, spec_id = "rog_phone_6_ph_product", "rog_phone_6_ph_specs"
    sources = [
        src(product_id, "ROG Philippines", product_url,
            "Philippine product configurations, listings and page-listed prices",
            "The product page lists ROG Phone 6 in 8 GB/256 GB at PHP 47,995 and 16 GB/512 GB at PHP 54,995. It does not list the workbook's 12 GB/256 GB variant."),
        src(spec_id, "ROG Philippines", spec_url,
            "Official Philippine technical configurations and specifications",
            "The technical comparison lists 12 GB/256 GB and 16 GB/512 GB configurations, and model-wide processor, camera, connectivity, battery and charging details. Technical inclusion of 12/256 does not by itself establish a Philippine retail offer."),
    ]
    common = [
        f("chipset", spec_id, "Qualcomm Snapdragon 8+ Gen 1 Mobile Platform", "Snapdragon 8+ Gen 1", key="chipset"),
        f("gpu", spec_id, "Qualcomm Adreno 730", "Adreno 730", key="gpu"),
        f("rear_camera_system", spec_id, "50 MP Sony IMX766 main + 13 MP ultrawide + 5 MP macro", "50 MP main + 13 MP ultrawide + 5 MP macro"),
        f("display_size", product_id, "6.78 inches", 6.78, key="displayInches", unit="in"),
        f("display_refresh_rate", product_id, "Up to 165 Hz", 165, key="refreshHz", unit="Hz"),
        f("battery_capacity", spec_id, "6000 mAh typical", 6000, key="batteryMah", unit="mAh"),
        f("wired_charging", spec_id, "Up to 65 W QC 5.0 / USB PD 3.0", 65, key="chargingW", unit="W"),
        f("wifi", spec_id, "Wi-Fi 6E; feature availability is subject to regional regulation", "Wi-Fi 6E", key="wifi"),
        f("bluetooth", spec_id, "Bluetooth 5.2", "Bluetooth 5.2"),
        f("nfc", spec_id, "NFC supported", "Yes"),
        f("sim_esim", spec_id, "Dual nano-SIM, dual standby", "Dual nano-SIM; eSIM not listed", key="sim"),
    ]
    configs = [
        (device + "-auto-12gb-256gb", "12 GB RAM / 256 GB storage", 12, 256, False),
        (device + "-auto-16gb-512gb", "16 GB RAM / 512 GB storage", 16, 512, True),
    ]
    for config, label, ram, storage, sold_page in configs:
        fields = [
            f("configuration", spec_id, label, label,
              note=("ROG Philippines' technical comparison lists this configuration; its product listing does not independently confirm a 12 GB/256 GB retail offer."
                    if not sold_page else "Exact 16 GB/512 GB configuration is listed on the official Philippine product page.")),
            f("ram_capacity", spec_id, f"{ram} GB LPDDR5", ram, key="ramGb", unit="GB"),
            f("ram_type", spec_id, "LPDDR5", "LPDDR5", key="ramType"),
            f("storage_capacity", spec_id, f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("storage_type", spec_id, "UFS 3.1", "UFS 3.1", key="storageType"),
            *common,
            f("philippine_release_date", product_id,
              "The official product page confirms local product listing but does not state first-sale date.", None,
              status="PENDING_VERIFICATION", note="Philippine first authorized-sale date remains unknown."),
        ]
        if sold_page:
            fields.extend([
                f("model_number", product_id, "S8475 (listed with the 16 GB/512 GB local model)", "S8475"),
                f("current_price_php", product_id,
                  "PHP 54,995 listed for 16 GB/512 GB on the ASUS ROG Philippines product page; observed 2026-11-26. Stock status is not stated.",
                  54995, unit="PHP", price_condition="new",
                  price_type="Official PH page-listed price; observed 2026-11-26, stock unconfirmed",
                  price_observed=OBSERVED,
                  note="The page's amount is recorded as a dated observation, not a stock-confirmed current offer.",
                  replace_existing=True),
            ])
        out.append(make(device, config, "ROG Phone 6", label, sources, fields,
                        availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                      "availabilityStatus": "Official Philippine product listing; configuration-specific limits apply",
                                      "philippineAvailability": "ROG Philippines lists ROG Phone 6 in 8 GB/256 GB and 16 GB/512 GB at dated page-observed prices. The workbook's 12 GB/256 GB configuration appears on the PH technical page but not the product listing; its local retail availability and price remain unverified.",
                                      "observedAt": OBSERVED,
                                      "qualityFlag": "Model listing verified; workbook 12 GB/256 GB retail availability remains unverified"} if sold_page else None,
                        model_code="S8475" if sold_page else None))

    # Both workbook variants are explicit Philippine product-page listings.
    device = "device_3f9fd3e4da0935"
    product_url = "https://rog.asus.com/ph/phones/rog-phone-7/"
    spec_url = "https://rog.asus.com/ph/phones/rog-phone-7/spec/"
    product_id, spec_id = "rog_phone_7_ph_product", "rog_phone_7_ph_specs"
    sources = [
        src(product_id, "ROG Philippines", product_url,
            "Official Philippine product configurations and dated page-listed prices",
            "The product page lists 12 GB/256 GB at PHP 50,995 and 16 GB/512 GB at PHP 54,995 in the Storm White and Phantom Black colors. Stock and listing-price validity period are not stated."),
        src(spec_id, "ROG Philippines", spec_url,
            "Official Philippine technical specifications",
            "The local tech-spec comparison identifies Android 13, Snapdragon 8 Gen 2, display, cameras, dimensions, connectivity, 6000 mAh battery and 65 W charging."),
    ]
    common = [
        f("operating_system", spec_id, "Android 13", "Android 13", key="os"),
        f("chipset", spec_id, "Qualcomm Snapdragon 8 Gen 2", "Snapdragon 8 Gen 2", key="chipset"),
        f("cpu", spec_id, "Octa-core CPU up to 3.2 GHz", "Octa-core up to 3.2 GHz"),
        f("gpu", spec_id, "Qualcomm Adreno 740", "Adreno 740", key="gpu"),
        f("display_size", spec_id, "6.78 inches", 6.78, key="displayInches", unit="in"),
        f("display_technology", spec_id, "Samsung AMOLED", "AMOLED", key="displayType"),
        f("display_resolution", spec_id, "2448 x 1080", "2448 x 1080", key="resolution"),
        f("display_refresh_rate", spec_id, "165 Hz", 165, key="refreshHz", unit="Hz"),
        f("display_protection", spec_id, "Corning Gorilla Glass Victus", "Corning Gorilla Glass Victus"),
        f("rear_camera_system", spec_id, "50 MP Sony IMX766 main + 13 MP ultrawide + 5 MP macro", "50 MP main + 13 MP ultrawide + 5 MP macro"),
        f("front_camera", product_id, "32 MP", 32, key="frontCameraMp", unit="MP"),
        f("battery_capacity", product_id, "6000 mAh typical", 6000, key="batteryMah", unit="mAh"),
        f("wired_charging", product_id, "65 W HyperCharge USB PD", 65, key="chargingW", unit="W"),
        f("ingress_protection", product_id, "IP54", "IP54"),
        f("weight", spec_id, "239 g", 239, key="weightG", unit="g"),
        f("wifi", product_id, "Wi-Fi 7 ready", "Wi-Fi 7 capable", key="wifi"),
    ]
    configs = [
        (device + "-auto-12gb-256gb", "12 GB RAM / 256 GB storage", 12, 256, 50995),
        (device + "-auto-16gb-512gb", "16 GB RAM / 512 GB storage", 16, 512, 54995),
    ]
    for config, label, ram, storage, price in configs:
        fields = [
            f("configuration", product_id, label, label),
            f("ram_capacity", product_id, f"{ram} GB LPDDR5X", ram, key="ramGb", unit="GB"),
            f("ram_type", product_id, "LPDDR5X", "LPDDR5X", key="ramType"),
            f("storage_capacity", product_id, f"{storage} GB", storage, key="storageGb", unit="GB"),
            f("storage_type", spec_id, "UFS 4.0", "UFS 4.0", key="storageType"),
            *common,
            f("current_price_php", product_id,
              f"PHP {price:,} listed for {ram} GB/{storage} GB on the ASUS ROG Philippines product page; observed 2026-11-26. Stock status is not stated.",
              price, unit="PHP", price_condition="new",
              price_type="Official PH page-listed price; observed 2026-11-26, stock unconfirmed",
              price_observed=OBSERVED,
              note="Dated product-page price observation; page does not confirm current stock.",
              replace_existing=True),
            f("philippine_release_date", product_id,
              "The official product page confirms local product listings but does not state first-sale date.", None,
              status="PENDING_VERIFICATION", note="Philippine first authorized-sale date remains unknown."),
        ]
        out.append(make(device, config, "ROG Phone 7", label, sources, fields,
                        availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                      "availabilityStatus": "Official Philippine product listing",
                                      "philippineAvailability": "ROG Philippines lists both 12 GB/256 GB and 16 GB/512 GB configurations in local colors. Current stock and first-sale date are not stated.",
                                      "observedAt": OBSERVED,
                                      "qualityFlag": "Philippine listing verified; current stock and first-sale date not recorded"}))

    # This FE model has an exact PH product SKU/configuration and a dated
    # page-observed promotional price; the sale and first-sale dates are not
    # treated as historical release dates.
    device = "device_59b130760709ea"
    config = device + "-auto-12gb-256gb"
    product_url = "https://rog.asus.com/ph/phones/rog-phone-9-fe/"
    spec_url = "https://rog.asus.com/ph/phones/rog-phone-9-fe/spec/"
    product_id, spec_id = "rog_phone_9_fe_ph_product", "rog_phone_9_fe_ph_specs"
    sources = [
        src(product_id, "ROG Philippines", product_url,
            "Official Philippine SKU, configuration, and page-listed promotional/regular price",
            "The Philippine product page lists SKU AI2401_N-7B109WW in 12 GB/256 GB at a special PHP 39,995, with PHP 44,995 shown as the regular price. Stock and promotion validity dates are not stated."),
        src(spec_id, "ROG Philippines", spec_url,
            "Official Philippine ROG Phone 9 FE technical specifications",
            "The local specifications page identifies the 12 GB/256 GB configuration and publishes the processor, display, camera, battery, charging and build values."),
    ]
    fields = [
        f("model_number", product_id, "AI2401_N-7B109WW", "AI2401_N-7B109WW"),
        f("configuration", product_id, "12 GB RAM / 256 GB storage · Phantom Black", "12 GB RAM / 256 GB storage"),
        f("ram_capacity", product_id, "12 GB", 12, key="ramGb", unit="GB"),
        f("ram_type", spec_id, "LPDDR5X", "LPDDR5X", key="ramType"),
        f("storage_capacity", product_id, "256 GB", 256, key="storageGb", unit="GB"),
        f("storage_type", spec_id, "UFS 4.0", "UFS 4.0", key="storageType"),
        f("chipset", spec_id, "Qualcomm Snapdragon 8 Gen 3", "Snapdragon 8 Gen 3", key="chipset"),
        f("cpu", spec_id, "Octa-core CPU up to 3.3 GHz", "Octa-core up to 3.3 GHz"),
        f("gpu", spec_id, "Qualcomm Adreno 750", "Adreno 750", key="gpu"),
        f("operating_system", spec_id, "Android 15 with ROG UI", "Android 15 with ROG UI", key="os"),
        f("display_size", spec_id, "6.78 inches", 6.78, key="displayInches", unit="in"),
        f("display_technology", spec_id, "Samsung Flexible AMOLED", "Flexible AMOLED", key="displayType"),
        f("display_resolution", spec_id, "2400 x 1080 FHD+", "2400 x 1080", key="resolution"),
        f("display_refresh_rate", product_id, "Up to 185 Hz", 185, key="refreshHz", unit="Hz",
          note="Manufacturer lists 185 Hz via Game Genie as the maximum mode."),
        f("display_brightness", product_id, "1600 nits HBM / 2500 nits peak", "1600 nits HBM / 2500 nits peak", unit="nits"),
        f("display_protection", spec_id, "Corning Gorilla Glass Victus 2", "Corning Gorilla Glass Victus 2"),
        f("rear_camera_system", product_id, "50 MP main + 13 MP ultrawide + 5 MP macro", "50 MP main + 13 MP ultrawide + 5 MP macro"),
        f("front_camera", product_id, "32 MP", 32, key="frontCameraMp", unit="MP"),
        f("battery_capacity", product_id, "5500 mAh typical", 5500, key="batteryMah", unit="mAh"),
        f("wired_charging", product_id, "65 W HyperCharge USB PD", 65, key="chargingW", unit="W"),
        f("wireless_charging", product_id, "15 W wireless charging", "15 W wireless charging"),
        f("dimensions", spec_id, "163.8 x 76.8 x 8.9 mm", "163.8 x 76.8 x 8.9 mm", key="dimensions", unit="mm"),
        f("weight", spec_id, "225 g", 225, key="weightG", unit="g"),
        f("ingress_protection", spec_id, "IP68", "IP68"),
        f("current_price_php", product_id,
          "Special price PHP 39,995 (regular price PHP 44,995 shown on page); observed 2026-11-26. Stock status and promotion dates are not stated.",
          39995, unit="PHP", price_condition="new",
          price_type="Official PH special page-listed price; observed 2026-11-26, stock unconfirmed",
          price_observed=OBSERVED,
          note="Dated observation of the displayed special price. The page does not state its validity dates or confirm stock.",
          replace_existing=True),
        f("philippine_release_date", product_id,
          "Official Philippine product page confirms local SKU listing but does not state first-sale date.", None,
          status="PENDING_VERIFICATION", note="Philippine first authorized-sale date remains unknown."),
    ]
    out.append(make(device, config, "ROG Phone 9 FE", "12 GB RAM / 256 GB storage · Phantom Black",
                    sources, fields,
                    availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                  "availabilityStatus": "Official Philippine SKU and product listing",
                                  "philippineAvailability": "ROG Philippines lists SKU AI2401_N-7B109WW in 12 GB/256 GB. The page shows a promotional price but does not state stock or promotion validity dates.",
                                  "observedAt": OBSERVED,
                                  "qualityFlag": "Philippine SKU verified; current stock and first-sale date not recorded"},
                    model_code="AI2401_N"))
    return out


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = records()
    keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, keys)
    for item in items:
        add_review(manual, catalog, item)
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"modelsReviewed": 3, "configurationReviews": len(items),
                      "fieldReviews": sum(len(item["fields"]) for item in items)}))


if __name__ == "__main__":
    main()
