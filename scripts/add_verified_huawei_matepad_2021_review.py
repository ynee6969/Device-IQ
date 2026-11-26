#!/usr/bin/env python3
"""Review the Philippine Huawei MatePad 10.4 (Kirin 820) inventory entry."""
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
DEVICE = "device_e82e93c423ed2a"

URL_HUAWEI_SPECS = "https://consumer.huawei.com/za/tablets/matepad-new/specs/"
URL_HUAWEI_PH_SUPPORT = "https://consumer.huawei.com/ph/support/content/en-us15819846/"
URL_HUAWEI_PENCIL = "https://consumer.huawei.com/ph/support/content/en-us00737675/"
URL_YUGA_SPECS = "https://www.yugatech.com/spec/huawei-matepad-10-4-2021/"
URL_YUGA_REVIEW = "https://www.yugatech.com/personal-computing/huawei-matepad-10-4-2021-review-philippines/"
URL_YUGA_PRICE = "https://www.yugatech.com/personal-computing/tablet-price-list-2021-philippines/"

SOURCES = [
    {"id": "huawei_matepad_kirin820_official_specs", "publisher": "HUAWEI South Africa",
     "url": URL_HUAWEI_SPECS, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Manufacturer hardware specifications for the Kirin 820 MatePad 10.4 family",
     "note": "HUAWEI lists 10.4-inch 2000 x 1200 IPS, Kirin 820, 4 GB RAM, 64 GB storage, cameras, battery, connectivity, dimensions, and audio. This is an official regional spec page; the PH variant and 128 GB tier are separately cross-checked against Philippine reporting."},
    {"id": "huawei_matepad_ph_support_model_year", "publisher": "HUAWEI Support Philippines",
     "url": URL_HUAWEI_PH_SUPPORT, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Manufacturer model-family and regional-code cross-check",
     "note": "HUAWEI Philippines groups BAH3-W59 / BAH3-AN10 under MatePad 10.4-inch 2020 (Kirin 820), while contemporaneous Philippine coverage calls the Kirin 820 refresh MatePad 10.4 (2021). This naming difference is retained; no variant-specific model code is assigned."},
    {"id": "huawei_matepad_ph_stylus_support", "publisher": "HUAWEI Support Philippines",
     "url": URL_HUAWEI_PENCIL, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Manufacturer stylus compatibility reference",
     "note": "HUAWEI's support table lists the BAH3 MatePad 10.4 family as M-Pencil compatible, subject to the stated charger and firmware requirements."},
    {"id": "yugatech_matepad_2021_specs", "publisher": "YugaTech",
     "url": URL_YUGA_SPECS, "publicationDate": None, "accessDate": OBSERVED,
     "purpose": "Exact Philippine-reviewed model and family specifications",
     "note": "YugaTech identifies the Kirin 820 edition as MatePad 10.4 (2021), with 4 GB RAM, 64/128 GB storage, LTE, Wi-Fi 6 class WLAN, cameras, and battery."},
    {"id": "yugatech_matepad_2021_review", "publisher": "YugaTech",
     "url": URL_YUGA_REVIEW, "publicationDate": "2021-07-06", "accessDate": OBSERVED,
     "purpose": "Contemporaneous Philippine review and exact 4 GB / 128 GB review-unit check",
     "note": "The review identifies the 2021 Kirin 820 update, tests a 4 GB / 128 GB Wi-Fi-only unit, and reports PHP 18,999 at review time. Wi-Fi-only is not generalized to every 128 GB unit."},
    {"id": "yugatech_matepad_ph_price_list_2021", "publisher": "YugaTech",
     "url": URL_YUGA_PRICE, "publicationDate": "2021-06-02", "accessDate": OBSERVED,
     "purpose": "Philippine launch month, configuration, and dated price-list observations",
     "note": "The article states it lists tablets officially launched in the Philippines in 2021, marks this model as launched in June, and lists 4 GB + 64 GB LTE at PHP 14,249 and 4 GB + 128 GB at PHP 18,999. Updated as of 2021-11-30; the table does not label these amounts as official SRPs or say whether they include a promotion."},
]


