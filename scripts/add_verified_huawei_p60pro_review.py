#!/usr/bin/env python3
"""Add exact Philippine-source evidence for the Huawei P60 Pro inventory row."""
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


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def field(fid: str, sid: str, value, normalized=None, *, key: str | None = None,
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


def build_record() -> dict:
    device = "device_a41c76670e8533"
    config = device + "-auto-8gb-256gb"
    specs_id = "huawei_p60_pro_ph_official_specs"
    launch_id = "huawei_p60_pro_ph_available_2023"
    specs_url = "https://consumer.huawei.com/ph/phones/p60-pro/buy/"
    launch_url = "https://consumer.huawei.com/ph/community/details/topicId-189003/"
    sources = [
        source(specs_id, "HUAWEI Philippines", specs_url,
               "Official Philippines product specifications, configuration and local store listing",
               "The official Philippines product page identifies the Rococo Pearl 8 GB + 256 GB version, lists its specifications and PHP 58,999 price, and showed out of stock when checked. The 12 GB + 512 GB inventory configuration is not established as a Philippine SKU by this page."),
        source(launch_id, "HUAWEI Philippines Community", launch_url,
               "Philippine authorized availability and launch-price evidence",
               "Huawei Philippines stated that the P60 Pro was available in stores and for purchase starting at PHP 58,999 in its 7 June 2023 notice. This confirms Philippine availability by that date, but does not establish the exact first-sale date.",
               "2023-06-07"),
    ]
    fields = [
        field("model_number", specs_id, "Exact Philippine model/SKU code is not published on the cited product page.", None,
              status="PENDING_VERIFICATION", note="Do not infer the full regional code from the model name."),
        field("configuration", specs_id, "HUAWEI P60 Pro (Rococo Pearl) 8 GB + 256 GB", "8 GB RAM / 256 GB storage"),
        pending("philippine_release_date", launch_id,
                "Huawei Philippines confirms that the model was available for purchase by 7 June 2023 but does not state the first authorized sale date.",
                "The article publication date is an availability bound, not an exact initial-sale date."),
        field("official_launch_price_php", launch_id,
              "Huawei Philippines announced the P60 Pro was available in stores starting at PHP 58,999.", 58999,
              unit="PHP", note="Historical official Philippine launch-price evidence; not a current offer."),
        field("display_size", specs_id, "6.67 inches", 6.67, key="displayInches", unit="in"),
        field("display_technology", specs_id, "LTPO OLED, adaptive 1–120 Hz", "LTPO OLED", key="displayType"),
        field("display_resolution", specs_id, "2700 x 1220 pixels", "2700 x 1220", key="resolution"),
        field("display_refresh_rate", specs_id, "Adaptive 1–120 Hz", 120, key="refreshHz", unit="Hz"),
        field("display_brightness", specs_id, "Brightness in nits is not stated on the cited PH product page.", None,
              status="NOT_DISCLOSED", note="The source lists PWM dimming and touch sampling, but no brightness value in nits."),
        field("display_protection", specs_id, "Kunlun Glass; Huawei states 10x drop resistance versus its regular-glass comparison in its lab test", "Kunlun Glass"),
        field("chipset", specs_id, "Snapdragon 8+ Gen 1 4G Mobile Platform", "Snapdragon 8+ Gen 1 4G", key="chipset"),
        field("cpu", specs_id, "CPU core layout and clock rates are not stated on the cited PH product page.", None,
              status="NOT_DISCLOSED", note="No CPU configuration is inferred from the chipset."),
        field("gpu", specs_id, "GPU is not named on the cited PH product page.", None,
              status="NOT_DISCLOSED", note="No GPU is inferred from the chipset."),
        field("rear_camera_system", specs_id,
              "48 MP Ultra Lighting main camera with OIS and variable f/1.4–f/4.0 aperture + 13 MP ultra-wide + 48 MP telephoto with OIS",
              "48 MP main with OIS + 13 MP ultra-wide + 48 MP telephoto with OIS"),
        field("ultrawide_camera", specs_id, "13 MP ultra-wide angle, f/2.2", "13 MP, f/2.2"),
        field("telephoto_camera", specs_id, "48 MP Ultra Lighting telephoto camera, f/2.1, OIS", "48 MP, f/2.1, OIS"),
        field("front_camera", specs_id, "13 MP selfie camera", 13, key="frontCameraMp", unit="MP"),
        field("battery_capacity", specs_id, "4,815 mAh typical value", 4815, key="batteryMah", unit="mAh"),
        field("wired_charging", specs_id, "Up to 88 W HUAWEI SuperCharge", 88, key="chargingW", unit="W"),
        field("wireless_charging", specs_id, "Up to 50 W HUAWEI Wireless SuperCharge", "Up to 50 W HUAWEI Wireless SuperCharge"),
        field("dimensions", specs_id, "161 x 74.5 x 8.3 mm", "161 x 74.5 x 8.3 mm", key="dimensions", unit="mm"),
        field("weight", specs_id, "Approx. 200 g (including battery)", 200, key="weightG", unit="g"),
        field("ingress_protection", specs_id, "IP68 splash, water and dust resistance", "IP68"),
    ]
    return {
        "deviceId": device, "configurationId": config,
        "brand": "Huawei", "model": "P60 Pro",
        "configuration": "8 GB RAM / 256 GB storage (Philippine product page)",
        "sources": sources, "fields": fields,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Huawei Philippines confirmed retail availability by 7 June 2023; official store page showed out of stock when checked.",
            "philippineAvailability": "Huawei Philippines stated the P60 Pro was available in stores and for purchase by 7 June 2023, starting at PHP 58,999. The exact first-sale date is not established. The official PH page identifies 8 GB + 256 GB; Philippine availability of the inventory's 12 GB + 512 GB configuration is unverified.",
            "observedAt": OBSERVED,
            "qualityFlag": "First authorized sale date and Philippine availability of 12 GB / 512 GB configuration not recorded",
        },
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    item = build_record()
    add_review(manual, catalog, item)
    device_id = item["deviceId"]
    target_keys = {
        (device_id, device_id + "-auto-8gb-256gb"),
        (device_id, device_id + "-auto-12gb-512gb"),
    }
    deduplicate_target_reviews(manual, target_keys)
    # The catalog builder applies a device's replacementVariants when it sees
    # the first review for that device. Put the reviewed 8/256 row, which owns
    # the two source-preserved configs, before the sibling 12/512 row.
    p60_rows = [r for r in manual["records"] if r.get("deviceId") == device_id]
    p60_rows.sort(key=lambda r: r["configurationId"] != device_id + "-auto-8gb-256gb")
    # Record the primary-source explanation for the two still-unverified
    # fields, even when an older crawler row already marked them pending.
    reviewed_fields = {f["fieldId"]: f for f in item["fields"]}
    primary_pending = {name: reviewed_fields[name] for name in ("model_number", "philippine_release_date")}
    for review in p60_rows:
        if review["configurationId"] != device_id + "-auto-8gb-256gb":
            continue
        by_field = {f["fieldId"]: i for i, f in enumerate(review["fields"])}
        for field_id, new_field in primary_pending.items():
            old = review["fields"][by_field[field_id]] if field_id in by_field else None
            replacement = dict(new_field)
            if old and old.get("candidateEvidence"):
                replacement["candidateEvidence"] = old["candidateEvidence"]
            if old:
                review["fields"][by_field[field_id]] = replacement
            else:
                review["fields"].append(replacement)
    remaining = [r for r in manual["records"] if r.get("deviceId") != device_id]
    manual["records"] = p60_rows + remaining
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewedConfiguration": item["configurationId"],
                      "reviewedAt": OBSERVED, "authorizedAvailability": "confirmed by 2023-06-07",
                      "firstSaleDate": "not recorded"}, indent=2))


if __name__ == "__main__":
    main()
