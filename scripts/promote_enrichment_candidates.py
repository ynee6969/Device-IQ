#!/usr/bin/env python3
"""Promote only exact-model, source-backed enrichment observations.

The collector records candidates without touching the public catalog. This
review pass creates explicit field reviews for accepted pages. Model-level
fields can be reused across a model's configurations; RAM, storage and prices
require an exact RAM/storage pair. Conflicting catalog values stay unresolved.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
LATEST = ROOT / "research/enrichment/latest.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
AUDIT = ROOT / "research/enrichment/specification-field-audit.json"

KEY_TO_FIELD = {
    "battery_mah": "battery_capacity",
    "ram_gb": "ram_capacity",
    "internal_storage_gb": "storage_capacity",
    "display_inches": "display_size",
    "chipset": "chipset",
    "cpu": "cpu",
    "gpu": "gpu",
    "operating_system": "operating_system",
    "resolution": "display_resolution",
    "refresh_hz": "display_refresh_rate",
    "weight": "weight",
    "dimensions": "dimensions",
    "charging": "wired_charging",
    "wifi": "wifi",
    "bluetooth": "bluetooth",
    "nfc": "nfc",
    "sim": "sim_esim",
    "front_camera": "front_camera",
    "rear_camera": "rear_camera_system",
    "ip_rating": "ingress_protection",
    "display_technology": "display_technology",
    "display_brightness": "display_brightness",
    "display_protection": "display_protection",
    "display_color": "display_color",
    "battery_technology": "battery_technology",
    "materials": "materials",
    "storage_expansion": "storage_expansion",
    "ram_type": "ram_type",
    "storage_type": "storage_type",
    "main_camera_sensor": "main_camera_sensor",
    "ultrawide_camera": "ultrawide_camera",
    "telephoto_camera": "telephoto_camera",
    "video_recording": "video_recording",
    "cellular": "cellular_bands",
    "gnss": "gnss",
    "audio": "audio",
    "sensors": "sensors",
    "usb": "usb",
    "webcam": "webcam",
    "battery_life": "battery_life",
    "keyboard": "keyboard",
    "touchpad": "touchpad",
    "ethernet": "ethernet",
    "warranty": "warranty",
    "touchscreen": "touchscreen",
    "tablet_stylus": "tablet_stylus",
    "tablet_keyboard": "tablet_keyboard",
    "ports": "usb",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_id(url: str) -> str:
    import hashlib
    return "candidate_" + hashlib.sha256(url.encode("utf-8")).hexdigest()[:14]


def source_publisher(url: str, kind: str) -> str:
    host = urlparse(url).hostname or ""
    if "pinoytechnoguide.com" in host:
        return "Pinoy Techno Guide"
    if host.endswith("mi.com"):
        return "Xiaomi Philippines"
    if host.endswith("samsung.com"):
        return "Samsung Philippines"
    if host.endswith("asus.com"):
        return "ASUS"
    if host.endswith("oppo.com"):
        return "OPPO"
    return host or ("Manufacturer" if kind == "official" else "Secondary source")


def source_record(url: str, kind: str, published: str | None, observed: str):
    return {
        "id": source_id(url),
        "publisher": source_publisher(url, kind),
        "url": url,
        "publicationDate": published,
        "accessDate": (observed or date.today().isoformat())[:10],
        "purpose": "Exact-model specification evidence; configuration-sensitive values are matched separately.",
        "note": "The collector accepted the page after an exact model heading/title match. Local availability and unrelated variants are not inferred.",
    }


def config_pair(variant: dict) -> tuple[int, int] | None:
    specs = variant.get("specs") or {}
    ram, storage = specs.get("ramGb"), specs.get("storageGb")
    if ram is None or storage is None:
        m = re.search(r"(\d+)\s*GB.*?(\d+)\s*GB", variant.get("label", ""), re.I)
        if m:
            ram, storage = map(int, m.groups())
    try:
        return (int(ram), int(storage)) if ram is not None and storage is not None else None
    except (TypeError, ValueError):
        return None


def number(value):
    try:
        parsed = float(value)
        return int(parsed) if parsed.is_integer() else parsed
    except (TypeError, ValueError):
        return None


def normalized_compare(value, field_id=None):
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value or "").casefold()
    text = text.replace(chr(0x00c3) + chr(0x2014), "x").replace(chr(0x00e3) + chr(0x2014), "x").replace(chr(0x00d7), "x").replace(chr(0xfffd), "x")
    if field_id == "display_resolution":
        match = re.search(r"\b(\d{3,4})\s*[x×]\s*(\d{3,4})\b", text)
        if match:
            return "x".join(map(str, sorted((int(match.group(1)), int(match.group(2))))))
    if field_id == "dimensions":
        numbers = re.findall(r"\d+(?:\.\d+)?", text)
        if numbers:
            return "dimensions:" + ",".join(sorted(numbers, key=float))
    if field_id == "cpu":
        core = re.search(r"\b(\d+)\s*[- ]?core", text)
        if not core:
            word_cores = {"single": 1, "dual": 2, "quad": 4, "hexa": 6, "octa": 8, "deca": 10, "dodeca": 12, "tetradeca": 14, "icosa": 20, "tetracosa": 24}
            core = next((re.match(r"(\d+)", str(count)) for word, count in word_cores.items() if re.search(rf"\b{word}[- ]?core\b", text)), None)
            core_count = int(core.group(1)) if core else None
        else:
            core_count = int(core.group(1))
        frequencies = [float(item) for item in re.findall(r"\b(\d+(?:\.\d+)?)\s*ghz\b", text)]
        if core_count is not None or frequencies:
            return f"cores={core_count};maxghz={max(frequencies) if frequencies else ''}"
    if field_id == "gpu":
        text = re.sub(r"\s*@\s*\d+(?:\.\d+)?\s*(?:ghz|mhz)\b", " ", text)
        text = re.sub(r"\b(?:gpu|graphics|graphics processor)\b", " ", text)
        if re.search(r"\bmali\s*-?\s*g57\s+m[cp]\s*2\b", text):
            return "malig572core"
    if field_id == "chipset":
        text = re.sub(r"\b(?:qualcomm|mediatek|mobile platform|flagship)\b", " ", text)
        text = re.sub(r"\(\s*\d+\s*nm\s*\)", " ", text)
    if field_id == "wifi":
        standards = set()
        for found in re.findall(r"802\.11\s*([a-z]+(?:/[a-z]+)*)", text):
            standards.update(found.split("/"))
        standards.update(re.findall(r"\b(?:wi-?fi\s*)?(5|6e|6|7)\b", text))
        if standards:
            ranks = {"7": 7, "be": 7, "6e": 6, "6": 6, "ax": 6, "5": 5, "ac": 5, "4": 4, "n": 4}
            rank = max((ranks.get(item, 0) for item in standards), default=0)
            if rank:
                return f"wifi{rank}"
    if field_id in {"cellular_bands", "cellular"}:
        generations = set(re.findall(r"\b[2-5]\s*g\b", text))
        if generations:
            return ",".join(sorted(generations))
    if field_id == "video_recording":
        resolutions = recording_resolutions(value)
        if resolutions:
            return "video:" + ",".join(sorted(resolutions, key=resolution_rank))
    if field_id == "nfc":
        if re.search(r"\b(no|not supported|unsupported)\b", text):
            return "nfc-no"
        if re.search(r"\b(yes|support|supported)\b", text):
            return "nfc-yes"
    if field_id == "sim_esim":
        tokens = set()
        if re.search(r"\bdual\b", text): tokens.add("dual")
        if re.search(r"\btriple\b", text): tokens.add("triple")
        if re.search(r"\bnano\s*-?\s*sim\b", text): tokens.add("nano-sim")
        if re.search(r"\bmicro\s*-?\s*sim\b", text): tokens.add("micro-sim")
        if re.search(r"\be\s*-?\s*sim\b", text): tokens.add("esim")
        if tokens:
            return ",".join(sorted(tokens))
    if field_id == "operating_system":
        custom_tokens = []
        for family in ("hyperos", "harmonyos", "coloros", "oxygenos", "funtouchos", "hios", "one ui", "ipados", "ios", "windows"):
            match = re.search(rf"\b{re.escape(family)}\s*(\d+)(?:\.\d+)?", text)
            if match:
                custom_tokens.append(f"{family.replace(' ', '')}{match.group(1)}")
            elif re.search(rf"\b{re.escape(family)}\b", text):
                custom_tokens.append(f"{family.replace(' ', '')}")
        if custom_tokens:
            return ",".join(sorted(set(custom_tokens)))
        os_tokens = [f"{family}{match.group(1)}" for family in ("android",)
                     if (match := re.search(rf"\b{family}\s*(\d+)(?:\.\d+)?", text))]
        if os_tokens:
            return ",".join(os_tokens)
    if field_id == "rear_camera_system":
        megapixels = set(re.findall(r"\b(\d+(?:\.\d+)?)\s*mp\b", text))
        if megapixels:
            return "camera-mp:" + ",".join(sorted(megapixels, key=float))
    if field_id == "sensors":
        tokens = sensor_tokens(value)
        if tokens:
            return "sensors:" + ",".join(sorted(tokens))
    if field_id == "audio":
        return "audio-compatible"
    text = re.sub(r"\s*@\s*\d+(?:\.\d+)?\s*(?:ghz|mhz)\b", " ", text)
    text = re.sub(r"\b(?:mobile platform|processor|cpu|gpu|display|technology|video recording|with|the)\b", " ", text)
    text = re.sub(r"\b(?:android|windows)\s+", lambda m: m.group(0).strip() + " ", text)
    return re.sub(r"[^a-z0-9]+", "", text)


def sensor_tokens(value):
    text = str(value or "").casefold().replace("x-axis", "xaxis")
    text = re.sub(r"\b(?:front|rear)\b", "", text)
    parts = re.split(r"[|,;/+]+", text)
    ignored = {"sensor", "sensors", "and", "with", "the"}
    result = set()
    for part in parts:
        token = re.sub(r"[^a-z0-9]+", "", part)
        token = token.replace("flickersenor", "flickersensor")
        if token and token not in ignored:
            token = re.sub(r"sensor$", "", token)
            result.add(token)
    return result


def recording_resolutions(value):
    text = str(value or "").casefold()
    if "format" in text and not re.search(r"\b(?:\d{3,4}p|\d+k|\d{3,4}\s*x\s*\d{3,4}|fps|frame)\b", text):
        return set()
    return set(recording_features(value))


def recording_features(value):
    text = str(value or "").casefold()
    if "format" in text and not re.search(r"\b(?:\d{3,4}p|\d+k|\d{3,4}\s*x\s*\d{3,4}|fps|frame)\b", text):
        return {}
    found = {}
    for match in re.finditer(r"\b(\d{1,2})\s*k(?:\s*@?\s*(\d{2,3})\s*fps?|\s*(\d{2,3}))?\b", text):
        fps = match.group(2) or match.group(3)
        found[f"{match.group(1)}k"] = int(fps) if fps else None
    for match in re.finditer(r"\b(\d{3,4})\s*p(?:\s*@?\s*(\d{2,3})\s*fps?|\s*(\d{2,3}))?\b", text):
        fps = match.group(2) or match.group(3)
        found[f"{match.group(1)}p"] = int(fps) if fps else None
    for width, height in re.findall(r"\b(\d{3,4})\s*x\s*(\d{3,4})\b", text):
        key = "8k" if int(width) >= 7000 else "4k" if int(width) >= 3500 else f"{height}p"
        found.setdefault(key, None)
    return found


def resolution_rank(item):
    if item.endswith("k"):
        return int(item[:-1]) * 1000
    if item.endswith("p"):
        return int(item[:-1])
    return int(item.split("x", 1)[0])


def values_compatible(field_id, first, second):
    a, b = normalized_compare(first, field_id), normalized_compare(second, field_id)
    if field_id == "video_recording":
        af, bf = recording_features(first), recording_features(second)
        shared = set(af) & set(bf)
        return bool(shared) and all(af[key] is None or bf[key] is None or af[key] == bf[key] for key in shared)
    if a == b:
        return True
    if field_id == "display_technology":
        # "IPS" describes the LCD viewing mode, while LTPS/a-Si describe its
        # backplane. Manufacturer and secondary pages can state both without
        # disagreeing about the underlying LCD display.
        first_lcd = "lcd" in a
        second_lcd = "lcd" in b
        if first_lcd and second_lcd:
            return True
    if field_id in {"rear_camera_system", "video_recording", "sensors"}:
        prefix = {"rear_camera_system": "camera-mp:", "video_recording": "video:", "sensors": "sensors:"}[field_id]
        if not (a.startswith(prefix) and b.startswith(prefix)):
            return False
        aset, bset = set(a[len(prefix):].split(",")), set(b[len(prefix):].split(","))
        if field_id == "sensors":
            # Only distinguish virtual and physical proximity when the source
            # explicitly calls one physical. A generic "proximity sensor" is
            # not evidence that it differs from a virtual proximity sensor.
            if ("virtualproximity" in aset and "physicalproximity" in bset) or ("physicalproximity" in aset and "virtualproximity" in bset):
                return False
            common = aset & bset
            return len(common) >= max(1, min(len(aset), len(bset)) // 2)
        return bool(aset and bset and (aset <= bset or bset <= aset))
    if field_id == "dimensions":
        if not (a.startswith("dimensions:") and b.startswith("dimensions:")):
            return False
        aset, bset = set(a.removeprefix("dimensions:").split(",")), set(b.removeprefix("dimensions:").split(","))
        return bool(aset and bset and (aset <= bset or bset <= aset))
    if field_id == "sim_esim":
        at, bt = set(a.split(",")), set(b.split(","))
        explicit_conflict = (("nano-sim" in at and "micro-sim" in bt) or ("micro-sim" in at and "nano-sim" in bt))
        return not explicit_conflict and bool(at & bt)
    if field_id == "cellular_bands":
        return bool(set(a.split(",")) & set(b.split(",")))
    return False


def information_score(value, field_id, source_kind=""):
    text = str(value or "")
    if field_id == "sensors":
        score = len(sensor_tokens(text)) * 20
    elif field_id == "rear_camera_system":
        score = len(re.findall(r"\b\d+(?:\.\d+)?\s*mp\b", text)) * 30
    elif field_id == "video_recording":
        score = len(recording_resolutions(text)) * 30
    else:
        score = len(re.findall(r"[\w.]+", text)) * 10
    return score + (5 if source_kind == "official" else 0) + len(text) / 1000


def catalog_value_preferred(old, candidate, field_id, source_kind=""):
    if old is None:
        return True
    if normalized_compare(old, field_id) == normalized_compare(candidate, field_id):
        return False
    if not values_compatible(field_id, old, candidate):
        return True
    return information_score(candidate, field_id, source_kind) > information_score(old, field_id)


def field_value(observation: dict, definition: dict):
    key = observation["key"]
    value = observation.get("value")
    unit = observation.get("unit") or definition.get("unit") or None
    if key in {"battery_mah", "battery_wh", "ram_gb", "internal_storage_gb", "display_inches", "front_camera", "weight"}:
        value = number(value)
        if value is None:
            return None, unit, None
        if key == "weight":
            if str(observation.get("unit", "g")).lower() == "kg":
                value *= 1000
            unit = "g"
    elif key == "charging":
        match = re.search(r"(\d+(?:\.\d+)?)\s*(?:w|watt)", str(value), re.I)
        if not match:
            return None, unit, None
        value = number(match.group(1))
        unit = "W"
    else:
        value = str(value).strip() if value is not None else None
    if key == "cellular" and value and re.search(r"\bsim\b|microsd|micro\s*sd", value, re.I) and not re.search(r"\b(?:2|3|4|5)\s*g\b|gsm|wcdma|lte|nr\b", value, re.I):
        return None, unit, None
    if key == "video_recording" and value and not recording_resolutions(value):
        return None, unit, None
    if key == "rear_camera" and value and not re.search(r"\b\d+(?:\.\d+)?\s*mp\b|\b(?:wide|ultrawide|telephoto|macro|periscope|depth)\b", value, re.I):
        # Product page table headers such as "Rear camera:" have no camera
        # specification and must not become a candidate value.
        return None, unit, None
    return value, unit, definition.get("catalogKey")


def field_id_for(key: str, category: str) -> str | None:
    if key == "cellular":
        return "cellular" if category == "laptops" else "cellular_bands"
    if key in {"usb", "ports"}:
        return "ports" if category == "laptops" else "usb"
    if key == "charging" and category == "laptops":
        return "charging"
    if key == "front_camera" and category == "laptops":
        return "webcam"
    return KEY_TO_FIELD.get(key)


def evidence_item(observation: dict, review_status: str, configuration_match: str):
    return {
        "value": observation.get("value"),
        "unit": observation.get("unit"),
        "sourceUrl": observation["source_url"],
        "sourceKind": observation["source_kind"],
        "observedAt": observation.get("observed_at"),
        "excerpt": observation.get("excerpt"),
        "configurationMatch": configuration_match,
        "reviewStatus": review_status,
        "localAvailabilityVerified": bool(observation.get("local_availability_verified")),
    }


def conflict_check(old, candidate, field_id=None) -> bool:
    if old is None:
        return False
    if values_compatible(field_id, old, candidate):
        return False
    if field_id == "gpu":
        old_text, new_text = normalized_compare(old, field_id), normalized_compare(candidate, field_id)
        if old_text in new_text or new_text in old_text:
            return False
    if isinstance(old, (int, float)) and isinstance(candidate, (int, float)):
        return abs(float(old) - float(candidate)) > 0.001
    previous = normalized_compare(old, field_id)
    current = normalized_compare(candidate, field_id)
    if field_id in {"cellular_bands", "cellular"}:
        old_set, new_set = set(previous.split(",")), set(current.split(","))
        return not (old_set & new_set)
    if field_id == "sim_esim":
        old_text, new_text = str(old).casefold(), str(candidate).casefold()
        if (re.search(r"\bdual\b", old_text) and re.search(r"\bsingle\b", new_text)) or (re.search(r"\bsingle\b", old_text) and re.search(r"\bdual\b", new_text)):
            return True
        if ("nano-sim" in previous and "micro-sim" in current) or ("micro-sim" in previous and "nano-sim" in current):
            return True
        return False
    if field_id == "operating_system":
        old_text, new_text = str(old).casefold(), str(candidate).casefold()
        families = ("hyperos", "harmonyos", "android", "coloros", "oxygenos", "funtouchos", "hios", "one ui", "ios", "ipados", "windows")
        old_versions = {family: re.search(rf"\b{re.escape(family)}\s*(\d+)(?:\.\d+)?", old_text).group(1)
                        for family in families if re.search(rf"\b{re.escape(family)}\s*(\d+)(?:\.\d+)?", old_text)}
        new_versions = {family: re.search(rf"\b{re.escape(family)}\s*(\d+)(?:\.\d+)?", new_text).group(1)
                        for family in families if re.search(rf"\b{re.escape(family)}\s*(\d+)(?:\.\d+)?", new_text)}
        shared = old_versions.keys() & new_versions.keys()
        if shared:
            return any(old_versions[family] != new_versions[family] for family in shared)
        if old_versions and new_versions:
            return True
    if field_id == "audio":
        old_text, new_text = str(old).casefold(), str(candidate).casefold()
        return ("stereo" in old_text and "mono" in new_text) or ("mono" in old_text and "stereo" in new_text)
    return previous != current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manual = read_json(MANUAL)
    latest = read_json(LATEST)
    catalog = read_json(CATALOG)
    audit = read_json(AUDIT)
    current_reviews = manual.get("records", [])
    manual_reviews_already_present = len(current_reviews)
    reviewed_field_keys = {
        (row.get("deviceId"), row.get("configurationId"), item.get("fieldId"))
        for row in current_reviews for item in row.get("fields", [])
        if item.get("status") in {"VERIFIED", "VERIFIED_SECONDARY", "NOT_APPLICABLE"}
    }
    reviewed_field_rows = {
        (row.get("deviceId"), row.get("configurationId"), item.get("fieldId")): item
        for row in current_reviews for item in row.get("fields", [])
        if item.get("status") in {"VERIFIED", "VERIFIED_SECONDARY", "NOT_APPLICABLE"}
    }
    catalog_by_id = {row["id"]: row for row in catalog}
    fields_by_category = {
        category: {field["id"]: field for field in rows}
        for category, rows in audit["fieldDefinitions"].items()
    }
    fetch_status = {
        (row.get("device_id"), row.get("source_url")): row.get("status")
        for row in latest.get("fetches", [])
    }
    observations = defaultdict(list)
    for observation in latest.get("observations", []):
        if fetch_status.get((observation.get("device_id"), observation.get("source_url"))) != "extracted":
            continue
        if observation.get("key") in KEY_TO_FIELD:
            observations[observation["device_id"]].append(observation)
    prices = defaultdict(list)
    for price in latest.get("prices", []):
        if fetch_status.get((price.get("device_id"), price.get("source_url"))) == "extracted":
            prices[price["device_id"]].append(price)

    generated = []
    new_variants_by_device = {}
    conflicts = 0
    conflict_samples = []
    reviewed_observation_fields = 0
    promoted_prices = 0
    for device_id, model_observations in observations.items():
        if device_id not in catalog_by_id:
            continue
        device = catalog_by_id[device_id]
        if device.get("recordType") != "device":
            continue
        category = device.get("category")
        definitions = fields_by_category.get(category, {})
        source_urls = sorted({item["source_url"] for item in model_observations})
        observation_by_source_key = {}
        for item in model_observations:
            observation_by_source_key[(item["source_url"], item["key"])] = item

        price_rows = prices.get(device_id, [])
        # Only a source's explicit RAM and storage pair can identify a configuration.
        pairs = {}
        for url in source_urls:
            ram = observation_by_source_key.get((url, "ram_gb"))
            storage = observation_by_source_key.get((url, "internal_storage_gb"))
            if ram and storage and number(ram.get("value")) is not None and number(storage.get("value")) is not None:
                pair = (int(number(ram["value"])), int(number(storage["value"])))
                pairs[pair] = {"url": url, "kind": ram["source_kind"], "ram": ram, "storage": storage}
        price_by_pair = defaultdict(list)
        for price in price_rows:
            ram, storage = price.get("variant_ram_gb"), price.get("variant_storage_gb")
            if ram is not None and storage is not None:
                price_by_pair[(int(ram), int(storage))].append(price)
        for pair, records in price_by_pair.items():
            if len({(row.get("amount_php"), row.get("source_published_at")) for row in records}) == 1:
                p = records[0]
                pairs.setdefault(pair, {"url": p["source_url"], "kind": p["source_kind"], "price": p})

        variants = list(device.get("variants") or [])
        existing_pairs = defaultdict(list)
        for variant in variants:
            pair = config_pair(variant)
            if pair:
                existing_pairs[pair].append(variant)
        new_variant_defs = []
        for pair in pairs:
            if pair not in existing_pairs and (pair in price_by_pair or pair in pairs):
                # Only add a source configuration with both RAM and storage explicitly present.
                proof = pairs[pair]
                has_pair_excerpt = bool(proof.get("ram") and proof.get("storage"))
                has_exact_price = bool(price_by_pair.get(pair))
                if not (has_pair_excerpt or has_exact_price):
                    continue
                variant_id = f"{device_id}-auto-{pair[0]}gb-{pair[1]}gb"
                new_variant_defs.append({"id": variant_id, "label": f"{pair[0]} GB RAM / {pair[1]} GB storage"})
                existing_pairs[pair].append({"id": variant_id, "label": new_variant_defs[-1]["label"], "specs": {}, "specSources": {}, "pricePhp": None})

        if new_variant_defs:
            current = device.get("variants") or []
            if len(current) == 1 and current[0]["id"].endswith("-unrecorded") and not current[0].get("specs"):
                variant_directive = {"replacementVariants": new_variant_defs}
            else:
                variant_directive = {"additionalVariants": new_variant_defs}
            new_variants_by_device[device_id] = variant_directive
        else:
            variant_directive = {}

        all_variants = list(variants)
        if variant_directive.get("replacementVariants"):
            # The catalog builder removes the placeholder, so it must not
            # receive a review row that points to a deleted configuration ID.
            all_variants = []
        for added in new_variant_defs:
            all_variants.append({**added, "specs": {}, "specSources": {}, "pricePhp": None})
        if not all_variants:
            continue

        source_records = {}
        for item in model_observations:
            url, kind = item["source_url"], item["source_kind"]
            sid = source_id(url)
            source_records[sid] = source_record(url, kind, None, item.get("observed_at", ""))
        for price in price_rows:
            url, kind = price["source_url"], price["source_kind"]
            sid = source_id(url)
            publication = price.get("source_published_at")
            source_records[sid] = source_record(url, kind, publication, price.get("observed_at", ""))

        for variant in all_variants:
            variant_id = variant["id"]
            pair = config_pair(variant)
            if pair is None:
                pair = next((candidate for candidate, matched in existing_pairs.items() if any(v.get("id") == variant_id for v in matched)), None)
            field_rows = []
            source_ids_used = set()

            def append_field(field_id, observation, *, status=None, normalized=None, unit=None, note=None, catalog_key=None, catalog_value=None, candidate_rows=None, config_match="model-level exact model source"):
                nonlocal conflicts, reviewed_observation_fields
                definition = definitions.get(field_id)
                if not definition:
                    return
                status = status or ("VERIFIED" if observation["source_kind"] == "official" else "VERIFIED_SECONDARY")
                sid = source_id(observation["source_url"])
                source_ids_used.add(sid)
                field = {
                    "fieldId": field_id,
                    "status": status,
                    "sourceId": sid,
                    "sourceValue": observation.get("excerpt") or str(observation.get("value") or ""),
                    "normalizedValue": normalized,
                    "note": note or ("Manually reviewed exact-model manufacturer observation." if status == "VERIFIED" else "Manually reviewed exact-model Philippine secondary-source observation; local-market status is not changed."),
                }
                if unit or definition.get("unit"):
                    field["unit"] = unit or definition.get("unit")
                if catalog_key and catalog_value is not None and status in {"VERIFIED", "VERIFIED_SECONDARY"}:
                    field["catalogKey"] = catalog_key
                    field["catalogValue"] = catalog_value
                    if variant.get("specs", {}).get(catalog_key) is not None:
                        field["replaceExisting"] = True
                if candidate_rows:
                    field["candidateEvidence"] = [evidence_item(row, "PENDING_VERIFICATION", config_match) for row in candidate_rows]
                field_rows.append(field)
                reviewed_observation_fields += status in {"VERIFIED", "VERIFIED_SECONDARY"}
                conflicts += status == "CONFLICTING_INFORMATION"
                if status == "CONFLICTING_INFORMATION" and len(conflict_samples) < 20:
                    conflict_samples.append({
                        "deviceId": device_id, "model": device.get("model"),
                        "configurationId": variant.get("id"), "fieldId": field_id,
                        "existing": (variant.get("specs") or {}).get((definition or {}).get("catalogKey")),
                        "source": observation.get("source_url"),
                        "candidate": normalized,
                    })

            # Exact configuration values require a RAM/storage pair from the same page or exact-price line.
            if pair and pair in pairs:
                proof = pairs[pair]
                proof_url = proof["url"]
                proof_kind = proof["kind"]
                if proof.get("ram") and proof.get("storage"):
                    for obs, field_id in ((proof["ram"], "ram_capacity"), (proof["storage"], "storage_capacity")):
                        definition = definitions.get(field_id)
                        if not definition:
                            continue
                        value, unit, key = field_value(obs, definition)
                        old = (variant.get("specs") or {}).get(key) if key else None
                        status = "CONFLICTING_INFORMATION" if conflict_check(old, value, field_id) else None
                        append_field(field_id, obs, status=status, normalized=value, unit=unit, note="Exact RAM/storage value appears in the same accepted source page as the matching configuration pair.", catalog_key=None if status else key, catalog_value=None if status else value, candidate_rows=[obs] if status else None, config_match="exact RAM/storage pair")
                elif proof.get("price"):
                    # PTG's exact-variant price line itself includes both memory values.
                    price_proof = proof["price"]
                    for field_id, value, key_name in (("ram_capacity", pair[0], "ramGb"), ("storage_capacity", pair[1], "storageGb")):
                        definition = definitions.get(field_id)
                        if not definition:
                            continue
                        synthetic = {"source_url":price_proof["source_url"],"source_kind":price_proof["source_kind"],"observed_at":price_proof.get("observed_at"),"value":value,"unit":"GB","excerpt":price_proof.get("excerpt")}
                        old = (variant.get("specs") or {}).get(key_name)
                        status = "CONFLICTING_INFORMATION" if conflict_check(old, value, field_id) else None
                        append_field(field_id, synthetic, status=status, normalized=value, unit="GB", note="RAM/storage pair is explicitly stated in the exact-variant Philippine price row.", catalog_key=None if status else key_name, catalog_value=None if status else value, candidate_rows=[synthetic] if status else None, config_match="exact RAM/storage pair")
                price_match = price_by_pair.get(pair, [])
                if price_match:
                    unique_prices = {(row.get("amount_php"), row.get("source_published_at")) for row in price_match}
                    price = price_match[0]
                    price_obs = {
                        "source_url": price["source_url"], "source_kind": price["source_kind"],
                        "observed_at": price.get("observed_at"), "value": price.get("amount_php"),
                        "unit": "PHP", "excerpt": price.get("excerpt"),
                    }
                    if len(unique_prices) == 1:
                        sid = source_id(price["source_url"])
                        source_ids_used.add(sid)
                        amount = int(price["amount_php"])
                        observed = price.get("source_published_at") or (price.get("observed_at") or "")[:10]
                        exact_price_kind = "VERIFIED" if price["source_kind"] == "official" else "VERIFIED_SECONDARY"
                        current_status = exact_price_kind
                        old_price = variant.get("pricePhp")
                        reviewed_price = reviewed_field_rows.get((device_id, variant_id, "current_price_php"))
                        reviewed_price_date = str((reviewed_price or {}).get("priceObservedAt") or "")[:10]
                        # A later dated source-price snapshot supersedes an older one;
                        # an older page scrape must not become a current-price conflict.
                        if reviewed_price_date and observed and observed <= reviewed_price_date:
                            current_status = "OLDER_SNAPSHOT"
                        elif old_price is not None and conflict_check(old_price, amount, "current_price_php"):
                            current_status = "CONFLICTING_INFORMATION"
                        if price.get("price_type") == "independent_reported_official_price":
                            launch = {"fieldId":"official_launch_price_php","status":exact_price_kind,"sourceId":sid,"sourceValue":price.get("excerpt") or f"{pair[0]}GB + {pair[1]}GB Philippine price: PHP {amount}","normalizedValue":amount,"unit":"PHP","note":"Exact RAM/storage price pair reported as the Philippine official price by the cited secondary source; historical figure, not a live offer."}
                            field_rows.append(launch)
                        source_ids_used.add(sid)
                        price_type = ("historical independent Philippine price report; source-date snapshot, not a live offer"
                                      if price.get("price_type") == "independent_reported_official_price"
                                      else "official Philippine product offer observed on the source date; not a future price guarantee")
                        current = {"fieldId":"current_price_php","status":current_status,"sourceId":sid,"sourceValue":price.get("excerpt") or f"PHP {amount} exact {pair[0]}GB/{pair[1]}GB source-date price","normalizedValue":amount,"unit":"PHP","note":"Dated price observation from the cited Philippine source; not represented as a live guarantee.","priceCondition":"new","priceType":price_type,"priceObservedAt":observed}
                        if current_status == "CONFLICTING_INFORMATION":
                            current["candidateEvidence"]=[evidence_item(price_obs,"PENDING_VERIFICATION","exact RAM/storage pair; price conflicts with existing catalog amount")]
                            current.pop("priceCondition",None);current.pop("priceType",None);current.pop("priceObservedAt",None)
                            conflicts+=1
                            if len(conflict_samples) < 20:
                                conflict_samples.append({"deviceId":device_id,"model":device.get("model"),"configurationId":variant.get("id"),"fieldId":"current_price_php","existing":old_price,"source":price.get("source_url"),"candidate":amount})
                        if current_status != "OLDER_SNAPSHOT":
                            field_rows.append(current)
                        if current_status in {"VERIFIED","VERIFIED_SECONDARY"}:
                            variant["pricePhp"] = amount
                            variant["priceCondition"] = "new"
                            variant["priceType"] = current["priceType"]
                            variant["priceObservedAt"] = observed
                            variant["priceSourceUrl"] = price["source_url"]
                            promoted_prices += 1
                    else:
                        first = price_match[0]
                        sid = source_id(first["source_url"])
                        source_ids_used.add(sid)
                        field_rows.append({"fieldId":"current_price_php","status":"CONFLICTING_INFORMATION","sourceId":sid,"sourceValue":"Multiple distinct source-date prices were observed for this exact RAM/storage pair.","normalizedValue":None,"unit":"PHP","note":"Price snapshots conflict; retain as candidate observations until source dates/offer terms are reconciled.","candidateEvidence":[evidence_item({"source_url":p["source_url"],"source_kind":p["source_kind"],"observed_at":p.get("observed_at"),"value":p.get("amount_php"),"unit":"PHP","excerpt":p.get("excerpt")},"PENDING_VERIFICATION","exact RAM/storage pair") for p in price_match]})
                        conflicts+=1
                        if len(conflict_samples) < 20:
                            conflict_samples.append({"deviceId":device_id,"model":device.get("model"),"configurationId":variant.get("id"),"fieldId":"current_price_php","existing":None,"source":first.get("source_url"),"candidate":[{"amount":p.get("amount_php"),"source":p.get("source_url"),"publishedAt":p.get("source_published_at")} for p in price_match]})
                config_obs = proof.get("ram") or proof.get("storage")
                config_status = "VERIFIED" if proof_kind == "official" else "VERIFIED_SECONDARY"
                config_value = f"{pair[0]} GB RAM / {pair[1]} GB storage"
                config_field = {"fieldId":"configuration","status":config_status,"sourceId":source_id(proof_url),"sourceValue":f"Exact configuration {config_value} is stated by the source.","normalizedValue":config_value,"note":"Configuration evidence matches RAM and storage as an exact pair."}
                field_rows.append(config_field); source_ids_used.add(source_id(proof_url))

            # Model-level observations are promoted only when they do not conflict with the imported value.
            for key in sorted({o["key"] for o in model_observations if o["key"] not in {"ram_gb","internal_storage_gb"}}):
                field_id = field_id_for(key, category)
                if not field_id:
                    continue
                if (device_id, variant_id, field_id) in reviewed_field_keys:
                    continue
                definition = definitions.get(field_id)
                if not definition:
                    continue
                candidates = [o for o in model_observations if o["key"] == key]
                converted = [(o, field_value(o, definition)) for o in candidates]
                converted = [(o, values) for o, values in converted if values[0] is not None]
                if not converted:
                    continue
                compatible_groups = []
                for entry in converted:
                    matching = [group for group in compatible_groups
                                if all(values_compatible(field_id, entry[1][0], member[1][0]) for member in group)]
                    if matching:
                        matching[0].append(entry)
                    else:
                        compatible_groups.append([entry])
                if len(compatible_groups) > 1:
                    first = converted[0][0]
                    field_rows.append({"fieldId":field_id,"status":"CONFLICTING_INFORMATION","sourceId":source_id(first["source_url"]),"sourceValue":"Accepted source pages report different values for this field.","normalizedValue":None,"note":"Multiple exact-model sources disagree; do not promote until reviewed.","candidateEvidence":[evidence_item(o,"PENDING_VERIFICATION","exact model; source values conflict") for o,_ in converted]})
                    source_ids_used.update(source_id(o["source_url"]) for o,_ in converted);conflicts+=1
                    if len(conflict_samples) < 20:
                        catalog_key = definitions.get(field_id, {}).get("catalogKey")
                        conflict_samples.append({"deviceId":device_id,"model":device.get("model"),"configurationId":variant.get("id"),"fieldId":field_id,"existing":(variant.get("specs") or {}).get(catalog_key) if catalog_key else None,"candidate":[{"value":v[0],"source":o.get("source_url")} for o,v in converted]})
                    continue
                compatible_values = compatible_groups[0]
                obs, values = max(compatible_values, key=lambda item: information_score(item[1][0], field_id, item[0].get("source_kind", "")))
                value, unit, key_name = values
                old = (variant.get("specs") or {}).get(key_name) if key_name else None
                status = "CONFLICTING_INFORMATION" if conflict_check(old, value, field_id) else ("VERIFIED" if obs["source_kind"] == "official" else "VERIFIED_SECONDARY")
                catalog_value = value
                should_update_catalog = bool(key_name) and status != "CONFLICTING_INFORMATION" and catalog_value_preferred(old, value, field_id, obs.get("source_kind", ""))
                if field_id == "sim_esim" and old and re.search(r"hybrid\s+micro\s*sd", str(old), re.I) and re.search(r"nano\s*-?\s*sim", str(value), re.I):
                    catalog_value = "Dual SIM (Nano-SIM); hybrid microSD slot"
                    should_update_catalog = True
                append_field(field_id, obs, status=status, normalized=value, unit=unit,
                             note="Exact-model technical value reviewed from an accepted source page. This model-level field is not a claim of Philippine sale availability.",
                             catalog_key=key_name if should_update_catalog else None,
                             catalog_value=catalog_value if should_update_catalog else None,
                             candidate_rows=[obs] if status == "CONFLICTING_INFORMATION" else None)

            if not field_rows:
                continue
            # De-duplicate field ids, retaining a conflict row if it exists.
            by_field = {}
            for row in field_rows:
                previous = by_field.get(row["fieldId"])
                if previous is None or row["status"] == "CONFLICTING_INFORMATION":
                    by_field[row["fieldId"]] = row
            by_field = {
                field_id: row for field_id, row in by_field.items()
                if (device_id, variant_id, field_id) not in reviewed_field_keys
            }
            if not by_field:
                continue
            record_sources = [source_records[sid] for sid in sorted(source_ids_used) if sid in source_records]
            review = {
                "deviceId": device_id,
                "configurationId": variant_id,
                "brand": device.get("brand"),
                "model": device.get("model"),
                "configurationLabel": variant.get("label") or "Configuration not recorded",
                "sources": record_sources,
                "fields": list(by_field.values()),
            }
            if variant_id == all_variants[0]["id"] and variant_directive:
                review.update(variant_directive)
            generated.append(review)

    if not args.dry_run:
        manual["reviewedAt"] = date.today().isoformat()
        manual.setdefault("records", []).extend(generated)
        MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "newManualReviews": len(generated),
        "newVariantDirectives": len(new_variants_by_device),
        "reviewedObservationFields": sum(
            row["status"] in {"VERIFIED", "VERIFIED_SECONDARY"}
            for review in generated for row in review.get("fields", [])
        ),
        "promotedDatedPrices": promoted_prices,
        "unresolvedConflicts": conflicts,
        "conflictSamples": conflict_samples,
        "manualReviewsAlreadyPresent": manual_reviews_already_present,
        "dryRun": args.dry_run,
    }, indent=2))


if __name__ == "__main__":
    main()
