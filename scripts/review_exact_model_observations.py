#!/usr/bin/env python3
"""Promote safe model-wide technical observations after exact-page checks.

This deliberately excludes prices, launch/availability dates, RAM/storage,
cellular/SIM and software-version claims. Those require exact variant or local
market evidence. A source must have passed the collector's exact-model page
check and be either an official manufacturer or Pinoy Techno Guide page.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "research/enrichment/latest.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
FIELDS = ROOT / "research/enrichment/specification-fields.json"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
REVIEWED_AT = "2026-11-26"

OFFICIAL_HOSTS = {
    "apple.com", "samsung.com", "mi.com", "asus.com", "acer.com", "lenovo.com",
    "huawei.com", "honor.com", "oppo.com", "vivo.com", "realme.com", "tecno-mobile.com",
    "infinixmobility.com", "motorola.com", "nokia.com", "oneplus.com", "nothing.tech",
    "poco.com", "redmi.com", "google.com", "dell.com", "hp.com", "msi.com",
    "gigabyte.com", "framework.com", "razer.com",
}
PTG_HOST = "www.pinoytechnoguide.com"

# Only facts that normally stay constant across RAM/storage configurations.
# The collector's regional/model match is not treated as proof of Philippine
# availability, exact market configuration, a dated launch, or a current price.
KEY_TO_FIELD = {
    "display_inches": "display_size", "display_technology": "display_technology",
    "resolution": "display_resolution", "refresh_hz": "display_refresh_rate",
    "display_brightness": "display_brightness", "display_protection": "display_protection",
    "chipset": "chipset", "cpu": "cpu", "gpu": "gpu", "battery_mah": "battery_capacity",
    "battery_technology": "battery_technology", "charging": "wired_charging",
    "dimensions": "dimensions", "weight": "weight", "materials": "materials",
    "ip_rating": "ingress_protection", "wifi": "wifi", "bluetooth": "bluetooth",
    "nfc": "nfc", "ports": "usb", "storage_expansion": "storage_expansion",
    "front_camera": "front_camera", "rear_camera": "rear_camera_system",
    "main_camera_sensor": "main_camera_sensor", "ultrawide_camera": "ultrawide_camera",
    "telephoto_camera": "telephoto_camera", "video_recording": "video_recording",
    "audio": "audio", "sensors": "sensors", "gnss": "gnss",
    "tablet_stylus": "tablet_stylus", "keyboard": "tablet_keyboard",
}
EXCLUDED_KEYS = {
    "ram_gb", "internal_storage_gb", "ram_type", "storage_type", "operating_system",
    "battery_wh", "sim", "cellular",
}
NUMERIC_KEYS = {"display_inches", "refresh_hz", "battery_mah", "weight", "charging", "front_camera"}
NUMERIC_CATALOG_KEYS = {"displayInches", "refreshHz", "batteryMah", "weightG", "chargingW", "frontCameraMp"}


def tidy(value) -> str | None:
    if value is None:
        return None
    text = unicodedata.normalize("NFKC", str(value)).replace("×", "x")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def canonical(value, key: str) -> str:
    text = (tidy(value) or "").replace(",", "")
    if key in NUMERIC_KEYS:
        numbers = re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", text)
        if len(numbers) == 1:
            try:
                return str(Decimal(numbers[0]).normalize())
            except InvalidOperation:
                pass
    return re.sub(r"[^a-z0-9.+-]+", " ", text.casefold()).strip()


def typed_catalog_value(value, key: str, catalog_key: str):
    text = tidy(value)
    if not text:
        return None
    if catalog_key not in NUMERIC_CATALOG_KEYS:
        return text
    numbers = re.findall(r"(?<![A-Za-z])\d+(?:[.,]\d+)?", text.replace(",", ""))
    if len(numbers) != 1:
        return None
    try:
        number = Decimal(numbers[0])
    except InvalidOperation:
        return None
    return int(number) if number == number.to_integral_value() else float(number)


def source_class(row: dict) -> str | None:
    try:
        url = urlparse(row.get("source_url", ""))
    except ValueError:
        return None
    if url.scheme != "https":
        return None
    host = (url.hostname or "").lower()
    kind = row.get("source_kind")
    if kind == "independent_ph_reference" and host == PTG_HOST and re.fullmatch(r"/(smartphones|tablets)/[a-z0-9-]+/?", url.path):
        return "VERIFIED_SECONDARY"
    if kind == "official" and any(host == allowed or host.endswith("." + allowed) for allowed in OFFICIAL_HOSTS):
        return "VERIFIED"
    return None


def make_source(row: dict, status: str) -> dict:
    url = row["source_url"]
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:14]
    host = urlparse(url).hostname or "Source"
    observed = str(row.get("observed_at") or REVIEWED_AT)
    try:
        observed = datetime.fromisoformat(observed.replace("Z", "+00:00")).astimezone(timezone(timedelta(hours=8))).date().isoformat()
    except ValueError:
        observed = REVIEWED_AT
    return {
        "id": f"reviewed_model_source_{digest}",
        "publisher": host.removeprefix("www."),
        "url": url,
        "publicationDate": None,
        "accessDate": observed,
        "purpose": "Exact-model technical specification reference",
        "note": ("The page passed the collector's exact model heading check. This reference supports technical specifications only; it does not establish Philippine availability, local launch date, or price."),
    }


def main():
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    definitions = json.loads(FIELDS.read_text(encoding="utf-8"))
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    devices = {row["id"]: row for row in catalog if row.get("recordType", "device") == "device"}
    field_definitions = {
        category: {field["id"]: field for field in rows}
        for category, rows in definitions.items() if category in {"smartphones", "tablets", "laptops"}
    }
    extracted_pages = {
        (row.get("device_id"), row.get("source_url"))
        for row in latest.get("fetches", []) if row.get("status") == "extracted"
    }

    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in latest.get("observations", []):
        device = devices.get(row.get("device_id"))
        key = row.get("key")
        field_id = KEY_TO_FIELD.get(key)
        if not device or not field_id or key in EXCLUDED_KEYS:
            continue
        if field_id not in field_definitions.get(device.get("category"), {}):
            continue
        if (device["id"], row.get("source_url")) not in extracted_pages:
            continue
        status = source_class(row)
        value = tidy(row.get("value"))
        if not status or not value:
            continue
        groups[(device["id"], field_id)].append({**row, "_review_status": status, "_canonical": canonical(value, key)})

    reviews_by_key: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for review in manual.get("records", []):
        reviews_by_key[(review["deviceId"], review["configurationId"])].append(review)

    latest_access_by_url = {}
    for row in latest.get("observations", []):
        url, observed = row.get("source_url"), row.get("observed_at")
        if url and observed and observed >= latest_access_by_url.get(url, ""):
            latest_access_by_url[url] = observed
    for review in manual.get("records", []):
        for source in review.get("sources", []):
            if source.get("id", "").startswith("reviewed_model_source_") and source.get("url") in latest_access_by_url:
                source["accessDate"] = make_source({"source_url": source["url"], "observed_at": latest_access_by_url[source["url"]]}, "VERIFIED_SECONDARY")["accessDate"]

    stats = {"modelsWithEvidence": 0, "fieldsAdded": 0, "primaryFields": 0, "secondaryFields": 0,
             "conflictingFieldsLeftPending": 0, "catalogValueMismatchesLeftPending": 0,
             "existingReviewsPreserved": 0}
    for (device_id, field_id), candidates in groups.items():
        device = devices[device_id]
        # Avoid counting repeated extraction of the same fact from the same page.
        unique = {}
        for candidate in candidates:
            unique[(candidate["source_url"], candidate["_canonical"], candidate.get("unit"))] = candidate
        candidates = list(unique.values())
        if not candidates:
            continue
        values = {row["_canonical"] for row in candidates}
        if len(values) != 1:
            stats["conflictingFieldsLeftPending"] += 1
            continue
        candidates.sort(key=lambda row: (row["_review_status"] != "VERIFIED", row.get("source_url", "")))
        chosen = candidates[0]
        status = chosen["_review_status"]
        definition = field_definitions[device["category"]][field_id]
        catalog_key = definition.get("catalogKey")
        value = tidy(chosen.get("value"))
        normalized_value = value
        catalog_value = None
        if catalog_key:
            catalog_value = typed_catalog_value(value, chosen["key"], catalog_key)
            if catalog_value is not None:
                existing_values = [variant.get("specs", {}).get(catalog_key) for variant in device.get("variants", [])]
                existing_values = [existing for existing in existing_values if existing is not None]
                if any(str(existing) != str(catalog_value) for existing in existing_values):
                    stats["catalogValueMismatchesLeftPending"] += 1
                    continue
                normalized_value = catalog_value

        source_id = make_source(chosen, status)["id"]
        note = (
            "Exact model page checked. This is a model-level technical fact shared across RAM/storage configurations; "
            "variant-specific fields, Philippine release/availability, and prices were not inferred. "
            + ("Primary manufacturer source." if status == "VERIFIED" else "Independent Philippine reference; manufacturer cross-check remains desirable.")
        )
        source_rows = []
        for candidate in candidates:
            source = make_source(candidate, candidate["_review_status"])
            if not any(existing["id"] == source["id"] for existing in source_rows):
                source_rows.append(source)
        field_row = {
            "fieldId": field_id,
            "status": status,
            "sourceId": source_id,
            "sourceValue": value,
            "normalizedValue": normalized_value,
            "unit": chosen.get("unit") or definition.get("unit") or None,
            "note": note,
            "configurationMatch": "exact model; shared model-level field",
        }
        if catalog_key and catalog_value is not None:
            field_row["catalogKey"] = catalog_key
            field_row["catalogValue"] = catalog_value
        # Preserve alternate same-value references in the audit trail.
        alternate_evidence = []
        for candidate in candidates:
            if candidate["source_url"] == chosen["source_url"]:
                continue
            alternate_evidence.append({
                "value": tidy(candidate.get("value")), "unit": candidate.get("unit"),
                "sourceUrl": candidate.get("source_url"), "sourceKind": candidate.get("source_kind"),
                "observedAt": candidate.get("observed_at"), "excerpt": tidy(candidate.get("excerpt")),
                "configurationMatch": "exact model; shared model-level field",
                "reviewStatus": candidate["_review_status"],
                "localAvailabilityVerified": False,
            })
        if alternate_evidence:
            field_row["candidateEvidence"] = alternate_evidence

        field_added_for_model = False
        for variant in device.get("variants", []):
            config_id = variant.get("id")
            key = (device_id, config_id)
            review_rows = reviews_by_key.get(key, [])
            existing_field_ids = {field.get("fieldId") for review in review_rows for field in review.get("fields", [])}
            if field_id in existing_field_ids:
                stats["existingReviewsPreserved"] += 1
                continue
            if not review_rows:
                review = {
                    "deviceId": device_id, "configurationId": config_id,
                    "brand": device.get("brand"), "model": device.get("model"),
                    "configuration": variant.get("label"), "configurationLabel": variant.get("label"),
                    "sources": [], "fields": [],
                }
                manual["records"].append(review)
                reviews_by_key[key].append(review)
                review_rows = [review]
            review = review_rows[-1]
            known_source_ids = {source.get("id") for source in review.get("sources", [])}
            for source in source_rows:
                if source["id"] not in known_source_ids:
                    review["sources"].append(source)
                    known_source_ids.add(source["id"])
            review["fields"].append(dict(field_row))
            stats["fieldsAdded"] += 1
            if status == "VERIFIED":
                stats["primaryFields"] += 1
            else:
                stats["secondaryFields"] += 1
            field_added_for_model = True
        if field_added_for_model:
            stats["modelsWithEvidence"] += 1

    manual["reviewedAt"] = REVIEWED_AT
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**stats, "latestRunAt": latest.get("run_at"), "reviewedAt": REVIEWED_AT}, indent=2))


if __name__ == "__main__":
    main()
