#!/usr/bin/env python3
"""Review the Philippine Huawei MatePad Pro 11 (2022) Wi-Fi configuration."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-26"
DEVICE = "device_070c7fa225849f"
CONFIG = f"{DEVICE}-8gb-256gb-wifi-got-w29"

URL_HUAWEI_SPECS = "https://consumer.huawei.com/ru/tablets/matepad-pro-11/specs/"
URL_HUAWEI_PH_CONFIG = "https://consumer.huawei.com/ph/support/content/en-us15907947/"
URL_HUAWEI_PH_LAUNCH = "https://consumer.huawei.com/ph/community/details/topicId-182067/"
URL_HUAWEI_PH_PENCIL = "https://consumer.huawei.com/ph/support/content/en-us00737675/"
URL_HUAWEI_PH_KEYBOARD = "https://consumer.huawei.com/ph/support/content/en-us15905486/"
URL_YUGA_LAUNCH = "https://www.yugatech.com/news/huawei-matepad-pro-11-priced-in-the-philippines/"
URL_YUGA_SPECS = "https://www.yugatech.com/spec/huawei-matepad-pro-11/"
URL_DATABLITZ = "https://ecommerce.datablitz.com.ph/products/huawei-matepad-pro-wifi-11-2-560x1-600-oled-120hz-8gb-256gb-harmonyos-3-got-w29-golden-black"


SOURCES = [
    {"id": "huawei_matepad_pro_11_2022_official_specs", "publisher": "HUAWEI Russia",
     "url": URL_HUAWEI_SPECS, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Manufacturer specifications for the exact GOT-W29 Wi-Fi hardware branch",
     "note": "Huawei's specifications distinguish GOT-W29 from GOT-AL09. GOT-W29 is the Wi-Fi model with Snapdragon 870, Adreno 650, Bluetooth 5.1, 40 W SuperCharge, 449 g weight, and the listed W29-specific network profile. Model-level display, camera, battery, USB, audio, and sensor fields are also taken from this official page."},
    {"id": "huawei_matepad_pro_11_ph_supported_configs", "publisher": "HUAWEI Support Philippines",
     "url": URL_HUAWEI_PH_CONFIG, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Philippine-supported product and memory configurations",
     "note": "The Philippine support page explicitly includes MatePad Pro 11-inch 2022 Wi-Fi 8 GB + 256 GB. It also lists separate 8 GB + 128 GB Wi-Fi and 8 GB + 256 GB LTE variants; only the Wi-Fi 8 GB + 256 GB Philippine launch configuration is used here."},
    {"id": "huawei_matepad_pro_11_ph_preorder", "publisher": "HUAWEI Philippines Community",
     "url": URL_HUAWEI_PH_LAUNCH, "publicationDate": "2022-09-01", "accessDate": OBSERVED,
     "purpose": "Official Philippine preorder window and local launch details",
     "note": "Huawei Philippines says the preorder promotion ran September 2–8, 2022. The window confirms local preorder availability; the notice does not establish the general retail delivery date."},
    {"id": "huawei_matepad_pro_11_ph_stylus", "publisher": "HUAWEI Support Philippines",
     "url": URL_HUAWEI_PH_PENCIL, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Official Philippine stylus compatibility",
     "note": "Huawei lists the MatePad Pro 11-inch 2022 GOT family as compatible with M-Pencil (2nd generation). The Philippine preorder offer also included the 2nd-generation pencil as a promotion accessory."},
    {"id": "huawei_matepad_pro_11_ph_keyboard", "publisher": "HUAWEI Support Philippines",
     "url": URL_HUAWEI_PH_KEYBOARD, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Official Philippine keyboard compatibility and model-family cross-check",
     "note": "Huawei's support article identifies the MatePad Pro 11-inch 2022 model family as GOT and documents its compatible Smart Magnetic Keyboard."},
    {"id": "yugatech_matepad_pro_11_ph_launch", "publisher": "YugaTech",
     "url": URL_YUGA_LAUNCH, "publicationDate": "2022-09-01", "accessDate": OBSERVED,
     "purpose": "Contemporaneous Philippine launch, preorder price, and local feature cross-check",
     "note": "YugaTech reports the Philippine Wi-Fi launch configuration, PHP 41,999 preorder price for September 2–8, authorized sales channels, and local device details. Price is retained as a historical preorder-price observation, not a current offer or separately confirmed MSRP."},
    {"id": "yugatech_matepad_pro_11_specs", "publisher": "YugaTech",
     "url": URL_YUGA_SPECS, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Independent Philippine specification cross-check",
     "note": "YugaTech's MatePad Pro 11 specification page corroborates the Wi-Fi model's 40 W SuperCharge and core hardware specifications."},
    {"id": "datablitz_matepad_pro_11_got_w29", "publisher": "DataBlitz",
     "url": URL_DATABLITZ, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Philippine retailer SKU / configuration cross-check",
     "note": "The Philippine retailer product listing identifies an 8 GB + 256 GB Wi-Fi unit with model code GOT-W29. Huawei's official regional specification page separately defines the W29 hardware branch; the retailer listing is used only to connect that code to a local product listing."},
]


def f(fid: str, source_id: str, value, normalized=None, *, status="VERIFIED",
      key=None, unit=None, note=None, price_condition=None, price_type=None,
      price_observed=None):
    row = {"fieldId": fid, "status": status, "sourceId": source_id,
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


def pending(fid: str, note: str, source_id= "huawei_matepad_pro_11_2022_official_specs"):
    return f(fid, source_id, "Not recorded in the reviewed model-matched sources.", None,
             status="PENDING_VERIFICATION", note=note)


def undisclosed(fid: str, note: str, source_id="huawei_matepad_pro_11_2022_official_specs"):
    return f(fid, source_id, "Not stated in the reviewed manufacturer and Philippine launch specifications.", None,
             status="NOT_DISCLOSED", note=note)


def common_fields() -> list[dict]:
    h = "huawei_matepad_pro_11_2022_official_specs"
    y = "yugatech_matepad_pro_11_ph_launch"
    display_protection = f("display_protection", y, "YugaTech reports TÜV Rheinland Full Care Display 3.0 certification; no cover-glass type is stated.", None,
                           status="NOT_DISCLOSED", note="The certification is recorded in the source, but it does not identify a protective glass material. No glass type is assigned.")
    display_protection["replaceExisting"] = True
    return [
        f("model_number", "datablitz_matepad_pro_11_got_w29",
          "Retailer lists GOT-W29; Huawei support identifies the Philippine model family as GOT.", "GOT-W29",
          status="VERIFIED_SECONDARY", note="Exact SKU code comes from the Philippine retailer listing. Huawei's primary spec page confirms GOT-W29 is the Wi-Fi hardware branch."),
        f("configuration", "huawei_matepad_pro_11_ph_supported_configs", "11-inch 2022 Wi-Fi, 8 GB RAM + 256 GB storage", "8 GB RAM / 256 GB storage / Wi-Fi",
          status="VERIFIED", note="Huawei Philippines explicitly lists this configuration; local launch reporting says this was the Philippine launch variant."),
        f("philippine_release_date", "huawei_matepad_pro_11_ph_preorder", "Philippine preorder promotion: September 2–8, 2022; first general retail sale date not stated.", "2022-09-02",
          status="VERIFIED", note="This is the start of Huawei Philippines' authorized preorder window, not a claimed shipment or general-retail date."),
        f("official_launch_price_php", y, "PHP 41,999 reported preorder price; source does not explicitly label this an SRP.", None,
          status="PENDING_VERIFICATION", unit="PHP", note="Keep official MSRP unresolved. The dated amount is separately recorded as the historical local preorder-price observation."),
        f("current_price_php", y, "PHP 41,999 Philippine preorder price, September 2–8, 2022.", 41999,
          status="VERIFIED_SECONDARY", unit="PHP", note="Historical preorder-price observation; the source also describes promotional accessories. This is not a current offer and is not asserted as a standalone MSRP.",
          price_condition="new", price_type="Historical Philippine preorder price (not current)", price_observed="2022-09-02"),
        f("display_size", h, "11 inches", 11, key="displayInches", unit="in"),
        f("display_technology", h, "OLED", "OLED", key="displayType"),
        f("display_resolution", h, "WQXGA 2560 × 1600", "2560 x 1600", key="resolution"),
        f("display_refresh_rate", h, "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", y, "600 nits peak brightness", 600, status="VERIFIED_SECONDARY", unit="nits",
          note="Contemporaneous Philippine launch specifications give a 600-nit peak figure; this value is sourced to YugaTech rather than the opened Huawei spec table."),
        display_protection,
        f("chipset", h, "Qualcomm Snapdragon 870 Mobile Platform (GOT-W29)", "Qualcomm Snapdragon 870", key="chipset"),
        undisclosed("process_node", "The reviewed Huawei specification page names the chipset but does not state its manufacturing process."),
        f("cpu", h, "1 × Cortex-A77 3.2 GHz + 3 × Cortex-A77 2.42 GHz + 4 × Cortex-A55 1.8 GHz",
          "1x Cortex-A77 3.2 GHz + 3x Cortex-A77 2.42 GHz + 4x Cortex-A55 1.8 GHz", key="cpu"),
        f("gpu", h, "Adreno 650 (GOT-W29)", "Adreno 650", key="gpu"),
        f("operating_system", h, "HarmonyOS 3", "HarmonyOS 3", key="os"),
        undisclosed("os_support", "A model-specific OS/security update schedule is not published in the reviewed sources."),
        f("ram_capacity", "huawei_matepad_pro_11_ph_supported_configs", "8 GB RAM", 8, key="ramGb", unit="GB"),
        undisclosed("ram_type", "The reviewed exact-configuration sources do not identify RAM type or speed."),
        f("storage_capacity", "huawei_matepad_pro_11_ph_supported_configs", "256 GB internal storage", 256, key="storageGb", unit="GB"),
        undisclosed("storage_type", "The reviewed manufacturer specification lists capacity but not the internal storage interface/type."),
        undisclosed("storage_expansion", "No supported memory-card expansion is stated on the reviewed model-matched specifications."),
        f("rear_camera_system", h, "13 MP f/1.8 autofocus main camera + 8 MP f/2.2 fixed-focus ultra-wide camera",
          "13 MP main + 8 MP ultra-wide rear cameras"),
        f("main_camera_sensor", h, "13 MP f/1.8 autofocus main camera; sensor make/model not stated.", "13 MP f/1.8 autofocus; sensor make/model not disclosed"),
        f("ultrawide_camera", h, "8 MP f/2.2 fixed-focus ultra-wide rear camera", "8 MP f/2.2 fixed-focus", unit="MP"),
        f("telephoto_camera", h, "The published rear-camera system lists main and ultra-wide cameras only.", "No telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", h, "16 MP f/2.2 fixed-focus front camera", 16, key="frontCameraMp", unit="MP"),
        f("video_recording", h, "Rear video up to 3840 × 2160; front video up to 1920 × 1080.", "Rear up to 3840 x 2160; front up to 1920 x 1080"),
        f("battery_capacity", h, "8,300 mAh typical; 8,200 mAh rated", 8300, key="batteryMah", unit="mAh",
          note="Catalog capacity uses Huawei's typical value; the manufacturer separately states 8,200 mAh rated capacity."),
        f("battery_technology", h, "Built-in, non-removable battery; chemistry not stated.", "Built-in, non-removable; chemistry not disclosed"),
        f("wired_charging", h, "GOT-W29 supports HUAWEI SuperCharge up to 40 W; 40 W adapter/cable sold separately.", 40, key="chargingW", unit="W"),
        f("wireless_charging", h, "USB OTG reverse wired charging up to 5 V / 1.5 A; wireless charging not stated.", "Reverse wired charging via USB OTG; wireless charging not disclosed"),
        f("dimensions", h, "160.38 × 249.23 × 5.9 mm", "160.38 x 249.23 x 5.9", key="dimensions", unit="mm"),
        f("weight", h, "Approximately 449 g for GOT-W29", 449, key="weightG", unit="g"),
        undisclosed("materials", "Frame and rear-cover materials are not identified in the reviewed exact-model specifications."),
        undisclosed("ingress_protection", "No IP ingress-protection rating is stated in the reviewed sources."),
        f("sim_esim", "huawei_matepad_pro_11_ph_supported_configs", "Philippine launch configuration is Wi-Fi only; no SIM/eSIM variant.", "Not applicable to Wi-Fi-only configuration", status="NOT_APPLICABLE"),
        f("cellular_bands", "huawei_matepad_pro_11_ph_supported_configs", "Wi-Fi-only Philippine launch configuration; cellular bands do not apply.", "Not applicable to Wi-Fi-only configuration", status="NOT_APPLICABLE"),
        f("wifi", h, "IEEE 802.11 a/b/g/n/ac/ax, 2.4 GHz and 5 GHz; GOT-W29 supports HE80.", "802.11 a/b/g/n/ac/ax; 2.4/5 GHz", key="wifi"),
        f("bluetooth", h, "Bluetooth 5.1 (GOT-W29)", "Bluetooth 5.1"),
        f("usb", h, "USB Type-C; USB 3.1 Gen 1 support requires a compatible separately purchased cable; bundled cable is USB 2.0.", "USB Type-C; USB 3.1 Gen 1 capable; bundled cable USB 2.0", key="ports"),
        undisclosed("nfc", "NFC is not mentioned in the reviewed model-matched specifications."),
        f("gnss", h, "GPS, GLONASS, BeiDou, Galileo, and QZSS listed for GOT-W29.", "GPS; GLONASS; BeiDou; Galileo; QZSS"),
        f("audio", h, "Six speakers; HUAWEI SOUND", "6 speakers; HUAWEI SOUND", key="sound"),
        f("sensors", h, "Ambient-light, compass, gravity, gyroscope, and Hall sensors.", "Ambient light; compass; gravity; gyroscope; Hall"),
        f("tablet_stylus", "huawei_matepad_pro_11_ph_stylus", "M-Pencil (2nd generation) supported for the GOT family.", "HUAWEI M-Pencil (2nd generation) compatible", key="stylus"),
        f("tablet_keyboard", "huawei_matepad_pro_11_ph_keyboard", "Compatible with HUAWEI Smart Magnetic Keyboard; preorder promotion included the detachable magnetic keyboard.", "HUAWEI Smart Magnetic Keyboard compatible", key="keyboard"),
        f("tablet_cellular_variant", "huawei_matepad_pro_11_ph_supported_configs", "Philippine launch configuration: Wi-Fi only, 8 GB RAM / 256 GB storage.", "Wi-Fi only", key="cellular"),
    ]


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    # Remove any earlier placeholder-only review while retaining all source evidence
    # in the replacement review below.
    manual["records"] = [row for row in manual["records"] if not (
        row.get("deviceId") == DEVICE and row.get("configurationId") == f"{DEVICE}-unrecorded"
    )]

    replacement = [{
        "id": CONFIG,
        "label": "8 GB RAM / 256 GB storage / Wi-Fi (GOT-W29)",
        "sku": None,
        "modelCode": "GOT-W29",
        "notes": "Philippine Wi-Fi configuration is named in Huawei Philippines support; the GOT-W29 SKU is cross-identified by a local retailer and Huawei's regional spec page.",
    }]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "HUAWEI Philippines preorder promotion ran September 2–8, 2022; general retail availability date not recorded.",
        "philippineAvailability": "The MatePad Pro 11 was offered through Huawei Philippines stores and authorized retail channels. The documented date is the start of the preorder window, not a confirmed general-sale or delivery date.",
        "observedAt": OBSERVED,
        "qualityFlag": "Preorder date is documented; general retail first-sale date not recorded.",
        "manufacturer": "Huawei",
        "productLine": "MatePad Pro",
        "modelNumber": "GOT",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Philippine preorder start",
        "researchNotes": "Philippine 8 GB / 256 GB Wi-Fi configuration matched to GOT-W29. Huawei's official regional specifications distinguish it from GOT-AL09 LTE hardware, so LTE chipset and 66 W charging details are not applied. Preorder timing and price are historical; general retail date and official SRP remain unconfirmed.",
        "openIssues": [{
            "issue": "General retail availability date not recorded",
            "action": "Keep the September 2, 2022 preorder start labeled as preorder availability; do not present it as the first delivery or general-sale date.",
        }],
    }
    image_asset = "https://www.yugatech.com/wp-content/uploads/2022/09/Huawei-MatePad-Pro-11-image-feature-image-720%C3%97377.png"
    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Exact-model product image was found, but no reusable license or written permission is recorded for this site.",
        "sourcePage": URL_YUGA_LAUNCH,
        "assetUrl": image_asset,
        "scope": "Exact model",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Huawei MatePad Pro 11 (2022)",
    }

    item = {
        "deviceId": DEVICE, "configurationId": CONFIG,
        "brand": "Huawei", "model": "MatePad Pro 11 (2022)",
        "configuration": "8 GB RAM / 256 GB storage / Wi-Fi (GOT-W29)",
        "sources": SOURCES, "fields": common_fields(),
        "replacementVariants": replacement,
        "availabilityEvidence": availability,
        "modelCode": "GOT-W29",
    }
    add_review(manual, catalog, item)
    review = next(row for row in manual["records"] if
                  (row["deviceId"], row["configurationId"]) == (DEVICE, CONFIG))
    review["configuration"] = item["configuration"]
    review["configurationLabel"] = item["configuration"]
    review.pop("additionalVariants", None)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": item["model"], "configuration": item["configuration"],
                      "fields": len(item["fields"]), "imageStatus": unavailable[DEVICE]["status"]}, indent=2))


if __name__ == "__main__":
    main()
