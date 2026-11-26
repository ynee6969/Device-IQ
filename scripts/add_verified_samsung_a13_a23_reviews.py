#!/usr/bin/env python3
"""Verify the Philippine LTE variants and historical prices for Galaxy A13/A23."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_samsung_a_series_reviews import f, record, src  # noqa: E402
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"


def build_records(manual):
    output = []
    price_url = "https://www.yugatech.com/mobile/samsung-galaxy-a13-a23-price-philippines/"
    price = src(
        "yugatech_samsung_a13_a23_local_prices_2022",
        "YugaTech",
        price_url,
        "Historical Philippine LTE configuration and price evidence",
        "YugaTech reported Philippine prices on 19 May 2022: Galaxy A13 4 GB/128 GB PHP 10,490; Galaxy A13 6 GB/128 GB PHP 11,490; Galaxy A23 6 GB/128 GB PHP 13,990. These are dated historical prices, not current offers.",
        "2022-05-19",
    )

    # These workbook rows refer to the LTE A13 and LTE A23. The 2022 Samsung
    # Philippines product pages and the contemporaneous Philippine pricing
    # report distinguish them from the later A13 5G and A23 5G models.
    for device_id, model, config_id, product_url, sku, ram, price_php, source_id in [
        (
            "device_ea7538b5f9c456",
            "Galaxy A13 LTE",
            "device_ea7538b5f9c456-samsung-6gb-128gb",
            "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a13-black-128gb-sm-a135fzkjphl/",
            "SM-A135FZKJPHL",
            6,
            11490,
            "samsung_a13_ph_lte_product",
        ),
        (
            "device_61c7ea30c4c22b",
            "Galaxy A23 LTE",
            "device_61c7ea30c4c22b-samsung-6gb-128gb",
            "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a23-white-128gb-sm-a235fzwhphl/",
            "SM-A235FZWHPHL",
            6,
            13990,
            "samsung_a23_ph_lte_product",
        ),
    ]:
        product = src(
            source_id,
            "Samsung Philippines",
            product_url,
            "Official Philippine LTE product identity and specifications",
            f"Samsung Philippines identifies the local LTE product page and SKU {sku}. The page is model-specific and does not establish the exact original first-sale date; its current sale status is not treated as an active offer.",
        )
        availability = {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Historical Philippine listing; current sale not confirmed",
            "philippineAvailability": (
                "Samsung Philippines product pages identify the local LTE model and SKU. "
                "YugaTech reported Philippine configurations and prices in May 2022. "
                "The exact first-sale date is not recorded, and current sale is not confirmed."
            ),
            "observedAt": OBSERVED,
            "qualityFlag": "Philippine LTE product listing verified; exact first-sale date not recorded",
        }
        fields = [
            f(
                "current_price_php",
                price["id"],
                f"Historical Philippine price reported 19 May 2022: PHP {price_php:,}",
                price_php,
                unit="PHP",
                note="Historical price reported in a Philippine launch coverage article; not a current offer.",
                price_condition="new",
                price_type="Historical Philippine price reported by YugaTech (not a current offer)",
                price_observed="2022-05-19",
            ),
            f(
                "philippine_release_date",
                source_id,
                "The official Philippine product page does not state the exact original first-sale date.",
                None,
                status="NOT_DISCLOSED",
                note="Philippine model identity and historical local pricing are verified, but the exact first-sale date is not established.",
            ),
        ]
        sources = [product, price]
        output.append(
            record(
                device_id,
                model,
                config_id,
                f"{ram} GB RAM / 128 GB storage",
                sources,
                fields,
                model_code="SM-A135F" if model == "Galaxy A13 LTE" else "SM-A235F",
                sku=sku,
                availability=availability,
            )
        )

    # Add the independently sourced 4 GB/128 GB LTE A13 configuration as a
    # distinct variant. The exact local SKU is not stated by the cited source.
    a13_device = "device_ea7538b5f9c456"
    a13_config = f"{a13_device}-samsung-4gb-128gb"
    a13_product_url = "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a13-black-128gb-sm-a135fzkjphl/"
    a13_review = next(
        r for r in manual["records"]
        if r["deviceId"] == a13_device
        and r["configurationId"] == f"{a13_device}-samsung-6gb-128gb"
    )
    config_fields = copy.deepcopy(a13_review["fields"])
    for row in config_fields:
        if row.get("sourceId") and row["sourceId"] != price["id"]:
            row["sourceId"] = "samsung_a13_ph_lte_product"
        if row["fieldId"] == "configuration":
            row.update({
                "sourceId": price["id"],
                "sourceValue": "Galaxy A13 LTE, 4 GB RAM / 128 GB storage",
                "normalizedValue": "4 GB RAM / 128 GB storage",
            })
        elif row["fieldId"] == "ram_capacity":
            row.update({
                "sourceId": price["id"],
                "sourceValue": "4 GB RAM",
                "normalizedValue": 4,
                "catalogValue": 4,
            })
        elif row["fieldId"] == "model_number":
            row.update({
                "sourceId": price["id"],
                "sourceValue": "The Philippine 4 GB/128 GB configuration is reported; a specific Samsung model code is not provided.",
                "normalizedValue": None,
                "status": "NOT_DISCLOSED",
                "catalogKey": None,
                "catalogValue": None,
            })
    config_fields.extend([
        f(
            "current_price_php",
            price["id"],
            "Historical Philippine price reported 19 May 2022: PHP 10,490",
            10490,
            unit="PHP",
            note="Historical price reported in a Philippine launch coverage article; not a current offer.",
            price_condition="new",
            price_type="Historical Philippine price reported by YugaTech (not a current offer)",
            price_observed="2022-05-19",
        ),
        f(
            "philippine_release_date",
            "samsung_a13_ph_lte_product",
            "The official Philippine product page does not state the exact original first-sale date.",
            None,
            status="NOT_DISCLOSED",
            note="Philippine model identity and historical local pricing are verified, but the exact first-sale date is not established.",
        ),
    ])
    sources = [
        src(
            "samsung_a13_ph_lte_product",
            "Samsung Philippines",
            a13_product_url,
            "Official Philippine LTE model identity and shared hardware specifications",
            "Samsung Philippines' model-specific A13 LTE product page supplies hardware details and confirms the local LTE family; it does not give the exact SKU for the 4 GB configuration.",
        ),
        price,
    ]
    a13_availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Historical Philippine listing; current sale not confirmed",
        "philippineAvailability": (
            "Samsung Philippines lists the Galaxy A13 LTE family, and YugaTech reported its "
            "4 GB/128 GB and 6 GB/128 GB Philippine configurations in May 2022. "
            "The exact first-sale date and the 4 GB SKU are not recorded."
        ),
        "observedAt": OBSERVED,
        "qualityFlag": "Philippine LTE product listing verified; exact first-sale date and 4 GB SKU not recorded",
    }
    additional = [{
        "id": a13_config,
        "label": "4 GB RAM / 128 GB storage",
        "modelCode": None,
        "sku": None,
        "notes": "Philippine 4 GB/128 GB variant reported by YugaTech; exact local Samsung SKU not recorded.",
    }]
    item = record(
        a13_device,
        "Galaxy A13 LTE",
        a13_config,
        "4 GB RAM / 128 GB storage",
        sources,
        config_fields,
        model_code=None,
        sku=None,
        availability=a13_availability,
    )
    item["additionalVariants"] = additional
    output.append(item)
    return output


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = build_records(manual)
    for item in items:
        add_review(manual, catalog, item)
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewedConfigurations": len(items), "models": 2, "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
