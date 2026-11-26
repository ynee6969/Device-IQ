#!/usr/bin/env python3
"""Record source-backed reviews for exact Xiaomi/Redmi PH tablet configurations."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-25"


def src(sid, url, purpose, note, publisher="Xiaomi Philippines", published=None):
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid, sid, value, normalized, *, status="VERIFIED", key=None, unit=None,
      note=None, price_condition=None, price_type=None, price_observed=None):
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized,
           "note": note or "Exact model and listed 8 GB / 256 GB configuration checked against the cited official source."}
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized
    if unit:
        row["unit"] = unit
    if price_condition:
        row["priceCondition"] = price_condition
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed
    return row


def pending(fid, sid, value, note, unit=None):
    return f(fid, sid, value, None, status="PENDING_VERIFICATION", unit=unit, note=note)


def add_review(manual, catalog, item):
    key = (item["deviceId"], item["configurationId"])
    device = next((d for d in catalog if d["id"] == item["deviceId"]), None)
    if not device:
        raise ValueError(f"Unknown device: {item['deviceId']}")
    variant = next((v for v in device.get("variants", []) if v["id"] == item["configurationId"]), None)
    if not variant and any(v.get("id") == item["configurationId"] for v in item.get("replacementVariants", [])):
        variant = {"id": item["configurationId"], "specs": {}}
    if not variant and any(v.get("id") == item["configurationId"] for v in item.get("additionalVariants", [])):
        variant = {"id": item["configurationId"], "specs": {}}
    if not variant:
        raise ValueError(f"Unknown configuration: {key}")
    review = next((r for r in manual["records"] if (r["deviceId"], r["configurationId"]) == key), None)
    if review is None:
        review = {"deviceId": item["deviceId"], "configurationId": item["configurationId"],
                  "brand": item["brand"], "model": item["model"],
                  "configuration": item["configuration"], "configurationLabel": item["configuration"],
                  "sources": [], "fields": []}
        manual["records"].append(review)
    if item.get("modelCode"):
        review["modelCode"] = item["modelCode"]
    if item.get("sku"):
        review["sku"] = item["sku"]
    if item.get("replacementVariants"):
        review["replacementVariants"] = item["replacementVariants"]
    if item.get("additionalVariants"):
        review["additionalVariants"] = item["additionalVariants"]
    if item.get("availabilityEvidence"):
        review["availabilityEvidence"] = item["availabilityEvidence"]
    for source in item["sources"]:
        if not any(old["id"] == source["id"] for old in review["sources"]):
            review["sources"].append(source)
    fields = {row["fieldId"]: i for i, row in enumerate(review["fields"])}
    sources = {s["id"]: s for s in review["sources"]}
    for row in item["fields"]:
        if row["fieldId"] in fields:
            old = review["fields"][fields[row["fieldId"]]]
            # The exact manufacturer-page review supersedes an older crawler
            # candidate, and explicit source conflicts supersede prior values.
            replace_review = (
                row.get("status") == "CONFLICTING_INFORMATION" and old.get("status") != "CONFLICTING_INFORMATION"
                or old.get("sourceId", "").startswith("candidate_")
                and row.get("status") in {"VERIFIED", "VERIFIED_SECONDARY", "CONFLICTING_INFORMATION"}
                or row.get("catalogKey") and not old.get("catalogKey")
                or old.get("catalogKey") and not row.get("catalogKey")
                or row.get("replaceExisting")
            )
            if row.get("catalogKey") and row.get("status") in {"VERIFIED", "VERIFIED_SECONDARY"}:
                current_value = variant.get("specs", {}).get(row["catalogKey"])
                if current_value is not None and str(current_value) != str(row.get("catalogValue")):
                    replace_review = True
            if replace_review:
                if row.get("catalogKey") and row.get("status") in {"VERIFIED", "VERIFIED_SECONDARY"}:
                    old_value = variant.get("specs", {}).get(row["catalogKey"])
                    if old_value is not None and str(old_value) != str(row.get("catalogValue")):
                        row["replaceExisting"] = True
                if row.get("catalogKey") and row.get("status") == "CONFLICTING_INFORMATION":
                    row["replaceExisting"] = True
                review["fields"][fields[row["fieldId"]]] = row
            continue
        if row.get("catalogKey") and row.get("status") in {"VERIFIED", "VERIFIED_SECONDARY"}:
            old_value = variant.get("specs", {}).get(row["catalogKey"])
            if old_value is not None and str(old_value) != str(row.get("catalogValue")):
                row["replaceExisting"] = True
        if row.get("catalogKey") and row.get("status") == "CONFLICTING_INFORMATION":
            row["replaceExisting"] = True
        review["fields"].append(row)
        fields[row["fieldId"]] = len(review["fields"]) - 1
    for row in item["fields"]:
        if row["fieldId"] == "current_price_php" and row["status"] in {"VERIFIED", "VERIFIED_SECONDARY"}:
            price = row["normalizedValue"]
            variant.update({"pricePhp": price, "priceCondition": row.get("priceCondition") or "new",
                            "priceType": row.get("priceType"), "priceObservedAt": row.get("priceObservedAt"),
                            "priceSourceUrl": sources[row["sourceId"]]["url"], "notes": row.get("note")})
    for source in item["sources"]:
        if not any(existing.get("url") == source["url"] for existing in device["sources"]):
            device["sources"].append({"organization": source["publisher"], "url": source["url"],
                                      "observedAt": source["accessDate"], "publishedAt": source.get("publicationDate"),
                                      "purpose": source["purpose"], "note": source["note"]})


def deduplicate_target_reviews(manual, target_keys):
    """Merge historical duplicate review rows without discarding evidence."""
    grouped = {}
    others = []
    for review in manual["records"]:
        key = (review["deviceId"], review["configurationId"])
        if key not in target_keys:
            others.append(review)
            continue
        grouped.setdefault(key, []).append(review)

    def rank(row):
        status = row.get("status")
        source = row.get("sourceId", "")
        if status == "CONFLICTING_INFORMATION":
            return 6
        if status in {"VERIFIED", "VERIFIED_SECONDARY"} and not source.startswith("candidate_"):
            return 5 if status == "VERIFIED" else 4
        if status in {"NOT_DISCLOSED", "NOT_APPLICABLE", "UNAVAILABLE_AFTER_RESEARCH"}:
            return 4
        if status in {"VERIFIED", "VERIFIED_SECONDARY"}:
            return 3
        if status == "PENDING_VERIFICATION":
            return 2
        return 1

    for key, reviews in grouped.items():
        merged = dict(reviews[0])
        merged["sources"] = []
        by_source = {}
        for review in reviews:
            for source in review.get("sources", []):
                by_source.setdefault(source["id"], source)
        merged["sources"] = list(by_source.values())
        rows = {}
        all_evidence = {}
        for review in reviews:
            for row in review.get("fields", []):
                fid = row["fieldId"]
                all_evidence.setdefault(fid, []).extend(row.get("candidateEvidence", []))
                current = rows.get(fid)
                if current is None or rank(row) > rank(current):
                    rows[fid] = row
                elif rank(row) == rank(current) and row.get("normalizedValue") is not None and current.get("normalizedValue") is not None and str(row["normalizedValue"]) != str(current["normalizedValue"]):
                    evidence = [
                        {"value": current.get("normalizedValue"), "unit": current.get("unit"),
                         "sourceUrl": by_source.get(current.get("sourceId"), {}).get("url"),
                         "sourceKind": "official" if not current.get("sourceId", "").startswith("candidate_") else "candidate",
                         "observedAt": OBSERVED, "excerpt": current.get("sourceValue"),
                         "configurationMatch": "exact model", "reviewStatus": "CONFLICTING_INFORMATION"},
                        {"value": row.get("normalizedValue"), "unit": row.get("unit"),
                         "sourceUrl": by_source.get(row.get("sourceId"), {}).get("url"),
                         "sourceKind": "official" if not row.get("sourceId", "").startswith("candidate_") else "candidate",
                         "observedAt": OBSERVED, "excerpt": row.get("sourceValue"),
                         "configurationMatch": "exact model", "reviewStatus": "CONFLICTING_INFORMATION"},
                    ]
                    current = dict(current)
                    current.update({"status": "CONFLICTING_INFORMATION", "normalizedValue": None,
                                    "note": "Conflicting reviewed source values; withheld from the public catalog pending resolution.",
                                    "candidateEvidence": evidence})
                    if current.get("catalogKey"):
                        current["catalogValue"] = None
                        current["replaceExisting"] = True
                    rows[fid] = current
        for fid, row in rows.items():
            evidence = all_evidence.get(fid, [])
            if evidence:
                row = dict(row)
                row["candidateEvidence"] = list({json.dumps(x, sort_keys=True): x for x in [*row.get("candidateEvidence", []), *evidence]}.values())
                rows[fid] = row
        merged["fields"] = list(rows.values())
        others.append(merged)
    manual["records"] = others


def review_records():
    promo = "https://www.mi.com/ph/support/terms/11-11-mega-sale/"
    records = []

    # Device ID, exact configuration ID, catalog name, official detail/FAQ URLs, price if the
    # campaign lists the tablet itself (not an accessory bundle).
    models = [
        {"id": "device_4da84f0152a569", "variant": "config_6d5db11cec127a", "brand": "Xiaomi", "model": "Pad 8",
         "faq": "https://www.mi.com/ph/support/faq/details/KA-667473/", "spec": "https://www.mi.com/ph/product/xiaomi-pad-8/specs/",
         "price": None, "launch": "2026-02-28", "price_note": "Official campaign lists the 8 GB / 256 GB Pad 8 only in a bundle with its keyboard; no tablet-only price is recorded for this workbook configuration."},
        {"id": "device_6623a9cefc20dc", "variant": "config_49328beb62a309", "brand": "Xiaomi", "model": "Pad 8 Pro",
         "faq": "https://www.mi.com/ph/support/faq/details/KA-667493/", "spec": "https://www.mi.com/ph/product/xiaomi-pad-8-pro/specs/",
         "price": None, "launch": "2026-02-28", "price_note": "Official campaign lists the 8 GB / 256 GB Pad 8 Pro with its Focus Keyboard; the bundle price is not assigned to the tablet-only workbook configuration."},
        {"id": "device_a69d21876446a9", "variant": "config_4b5c4d8d92c12d", "brand": "Xiaomi", "model": "Pad Mini",
         "faq": "https://www.mi.com/ph/support/faq/details/KA-607905/", "spec": "https://www.mi.com/ph/product/xiaomi-pad-mini/specs/",
         "price": 28999, "srp": 29499, "launch": "2025-09-24"},
        {"id": "device_80fc6d91b24f4b", "variant": "config_4efe2baa687b69", "brand": "Redmi", "model": "Pad 2 Pro",
         "faq": "https://www.mi.com/global/support/faq/details/KA-608151/", "spec": "https://www.mi.com/ph/product/redmi-pad-2-pro/specs/",
         "price": 18999, "srp": 21999, "launch": None},
    ]

    for m in models:
        prefix = "xiaomi_" + m["model"].lower().replace(" ", "_").replace("-", "_")
        spec_id, faq_id, price_id = prefix + "_ph_specs", prefix + "_official_faq", "xiaomi_ph_1111_2026_prices"
        sources = [
            src(spec_id, m["spec"], "Official Philippine product specifications",
                f"Official Xiaomi Philippines specifications for {m['brand']} {m['model']}; the page lists the 8 GB + 256 GB configuration."),
            src(faq_id, m["faq"], "Manufacturer FAQ: model-specific technical details and connectivity",
                f"Official manufacturer FAQ for {m['brand']} {m['model']}; values are model-level and cross-checked against the 8 GB / 256 GB configuration.",
                publisher="Xiaomi Global" if m["model"] == "Pad 2 Pro" else "Xiaomi Philippines"),
            src(price_id, promo, "Official Philippine campaign and price table",
                "Mi Technologies Philippines Corporation campaign; price table is valid November 12–26 and November 28–30, 2026 (GMT+8). Accessed November 25, during the listed period."),
        ]
        fields = [
            f("configuration", spec_id, "8 GB + 256 GB", "8 GB RAM / 256 GB storage"),
            pending("philippine_release_date", faq_id,
                    f"FAQ says manufacturer launch date {m['launch'] or 'not listed'} on the /ph or global support page.",
                    "A localized support FAQ gives a model launch date, but does not state that the date is the Philippine launch or first authorized sale. Keep local release date unresolved."),
            f("display_size", spec_id, "11.2 inches" if m["model"].startswith("Pad 8") else "8.8 inches" if m["model"] == "Pad Mini" else "12.1 inches",
              11.2 if m["model"].startswith("Pad 8") else 8.8 if m["model"] == "Pad Mini" else 12.1, key="displayInches", unit="in"),
            f("display_resolution", spec_id,
              "3200 x 2136" if m["model"].startswith("Pad 8") else "3008 x 1880" if m["model"] == "Pad Mini" else "2560 x 1600",
              "3200 x 2136" if m["model"].startswith("Pad 8") else "3008 x 1880" if m["model"] == "Pad Mini" else "2560 x 1600", key="resolution"),
            f("display_refresh_rate", spec_id,
              "Up to 144 Hz" if m["model"].startswith("Pad 8") else "Up to 165 Hz" if m["model"] == "Pad Mini" else "Up to 120 Hz",
              144 if m["model"].startswith("Pad 8") else 165 if m["model"] == "Pad Mini" else 120, key="refreshHz", unit="Hz"),
            f("chipset", spec_id,
              "Snapdragon 8s Gen 4" if m["model"] == "Pad 8" else "Snapdragon 8 Elite" if m["model"] == "Pad 8 Pro" else "MediaTek Dimensity 9400+" if m["model"] == "Pad Mini" else "Snapdragon 7s Gen 4",
              "Snapdragon 8s Gen 4" if m["model"] == "Pad 8" else "Snapdragon 8 Elite" if m["model"] == "Pad 8 Pro" else "MediaTek Dimensity 9400+" if m["model"] == "Pad Mini" else "Snapdragon 7s Gen 4", key="chipset"),
            f("process_node", spec_id, "4 nm" if m["model"] in {"Pad 8", "Pad 2 Pro"} else "3 nm", 4 if m["model"] in {"Pad 8", "Pad 2 Pro"} else 3, unit="nm"),
            f("cpu", spec_id,
              "8-core: 1x Cortex-X4 up to 3.21 GHz + 3x Cortex-A720 up to 3.0 GHz + 2x Cortex-A720 up to 2.8 GHz + 2x Cortex-A720 up to 2.0 GHz" if m["model"] == "Pad 8" else
              "8-core Oryon: 2x 4.32 GHz + 6x 3.53 GHz" if m["model"] == "Pad 8 Pro" else
              "8-core: 1x Cortex-X925 3.73 GHz + 3x Cortex-X4 3.3 GHz + 4x Cortex-A720 2.4 GHz" if m["model"] == "Pad Mini" else
              "8-core: 1x Cortex-A720 2.7 GHz + 3x Cortex-A720 2.4 GHz + 4x Cortex-A520 1.8 GHz",
              "8-core CPU; exact core configuration listed in official source"),
            f("gpu", spec_id, "Adreno 825" if m["model"] == "Pad 8" else "Adreno 830" if m["model"] == "Pad 8 Pro" else "Immortalis-G925 MC12" if m["model"] == "Pad Mini" else "Adreno 810", "Adreno 825" if m["model"] == "Pad 8" else "Adreno 830" if m["model"] == "Pad 8 Pro" else "Immortalis-G925 MC12" if m["model"] == "Pad Mini" else "Adreno 810", key="gpu"),
            f("operating_system", spec_id, "Xiaomi HyperOS 3" if m["model"].startswith("Pad 8") else "Xiaomi HyperOS 2", "Xiaomi HyperOS 3" if m["model"].startswith("Pad 8") else "Xiaomi HyperOS 2", key="os"),
            f("ram_capacity", spec_id, "8 GB RAM", 8, key="ramGb", unit="GB"),
            f("ram_type", spec_id, "LPDDR5X" if m["model"] != "Pad 2 Pro" else "LPDDR4X", "LPDDR5X" if m["model"] != "Pad 2 Pro" else "LPDDR4X", key="ramType"),
            f("storage_capacity", spec_id, "256 GB", 256, key="storageGb", unit="GB"),
            f("storage_type", spec_id, "UFS 4.1" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "UFS 2.2", "UFS 4.1" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "UFS 2.2", key="storageType"),
            f("storage_expansion", faq_id if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else spec_id,
              "No SD card or expandable storage" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "MicroSD expansion supported up to 2 TB",
              "No SD card or expandable storage" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "microSD supported up to 2 TB"),
            f("rear_camera_system", spec_id, "Single rear camera" if m["model"].startswith("Pad 8") else "Rear camera: 13 MP" if m["model"] == "Pad Mini" else "Rear camera: 8 MP", "Single rear camera" if m["model"].startswith("Pad 8") else "13 MP rear camera" if m["model"] == "Pad Mini" else "8 MP rear camera"),
            f("ultrawide_camera", faq_id, "Single rear camera system" if m["model"].startswith("Pad 8") else "Official specification lists only one rear camera", "No ultrawide rear camera listed", status="NOT_APPLICABLE"),
            f("telephoto_camera", faq_id, "Single rear camera system" if m["model"].startswith("Pad 8") else "Official specification lists only one rear camera", "No telephoto rear camera listed", status="NOT_APPLICABLE"),
            f("front_camera", spec_id, "8 MP" if m["model"] in {"Pad 8", "Pad Mini"} else "32 MP" if m["model"] == "Pad 8 Pro" else "8 MP", 8 if m["model"] in {"Pad 8", "Pad Mini"} or m["model"] == "Pad 2 Pro" else 32, key="frontCameraMp", unit="MP"),
            f("video_recording", spec_id,
              "Rear: 4K/30; 1080p/30,60; 720p/30" if m["model"] in {"Pad 8", "Pad Mini"} else "Rear: 4K/30,60; 1080p/30,60; 720p/30" if m["model"] == "Pad 8 Pro" else "Rear: 1080p/30; 720p/30",
              "Rear video up to 4K/30 fps; front video up to 1080p/30 fps" if m["model"] in {"Pad 8", "Pad Mini"} else "Rear video up to 4K/60 fps; front video up to 1080p/30 fps" if m["model"] == "Pad 8 Pro" else "Rear video up to 1080p/30 fps; front video up to 1080p/30 fps", key="video"),
            f("wired_charging", spec_id, "45 W" if m["model"] == "Pad 8" else "67 W" if m["model"] in {"Pad 8 Pro", "Pad Mini"} else "33 W", 45 if m["model"] == "Pad 8" else 67 if m["model"] in {"Pad 8 Pro", "Pad Mini"} else 33, key="chargingW", unit="W"),
            f("battery_technology", faq_id, "Lithium-polymer, dual-cell" if m["model"].startswith("Pad 8") else "Lithium-ion polymer" if m["model"] == "Pad Mini" else "Lithium-polymer, dual-cell", "Lithium-polymer battery"),
            f("dimensions", spec_id,
              "251.22 x 173.42 x 5.75 mm" if m["model"].startswith("Pad 8") else "205.13 x 132.03 x 6.46 mm" if m["model"] == "Pad Mini" else "279.80 x 181.65 x 7.50 mm",
              "251.22 x 173.42 x 5.75 mm" if m["model"].startswith("Pad 8") else "205.13 x 132.03 x 6.46 mm" if m["model"] == "Pad Mini" else "279.80 x 181.65 x 7.50 mm", key="dimensions", unit="mm"),
            f("weight", spec_id, "485 g" if m["model"].startswith("Pad 8") else "326 g" if m["model"] == "Pad Mini" else "610 g", 485 if m["model"].startswith("Pad 8") else 326 if m["model"] == "Pad Mini" else 610, key="weightG", unit="g"),
            f("sim_esim", faq_id, "No SIM card or eSIM support", "No physical SIM or eSIM", key="sim"),
            f("tablet_cellular_variant", faq_id, "No mobile network support; Wi-Fi model", "Wi-Fi only; no cellular radio", key="cellular"),
            f("cellular_bands", faq_id, "No mobile network support", "No cellular radio"),
            f("wifi", faq_id if m["model"].startswith("Pad 8") else spec_id,
              "Wi-Fi 7" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "Wi-Fi 6",
              "Wi-Fi 7" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "Wi-Fi 6", key="wifi"),
            f("bluetooth", faq_id if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else spec_id, "Bluetooth 6.0" if m["model"].startswith("Pad 8") else "Bluetooth 5.4", "Bluetooth 6.0" if m["model"].startswith("Pad 8") else "Bluetooth 5.4"),
            f("usb", spec_id,
              "USB Type-C, USB 3.2 Gen 1 (up to 5 Gbps)" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "USB Type-C, USB 2.0",
              "USB Type-C, USB 3.2 Gen 1" if m["model"].startswith("Pad 8") or m["model"] == "Pad Mini" else "USB Type-C, USB 2.0", key="ports"),
            f("audio", faq_id,
              "Dual speakers; Type-C headphone jack" if m["model"] == "Pad Mini" else "Quad speakers; Dolby Atmos",
              "Dual speakers; Type-C headphone output" if m["model"] == "Pad Mini" else "Quad speakers; Dolby Atmos", key="sound"),
        ]
        if m["model"] != "Pad Mini":
            fields.append(f("display_technology", faq_id,
                            "LCD screen" if m["model"].startswith("Pad 8") else "LCD",
                            "LCD", key="displayType"))
        else:
            fields.extend([
                f("display_technology", faq_id, "LCD hard screen", "LCD", key="displayType"),
                f("display_protection", faq_id, "Corning Gorilla Glass 5", "Corning Gorilla Glass 5"),
                f("display_brightness", faq_id, "700 nits HBM; 600 nits manually adjustable maximum", "700 nits HBM; 600 nits typical", unit="nits"),
            ])
        if m["model"] == "Pad 2 Pro":
            fields.extend([
                f("display_brightness", faq_id, "500 nits typical; 600 nits HBM", "500 nits typical; 600 nits HBM", unit="nits"),
                f("display_protection", faq_id, "Corning Gorilla Glass 3", "Corning Gorilla Glass 3"),
                f("ingress_protection", faq_id, "IP53", "IP53"),
            ])
        if m["model"] in {"Pad 8", "Pad 8 Pro"}:
            fields.extend([
                f("tablet_stylus", faq_id, "Supports Xiaomi Focus Pen Pro", "Xiaomi Focus Pen Pro supported"),
                f("tablet_keyboard", faq_id, "Supports Xiaomi Pad 8 / 8 Pro Focus Keyboard", "Xiaomi Pad 8 / 8 Pro Focus Keyboard supported"),
                f("display_protection", faq_id, "Panda-X glass", "Panda-X glass"),
                f("nfc", faq_id, "Pad 8 supports NFC tags/transfers but not payments" if m["model"] == "Pad 8" else "Does not support NFC", "NFC tags/transfers; no payment" if m["model"] == "Pad 8" else "No NFC"),
                f("display_brightness", faq_id, "FAQ states typical 6000 nits and maximum 800 nits; product spec states 800 nits peak", None,
                  status="CONFLICTING_INFORMATION", unit="nits",
                  note="The official FAQ's 6000-nit typical figure conflicts with its 800-nit maximum and the product specification's 800-nit peak figure. Brightness is withheld pending Xiaomi clarification."),
            ])
            fields.append(f("battery_capacity", spec_id, "9200 mAh (typical)", None,
                            status="CONFLICTING_INFORMATION", key="batteryMah", unit="mAh",
                            note="Official product specs say 9200 mAh typical; official FAQ says rated 9200 mAh and typical 9000 mAh. Public battery value is cleared until Xiaomi resolves the contradiction."))
            battery_conflict = next(x for x in fields if x["fieldId"] == "battery_capacity")
            battery_conflict["candidateEvidence"] = [
                {"value": "9200 mAh (typical)", "unit": "mAh", "sourceUrl": m["spec"],
                 "sourceKind": "official", "observedAt": OBSERVED, "excerpt": "Battery&charging: 9200mAh (typ)",
                 "configurationMatch": "exact model", "reviewStatus": "CONFLICTING_INFORMATION"},
                {"value": "9200 mAh rated; 9000 mAh typical", "unit": "mAh", "sourceUrl": m["faq"],
                 "sourceKind": "official", "observedAt": OBSERVED,
                 "excerpt": "FAQ battery specification: rated capacity 9200 mAh and typical capacity 9000 mAh",
                 "configurationMatch": "exact model", "reviewStatus": "CONFLICTING_INFORMATION"},
            ]
            brightness_conflict = next(x for x in fields if x["fieldId"] == "display_brightness")
            brightness_conflict["candidateEvidence"] = [
                {"value": "800 nits peak brightness", "unit": "nits", "sourceUrl": m["spec"],
                 "sourceKind": "official", "observedAt": OBSERVED, "excerpt": "800 nits peak brightness",
                 "configurationMatch": "exact model", "reviewStatus": "CONFLICTING_INFORMATION"},
                {"value": "6000 nits typical; 800 nits maximum", "unit": "nits", "sourceUrl": m["faq"],
                 "sourceKind": "official", "observedAt": OBSERVED,
                 "excerpt": "FAQ reports 6000 nits typical and 800 nits maximum",
                 "configurationMatch": "exact model", "reviewStatus": "CONFLICTING_INFORMATION"},
            ]
        else:
            fields.append(f("battery_capacity", spec_id, "7500 mAh (typical)" if m["model"] == "Pad Mini" else "12000 mAh (typical)",
                            7500 if m["model"] == "Pad Mini" else 12000, key="batteryMah", unit="mAh"))
        if m["model"] == "Pad Mini":
            fields.extend([
                f("tablet_stylus", faq_id, "Supports Xiaomi Focus Pen", "Xiaomi Focus Pen supported"),
                f("nfc", faq_id, "Does not support NFC", "No NFC"),
                f("wireless_charging", faq_id, "Does not support wireless charging; reverse wireless charging up to 3 W for stylus", "No wireless charging; reverse wireless up to 3 W for stylus"),
            ])
        if m.get("price"):
            fields.append(f("current_price_php", price_id,
                            f"8 GB + 256 GB: SRP PHP {m['srp']:,}; campaign price PHP {m['price']:,}",
                            m["price"], unit="PHP", price_condition="new",
                            price_type="Official Philippine 11.11 campaign promotional price; valid Nov 12–26 and Nov 28–30, 2026",
                            price_observed=OBSERVED,
                            note="Exact 8 GB / 256 GB device row in Xiaomi Philippines' active campaign table on the observation date; the price is a dated promotion, not a permanent price."))
        else:
            fields.append(pending("current_price_php", price_id, "The 8 GB + 256 GB campaign listing is an accessory bundle.", m["price_note"], "PHP"))
        for reviewed_field in fields:
            if reviewed_field["fieldId"] == "display_resolution" and reviewed_field["status"] == "VERIFIED":
                # Normalize multiplication-sign variations in the source workbook to ASCII x.
                reviewed_field["replaceExisting"] = True
        records.append({"deviceId": m["id"], "configurationId": m["variant"], "brand": m["brand"], "model": m["model"],
                        "configuration": "8 GB RAM / 256 GB storage", "sources": sources, "fields": fields})
    records.append(redmi_5g_review(promo))
    return records


def redmi_5g_review(promo):
    device_id = "device_c40842fa2183ab"
    configuration_id = "device_c40842fa2183ab-redmi-pad-2-pro-5g-8-256"
    spec_url = "https://www.mi.com/ph/product/redmi-pad-2-pro-5g/specs/"
    faq_url = "https://www.mi.com/global/support/faq/details/KA-611514/"
    spec_id, faq_id, price_id = "redmi_pad_2_pro_5g_ph_specs", "redmi_pad_2_pro_5g_official_faq", "xiaomi_ph_1111_2026_prices"
    sources = [
        src(spec_id, spec_url, "Official Philippine 5G model specifications",
            "Official Xiaomi Philippines specification page identifies REDMI Pad 2 Pro 5G, the 8 GB + 256 GB configuration, and local 5G/eSIM support."),
        src(faq_id, faq_url, "Manufacturer FAQ: exact 5G model connectivity and technical details",
            "Official Xiaomi FAQ specifically for REDMI Pad 2 Pro 5G. eSIM availability can vary by region; the Philippine product page is checked separately.",
            publisher="Xiaomi Global"),
        src(price_id, promo, "Official Philippine campaign and price table",
            "Mi Technologies Philippines Corporation campaign; price table is valid November 12–26 and November 28–30, 2026 (GMT+8). Accessed November 25, during the listed period."),
    ]
    fields = [
        f("configuration", spec_id, "8 GB + 256 GB", "8 GB RAM / 256 GB storage"),
        pending("philippine_release_date", faq_id, "No Philippine first-sale date is stated in the cited pages.",
                "Official Philippine listing and active Philippine sale verify local listing, but neither source establishes the Philippine launch or first-sale date."),
        f("display_size", spec_id, "12.1 inches", 12.1, key="displayInches", unit="in"),
        f("display_technology", faq_id, "LCD", "LCD", key="displayType"),
        f("display_resolution", spec_id, "2560 x 1600", "2560 x 1600", key="resolution", note="Official source normalized to width x height."),
        f("display_refresh_rate", spec_id, "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", spec_id, "500 nits typical; 600 nits HBM", "500 nits typical; 600 nits HBM", unit="nits"),
        f("display_protection", faq_id, "Corning Gorilla Glass 3", "Corning Gorilla Glass 3"),
        f("chipset", spec_id, "Snapdragon 7s Gen 4", "Snapdragon 7s Gen 4", key="chipset"),
        f("process_node", spec_id, "4 nm", 4, unit="nm"),
        f("cpu", spec_id, "8-core: 1x Cortex-A720 2.7 GHz + 3x Cortex-A720 2.4 GHz + 4x Cortex-A520 1.8 GHz", "8-core CPU; exact core configuration listed in official source"),
        f("gpu", spec_id, "Adreno 810", "Adreno 810", key="gpu"),
        f("operating_system", spec_id, "Xiaomi HyperOS 2", "Xiaomi HyperOS 2", key="os"),
        f("ram_capacity", spec_id, "8 GB", 8, key="ramGb", unit="GB"),
        f("ram_type", spec_id, "LPDDR4X", "LPDDR4X", key="ramType"),
        f("storage_capacity", spec_id, "256 GB", 256, key="storageGb", unit="GB"),
        f("storage_type", spec_id, "UFS 2.2", "UFS 2.2", key="storageType"),
        f("storage_expansion", spec_id, "MicroSD expandable up to 2 TB", "microSD supported up to 2 TB"),
        f("rear_camera_system", spec_id, "13 MP rear camera", 13, key="rearCameraMp", unit="MP"),
        f("ultrawide_camera", faq_id, "Official FAQ identifies a single rear camera", "No ultrawide rear camera listed", status="NOT_APPLICABLE"),
        f("telephoto_camera", faq_id, "Official FAQ identifies a single rear camera", "No telephoto rear camera listed", status="NOT_APPLICABLE"),
        f("front_camera", spec_id, "8 MP", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", spec_id, "Rear 1080p up to 60 fps; front 1080p up to 30 fps", "Rear video up to 1080p/60 fps; front up to 1080p/30 fps", key="video"),
        f("battery_capacity", spec_id, "12000 mAh typical", 12000, key="batteryMah", unit="mAh"),
        f("battery_technology", faq_id, "Dual-cell lithium-polymer battery; rated capacity 11800 mAh, typical 12000 mAh", "Dual-cell lithium-polymer; 11800 mAh rated / 12000 mAh typical"),
        f("wired_charging", spec_id, "33 W", 33, key="chargingW", unit="W"),
        f("dimensions", spec_id, "279.80 x 181.65 x 7.50 mm", "279.80 x 181.65 x 7.50 mm", key="dimensions", unit="mm"),
        f("weight", spec_id, "600 g", 600, key="weightG", unit="g"),
        f("sim_esim", spec_id, "Dual SIM slot; nano SIM + nano SIM or nano SIM + eSIM; eSIM availability may vary by region", "Dual nano-SIM or nano-SIM + eSIM; regional eSIM availability applies", key="sim"),
        f("cellular_bands", spec_id, "5G SA/NSA; supported bands are listed on the official Philippine specification page", "5G SA/NSA; bands listed on source page"),
        f("tablet_cellular_variant", spec_id, "REDMI Pad 2 Pro 5G; 5G + eSIM", "5G cellular; eSIM availability varies by region", key="cellular"),
        f("wifi", spec_id, "Wi-Fi 6", "Wi-Fi 6", key="wifi"),
        f("bluetooth", spec_id, "Bluetooth 5.4", "Bluetooth 5.4"),
        f("usb", spec_id, "USB Type-C, USB 2.0", "USB Type-C, USB 2.0", key="ports"),
        f("audio", faq_id, "Quad speakers; 3.5 mm headphone jack; Dolby Atmos", "Quad speakers; 3.5 mm headphone jack; Dolby Atmos", key="sound"),
        f("current_price_php", price_id, "8 GB + 256 GB: SRP PHP 24,999; campaign price PHP 21,999", 21999, unit="PHP",
          price_condition="new", price_type="Official Philippine 11.11 campaign promotional price; valid Nov 12–26 and Nov 28–30, 2026",
          price_observed=OBSERVED,
          note="Exact REDMI Pad 2 Pro 5G 8 GB + 256 GB rows in Xiaomi Philippines' active campaign table; dated promotional price."),
    ]
    return {
        "deviceId": device_id, "configurationId": configuration_id, "brand": "Redmi", "model": "Pad 2 Pro 5G",
        "configuration": "8 GB RAM / 256 GB storage", "sources": sources,
        "replacementVariants": [{"id": configuration_id, "label": "8 GB RAM / 256 GB storage", "sku": None,
                                 "modelCode": None, "notes": "Configuration identified from Xiaomi Philippines official product page and 8 GB + 256 GB local campaign listing."}],
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Listed on official Xiaomi Philippines product page and official Philippine sale campaign; observed 2026-11-25.",
            "philippineAvailability": "Official Xiaomi Philippines product and active campaign pages list the 5G model and its 8 GB + 256 GB configuration.",
            "observedAt": OBSERVED,
            "qualityFlag": "Philippine launch or first-sale date not recorded",
        },
        "fields": fields,
    }


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    records = review_records()
    for item in records:
        add_review(manual, catalog, item)
    deduplicate_target_reviews(manual, {(r["deviceId"], r["configurationId"]) for r in records})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"tabletConfigurationsReviewed": len(records), "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
