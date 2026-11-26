"""Build a source-aware, field-level audit from DeviceIQ's public inventory.

The supplied workbook is only read. When available, an enriched copy is written
under outputs/ with appended audit sheets. Candidate observations remain pending
until a person verifies the exact model/configuration and source evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote_plus


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "lib/catalog/public-inventory.json"
LATEST = ROOT / "research/enrichment/latest.json"
SOURCES = ROOT / "research/enrichment/reference-sources.json"
AUDIT_DIR = ROOT / "research/enrichment"
PUBLIC_AUDIT = ROOT / "lib/catalog/specification-audit.json"
REPORT = ROOT / "DEVICEIQ_SPECIFICATION_COMPLETENESS_REPORT.md"
PROGRESS = ROOT / "DEVICEIQ_RESEARCH_PROGRESS.md"
DEFAULT_WORKBOOK = Path.home() / "Downloads/DeviceIQ_Philippine_Device_Inventory_2021-2026.xlsx"
WORKBOOK_COPY = ROOT / "outputs/deviceiq-inventory-2026-11-25/DeviceIQ_Philippine_Device_Inventory_2021-2026_ENRICHMENT_AUDIT.xlsx"


def field(field_id: str, label: str, group: str, unit: str = "", catalog_key: str = "") -> dict:
    return {"id": field_id, "label": label, "group": group, "unit": unit, "catalogKey": catalog_key or None}


PHONE_FIELDS = [
    field("model_number", "Exact model / regional number", "Identity"),
    field("configuration", "RAM and storage configuration", "Identity"),
    field("philippine_release_date", "Philippine launch or first authorized sale date", "Philippine market"),
    field("official_launch_price_php", "Official Philippine launch price", "Philippine market", "PHP"),
    field("current_price_php", "Dated Philippine price observation", "Philippine market", "PHP"),
    field("display_size", "Display size", "Display", "in", "displayInches"),
    field("display_technology", "Display technology", "Display", "", "displayType"),
    field("display_resolution", "Display resolution", "Display", "", "resolution"),
    field("display_refresh_rate", "Display refresh rate", "Display", "Hz", "refreshHz"),
    field("display_brightness", "Peak or typical brightness", "Display", "nits"),
    field("display_protection", "Display protection", "Display"),
    field("chipset", "System-on-chip / chipset", "Platform", "", "chipset"),
    field("process_node", "Chip manufacturing process", "Platform", "nm"),
    field("cpu", "CPU cores and configuration", "Platform", "", "cpu"),
    field("gpu", "GPU model", "Platform", "", "gpu"),
    field("operating_system", "Operating system at launch", "Platform", "", "os"),
    field("os_support", "Published OS / security update policy", "Platform"),
    field("ram_capacity", "RAM capacity by configuration", "Memory", "GB", "ramGb"),
    field("ram_type", "RAM type", "Memory", "", "ramType"),
    field("storage_capacity", "Internal storage by configuration", "Memory", "GB", "storageGb"),
    field("storage_type", "Internal storage type", "Memory", "", "storageType"),
    field("storage_expansion", "Expandable storage support", "Memory"),
    field("rear_camera_system", "Rear camera modules and roles", "Camera"),
    field("main_camera_sensor", "Main camera sensor / lens", "Camera"),
    field("ultrawide_camera", "Ultrawide camera", "Camera"),
    field("telephoto_camera", "Telephoto camera", "Camera"),
    field("front_camera", "Front camera", "Camera", "MP", "frontCameraMp"),
    field("video_recording", "Video recording modes", "Camera", "", "video"),
    field("battery_capacity", "Battery capacity", "Battery", "mAh", "batteryMah"),
    field("battery_technology", "Battery chemistry / design", "Battery"),
    field("wired_charging", "Wired charging", "Battery", "W", "chargingW"),
    field("wireless_charging", "Wireless / reverse charging", "Battery"),
    field("dimensions", "Dimensions", "Build", "mm", "dimensions"),
    field("weight", "Weight", "Build", "g", "weightG"),
    field("materials", "Frame and back materials", "Build"),
    field("ingress_protection", "Ingress protection rating", "Build"),
    field("sim_esim", "SIM and eSIM configuration", "Connectivity", "", "sim"),
    field("cellular_bands", "Cellular technology and bands", "Connectivity", "", "cellular"),
    field("wifi", "Wi-Fi standard", "Connectivity", "", "wifi"),
    field("bluetooth", "Bluetooth version", "Connectivity"),
    field("usb", "USB connector and data standard", "Connectivity", "", "ports"),
    field("nfc", "NFC support", "Connectivity"),
    field("gnss", "GNSS / satellite positioning", "Connectivity"),
    field("audio", "Audio jack and speaker configuration", "Audio", "", "sound"),
    field("sensors", "Sensors", "Other"),
]

TABLET_FIELDS = [
    *PHONE_FIELDS,
    field("tablet_stylus", "Stylus support and compatibility", "Accessories", "", "stylus"),
    field("tablet_keyboard", "Keyboard support and compatibility", "Accessories", "", "keyboard"),
    field("tablet_cellular_variant", "Wi-Fi-only / cellular variant", "Connectivity", "", "cellular"),
]

LAPTOP_FIELDS = [
    field("model_number", "Exact model / regional SKU", "Identity"),
    field("configuration", "Exact CPU, GPU, RAM, storage and panel configuration", "Identity"),
    field("philippine_release_date", "Philippine launch or first authorized sale date", "Philippine market"),
    field("official_launch_price_php", "Official Philippine launch price", "Philippine market", "PHP"),
    field("current_price_php", "Dated Philippine price observation", "Philippine market", "PHP"),
    field("display_size", "Display size", "Display", "in", "displayInches"),
    field("display_resolution", "Display resolution", "Display", "", "resolution"),
    field("display_technology", "Panel technology", "Display", "", "displayType"),
    field("display_refresh_rate", "Display refresh rate", "Display", "Hz", "refreshHz"),
    field("display_brightness", "Panel brightness", "Display", "nits"),
    field("display_color", "Color gamut / coverage", "Display"),
    field("touchscreen", "Touchscreen support", "Display", "", "touchscreen"),
    field("cpu", "Exact processor model", "Platform", "", "cpu"),
    field("cpu_cores_threads", "CPU cores and threads", "Platform"),
    field("gpu", "Integrated / discrete GPU model", "Platform", "", "gpu"),
    field("gpu_vram", "Dedicated GPU memory", "Platform", "GB"),
    field("gpu_tgp", "GPU total graphics power", "Platform", "W"),
    field("operating_system", "Operating system", "Platform", "", "os"),
    field("ram_capacity", "Installed RAM by configuration", "Memory", "GB", "ramGb"),
    field("ram_type", "RAM type and speed", "Memory", "", "ramType"),
    field("ram_upgradeability", "RAM slots, soldering and upgrade limit", "Memory", "", "ramMaxGb"),
    field("storage_capacity", "Installed storage by configuration", "Memory", "GB", "storageGb"),
    field("storage_type", "SSD interface and generation", "Memory", "", "storageType"),
    field("storage_slots", "Storage slots and expansion limit", "Memory"),
    field("battery_capacity", "Battery capacity", "Battery", "Wh", "batteryWh"),
    field("battery_life", "Published battery runtime and test basis", "Battery"),
    field("charging", "Power adapter / USB-C charging", "Battery", "W", "chargingW"),
    field("webcam", "Webcam resolution and features", "Camera"),
    field("audio", "Speakers and microphone", "Audio", "", "sound"),
    field("keyboard", "Keyboard layout and backlight", "Input", "", "keyboard"),
    field("touchpad", "Touchpad / pointing device", "Input"),
    field("ports", "Ports and supported standards", "Connectivity", "", "ports"),
    field("wifi", "Wi-Fi standard", "Connectivity", "", "wifi"),
    field("bluetooth", "Bluetooth version", "Connectivity"),
    field("ethernet", "Ethernet / LAN", "Connectivity"),
    field("cellular", "WWAN / cellular option", "Connectivity", "", "cellular"),
    field("dimensions", "Dimensions", "Build", "mm", "dimensions"),
    field("weight", "Weight by configuration", "Build", "g", "weightG"),
    field("materials", "Chassis materials", "Build"),
    field("security", "Biometrics and security hardware", "Other"),
    field("warranty", "Philippine warranty terms", "Philippine market"),
]

FIELD_SETS = {"smartphones": PHONE_FIELDS, "tablets": TABLET_FIELDS, "laptops": LAPTOP_FIELDS}
OBSERVATION_TO_FIELD = {
    "battery_mah": "battery_capacity", "battery_wh": "battery_capacity", "ram_gb": "ram_capacity",
    "internal_storage_gb": "storage_capacity", "display_inches": "display_size",
    "chipset": "chipset", "cpu": "cpu", "gpu": "gpu", "operating_system": "operating_system",
    "resolution": "display_resolution", "refresh_hz": "display_refresh_rate", "weight": "weight",
    "dimensions": "dimensions", "charging": "wired_charging", "wifi": "wifi", "bluetooth": "bluetooth",
    "nfc": "nfc", "sim": "sim_esim", "front_camera": "front_camera", "rear_camera": "rear_camera_system",
    "ip_rating": "ingress_protection", "ports": "ports",
    "cellular": "cellular_bands", "display_technology": "display_technology",
    "display_brightness": "display_brightness", "display_protection": "display_protection",
    "storage_expansion": "storage_expansion", "storage_type": "storage_type",
    "ram_type": "ram_type", "battery_technology": "battery_technology",
    "main_camera_sensor": "main_camera_sensor", "ultrawide_camera": "ultrawide_camera",
    "telephoto_camera": "telephoto_camera", "video_recording": "video_recording",
    "materials": "materials", "audio": "audio", "sensors": "sensors", "gnss": "gnss",
    "tablet_stylus": "tablet_stylus", "keyboard": "tablet_keyboard", "usb": "usb",
}
STATUS_PENDING = "PENDING_VERIFICATION"
ASSESSED_STATUSES = {"VERIFIED", "VERIFIED_SECONDARY", "NOT_DISCLOSED", "NOT_APPLICABLE", "UNAVAILABLE_AFTER_RESEARCH", "CONFLICTING_INFORMATION"}
VERIFIED_STATUSES = {"VERIFIED", "VERIFIED_SECONDARY"}


def stable_id(*parts: str) -> str:
    return hashlib.sha256("|".join(str(part or "") for part in parts).encode("utf-8")).hexdigest()[:20]


def clean(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "Yes" if value else "No"
    text = str(value).strip()
    return text if text else None


def year_for(device: dict) -> str:
    year = device.get("claimedReleaseYear") or device.get("philippineReleaseYear")
    if not year and device.get("releaseDate"):
        year = str(device["releaseDate"])[:4]
    return str(year) if year else "Unassigned"


def publisher(url: str | None) -> str | None:
    if not url:
        return None
    from urllib.parse import urlparse
    return urlparse(url).hostname


def candidate_links(device: dict) -> list[dict]:
    query = quote_plus(f'"{device.get("brand", "")}" "{device.get("model", "")}"')
    return [
        {"sourceId": "official_manufacturer", "label": "Search official manufacturer pages", "url": f"https://www.google.com/search?q={query}+official+specifications"},
        {"sourceId": "pinoy_techno_guide", "label": "Search Pinoy Techno Guide", "url": f"https://www.google.com/search?q=site%3Apinoytechnoguide.com+{query}+specifications"},
        {"sourceId": "nanoreview", "label": "NanoReview manual lookup (link only)", "url": f"https://www.google.com/search?q=site%3Ananoreview.net+{query}"},
        {"sourceId": "kimovil", "label": "Kimovil manual lookup (link only)", "url": f"https://www.google.com/search?q=site%3Akimovil.com+{query}"},
        {"sourceId": "notebookcheck", "label": "Search Notebookcheck", "url": f"https://www.google.com/search?q=site%3Anotebookcheck.net+{query}"},
    ]


def style_sheet(ws, header_row=1):
    from openpyxl.styles import Font, PatternFill, Alignment
    ws.freeze_panes = f"A{header_row + 1}"
    ws.auto_filter.ref = ws.dimensions
    for cell in ws[header_row]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="2457A6")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[header_row].height = 30
    for col in ws.columns:
        letter = col[0].column_letter
        max_len = min(48, max((len(str(c.value or "")) for c in col[: min(len(col), 250)]), default=12))
        ws.column_dimensions[letter].width = max(12, max_len + 2)


def write_large_text(path: Path, text: str) -> None:
    """Write large JSON artifacts in bounded chunks and replace atomically."""
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as output:
        for start in range(0, len(text), 1024 * 1024):
            output.write(text[start:start + 1024 * 1024])
    os.replace(temporary, path)


def make_workbook_copy(source: Path, target: Path, audit_rows: list[dict], summaries: list[dict], lookups: list[dict], prices: list[dict], devices_by_id: dict[str, dict], image_manifest: dict[str, dict], unavailable_images: dict[str, dict]):
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
    target.parent.mkdir(parents=True, exist_ok=True)
    # Open the supplied inventory for reading and save only to the separate
    # audit output. shutil.copy2 can fail on Windows when Excel has the source
    # workbook memory-mapped; openpyxl can read it without changing the source.
    wb = load_workbook(source)
    for name in ("SPEC FIELD AUDIT", "AUDIT SUMMARY", "REFERENCE LOOKUPS", "PRICE CANDIDATES", "IMAGE AUDIT"):
        if name in wb.sheetnames:
            del wb[name]
    ws = wb.create_sheet("SPEC FIELD AUDIT")
    columns = [
        "Evidence ID", "Device ID", "Configuration ID", "Category", "Brand", "Model", "Claimed research year",
        "Specification group", "Specification field", "Original source value", "Normalized value", "Unit", "Source ID",
        "Source URL", "Source publisher", "Publication date", "Access date", "Verification status", "Confidence level", "Notes",
        "Candidate evidence URLs", "Candidate values / excerpts",
    ]
    ws.append(columns)
    for item in audit_rows:
        candidates = item.get("candidateEvidence", [])
        ws.append([
            item["evidence_id"], item["device_id"], item["configuration_id"], item["category"], item["brand"], item["model"],
            item["claimed_research_year"], item["specification_group"], item["specification_field"],
            item["original_source_value"], item["normalized_value"], item["unit"], item["source_id"], item["source_url"],
            item["source_publisher"], item["publication_date"], item["access_date"], item["verification_status"],
            item["confidence_level"], item["notes"], "\n".join(x.get("source_url", "") for x in candidates),
            "\n".join(f"{x.get('value', '')} — {x.get('excerpt', '')}" for x in candidates),
        ])
    style_sheet(ws)
    ws.column_dimensions[get_column_letter(20)].width = 60
    ws.column_dimensions[get_column_letter(22)].width = 72

    summary_ws = wb.create_sheet("AUDIT SUMMARY")
    summary_ws.append(["Metric", "Value", "Notes"])
    for row in summaries:
        summary_ws.append([row.get("metric"), row.get("value"), row.get("notes")])
    style_sheet(summary_ws)

    refs = wb.create_sheet("REFERENCE LOOKUPS")
    refs.append(["Device ID", "Category", "Brand", "Exact model", "Claimed research year", "Source", "Manual lookup URL", "Access policy"])
    for row in lookups:
        for link in row["links"]:
            refs.append([row["device_id"], row["category"], row["brand"], row["model"], row["year"], link["sourceId"], link["url"], link["policy"]])
    style_sheet(refs)
    refs.column_dimensions["G"].width = 80
    refs.column_dimensions["H"].width = 75

    price_ws = wb.create_sheet("PRICE CANDIDATES")
    price_ws.append(["Device ID", "Category", "Brand", "Exact model", "Candidate amount PHP", "Source RAM GB", "Source storage GB", "Configuration match", "Price type", "Source publication date", "Observed date", "Local availability verified", "Source URL", "Source excerpt"])
    for price in prices:
        device = devices_by_id.get(price.get("device_id"), {})
        price_ws.append([
            price.get("device_id"), device.get("category"), device.get("brand"), device.get("model"),
            price.get("amount_php"), price.get("variant_ram_gb"), price.get("variant_storage_gb"),
            price.get("configuration_match"), price.get("price_type"), price.get("source_published_at"),
            price.get("observed_at"), price.get("local_availability_verified"), price.get("source_url"), price.get("excerpt"),
        ])
    style_sheet(price_ws)
    price_ws.column_dimensions["M"].width = 72
    price_ws.column_dimensions["N"].width = 60

    image_ws = wb.create_sheet("IMAGE AUDIT")
    image_ws.append(["Device ID", "Category", "Brand", "Exact model", "Claimed research year", "Image status", "Match scope", "Asset path", "Source page", "Image asset URL", "Credit", "Usage terms", "License URL", "Rights checked date", "Rights status / reason", "Rights terms URL", "Changes / attribution note", "Alt text", "Manual image lookup"])
    for device in devices_by_id.values():
        image_key = device.get("imageId") or device.get("id")
        image = image_manifest.get(image_key)
        unavailable = unavailable_images.get(device.get("id"), {})
        display_status = {
            "REUSE_PERMISSION_REQUIRED": "Image unavailable - reuse permission required",
            "REUSE_RIGHTS_NOT_ESTABLISHED": "Image unavailable - reuse rights not established",
            "NO_RELIABLE_MATCH": "Image unavailable - no reliable exact match",
        }
        image_status = "Reviewed image with reusable license" if image else display_status.get(
            unavailable.get("status"), unavailable.get("status", "Image status not recorded"))
        query = quote_plus(f'"{device.get("brand", "")}" "{device.get("model", "")}" official product image')
        image_ws.append([
            device.get("id"), device.get("category"), device.get("brand"), device.get("model"), year_for(device),
            image_status,
            (image or {}).get("scope"), (image or {}).get("path"), (image or {}).get("sourcePage"),
            (image or {}).get("assetUrl"), (image or {}).get("credit"), (image or {}).get("usageTerms"),
            (image or {}).get("licenseUrl"), (image or {}).get("rightsCheckedAt"),
            unavailable.get("reason") if not image else None, unavailable.get("rightsTermsUrl") if not image else None,
            (image or {}).get("changes"),
            f"{device.get('brand', '')} {device.get('model', '')} product image" if image else f"Image unavailable for {device.get('brand', '')} {device.get('model', '')}",
            f"https://www.google.com/search?q={query}",
        ])
    style_sheet(image_ws)
    for column, width in {"I": 70, "J": 70, "O": 65, "P": 65, "Q": 55, "S": 82}.items():
        image_ws.column_dimensions[column].width = width
    wb.save(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--latest", type=Path, default=LATEST)
    parser.add_argument("--source-policy", type=Path, default=SOURCES)
    parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK)
    parser.add_argument("--skip-workbook", action="store_true")
    args = parser.parse_args()

    devices = json.loads(args.inventory.read_text(encoding="utf-8"))
    latest = json.loads(args.latest.read_text(encoding="utf-8")) if args.latest.exists() else {"observations": [], "prices": [], "fetches": [], "discovery": []}
    source_policy = json.loads(args.source_policy.read_text(encoding="utf-8"))
    image_manifest = json.loads((ROOT / "lib/catalog/image-manifest.json").read_text(encoding="utf-8"))
    unavailable_images = json.loads((ROOT / "research/catalog-image-unavailable.json").read_text(encoding="utf-8")) if (ROOT / "research/catalog-image-unavailable.json").exists() else {}
    manual_reviews = json.loads((AUDIT_DIR / "manual-field-reviews.json").read_text(encoding="utf-8")) if (AUDIT_DIR / "manual-field-reviews.json").exists() else {"records": []}
    manual_by_key = {}
    manual_source_by_id = {}
    manual_reviewed_device_ids = set()
    for manual_record in manual_reviews.get("records", []):
        manual_reviewed_device_ids.add(manual_record["deviceId"])
        sources = {s["id"]: s for s in manual_record.get("sources", [])}
        for source in sources.values():
            manual_source_by_id[source["id"]] = source
        for reviewed_field in manual_record.get("fields", []):
            manual_by_key[(manual_record["deviceId"], manual_record["configurationId"], reviewed_field["fieldId"])] = {
                **reviewed_field, "_sources": sources,
            }
    source_policy_by_id = {x["id"]: x for x in source_policy.get("sources", [])}
    candidates_by_device_field: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for observation in latest.get("observations", []):
        field_id = OBSERVATION_TO_FIELD.get(observation.get("key"))
        if not field_id:
            continue
        candidates_by_device_field[(observation.get("device_id", ""), field_id)].append({
            "value": clean(observation.get("value")), "source_url": observation.get("source_url"),
            "source_kind": observation.get("source_kind"), "observed_at": observation.get("observed_at"),
            "excerpt": clean(observation.get("excerpt")), "unit": observation.get("unit"), "review_status": "PENDING_VERIFICATION",
            "configuration_match": "model_level_unmatched",
            "local_availability_verified": bool(observation.get("local_availability_verified", False)),
        })
    for price in latest.get("prices", []):
        candidates_by_device_field[(price.get("device_id", ""), "current_price_php")].append({
            "value": clean(price.get("amount_php")), "unit": "PHP", "source_url": price.get("source_url"),
            "source_kind": price.get("source_kind"), "observed_at": price.get("observed_at"),
            "excerpt": clean(price.get("excerpt")), "configuration_match": price.get("configuration_match"),
            "review_status": "PENDING_VERIFICATION", "local_availability_verified": bool(price.get("local_availability_verified", False)),
            "variant_ram_gb": price.get("variant_ram_gb"), "variant_storage_gb": price.get("variant_storage_gb"),
        })

    audit_rows: list[dict] = []
    public_variants: dict[str, dict] = {}
    device_rows = [d for d in devices if d.get("recordType", "device") == "device"]
    device_by_id = {d["id"]: d for d in device_rows}
    manually_verified_configurations = {
        (record["deviceId"], record["configurationId"])
        for record in manual_reviews.get("records", [])
        if any(field.get("status") in VERIFIED_STATUSES for field in record.get("fields", []))
    }
    manually_verified_models = {device_id for device_id, _ in manually_verified_configurations}
    laptop_device_ids = {d["id"] for d in device_rows if d.get("category") == "laptops"}
    laptop_reviewed_configurations = {
        key for key in manually_verified_configurations if key[0] in laptop_device_ids
    }
    assignment_totals = Counter()
    brand_year_groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for device in device_rows:
        category = device.get("category")
        definitions = FIELD_SETS.get(category, [])
        assignment_totals[category] += len(definitions) * max(1, len(device.get("variants", [])))
        year = year_for(device)
        brand_year_groups[(year, category, device.get("brand") or "Unassigned")].append(device)
        variants = device.get("variants") or [{"id": f"{device['id']}:base", "label": "Base model", "specs": {}}]
        for variant in variants:
            variant_id = variant.get("id") or f"{device['id']}:base"
            specs = variant.get("specs") or {}
            compact_fields = []
            group_source_statuses = Counter()
            for definition in definitions:
                field_id = definition["id"]
                catalog_key = definition.get("catalogKey")
                model_value = None
                if field_id == "model_number":
                    model_value = variant.get("modelCode") or variant.get("sku") or device.get("modelNumber")
                elif field_id == "configuration":
                    model_value = variant.get("label")
                elif field_id == "philippine_release_date":
                    model_value = device.get("philippineAvailabilityDate")
                elif field_id == "official_launch_price_php":
                    model_value = None
                elif field_id == "current_price_php":
                    model_value = variant.get("pricePhp")
                elif catalog_key:
                    model_value = specs.get(catalog_key)
                if field_id == "tablet_cellular_variant" and category == "tablets":
                    model_value = specs.get("cellular")

                value_text = clean(model_value)
                source_url = (variant.get("specSources") or {}).get(catalog_key) if catalog_key else None
                if field_id == "current_price_php":
                    source_url = variant.get("priceSourceUrl") or source_url
                if field_id == "philippine_release_date":
                    source_url = next((s.get("url") for s in device.get("sources", []) if s.get("url") and "philippine" in (s.get("purpose") or "").lower()), None)
                candidate_evidence = candidates_by_device_field.get((device["id"], field_id), [])
                # Keep device-level observations visible but clearly unresolved against configurations.
                if field_id == "current_price_php":
                    current_ram = specs.get("ramGb")
                    current_storage = specs.get("storageGb")
                    candidate_evidence = [
                        x for x in candidate_evidence
                        if x.get("variant_ram_gb") is not None and x.get("variant_storage_gb") is not None
                        and current_ram is not None and current_storage is not None
                            and x.get("variant_ram_gb") is not None and x.get("variant_storage_gb") is not None
                            and float(current_ram) == float(x["variant_ram_gb"])
                            and float(current_storage) == float(x["variant_storage_gb"])
                    ]
                    candidate_evidence = [{**x, "configuration_match": "ram_storage_match_needs_review"} for x in candidate_evidence]
                source_id = f"source_{stable_id(source_url)}" if source_url else None
                source_record = next((s for s in device.get("sources", []) if s.get("url") == source_url), None) if source_url else None
                notes = "Existing workbook/catalog value or research observation has not been independently field-reviewed."
                if not value_text and not candidate_evidence:
                    notes = "Not recorded; research this field for the exact model and configuration."
                if candidate_evidence:
                    notes = "Candidate evidence is unreviewed; confirm exact model, region, and configuration before use."
                verification_status = STATUS_PENDING
                confidence_level = "UNREVIEWED"
                publication_date = (source_record or {}).get("publishedAt") or next((x.get("source_published_at") for x in candidate_evidence if x.get("source_published_at")), None)
                access_date = (source_record or {}).get("observedAt") or next((x.get("observed_at", "")[:10] for x in candidate_evidence if x.get("observed_at")), None)
                original_source_value = value_text
                normalized_value = value_text
                audit_unit = definition.get("unit") or None
                manual_field = manual_by_key.get((device["id"], variant_id, field_id))
                if manual_field:
                    manual_source = manual_field["_sources"].get(manual_field.get("sourceId"))
                    if not manual_source:
                        raise ValueError(f"Manual verification has no source: {device['id']} {field_id}")
                    for manual_candidate in manual_field.get("candidateEvidence", []):
                        candidate_evidence.append({
                            "value": clean(manual_candidate.get("value")), "unit": manual_candidate.get("unit"),
                            "source_url": manual_candidate.get("sourceUrl"), "source_kind": manual_candidate.get("sourceKind", "manual_secondary"),
                            "observed_at": manual_candidate.get("observedAt"), "excerpt": clean(manual_candidate.get("excerpt")),
                            "configuration_match": manual_candidate.get("configurationMatch", "exact"),
                            "review_status": manual_candidate.get("reviewStatus", STATUS_PENDING),
                            "local_availability_verified": bool(manual_candidate.get("localAvailabilityVerified", False)),
                        })
                    if manual_field.get("status") in VERIFIED_STATUSES:
                        verification_status = manual_field["status"]
                        confidence_level = "HIGH_MANUFACTURER_PRIMARY" if manual_field["status"] == "VERIFIED" else "MEDIUM_SECONDARY_SOURCE"
                        original_source_value = clean(manual_field.get("sourceValue"))
                        normalized_value = clean(manual_field.get("normalizedValue"))
                        value_text = normalized_value
                        audit_unit = manual_field.get("unit") or audit_unit
                        source_id = manual_source["id"]
                        source_url = manual_source["url"]
                        source_record = manual_source
                        publication_date = manual_source.get("publicationDate")
                        access_date = manual_source.get("accessDate")
                        notes = manual_field.get("note") or "Manually checked against the official manufacturer specification page."
                    elif manual_field.get("status") in ASSESSED_STATUSES:
                        verification_status = manual_field["status"]
                        confidence_level = "SOURCE_CONFLICT" if verification_status == "CONFLICTING_INFORMATION" else "RESEARCHED_STATUS"
                        original_source_value = clean(manual_field.get("sourceValue"))
                        normalized_value = clean(manual_field.get("normalizedValue"))
                        value_text = normalized_value
                        audit_unit = manual_field.get("unit") or audit_unit
                        source_id = manual_source["id"]
                        source_url = manual_source["url"]
                        source_record = manual_source
                        publication_date = manual_source.get("publicationDate")
                        access_date = manual_source.get("accessDate")
                        notes = manual_field.get("note") or "Field status was explicitly assessed from the cited source evidence."
                    elif manual_field.get("normalizedValue") is not None:
                        candidate_evidence = [*candidate_evidence, {
                            "value": clean(manual_field.get("normalizedValue")),
                            "unit": manual_field.get("unit"), "source_url": manual_source["url"],
                            "source_kind": "official", "observed_at": manual_source.get("accessDate"),
                            "excerpt": clean(manual_field.get("sourceValue")),
                            "configuration_match": manual_field.get("configurationMatch", "model-level candidate needs configuration review"),
                            "review_status": STATUS_PENDING,
                        }]
                        notes = manual_field.get("note") or "Manual source candidate; exact field/configuration relationship remains under review."
                    elif manual_field.get("status") == STATUS_PENDING:
                        verification_status = STATUS_PENDING
                        confidence_level = "UNREVIEWED"
                        original_source_value = clean(manual_field.get("sourceValue"))
                        normalized_value = None
                        value_text = None
                        source_id = manual_source["id"]
                        source_url = manual_source["url"]
                        source_record = manual_source
                        publication_date = manual_source.get("publicationDate")
                        access_date = manual_source.get("accessDate")
                        notes = manual_field.get("note") or "A source was checked, but this field remains unresolved."
                row = {
                    "evidence_id": f"evidence_{stable_id(device['id'], variant_id, field_id)}",
                    "device_id": device["id"], "configuration_id": variant_id, "category": category,
                    "brand": device.get("brand"), "model": device.get("model"), "claimed_research_year": year,
                    "specification_group": definition["group"], "specification_field": field_id,
                    "original_source_value": original_source_value, "normalized_value": normalized_value, "unit": audit_unit,
                    "source_id": source_id, "source_url": source_url, "source_publisher": publisher(source_url),
                    "publication_date": publication_date, "access_date": access_date,
                    "verification_status": verification_status,
                    "confidence_level": confidence_level, "notes": notes, "candidateEvidence": candidate_evidence,
                }
                audit_rows.append(row)
                compact_fields.append({
                    "id": field_id, "status": verification_status, "value": value_text,
                    "unit": audit_unit, "sourceUrl": source_url,
                    "candidateEvidence": candidate_evidence,
                })
            applicable = len(compact_fields)
            assessed = sum(item["status"] in ASSESSED_STATUSES for item in compact_fields)
            verified = sum(item["status"] in VERIFIED_STATUSES for item in compact_fields)
            pending = applicable - assessed
            public_variants[variant_id] = {
                "deviceId": device["id"], "category": category, "completenessStatus": "SPECIFICATION_INCOMPLETE",
                "assessmentCoveragePct": round(assessed / applicable * 100, 2) if applicable else 0,
                "verifiedCoveragePct": round(verified / applicable * 100, 2) if applicable else 0,
                "applicableFields": applicable, "assessedFields": assessed, "verifiedFields": verified,
                "pendingFields": pending, "fields": compact_fields,
                "researchLinks": candidate_links(device),
            }

    def model_completeness(device: dict) -> str:
        variants = device.get("variants") or [{"id": f"{device['id']}:base"}]
        rows = [public_variants.get(v.get("id") or f"{device['id']}:base", {}) for v in variants]
        statuses = [field["status"] for variant_record in rows for field in variant_record.get("fields", [])]
        if not statuses or any(status == STATUS_PENDING for status in statuses) or "CONFLICTING_INFORMATION" in statuses:
            return "SPECIFICATION_INCOMPLETE"
        if any(status in {"NOT_DISCLOSED", "NOT_APPLICABLE", "UNAVAILABLE_AFTER_RESEARCH"} for status in statuses):
            return "SPECIFICATION_COMPLETE_WITH_DISCLOSED_GAPS"
        return "SPECIFICATION_COMPLETE"

    model_statuses = {d["id"]: model_completeness(d) for d in device_rows}
    for variant in public_variants.values():
        variant["completenessStatus"] = model_statuses.get(variant["deviceId"], "SPECIFICATION_INCOMPLETE")

    fields_json = {category: defs for category, defs in FIELD_SETS.items()}
    (AUDIT_DIR / "specification-fields.json").write_text(json.dumps(fields_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    full_audit = {
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "sourceInventory": str(args.inventory.relative_to(ROOT)) if args.inventory.is_relative_to(ROOT) else args.inventory.name,
        "latestEnrichmentRun": latest.get("run_at"),
        "policyReviewedAt": source_policy.get("policyReviewedAt"),
        "fieldDefinitions": fields_json,
        "recordCount": len(device_rows), "configurationCount": len(public_variants), "fieldRowCount": len(audit_rows),
        "records": audit_rows,
    }
    write_large_text(AUDIT_DIR / "specification-field-audit.json", json.dumps(full_audit, ensure_ascii=False, separators=(",", ":")) + "\n")
    public = {
        "generatedAt": full_audit["generatedAt"], "fieldDefinitions": fields_json,
        "sourcePolicies": [
            {"id": x["id"], "name": x["name"], "homepage": x.get("homepage"), "robotsTxt": x.get("robotsTxt"),
             "termsUrl": x.get("termsUrl"), "automatedUse": x.get("automatedUse"), "promotionRule": x.get("promotionRule")}
            for x in source_policy.get("sources", [])
        ],
        "variants": public_variants,
    }
    write_large_text(PUBLIC_AUDIT, json.dumps(public, ensure_ascii=False, separators=(",", ":")) + "\n")

    status_counts = Counter(row["verification_status"] for row in audit_rows)
    category_summary = {}
    for category in FIELD_SETS:
        models = [d for d in device_rows if d.get("category") == category]
        configs = sum(len(d.get("variants", [])) or 1 for d in models)
        rows = [r for r in audit_rows if r["category"] == category]
        assessed = sum(r["verification_status"] in ASSESSED_STATUSES for r in rows)
        verified = sum(r["verification_status"] in VERIFIED_STATUSES for r in rows)
        category_summary[category] = {
            "models": len(models), "configurations": configs, "fields": len(rows),
            "assessed": assessed, "verified": verified, "pending": len(rows) - assessed,
        }

    candidate_source_counts = Counter(c.get("source_kind") for rows in candidates_by_device_field.values() for c in rows)
    candidate_model_counts = Counter()
    for device_id, field_id in candidates_by_device_field:
        matching = next((x for x in latest.get("observations", []) if x.get("device_id") == device_id and OBSERVATION_TO_FIELD.get(x.get("key")) == field_id), None)
        if matching:
            candidate_model_counts[matching.get("source_kind", "unknown")] += 1
    extracted_fetches = [x for x in latest.get("fetches", []) if x.get("status") == "extracted"]
    fetch_sources = Counter(x.get("source_kind", "unknown") for x in extracted_fetches)
    fetch_models_by_source = defaultdict(set)
    for item in extracted_fetches:
        fetch_models_by_source[item.get("source_kind", "unknown")].add(item.get("device_id"))
    model_category = {m.get("device_id"): m.get("category") for m in latest.get("models", [])}
    fetch_attempts_by_category = Counter(model_category.get(f.get("device_id"), "unknown") for f in latest.get("fetches", []))
    fetch_errors_by_category = Counter(
        model_category.get(f.get("device_id"), "unknown") for f in latest.get("fetches", [])
        if f.get("status") != "extracted"
    )
    fetched_ids_by_source = defaultdict(set)
    attempted_by_id = Counter()
    unextracted_by_id = Counter()
    for item in extracted_fetches:
        fetched_ids_by_source[item.get("source_kind", "unknown")].add(item.get("device_id"))
    for item in latest.get("fetches", []):
        attempted_by_id[item.get("device_id")] += 1
        if item.get("status") != "extracted":
            unextracted_by_id[item.get("device_id")] += 1
    image_count = sum(bool(image_manifest.get(d.get("imageId") or d.get("id"))) for d in device_rows)
    image_unavailable_counts = Counter(
        unavailable_images.get(d["id"], {}).get("status", "NO_RELIABLE_MATCH")
        for d in device_rows if not image_manifest.get(d.get("imageId") or d.get("id"))
    )
    held_out_count = sum(d.get("recordType") == "held_out_claim" for d in devices)
    excluded_count = sum(d.get("scopeStatus") == "Excluded" for d in device_rows)
    held_record_count = sum(d.get("scopeStatus") == "Held out" for d in device_rows) + held_out_count
    all_assessed_models = sum(
        all(public_variants.get(v.get("id") or f"{device['id']}:base", {}).get("pendingFields", 0) == 0
            for v in (device.get("variants") or [{"id": f"{device['id']}:base"}]))
        for device in device_rows
    )
    complete_models = sum(status == "SPECIFICATION_COMPLETE" for status in model_statuses.values())
    disclosed_gap_models = sum(status == "SPECIFICATION_COMPLETE_WITH_DISCLOSED_GAPS" for status in model_statuses.values())
    incomplete_models = len(device_rows) - complete_models - disclosed_gap_models
    assessed_field_count = sum(status_counts[status] for status in ASSESSED_STATUSES)
    verified_field_count = sum(status_counts[status] for status in VERIFIED_STATUSES)
    assessment_coverage = assessed_field_count / len(audit_rows) if audit_rows else 0
    verified_coverage = verified_field_count / len(audit_rows) if audit_rows else 0
    manual_pending_price_count = sum(
        1 for record in manual_reviews.get("records", []) for reviewed_field in record.get("fields", [])
        if reviewed_field.get("fieldId") == "current_price_php" and reviewed_field.get("status") == STATUS_PENDING
    )
    metrics = [
        ("Models", len(device_rows), "Device records; seven held-out claims are summarized separately."),
        ("Configurations", len(public_variants), "Separate catalog configuration records audited."),
        ("Models with manually verified source fields", len(manually_verified_models), "At least one exact-model or exact-configuration field has an accepted source review."),
        ("Configurations with manually verified source fields", len(manually_verified_configurations), "Distinct model/configuration pairs with at least one manually reviewed verified field."),
        ("Laptop models with official-source reviews", f"{len({key[0] for key in laptop_reviewed_configurations})}/{len(laptop_device_ids)}", "All 18 laptop model records have official manufacturer evidence; all remain incomplete because many fields are still pending."),
        ("Laptop configurations with reviewed source fields", len(laptop_reviewed_configurations), "Exact SKU/configuration rows reviewed across the laptop records."),
        ("Models with all fields assessed", all_assessed_models, "Every applicable field across every configuration has an assessed status."),
        ("Specification-complete models", complete_models, "Every applicable field is verified with no disclosed gaps or conflicts."),
        ("Complete with disclosed gaps", disclosed_gap_models, "All applicable fields are assessed; one or more are explicitly disclosed or not applicable."),
        ("Incomplete models", incomplete_models, "At least one applicable configuration field remains pending or conflicting."),
        ("Conflicting specification records", sum(1 for r in audit_rows if r["verification_status"] == "CONFLICTING_INFORMATION"), "No conflicts are promoted; candidate conflicts remain a review task."),
        ("Assessed specification fields", assessed_field_count, "Fields with a reviewed status, including verified values and justified disclosed gaps."),
        ("Verified specification fields", verified_field_count, "Candidate observations are not counted as verified."),
        ("Unavailable fields", status_counts["UNAVAILABLE_AFTER_RESEARCH"] + status_counts["NOT_DISCLOSED"], "These fields were reviewed in sources that omit them; values remain blank rather than being zero-filled."),
        ("Not applicable fields", status_counts["NOT_APPLICABLE"], "Category templates list applicable fields only; configuration-dependent N/A decisions await review."),
        ("Pending verification fields", status_counts[STATUS_PENDING], "Each current value and missing field is explicit in the audit."),
        ("Manually reviewed price candidates", manual_pending_price_count, "Source evidence is retained, but configuration ambiguity keeps the amount out of the public price."),
        ("Assessment coverage", f"{assessment_coverage:.2%}", f"{assessed_field_count} assessed fields / all applicable field rows."),
        ("Verified coverage", f"{verified_coverage:.2%}", f"{verified_field_count} verified fields / all applicable field rows."),
        ("Candidate field observations", len(latest.get("observations", [])), "Existing collection snapshot; unreviewed and not promoted."),
        ("Candidate prices", len(latest.get("prices", [])) + manual_pending_price_count, "Dated candidate observations; exact configuration review still required."),
        ("Candidate source links", len(latest.get("discovery", [])), "Discovery links only; not proof that a page was opened or confirmed."),
        ("Image-matched models", image_count, "Pre-existing reviewed image assignments in the catalog."),
        ("Models with image unavailable", len(device_rows) - image_count, "Neutral placeholder remains visible where no reviewed image is assigned."),
        ("Excluded models", excluded_count, "Visible only with Excluded status under current catalog rules."),
        ("Held-out claims / records", held_record_count, "Not treated as eligible device models."),
    ]
    summary_rows = [{"metric": name, "value": value, "notes": notes} for name, value, notes in metrics]

    # Per-year/category/brand tracker uses claimed year first and labels it as unverified research scope.
    progress_rows = []
    for (year, category, brand), grouped in sorted(brand_year_groups.items()):
        assignments = sum(len(FIELD_SETS.get(category, [])) * max(1, len(d.get("variants", []))) for d in grouped)
        images = sum(bool(d.get("imageId")) for d in grouped)
        verified_local = sum(str(d.get("verificationStatus", "")).startswith("VERIFIED_") for d in grouped)
        group_variants = [
            public_variants.get(v.get("id") or f"{d['id']}:base", {})
            for d in grouped for v in (d.get("variants") or [{"id": f"{d['id']}:base"}])
        ]
        group_fields = [field_record for variant_record in group_variants for field_record in variant_record.get("fields", [])]
        models = [d for d in grouped]
        progress_rows.append({
            "year": year, "category": category, "brand": brand, "models": len(grouped),
            "local_status_verified": verified_local, "inserted": len(grouped),
            "spec_complete": sum(model_statuses.get(d["id"]) == "SPECIFICATION_COMPLETE" for d in models),
            "disclosed_gaps": sum(model_statuses.get(d["id"]) == "SPECIFICATION_COMPLETE_WITH_DISCLOSED_GAPS" for d in models),
            "incomplete": sum(model_statuses.get(d["id"]) == "SPECIFICATION_INCOMPLETE" for d in models),
            "applicable_field_assignments": assignments,
            "fields_assessed": sum(x["status"] in ASSESSED_STATUSES for x in group_fields),
            "fields_verified": sum(x["status"] in VERIFIED_STATUSES for x in group_fields),
            "fields_pending": sum(x["status"] not in ASSESSED_STATUSES for x in group_fields),
            "ptg_references_checked": len({d["id"] for d in grouped} & fetched_ids_by_source.get("independent_ph_reference", set())),
            "manufacturer_references_checked": len(({d["id"] for d in grouped} & fetched_ids_by_source.get("official", set())) | ({d["id"] for d in grouped} & manual_reviewed_device_ids)),
            "unsuccessful_fetch_attempts": sum(unextracted_by_id[d["id"]] for d in grouped),
            "independent_technical_references_checked": 0, "approved_images": images,
            "pending_images": len(grouped) - images,
            "status": "COMPLETE" if all(model_statuses.get(d["id"]) == "SPECIFICATION_COMPLETE" for d in models) else "PARTIAL_WITH_PENDING_FIELDS",
        })
    by_device = []
    for device in sorted(device_rows, key=lambda d: (d.get("category", ""), d.get("brand", ""), d.get("model", ""))):
        variant_list = device.get("variants") or [{"id": "base", "label": "Base model"}]
        for variant in variant_list:
            variant_id = variant.get("id") or f"{device['id']}:base"
            variant_audit = public_variants.get(variant_id, {})
            by_device.append({
                "year": year_for(device), "category": device.get("category"), "brand": device.get("brand"),
                "model": device.get("model"), "device_id": device.get("id"),
                "configuration": variant.get("label"), "configuration_id": variant_id,
                "model_status": model_statuses.get(device["id"], "SPECIFICATION_INCOMPLETE"),
                "applicable_fields": variant_audit.get("applicableFields", 0),
                "assessed_fields": variant_audit.get("assessedFields", 0),
                "verified_fields": variant_audit.get("verifiedFields", 0),
                "pending_fields": variant_audit.get("pendingFields", 0),
                "missing_catalog_values": sum(1 for f in variant_audit.get("fields", []) if f.get("value") is None),
            })

    report_lines = [
        "# DeviceIQ Specification Completeness Report", "",
        f"Generated: {full_audit['generatedAt']}", "",
        "> Research status only. The workbook and catalog are provisional research inputs, not a complete or fully verified census of Philippine releases.", "",
        "## Coverage summary", "",
        "| Metric | Actual result |", "| --- | ---: |",
    ]
    report_lines += [f"| {name} | {value} |" for name, value, _ in metrics]
    report_lines += ["", "Assessment coverage = fields with a reviewed status / applicable field rows. Verified coverage = fields supported by reviewed source evidence / applicable field rows. A model remains incomplete while any applicable field is pending or conflicting.", "",
                     "## By category", "", "| Category | Models | Configurations | Applicable field rows | Assessed | Verified | Pending | Assessment | Verified coverage |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for category, entry in category_summary.items():
        report_lines.append(f"| {category} | {entry['models']} | {entry['configurations']} | {entry['fields']} | {entry['assessed']} | {entry['verified']} | {entry['pending']} | {entry['assessed']/entry['fields']:.2%} | {entry['verified']/entry['fields']:.2%} |")
    report_lines += ["", "## Collection snapshot (candidate evidence, not verified facts)", "",
                     f"- Snapshot timestamp: `{latest.get('run_at', 'not recorded')}`.",
                     f"- Fetch attempts: {len(latest.get('fetches', []))}; successful page extractions: {len(extracted_fetches)}.",
                     f"- Extracted pages by source type: `{dict(fetch_sources)}`; extracted models by source type: `{ {k: len(v) for k, v in fetch_models_by_source.items()} }`.",
                     f"- Fetch attempts by category: `{dict(fetch_attempts_by_category)}`; unsuccessful attempts by category: `{dict(fetch_errors_by_category)}`.",
                     f"- Candidate field observations by source type: `{dict(candidate_source_counts)}`.",
                     f"- Candidate prices: {len(latest.get('prices', [])) + manual_pending_price_count}; discovery links: {len(latest.get('discovery', []))}.",
                     "- Source observations are promoted only when the fetched page passes an exact-model check and the field is safe to share across configurations. Unmatched, conflicting, variant-specific, price, and Philippine-availability claims remain candidates until reviewed.",
                     f"- {status_counts[STATUS_PENDING]} applicable fields remain pending because no sufficiently matched source was recorded, a source does not establish the exact variant/region, or the available result is still only a candidate. A blank is not treated as zero or as a negative specification.", "",
                     "## Field backlog", "",
                     "Every category template field is enumerated in `research/enrichment/specification-fields.json`. The full configuration-level evidence matrix is in `research/enrichment/specification-field-audit.json`; a review copy is appended to the supplied workbook when it is available.", "",
                     "| Group | Applicable rows | Assessed | Verified | Pending |", "| --- | ---: | ---: | ---: | ---: |"]
    group_counts = Counter(row["specification_group"] for row in audit_rows)
    for group, count in sorted(group_counts.items()):
        rows = [row for row in audit_rows if row["specification_group"] == group]
        assessed = sum(row["verification_status"] in ASSESSED_STATUSES for row in rows)
        verified = sum(row["verification_status"] in VERIFIED_STATUSES for row in rows)
        report_lines.append(f"| {group} | {count} | {assessed} | {verified} | {count-assessed} |")
    report_lines += ["", "## Priority list", "",
                     f"{incomplete_models} model records remain `SPECIFICATION_INCOMPLETE`. The list below is ordered by pending fields and missing current values, with exact configuration IDs so work can be assigned without merging variants.", "",
                     "| Year (claimed) | Category | Brand | Model | Configuration | Record ID | Missing current values | Applicable fields | Status |", "| --- | --- | --- | --- | --- | --- | ---: | ---: | --- |"]
    for row in sorted(by_device, key=lambda item: (-item["pending_fields"], -item["missing_catalog_values"], item["year"], item["category"], item["brand"], item["model"])):
        report_lines.append(f"| {row['year']} | {row['category']} | {row['brand']} | {row['model']} | {row['configuration']} | `{row['configuration_id']}` | {row['missing_catalog_values']} | {row['applicable_fields']} | {row['model_status']} |")
    report_lines += ["", "## Philippine market and image coverage", "",
                     f"- Models with an exact-match catalog image carrying a reusable license: {image_count}/{len(device_rows)}. The remaining {len(device_rows)-image_count} show the neutral unavailable-image placeholder.",
                     f"- Of those unavailable images, {image_unavailable_counts['REUSE_PERMISSION_REQUIRED']} require reuse permission, {image_unavailable_counts['REUSE_RIGHTS_NOT_ESTABLISHED']} have reuse rights that are not established, and {image_unavailable_counts['NO_RELIABLE_MATCH']} have no reliable exact-model match recorded.",
                     "- The workbook copy's `IMAGE AUDIT` sheet records each image's source, credit, license, rights-check date, and the reason an image is unavailable. Images without documented reuse rights are not published.",
                     f"- Excluded master records: {excluded_count}; held-out records/claims: {held_record_count}. These are visible with explicit labels but stay outside eligible searches/recommendations.",
                     "- The public site retains each record's existing verification and scope status. This specification audit does not upgrade Philippine availability status.", "",
                     "## Reference source policy", ""]
    for source in source_policy.get("sources", []):
        links = []
        if source.get("homepage"):
            links.append(f"[{source['name']}]({source['homepage']})")
        if source.get("robotsTxt"):
            links.append(f"[robots.txt]({source['robotsTxt']})")
        if source.get("termsUrl"):
            links.append(f"[terms]({source['termsUrl']})")
        label = ", ".join(links) if links else source["name"]
        report_lines.append(f"- **{label}** (`{source['id']}`): {source.get('automatedUse', '')} {source.get('promotionRule', '')}")
    report_lines += ["", "## Scope and limitations", "",
                     "- NanoReview and Kimovil are included as manual discovery/reference links. No NanoReview specifications were collected because its published robots rules disallow GPT/ChatGPT automated access. Kimovil specifications and images were not extracted because its terms restrict copying or transformation without express authorization.",
                     f"- The automated collector made {fetch_attempts_by_category.get('laptops', 0)} laptop-page attempts without extracting structured laptop specifications. A separate manual review added official manufacturer evidence for {len({key[0] for key in laptop_reviewed_configurations})}/{len(laptop_device_ids)} laptop models across {len(laptop_reviewed_configurations)} exact configurations; the laptop records remain incomplete where fields are still pending.",
                     "- `NOT_DISCLOSED`, `UNAVAILABLE_AFTER_RESEARCH`, `CONFLICTING_INFORMATION`, and `NOT_APPLICABLE` are reserved for field decisions supported by actual research. They are not assigned by guesswork.",
                     "- `DEVICEIQ_RESEARCH_PROGRESS.md` records actual source-extraction counts and remaining work by claimed year, category, and brand.", ""]
    REPORT.write_text("\n".join(report_lines), encoding="utf-8")

    progress_lines = [
        "# DeviceIQ Research Progress", "", f"Updated: {full_audit['generatedAt']}", "",
        "> Claimed research year is not a verified Philippine release year. Inventory presence does not establish release eligibility.", "",
        "## Actual run totals", "", "| Measure | Count |", "| --- | ---: |",
        f"| Device models | {len(device_rows)} |", f"| Configurations | {len(public_variants)} |",
        f"| Models with manually verified source fields | {len(manually_verified_models)} |",
        f"| Configurations with manually verified source fields | {len(manually_verified_configurations)} |",
        f"| Laptop models with official-source reviews | {len({key[0] for key in laptop_reviewed_configurations})}/{len(laptop_device_ids)} |",
        f"| Laptop configurations with reviewed source fields | {len(laptop_reviewed_configurations)} |",
        f"| Models with all fields assessed | {all_assessed_models} |", f"| Specification-complete models | {complete_models} |",
        f"| Incomplete models | {incomplete_models} |", f"| Applicable field assignments | {len(audit_rows)} |",
        f"| Fields assessed | {assessed_field_count} |", f"| Verified fields | {verified_field_count} |", f"| Pending fields | {status_counts[STATUS_PENDING]} |",
        f"| PTG extracted pages | {fetch_sources.get('independent_ph_reference', 0)} |",
        f"| Official extracted pages | {fetch_sources.get('official', 0)} |",
        f"| Independent technical source pages (NanoReview/Kimovil/Notebookcheck) | 0 |",
        f"| Existing reviewed catalog images | {image_count} |", f"| Models without reviewed catalog image | {len(device_rows)-image_count} |", "",
        "## Brand-year execution tracker", "",
        "The table counts the existing records and this run's review state; it does not mark records researched simply because they were imported.", "",
        "| Claimed year | Category | Brand | Models identified | Models verified locally | Inserted | Specs complete | Disclosed gaps | Incomplete | Fields assessed | Fields verified | Fields pending | PTG pages reviewed | Manufacturer pages reviewed | Unsuccessful fetch attempts | Independent technical pages reviewed | Images approved | Images pending | Status |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in progress_rows:
        progress_lines.append("| " + " | ".join(str(row[k]) for k in ["year", "category", "brand", "models", "local_status_verified", "inserted", "spec_complete", "disclosed_gaps", "incomplete", "fields_assessed", "fields_verified", "fields_pending", "ptg_references_checked", "manufacturer_references_checked", "unsuccessful_fetch_attempts", "independent_technical_references_checked", "approved_images", "pending_images", "status"]) + " |")
    progress_lines += ["", "## Current blockers and next actions", "",
                       "1. Research remaining fields for each exact model and configuration against manufacturer documents and Philippine-market sources.",
                       f"2. Review the {len(latest.get('observations', []))} source-derived field observations and {len(latest.get('prices', [])) + manual_pending_price_count} dated price candidates; retain source URL, quoted excerpt, observed date, region, and exact configuration.",
                       f"3. Continue source coverage for the 438 smartphone and tablet records; the collector has not extracted structured laptop pages, but manual official-source reviews now cover {len({key[0] for key in laptop_reviewed_configurations})}/{len(laptop_device_ids)} laptop models and {len(laptop_reviewed_configurations)} exact configurations.",
                       "4. Use NanoReview and Kimovil only through a permitted manual lookup or written authorization; cross-check any candidate against sources that may be recorded and reused.",
                       "5. Research missing fields before assigning negative statuses; keep all unresolved values blank with `PENDING_VERIFICATION`.",
                       "6. Complete model/configuration image matching and preserve image source, license, and attribution metadata.", "",
                       "See `DEVICEIQ_SPECIFICATION_COMPLETENESS_REPORT.md` and `research/enrichment/specification-field-audit.json` for the record-level matrix.", ""]
    PROGRESS.write_text("\n".join(progress_lines), encoding="utf-8")

    if not args.skip_workbook and args.workbook.exists():
        policies = {x["id"]: x for x in source_policy.get("sources", [])}
        lookups = []
        for device in device_rows:
            links = candidate_links(device)
            for link in links:
                link["policy"] = policies.get(link["sourceId"], {}).get("automatedUse", "Check source terms before access or reuse.")
            lookups.append({"device_id": device["id"], "category": device["category"], "brand": device.get("brand"), "model": device.get("model"), "year": year_for(device), "links": links})
        workbook_summaries = [{"metric": n, "value": v, "notes": note} for n, v, note in metrics]
        workbook_prices = list(latest.get("prices", []))
        for manual_record in manual_reviews.get("records", []):
            device = next((item for item in device_rows if item["id"] == manual_record["deviceId"]), {})
            variant = next((item for item in device.get("variants", []) if item["id"] == manual_record["configurationId"]), {})
            for reviewed_field in manual_record.get("fields", []):
                if reviewed_field.get("fieldId") != "current_price_php" or reviewed_field.get("status") != STATUS_PENDING:
                    continue
                source = next((item for item in manual_record.get("sources", []) if item["id"] == reviewed_field.get("sourceId")), {})
                specs = variant.get("specs", {})
                workbook_prices.append({
                    "device_id": manual_record["deviceId"], "amount_php": reviewed_field.get("normalizedValue"),
                    "variant_ram_gb": specs.get("ramGb"), "variant_storage_gb": specs.get("storageGb"),
                    "configuration_match": reviewed_field.get("configurationMatch", "pending review"),
                    "price_type": "manufacturer starting price candidate", "source_published_at": source.get("publicationDate"),
                    "observed_at": source.get("accessDate"), "local_availability_verified": False,
                    "source_url": source.get("url"), "excerpt": reviewed_field.get("sourceValue"),
                })
        make_workbook_copy(args.workbook, WORKBOOK_COPY, audit_rows, workbook_summaries, lookups,
                           workbook_prices, {d["id"]: d for d in device_rows}, image_manifest, unavailable_images)
        print(f"Enriched workbook copy: {WORKBOOK_COPY}")
    elif not args.skip_workbook:
        print(f"Workbook not found; original was not modified: {args.workbook}")

    print(json.dumps({
        "models": len(device_rows), "heldOutClaims": held_out_count, "configurations": len(public_variants),
        "manuallyVerifiedModels": len(manually_verified_models), "manuallyVerifiedConfigurations": len(manually_verified_configurations),
        "laptopModelsReviewed": len({key[0] for key in laptop_reviewed_configurations}), "laptopConfigurationsReviewed": len(laptop_reviewed_configurations),
        "fieldRows": len(audit_rows), "assessedFields": assessed_field_count,
        "verifiedFields": verified_field_count, "pendingFields": status_counts[STATUS_PENDING],
        "candidateObservations": len(latest.get("observations", [])), "candidatePrices": len(latest.get("prices", [])) + manual_pending_price_count,
        "imageMatchedModels": image_count, "report": str(REPORT), "progress": str(PROGRESS),
        "publicAudit": str(PUBLIC_AUDIT), "workbookCopy": str(WORKBOOK_COPY) if not args.skip_workbook and args.workbook.exists() else None,
    }, indent=2))


if __name__ == "__main__":
    main()
