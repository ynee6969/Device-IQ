#!/usr/bin/env python3
"""Add exact Samsung Philippines model/configuration evidence from product specs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"


def source(source_id: str, url: str, purpose: str, note: str, publisher: str = "Samsung Philippines") -> dict:
    return {"id": source_id, "publisher": publisher, "url": url,
            "publicationDate": None, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def field(field_id: str, source_id: str, raw, normalized, *, key: str | None = None,
          unit: str | None = None, status: str = "VERIFIED", note: str | None = None,
          catalog_value=None) -> dict:
    row = {"fieldId": field_id, "status": status, "sourceId": source_id,
           "sourceValue": raw, "normalizedValue": normalized,
           "note": note or "Checked against the exact Samsung Philippines product specification page."}
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        row["unit"] = unit
    return row


def model_review(device_id: str, brand: str, model: str, configuration_id: str,
                 configuration: str, model_code: str, source_id: str, url: str,
                 publisher: str, fields: list[dict], *, variant_note: str) -> dict:
    return {
        "deviceId": device_id, "configurationId": configuration_id,
        "brand": brand, "model": model, "configuration": configuration,
        "configurationLabel": configuration, "modelCode": model_code,
        "replaceUnrecordedPlaceholder": True,
        "replacementVariants": [{"id": configuration_id, "label": configuration,
                                 "sku": model_code, "modelCode": model_code, "notes": variant_note}],
        "sources": [source(source_id, url, "Official exact-model and configuration specifications",
                            f"The Samsung Philippines product page identifies model code {model_code} and lists the cited configuration and specifications. It does not establish a Philippine launch date or a current price.", publisher)],
        "fields": fields,
    }


def reviews() -> list[dict]:
    a13_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a13-black-128gb-sm-a135fzkjphl/"
    a13 = "samsung_a13_ph_specs"
    a13_fields = [
        field("model_number", a13, "SM-A135FZKJPHL", "SM-A135FZKJPHL"),
        field("configuration", a13, "Memory 6 GB; Storage 128 GB", "6 GB RAM / 128 GB storage"),
        field("display_size", a13, "6.6-inch display", 6.6, key="displayInches", unit="in"),
        field("display_technology", a13, "PLS LCD", "PLS LCD", key="displayType"),
        field("display_resolution", a13, "1080 x 2408 (FHD+)", "1080 x 2408", key="resolution"),
        field("chipset", a13, "Samsung Philippines spec page lists CPU type/speed but no SoC model.", None,
              status="NOT_DISCLOSED", note="The exact-model product page lists an octa-core CPU at 2.0 GHz but does not name the chipset; no SoC is inferred."),
        field("cpu", a13, "Octa-Core; CPU speed 2 GHz", "Octa-core, 2.0 GHz", key="cpu"),
        field("operating_system", a13, "Android", "Android", key="os"),
        field("ram_capacity", a13, "6 GB", 6, key="ramGb", unit="GB"),
        field("storage_capacity", a13, "128 GB", 128, key="storageGb", unit="GB"),
        field("storage_expansion", a13, "MicroSD up to 1 TB", "MicroSD supported up to 1 TB"),
        field("rear_camera_system", a13, "50 MP + 5 MP + 2 MP + 2 MP", "50 MP main + 5 MP ultra-wide + 2 MP depth + 2 MP macro",
              key="rearCameraMp", catalog_value=50),
        field("ultrawide_camera", a13, "Official page identifies a 5 MP ultra-wide rear camera", "5 MP ultra-wide camera"),
        field("telephoto_camera", a13, "Official page enumerates main, ultra-wide, depth, and macro rear cameras", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        field("front_camera", a13, "8 MP", 8, key="frontCameraMp", unit="MP"),
        field("video_recording", a13, "FHD (1920 x 1080) at 30 fps", "Up to 1080p/30 fps"),
        field("battery_capacity", a13, "5000 mAh typical; 4900 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
              note="The cited Samsung page distinguishes typical (5000 mAh) from rated minimum (4900 mAh); the catalog scalar records typical capacity."),
        field("dimensions", a13, "165.1 x 76.4 x 8.8 mm", "165.1 x 76.4 x 8.8 mm", key="dimensions", unit="mm"),
        field("weight", a13, "195 g", 195, key="weightG", unit="g"),
        field("sim_esim", a13, "Dual-SIM; Nano-SIM; SIM 1 + SIM 2 + MicroSD", "Dual Nano-SIM; separate SIM slots and MicroSD"),
        field("cellular_bands", a13, "2G GSM, 3G WCDMA, 4G LTE FDD/TDD", "2G/3G/4G LTE; official page lists supported bands"),
        field("wifi", a13, "802.11 a/b/g/n/ac, 2.4 + 5 GHz", "Wi-Fi 5 (802.11 a/b/g/n/ac)"),
        field("bluetooth", a13, "Bluetooth v5.0", "Bluetooth 5.0"),
        field("usb", a13, "USB Type-C; USB 2.0", "USB Type-C, USB 2.0", key="ports"),
        field("nfc", a13, "No", "No NFC"),
        field("gnss", a13, "GPS, GLONASS, BeiDou, Galileo, QZSS", "GPS, GLONASS, BeiDou, Galileo, QZSS"),
        field("audio", a13, "3.5 mm stereo jack; Dolby Atmos for compatible stereo headsets/Bluetooth speakers", "3.5 mm stereo jack; Dolby Atmos support"),
        field("sensors", a13, "Accelerometer, fingerprint sensor, geomagnetic sensor, virtual light sensing, virtual proximity sensing", "Accelerometer; fingerprint; geomagnetic; virtual light and proximity sensors"),
    ]

    a23_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a23-white-128gb-sm-a235fzwhphl/"
    a23 = "samsung_a23_lte_ph_specs"
    a23_fields = [
        field("model_number", a23, "SM-A235FZWHPHL", "SM-A235FZWHPHL"),
        field("configuration", a23, "Memory 6 GB; Storage 128 GB", "6 GB RAM / 128 GB storage"),
        field("display_size", a23, "6.6-inch display", 6.6, key="displayInches", unit="in"),
        field("display_technology", a23, "PLS TFT LCD", "PLS TFT LCD", key="displayType"),
        field("display_resolution", a23, "1080 x 2408 (FHD+)", "1080 x 2408", key="resolution"),
        field("display_refresh_rate", a23, "90 Hz refresh rate", 90, key="refreshHz", unit="Hz"),
        field("chipset", a23, "Samsung Philippines spec page lists CPU type/speed but no SoC model.", None,
              status="NOT_DISCLOSED", note="The exact-model product page lists CPU type and speeds but does not name the chipset; no SoC is inferred."),
        field("cpu", a23, "Octa-Core; CPU speeds 2.4 GHz and 1.9 GHz", "Octa-core, 2.4 GHz + 1.9 GHz", key="cpu"),
        field("operating_system", a23, "Android", "Android", key="os"),
        field("ram_capacity", a23, "6 GB", 6, key="ramGb", unit="GB"),
        field("storage_capacity", a23, "128 GB", 128, key="storageGb", unit="GB"),
        field("storage_expansion", a23, "MicroSD up to 1 TB", "MicroSD supported up to 1 TB"),
        field("rear_camera_system", a23, "50 MP + 5 MP + 2 MP + 2 MP; main camera includes OIS", "50 MP main with OIS + 5 MP ultra-wide + 2 MP depth + 2 MP macro",
              key="rearCameraMp", catalog_value=50),
        field("ultrawide_camera", a23, "Official page identifies a 5 MP ultra-wide rear camera", "5 MP ultra-wide camera"),
        field("telephoto_camera", a23, "Official page enumerates main, ultra-wide, depth, and macro rear cameras", "No dedicated telephoto camera listed", status="NOT_APPLICABLE"),
        field("front_camera", a23, "8 MP", 8, key="frontCameraMp", unit="MP"),
        field("video_recording", a23, "UHD 4K (3840 x 2160) at 30 fps", "Up to 4K/30 fps"),
        field("battery_capacity", a23, "5000 mAh typical; 4860 mAh rated minimum", 5000, key="batteryMah", unit="mAh",
              note="The cited Samsung page distinguishes typical (5000 mAh) from rated minimum (4860 mAh); the catalog scalar records typical capacity."),
        field("wired_charging", a23, "25W Super Fast Charging support; charger sold separately", 25, key="chargingW", unit="W"),
        field("dimensions", a23, "165.4 x 76.9 x 8.4 mm", "165.4 x 76.9 x 8.4 mm", key="dimensions", unit="mm"),
        field("weight", a23, "195 g", 195, key="weightG", unit="g"),
        field("sim_esim", a23, "Dual-SIM; Nano-SIM; SIM 1 + SIM 2 + MicroSD", "Dual Nano-SIM; separate SIM slots and MicroSD"),
        field("cellular_bands", a23, "2G GSM, 3G WCDMA, 4G LTE FDD/TDD", "2G/3G/4G LTE; official page lists supported bands"),
        field("wifi", a23, "802.11 a/b/g/n/ac, 2.4 + 5 GHz", "Wi-Fi 5 (802.11 a/b/g/n/ac)"),
        field("bluetooth", a23, "Bluetooth v5.0", "Bluetooth 5.0"),
        field("usb", a23, "USB Type-C; USB 2.0", "USB Type-C, USB 2.0", key="ports"),
        field("nfc", a23, "No", "No NFC"),
        field("gnss", a23, "GPS, GLONASS, BeiDou, Galileo, QZSS", "GPS, GLONASS, BeiDou, Galileo, QZSS"),
        field("audio", a23, "3.5 mm stereo jack; Dolby Atmos for compatible stereo headsets/Bluetooth speakers", "3.5 mm stereo jack; Dolby Atmos support"),
        field("sensors", a23, "Accelerometer, fingerprint sensor, gyroscope, geomagnetic sensor, virtual light sensing, virtual proximity sensing", "Accelerometer; fingerprint; gyroscope; geomagnetic; virtual light and proximity sensors"),
    ]

    tab_url = "https://www.samsung.com/ph/business/tablets/galaxy-tab-s/galaxy-tab-s7-fe-black-128gb-sm-t735nzkextc/"
    tab = "samsung_tab_s7_fe_ph_specs"
    tab_fields = [
        field("model_number", tab, "SM-T735NZKEXTC", "SM-T735NZKEXTC"),
        field("configuration", tab, "Memory 6 GB; Storage 128 GB", "6 GB RAM / 128 GB storage"),
        field("display_size", tab, "12.4 inches", 12.4, key="displayInches", unit="in"),
        field("display_technology", tab, "TFT", "TFT", key="displayType"),
        field("display_resolution", tab, "2560 x 1600 (WQXGA)", "2560 x 1600", key="resolution"),
        field("chipset", tab, "Snapdragon 750G", "Qualcomm Snapdragon 750G", key="chipset"),
        field("cpu", tab, "Octa-Core; CPU speeds 2.2 GHz and 1.8 GHz", "Octa-core, 2.2 GHz + 1.8 GHz", key="cpu"),
        field("operating_system", tab, "Android", "Android", key="os"),
        field("ram_capacity", tab, "6 GB", 6, key="ramGb", unit="GB"),
        field("storage_capacity", tab, "128 GB", 128, key="storageGb", unit="GB"),
        field("storage_expansion", tab, "MicroSD up to 1 TB", "MicroSD supported up to 1 TB"),
        field("rear_camera_system", tab, "8 MP rear camera", "8 MP rear camera"),
        field("ultrawide_camera", tab, "Single 8 MP rear camera listed", "No ultra-wide rear camera listed", status="NOT_APPLICABLE"),
        field("telephoto_camera", tab, "Single 8 MP rear camera listed", "No telephoto rear camera listed", status="NOT_APPLICABLE"),
        field("front_camera", tab, "5 MP", 5, key="frontCameraMp", unit="MP"),
        field("video_recording", tab, "FHD (1920 x 1080) at 30 fps", "Up to 1080p/30 fps"),
        field("battery_capacity", tab, "10090 mAh typical", 10090, key="batteryMah", unit="mAh"),
        field("wired_charging", tab, "45W Super Fast Charging support; included adapter is 15W; 45W adapter sold separately", 45, key="chargingW", unit="W"),
        field("dimensions", tab, "185.0 x 284.8 x 6.3 mm (H x W x D)", "185.0 x 284.8 x 6.3 mm", key="dimensions", unit="mm"),
        field("weight", tab, "608 g", 608, key="weightG", unit="g"),
        field("sim_esim", tab, "SM-T735 LTE model; Nano-SIM details not disclosed on the cited product page", "4G LTE model; SIM format not recorded"),
        field("cellular_bands", tab, "2G GSM, 3G WCDMA, 4G LTE FDD/TDD; exact supported bands listed on the official product page", "2G/3G/4G LTE; official page lists supported bands"),
        field("tablet_cellular_variant", tab, "Galaxy Tab S7 FE LTE (SM-T735)", "4G LTE cellular model", key="cellular"),
        field("wifi", tab, "802.11 a/b/g/n/ac, 2.4 + 5 GHz", "Wi-Fi 5 (802.11 a/b/g/n/ac)"),
        field("bluetooth", tab, "Bluetooth v5.0", "Bluetooth 5.0"),
        field("usb", tab, "USB 3.2 Gen 1", "USB 3.2 Gen 1", key="ports"),
        field("nfc", tab, "No", "No NFC"),
        field("gnss", tab, "GPS, GLONASS, BeiDou, Galileo, QZSS", "GPS, GLONASS, BeiDou, Galileo, QZSS"),
        field("audio", tab, "Dual speakers by AKG; Dolby Atmos", "Dual AKG speakers; Dolby Atmos"),
        field("sensors", tab, "Accelerometer, gyroscope, geomagnetic sensor, hall sensor, light sensor", "Accelerometer; gyroscope; geomagnetic; hall; light sensors"),
        field("tablet_stylus", tab, "S Pen support; S Pen included", "S Pen included"),
        field("tablet_keyboard", tab, "Samsung Keyboard support; keyboard cover not included", "Keyboard cover is a separately sold accessory"),
    ]

    return [
        model_review("device_ea7538b5f9c456", "Samsung", "A13", "device_ea7538b5f9c456-samsung-6gb-128gb",
                     "6 GB RAM / 128 GB storage", "SM-A135FZKJPHL", a13, a13_url, "Samsung Philippines", a13_fields,
                     variant_note="Exact 6 GB / 128 GB configuration and regional model code shown on Samsung Philippines product page."),
        model_review("device_61c7ea30c4c22b", "Samsung", "A23", "device_61c7ea30c4c22b-samsung-6gb-128gb",
                     "6 GB RAM / 128 GB storage", "SM-A235FZWHPHL", a23, a23_url, "Samsung Philippines", a23_fields,
                     variant_note="Exact Galaxy A23 LTE 6 GB / 128 GB configuration and regional model code shown on Samsung Philippines product page."),
        model_review("device_a1f3d16dd15fe1", "Samsung", "Galaxy Tab S7 FE", "device_a1f3d16dd15fe1-samsung-lte-6gb-128gb",
                     "6 GB RAM / 128 GB storage, LTE", "SM-T735NZKEXTC", tab, tab_url, "Samsung Philippines for Business", tab_fields,
                     variant_note="Exact LTE 6 GB / 128 GB configuration and regional model code shown on Samsung Philippines product page."),
    ]


def main() -> None:
    from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = reviews()
    for item in items:
        add_review(manual, catalog, item)
    deduplicate_target_reviews(manual, {(item["deviceId"], item["configurationId"]) for item in items})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"modelsReviewed": len(items), "variantsAdded": len(items),
                      "verifiedFieldsAdded": sum(len(item["fields"]) for item in items), "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
