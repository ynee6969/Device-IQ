#!/usr/bin/env python3
"""Replace iPad Pro M1's unconfigured placeholder with exact 2021 variants."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_e8026097f286fd"
UNRECORDED = f"{DEVICE}-unrecorded"
MODEL = "iPad Pro M1 (2021)"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/apple-ipad-pro-m1-ph-prices-2026-11-27.json"
ARCHIVE = ROOT / "research/enrichment/superseded-model-level-reviews-2026-11-27.json"

URL_11 = "https://support.apple.com/en-us/111897"
URL_12 = "https://support.apple.com/en-us/111896"
URL_MODEL_IDS = "https://support.apple.com/en-us/108043"
URL_ANNOUNCE = "https://www.apple.com/newsroom/2021/04/apple-unveils-new-ipad-pro-with-m1-chip-and-stunning-liquid-retina-xdr-display/"
URL_GLOBAL = "https://www.apple.com/newsroom/2021/05/imac-ipad-pro-and-apple-tv-4k-in-stores-friday/"
URL_PROMOTION = "https://developer.apple.com/documentation/quartzcore/optimizing-iphone-and-ipad-apps-to-support-promotion-displays"
URL_YUGA_PRICE = "https://www.yugatech.com/news/apple-ipad-pro-m1-specs-price-philippines/"
URL_REVU = "https://www.revu.com.ph/2021/05/ipad-pro-2021-m1-chip-now-in-philippines/"
URL_YUGA_LIST = "https://www.yugatech.com/personal-computing/tablet-price-list-2021-philippines/"

CAPACITIES = [
    {"storage": 128, "label": "128 GB", "slug": "128gb", "ram": 8},
    {"storage": 256, "label": "256 GB", "slug": "256gb", "ram": 8},
    {"storage": 512, "label": "512 GB", "slug": "512gb", "ram": 8},
    {"storage": 1024, "label": "1 TB", "slug": "1tb", "ram": 16},
    {"storage": 2048, "label": "2 TB", "slug": "2tb", "ram": 16},
]


def historical_price(size: float, storage: int, cellular: bool) -> int:
    prices = {
        (11.0, 128): 45990, (11.0, 256): 51990, (11.0, 512): 63990,
        (11.0, 1024): 87990, (11.0, 2048): 111990,
        (12.9, 128): 62990, (12.9, 256): 68990, (12.9, 512): 80990,
        (12.9, 1024): 104990, (12.9, 2048): 128990,
    }
    return prices[(size, storage)] + (9000 if cellular else 0)


SIZES = {
    "11in": {
        "size": 11.0, "generation": "3rd generation", "model_wifi": "A2377",
        "model_cell": "A2459", "tech": URL_11,
        "display": "Liquid Retina LED-backlit Multi-Touch IPS LCD",
        "resolution": "2388 x 1668", "battery_wh": 28.65,
        "dimensions": "247.6 x 178.5 x 5.9 mm", "weight_wifi": 466,
        "weight_cell": 470, "image": "https://cdsassets.apple.com/live/7WUAS350/images/ipad/ipad/2021-ipad-pro-11-colors.png",
        "image_scope": "2021 iPad Pro 11-inch (3rd generation), Silver and Space Gray; size-specific official identification image.",
    },
    "12_9in": {
        "size": 12.9, "generation": "5th generation", "model_wifi": "A2378",
        "model_cell": "A2461", "tech": URL_12,
        "display": "Liquid Retina XDR mini-LED-backlit Multi-Touch IPS LCD",
        "resolution": "2732 x 2048", "battery_wh": 40.88,
        "dimensions": "280.6 x 214.9 x 6.4 mm", "weight_wifi": 682,
        "weight_cell": 685, "image": "https://cdsassets.apple.com/live/7WUAS350/images/ipad/ipad/2021-ipad-pro-12-9-colors.png",
        "image_scope": "2021 iPad Pro 12.9-inch (5th generation), Silver and Space Gray; size-specific official identification image.",
    },
}
VARIANTS: list[dict] = []
for size_id, size in SIZES.items():
    for capacity in CAPACITIES:
        for connectivity in ("wifi", "wifi-cellular"):
            cell = connectivity == "wifi-cellular"
            model_code = size["model_cell"] if cell else size["model_wifi"]
            label = f"{size['size']:g}-inch / {capacity['label']} / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}"
            variant = {
                **size, **capacity, "size_id": size_id, "connectivity": connectivity,
                "cellular": cell, "modelCode": model_code, "label": label,
                "historical": historical_price(size["size"], capacity["storage"], cell),
            }
            variant["id"] = f"{DEVICE}-{size_id}-{capacity['slug']}-{connectivity}"
            VARIANTS.append(variant)


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid: str, sid: str, value: str, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      candidate_evidence: list[dict] | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized,
           "note": note or "Exact size, model number, storage and connectivity configuration checked against the cited source."}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if candidate_evidence:
        row["candidateEvidence"] = candidate_evidence
    return row


def nd(fid: str, sid: str, value: str, note: str, unit: str | None = None) -> dict:
    return f(fid, sid, value, None, status="NOT_DISCLOSED", unit=unit, note=note)


def na(fid: str, sid: str, value: str, note: str) -> dict:
    return f(fid, sid, value, None, status="NOT_APPLICABLE", note=note)


def pending(fid: str, sid: str, value: str, note: str, unit: str | None = None) -> dict:
    return f(fid, sid, value, None, status="PENDING_VERIFICATION", unit=unit, note=note)


def sources(v: dict) -> list[dict]:
    return [
        src("apple_ipad_pro_m1_11_specs", URL_11, "Apple Support",
            "Exact technical specification for iPad Pro 11-inch (3rd generation)",
            "Lists capacity, display, M1/CPU/GPU/Neural Engine, RAM by storage tier, cameras, battery energy, physical dimensions/weight by connectivity, wireless, SIM, sensors, USB/Thunderbolt, and accessories."),
        src("apple_ipad_pro_m1_12_9_specs", URL_12, "Apple Support",
            "Exact technical specification for iPad Pro 12.9-inch (5th generation)",
            "Lists capacity, Liquid Retina XDR display, M1/CPU/GPU/Neural Engine, RAM by storage tier, cameras, battery energy, physical dimensions/weight by connectivity, wireless, SIM, sensors, USB/Thunderbolt, and accessories."),
        src("apple_ipad_pro_m1_model_ids", URL_MODEL_IDS, "Apple Support",
            "Exact generation, capacity and regional model-number mapping",
            "Apple identifies 2021 iPad Pro 11-inch (3rd generation) Wi-Fi A2377 and standard Wi-Fi + Cellular A2459, and 12.9-inch (5th generation) Wi-Fi A2378 and standard Wi-Fi + Cellular A2461. A2301/A2379 are separate mmWave models; A2460/A2462 are China-mainland-only models. Philippine local price reports do not give model codes, so these are Apple's matched global model numbers; a Philippine part-number assignment was not separately documented."),
        src("apple_ipad_pro_m1_announcement", URL_ANNOUNCE, "Apple Newsroom",
            "Announcement, product overview, launch software and global preorder window",
            "Apple announced the M1 iPad Pro on 2021-04-20, described 128GB through 2TB capacities, 5G for cellular models, eSIM, external storage, accessories, 100% recycled aluminum, and iPadOS 14.5; initial availability was set for the second half of May.",
            "2021-04-20"),
        src("apple_ipad_pro_m1_global_availability", URL_GLOBAL, "Apple Newsroom",
            "Dated initial global Apple Store/authorized reseller availability",
            "Apple's 2021-05-18 update says deliveries and store/authorized reseller availability around the world began Friday 2021-05-21. This does not establish the first Philippine sale.",
            "2021-05-18"),
        src("apple_promotion_refresh", URL_PROMOTION, "Apple Developer",
            "Refresh-rate range of ProMotion on iPad Pro",
            "Apple Developer documents ProMotion on iPad Pro as dynamically switching between 24Hz and 120Hz; the 2021 size-specific Apple specs identify ProMotion on both models."),
        src("yugatech_ipad_pro_m1_ph_prices", URL_YUGA_PRICE, "YugaTech",
            "Contemporaneous Philippine configuration price report before local availability was announced",
            "Published 2021-04-21, lists all 20 size/storage/connectivity peso prices. The same article explicitly says the date of local availability was yet to be announced; prices are therefore dated reported prices, not a current offer or proof of April local sales.",
            "2021-04-21"),
        src("revu_ipad_pro_m1_ph_prices", URL_REVU, "REVU Philippines",
            "Dated Philippine availability report and matching variant prices",
            "Published 2021-05-27, says the 2021 11-inch and 12.9-inch models were now available in the Philippines, links to Apple Philippines, and lists the same 20 configurations/prices. Supports availability by this date, not the exact first-sale date.",
            "2021-05-27"),
        src("yugatech_2021_tablet_price_list", URL_YUGA_LIST, "YugaTech",
            "Updated 2021 Philippine tablet list with variant prices and a reported launch month",
            "Article published 2021-06-02 and marked updated as of 2021-11-30. It repeats all 20 prices and labels both iPad Pro sizes as April PH launches; this conflicts with YugaTech's 2021-04-21 notice that local availability date was not yet announced and later 2021-05-27 report saying they were now available. Preserve the conflict; do not derive an exact first-sale date.",
            "2021-06-02"),
    ]


def make_fields(v: dict) -> list[dict]:
    cell = v["cellular"]
    spec = "apple_ipad_pro_m1_11_specs" if v["size_id"] == "11in" else "apple_ipad_pro_m1_12_9_specs"
    model_source = "apple_ipad_pro_m1_model_ids"
    yuga = "yugatech_ipad_pro_m1_ph_prices"
    revu = "revu_ipad_pro_m1_ph_prices"
    size_display = f"{v['size']:g}-inch"
    weights_yuga = 468 if (v["size"] == 11.0 and cell) else 684 if (v["size"] == 12.9 and cell) else None
    weight_evidence = ([{
        "value": weights_yuga, "unit": "g", "sourceUrl": URL_YUGA_PRICE,
        "sourceKind": "dated_philippine_secondary_source", "observedAt": "2021-04-21",
        "excerpt": f"YugaTech reports {weights_yuga}g for the {size_display} Wi-Fi + Cellular model.",
        "configurationMatch": f"{size_display} / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}",
        "reviewStatus": "CONFLICTING_INFORMATION",
    }] if weights_yuga is not None else None)
    launch_price = pending(
        "official_launch_price_php", revu,
        f"YugaTech and REVU report PHP {v['historical']:,} for {v['label']}, but an authoritative Apple/authorized-retailer launch MSRP record was not located.",
        "Keep the official launch MSRP blank. The two dated Philippine publications' exact configuration prices are preserved as historical price observations, not asserted to be official first-day MSRP.",
        "PHP")
    launch_price["replaceExisting"] = True
    model_field = f("model_number", model_source, v["modelCode"], v["modelCode"],
        note=f"Apple maps {v['modelCode']} to the {size_display} {v['generation']} {('standard Wi-Fi + Cellular' if cell else 'Wi-Fi')} global model. The mmWave model number and China-only cellular model are separate and excluded; the local PH price articles do not independently identify the regional part number.")
    model_field["replaceExisting"] = True
    configuration_field = f("configuration", spec,
        f"{size_display} / {v['ram']}GB unified memory / {v['label'].split(' / ')[1]} / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}",
        f"{size_display} / {v['ram']} GB RAM / {v['label'].split(' / ')[1]} / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}",
        note=f"Apple's size-specific technical specification identifies the storage tier and RAM amount; Apple's model-identification page separately maps connectivity to {'Wi-Fi + Cellular' if cell else 'Wi-Fi'} model {v['modelCode']}. The model number is Apple's global model mapping, not a separately confirmed local part number.")
    configuration_field["replaceExisting"] = True
    rows = [
        model_field,
        f("global_release_date", "apple_ipad_pro_m1_global_availability", "Apple announced 2021-04-20; initial global store and authorized reseller availability began 2021-05-21", "2021-05-21", unit="date",
          note="Apple Newsroom gives the announcement date and then confirms worldwide store/authorized reseller availability from 2021-05-21. This is the global date, not a Philippine first-sale date."),
        configuration_field,
        pending("philippine_release_date", "yugatech_2021_tablet_price_list",
                "The exact Philippine first-sale date is unresolved: YugaTech's 2021-04-21 article said local availability was yet to be announced; its table updated 2021-11-30 reports an April launch month; REVU reported the models now available on 2021-05-27.",
                "Do not use a specific Philippine date or month. Evidence supports availability by 2021-05-27; the annual list's April label is retained as conflicting evidence."),
        launch_price,
        pending("current_price_php", revu,
                "No current buyable Philippine listing or stock check was part of this dated historical review; the 2021 prices are not current prices.",
                "Keep current price blank; retain only dated historical Philippine price evidence.", "PHP"),
        f("display_size", spec, f"{size_display} diagonal", v["size"], key="displayInches", unit="in"),
        f("display_technology", spec, v["display"], v["display"], key="displayType"),
        f("display_resolution", spec, v["resolution"], v["resolution"], key="resolution", note=f"Apple lists {v['resolution']} pixels for the {size_display} {v['generation']} model."),
        f("display_refresh_rate", "apple_promotion_refresh", "ProMotion adaptive refresh from 24Hz to 120Hz", 120, key="refreshHz", unit="Hz",
          note="Apple's size-specific technical specification lists ProMotion; Apple Developer documents the supported iPad Pro ProMotion range as 24Hz to 120Hz."),
        f("display_brightness", spec,
          "SDR brightness: up to 600 nits; XDR brightness: up to 1,000 nits full-screen and 1,600 nits peak HDR" if v["size"] == 12.9 else "SDR brightness: up to 600 nits",
          "600 nits SDR; 1000 nits full-screen XDR; 1600 nits peak HDR" if v["size"] == 12.9 else "600 nits SDR", unit="nits"),
        f("display_protection", spec, "P3 wide color, True Tone, fully laminated display, anti-reflective coating, fingerprint-resistant oleophobic coating", "P3; True Tone; fully laminated; anti-reflective; oleophobic coating"),
        f("chipset", spec, "Apple M1 chip", "Apple M1", key="chipset"),
        nd("process_node", "apple_ipad_pro_m1_announcement", "The reviewed Apple iPad Pro technical pages and launch announcement do not state a fabrication node for this iPad configuration.", "No process node inferred from other M1 products or third-party reports.", "nm"),
        f("cpu", spec, "8-core CPU: 4 performance cores and 4 efficiency cores", "8-core CPU (4 performance + 4 efficiency)", key="cpu"),
        f("gpu", spec, "8-core GPU", "8-core Apple GPU", key="gpu"),
        f("operating_system", "apple_ipad_pro_m1_announcement", "Apple announced iPadOS 14.5 in the launch release; its current technical pages show iPadOS 15.", "iPadOS 14.5", key="os",
          note="The launch release says iPadOS 14.5 would become available in the week after announcement, while Apple's current technical pages have since been updated to iPadOS 15. This is not a claim about the currently installed OS version."),
        nd("os_support", spec, "Apple does not publish a guaranteed iPadOS support end date for this model.", "Support duration/end date not inferred."),
        f("ram_capacity", spec, f"{v['ram']}GB unified memory for {v['label']}", v["ram"], key="ramGb", unit="GB",
          note="Apple explicitly lists 8GB RAM for 128GB/256GB/512GB models and 16GB RAM for 1TB/2TB models."),
        nd("ram_type", spec, "Apple does not identify the memory technology/type on the reviewed specification page.", "Memory type not inferred."),
        f("storage_capacity", spec, v["label"], v["storage"], key="storageGb", unit="GB",
          note="Apple lists marketed 1TB and 2TB capacities. Numeric catalog values use the conventional 1024GB and 2048GB equivalents; printed labels retain Apple's TB units."),
        nd("storage_type", spec, "Apple does not specify the internal storage interface or media type on the reviewed technical specification.", "Storage interface/type not inferred."),
        f("storage_expansion", "apple_ipad_pro_m1_announcement", "Thunderbolt/USB 4 supports external storage accessories; internal storage remains the selected fixed capacity.", "External storage can connect over Thunderbolt/USB 4; no removable internal expansion claimed"),
        f("rear_camera_system", spec, "12MP Wide ƒ/1.8 and 10MP Ultra Wide ƒ/2.4 rear cameras with 125-degree field of view", 12, key="rearCameraMp", unit="MP", note="Apple identifies both rear camera modules and their apertures; the numeric catalog field denotes the main wide camera's 12MP resolution. The 10MP Ultra Wide module is detailed separately."),
        nd("main_camera_sensor", spec, "Apple does not identify the sensor manufacturer or sensor part number.", "Sensor make/model not disclosed."),
        f("ultrawide_camera", spec, "10MP rear Ultra Wide camera, ƒ/2.4, 125-degree field of view", "10MP rear Ultra Wide, f/2.4, 125-degree FoV"),
        na("telephoto_camera", spec, "Apple lists rear Wide and Ultra Wide cameras; no rear telephoto module is listed.", "No telephoto camera specified for this model."),
        f("front_camera", spec, "12MP TrueDepth Ultra Wide camera, ƒ/2.4, 122-degree field of view", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", spec, "Rear: 4K at 24/25/30/60fps; 1080p at 25/30/60fps; 720p at 30fps; 1080p slow motion at 120/240fps. Front: 1080p at 25/30/60fps.", "Rear 4K/60fps; front 1080p/60fps; slow motion 1080p/240fps", key="video"),
        f("battery_capacity", spec, f"Built-in {v['battery_wh']}Wh rechargeable lithium-polymer battery; mAh is not published", v["battery_wh"], key="batteryWh", unit="Wh",
          note="Apple publishes battery energy in watt-hours, not mAh. No mAh conversion is made without a published nominal voltage."),
        f("battery_technology", spec, "Rechargeable lithium-polymer battery", "Lithium-polymer"),
        f("wired_charging", spec, "USB-C wired charging; Apple lists charging via power adapter or USB-C computer and includes a 20W USB-C adapter. Maximum device input wattage is not stated.", "USB-C wired charging; 20W adapter included; maximum input not stated"),
        nd("wireless_charging", spec, "Wireless or reverse charging is not listed in Apple's reviewed technical specification.", "No wireless charging capability inferred from omission."),
        f("dimensions", spec, v["dimensions"], v["dimensions"], key="dimensions", unit="mm"),
        f("weight", spec, f"{'Wi-Fi + Cellular' if cell else 'Wi-Fi'} model: {v['weight_cell'] if cell else v['weight_wifi']}g", v["weight_cell"] if cell else v["weight_wifi"], key="weightG", unit="g",
          note=("Apple's size-specific technical specification lists 470g; YugaTech's 2021-04-21 summary lists 468g for the 11-inch Wi-Fi + Cellular model. The manufacturer value is retained; the secondary discrepancy is preserved in candidate evidence." if v["size"] == 11.0 and cell else
                "Apple's size-specific technical specification lists 685g; YugaTech's 2021-04-21 summary lists 684g for the 12.9-inch Wi-Fi + Cellular model. The manufacturer value is retained; the secondary discrepancy is preserved in candidate evidence." if v["size"] == 12.9 and cell else
                "Apple lists the size/connectivity-specific device weight."), candidate_evidence=weight_evidence),
        f("materials", "apple_ipad_pro_m1_announcement", "Aluminum enclosure made with 100% recycled aluminum", "Aluminum enclosure (100% recycled aluminum)"),
        nd("ingress_protection", spec, "Apple's reviewed specifications do not publish an IP water- or dust-resistance rating.", "No IP rating inferred."),
    ]
    if cell:
        rows += [
            f("sim_esim", spec, "Wi-Fi + Cellular models list Nano-SIM and eSIM", "Nano-SIM and eSIM", key="sim"),
            pending("cellular_bands", spec,
                    f"Apple lists detailed bands under the separate mmWave model ({'A2301' if v['size'] == 11.0 else 'A2379'}), not exact Philippine cellular model {v['modelCode']}.",
                    f"Do not transfer the mmWave variant's band list to {v['modelCode']}; exact A2459/A2461 band support remains unverified."),
            f("gnss", spec, "GPS/GNSS is listed for Wi-Fi + Cellular models", "GPS/GNSS"),
            f("tablet_cellular_variant", spec, f"Wi-Fi + Cellular {v['modelCode']}; 5G/LTE cellular model", "Wi-Fi + Cellular 5G/LTE", key="cellular"),
        ]
    else:
        rows += [
            na("sim_esim", model_source, f"Wi-Fi-only {v['modelCode']}; SIM/eSIM does not apply", "Apple identifies the cellular model as a separate configuration."),
            na("cellular_bands", model_source, f"Wi-Fi-only {v['modelCode']} has no cellular radio", "Cellular bands are not applicable to Wi-Fi-only configuration."),
            nd("gnss", spec, "Apple lists GPS/GNSS for Wi-Fi + Cellular models; it does not list built-in GPS/GNSS for this Wi-Fi model.", "Wi-Fi model has no GPS/GNSS feature stated by Apple."),
            f("tablet_cellular_variant", spec, f"Wi-Fi-only model {v['modelCode']}", "Wi-Fi only; no cellular modem", key="cellular"),
        ]
    rows += [
        f("wifi", spec, "Wi-Fi 6 (802.11ax), dual band, MIMO", "Wi-Fi 6 (802.11ax); dual band; MIMO", key="wifi"),
        f("bluetooth", spec, "Bluetooth 5.0", "Bluetooth 5.0"),
        f("usb", spec, "Thunderbolt/USB 4 over USB-C; Thunderbolt 3 and USB 4 up to 40Gb/s; USB 3.1 Gen 2 up to 10Gb/s; DisplayPort", "USB-C; Thunderbolt 3 / USB 4 up to 40Gb/s; USB 3.1 Gen 2 up to 10Gb/s; DisplayPort", key="ports"),
        nd("nfc", spec, "NFC is not listed in Apple's reviewed technical specification.", "NFC not inferred."),
        f("audio", spec, "Four speakers and five microphones; no analog headphone jack is listed", "Four speakers; five microphones" , key="sound"),
        f("sensors", spec, "Face ID/TrueDepth, LiDAR Scanner, three-axis gyro, accelerometer, barometer, ambient-light sensor", "Face ID; LiDAR; three-axis gyro; accelerometer; barometer; ambient-light sensor"),
        f("tablet_stylus", spec, "Apple Pencil (2nd generation) and Apple Pencil (USB-C) supported", "Apple Pencil (2nd generation); Apple Pencil (USB-C)", key="stylus"),
        f("tablet_keyboard", "apple_ipad_pro_m1_announcement", "Magic Keyboard and Smart Keyboard Folio compatible", "Apple Magic Keyboard; Smart Keyboard Folio", key="keyboard"),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct field reviews, got {len(rows)}")
    return rows


def availability(v: dict) -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "REVU reported on 2021-05-27 that both 2021 iPad Pro sizes were now available in the Philippines and linked to Apple Philippines. YugaTech also published exact peso prices, but its dated reports conflict about the Philippine launch month/date. Exact first local sale date is unresolved; current resale stock and price were not checked.",
        "philippineAvailability": "Philippine availability is reported by REVU by 2021-05-27 with a link to the Apple Philippines store. The exact first-sale date/month remains unresolved because YugaTech's April 21 report said it was not announced while its later annual list labels April as the launch month.",
        "observedAt": OBSERVED,
        "qualityFlag": "Apple's model-number mapping, size-specific specifications and exact storage/RAM configurations are reviewed. A dated Philippine availability report and matching historical local prices are recorded. The first-sale date/month is disputed; current price and stock are unverified; exact A2459/A2461 cellular band lists remain pending. Study eligibility remains Pending.",
        "catalogModel": MODEL, "manufacturer": "Apple Inc.", "productLine": "iPad Pro",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "First dated Philippine availability report; exact first-sale date unresolved",
        "researchNotes": f"Workbook row 49 is matched to the 2021 M1 iPad Pro family. Apple documents two distinct configurations by size/generation: 11-inch (3rd generation) and 12.9-inch (5th generation). This record is represented as five storage capacities × Wi-Fi/Wi-Fi + Cellular for each size (20 exact configurations). Apple maps Wi-Fi/cellular variants to A2377/A2459 (11-inch) and A2378/A2461 (12.9-inch); US mmWave and China-only model numbers are not substituted. REVU reported PH availability by 2021-05-27 and listed exact prices; the first-sale timing remains unresolved because YugaTech sources conflict. Battery is retained in Wh as Apple reports it. Current prices and stock are not asserted. Apple image candidates are preserved for rights review; the public catalog keeps the neutral placeholder. Study scope remains Pending.",
        "openIssues": [
            {"issue": "Exact Philippine first-sale date/month is unresolved", "action": "Keep exact date blank and retain the 2021-05-27 dated availability report plus the conflicting YugaTech April-month entry."},
            {"issue": "Current price and buyable stock were not checked", "action": "Keep current price blank; preserve only dated historical price reports."},
            {"issue": "Exact A2459/A2461 cellular band lists are not identified in Apple's reviewed band table", "action": "Keep cellular bands pending; do not copy the US mmWave models' list."},
            {"issue": "Image reuse rights are not established", "action": "Keep neutral placeholder and retain exact-size Apple image candidates for rights review."},
            {"issue": "Study eligibility remains Pending", "action": "Preserve the workbook study scope."},
        ],
    }


def make_review(v: dict, index: int, replace_placeholder: bool) -> dict:
    record = {"deviceId": DEVICE, "configurationId": v["id"], "brand": "Apple",
              "model": MODEL, "configuration": v["label"], "configurationLabel": v["label"],
              "modelCode": v["modelCode"], "sources": sources(v), "fields": make_fields(v),
              "availabilityEvidence": availability(v)}
    variant = {"id": v["id"], "label": v["label"], "modelCode": v["modelCode"],
               "notes": f"Distinct {v['size']:g}-inch {v['generation']} Apple storage/connectivity configuration; Silver and Space Gray finishes are not split."}
    if replace_placeholder:
        record["replacementVariants"] = ([{
            "id": item["id"], "label": item["label"], "modelCode": item["modelCode"],
            "notes": f"Distinct {item['size']:g}-inch {item['generation']} Apple storage/connectivity configuration; Silver and Space Gray finishes are not split.",
        } for item in VARIANTS] if index == 0 else [variant])
        if index == 0:
            record["replaceUnrecordedPlaceholder"] = True
    return record


def price_rows() -> list[dict]:
    rows = []
    for v in VARIANTS:
        for source_id, url, date, kind, availability_verified, status in [
            ("yugatech_ipad_pro_m1_ph_prices", URL_YUGA_PRICE, "2021-04-21",
             "dated_secondary_ph_price_report_before_local_availability_date_announced", False,
             "price_reported_2021_04_21_local_availability_not_yet_announced"),
            ("revu_ipad_pro_m1_ph_prices", URL_REVU, "2021-05-27",
             "dated_secondary_ph_price_and_local_availability_report", True,
             "reported_available_in_ph_by_2021_05_27_exact_first_sale_unknown"),
        ]:
            rows.append({
                "device_id": DEVICE, "amount_php": v["historical"], "configuration_id": v["id"],
                "configuration_match": f"exact_ipad_pro_m1_{v['size_id']}_{v['slug']}_{v['connectivity']}",
                "variant_storage_gb": v["storage"],
                "variant_connectivity": "Wi-Fi + Cellular" if v["cellular"] else "Wi-Fi",
                "variant_display_size_in": v["size"], "variant_model_number": v["modelCode"],
                "price_type": "historical_ph_published_configuration_price_not_confirmed_first_day_msrp",
                "source_published_at": date,
                "excerpt": f"{('YugaTech' if source_id.startswith('yuga') else 'REVU')} lists PHP {v['historical']:,} for the exact {v['label']} configuration. This is a dated 2021 PH report, not a current offer or confirmed first-day MSRP.",
                "source_url": url,
                "source_kind": kind,
                "observed_at": date,
                "local_availability_verified": availability_verified,
                "availability_status": status,
            })
    return rows


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the pending workbook iPad Pro M1 record; refusing unexpected scope/device.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {v["id"] for v in VARIANTS}
    replacing_placeholder = len(current_ids) == 1 and current_ids == {UNRECORDED}
    updating_integrated = current_ids == expected_ids
    if not (replacing_placeholder or updating_integrated):
        raise ValueError("Expected either the original unrecorded placeholder or the exact 20 integrated variants; refusing unexpected configurations.")

    archive = json.loads(ARCHIVE.read_text(encoding="utf-8")) if ARCHIVE.exists() else {"records": []}
    old = next((r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED), None)
    if old:
        exists = any(r.get("deviceId") == DEVICE and r.get("supersededConfigurationId") == UNRECORDED for r in archive["records"])
        if not exists:
            archive["records"].append({"deviceId": DEVICE, "model": MODEL,
                "supersededConfigurationId": UNRECORDED, "supersededAt": OBSERVED,
                "reason": "Replaced one model-level placeholder with 20 exact size/storage/connectivity configurations; original source review is retained in this archive.",
                "review": old})
        manual["records"] = [r for r in manual["records"] if not (r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED)]
    ARCHIVE.write_text(json.dumps(archive, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # The catalog builder always starts from the read-only workbook's single
    # unconfigured placeholder. Keep the reviewed replacement declaration on
    # the first record even when this script is rerun after a prior build.
    for review in [make_review(v, index, True) for index, v in enumerate(VARIANTS)]:
        add_review(manual, catalog, review)
    targets = {(DEVICE, v["id"]) for v in VARIANTS}
    for v in VARIANTS[1:]:
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, v["id"]))
        saved.pop("replacementVariants", None)
        saved.pop("replaceUnrecordedPlaceholder", None)
        saved.pop("additionalVariants", None)
    deduplicate_target_reviews(manual, targets)
    for v in VARIANTS:
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, v["id"]))
        saved.update({"model": MODEL, "configuration": v["label"], "configurationLabel": v["label"], "modelCode": v["modelCode"]})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Apple Support provides exact-size 2021 model-identification illustrations, but no permission or reusable license for publication or hotlinking was recorded. Keep the neutral placeholder.",
        "sourcePage": URL_MODEL_IDS, "assetUrl": None,
        "candidateAssetUrl": SIZES["11in"]["image"],
        "candidateImages": [
            {"displaySize": f"{SIZES[key]['size']:g}-inch", "assetUrl": value["image"],
             "sourcePage": URL_MODEL_IDS, "scope": value["image_scope"],
             "publisher": "Apple", "rightsTermsUrl": None,
             "rightsCheck": "No reuse permission/license is recorded; do not download or hotlink."}
            for key, value in SIZES.items()
        ],
        "scope": "Two exact-size Apple Support product diagrams for iPad Pro M1 (2021), separated by 11-inch/12.9-inch generation; not a storage or connectivity-specific photograph.",
        "rightsTermsUrl": None,
        "rightsCheck": "No reuse permission or license was found on the reviewed Apple Support page. Do not download or hotlink.",
        "rightsCheckSourcePage": URL_MODEL_IDS, "observedAt": OBSERVED,
        "altText": "Image unavailable for Apple iPad Pro M1 (2021)",
    }
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = price_rows()
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Apple", "model_name": MODEL,
                    "category": "tablets", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": s["url"], "source_kind": s["purpose"],
                       "status": "reviewed", "result": s["note"]} for s in sources(VARIANTS[0])],
        "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    model = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if model:
        model["status"] = "manually_reviewed"
    known = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type"), p.get("source_url")) for p in latest.get("prices", [])}
    for price in prices:
        key = (price["device_id"], price["configuration_id"], price["price_type"], price["source_url"])
        if key not in known:
            latest.setdefault("prices", []).append(price)
            known.add(key)
    latest["run_at"] = OBSERVED
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "model": MODEL,
        "configurations": [{"id": v["id"], "modelNumber": v["modelCode"], "label": v["label"],
                            "historicalPhilippinePricePhp": v["historical"], "currentPricePhp": None}
                           for v in VARIANTS],
        "reviewedConfigurations": len(VARIANTS), "reviewedFieldsPerConfiguration": 49,
        "philippineAvailability": "REVU reported available in PH by 2021-05-27; exact first-sale date/month unresolved",
        "priceConflicts": "Same exact variant prices are repeated by YugaTech and REVU; they are dated historical quotes, not current offers or confirmed first-day MSRP.",
        "image": "two exact-size Apple product diagrams retained as rights-unverified candidates; neutral placeholder kept",
        "eligibility": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
