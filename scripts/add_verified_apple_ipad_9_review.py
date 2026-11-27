#!/usr/bin/env python3
"""Replace the iPad 9th Gen placeholder with exact PH storage/connectivity configs."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_80a03073c65780"
UNRECORDED = f"{DEVICE}-unrecorded"
MODEL = "iPad 9th Gen"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/apple-ipad-9-ph-prices-2026-11-27.json"
ARCHIVE = ROOT / "research/enrichment/superseded-model-level-reviews-2026-11-27.json"

URL_TECH = "https://support.apple.com/en-us/111898"
URL_MODEL_IDS = "https://support.apple.com/en-us/108043"
URL_NEWS = "https://www.apple.com/newsroom/2021/09/apples-most-popular-ipad-delivers-even-more-performance-and-advanced-features/"
URL_PH = "https://www.yugatech.com/personal-computing/apple-ipad-2021-ipad-mini-2021-now-available-in-the-philippines/"
URL_PICKAROO = "https://pickaroo.com/power-mac-center/products/power-mac-center-sm-city-pampanga?group=682-ipad&list=True"
IMAGE_ASSET = "https://cdsassets.apple.com/live/SZLF0YNV/images/sp/111898_sp849-ipad-9gen-480.png"

VARIANTS = [
    {"storage": 64, "connectivity": "wifi", "label": "64 GB / Wi-Fi", "modelCode": "A2602", "historical": 19990, "listed": 25490},
    {"storage": 256, "connectivity": "wifi", "label": "256 GB / Wi-Fi", "modelCode": "A2602", "historical": 28990, "listed": 34490},
    {"storage": 64, "connectivity": "wifi-cellular", "label": "64 GB / Wi-Fi + Cellular", "modelCode": "A2604", "historical": 27990, "listed": 33990},
    {"storage": 256, "connectivity": "wifi-cellular", "label": "256 GB / Wi-Fi + Cellular", "modelCode": "A2604", "historical": 36990, "listed": 42490},
]
for variant in VARIANTS:
    variant["id"] = f"{DEVICE}-{variant['storage']}gb-{variant['connectivity']}"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid: str, sid: str, value: str, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      price_condition: str | None = None, price_type: str | None = None,
      price_observed: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized,
           "note": note or "Exact iPad (9th generation) model fact checked against the cited source."}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if price_condition:
        row.update({"priceCondition": price_condition, "priceType": price_type,
                    "priceObservedAt": price_observed})
    return row


def nd(fid: str, sid: str, value: str, note: str, unit: str | None = None) -> dict:
    return f(fid, sid, value, None, status="NOT_DISCLOSED", unit=unit, note=note)


def na(fid: str, sid: str, value: str, note: str) -> dict:
    return f(fid, sid, value, None, status="NOT_APPLICABLE", note=note)


def pending(fid: str, sid: str, value: str, note: str, unit: str | None = None) -> dict:
    return f(fid, sid, value, None, status="PENDING_VERIFICATION", unit=unit, note=note)


def sources(v: dict) -> list[dict]:
    return [
        src("apple_ipad9_tech_specs", URL_TECH, "Apple Support",
            "Technical specifications for iPad (9th generation)",
            "Apple lists capacities, display, A13 Bionic, cameras, battery energy, dimensions and weights by connectivity, Wi-Fi, audio, ports, SIM features, sensors and accessories."),
        src("apple_ipad9_model_identification", URL_MODEL_IDS, "Apple Support",
            "Exact model number, generation, capacity and connectivity mapping",
            "Apple identifies A2602 as iPad (9th generation) and A2604 as Wi-Fi + Cellular; A2603 is North America only and A2605 is China mainland only. Capacities are 64GB and 256GB."),
        src("apple_ipad9_newsroom", URL_NEWS, "Apple Newsroom",
            "Announcement, initial-market availability, launch OS and product overview",
            "Apple announced iPad (9th generation) on 2021-09-14 and said store availability in initial markets begins 2021-09-24. It shipped with iPadOS 15 and supports Apple Pencil (1st generation) and Smart Keyboard.",
            "2021-09-14"),
        src("yugatech_ipad9_ph", URL_PH, "YugaTech",
            "Dated Philippine availability and configuration prices",
            "Article dated 2021-10-10 says the 2021 iPad is now available in the Philippines, lists 64GB/256GB Wi-Fi and cellular configurations, says they can be purchased on Apple Philippines, and lists four prices. This is a dated availability report, not proof of the first transaction date.",
            "2021-10-10"),
        src("pickaroo_pmc_ipad9_listing", URL_PICKAROO, "Pick.A.Roo / Power Mac Center - SM City Pampanga",
            "Exact configuration retailer-listing price cross-check; not used as a buyable current price",
            "The page displays exact iPad 9th Gen variants and prices with Add controls, but marks the store CLOSED and says it is outside delivery range. Current stock/orderability is therefore not verified; prices are retained as page-listed observations only."),
    ]


def make_fields(v: dict) -> list[dict]:
    cell = v["connectivity"] == "wifi-cellular"
    model_source = "apple_ipad9_model_identification"
    tech = "apple_ipad9_tech_specs"
    local = "yugatech_ipad9_ph"
    cfg = f("configuration", tech,
            f"{v['storage']}GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}; model {v['modelCode']}",
            f"{v['storage']} GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'} / {v['modelCode']}",
            note="Apple identifies separate 64GB and 256GB capacities and distinguishes A2602 Wi-Fi from A2604 Wi-Fi + Cellular. Color is not a separate technical configuration.")
    rows = [
        f("model_number", model_source, v["modelCode"], v["modelCode"], note="Apple maps A2602 to iPad (9th generation) and A2604 to its Wi-Fi + Cellular model; A2603 and A2605 are explicitly regional models and are not assigned to these PH configurations."),
        f("global_release_date", "apple_ipad9_newsroom", "Announced 2021-09-14; store availability in initial markets from 2021-09-24", "2021-09-24", note="Apple's announcement gives 2021-09-14 as the announcement date and says store availability in initial markets begins 2021-09-24. This is not the Philippine availability date."),
        cfg,
        pending("philippine_release_date", local, "YugaTech reported on 2021-10-10 that the 2021 iPad was now available in the Philippines; no exact first-sale date is stated.", "Retain the exact Philippine first-sale date as unrecorded. The dated report proves availability by 2021-10-10, not the date sales first began."),
        f("official_launch_price_php", local,
          f"PHP {v['historical']:,} ({v['storage']}GB, {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}) in YugaTech's 2021-10-10 PH availability article",
          v["historical"], status="VERIFIED_SECONDARY", unit="PHP",
          note="Contemporaneous secondary Philippine report dated 2021-10-10 lists this exact storage/connectivity price and says the device can be purchased from Apple Philippines. It does not label the amount as the exact first-day MSRP."),
        pending("current_price_php", "pickaroo_pmc_ipad9_listing",
                f"A Power Mac Center listing displayed PHP {v['listed']:,} for {v['label']} on the reviewed page.",
                "The page labels its store CLOSED and says delivery is unavailable for the selected location. Preserve as a dated retailer listing observation only; do not treat this as an available/current buyable price or use it for numeric filtering.", "PHP"),
        f("display_size", tech, "10.2-inch diagonal", 10.2, key="displayInches", unit="in"),
        f("display_technology", tech, "LED-backlit Multi-Touch display with IPS technology", "LED-backlit Multi-Touch IPS LCD", key="displayType"),
        f("display_resolution", tech, "2160-by-1620 pixels", "2160 x 1620", key="resolution"),
        nd("display_refresh_rate", tech, "Apple does not state a refresh rate in the technical specifications.", "Refresh rate is not inferred." , "Hz"),
        f("display_brightness", tech, "500 nits", "500 nits", unit="nits"),
        f("display_protection", tech, "Fingerprint-resistant oleophobic coating", "Fingerprint-resistant oleophobic coating"),
        f("chipset", tech, "A13 Bionic chip", "Apple A13 Bionic", key="chipset"),
        nd("process_node", tech, "Apple's technical specifications do not state a semiconductor process node.", "Process node is not inferred.", "nm"),
        nd("cpu", tech, "Apple identifies the A13 Bionic chip but does not state CPU core count/configuration on this specification page.", "No CPU core configuration inferred."),
        nd("gpu", tech, "Apple identifies the A13 Bionic chip but does not state GPU core count/configuration on this specification page.", "No GPU core configuration inferred."),
        f("operating_system", "apple_ipad9_newsroom", "Ships with iPadOS 15; Apple Support describes the platform as iPadOS", "iPadOS", key="os", note="iPadOS is the platform. iPadOS 15 is the original launch version; a current software version is not asserted."),
        nd("os_support", tech, "Apple does not publish a guaranteed end date for iPadOS support on this page.", "Do not infer an end-of-support date."),
        nd("ram_capacity", tech, "Apple does not state RAM capacity in the reviewed technical specifications.", "RAM remains unrecorded; no estimate substituted.", "GB"),
        nd("ram_type", tech, "Apple does not state RAM type in the reviewed technical specifications.", "Memory type remains unrecorded."),
        f("storage_capacity", tech, f"{v['storage']}GB", v["storage"], key="storageGb", unit="GB"),
        nd("storage_type", tech, "Apple does not state a flash-storage interface/type in the reviewed specification.", "Storage type is not inferred."),
        nd("storage_expansion", tech, "Apple does not document an external storage expansion option on the reviewed specification page.", "Expansion capability remains unrecorded rather than inferred from omission."),
        f("rear_camera_system", tech, "8MP Wide camera, ƒ/2.4", "8 MP Wide rear camera; f/2.4", key="rearCameraMp"),
        nd("main_camera_sensor", tech, "Apple does not identify the rear image sensor manufacturer or model.", "Sensor make/model not disclosed."),
        na("ultrawide_camera", tech, "The rear camera is an 8MP Wide camera; no rear Ultra Wide camera is listed.", "The Ultra Wide camera on this model is front-facing."),
        na("telephoto_camera", tech, "No telephoto rear camera is listed.", "Apple specifies a single Wide rear camera."),
        f("front_camera", tech, "12MP Ultra Wide camera, 122-degree field of view, ƒ/2.4", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", tech, "Rear: 1080p at 25/30fps and 720p at 30fps; rear slow-motion 720p at 120fps; front: 1080p at 25/30/60fps", "Rear 1080p/30fps; front 1080p/60fps; slow motion 720p/120fps", key="video"),
        f("battery_capacity", tech, "Built-in 32.4Wh rechargeable lithium-polymer battery; Apple does not list mAh", 32.4, key="batteryWh", unit="Wh", note="Apple publishes energy in watt-hours, not milliampere-hours. No mAh conversion is made without a published nominal voltage."),
        f("battery_technology", tech, "Rechargeable lithium-polymer battery", "Lithium-polymer"),
        nd("wired_charging", tech, "Apple states charging via power adapter or USB-C to computer; it does not state maximum input wattage. A 20W USB-C adapter is listed in the box.", "Included adapter wattage is not treated as device charging-rate specification.", "W"),
        nd("wireless_charging", tech, "Wireless/reverse charging is not specified on the reviewed Apple page.", "No capability inferred from omission."),
        f("dimensions", tech, "250.6 × 174.1 × 7.5 mm", "250.6 x 174.1 x 7.5 mm", key="dimensions", unit="mm"),
        f("weight", tech, "Wi-Fi: 487g; Wi-Fi + Cellular: 498g", 498 if cell else 487, key="weightG", unit="g"),
        nd("materials", tech, "Apple's reviewed technical specification does not identify chassis material composition.", "Material claims not inferred."),
        nd("ingress_protection", tech, "Apple's reviewed technical specification does not state an IP water/dust rating.", "No IP rating inferred."),
    ]
    if cell:
        rows += [
            f("sim_esim", tech, "Wi-Fi + Cellular models list Nano-SIM and eSIM", "Nano-SIM and eSIM", key="sim", note="Apple's technical specification lists Nano-SIM/eSIM for the Wi-Fi + Cellular family; it does not provide A2604-specific SIM details in the rendered table."),
            pending("cellular_bands", tech, "Apple lists UMTS and LTE bands under model A2603 (North America); this record is model A2604.", "Do not assign A2603's region-specific bands to A2604. Exact A2604 supported band list remains unverified."),
            f("gnss", tech, "GPS/GNSS on Wi-Fi + Cellular models", "GPS/GNSS"),
            f("tablet_cellular_variant", tech, "Wi-Fi + Cellular model A2604; cellular radio", "Wi-Fi + Cellular; LTE", key="cellular"),
        ]
    else:
        rows += [
            na("sim_esim", model_source, "Wi-Fi-only model A2602; cellular SIM/eSIM is not applicable", "Apple distinguishes A2602 Wi-Fi from A2604 Wi-Fi + Cellular."),
            na("cellular_bands", model_source, "Wi-Fi-only A2602 has no cellular radio", "Cellular bands are not applicable to this Wi-Fi configuration."),
            na("gnss", tech, "Apple lists GPS/GNSS for Wi-Fi + Cellular models only", "No GPS/GNSS feature is claimed for Wi-Fi-only A2602."),
            f("tablet_cellular_variant", tech, "Wi-Fi model A2602", "Wi-Fi only; no cellular modem", key="cellular"),
        ]
    rows += [
        f("wifi", tech, "Wi-Fi 5 (802.11ac), 2×2 MIMO", "Wi-Fi 5 (802.11ac), 2x2 MIMO", key="wifi"),
        f("bluetooth", tech, "Bluetooth 4.2", "Bluetooth 4.2"),
        f("usb", tech, "Lightning connector", "Lightning", key="ports"),
        nd("nfc", tech, "NFC is not stated in Apple's reviewed technical specification.", "NFC capability not inferred."),
        f("audio", tech, "Stereo speakers; dual microphones", "Stereo speakers; dual microphones", key="sound"),
        f("sensors", tech, "Touch ID, three-axis gyroscope, accelerometer, barometer, ambient-light sensor", "Touch ID; three-axis gyroscope; accelerometer; barometer; ambient-light sensor"),
        f("tablet_stylus", tech, "Apple Pencil (1st generation)", "Apple Pencil (1st generation)", key="stylus"),
        f("tablet_keyboard", "apple_ipad9_newsroom", "Smart Keyboard support; accessory sold separately", "Apple Smart Keyboard support; sold separately", key="keyboard"),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct field reviews, got {len(rows)}")
    return rows


def availability(v: dict) -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "YugaTech's 2021-10-10 report says iPad (2021) was available in the Philippines and could be purchased on Apple Philippines. The article lists this exact storage/connectivity price but does not identify the first-sale date. Current retailer page observation is marked closed/out of delivery range.",
        "philippineAvailability": "Dated Philippine availability is supported by a 2021-10-10 local report that linked to Apple Philippines purchase; the exact first-sale date is not recorded.",
        "observedAt": OBSERVED,
        "qualityFlag": "Exact model/configuration matching reviewed against Apple model identification and technical specifications. Philippine availability supported by a dated report. Exact first-sale date, present stock and current buyable price remain unverified. Study eligibility remains Pending.",
        "catalogModel": MODEL, "manufacturer": "Apple Inc.", "productLine": "iPad",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Dated Philippine availability report; not first-sale date",
        "researchNotes": f"The workbook's {MODEL} entry is matched to Apple's 2021 iPad (9th generation), with distinct 64GB/256GB Wi-Fi (A2602) and Wi-Fi + Cellular (A2604) configurations. YugaTech reported Philippine availability on 2021-10-10 and gave contemporaneous prices for all four. Exact first-sale date remains unknown. Pick.A.Roo currently displays a closed store/out-of-range banner; its page prices are recorded as non-orderable observations, not current buyable prices. Apple does not disclose RAM or mAh battery capacity. The exact-model Apple diagram is not reused because image rights are not established. Study scope remains Pending.",
        "openIssues": [
            {"issue": "Exact Philippine first-sale date is not documented", "action": "Keep exact date blank; retain only the dated 2021-10-10 availability report."},
            {"issue": "A2604-specific cellular band list is not distinguished on Apple's displayed spec page", "action": "Do not attribute A2603 North America bands to A2604."},
            {"issue": "RAM, RAM type, storage type, current buyable price and stock are not verified", "action": "Keep values unrecorded; preserve the closed/out-of-range retailer listing as a dated observation."},
            {"issue": "Image reuse rights are not established", "action": "Use neutral placeholder and retain official exact-family image source metadata."},
            {"issue": "Study eligibility remains Pending", "action": "Preserve workbook scope."},
        ],
    }


def make_review(v: dict, index: int) -> dict:
    record = {"deviceId": DEVICE, "configurationId": v["id"], "brand": "Apple",
              "model": MODEL, "configuration": v["label"], "configurationLabel": v["label"],
              "modelCode": v["modelCode"], "sources": sources(v), "fields": make_fields(v),
              "availabilityEvidence": availability(v)}
    # The helper resolves each incoming variant against its own replacement list.
    # Remove this list from non-primary persisted rows after all four are added.
    record["replacementVariants"] = [{"id": x["id"], "label": x["label"], "modelCode": x["modelCode"],
        "notes": "Distinct Apple storage/connectivity configuration; finish color is not split."} for x in VARIANTS]
    return record


def price_rows() -> list[dict]:
    result = []
    for v in VARIANTS:
        cell = v["connectivity"] == "wifi-cellular"
        result.append({
            "device_id": DEVICE, "amount_php": v["historical"], "configuration_id": v["id"],
            "configuration_match": f"exact_apple_ipad9_{v['storage']}gb_{'wifi_cellular' if cell else 'wifi'}_ph_2021",
            "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi + Cellular" if cell else "Wi-Fi",
            "price_type": "historical_ph_listing_price_not_confirmed_first_day_msrp",
            "source_published_at": "2021-10-10",
            "excerpt": f"YugaTech's 2021-10-10 article reporting Philippine availability gives PHP {v['historical']:,} for {v['storage']}GB {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}; first-sale-day MSRP is not specified.",
            "source_url": URL_PH, "source_kind": "dated_secondary_ph_market_availability_and_price",
            "observed_at": "2021-10-10", "local_availability_verified": True,
            "availability_status": "reported_available_in_ph_by_2021_10_10_exact_first_sale_unknown"})
        result.append({
            "device_id": DEVICE, "amount_php": v["listed"], "configuration_id": v["id"],
            "configuration_match": f"exact_apple_ipad9_{v['storage']}gb_{'wifi_cellular' if cell else 'wifi'}_pickaroo_page_listing",
            "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi + Cellular" if cell else "Wi-Fi",
            "price_type": "retailer_page_price_store_closed_delivery_unavailable_not_buyable",
            "source_published_at": None,
            "excerpt": f"Pick.A.Roo / Power Mac Center page displayed PHP {v['listed']:,} for this exact configuration with Add controls, but marks store CLOSED and outside the selected delivery range. Not a current buyable price.",
            "source_url": URL_PICKAROO, "source_kind": "philippine_retailer_listing_not_orderable_at_observation",
            "observed_at": OBSERVED, "local_availability_verified": False,
            "availability_status": "store_closed_delivery_unavailable_current_stock_not_verified"})
    return result


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the pending workbook iPad 9th Gen record; refusing unexpected scope/device.")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != UNRECORDED:
        raise ValueError("Expected exactly one unrecorded placeholder configuration; review before replacement.")

    archive = json.loads(ARCHIVE.read_text(encoding="utf-8")) if ARCHIVE.exists() else {"records": []}
    old = next((r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED), None)
    if old:
        exists = any(r.get("deviceId") == DEVICE and r.get("supersededConfigurationId") == UNRECORDED for r in archive["records"])
        if not exists:
            archive["records"].append({"deviceId": DEVICE, "model": MODEL,
                "supersededConfigurationId": UNRECORDED, "supersededAt": OBSERVED,
                "reason": "Replaced one model-level placeholder with four exact Apple storage/connectivity configurations; underlying source observations are preserved.",
                "review": old})
        manual["records"] = [r for r in manual["records"] if not (r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED)]
    ARCHIVE.write_text(json.dumps(archive, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reviews = [make_review(v, i) for i, v in enumerate(VARIANTS)]
    for review in reviews:
        add_review(manual, catalog, review)
    for v in VARIANTS[1:]:
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, v["id"]))
        saved.pop("replacementVariants", None)
        saved.pop("replaceUnrecordedPlaceholder", None)
        saved.pop("additionalVariants", None)
    target_keys = {(DEVICE, v["id"]) for v in VARIANTS}
    deduplicate_target_reviews(manual, target_keys)
    for v in VARIANTS:
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, v["id"]))
        saved.update({"model": MODEL, "configuration": v["label"], "configurationLabel": v["label"], "modelCode": v["modelCode"]})
        source_updates = {source["id"]: source for source in sources(v)}
        saved["sources"] = [source_updates.get(source["id"], source) for source in saved.get("sources", [])]
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact-family Apple Support diagram was located, but it is not a standalone product photograph and no permission or reusable license to republish or hotlink it is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_TECH, "assetUrl": None, "candidateAssetUrl": IMAGE_ASSET,
        "scope": "Official Apple Support diagram for iPad (9th generation); exact model family, not specific to one storage/connectivity configuration.",
        "rightsTermsUrl": None,
        "rightsCheck": "No reuse permission or license was found on the reviewed page. Do not download or hotlink.",
        "rightsCheckSourcePage": URL_TECH, "observedAt": OBSERVED,
        "altText": "Image unavailable for Apple iPad 9th Gen",
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
    known = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type")) for p in latest.get("prices", [])}
    for price in prices:
        key = (price["device_id"], price["configuration_id"], price["price_type"])
        if key not in known:
            latest.setdefault("prices", []).append(price)
            known.add(key)
    latest["run_at"] = OBSERVED
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "model": MODEL,
        "configurations": [{"id": v["id"], "modelNumber": v["modelCode"], "label": v["label"],
                            "historicalPhilippineListingPricePhp": v["historical"],
                            "currentBuyablePricePhp": None, "retailerPageListingPhp": v["listed"]} for v in VARIANTS],
        "reviewedConfigurations": len(reviews), "reviewedFieldsPerConfiguration": 49,
        "philippineAvailabilityEvidence": "YugaTech reported available in PH and Apple Philippines purchase link on 2021-10-10; exact first-sale date unknown",
        "retailerListing": "Power Mac Center Pick.A.Roo page marks the store CLOSED and out of delivery range; page prices are not current buyable offers",
        "image": "exact-family Apple Support diagram found; reuse rights not documented; placeholder retained",
        "eligibility": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