def f(field_id: str, source_id: str, value: str, normalized=None, *, status="VERIFIED",
      key=None, unit=None, note=None, price_condition=None, price_type=None,
      price_observed=None) -> dict:
    row = {"fieldId": field_id, "status": status, "sourceId": source_id,
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


def pending(field_id: str, note: str, source_id="huawei_matepad_kirin820_official_specs") -> dict:
    return f(field_id, source_id, "Not recorded in the reviewed model-matched sources.", None,
             status="PENDING_VERIFICATION", note=note)


def n_a(field_id: str, source_id: str, note: str) -> dict:
    return f(field_id, source_id, "Not applicable to the documented single-camera configuration.", None,
             status="NOT_APPLICABLE", note=note)


def variants() -> list[dict]:
    return [
        {"id": f"{DEVICE}-kirin820-4gb-64gb-lte",
         "label": "4 GB RAM / 64 GB storage / LTE",
         "notes": "Configuration and dated Philippine price-list value are from YugaTech; exact regional model code not recorded."},
        {"id": f"{DEVICE}-kirin820-4gb-128gb",
         "label": "4 GB RAM / 128 GB storage",
         "notes": "Configuration is reported by YugaTech; its review unit was Wi-Fi only, but that radio configuration is not generalized to all units."},
    ]


def common_fields() -> list[dict]:
    h = "huawei_matepad_kirin820_official_specs"
    y = "yugatech_matepad_2021_specs"
    review = "yugatech_matepad_2021_review"
    return [
        f("model_number", "huawei_matepad_ph_support_model_year",
          "Official PH support lists BAH3-W59 / BAH3-AN10 for the Kirin 820 family but does not map a code to either PH price-list configuration.", None,
          status="PENDING_VERIFICATION", note="Do not assign a regional model code until the exact code-to-configuration mapping is sourced."),
        f("display_size", h, "10.4 inches", 10.4, key="displayInches", unit="in"),
        f("display_technology", h, "IPS touchscreen", "IPS", key="displayType"),
        f("display_resolution", h, "2000 x 1200", "2000 x 1200", key="resolution"),
        pending("display_refresh_rate", "No refresh-rate figure is published in the reviewed specifications."),
        f("display_brightness", h, "470 nit typical value", "470 nits typical", unit="nits"),
        pending("display_protection", "No display-glass protection type is recorded in the reviewed specifications."),
        f("chipset", h, "HUAWEI Kirin 820", "HUAWEI Kirin 820", key="chipset"),
        pending("process_node", "A process-node value was not stated in the reviewed model-matched official specification table."),
        f("cpu", h, "1 x A76-based 2.36 GHz + 3 x A76-based 2.22 GHz + 4 x A55-based 1.84 GHz",
          "1x Cortex-A76 2.36 GHz; 3x Cortex-A76 2.22 GHz; 4x Cortex-A55 1.84 GHz", key="cpu"),
        f("gpu", h, "Mali-G57", "Mali-G57", key="gpu"),
        f("operating_system", h, "EMUI 10.1 based on Android 10.0", "EMUI 10.1 / Android 10", key="os"),
        pending("os_support", "No model-specific OS/security support schedule was established."),
        f("ram_capacity", y, "4 GB", 4, key="ramGb", unit="GB"),
        pending("ram_type", "RAM technology is not recorded in the reviewed manufacturer and Philippine sources."),
        pending("storage_type", "Flash-storage technology is not recorded in the reviewed sources."),
        f("storage_expansion", h, "MicroSD expansion supported up to 512 GB; card sold separately.",
          "microSD up to 512 GB", note="Manufacturer states expansion limit; this does not add card capacity to internal storage."),
        f("rear_camera_system", h, "8 MP rear camera with autofocus and flash", "8 MP rear camera with autofocus and flash"),
        f("main_camera_sensor", h, "8 MP rear camera with autofocus", "8 MP rear camera with autofocus"),
        n_a("ultrawide_camera", h, "The reviewed manufacturer specification lists one 8 MP rear camera; the ultrawide camera is front-facing."),
        n_a("telephoto_camera", h, "The reviewed manufacturer specification lists one 8 MP rear camera and no rear telephoto module."),
        f("front_camera", h, "8 MP ultra-wide front camera", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", h, "Camera resolution up to 1920 x 1080; frame rate not stated.", "Up to 1920 x 1080"),
        f("battery_capacity", h, "7,250 mAh typical; 7,150 mAh rated", 7250, key="batteryMah", unit="mAh",
          note="Catalog capacity is typical; manufacturer separately states 7,150 mAh rated capacity."),
        f("battery_technology", h, "Built-in, non-removable battery; chemistry not stated.", "Built-in, non-removable; chemistry not recorded"),
        f("wired_charging", h, "Included charger supports 10 V / 2.25 A.", "10 V / 2.25 A charger profile",
          note="Exact adapter output as published; no wattage is inferred."),
        pending("wireless_charging", "No wireless charging statement appears in the reviewed model-matched sources."),
        f("dimensions", h, "245.20 x 154.96 x 7.45 mm", "245.20 x 154.96 x 7.45", key="dimensions", unit="mm"),
        f("weight", h, "Approximately 460 g including battery", 460, key="weightG", unit="g"),
        f("materials", review, "All-aluminum frame with matte finish", "Aluminum frame; matte finish", status="VERIFIED_SECONDARY"),
        pending("ingress_protection", "No ingress-protection rating is recorded in the reviewed sources."),
        pending("sim_esim", "SIM/eSIM count and type are not recorded for the specific listed configurations.", y),
        f("wifi", h, "IEEE 802.11a/b/g/n/ac/ax on 2.4 GHz and 5 GHz", "IEEE 802.11a/b/g/n/ac/ax; 2.4/5 GHz", key="wifi"),
        f("bluetooth", h, "Bluetooth 5.1", "Bluetooth 5.1"),
        f("usb", h, "USB Type-C, USB 2.0", "USB Type-C; USB 2.0", key="ports"),
        pending("nfc", "NFC support is not stated in the reviewed sources."),
        f("gnss", h, "GPS, GLONASS, BDS, Galileo", "GPS; GLONASS; BDS; Galileo"),
        f("audio", h, "Four speakers, four-channel output, HUAWEI Histen 6.1", "Four speakers; HUAWEI Histen 6.1", key="sound"),
        f("sensors", h, "Gravity, ambient light, hall, compass, and indicator sensors", "Gravity; ambient light; hall; compass; indicator"),
        f("tablet_stylus", review, "Stylus support; HUAWEI support lists M-Pencil compatibility for the BAH3 family.", "HUAWEI M-Pencil support; charger/firmware requirements apply", key="stylus", status="VERIFIED_SECONDARY"),
        pending("tablet_keyboard", "A compatible keyboard option was not confirmed for these exact configurations."),
    ]


def make_fields(config: dict) -> list[dict]:
    phprice = "yugatech_matepad_ph_price_list_2021"
    fields = [
        f("philippine_release_date", phprice, "Philippine launch month: June 2021 (exact first-sale day not stated).", "June 2021",
          status="VERIFIED_SECONDARY", note="Month-level evidence only; no exact day is inferred."),
        f("official_launch_price_php", phprice, "Official launch SRP not explicitly identified for this exact variant.", None,
          status="PENDING_VERIFICATION", note="The cited local price list gives a dated listed price, but does not identify it as official SRP."),
        f("current_price_php", phprice,
          f"YugaTech Philippine price-list observation: PHP {config['price']:,}; promotion/SRP status unspecified.", config["price"],
          status="VERIFIED_SECONDARY", unit="PHP", note="Historical 2021 price-list snapshot, not a current offer; source does not state whether this amount is SRP or promotional.",
          price_condition="new", price_type="Historical YugaTech Philippine price-list observation (not a current offer)",
          price_observed="2021-11-30"),
        f("configuration", "yugatech_matepad_ph_price_list_2021", config["label"], config["label"],
          status="VERIFIED_SECONDARY", note="The 2021 Philippine price list distinguishes 4 GB / 64 GB LTE and 4 GB / 128 GB configurations."),
        f("storage_capacity", phprice, f"{config['storage']} GB", config["storage"], key="storageGb", unit="GB",
          status="VERIFIED_SECONDARY"),
        *common_fields(),
    ]
    if config["cellular"]:
        fields.extend([
            f("cellular_bands", "yugatech_matepad_ph_price_list_2021", "4G LTE; supported bands not stated.", "4G LTE",
              key="cellular", status="VERIFIED_SECONDARY"),
            f("tablet_cellular_variant", "yugatech_matepad_ph_price_list_2021", "4 GB / 64 GB 4G LTE variant", "4G LTE",
              key="cellular", status="VERIFIED_SECONDARY"),
        ])
    else:
        fields.extend([
            pending("cellular_bands", "The Philippine price list does not identify network-radio details for the 4 GB / 128 GB tier.", phprice),
            pending("tablet_cellular_variant", "YugaTech tested a Wi-Fi-only 4 GB / 128 GB unit; the listing does not establish that every unit in this storage tier is Wi-Fi only.", "yugatech_matepad_2021_review"),
        ])
    return fields


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    # The original placeholder-only review is superseded by the two sourced,
    # configuration-specific records below. Its model/year and stylus source
    # URLs are retained in the new review sources.
    manual["records"] = [row for row in manual["records"] if not (
        row.get("deviceId") == DEVICE
        and row.get("configurationId") == f"{DEVICE}-unrecorded"
    )]
    config_rows = [
        {"id": f"{DEVICE}-kirin820-4gb-64gb-lte", "label": "4 GB RAM / 64 GB storage / LTE",
         "storage": 64, "price": 14249, "cellular": True},
        {"id": f"{DEVICE}-kirin820-4gb-128gb", "label": "4 GB RAM / 128 GB storage",
         "storage": 128, "price": 18999, "cellular": False},
    ]
    replacement = [{"id": row["id"], "label": row["label"],
                    "notes": "Configuration code not recorded; sourced from the 2021 Philippine price list."}
                   for row in config_rows]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine launch month documented as June 2021; exact first-sale day not recorded",
        "philippineAvailability": "YugaTech's 2021 Philippine tablet list identifies this Kirin 820 MatePad 10.4 as a June launch and lists its 4 GB / 64 GB LTE and 4 GB / 128 GB configurations. Huawei Philippines support uses a different 2020 naming label for the BAH3 Kirin 820 family; that discrepancy is retained in the source notes.",
        "observedAt": OBSERVED,
        "qualityFlag": "Year label differs by source; exact BAH3 variant code not confirmed.",
    }
    target_keys = {(DEVICE, row["id"]) for row in config_rows}
    for index, config in enumerate(config_rows):
        item = {
            "deviceId": DEVICE, "configurationId": config["id"],
            "brand": "Huawei", "model": "MatePad 10.4 (2021)",
            "configuration": config["label"], "configurationLabel": config["label"],
            "sources": SOURCES, "fields": make_fields(config),
            "replacementVariants": replacement,
        }
        if index == 0:
            item["availabilityEvidence"] = availability
        add_review(manual, catalog, item)
        review = next(row for row in manual["records"] if
                      (row["deviceId"], row["configurationId"]) == (DEVICE, config["id"]))
        review["configuration"] = config["label"]
        review["configurationLabel"] = config["label"]
        review.pop("additionalVariants", None)
        if index > 0:
            # The first review row replaces the original placeholder with both
            # source-established variants; only one row may carry that action.
            review.pop("replacementVariants", None)
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "MatePad 10.4 (2021)", "variants": len(config_rows),
                      "reviewedAt": OBSERVED, "status": "naming discrepancy retained"}, indent=2))


if __name__ == "__main__":
    main()
