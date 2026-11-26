#!/usr/bin/env python3
"""Add a source-backed manual review batch for unresolved tablet inventory records."""
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


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def field(fid: str, sid: str, value, normalized=None, *, key=None, unit=None,
          status="VERIFIED", note=None, price_condition=None, price_type=None,
          price_observed=None):
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    if price_condition:
        row["priceCondition"] = price_condition
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed
    return row


def record(device, config, brand, model, label, sources, fields, *, replacements=None,
           availability=None, model_code=None):
    item = {"deviceId": device, "configurationId": config, "brand": brand,
            "model": model, "configuration": label, "sources": sources,
            "fields": fields}
    if replacements:
        item["replacementVariants"] = replacements
    if availability:
        item["availabilityEvidence"] = availability
    if model_code:
        item["modelCode"] = model_code
    return item


def records():
    out = []

    # Huawei MatePad Pro 12.6 (2021), exact PH-supported configuration.
    device = "device_3a670bbfcef402"
    config = device + "-8-256-ph"
    huawei_specs = "https://consumer.huawei.com/sa-en/tablets/matepad-pro-12-6-2021/specs/"
    huawei_features = "https://consumer.huawei.com/sa-en/tablets/matepad-pro-12-6-2021/"
    huawei_ph = "https://consumer.huawei.com/ph/community/details/topicId-136912/"
    huawei_support = "https://consumer.huawei.com/ph/support/content/en-us15818652/"
    sid_specs, sid_features = "matepad_pro_126_2021_specs", "matepad_pro_126_2021_features"
    sid_ph, sid_support = "matepad_pro_126_2021_ph_launch", "matepad_pro_126_2021_ph_config"
    pro_sources = [
        src(sid_specs, "HUAWEI KSA", huawei_specs, "Official manufacturer specifications",
            "Official specifications for MatePad Pro 12.6 2021. The listed 8 GB / 256 GB configuration is also named in Huawei Philippines support; regional model code is not supplied there."),
        src(sid_features, "HUAWEI KSA", huawei_features, "Official manufacturer product details",
            "Official feature page documents the Kirin 9000E process, stylus and keyboard compatibility, and charging capabilities."),
        src(sid_ph, "HUAWEI Philippines Community", huawei_ph, "Philippine retail and availability evidence",
            "Huawei Philippines says the tablet retails for PHP 55,999 and is available through Huawei stores and its official online store. The contemporary notice includes June–July 2021 sales dates but does not establish the first authorized sale date."),
        src(sid_support, "HUAWEI Support Philippines", huawei_support, "Philippine-supported configuration",
            "Applicable product is explicitly identified as MatePad Pro 12.6-inch 2021 Edition, 8 GB + 256 GB."),
    ]
    pro_common = [
        field("model_number", sid_support, "MatePad Pro 12.6-inch 2021 Edition; Huawei support page does not provide the exact Philippine SKU", None,
              status="PENDING_VERIFICATION", note="The edition and memory configuration are confirmed, but the exact Philippine model/SKU code is not stated on the cited support page."),
        field("configuration", sid_support, "8 GB RAM + 256 GB ROM", "8 GB RAM / 256 GB storage"),
        pending("philippine_release_date", sid_ph, "Huawei Philippines confirms retail availability but does not state the first authorized sale date.",
                "Do not infer the initial sale date from the 2021 promotion window."),
        field("official_launch_price_php", sid_ph, "Philippine retail price PHP 55,999", 55999, unit="PHP",
              note="Official Huawei Philippines community notice reports PHP 55,999 retail pricing. This is a dated historical retail figure, not a current price."),
        field("display_size", sid_specs, "12.6 inches", 12.6, key="displayInches", unit="in"),
        field("display_technology", sid_specs, "OLED", "OLED", key="displayType"),
        field("display_resolution", sid_specs, "2560 x 1600", "2560 x 1600", key="resolution"),
        field("chipset", sid_specs, "HUAWEI Kirin 9000E", "Kirin 9000E", key="chipset"),
        field("process_node", sid_features, "5 nm", 5, unit="nm"),
        field("cpu", sid_specs, "1 x Cortex-A77 at 3.13 GHz + 3 x Cortex-A77 at 2.54 GHz + 4 x Cortex-A55 at 2.05 GHz",
              "1x Cortex-A77 3.13 GHz + 3x Cortex-A77 2.54 GHz + 4x Cortex-A55 2.05 GHz"),
        field("gpu", sid_specs, "22-core Mali-G78", "22-core Mali-G78", key="gpu"),
        field("operating_system", sid_specs, "HarmonyOS 2", "HarmonyOS 2", key="os"),
        field("ram_capacity", sid_specs, "8 GB", 8, key="ramGb", unit="GB"),
        field("storage_capacity", sid_specs, "256 GB", 256, key="storageGb", unit="GB"),
        field("storage_expansion", sid_specs, "NM memory card up to 256 GB; card sold separately", "NM card up to 256 GB"),
        field("rear_camera_system", sid_specs, "13 MP main + 8 MP wide-angle + 3D depth-sensing camera", "13 MP main + 8 MP wide angle + 3D depth sensing"),
        field("ultrawide_camera", sid_specs, "8 MP wide-angle rear camera", "8 MP", unit="MP"),
        field("telephoto_camera", sid_specs, "The rear system is listed as main, wide-angle, and 3D depth sensing; no telephoto module is listed.",
              "No telephoto camera listed", status="NOT_APPLICABLE"),
        field("front_camera", sid_specs, "8 MP", 8, key="frontCameraMp", unit="MP"),
        field("video_recording", sid_specs, "Rear video resolution up to 3840 x 2160; front video resolution up to 1920 x 1080", "Rear up to 3840 x 2160; front up to 1920 x 1080"),
        field("battery_capacity", sid_specs, "10,050 mAh typical; 10,000 mAh rated", 10050, key="batteryMah", unit="mAh",
              note="Catalog value is the manufacturer’s typical capacity; the source separately lists 10,000 mAh rated capacity."),
        field("wired_charging", sid_specs, "Up to 10 V / 4 A HUAWEI SuperCharge (40 W)", 40, key="chargingW", unit="W"),
        field("dimensions", sid_specs, "184.7 x 286.5 x 6.7 mm", "184.7 x 286.5 x 6.7 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "Approx. 609 g (WGR-W09); approx. 616 g (WGR-W19)", "609 g (WGR-W09) / 616 g (WGR-W19)", unit="g",
              note="The two source model codes have different stated weights; the Philippine support page does not identify which code applies, so no single catalog weight is assigned."),
        field("wifi", sid_specs, "Wi-Fi 6+; 802.11 a/b/g/n/ac/ax", "Wi-Fi 6+", key="wifi"),
        field("bluetooth", sid_specs, "Bluetooth 5.2", "Bluetooth 5.2"),
        field("usb", sid_specs, "USB Type-C, USB 3.1 Gen 1 (included cable supports USB 2.0)", "USB Type-C; USB 3.1 Gen 1", key="ports"),
        field("gnss", sid_specs, "GPS / GLONASS / BeiDou / Galileo / QZSS", "GPS, GLONASS, BeiDou, Galileo, QZSS"),
        field("audio", sid_specs, "8 speakers; HUAWEI Histen 7.0", "8 speakers; HUAWEI Histen 7.0", key="sound"),
        field("sensors", sid_specs, "Ambient light, compass, gravity, gyroscope, and Hall sensors", "Ambient light; compass; gravity; gyroscope; Hall"),
        field("tablet_stylus", sid_features, "Compatible with 2nd-generation HUAWEI M-Pencil; accessory availability varies by market", "2nd-generation HUAWEI M-Pencil compatible" , key="stylus"),
        field("tablet_keyboard", sid_features, "Compatible with HUAWEI Smart Magnetic Keyboard; accessory availability varies by market", "HUAWEI Smart Magnetic Keyboard compatible", key="keyboard"),
    ]
    out.append(record(device, config, "Huawei", "MatePad Pro 12.6", "8 GB RAM / 256 GB storage",
                      pro_sources, pro_common,
                      replacements=[{"id": config, "label": "8 GB RAM / 256 GB storage (Philippine-supported)", "sku": None,
                                     "modelCode": None, "notes": "Huawei Philippines support identifies this exact memory configuration; no local SKU code is published."}],
                      availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                    "availabilityStatus": "Huawei Philippines reported the MatePad Pro 12.6 as available through Huawei stores and its official online store in a 2021 notice.",
                                    "philippineAvailability": "Philippine authorized retail availability confirmed by a Huawei Philippines notice; exact first-sale date is not documented.",
                                    "observedAt": OBSERVED,
                                    "qualityFlag": "Philippine launch or first-sale date not recorded"}))

    # Huawei MatePad 11: Philippine support lists 6/128 and 6/256; global page supplies model-level specs.
    device = "device_a12a6e701e607e"
    ph_support = "https://consumer.huawei.com/ph/support/content/en-us15925868/"
    preorder = "https://consumer.huawei.com/ph/offer/product/matepad-11/buy/"
    store = "https://consumer.huawei.com/ph/offer/smart-office/"
    specs = "https://consumer.huawei.com/sg/tablets/matepad-11/specs/"
    sid_ph, sid_sale, sid_specs, sid_price = "matepad_11_ph_supported_configs", "matepad_11_ph_preorder", "matepad_11_sg_specs", "matepad_11_ph_store_price"
    sources = [
        src(sid_ph, "HUAWEI Support Philippines", ph_support, "Philippine-supported configurations",
            "Huawei Philippines lists MatePad 11 configurations including 10.95-inch 6 GB + 128 GB and 6 GB + 256 GB; it also lists a separate Wi-Fi-only 4 GB + 128 GB configuration, which is not conflated with the 6 GB variants."),
        src(sid_sale, "HUAWEI Philippines Store", preorder, "Philippine pre-order / fulfillment evidence",
            "The official product page states delivery from 23 August 2021 onwards; this is an availability bound, not proof of the first sale date."),
        src(sid_specs, "HUAWEI Singapore", specs, "Official manufacturer technical specifications",
            "Manufacturer specification page for MatePad 11. Model-level technical fields are used as device references; local network SKU and configuration differences are kept separate."),
        src(sid_price, "HUAWEI Philippines Store", store, "Official Philippine store page price candidate",
            "The page lists MatePad 11 6 GB + 128 GB at PHP 26,999. The product checkout page was out of stock when checked; retained as a pending page-listed price and not presented as a purchasable current offer."),
    ]
    base = [
        field("display_size", sid_specs, "10.95 inches", 10.95, key="displayInches", unit="in"),
        field("display_technology", sid_specs, "TFT LCD (IPS)", "TFT LCD (IPS)", key="displayType"),
        field("display_resolution", sid_specs, "2560 x 1600", "2560 x 1600", key="resolution"),
        field("chipset", sid_specs, "Qualcomm Snapdragon 865", "Snapdragon 865", key="chipset"),
        field("cpu", sid_specs, "1 x Cortex-A77-based 2.84 GHz + 3 x Cortex-A77-based 2.4 GHz + 4 x Cortex-A55-based 1.8 GHz", "1x Cortex-A77 2.84 GHz + 3x Cortex-A77 2.4 GHz + 4x Cortex-A55 1.8 GHz"),
        field("gpu", sid_specs, "Adreno 650 at 587 MHz", "Adreno 650", key="gpu"),
        field("operating_system", sid_specs, "HarmonyOS 2", "HarmonyOS 2", key="os"),
        field("rear_camera_system", sid_specs, "13 MP rear camera, f/1.8, autofocus, LED flash", "13 MP AF rear camera"),
        field("front_camera", sid_specs, "8 MP", 8, key="frontCameraMp", unit="MP"),
        field("video_recording", sid_specs, "Rear up to 3840 x 2160; front up to 1920 x 1080", "Rear up to 3840 x 2160; front up to 1920 x 1080"),
        field("battery_capacity", sid_specs, "7,250 mAh typical; 7,150 mAh rated", 7250, key="batteryMah", unit="mAh",
              note="Catalog value is the typical figure; Huawei separately states the 7,150 mAh rated value."),
        field("wired_charging", sid_specs, "10 V / 2.25 A maximum (22.5 W)", 22.5, key="chargingW", unit="W"),
        field("dimensions", sid_specs, "165.3 x 253.8 x 7.25 mm", "165.3 x 253.8 x 7.25 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "Approx. 485 g including battery", 485, key="weightG", unit="g"),
        field("wifi", sid_specs, "Wi-Fi 6 (802.11 a/b/g/n/ac/ax)", "Wi-Fi 6", key="wifi"),
        field("bluetooth", sid_specs, "Bluetooth 5.1", "Bluetooth 5.1"),
        field("usb", sid_specs, "USB Type-C, USB 3.0; inbox cable supports USB 2.0", "USB Type-C; USB 3.0", key="ports"),
        field("gnss", sid_specs, "GPS / GLONASS / BeiDou / Galileo / QZSS", "GPS, GLONASS, BeiDou, Galileo, QZSS"),
        field("audio", sid_specs, "Four speakers; HUAWEI Histen 7.0", "4 speakers; HUAWEI Histen 7.0", key="sound"),
        field("tablet_stylus", sid_specs, "Compatible with 2nd-generation HUAWEI M-Pencil", "2nd-generation HUAWEI M-Pencil compatible", key="stylus"),
        field("tablet_keyboard", sid_specs, "HUAWEI Smart Magnetic Keyboard compatibility", "HUAWEI Smart Magnetic Keyboard compatible", key="keyboard"),
    ]
    replacement = [
        {"id": device + "-6-128-ph", "label": "6 GB RAM / 128 GB storage (Philippine-supported)", "sku": None, "modelCode": None,
         "notes": "Configuration listed by Huawei Philippines support. Philippine availability is supported at model level; network code is not identified."},
        {"id": device + "-6-256-ph", "label": "6 GB RAM / 256 GB storage (Philippine-supported)", "sku": None, "modelCode": None,
         "notes": "Configuration listed by Huawei Philippines support. Philippine availability is supported at model level; network code is not identified."},
    ]
    for index, (vid, ram, storage) in enumerate([(replacement[0]["id"], 6, 128), (replacement[1]["id"], 6, 256)]):
        fields = [field("configuration", sid_ph, f"{ram} GB + {storage} GB", f"{ram} GB RAM / {storage} GB storage"),
                  field("ram_capacity", sid_ph, f"{ram} GB", ram, key="ramGb", unit="GB"),
                  field("storage_capacity", sid_ph, f"{storage} GB", storage, key="storageGb", unit="GB"),
                  *base,
                  pending("philippine_release_date", sid_sale, "Official product page states delivery from 23 August 2021 onwards; exact first-sale/pre-order start date is not stated.",
                          "A delivery start date confirms an availability bound but is not the first authorized sale date."),
                  pending("current_price_php", sid_price, "Official store page lists PHP 26,999 for 6 GB + 128 GB; checkout was out of stock when checked.",
                          "Retain the page-listed amount for research, but do not publish as a current purchasable price without an in-stock offer."),
                  field("tablet_cellular_variant", sid_specs, "The Singapore specification page says network is not supported; this local page does not identify the PH network configuration.",
                        None, status="PENDING_VERIFICATION", note="Foreign regional SKU connectivity must not be assumed for the Philippine-supported configuration.")]
        out.append(record(device, vid, "Huawei", "MatePad 11", f"{ram} GB RAM / {storage} GB storage",
                          sources, fields, replacements=replacement if index == 0 else None,
                          availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                        "availabilityStatus": "Official Huawei Philippines page documented delivery from 23 August 2021 onwards; current store status is out of stock.",
                                        "philippineAvailability": "A Huawei Philippines product/order page confirms local authorized availability; the first sale date and current stock are not confirmed.",
                                        "observedAt": OBSERVED,
                                        "qualityFlag": "Philippine launch or first-sale date not recorded"} if index == 0 else None))
        if index == 0:
            device_row = next(d for d in json.loads(CATALOG.read_text(encoding="utf-8")) if d["id"] == device)
            # The helper validates subsequent configuration IDs against this in-memory catalog.
            device_row["variants"] = [{"id": item["id"], "specs": {}} for item in replacement]
            setattr(record, "_catalog_override_" + device, device_row)

    # Huawei MatePad 10.4 (2022): source lists configs, but its public launch price included accessories.
    device = "device_dcf630692f9701"
    ph_support = "https://consumer.huawei.com/ph/support/content/en-us15798196/"
    launch = "https://consumer.huawei.com/ph/community/details/topicId-177472/"
    specs = "https://consumer.huawei.com/co/tablets/matepad-2022/specs/"
    ph_identity = "https://consumer.huawei.com/ph/support/content/en-us15819846/"
    sid_support, sid_launch, sid_specs, sid_identity = "matepad_104_2022_ph_configs", "matepad_104_2022_ph_launch", "matepad_104_2022_global_specs", "matepad_104_2022_model_code"
    sources = [
        src(sid_support, "HUAWEI Support Philippines", ph_support, "Manufacturer-listed configurations",
            "Huawei Philippines support lists four configurations explicitly tagged 10.4-inch 2022: Wi-Fi 4+64, LTE 4+64, Wi-Fi 4+128, and LTE 4+128. The source is a support applicability list, not a retail SKU availability table."),
        src(sid_launch, "HUAWEI Philippines Community", launch, "Philippine launch and local product description",
            "A Huawei Philippines article edited 27 May 2022 says the 2022 MatePad launched in the Philippines earlier that month and was available for PHP 18,999 with a keyboard, M-Pencil, and app benefits. The bundle amount is not assigned as a tablet-only variant price.", "2022-05-27"),
        src(sid_specs, "HUAWEI Colombia", specs, "Official manufacturer technical specifications",
            "Official MatePad 2022 product specification page. Global model-level data is used only where it matches the 2022 product; it does not establish Philippine configuration details."),
        src(sid_identity, "HUAWEI Support Philippines", ph_identity, "Model-year identity cross-check",
            "Official support table identifies MatePad 10.4-inch 2022 as model family BAH4 and distinguishes it from MatePad 10.4-inch 2020 BAH3."),
    ]
    variants = [
        (device + "-wifi-4-64", "Wi-Fi only · 4 GB RAM / 64 GB storage", "Wi-Fi only", 4, 64),
        (device + "-lte-4-64", "LTE · 4 GB RAM / 64 GB storage", "LTE", 4, 64),
        (device + "-wifi-4-128", "Wi-Fi only · 4 GB RAM / 128 GB storage", "Wi-Fi only", 4, 128),
        (device + "-lte-4-128", "LTE · 4 GB RAM / 128 GB storage", "LTE", 4, 128),
    ]
    common = [
        field("model_number", sid_identity, "BAH4 model family", "BAH4"),
        field("display_size", sid_specs, "10.4 inches", 10.4, key="displayInches", unit="in"),
        field("display_technology", sid_specs, "IPS touchscreen", "IPS", key="displayType"),
        field("display_resolution", sid_specs, "2000 x 1200", "2000 x 1200", key="resolution"),
        field("display_brightness", sid_specs, "470 nits typical", "470 nits typical", unit="nits"),
        field("chipset", sid_specs, "HUAWEI Kirin 710A", "Kirin 710A", key="chipset"),
        field("cpu", sid_specs, "4 x Cortex-A73 at 2.0 GHz + 4 x Cortex-A53 at 1.7 GHz", "4x Cortex-A73 2.0 GHz + 4x Cortex-A53 1.7 GHz"),
        field("gpu", sid_specs, "Mali G51", "Mali G51", key="gpu"),
        field("operating_system", sid_specs, "HarmonyOS 2", "HarmonyOS 2", key="os"),
        field("storage_expansion", sid_specs, "microSD up to 512 GB", "microSD up to 512 GB"),
        field("rear_camera_system", sid_specs, "13 MP autofocus rear camera", "13 MP autofocus rear camera"),
        field("front_camera", sid_specs, "8 MP", 8, key="frontCameraMp", unit="MP"),
        field("video_recording", sid_specs, "Camera video resolution up to 1920 x 1080", "Up to 1920 x 1080"),
        field("battery_capacity", sid_specs, "7,250 mAh typical; 7,150 mAh rated", 7250, key="batteryMah", unit="mAh",
              note="Catalog value is typical capacity; manufacturer separately lists rated capacity of 7,150 mAh."),
        field("wired_charging", sid_specs, "10 V / 2.25 A (22.5 W); compatible with 9 V / 2 A and 5 V / 2 A", 22.5, key="chargingW", unit="W"),
        field("dimensions", sid_specs, "154.96 x 245.2 x 7.35 mm", "154.96 x 245.2 x 7.35 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "Approximately 450 g including battery", 450, key="weightG", unit="g"),
        field("wifi", sid_specs, "802.11 a/b/g/n/ac; 2.4 and 5 GHz", "Wi-Fi 5", key="wifi"),
        field("bluetooth", sid_specs, "Bluetooth 5.1", "Bluetooth 5.1"),
        field("usb", sid_specs, "USB Type-C, USB 2.0", "USB Type-C; USB 2.0", key="ports"),
        field("audio", sid_launch, "Four speakers tuned by Harman Kardon", "4 speakers; Harman Kardon tuned", key="sound"),
        field("tablet_stylus", sid_launch, "The Philippine launch article describes compatibility with 2nd-generation HUAWEI M-Pencil", "2nd-generation HUAWEI M-Pencil compatible", key="stylus"),
        field("tablet_keyboard", sid_launch, "The Philippine launch article lists HUAWEI Smart Keyboard as part of the offer", "HUAWEI Smart Keyboard compatible", key="keyboard"),
    ]
    replacement = [{"id": vid, "label": label, "sku": None, "modelCode": None,
                    "notes": "Configuration and connectivity type appear in Huawei Philippines support applicability list. The article's PHP 18,999 offer bundled accessories and is not assigned as a tablet-only price."}
                   for vid, label, _, _, _ in variants]
    for index, (vid, label, network, ram, storage) in enumerate(variants):
        fields = [field("configuration", sid_support, label, label),
                  field("ram_capacity", sid_support, f"{ram} GB", ram, key="ramGb", unit="GB"),
                  field("storage_capacity", sid_support, f"{storage} GB", storage, key="storageGb", unit="GB"),
                  field("tablet_cellular_variant", sid_support, network, network, key="cellular"),
                  *common,
                  pending("philippine_release_date", sid_launch, "Article says launched earlier in May 2022; no exact launch or first authorized sale day is stated.",
                          "Preserve month-level evidence only; do not infer a day from the article's last-edited date."),
                  pending("official_launch_price_php", sid_launch, "PHP 18,999 offer included a keyboard, M-Pencil, and app benefits; no tablet-only price/configuration was stated.",
                          "A bundle price cannot be assigned as the tablet-only launch price."),
                  pending("current_price_php", sid_launch, "No current Philippine tablet-only price was located in the reviewed sources.",
                          "The cited launch bundle is historical and includes accessories."),
                  pending("cellular_bands", sid_support, "Configuration list distinguishes Wi-Fi and LTE but does not identify LTE band support.",
                          "No band values are inferred from the model family.")]
        out.append(record(device, vid, "Huawei", "MatePad 10.4 (2022)", label, sources, fields,
                          replacements=replacement if index == 0 else None,
                          availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                        "availabilityStatus": "Huawei Philippines reported the 2022 MatePad launched in the Philippines earlier in May 2022; the exact day is not recorded.",
                                        "philippineAvailability": "Philippine launch and local availability are documented in an official Huawei Philippines community article; specific retail availability of each listed support configuration is not established.",
                                        "observedAt": OBSERVED,
                                        "qualityFlag": "Exact Philippine launch date and per-configuration sale evidence not recorded"} if index == 0 else None))
        if index == 0:
            device_row = next(d for d in json.loads(CATALOG.read_text(encoding="utf-8")) if d["id"] == device)
            device_row["variants"] = [{"id": item["id"], "specs": {}} for item in replacement]
            setattr(record, "_catalog_override_" + device, device_row)

    # Samsung Galaxy Tab A7 Lite LTE: Philippine support listing and retailer promotion identify local SKU and SRP.
    device = "device_2bbc3980a61c93"
    samsung = "https://www.samsung.com/ph/business/tablets/galaxy-tab-a/galaxy-tab-a7-lite-lte-gray-32g-sm-t225nzaaxtc/"
    silver = "https://www.samsung.com/ph/business/tablets/galaxy-tab-a/galaxy-tab-a7-lite-lte-silver-32g-sm-t225nzsaxtc/"
    support = "https://www.samsung.com/ph/support/model/SM-T225NZAAXTC/"
    promo = "https://www.samsung.com/ph/offer/offline/2021/galaxy-tab-a7-lite//token-promo/"
    sid_specs, sid_support, sid_promo = "tab_a7_lite_ph_lte_specs", "tab_a7_lite_ph_support", "tab_a7_lite_ph_2021_srp"
    sid_silver = "tab_a7_lite_ph_silver_specs"
    sources = [
        src(sid_specs, "Samsung Philippines for Business", samsung, "Official Philippine model specifications",
            "Samsung Philippines product detail identifies LTE Galaxy Tab A7 Lite SM-T225NZAAXTC, 3 GB RAM, 32 GB storage, and local hardware specifications."),
        src("tab_a7_lite_global_lte_datasheet", "Samsung Electronics", "https://image-us.samsung.com/SamsungUS/samsungbusiness/pdfs/datasheet/Galaxy_Tab_A7_Lite_Datasheet_LTE_Verizon.pdf", "Official manufacturer chipset reference",
            "Samsung's LTE datasheet lists MediaTek MT8768T and an octa-core 2.3 GHz + 1.8 GHz CPU for the A7 Lite LTE family. Used only for chipset/CPU, not regional LTE band data."),
        src(sid_support, "Samsung Support Philippines", support, "Philippine model code and support identity",
            "Official Samsung Philippines support identifies Galaxy Tab A7 Lite LTE model SM-T225."),
        src(sid_promo, "Samsung Philippines", promo, "Dated Philippine SRP and promotion terms",
            "Samsung's June 2021 promotion lists the Gray and Silver LTE SKUs, SRP PHP 9,490, and a separate non-cash PHP 1,000 token offer. The PHP 8,490 promotional amount is conditional on the token and is not recorded as ordinary SRP.", "2021-06-25"),
        src(sid_silver, "Samsung Philippines for Business", silver, "Official Philippine silver LTE model SKU",
            "Samsung Philippines product detail identifies the Silver SM-T225NZSAXTC variant; its shared specifications match the listed Gray 3 GB / 32 GB LTE configuration."),
    ]
    base = [
        field("display_size", sid_specs, "8.7 inches", 8.7, key="displayInches", unit="in"),
        field("display_technology", sid_specs, "TFT", "TFT", key="displayType"),
        field("display_resolution", sid_specs, "1340 x 800 (WXGA+)", "1340 x 800", key="resolution"),
        field("chipset", "tab_a7_lite_global_lte_datasheet", "MediaTek MT8768T", "MediaTek MT8768T", key="chipset",
              note="Samsung's official LTE family datasheet supplies the chipset; Samsung Philippines supplies the exact SKU and local network specifications."),
        field("cpu", sid_specs, "Octa-core 2.3 GHz + 1.8 GHz", "Octa-core 2.3 GHz + 1.8 GHz"),
        field("operating_system", sid_specs, "Android (Samsung Philippines product page does not specify the shipped version)", "Android", key="os",
              note="The Philippine product detail identifies Android but does not specify its original launch version; Android 11 from other regional sources is not used here."),
        field("storage_expansion", sid_specs, "microSD up to 1 TB", "microSD up to 1 TB"),
        field("rear_camera_system", sid_specs, "8 MP autofocus rear camera", "8 MP AF rear camera"),
        field("front_camera", sid_specs, "2 MP", 2, key="frontCameraMp", unit="MP"),
        field("video_recording", sid_specs, "FHD 1920 x 1080 at 30 fps", "1920 x 1080 at 30 fps"),
        field("battery_capacity", sid_specs, "5,100 mAh typical", 5100, key="batteryMah", unit="mAh"),
        field("dimensions", sid_specs, "212.5 x 124.7 x 8.0 mm", "212.5 x 124.7 x 8.0 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "371 g", 371, key="weightG", unit="g"),
        field("cellular_bands", sid_specs, "LTE FDD bands 1/2/3/4/5/7/8/12/17/20/28/66; LTE TDD 38/40; 3G and GSM bands listed on source page", "LTE FDD 1/2/3/4/5/7/8/12/17/20/28/66; LTE TDD 38/40", key="cellular"),
        field("tablet_cellular_variant", sid_specs, "LTE model", "LTE"),
        field("wifi", sid_specs, "802.11 a/b/g/n/ac, 2.4 GHz + 5 GHz", "Wi-Fi 5", key="wifi"),
        field("bluetooth", sid_specs, "Bluetooth 5.0", "Bluetooth 5.0"),
        field("usb", sid_specs, "USB Type-C, USB 2.0", "USB Type-C; USB 2.0", key="ports"),
        field("sim_esim", sid_specs, "LTE nano-SIM model; eSIM not listed", "Nano-SIM; no eSIM listed", key="sim"),
        field("gnss", sid_specs, "GPS / GLONASS / BeiDou / Galileo", "GPS, GLONASS, BeiDou, Galileo"),
        field("audio", sid_specs, "Stereo dual speakers with Dolby Atmos; 3.5 mm stereo jack", "Stereo dual speakers; Dolby Atmos; 3.5 mm jack", key="sound"),
        field("sensors", sid_specs, "Accelerometer, geomagnetic sensor, light sensor", "Accelerometer; geomagnetic; light sensor"),
        field("philippine_release_date", sid_promo, "Samsung PH promotion was valid June 18–20 and June 25–27, 2021; it does not state first sale.", None,
              status="PENDING_VERIFICATION", note="The promotion confirms local availability in June 2021 but does not establish the first authorized-sale date."),
        field("current_price_php", sid_promo, "Gray / Silver LTE SKU SRP PHP 9,490; separate token promo could reduce checkout amount conditionally.", 9490,
              unit="PHP", price_condition="new", price_type="Historical official Philippine SRP (June 2021; not a current offer)",
              price_observed="2021-06-25",
              note="Historical SRP listed by Samsung Philippines. The page separately describes a conditional PHP 1,000 non-cash token promotion; PHP 8,490 is not represented as the standard price."),
    ]
    replacements = [
        {"id": device + "-lte-gray-3-32", "label": "LTE · 3 GB RAM / 32 GB storage · Gray", "sku": "SM-T225NZAAXTC", "modelCode": "SM-T225",
         "notes": "Exact Philippine Gray SKU from Samsung Philippines; SRP and specifications are dated source observations."},
        {"id": device + "-lte-silver-3-32", "label": "LTE · 3 GB RAM / 32 GB storage · Silver", "sku": "SM-T225NZSAXTC", "modelCode": "SM-T225",
         "notes": "Exact Philippine Silver SKU from Samsung Philippines; same memory/connectivity configuration as Gray."},
    ]
    for index, (item, ram, storage, color, sku) in enumerate([
        (replacements[0], 3, 32, "Gray", "SM-T225NZAAXTC"),
        (replacements[1], 3, 32, "Silver", "SM-T225NZSAXTC"),
    ]):
        sku_source = sid_specs if color == "Gray" else sid_silver
        fields = [field("model_number", sku_source, sku, sku),
                  field("configuration", sku_source, f"LTE; {ram} GB RAM / {storage} GB storage; {color} ({sku})", f"LTE · {ram} GB / {storage} GB · {color}"),
                  field("ram_capacity", sid_specs, f"{ram} GB", ram, key="ramGb", unit="GB"),
                  field("storage_capacity", sid_specs, f"{storage} GB", storage, key="storageGb", unit="GB"),
                  *base]
        out.append(record(device, item["id"], "Samsung", "Galaxy Tab A7 Lite", item["label"], sources, fields,
                          replacements=replacements if index == 0 else None,
                          availability={"verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                                        "availabilityStatus": "Samsung Philippines promotion and product pages identify LTE model codes and Philippine SRP in June 2021.",
                                        "philippineAvailability": "Philippine LTE SKUs and local price are confirmed; first authorized-sale date and present stock are not established.",
                                        "observedAt": OBSERVED,
                                        "qualityFlag": "First Philippine sale date not recorded"} if index == 0 else None))
        if index == 0:
            device_row = next(d for d in json.loads(CATALOG.read_text(encoding="utf-8")) if d["id"] == device)
            device_row["variants"] = [{"id": variant["id"], "specs": {}} for variant in replacements]
            setattr(record, "_catalog_override_" + device, device_row)

    # Xiaomi Pad 5: globally documented 6/128 and 6/256 configurations; no local sale evidence is inferred.
    device = "device_eb3d0871ddd09e"
    specs = "https://www.mi.com/ae-en/product/xiaomi-pad-5/specs/"
    faq = "https://www.mi.com/global/support/faq/details/KA-07774/"
    sid_specs, sid_faq = "xiaomi_pad_5_uae_specs", "xiaomi_pad_5_global_faq"
    sources = [
        src(sid_specs, "Xiaomi United Arab Emirates", specs, "Official regional product specifications",
            "Official Xiaomi specification page lists both 6 GB + 128 GB and 6 GB + 256 GB configurations and shared device specifications. It does not establish Philippine sale or pricing."),
        src(sid_faq, "Xiaomi Global Support", faq, "Official manufacturer FAQ on connectivity and battery",
            "Official global FAQ confirms model-level connectivity limitations and battery/charging details; regional offer and availability remain unverified."),
    ]
    variants = [(device + "-6-128-global", "6 GB RAM / 128 GB storage (global source configuration)", 128),
                (device + "-6-256-global", "6 GB RAM / 256 GB storage (global source configuration)", 256)]
    base = [
        field("display_size", sid_specs, "11 inches", 11, key="displayInches", unit="in"),
        field("display_resolution", sid_specs, "2560 x 1600", "2560 x 1600", key="resolution"),
        field("display_refresh_rate", sid_specs, "120 Hz", 120, key="refreshHz", unit="Hz"),
        field("display_brightness", sid_specs, "500 nits typical", "500 nits typical", unit="nits"),
        field("chipset", sid_specs, "Qualcomm Snapdragon 860", "Snapdragon 860", key="chipset"),
        field("ram_type", sid_specs, "LPDDR4X", "LPDDR4X", key="ramType"),
        field("storage_type", sid_specs, "UFS 3.1", "UFS 3.1", key="storageType"),
        field("rear_camera_system", sid_specs, "13 MP rear camera", "13 MP rear camera"),
        field("front_camera", sid_specs, "8 MP", 8, key="frontCameraMp", unit="MP"),
        field("video_recording", sid_specs, "Rear up to 4K at 30 fps; front up to 1080p at 30 fps", "Rear up to 4K/30 fps; front up to 1080p/30 fps"),
        field("battery_capacity", sid_specs, "8,720 mAh typical", 8720, key="batteryMah", unit="mAh"),
        field("dimensions", sid_specs, "254.69 x 166.25 x 6.85 mm", "254.69 x 166.25 x 6.85 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "511 g", 511, key="weightG", unit="g"),
        field("wifi", sid_specs, "802.11 a/b/g/n/ac", "Wi-Fi 5", key="wifi"),
        field("bluetooth", sid_specs, "Bluetooth 5.0", "Bluetooth 5.0"),
        field("usb", sid_specs, "USB Type-C", "USB Type-C", key="ports"),
        field("audio", sid_specs, "Four speakers with Dolby Atmos", "Four speakers; Dolby Atmos", key="sound"),
        field("tablet_cellular_variant", sid_faq, "Wi-Fi tablet; does not support a SIM card or eSIM", "Wi-Fi only", key="cellular"),
        field("sim_esim", sid_faq, "No SIM or eSIM support", "No SIM / eSIM", key="sim"),
    ]
    replacements = [{"id": vid, "label": label, "sku": None, "modelCode": None,
                     "notes": "Manufacturer global/UAE specification page lists this memory/storage configuration. Philippine market availability is not verified."}
                    for vid, label, _ in variants]
    for index, (vid, label, storage) in enumerate(variants):
        fields = [field("configuration", sid_specs, f"6 GB + {storage} GB", f"6 GB RAM / {storage} GB storage"),
                  field("ram_capacity", sid_specs, "6 GB", 6, key="ramGb", unit="GB"),
                  field("storage_capacity", sid_specs, f"{storage} GB", storage, key="storageGb", unit="GB"),
                  field("operating_system", sid_specs, "MIUI for Pad", "MIUI for Pad", key="os"),
                  *base,
                  pending("philippine_release_date", sid_specs, "No Philippine launch or authorized-sale evidence was found in these sources.",
                          "Global technical specifications do not establish Philippine market release."),
                  pending("official_launch_price_php", sid_specs, "No Philippine price is stated in the cited sources.",
                          "Do not convert foreign-market prices to PHP."),
                  pending("current_price_php", sid_specs, "No dated Philippine price observation in the cited sources.",
                          "Foreign-market price pages are not a Philippine price source.")]
        out.append(record(device, vid, "Xiaomi", "Pad 5", label, sources, fields,
                          replacements=replacements if index == 0 else None))
        if index == 0:
            device_row = next(d for d in json.loads(CATALOG.read_text(encoding="utf-8")) if d["id"] == device)
            device_row["variants"] = [{"id": variant["id"], "specs": {}} for variant in replacements]
            setattr(record, "_catalog_override_" + device, device_row)

    # Nokia T20: international HMD specifications; preserve global configuration and no Philippine sale claim.
    device = "device_1352c430fa0bb9"
    specs = "https://www.hmd.com/en_int/nokia-t-20/specs"
    release = "https://www.hmd.com/en_int/press/introducing-the-new-nokia-t-20-tablet"
    sid_specs, sid_press = "nokia_t20_hmd_global_specs", "nokia_t20_global_launch"
    sources = [
        src(sid_specs, "HMD", specs, "Official international model specifications",
            "HMD's international Nokia T20 specifications describe the global 4 GB + 64 GB page configuration, Wi-Fi/LTE distinctions, and technical specifications. Other regions may have different memory, bands, and weight."),
        src(sid_press, "HMD", release, "Global product introduction date",
            "HMD global press release dated 6 October 2021 announces Nokia T20 globally; this is not a Philippine launch date.", "2021-10-06"),
    ]
    config = device + "-4-64-global"
    fields = [
        field("configuration", sid_specs, "4 GB RAM + 64 GB storage (HMD international spec page)", "4 GB RAM / 64 GB storage"),
        pending("philippine_release_date", sid_press, "HMD global announcement is dated 6 October 2021; no Philippine launch/first-sale evidence is provided.",
                "Do not use global launch date as Philippine release date."),
        field("display_size", sid_specs, "10.4 inches", 10.4, key="displayInches", unit="in"),
        field("display_resolution", sid_specs, "In-cell 2K 1200 x 2000", "1200 x 2000", key="resolution"),
        field("display_brightness", sid_specs, "400 nits typical", "400 nits typical", unit="nits"),
        field("front_camera", sid_specs, "5 MP fixed focus", 5, key="frontCameraMp", unit="MP"),
        field("rear_camera_system", sid_specs, "8 MP autofocus rear camera", "8 MP autofocus rear camera"),
        field("battery_capacity", sid_specs, "8,200 mAh", 8200, key="batteryMah", unit="mAh"),
        field("wired_charging", sid_specs, "15 W USB-PD compatible; 10 W charger supplied", 15, key="chargingW", unit="W",
              note="Manufacturer states USB-PD 15 W compatibility and a 10 W inbox charger; catalog figure records the supported charging standard, not bundled-adapter output."),
        field("operating_system", sid_specs, "Android 11", "Android 11", key="os"),
        field("os_support", sid_specs, "2 years of OS upgrades; 3 years monthly security updates, optional fourth year for Enterprise", "2 OS upgrade years; 3 years monthly security updates; optional enterprise year"),
        field("storage_expansion", sid_specs, "microSD up to 512 GB", "microSD up to 512 GB"),
        field("tablet_cellular_variant", sid_specs, "Wi-Fi-only and LTE variants exist; LTE version uses Nano-SIM", "Wi-Fi-only and LTE variants exist"),
        field("sim_esim", sid_specs, "Nano-SIM for LTE data version; no standard calls or SMS; Wi-Fi-only model has no SIM", "Nano-SIM on LTE variant; no standard calls/SMS", key="sim"),
        field("cellular_bands", sid_specs, "International LTE bands 1/3/5/7/8/20/28 and TDD 38/40/41; bands vary by region", "International LTE 1/3/5/7/8/20/28; TDD 38/40/41"),
        field("wifi", sid_specs, "Dual-band 2.4 / 5 GHz Wi-Fi", "Dual-band Wi-Fi", key="wifi"),
        field("usb", sid_specs, "USB Type-C (USB 2.0)", "USB Type-C; USB 2.0", key="ports"),
        field("audio", sid_specs, "Stereo speakers with amplifier; 3.5 mm headphone jack; OZO Audio", "Stereo speakers; 3.5 mm jack; OZO Audio", key="sound"),
        field("dimensions", sid_specs, "247.6 x 157.5 x 7.8 mm", "247.6 x 157.5 x 7.8 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "470 g LTE / 465 g Wi-Fi-only", "470 g LTE / 465 g Wi-Fi-only", unit="g",
              note="Regional/model variants differ; no single weight assigned to the unconfirmed Philippine configuration."),
        field("ingress_protection", sid_specs, "IP52", "IP52"),
        field("sensors", sid_specs, "Accelerometer, ambient light, Hall", "Accelerometer; ambient light; Hall"),
        pending("current_price_php", sid_specs, "No Philippine price is stated in the international specifications.",
                "Do not convert international or third-party prices to PHP."),
    ]
    out.append(record(device, config, "Nokia", "T20", "4 GB RAM / 64 GB storage (global source configuration)",
                      sources, fields,
                      replacements=[{"id": config, "label": "4 GB RAM / 64 GB storage (global source configuration)", "sku": None,
                                     "modelCode": None, "notes": "HMD international page's configuration; Philippine market SKU and availability are unverified."}]))

    # realme Pad: Philippine-localized manufacturer specifications but no exact configuration pairing or dated sale.
    device = "device_23b53732758d44"
    specs = "https://www.realme.com/ph/realme-pad/specs"
    sid_specs = "realme_pad_ph_official_specs"
    sources = [src(sid_specs, "realme Philippines", specs, "Official Philippines-localized technical specifications",
                   "The official realme Philippines product specification page lists device-level specifications, memory/storage ranges, and an optional 4G version. It does not document exact RAM/storage pairings, local first-sale date, or a dated Philippine price.")]
    fields = [
        field("model_number", sid_specs, "The official page does not provide a distinct regional SKU/model code.", None, status="PENDING_VERIFICATION"),
        pending("configuration", sid_specs, "Page lists 3/4 GB RAM, 32/64 GB ROM, and says 'up to 4+64GB'; exact pairings are not enumerated.",
                "Do not infer that only 3+32 and 4+64 combinations exist."),
        field("display_size", sid_specs, "10.4 inches", 10.4, key="displayInches", unit="in"),
        field("display_technology", sid_specs, "LCD", "LCD", key="displayType"),
        field("display_resolution", sid_specs, "2000 x 1200", "2000 x 1200", key="resolution"),
        field("display_brightness", sid_specs, "360 nits typical", "360 nits typical", unit="nits"),
        field("chipset", sid_specs, "MediaTek Helio G80", "Helio G80", key="chipset"),
        field("process_node", sid_specs, "12 nm", 12, unit="nm"),
        field("cpu", sid_specs, "Octa-core: 2 x Cortex-A75 at 2.0 GHz + 6 x Cortex-A55 at 1.8 GHz", "2x Cortex-A75 2.0 GHz + 6x Cortex-A55 1.8 GHz"),
        field("gpu", sid_specs, "Mali-G52 at 950 MHz", "Mali-G52", key="gpu"),
        field("ram_capacity", sid_specs, "3 GB / 4 GB (configuration-specific pairing not recorded)", "3 GB or 4 GB; pairing not recorded", unit="GB"),
        field("storage_capacity", sid_specs, "32 GB / 64 GB (configuration-specific pairing not recorded)", "32 GB or 64 GB; pairing not recorded", unit="GB"),
        field("storage_expansion", sid_specs, "Memory expansion up to 1 TB", "microSD up to 1 TB"),
        field("rear_camera_system", sid_specs, "8 MP rear camera", "8 MP rear camera"),
        field("front_camera", sid_specs, "8 MP front camera, 105-degree wide angle", 8, key="frontCameraMp", unit="MP"),
        field("battery_capacity", sid_specs, "7,100 mAh typical", 7100, key="batteryMah", unit="mAh"),
        field("wired_charging", sid_specs, "18 W Quick Charge", 18, key="chargingW", unit="W"),
        field("wireless_charging", sid_specs, "Reverse charging supported", "Reverse charging supported"),
        field("dimensions", sid_specs, "246.1 x 155.9 x 6.9 mm", "246.1 x 155.9 x 6.9 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "440 g", 440, key="weightG", unit="g"),
        field("tablet_cellular_variant", sid_specs, "A 4G version is available; exact Philippine configuration is not identified.", "4G version available; local variant unspecified"),
        field("cellular_bands", sid_specs, "4G version bands: GSM 850/900/1800/1900; WCDMA 1/5/8; FDD-LTE 1/3/5/7/8/20/28; TDD-LTE 38/40/41", "GSM 850/900/1800/1900; WCDMA 1/5/8; LTE FDD 1/3/5/7/8/20/28; LTE TDD 38/40/41"),
        field("wifi", sid_specs, "Wi-Fi 5 (802.11 a/b/g/n/ac), 2.4/5 GHz", "Wi-Fi 5", key="wifi"),
        field("bluetooth", sid_specs, "Bluetooth 5.0", "Bluetooth 5.0"),
        field("audio", sid_specs, "Stereo quad speakers; Dolby Atmos; Hi-Res Audio", "Quad speakers; Dolby Atmos; Hi-Res Audio", key="sound"),
        field("sensors", sid_specs, "Light, acceleration, Hall, and gyroscope sensors", "Light; acceleration; Hall; gyroscope"),
        field("gnss", sid_specs, "GPS/AGPS, BeiDou, GLONASS", "GPS/AGPS, BeiDou, GLONASS"),
        field("operating_system", sid_specs, "realme UI for Pad based on Android 11", "realme UI for Pad; Android 11", key="os"),
        pending("philippine_release_date", sid_specs, "Philippine-localized specifications page does not state launch or first authorized sale date.",
                "A local-language specification page alone is not sale-date evidence."),
        pending("current_price_php", sid_specs, "No dated Philippine price is stated on the specifications page.",
                "No price is inferred from memory or third-party listings."),
    ]
    out.append(record(device, device + "-unrecorded", "realme", "Pad", "Configuration not recorded", sources, fields))

    # TCL TAB 10S: global technical specs; preserve unrecorded variant because the page's network SKU is not tied to RAM/storage.
    device = "device_59bc941c580cee"
    specs = "https://www.tcl.com/global/en/tablets/tcl-tab-10s/specifications"
    sid_specs = "tcl_tab_10s_global_specs"
    sources = [src(sid_specs, "TCL Global", specs, "Official global model specifications",
                   "TCL's global product page lists 3 GB + 32 GB memory and a separately described LTE version; it does not tie each network version to a local Philippine SKU or establish Philippine sale.")]
    fields = [
        pending("philippine_release_date", sid_specs, "Global product page does not establish Philippine launch or authorized-sale date.",
                "Global specifications do not establish Philippine market availability."),
        field("configuration", sid_specs, "Global page lists 3 GB RAM + 32 GB storage, but no exact Philippine SKU is identified.", "3 GB RAM / 32 GB storage (global listing; PH SKU unknown)"),
        field("display_size", sid_specs, "10.1 inches", 10.1, key="displayInches", unit="in"),
        field("display_resolution", sid_specs, "1200 x 1920", "1200 x 1920", key="resolution"),
        field("chipset", sid_specs, "MediaTek MT8768", "MediaTek MT8768", key="chipset"),
        field("cpu", sid_specs, "Octa-core: 4 x Cortex-A53 2.0 GHz + 4 x Cortex-A53 1.5 GHz", "4x Cortex-A53 2.0 GHz + 4x Cortex-A53 1.5 GHz"),
        field("gpu", sid_specs, "PowerVR GE8320 at 650 MHz", "PowerVR GE8320", key="gpu"),
        field("operating_system", sid_specs, "Android 10", "Android 10", key="os"),
        field("ram_capacity", sid_specs, "3 GB RAM", 3, key="ramGb", unit="GB"),
        field("storage_capacity", sid_specs, "32 GB ROM", 32, key="storageGb", unit="GB"),
        field("storage_expansion", sid_specs, "microSD up to 256 GB", "microSD up to 256 GB"),
        field("rear_camera_system", sid_specs, "8 MP autofocus rear camera", "8 MP autofocus rear camera"),
        field("front_camera", sid_specs, "5 MP fixed-focus", 5, key="frontCameraMp", unit="MP"),
        field("video_recording", sid_specs, "Rear and front video capture up to 1080p at 30 fps", "1080p/30 fps"),
        field("battery_capacity", sid_specs, "8,000 mAh typical", 8000, key="batteryMah", unit="mAh"),
        field("wired_charging", sid_specs, "Supports 9 V / 2 A maximum (18 W); bundled charger also lists 5 V / 2 A", 18, key="chargingW", unit="W"),
        field("dimensions", sid_specs, "241 x 158.6 x 8.3 mm", "241 x 158.6 x 8.3 mm", key="dimensions", unit="mm"),
        field("weight", sid_specs, "490 g", 490, key="weightG", unit="g"),
        field("cellular_bands", sid_specs, "The page documents an LTE version and lists its GSM/WCDMA/TD-SCDMA/LTE bands; exact Philippine model version is not identified.", "LTE variant documented; Philippine bands unverified"),
        field("wifi", sid_specs, "802.11 a/b/g/n/ac", "Wi-Fi 5", key="wifi"),
        field("bluetooth", sid_specs, "Bluetooth 5.0", "Bluetooth 5.0"),
        field("usb", sid_specs, "USB Type-C, USB 2.0", "USB Type-C; USB 2.0", key="ports"),
        field("audio", sid_specs, "Two speakers and two microphones", "2 speakers; 2 microphones", key="sound"),
        field("sensors", sid_specs, "GPS, G-sensor, Hall switch, light sensor, proximity sensor", "GPS; G-sensor; Hall; light; proximity"),
        pending("current_price_php", sid_specs, "No Philippine price is stated in the cited source.", "Do not infer a local price from a global product page."),
    ]
    out.append(record(device, device + "-unrecorded", "TCL", "TAB 10S", "Configuration not recorded", sources, fields))

    # Inventory label does not match a confirmed official 2021 Huawei model-year name; do not borrow 2020/2022 specs.
    device = "device_e82e93c423ed2a"
    support = "https://consumer.huawei.com/ph/support/content/en-us15819846/"
    stylus = "https://consumer.huawei.com/ph/support/content/en-us00737675/"
    sid_support, sid_stylus = "matepad_104_year_identity_ph", "matepad_104_year_identity_stylus"
    sources = [
        src(sid_support, "HUAWEI Support Philippines", support, "Model-year and model-code cross-check",
            "Official support material names MatePad 10.4-inch 2020 (BAH3) and MatePad 10.4-inch 2022 (BAH4); it does not confirm the inventory's claimed 2021 edition."),
        src(sid_stylus, "HUAWEI Support Philippines", stylus, "Manufacturer product-family identity cross-check",
            "HUAWEI's support index separately lists the 2020 and 2022 MatePad 10.4 model-year families."),
    ]
    fields = [
        pending("model_number", sid_support, "No official source located that confirms a distinct MatePad 10.4 (2021) model; official support lists 2020 BAH3 and 2022 BAH4.",
                "Keep this workbook identity unresolved; do not copy specifications from the 2020 or 2022 products."),
        pending("philippine_release_date", sid_support, "Claimed 2021 model identity and Philippine release date remain unresolved.",
                "A release date must not be inferred from adjacent product years."),
    ]
    out.append(record(device, device + "-unrecorded", "Huawei", "MatePad 10.4 (2021)", "Configuration not recorded", sources, fields))

    return out


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = records()
    for item in items:
        # For multi-configuration replacements, expose the target IDs to the existing review merge helper.
        override = getattr(record, "_catalog_override_" + item["deviceId"], None)
        if override:
            target = next(d for d in catalog if d["id"] == item["deviceId"])
            target["variants"] = override["variants"]
        add_review(manual, catalog, item)
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewedTabletConfigurations": len(items), "models": len({i['deviceId'] for i in items}),
                      "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
