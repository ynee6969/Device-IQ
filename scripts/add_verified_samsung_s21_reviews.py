#!/usr/bin/env python3
"""Review the Philippine Galaxy S21 5G, S21+ 5G, and S21 Ultra 5G records."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_samsung_a_series_reviews import f, src  # noqa: E402
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"

PRICE_URL = "https://www.samsung.com/ph/offer/offline/2021/galaxy-s21-5g/flexi-tradeup/"
PH_LAUNCH_URL = "https://www.gadgetmatch.com/samsung-galaxy-s21-series-price-availability-philippines/"
YUGA_URL = "https://www.yugatech.com/mobile/samsung-galaxy-s21-series-galaxy-buds-pro-now-available-nationwide/"
S21_GLOBAL_URL = "https://news.samsung.com/global/make-every-day-epic-with-samsung-galaxy-s21-and-galaxy-s21plus"
ULTRA_GLOBAL_URL = "https://www.samsungmobilepress.com/articles/samsung-galaxy-s21-ultra-the-ultimate-smartphone-experience-designed-to-be-epic-in-every-way"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           published: str | None = None) -> dict:
    return src(sid, publisher, url, purpose, note, published)


def pending(field_id: str, source_id: str, note: str) -> dict:
    return f(field_id, source_id, "Not recorded in the reviewed product pages.", None,
             status="PENDING_VERIFICATION", note=note)


def sources_for(model: dict) -> list[dict]:
    code, product_url, gsm_url = model["code"], model["product_url"], model["gsm_url"]
    result = [
        source(
            f"samsung_{code.lower()}_ph_product",
            "Samsung Philippines",
            product_url,
            "Philippine SKU identity and product page",
            model["product_note"],
        ),
        source(
            "samsung_s21_ph_official_srp_2021",
            "Samsung Philippines",
            PRICE_URL,
            "Dated Philippine SRP and local model/SKU table for the S21 family",
            "Samsung Philippines' 2021 promotion lists the S21, S21+, and S21 Ultra SRPs by capacity and color-specific SKU; the SRPs are historical and are not current offers.",
            "2021-01-29",
        ),
        source(
            "gadgetmatch_s21_ph_launch_2021",
            "GadgetMatch",
            PH_LAUNCH_URL,
            "Contemporaneous Philippine launch prices and availability dates",
            "The 14 January 2021 report states the standard Galaxy S21 5G would be available from 5 February and S21+ / S21 Ultra from 29 January. Samsung Philippines' SRP table independently supports the prices and configurations.",
            "2021-01-14",
        ),
        source(
            f"gsmarena_{code.lower()}_specs",
            "GSMArena",
            gsm_url,
            "Independent exact-model technical cross-check",
            "The exact S21-series model page is used for chipset-region distinctions, GPU, storage interface, expandable-storage status, and secondary hardware details not consistently printed in local Samsung tables.",
        ),
    ]
    if model["name"] in {"Galaxy S21+ 5G", "Galaxy S21 Ultra 5G"}:
        result.append(source(
            "yugatech_s21_ph_availability_2021",
            "YugaTech",
            YUGA_URL,
            "Philippine authorized-channel availability for Galaxy S21+ and S21 Ultra",
            "YugaTech reported on 29 January 2021 that the S21+ and S21 Ultra were available through Samsung and authorized partners; the article explicitly said the standard S21's availability had not yet been announced.",
            "2021-01-29",
        ))
    if model["name"] == "Galaxy S21 Ultra 5G":
        result.append(source(
            "samsung_s21_ultra_global_specs_2021",
            "Samsung Mobile Press",
            ULTRA_GLOBAL_URL,
            "Manufacturer launch specifications for Galaxy S21 Ultra 5G",
            "Samsung's 15 January 2021 specification table documents the Ultra display, camera system, memory configurations, battery, dimensions, connectivity, and IP rating.",
            "2021-01-15",
        ))
    else:
        result.append(source(
            "samsung_s21_global_specs_2021",
            "Samsung Global Newsroom",
            S21_GLOBAL_URL,
            "Manufacturer launch specifications for Galaxy S21 and Galaxy S21+",
            "Samsung's launch specification table gives the model-specific displays, cameras, processors, RAM/storage tiers, battery, charging, software, and connectivity for S21 and S21+.",
            "2021-01-14",
        ))
    return result


def technical_fields(model: dict) -> list[dict]:
    code = model["code"]
    product = f"samsung_{code.lower()}_ph_product"
    gsm = f"gsmarena_{code.lower()}_specs"
    official = "samsung_s21_ultra_global_specs_2021" if model["name"] == "Galaxy S21 Ultra 5G" else "samsung_s21_global_specs_2021"
    # Samsung's PH S21 Ultra page is a support page that identifies the local
    # B/DS SKU. Its hardware values come from Samsung's launch specification.
    spec_source = official if model["name"] == "Galaxy S21 Ultra 5G" else product
    fields = [
        f("model_number", product, f"Philippine family model {model['model_code']}; the cited Samsung SKU is color-specific.", model["model_code"],
          note="The color-specific order code is not assigned to this color-unspecified inventory configuration."),
        f("configuration", spec_source, model["label"], model["label"]),
        f("ram_capacity", spec_source, f"{model['ram']} GB", model["ram"], key="ramGb", unit="GB"),
        f("storage_capacity", spec_source, "256 GB", 256, key="storageGb", unit="GB"),
        f("display_size", spec_source, model["display_size"], model["display_inches"], key="displayInches", unit="in"),
        f("display_technology", spec_source, "Dynamic AMOLED 2X", "Dynamic AMOLED 2X", key="displayType"),
        f("display_resolution", spec_source, model["resolution"], model["resolution_value"], key="resolution"),
        f("display_refresh_rate", spec_source, model["refresh"], 120, key="refreshHz", unit="Hz"),
        f("display_protection", spec_source, model["protection"], model["protection"]),
        f("chipset", gsm, "Exynos 2100 for the international SM-G99xB/DS model family; other regions used Snapdragon 888.", "Samsung Exynos 2100", key="chipset",
          status="VERIFIED_SECONDARY", note="Samsung's Philippine model code is the international B/DS family; GSMArena distinguishes this model from Snapdragon regional variants."),
        f("process_node", gsm, "Exynos 2100 is manufactured on a 5 nm process.", "5 nm", status="VERIFIED_SECONDARY"),
        f("cpu", official, model["cpu"], model["cpu_value"], key="cpu"),
        f("gpu", gsm, "Mali-G78 MP14 on the international Exynos 2100 variant.", "Mali-G78 MP14", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", official, "Android 11 with One UI 3.1 at launch.", "Android 11 / One UI 3.1", key="os"),
        pending("os_support", gsm, "A current published software-support schedule was not established in this model review."),
        f("ram_type", official, "LPDDR5", "LPDDR5"),
        f("storage_type", gsm, "UFS 3.1", "UFS 3.1", key="storageType", status="VERIFIED_SECONDARY"),
        f("storage_expansion", gsm, "No microSD card slot.", "No microSD card slot", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", official, model["rear_cameras"], model["main_camera_mp"], key="rearCameraMp", unit="MP",
          note="The catalog's numeric rear-camera field stores the main wide sensor; source value preserves the complete camera array."),
        f("main_camera_sensor", official, model["main_camera"], model["main_camera"]),
        f("ultrawide_camera", official, model["ultrawide"], model["ultrawide"]),
        f("telephoto_camera", official, model["telephoto"], model["telephoto"]),
        f("front_camera", official, model["front_camera"], model["front_mp"], key="frontCameraMp", unit="MP"),
        f("video_recording", official, model["video"], model["video"], key="video"),
        f("battery_capacity", official, model["battery"], model["battery_typical"], key="batteryMah", unit="mAh",
          note=f"Samsung reports {model['battery_min']} mAh rated minimum; the public field stores typical capacity."),
        pending("battery_technology", gsm, "The reviewed local manufacturer pages do not identify cell chemistry."),
        f("wired_charging", gsm, "Up to 25 W wired charging.", 25, key="chargingW", unit="W", status="VERIFIED_SECONDARY"),
        f("wireless_charging", gsm, "15 W wireless charging and reverse wireless PowerShare.", "15 W wireless; reverse wireless PowerShare", status="VERIFIED_SECONDARY"),
        f("dimensions", spec_source, model["dimensions"], model["dimensions_value"], key="dimensions", unit="mm"),
        f("weight", spec_source, f"{model['weight']} g", model["weight"], key="weightG", unit="g"),
        f("materials", gsm, model["materials"], model["materials"], status="VERIFIED_SECONDARY"),
        f("ingress_protection", spec_source, "IP68", "IP68"),
        f("sim_esim", spec_source, "Dual Nano-SIM; SIM1 + SIM2 or SIM1 + eSIM, subject to market/carrier support.", "Dual Nano-SIM / eSIM varies", key="sim"),
        f("cellular_bands", spec_source, "5G Sub-6, LTE, WCDMA, and GSM; supported bands vary by region and carrier.", "5G Sub-6; LTE; WCDMA; GSM", key="cellular"),
        f("wifi", spec_source, model["wifi"], model["wifi"], key="wifi"),
        f("bluetooth", spec_source, model["bluetooth"], model["bluetooth"]),
        f("usb", spec_source, "USB Type-C, USB 3.2 Gen 1.", "USB Type-C; USB 3.2 Gen 1", key="ports"),
        f("nfc", spec_source, "NFC supported.", "Yes"),
        f("gnss", spec_source, "GPS, GLONASS, BeiDou, and Galileo.", "GPS; GLONASS; BeiDou; Galileo"),
        f("audio", spec_source, model["audio"], model["audio"], key="sound"),
        f("sensors", spec_source, "Accelerometer, barometer, fingerprint sensor, gyroscope, geomagnetic sensor, hall sensor, light sensor, and proximity sensor.",
          "Accelerometer; barometer; fingerprint; gyroscope; geomagnetic; hall; light; proximity"),
    ]
    if model["brightness"]:
        fields.append(f("display_brightness", spec_source, model["brightness"], model["brightness"], unit="nits"))
    else:
        fields.append(pending("display_brightness", official, "A model-specific brightness figure was not located in the reviewed first-party source."))
    return fields


def models() -> list[dict]:
    return [
        {
            "id": "device_408426b533b92e", "name": "Galaxy S21 5G", "code": "s21",
            "model_code": "SM-G991B/DS", "config": "config_07943b6753bcc7", "ram": 8,
            "price": 47990, "date": "2021-02-05", "date_source": "gadgetmatch_s21_ph_launch_2021",
            "product_url": "https://www.samsung.com/ph/business/smartphones/galaxy-s/galaxy-s21-5g-g991-sm-g991bzagphl/",
            "product_note": "Samsung Philippines' Phantom Gray product entry identifies local SKU SM-G991BZAGPHL and publishes exact 8 GB/256 GB specifications. The color-specific SKU is not applied to the inventory variant.",
            "gsm_url": "https://www.gsmarena.com/samsung_galaxy_s21_5g-10626.php",
            "label": "8 GB RAM / 256 GB storage", "display_size": "6.2 inches (full rectangle)", "display_inches": 6.2,
            "resolution": "2400 x 1080 (FHD+)", "resolution_value": "2400 x 1080", "refresh": "Adaptive 48–120 Hz",
            "protection": "Corning Gorilla Glass Victus", "cpu": "5 nm octa-core, up to 2.9 GHz + 2.8 GHz + 2.2 GHz",
            "cpu_value": "Octa-core 2.9 / 2.8 / 2.2 GHz", "brightness": "Up to 1,300 peak nits",
            "rear_cameras": "12 MP wide with OIS + 12 MP ultra-wide + 64 MP telephoto with hybrid 3x optical zoom",
            "main_camera_mp": 12, "main_camera": "12 MP wide, Dual Pixel AF, OIS, f/1.8",
            "ultrawide": "12 MP ultra-wide, f/2.2", "telephoto": "64 MP telephoto, PDAF, OIS, f/2.0; hybrid 3x optical zoom",
            "front_camera": "10 MP front camera, Dual Pixel AF, f/2.2", "front_mp": 10,
            "video": "Rear video recording up to UHD 8K at 24 fps.", "battery": "4,000 mAh typical; 3,880 mAh rated minimum",
            "battery_typical": 4000, "battery_min": 3880, "dimensions": "151.7 x 71.2 x 7.9 mm", "dimensions_value": "151.7 x 71.2 x 7.9",
            "weight": 169, "materials": "Glass front, plastic back, aluminum frame", "wifi": "Wi-Fi 6",
            "bluetooth": "Bluetooth 5.0", "audio": "Stereo speakers; USB Type-C audio output; Dolby Atmos",
        },
        {
            "id": "device_2abcf9948e9239", "name": "Galaxy S21+ 5G", "code": "s21plus",
            "model_code": "SM-G996B/DS", "config": "config_13d4c1daf696b2", "ram": 8,
            "price": 57990, "date": "2021-01-29", "date_source": "yugatech_s21_ph_availability_2021",
            "product_url": "https://www.samsung.com/ph/business/smartphones/galaxy-s/galaxy-s21-5g-g996-sm-g996bzvgphl/",
            "product_note": "Samsung Philippines' Phantom Violet product entry identifies local SKU SM-G996BZVGPHL and exact 8 GB/256 GB specifications. The color-specific SKU is not applied to the inventory variant.",
            "gsm_url": "https://www.gsmarena.com/samsung_galaxy_s21_plus_5g-10625.php",
            "label": "8 GB RAM / 256 GB storage", "display_size": "6.7 inches (full rectangle)", "display_inches": 6.7,
            "resolution": "2400 x 1080 (FHD+)", "resolution_value": "2400 x 1080", "refresh": "Adaptive 48–120 Hz",
            "protection": "Corning Gorilla Glass Victus", "cpu": "5 nm octa-core, up to 2.9 GHz + 2.8 GHz + 2.2 GHz",
            "cpu_value": "Octa-core 2.9 / 2.8 / 2.2 GHz", "brightness": "Up to 1,300 peak nits",
            "rear_cameras": "12 MP wide with OIS + 12 MP ultra-wide + 64 MP telephoto with hybrid 3x optical zoom",
            "main_camera_mp": 12, "main_camera": "12 MP wide, Dual Pixel AF, OIS, f/1.8",
            "ultrawide": "12 MP ultra-wide, f/2.2", "telephoto": "64 MP telephoto, PDAF, OIS, f/2.0; hybrid 3x optical zoom",
            "front_camera": "10 MP front camera, Dual Pixel AF, f/2.2", "front_mp": 10,
            "video": "Rear video recording up to UHD 8K at 24 fps.", "battery": "4,800 mAh typical; 4,660 mAh rated minimum",
            "battery_typical": 4800, "battery_min": 4660, "dimensions": "161.5 x 75.6 x 7.8 mm", "dimensions_value": "161.5 x 75.6 x 7.8",
            "weight": 200, "materials": "Glass front and back, aluminum frame", "wifi": "Wi-Fi 6",
            "bluetooth": "Bluetooth 5.0", "audio": "Stereo speakers; USB Type-C audio output; Dolby Atmos",
        },
        {
            "id": "device_7327b88b5fe9d6", "name": "Galaxy S21 Ultra 5G", "code": "s21ultra",
            "model_code": "SM-G998B/DS", "config": "config_aec7e905ce4e48", "ram": 12,
            "price": 69990, "date": "2021-01-29", "date_source": "yugatech_s21_ph_availability_2021",
            "product_url": "https://www.samsung.com/ph/support/model/SM-G998BZKGPHL/",
            "product_note": "Samsung Philippines support identifies local Phantom Black SKU SM-G998BZKGPHL and family model SM-G998B/DS. The color-specific SKU is not applied to the color-unspecified inventory variant.",
            "gsm_url": "https://www.gsmarena.com/samsung_galaxy_s21_ultra_5g-10596.php",
            "label": "12 GB RAM / 256 GB storage", "display_size": "6.8 inches (full rectangle)", "display_inches": 6.8,
            "resolution": "3200 x 1440 (QHD+)", "resolution_value": "3200 x 1440", "refresh": "Adaptive 10–120 Hz",
            "protection": "Corning Gorilla Glass Victus", "cpu": "5 nm octa-core, up to 2.9 GHz + 2.8 GHz + 2.2 GHz",
            "cpu_value": "Octa-core 2.9 / 2.8 / 2.2 GHz", "brightness": "Up to 1,500 peak nits",
            "rear_cameras": "108 MP wide with OIS + 12 MP ultra-wide + 10 MP telephoto (3x) + 10 MP periscope telephoto (10x)",
            "main_camera_mp": 108, "main_camera": "108 MP wide, PDAF, OIS, f/1.8",
            "ultrawide": "12 MP ultra-wide, Dual Pixel AF, f/2.2", "telephoto": "10 MP telephoto (3x optical) + 10 MP periscope telephoto (10x optical); both with Dual Pixel AF and OIS",
            "front_camera": "40 MP front camera, PDAF, f/2.2", "front_mp": 40,
            "video": "Up to 8K at 24 fps; 4K at 60 fps across the camera lenses.", "battery": "5,000 mAh typical; 4,855 mAh rated minimum",
            "battery_typical": 5000, "battery_min": 4855, "dimensions": "165.1 x 75.6 x 8.9 mm", "dimensions_value": "165.1 x 75.6 x 8.9",
            "weight": 227, "materials": "Glass front and back, aluminum frame", "wifi": "Wi-Fi 6E",
            "bluetooth": "Bluetooth 5.2", "audio": "Stereo speakers; USB Type-C audio output; Dolby Atmos",
        },
    ]


def build_item(model: dict) -> dict:
    label = model["label"]
    price = model["price"]
    return {
        "deviceId": model["id"], "configurationId": model["config"],
        "brand": "Samsung", "model": model["name"],
        "configuration": label, "modelCode": model["model_code"],
        "configurationLabel": label, "sources": sources_for(model),
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": f"Philippine authorized-channel availability reported from {model['date']}",
            "philippineAvailability": "Contemporaneous Philippine launch coverage gives the local availability date; the S21+ and Ultra dates are also reported by YugaTech. Existing study eligibility remains Excluded because the claimed year is outside the workbook's selected window.",
            "observedAt": OBSERVED,
            "qualityFlag": "Local model/configuration and historical SRP verified; source dates retained as secondary evidence",
        },
        "fields": [
            f("philippine_release_date", model["date_source"],
              f"Contemporaneous Philippine reporting gives authorized-channel availability from {model['date']}.", model["date"],
              status="VERIFIED_SECONDARY", note="This is the reported Philippine availability date; it does not change the workbook's Excluded scope status."),
            f("official_launch_price_php", "samsung_s21_ph_official_srp_2021",
              f"Samsung Philippines historical SRP for {label}: PHP {price:,}.", price, unit="PHP"),
            f("current_price_php", "samsung_s21_ph_official_srp_2021",
              f"Historical Samsung Philippines SRP effective 29 January 2021: PHP {price:,}.", price, unit="PHP",
              note="Dated historical SRP; not a current offer.", price_condition="new",
              price_type="Historical Samsung Philippines official SRP (not a current offer)", price_observed="2021-01-29",
              replace_existing=True),
            *technical_fields(model),
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    reviewed = [build_item(model) for model in models()]

    # The old S21 8/256GB auto-generated variant duplicates the workbook's
    # single 256GB configuration. Samsung's exact local SKU now establishes
    # the missing RAM, so keep one correctly identified variant and preserve
    # the workbook's configuration row.
    base_id = "device_408426b533b92e"
    auto_id = f"{base_id}-auto-8gb-256gb"
    for review in manual["records"]:
        if review.get("deviceId") == base_id and review.get("configurationId") == "config_07943b6753bcc7":
            review.pop("additionalVariants", None)
    manual["records"] = [
        review for review in manual["records"]
        if not (review.get("deviceId") == base_id and review.get("configurationId") == auto_id)
    ]

    for item in reviewed:
        add_review(manual, catalog, item)
        review = next(r for r in manual["records"] if
                      (r["deviceId"], r["configurationId"]) ==
                      (item["deviceId"], item["configurationId"]))
        review["configurationLabel"] = item["configuration"]
        review["configuration"] = item["configuration"]
        review["modelCode"] = item["modelCode"]
        review.pop("additionalVariants", None)
        review.pop("replacementVariants", None)

    target_keys = {(item["deviceId"], item["configurationId"]) for item in reviewed}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"models": len(reviewed), "reviewedConfigurations": len(reviewed),
                      "deduplicatedConfiguration": auto_id, "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
