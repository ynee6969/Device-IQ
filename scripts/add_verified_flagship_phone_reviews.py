#!/usr/bin/env python3
"""Add field-level manufacturer reviews for four source-rich flagship phones."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews, pending  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"


def src(sid, publisher, url, purpose, note, published=None):
    return {"id": sid, "publisher": publisher, "url": url, "publicationDate": published,
            "accessDate": OBSERVED, "purpose": purpose, "note": note}


def f(fid, sid, value, normalized=None, *, key=None, unit=None, status="VERIFIED", note=None,
      price_condition=None, price_type=None, price_observed=None):
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


def make(device, config, brand, model, label, sources, fields, *, replacements=None,
         availability=None, sku=None, model_code=None):
    row = {"deviceId": device, "configurationId": config, "brand": brand, "model": model,
           "configuration": label, "sources": sources, "fields": fields}
    if replacements:
        row["replacementVariants"] = replacements
    if availability:
        row["availabilityEvidence"] = availability
    if sku:
        row["sku"] = sku
    if model_code:
        row["modelCode"] = model_code
    return row


def records():
    out = []
    replacements_for = {}

    # ASUS ROG Phone 8, Philippine-supported 12/256 SKU/color variants.
    device = "device_fca6be23997740"
    spec = "https://rog.asus.com/ph/phones/rog-phone-8/spec/"
    promo = "https://www.asus.com/ph/events/infoM/activity_ShareHolidayROGPhone"
    launch = "https://rog.asus.com/ph/articles/smartphones/the-rog-phone-8-and-rog-phone-8-pro-beyond-gaming-with-a-slim-new-design/"
    sid_spec, sid_promo, sid_launch = "rog_phone_8_ph_specs", "rog_phone_8_ph_2024_campaign", "rog_phone_8_global_launch"
    sources = [
        src(sid_spec, "ROG Philippines", spec, "Official Philippine specifications and local configuration evidence",
            "Official ROG Philippines page lists local colors, 12 GB/256 GB product SKU, and detailed hardware specifications."),
        src(sid_promo, "ASUS Philippines", promo, "Dated Philippine campaign SRP and exact local SKU codes",
            "ASUS Philippines promotion runs 27 Nov 2024 through 31 Jan 2025 and lists ROG Phone 8 Gray and Black, both 12 GB/256 GB with campaign SRP PHP 48,995.", "2024-11-27"),
        src(sid_launch, "ROG Philippines", launch, "Manufacturer model introduction",
            "ROG product article dated 9 Jan 2024 introduces the Phone 8 series globally; it does not establish Philippine first-sale date.", "2024-01-09"),
    ]
    base = [
        f("philippine_release_date", sid_promo, "Philippine campaign establishes authorized local sale during 27 Nov 2024–31 Jan 2025, but not first-sale date.", None,
          status="PENDING_VERIFICATION", note="Campaign start date is not treated as the device's first authorized sale date."),
        f("display_size", sid_spec, "6.78 inches", 6.78, key="displayInches", unit="in"),
        f("display_technology", sid_spec, "Samsung Flexible AMOLED", "Flexible AMOLED", key="displayType"),
        f("display_resolution", sid_spec, "2400 x 1080", "2400 x 1080", key="resolution"),
        f("display_refresh_rate", sid_spec, "LTPO 1–120 Hz; up to 165 Hz", 165, key="refreshHz", unit="Hz",
          note="The source lists adaptive 1–120 Hz and a maximum 165 Hz gaming refresh rate; catalog stores the maximum."),
        f("display_brightness", sid_spec, "1,600 nits HBM / 2,500 nits peak", "1,600 nits HBM / 2,500 nits peak", unit="nits"),
        f("display_protection", sid_spec, "Corning Gorilla Glass Victus 2", "Corning Gorilla Glass Victus 2"),
        f("chipset", sid_spec, "Qualcomm Snapdragon 8 Gen 3 (SM8650)", "Snapdragon 8 Gen 3", key="chipset"),
        f("cpu", sid_spec, "Octa-core CPUs up to 3.3 GHz", "Octa-core up to 3.3 GHz"),
        f("gpu", sid_spec, "Qualcomm Adreno 750", "Adreno 750", key="gpu"),
        f("operating_system", sid_spec, "Android 14 with ROG UI", "Android 14 with ROG UI", key="os"),
        f("rear_camera_system", sid_spec, "50 MP main with gimbal OIS + 13 MP 120° ultrawide + 5 MP macro", "50 MP main + 13 MP ultrawide + 5 MP macro"),
        f("main_camera_sensor", sid_spec, "Sony IMX890 50 MP, f/1.9, gimbal OIS", "Sony IMX890 50 MP; f/1.9; gimbal OIS"),
        f("ultrawide_camera", sid_spec, "13 MP, 120-degree ultrawide", "13 MP, 120-degree ultrawide"),
        f("telephoto_camera", sid_spec, "No telephoto module is listed in the ROG Phone 8 local spec table.", "No telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", sid_spec, "32 MP RGBW sensor; binned output 8 MP", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", sid_spec, "Main rear camera up to 8K/24 fps; 4K/30 or 60 fps; front video modes not listed here", "Rear main up to 8K/24 fps; 4K/30 or 60 fps"),
        f("battery_capacity", sid_spec, "5,500 mAh typical", 5500, key="batteryMah", unit="mAh"),
        f("wired_charging", sid_spec, "65 W HyperCharge / USB PD adapter support", 65, key="chargingW", unit="W"),
        f("wireless_charging", sid_launch, "Qi-certified 15 W wireless charging", "15 W Qi wireless charging"),
        f("dimensions", sid_spec, "163.8 x 76.8 x 8.9 mm", "163.8 x 76.8 x 8.9 mm", key="dimensions", unit="mm"),
        f("weight", sid_spec, "225 g", 225, key="weightG", unit="g"),
        f("ingress_protection", sid_spec, "IP68", "IP68"),
        f("sim_esim", sid_spec, "Dual nano-SIM; dual standby", "Dual nano-SIM; no eSIM listed", key="sim"),
        f("wifi", sid_spec, "Wi-Fi 7 ready; 802.11 a/b/g/n/ac/ax/be; availability may vary by regulatory region", "Wi-Fi 7 capable", key="wifi"),
        f("bluetooth", sid_spec, "Bluetooth 5.3", "Bluetooth 5.3"),
        f("usb", sid_spec, "USB Type-C", "USB Type-C", key="ports"),
        f("audio", sid_spec, "Dual stereo speakers; 3.5 mm audio output; Dirac Virtuo", "Dual stereo speakers; 3.5 mm jack; Dirac Virtuo", key="sound"),
    ]
    replacements = [
        {"id": device + "-12-256-black-ph", "label": "12 GB RAM / 256 GB storage · Phantom Black", "sku": "AI2401_C-1A078WW", "modelCode": "AI2401_C"},
        {"id": device + "-12-256-gray-ph", "label": "12 GB RAM / 256 GB storage · Storm Gray", "sku": "AI2401_C-1C079WW", "modelCode": "AI2401_C"},
    ]
    replacements_for[device] = replacements
    for index, v in enumerate(replacements):
        fields = [f("model_number", sid_promo, v["sku"], v["sku"]),
                  f("configuration", sid_promo, "12 GB LPDDR5X + 256 GB UFS 4.0", "12 GB RAM / 256 GB storage"),
                  f("ram_capacity", sid_spec, "12 GB LPDDR5X", 12, key="ramGb", unit="GB"),
                  f("ram_type", sid_spec, "LPDDR5X", "LPDDR5X", key="ramType"),
                  f("storage_capacity", sid_spec, "256 GB", 256, key="storageGb", unit="GB"),
                  f("storage_type", sid_spec, "UFS 4.0", "UFS 4.0", key="storageType"),
                  f("current_price_php", sid_promo, "Campaign SRP PHP 48,995", 48995, unit="PHP",
                    price_condition="new", price_type="Historical ASUS Philippines campaign SRP (27 Nov 2024–31 Jan 2025; not a current offer)",
                    price_observed="2024-11-27",
                    note="Dated campaign SRP for the specified local 12 GB/256 GB model; campaign bundle benefits are separate and this is not a current price."),
                  *base]
        out.append(make(device, v["id"], "ASUS", "ROG Phone 8", v["label"], sources, fields,
                        replacements=replacements if index == 0 else None,
                        availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                      "availabilityStatus": "ASUS Philippines campaign and official ROG Philippines specification pages list local 12 GB/256 GB model SKUs.",
                                      "philippineAvailability": "Philippine authorized-channel model listing is confirmed; first authorized-sale date and current stock are not established.",
                                      "observedAt": OBSERVED,
                                      "qualityFlag": "First Philippine sale date and present stock not recorded"} if index == 0 else None,
                        sku=v["sku"], model_code=v["modelCode"]))

    # ASUS ROG Phone 8 Pro and Pro Edition, exact Philippine SKUs, listed prices, and official technical specs.
    device = "device_92c3d063a77fd3"
    product = "https://rog.asus.com/ph/phones/rog-phone-8-pro/"
    spec = "https://rog.asus.com/ph/phones/rog-phone-8-pro/spec/"
    promo = "https://www.asus.com/ph/events/infoM/activity_ShareHolidayROGPhone"
    sid_product, sid_spec, sid_campaign = "rog_phone_8_pro_ph_product", "rog_phone_8_pro_ph_specs", "rog_phone_8_pro_ph_2024_campaign"
    sources = [
        src(sid_product, "ROG Philippines", product, "Official Philippine product, model codes, configurations, and page-listed prices",
            "Official ROG Philippines page lists Pro 16 GB/512 GB SKU AI2401_D-5B077WW at PHP 60,995 and Pro Edition 24 GB/1 TB SKU AI2401_D-5B076WW at PHP 75,995. Stock status is not shown in the cited text."),
        src(sid_spec, "ROG Philippines", spec, "Official manufacturer technical specifications",
            "Official ROG Philippines technical page supplies device specifications; exact network and camera descriptions are taken from the local page and manufacturer model-level values."),
        src(sid_campaign, "ASUS Philippines", promo, "Dated official campaign pricing cross-check",
            "ASUS Philippines 2024 holiday campaign listed Pro 16/512 campaign SRP PHP 59,995 and Pro Edition 24/1 TB SRP PHP 75,995. This historical campaign amount is kept as corroborating context, not substituted for the product-page amount."),
    ]
    base = [
        f("philippine_release_date", sid_campaign, "Official PH product and campaign pages confirm local sale but do not state first authorized-sale date.", None,
          status="PENDING_VERIFICATION", note="Do not infer first sale from a dated campaign window."),
        f("display_size", sid_spec, "6.78 inches", 6.78, key="displayInches", unit="in"),
        f("display_technology", sid_spec, "Samsung Flexible AMOLED", "Flexible AMOLED", key="displayType"),
        f("display_resolution", sid_spec, "2400 x 1080", "2400 x 1080", key="resolution"),
        f("display_refresh_rate", sid_spec, "LTPO 1–120 Hz; up to 165 Hz", 165, key="refreshHz", unit="Hz",
          note="Adaptive 1–120 Hz; maximum gaming refresh rate 165 Hz."),
        f("display_brightness", sid_spec, "1,600 nits HBM / 2,500 nits peak", "1,600 nits HBM / 2,500 nits peak", unit="nits"),
        f("display_protection", sid_spec, "Corning Gorilla Glass Victus 2", "Corning Gorilla Glass Victus 2"),
        f("chipset", sid_spec, "Qualcomm Snapdragon 8 Gen 3 (SM8650)", "Snapdragon 8 Gen 3", key="chipset"),
        f("cpu", sid_spec, "Octa-core CPU up to 3.3 GHz", "Octa-core up to 3.3 GHz"),
        f("gpu", sid_spec, "Qualcomm Adreno 750", "Adreno 750", key="gpu"),
        f("operating_system", sid_spec, "Android 14 with ROG UI", "Android 14 with ROG UI", key="os"),
        f("rear_camera_system", sid_spec, "50 MP gimbal-OIS main + 13 MP ultrawide + 32 MP 3x OIS telephoto + 5 MP macro listed on the manufacturer spec page", "50 MP main + 13 MP ultrawide + 32 MP telephoto + 5 MP macro"),
        f("main_camera_sensor", sid_spec, "Sony IMX890 50 MP, f/1.9, gimbal OIS", "Sony IMX890 50 MP; f/1.9; gimbal OIS"),
        f("ultrawide_camera", sid_spec, "13 MP, 120-degree ultrawide", "13 MP, 120-degree ultrawide"),
        f("telephoto_camera", sid_spec, "32 MP, f/2.4, OIS, 3x optical zoom", "32 MP; f/2.4; OIS; 3x optical zoom"),
        f("front_camera", sid_spec, "32 MP RGBW; binned output 8 MP", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", sid_spec, "Main rear up to 8K/24 fps; 4K/30 or 60 fps; ultrawide up to 4K/30 fps", "Rear main up to 8K/24 fps; 4K/30 or 60 fps"),
        f("battery_capacity", sid_spec, "5,500 mAh typical", 5500, key="batteryMah", unit="mAh"),
        f("wired_charging", sid_spec, "65 W HyperCharge; QC 5.0 / USB-PD support", 65, key="chargingW", unit="W"),
        f("wireless_charging", sid_spec, "Qi 1.3 wireless charging supported", "Qi wireless charging supported"),
        f("dimensions", sid_spec, "163.8 x 76.8 x 8.9 mm", "163.8 x 76.8 x 8.9 mm", key="dimensions", unit="mm"),
        f("weight", sid_spec, "225 g", 225, key="weightG", unit="g"),
        f("ingress_protection", sid_spec, "IP68", "IP68"),
        f("sim_esim", sid_spec, "Dual nano-SIM, dual standby", "Dual nano-SIM; eSIM not listed", key="sim"),
        f("wifi", sid_spec, "Wi-Fi 7-capable (802.11 a/b/g/n/ac/ax/be); regional features may vary", "Wi-Fi 7 capable", key="wifi"),
        f("bluetooth", sid_spec, "Bluetooth 5.4", "Bluetooth 5.4"),
        f("usb", sid_spec, "USB Type-C", "USB Type-C", key="ports"),
        f("audio", sid_spec, "Dual stereo speakers; 3.5 mm output; Dirac Virtuo for Headphone", "Dual stereo speakers; 3.5 mm jack; Dirac Virtuo", key="sound"),
    ]
    replacements = [
        {"id": device + "-16-512-ph", "label": "16 GB RAM / 512 GB storage · Phantom Black", "sku": "AI2401_D-5B077WW", "modelCode": "AI2401_D"},
        {"id": device + "-24-1024-ph", "label": "24 GB RAM / 1 TB storage · Phantom Black · Pro Edition", "sku": "AI2401_D-5B076WW", "modelCode": "AI2401_D"},
    ]
    replacements_for[device] = replacements
    for index, (v, ram, storage, price) in enumerate([(replacements[0], 16, 512, 60995), (replacements[1], 24, 1024, 75995)]):
        fields = [f("model_number", sid_product, v["sku"], v["sku"]),
                  f("configuration", sid_product, f"{ram} GB LPDDR5X + {storage} GB UFS 4.0", f"{ram} GB RAM / {storage} GB storage"),
                  f("ram_capacity", sid_product, f"{ram} GB LPDDR5X", ram, key="ramGb", unit="GB"),
                  f("ram_type", sid_spec, "LPDDR5X", "LPDDR5X", key="ramType"),
                  f("storage_capacity", sid_product, f"{storage} GB", storage, key="storageGb", unit="GB"),
                  f("storage_type", sid_spec, "UFS 4.0", "UFS 4.0", key="storageType"),
                  f("current_price_php", sid_product, f"Official page-listed price PHP {price:,}", price, unit="PHP",
                    price_condition="new", price_type="Official ROG Philippines product-page listed price (stock not verified)",
                    price_observed=OBSERVED,
                    note="Amount is transcribed from the official Philippines product page. The page did not establish stock at observation; treat this as a dated page-listed price, not a confirmed in-stock offer."),
                  *base]
        out.append(make(device, v["id"], "ASUS", "ROG Phone 8 Pro", v["label"], sources, fields,
                        replacements=replacements if index == 0 else None,
                        availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                      "availabilityStatus": "Official ROG Philippines page lists both Pro SKUs and PHP-denominated prices; current stock is not shown.",
                                      "philippineAvailability": "Local authorized-channel configurations and official page-listed prices are confirmed; first-sale date and present stock are not.",
                                      "observedAt": OBSERVED,
                                      "qualityFlag": "First Philippine sale date and present stock not recorded"} if index == 0 else None,
                        sku=v["sku"], model_code=v["modelCode"]))

    # OnePlus 12: official regional configurations and specifications; no PH sale/price evidence found.
    device = "device_a8aa4ea8df33a0"
    spec = "https://www.oneplus.com/qa_en/12/specs"
    sid = "oneplus_12_qa_specs"
    sources = [src(sid, "OnePlus", spec, "Official manufacturer regional specifications",
                   "OnePlus official page lists 12 GB+256 GB and 16 GB+512 GB configurations and detailed model specifications. It is not a Philippine retail or launch page.")]
    base = [
        f("philippine_release_date", sid, "No Philippine launch or authorized-sale date appears on the cited regional specifications page.", None,
          status="PENDING_VERIFICATION", note="Global product specifications do not establish Philippine availability."),
        f("display_size", sid, "6.82 inches", 6.82, key="displayInches", unit="in"),
        f("display_technology", sid, "120 Hz ProXDR LTPO display", "LTPO ProXDR display", key="displayType"),
        f("display_resolution", sid, "3168 x 1440", "3168 x 1440", key="resolution"),
        f("display_refresh_rate", sid, "Dynamic 1–120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", sid, "1,600 nits HBM / 4,500 nits peak", "1,600 nits HBM / 4,500 nits peak", unit="nits"),
        f("display_protection", sid, "Corning Gorilla Glass Victus 2", "Corning Gorilla Glass Victus 2"),
        f("chipset", sid, "Snapdragon 8 Gen 3 Mobile Platform", "Snapdragon 8 Gen 3", key="chipset"),
        f("cpu", sid, "Qualcomm Kryo CPU", "Qualcomm Kryo CPU"),
        f("gpu", sid, "Adreno 750", "Adreno 750", key="gpu"),
        f("operating_system", sid, "OxygenOS 14.0 based on Android 14", "OxygenOS 14 / Android 14", key="os"),
        f("ram_type", sid, "LPDDR5X", "LPDDR5X", key="ramType"),
        f("storage_type", sid, "UFS 4.0", "UFS 4.0", key="storageType"),
        f("rear_camera_system", sid, "50 MP main + 64 MP periscope telephoto + 48 MP ultrawide", "50 MP main + 64 MP telephoto + 48 MP ultrawide"),
        f("main_camera_sensor", sid, "Sony LYT-808, 50 MP, OIS, f/1.6", "Sony LYT-808 50 MP; OIS; f/1.6"),
        f("ultrawide_camera", sid, "Sony IMX581, 48 MP, 114-degree field of view", "Sony IMX581 48 MP; 114 degrees"),
        f("telephoto_camera", sid, "OmniVision OV64B, 64 MP periscope, 3x optical zoom, OIS", "OV64B 64 MP periscope; 3x optical zoom; OIS"),
        f("front_camera", sid, "Sony IMX615, 32 MP", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", sid, "Rear up to 8K/24 fps; 4K/30 or 60 fps; front up to 4K/30 fps", "Rear up to 8K/24 fps; 4K/30 or 60 fps; front 4K/30 fps"),
        f("battery_capacity", sid, "5,400 mAh typical dual-cell equivalent", 5400, key="batteryMah", unit="mAh"),
        f("wired_charging", sid, "100 W SUPERVOOC", 100, key="chargingW", unit="W"),
        f("wireless_charging", sid, "50 W AIRVOOC wireless charging", "50 W wireless charging"),
        f("dimensions", sid, "164.3 x 75.8 x 9.15 mm", "164.3 x 75.8 x 9.15 mm", key="dimensions", unit="mm"),
        f("weight", sid, "220 g", 220, key="weightG", unit="g"),
        f("sim_esim", sid, "Dual nano-SIM; eSIM availability may vary by carrier/region", "Dual nano-SIM; eSIM region-dependent"),
        f("cellular_bands", sid, "Global 2G/3G/4G/5G bands are listed on the source page; regional support may vary", "Regional bands listed on source page"),
        f("wifi", sid, "Wi-Fi 7 / Wi-Fi 6E and earlier standards", "Wi-Fi 7 / Wi-Fi 6E", key="wifi"),
        f("bluetooth", sid, "Bluetooth 5.4", "Bluetooth 5.4"),
        f("usb", sid, "USB Type-C, USB 3.2 Gen 1", "USB Type-C; USB 3.2 Gen 1", key="ports"),
        f("nfc", sid, "NFC enabled", "Yes"),
        f("audio", sid, "Dolby Atmos audio", "Dolby Atmos", key="sound"),
    ]
    variants = [(device + "-12-256-global", "12 GB RAM / 256 GB storage (global source configuration)", 12, 256),
                (device + "-16-512-global", "16 GB RAM / 512 GB storage (global source configuration)", 16, 512)]
    replacements = [{"id": vid, "label": label, "sku": None, "modelCode": None,
                     "notes": "Official OnePlus regional specification page lists this configuration; Philippine SKU, sale, and price are unverified."}
                    for vid, label, _, _ in variants]
    replacements_for[device] = replacements
    for index, (vid, label, ram, storage) in enumerate(variants):
        fields = [f("model_number", sid, "Regional model code not listed on the cited specifications page.", None, status="PENDING_VERIFICATION"),
                  f("configuration", sid, f"{ram} GB + {storage} GB", f"{ram} GB RAM / {storage} GB storage"),
                  f("ram_capacity", sid, f"{ram} GB LPDDR5X", ram, key="ramGb", unit="GB"),
                  f("storage_capacity", sid, f"{storage} GB UFS 4.0", storage, key="storageGb", unit="GB"),
                  *base,
                  pending("official_launch_price_php", sid, "No Philippine launch price is stated on this regional specification page.", "Foreign-market prices are not converted to PHP."),
                  pending("current_price_php", sid, "No dated Philippine price observation was located in the cited source.", "Regional product specification does not establish a Philippine retail offer.")]
        out.append(make(device, vid, "OnePlus", "12", label, sources, fields,
                        replacements=replacements if index == 0 else None))

    # OnePlus 13: official Philippine-language specification page confirms configurations and detailed hardware.
    device = "device_edc07536e9cd09"
    spec = "https://www.oneplus.com/ph/13/specs"
    sid = "oneplus_13_ph_specs"
    sources = [src(sid, "OnePlus Philippines", spec, "Official Philippines-localized product specifications",
                   "Official OnePlus Philippines specs list 12 GB+256 GB and 16 GB+512 GB configurations. The specification page does not by itself establish a Philippine sale date or PHP price.")]
    base = [
        f("philippine_release_date", sid, "Philippines-localized specification page does not state launch/first-sale date or show a Philippine sale offer.", None,
          status="PENDING_VERIFICATION", note="The localized spec page is technical evidence only, not evidence of authorized sale."),
        f("display_size", sid, "6.82 inches", 6.82, key="displayInches", unit="in"),
        f("display_technology", sid, "120 Hz ProXDR display with LTPO 4.1", "LTPO 4.1 ProXDR display", key="displayType"),
        f("display_resolution", sid, "3168 x 1440", "3168 x 1440", key="resolution"),
        f("display_refresh_rate", sid, "Dynamic 1–120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", sid, "1,600 nits HBM / 4,500 nits peak", "1,600 nits HBM / 4,500 nits peak", unit="nits"),
        f("display_protection", sid, "Ceramic Guard cover glass", "Ceramic Guard"),
        f("chipset", sid, "Snapdragon 8 Elite Mobile Platform", "Snapdragon 8 Elite", key="chipset"),
        f("cpu", sid, "Qualcomm Oryon CPU up to 4.32 GHz", "Qualcomm Oryon up to 4.32 GHz"),
        f("gpu", sid, "Adreno 830", "Adreno 830", key="gpu"),
        f("operating_system", sid, "OxygenOS 15.0 based on Android 15", "OxygenOS 15 / Android 15", key="os"),
        f("ram_type", sid, "LPDDR5X", "LPDDR5X", key="ramType"),
        f("storage_type", sid, "UFS 4.0", "UFS 4.0", key="storageType"),
        f("rear_camera_system", sid, "50 MP main + 50 MP 3x telephoto + 50 MP ultrawide", "50 MP main + 50 MP telephoto + 50 MP ultrawide"),
        f("main_camera_sensor", sid, "Sony LYT-808, 50 MP, OIS, f/1.6", "Sony LYT-808 50 MP; OIS; f/1.6"),
        f("ultrawide_camera", sid, "S5KJN5, 50 MP, 120-degree field of view", "S5KJN5 50 MP; 120 degrees"),
        f("telephoto_camera", sid, "Sony LYT-600, 50 MP, 3x optical zoom, OIS", "Sony LYT-600 50 MP; 3x optical zoom; OIS"),
        f("front_camera", sid, "Sony IMX615, 32 MP", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", sid, "Rear up to 8K/30 fps; 4K/30 or 60 fps; front up to 4K/60 fps", "Rear up to 8K/30 fps; 4K/30 or 60 fps"),
        f("battery_capacity", sid, "6,000 mAh typical dual-cell equivalent; 5,840 mAh rated equivalent", 6000, key="batteryMah", unit="mAh",
          note="Catalog value is the manufacturer-stated typical equivalent capacity; rated equivalent capacity is 5,840 mAh."),
        f("wired_charging", sid, "100 W SUPERVOOC", 100, key="chargingW", unit="W"),
        f("wireless_charging", sid, "50 W AIRVOOC wireless charging", "50 W wireless charging"),
        f("dimensions", sid, "162.9 x 76.5 x 8.5 mm (Arctic Dawn/Black Eclipse); 8.9 mm (Midnight Ocean)", "162.9 x 76.5 x 8.5 or 8.9 mm", unit="mm",
          note="Color/finish-specific dimensions differ; no single scalar is assigned."),
        f("weight", sid, "213 g (Arctic Dawn/Black Eclipse); 210 g (Midnight Ocean)", "213 g or 210 g by finish", unit="g",
          note="Official source gives finish-specific weights; no single scalar is assigned."),
        f("sim_esim", sid, "Dual nano-SIM; eSIM feature availability can vary by local carrier", "Dual nano-SIM; eSIM carrier/region-dependent"),
        f("cellular_bands", sid, "2G/3G/4G/5G bands listed on source page; regional coverage depends on variant and carrier", "Bands listed on official PH page; regional support applies"),
        f("wifi", sid, "Wi-Fi 7 / Wi-Fi 6 / Wi-Fi 5", "Wi-Fi 7", key="wifi"),
        f("bluetooth", sid, "Bluetooth 5.4", "Bluetooth 5.4"),
        f("usb", sid, "USB Type-C, USB 3.2 Gen 1", "USB Type-C; USB 3.2 Gen 1", key="ports"),
        f("nfc", sid, "NFC enabled", "Yes"),
        f("gnss", sid, "GPS dual-band, GLONASS, BeiDou, Galileo, QZSS", "GPS; GLONASS; BeiDou; Galileo; QZSS"),
        f("audio", sid, "OReality Audio; noise cancellation support", "OReality Audio"),
    ]
    variants = [(device + "-12-256-phspec", "12 GB RAM / 256 GB storage (OnePlus Philippines spec page)", 12, 256),
                (device + "-16-512-phspec", "16 GB RAM / 512 GB storage (OnePlus Philippines spec page)", 16, 512)]
    replacements = [{"id": vid, "label": label, "sku": None, "modelCode": None,
                     "notes": "Configuration listed on official OnePlus Philippines specification page. This does not establish a local sale or Philippine SKU."}
                    for vid, label, _, _ in variants]
    replacements_for[device] = replacements
    for index, (vid, label, ram, storage) in enumerate(variants):
        fields = [f("model_number", sid, "OnePlus Philippines page does not provide the exact SKU/model code.", None, status="PENDING_VERIFICATION"),
                  f("configuration", sid, f"{ram} GB + {storage} GB", f"{ram} GB RAM / {storage} GB storage"),
                  f("ram_capacity", sid, f"{ram} GB LPDDR5X", ram, key="ramGb", unit="GB"),
                  f("storage_capacity", sid, f"{storage} GB UFS 4.0", storage, key="storageGb", unit="GB"),
                  *base,
                  pending("official_launch_price_php", sid, "No Philippine launch price is stated on the specification page.", "Do not infer price from the Philippines locale or foreign retailer listings."),
                  pending("current_price_php", sid, "No dated Philippine store offer or price appears on the specification page.", "Technical specifications alone do not establish local pricing.")]
        out.append(make(device, vid, "OnePlus", "13", label, sources, fields,
                        replacements=replacements if index == 0 else None))

    return out, replacements_for


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items, replacements_for = records()
    for device, replacement in replacements_for.items():
        target = next(d for d in catalog if d["id"] == device)
        target["variants"] = [{"id": v["id"], "specs": {}} for v in replacement]
    for item in items:
        add_review(manual, catalog, item)
    deduplicate_target_reviews(manual, {(i["deviceId"], i["configurationId"]) for i in items})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewedPhoneConfigurations": len(items), "models": len(replacements_for), "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
