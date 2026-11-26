#!/usr/bin/env python3
"""Record official ASUS ROG source reviews for three exact phone models."""
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


def make(device, config, model, label, sources, fields, *, replacements=None,
         availability=None, model_code=None):
    item = {"deviceId": device, "configurationId": config, "brand": "ASUS",
            "model": model, "configuration": label, "sources": sources, "fields": fields}
    if replacements:
        item["replacementVariants"] = replacements
    if availability:
        item["availabilityEvidence"] = availability
    if model_code:
        item["modelCode"] = model_code
    return item


def records():
    out = []

    # Exact model technical evidence only. This source is ASUS India, so it does
    # not establish Philippine availability or which local RAM/storage variant
    # is represented by the workbook's unspecified configuration.
    device = "device_603fa1d223e7e0"
    specs_url = "https://rog.asus.com/in/phones/rog-phone-5-model/spec/"
    source_id = "rog_phone_5_asus_india_model_specs"
    local_article_id = "rog_phone_5_ph_model_article"
    local_article_url = "https://rog.asus.com/ph/articles/smartphones/the-rog-phone-5-levels-up-the-mobile-gaming-experience/"
    sources = [src(source_id, "ROG India", specs_url,
                   "Manufacturer technical specifications for the exact ROG Phone 5 model",
                   "The India technical comparison lists multiple memory/storage and physical variants. Only model-level values are used where they match the exact base phone; this page alone does not verify Philippine availability or the workbook's local configuration."),
               src(local_article_id, "ROG Philippines", local_article_url,
                   "Dated Philippine-region launch article with base-model configuration and display/charging specifications",
                   "ROG Philippines identifies ROG Phone 5 separately from Phone 5 Pro and Ultimate, dates this article 13 March 2021, and states 144 Hz, 65 W charging, and several base-model memory/storage options.",
                   "2021-03-13")]
    fields = [
        f("operating_system", source_id, "Android 11 with ROG UI", "Android 11 with ROG UI", key="os"),
        f("chipset", source_id, "Qualcomm Snapdragon 888 5G Mobile Platform", "Snapdragon 888", key="chipset"),
        f("cpu", source_id, "64-bit octa-core processor up to 2.84 GHz", "Octa-core up to 2.84 GHz"),
        f("gpu", source_id, "Qualcomm Adreno 660", "Adreno 660", key="gpu"),
        f("display_size", source_id, "6.78 inches", 6.78, key="displayInches", unit="in"),
        f("display_technology", source_id, "AMOLED", "AMOLED", key="displayType"),
        f("display_resolution", source_id, "2448 x 1080", "2448 x 1080", key="resolution"),
        f("display_refresh_rate", local_article_id, "144 Hz", 144, key="refreshHz", unit="Hz",
          note="ROG Philippines' dated article identifies the base ROG Phone 5 at 144 Hz. The India comparison page currently mixes 165 Hz and multiple sibling configurations, so its 165 Hz value is not applied to this exact model."),
        f("display_protection", source_id, "Corning Gorilla Glass Victus", "Corning Gorilla Glass Victus"),
        f("rear_camera_system", source_id, "64 MP main + 13 MP ultrawide + 5 MP macro", "64 MP main + 13 MP ultrawide + 5 MP macro"),
        f("front_camera", source_id, "24 MP", 24, key="frontCameraMp", unit="MP"),
        f("video_recording", source_id, "Main rear camera: up to 8K/30 fps and 4K/30 or 60 fps; second rear camera: 4K/30 fps", "Rear main up to 8K/30 and 4K/30 or 60 fps; ultrawide up to 4K/30 fps"),
        f("battery_capacity", source_id, "6000 mAh typical", 6000, key="batteryMah", unit="mAh"),
        f("wired_charging", local_article_id, "65 W HyperCharge", 65, key="chargingW", unit="W",
          note="ROG Philippines' dated base-model article reports 65 W. A regional technical comparison page shows a different adapter in its multi-configuration table; that value is not applied here."),
        f("configuration", local_article_id, "ROG Phone 5 base-model options listed by the manufacturer: 8 GB/128 GB, 12 GB/256 GB, and 16 GB/256 GB; workbook configuration is unspecified.", None,
          status="PENDING_VERIFICATION", note="The article is a Philippine-region source but does not identify which option belongs to this inventory record; no single variant is assigned.", replace_existing=True),
        f("philippine_release_date", local_article_id, "The dated Philippine-region article introduces the model but does not document a first authorized Philippine sale date.", None,
          status="PENDING_VERIFICATION", note="Do not treat the article date as a local sale date; Philippine availability and first-sale timing remain unverified.", replace_existing=True),
    ]
    out.append(make(device, device + "-unrecorded", "ROG Phone 5", "Configuration not recorded",
                    sources, fields))

    # Official Philippine product and specification pages establish the local
    # 18/512 Storm White configuration. Their product listing does not state a
    # first-sale date or confirm current stock.
    device = "device_645b2e6accb6b4"
    config = device + "-18gb-512gb-ph"
    product_url = "https://rog.asus.com/ph/phones/rog-phone-6-pro-model/"
    spec_url = "https://rog.asus.com/ph/phones/rog-phone-6-pro-model/spec/"
    product_id, spec_id = "rog_phone_6_pro_ph_product", "rog_phone_6_pro_ph_specs"
    sources = [
        src(product_id, "ROG Philippines", product_url,
            "Philippine product listing, local 18 GB/512 GB configuration and page-listed price",
            "The official Philippine product page lists ROG Phone 6 Pro with 18 GB RAM, 512 GB storage, model code S8475, and PHP 64,995. Page stock status and the date to which its listed price applies are not stated."),
        src(spec_id, "ROG Philippines", spec_url,
            "Official Philippine specifications for the local ROG Phone 6 Pro configuration",
            "Manufacturer page identifies Storm White, 18 GB LPDDR5, 512 GB UFS 3.1, chipset, cameras, connectivity, battery and charging details."),
    ]
    fields = [
        f("model_number", product_id, "S8475 (displayed with the local 18 GB/512 GB ROG Phone 6 Pro listing)", "S8475"),
        f("configuration", spec_id, "18 GB LPDDR5 RAM / 512 GB UFS 3.1 storage · Storm White", "18 GB RAM / 512 GB storage"),
        f("ram_capacity", spec_id, "18 GB LPDDR5", 18, key="ramGb", unit="GB"),
        f("ram_type", spec_id, "LPDDR5", "LPDDR5", key="ramType"),
        f("storage_capacity", spec_id, "512 GB", 512, key="storageGb", unit="GB"),
        f("storage_type", spec_id, "UFS 3.1", "UFS 3.1", key="storageType"),
        f("chipset", spec_id, "Qualcomm Snapdragon 8+ Gen 1 Mobile Platform", "Snapdragon 8+ Gen 1", key="chipset"),
        f("gpu", spec_id, "Qualcomm Adreno 730", "Adreno 730", key="gpu"),
        f("rear_camera_system", spec_id, "50 MP Sony IMX766 main + 13 MP ultrawide + 5 MP macro", "50 MP main + 13 MP ultrawide + 5 MP macro"),
        f("battery_capacity", spec_id, "6000 mAh typical", 6000, key="batteryMah", unit="mAh"),
        f("wired_charging", spec_id, "Up to 65 W QC 5.0 / USB PD 3.0", 65, key="chargingW", unit="W"),
        f("wifi", spec_id, "Wi-Fi 6E; feature availability is subject to regional regulation", "Wi-Fi 6E", key="wifi"),
        f("bluetooth", spec_id, "Bluetooth 5.2", "Bluetooth 5.2"),
        f("nfc", spec_id, "NFC supported", "Yes"),
        f("sim_esim", spec_id, "Dual nano-SIM, dual standby", "Dual nano-SIM; eSIM not listed", key="sim"),
        f("current_price_php", product_id,
          "PHP 64,995 listed on the ASUS ROG Philippines product page; observed 2026-11-26. Stock status is not stated.",
          64995, unit="PHP", price_condition="new",
          price_type="Official PH page-listed price; observed 2026-11-26, stock unconfirmed",
          price_observed=OBSERVED,
          note="Dated observation of a manufacturer page-listed amount; it is not represented as an available live offer.",
          replace_existing=True),
        f("philippine_release_date", product_id,
          "Official Philippine product listing confirms local model listing but gives no first-sale date.", None,
          status="PENDING_VERIFICATION", note="Local first authorized-sale date remains unknown."),
    ]
    replacements = [{"id": config, "label": "18 GB RAM / 512 GB storage · Storm White",
                     "sku": None, "modelCode": "S8475",
                     "notes": "Exact Philippine product-page configuration; page does not provide a color-specific order SKU."}]
    out.append(make(device, config, "ROG Phone 6 Pro", replacements[0]["label"], sources, fields,
                    replacements=replacements,
                    availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                  "availabilityStatus": "Official Philippine product listing",
                                  "philippineAvailability": "ROG Philippines lists the 18 GB/512 GB ROG Phone 6 Pro configuration. Current stock and original first-sale date are not stated.",
                                  "observedAt": OBSERVED,
                                  "qualityFlag": "Philippine listing verified; current stock and first-sale date not recorded"},
                    model_code="S8475"))

    # The Philippine product page identifies the standard Pro (not the Pro
    # Edition), exact local SKU, 16/512 configuration and its page-listed price.
    device = "device_d8d3dc343261b9"
    config = device + "-16gb-512gb-ph"
    product_url = "https://rog.asus.com/ph/phones/rog-phone-9-pro/"
    spec_url = "https://rog.asus.com/ph/phones/rog-phone-9-pro/spec/"
    global_spec_url = "https://rog.asus.com/phones/rog-phone-9-pro/spec/"
    product_id, spec_id, global_id = "rog_phone_9_pro_ph_product", "rog_phone_9_pro_ph_specs", "rog_phone_9_pro_global_specs"
    feature_id = "rog_phone_9_pro_ph_camera_features"
    sources = [
        src(product_id, "ROG Philippines", product_url,
            "Philippine product listing, exact standard Pro SKU/configuration, and page-listed price",
            "The PH product page distinguishes ROG Phone 9 Pro from Pro Edition and lists SKU AI2501C-3B048WW, 16 GB RAM, 512 GB storage, and PHP 62,995. Page stock status and price validity period are not stated."),
        src(feature_id, "ROG Philippines", product_url,
            "Official Philippine camera specifications",
            "The local product page lists the standard ROG Phone 9 Pro's 32 MP front camera, distinct from the Pro Edition model listing."),
        src(spec_id, "ROG Philippines", spec_url,
            "Official Philippine technical specifications for ROG Phone 9 Pro",
            "The Philippine specifications page lists the standard Pro at 16 GB RAM and 512 GB storage and supplies processor, display, video, audio, wireless, and charging specifications."),
        src(global_id, "ROG Global", global_spec_url,
            "Supplementary exact-model specifications not fully shown in the Philippine page text",
            "Global model specification lists shared standard Pro/Pro Edition camera, battery, dimensions, weight and protection details. Configuration-specific RAM/storage are taken from the Philippine product page."),
    ]
    fields = [
        f("model_number", product_id, "AI2501C-3B048WW (Philippine ROG Phone 9 Pro, 16 GB/512 GB)", "AI2501C-3B048WW"),
        f("configuration", product_id, "16 GB LPDDR5X RAM / 512 GB UFS 4.0 storage", "16 GB RAM / 512 GB storage"),
        f("ram_capacity", product_id, "16 GB", 16, key="ramGb", unit="GB"),
        f("ram_type", spec_id, "LPDDR5X", "LPDDR5X", key="ramType"),
        f("storage_capacity", product_id, "512 GB", 512, key="storageGb", unit="GB"),
        f("storage_type", spec_id, "UFS 4.0", "UFS 4.0", key="storageType"),
        f("chipset", spec_id, "Qualcomm Snapdragon 8 Elite Mobile Platform", "Snapdragon 8 Elite", key="chipset"),
        f("cpu", spec_id, "64-bit octa-core up to 4.3 GHz", "Octa-core up to 4.3 GHz"),
        f("gpu", spec_id, "Qualcomm Adreno 830", "Adreno 830", key="gpu"),
        f("operating_system", spec_id, "Android 15", "Android 15", key="os"),
        f("display_size", spec_id, "6.78 inches", 6.78, key="displayInches", unit="in"),
        f("display_technology", global_id, "Samsung Flexible AMOLED", "Flexible AMOLED", key="displayType"),
        f("display_resolution", spec_id, "2400 x 1080 FHD+", "2400 x 1080", key="resolution"),
        f("display_refresh_rate", spec_id, "Up to 165 Hz in system settings / 185 Hz in Game Genie", 185, key="refreshHz", unit="Hz",
          note="Catalog value is the highest manufacturer-listed mode; 185 Hz requires Game Genie."),
        f("display_brightness", global_id, "1,600 nits HBM / 2,500 nits peak", "1,600 nits HBM / 2,500 nits peak", unit="nits"),
        f("display_protection", global_id, "Corning Gorilla Glass Victus 2", "Corning Gorilla Glass Victus 2"),
        f("rear_camera_system", global_id, "50 MP Sony Lytia 700 main with gimbal OIS + 13 MP ultrawide + 32 MP telephoto with 3x optical zoom and OIS", "50 MP main + 13 MP ultrawide + 32 MP 3x telephoto"),
        f("main_camera_sensor", global_id, "Sony Lytia 700 50 MP, f/1.9, gimbal OIS", "Sony Lytia 700 50 MP; f/1.9; gimbal OIS"),
        f("ultrawide_camera", global_id, "13 MP, 120-degree ultrawide", "13 MP, 120-degree ultrawide"),
        f("telephoto_camera", global_id, "32 MP, f/2.4, OIS, 3x optical zoom", "32 MP; f/2.4; OIS; 3x optical zoom"),
        f("front_camera", feature_id, "32 MP", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", spec_id, "Rear main up to 8K/30 fps; 4K/30 or 60 fps main; ultrawide 4K/30 fps; HDR10+ 4K recording", "Rear main up to 8K/30 and 4K/30 or 60 fps; ultrawide 4K/30 fps"),
        f("battery_capacity", global_id, "5800 mAh typical", 5800, key="batteryMah", unit="mAh"),
        f("wired_charging", spec_id, "Up to 65 W QC 5.0 / USB PD 3.0", 65, key="chargingW", unit="W"),
        f("wireless_charging", spec_id, "Up to 15 W, Qi 1.3", "15 W Qi wireless charging"),
        f("dimensions", global_id, "163.8 x 77 x 8.9 mm", "163.8 x 77 x 8.9 mm", key="dimensions", unit="mm"),
        f("weight", global_id, "227 g", 227, key="weightG", unit="g"),
        f("ingress_protection", global_id, "IP68", "IP68"),
        f("wifi", spec_id, "802.11be/ax/ac/a/b/g/n; 6 GHz support subject to regional restrictions", "Wi-Fi 7 capable", key="wifi"),
        f("bluetooth", spec_id, "Bluetooth 5.4", "Bluetooth 5.4"),
        f("nfc", spec_id, "NFC supported", "Yes"),
        f("sim_esim", global_id, "Dual nano-SIM, dual standby", "Dual nano-SIM; eSIM not listed", key="sim"),
        f("current_price_php", product_id,
          "PHP 62,995 listed on the ASUS ROG Philippines product page; observed 2026-11-26. Stock status is not stated.",
          62995, unit="PHP", price_condition="new",
          price_type="Official PH page-listed price; observed 2026-11-26, stock unconfirmed",
          price_observed=OBSERVED,
          note="Dated observation of a manufacturer page-listed amount; it is not represented as an available live offer.",
          replace_existing=True),
        f("philippine_release_date", product_id,
          "Official Philippine product listing confirms local model listing but gives no first-sale date.", None,
          status="PENDING_VERIFICATION", note="Local first authorized-sale date remains unknown."),
    ]
    replacements = [{"id": config, "label": "16 GB RAM / 512 GB storage · Phantom Black",
                     "sku": "AI2501C-3B048WW", "modelCode": "AI2501C",
                     "notes": "Exact standard Pro Philippine configuration; Pro Edition is a separate model and is not merged here."}]
    out.append(make(device, config, "ROG Phone 9 Pro", replacements[0]["label"], sources, fields,
                    replacements=replacements,
                    availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                  "availabilityStatus": "Official Philippine product listing",
                                  "philippineAvailability": "ROG Philippines lists standard ROG Phone 9 Pro SKU AI2501C-3B048WW in 16 GB/512 GB. Current stock and original first-sale date are not stated.",
                                  "observedAt": OBSERVED,
                                  "qualityFlag": "Philippine listing verified; current stock and first-sale date not recorded"},
                    model_code="AI2501C"))

    return out


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = records()
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    for item in items:
        add_review(manual, catalog, item)
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"modelsReviewed": len(items), "fieldReviews": sum(len(x["fields"]) for x in items),
                      "replacementConfigurations": sum(bool(x.get("replacementVariants")) for x in items)}))


if __name__ == "__main__":
    main()
