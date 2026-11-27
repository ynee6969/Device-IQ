#!/usr/bin/env python3
"""Replace iPad mini 6 placeholder with exact Philippine storage/connectivity configs."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_b3800bdea59d3d"
UNRECORDED = f"{DEVICE}-unrecorded"
MODEL = "iPad mini 6"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/apple-ipad-mini-6-ph-prices-2026-11-27.json"
ARCHIVE = ROOT / "research/enrichment/superseded-model-level-reviews-2026-11-27.json"

URL_TECH = "https://support.apple.com/en-ie/111886"
URL_MODEL_IDS = "https://support.apple.com/en-us/108043"
URL_NEWS = "https://www.apple.com/newsroom/2021/09/apple-unveils-new-ipad-mini-with-breakthrough-performance-in-stunning-new-design/"
URL_PH = "https://www.yugatech.com/personal-computing/apple-ipad-2021-ipad-mini-2021-now-available-in-the-philippines/"
URL_PICKAROO = "https://pickaroo.com/power-mac-center/products/power-mac-center-sm-city-pampanga?group=682-ipad&list=True"
IMAGE_ASSET = "https://cdsassets.apple.com/live/SZLF0YNV/images/sp/111886_sp850-ipad-mini-6gen-480.png"

VARIANTS = [
    {"storage": 64, "connectivity": "wifi", "label": "64 GB / Wi-Fi", "modelCode": "A2567", "historical": 29990, "listed": 35490},
    {"storage": 256, "connectivity": "wifi", "label": "256 GB / Wi-Fi", "modelCode": "A2567", "historical": 38990, "listed": 44990},
    {"storage": 64, "connectivity": "wifi-cellular", "label": "64 GB / Wi-Fi + Cellular", "modelCode": "A2568", "historical": 38990, "listed": 44990},
    {"storage": 256, "connectivity": "wifi-cellular", "label": "256 GB / Wi-Fi + Cellular", "modelCode": "A2568", "historical": 47990, "listed": 54490},
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
           "note": note or "Exact iPad mini (6th generation) model fact checked against the cited source."}
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
        src("apple_ipad_mini6_tech_specs", URL_TECH, "Apple Support",
            "Technical specifications for iPad mini (6th generation)",
            "Apple lists 64GB and 256GB capacities, display, A15 CPU/GPU, cameras, battery energy, dimensions/weights by connectivity, A2568 cellular bands, wireless, SIM, ports, sensors and Pencil compatibility."),
        src("apple_ipad_mini6_model_identification", URL_MODEL_IDS, "Apple Support",
            "Exact model number, generation, capacity and connectivity mapping",
            "Apple identifies A2567 as iPad mini (6th generation), A2568 as Wi-Fi + Cellular and A2569 as the China-mainland-only cellular model; capacities are 64GB and 256GB."),
        src("apple_ipad_mini6_newsroom", URL_NEWS, "Apple Newsroom",
            "Announcement, initial-market availability, original OS and product overview",
            "Apple announced the iPad mini on 2021-09-14 and said store availability in initial markets begins 2021-09-24. The launch release names A15 Bionic, 5G, Pencil 2, iPadOS 15 and product features.",
            "2021-09-14"),
        src("yugatech_ipad_mini6_ph", URL_PH, "YugaTech",
            "Dated Philippine availability and configuration prices",
            "Article dated 2021-10-10 says the 2021 iPad mini was available in the Philippines, lists 64GB/256GB Wi-Fi and cellular configurations, says it could be purchased on Apple Philippines, and gives four prices. It does not state the first-sale date.",
            "2021-10-10"),
        src("pickaroo_pmc_ipad_mini6_listing", URL_PICKAROO, "Pick.A.Roo / Power Mac Center - SM City Pampanga",
            "Exact configuration retailer-listing price cross-check; not used as buyable current price",
            "The page displays exact iPad mini 6 variants and prices with Add controls but marks the store CLOSED and out of delivery range. Current stock/orderability is not verified; values are retained only as page-listed observations."),
    ]


def make_fields(v: dict) -> list[dict]:
    cell = v["connectivity"] == "wifi-cellular"
    model_source = "apple_ipad_mini6_model_identification"
    tech = "apple_ipad_mini6_tech_specs"
    local = "yugatech_ipad_mini6_ph"
    cfg = f("configuration", tech,
            f"{v['storage']}GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}; model {v['modelCode']}",
            f"{v['storage']} GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'} / {v['modelCode']}",
            note="Apple identifies 64GB and 256GB capacities and separates Wi-Fi model A2567 from Wi-Fi + Cellular A2568. Colors do not change the technical configuration.")
    rows = [
        f("model_number", model_source, v["modelCode"], v["modelCode"], note="Apple maps A2567 to Wi-Fi, A2568 to Wi-Fi + Cellular and A2569 to the separate China-mainland cellular model."),
        f("global_release_date", "apple_ipad_mini6_newsroom", "Announced 2021-09-14; store availability in initial markets from 2021-09-24", "2021-09-24", note="Apple's newsroom gives the announcement date and store availability in initial markets. This is not the Philippine availability date."),
        cfg,
        pending("philippine_release_date", local, "YugaTech reported on 2021-10-10 that iPad mini (2021) was available in the Philippines; the report does not give the first-sale date.", "Keep the exact Philippine first-sale date blank; the source supports availability by 2021-10-10, not the date sales first began."),
        f("official_launch_price_php", local,
          f"PHP {v['historical']:,} ({v['storage']}GB, {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}) in YugaTech's 2021-10-10 PH availability article",
          v["historical"], status="VERIFIED_SECONDARY", unit="PHP",
          note="Contemporaneous Philippine report dated 2021-10-10 lists this exact storage/connectivity price and says it could be purchased from Apple Philippines. It does not explicitly call this the first-day MSRP."),
        pending("current_price_php", "pickaroo_pmc_ipad_mini6_listing",
                f"A Power Mac Center listing displayed PHP {v['listed']:,} for {v['label']} on the reviewed page.",
                "The page marks its store CLOSED and says delivery is unavailable for the selected location. Retain as a dated retailer page observation only; not a currently buyable price and not included in numeric price filtering.", "PHP"),
        f("display_size", tech, "8.3-inch diagonal", 8.3, key="displayInches", unit="in"),
        f("display_technology", tech, "Liquid Retina LED-backlit Multi-Touch IPS display", "Liquid Retina LED-backlit Multi-Touch IPS LCD", key="displayType"),
        f("display_resolution", tech, "2266-by-1488 pixels", "2266 x 1488", key="resolution"),
        nd("display_refresh_rate", tech, "Apple does not state a display refresh rate in the reviewed specifications.", "Refresh rate remains unrecorded.", "Hz"),
        f("display_brightness", tech, "500 nits", "500 nits", unit="nits"),
        f("display_protection", tech, "Fingerprint-resistant oleophobic coating, full lamination and anti-reflective coating", "Fully laminated; anti-reflective; fingerprint-resistant oleophobic coating"),
        f("chipset", tech, "A15 Bionic chip", "Apple A15 Bionic", key="chipset"),
        nd("process_node", tech, "Apple's reviewed iPad mini technical specification does not state the semiconductor process node.", "No process node inferred.", "nm"),
        f("cpu", tech, "6-core CPU with 2 performance cores and 4 efficiency cores", "6-core CPU (2 performance + 4 efficiency)", key="cpu"),
        f("gpu", tech, "5-core GPU", "5-core Apple GPU", key="gpu"),
        f("operating_system", "apple_ipad_mini6_newsroom", "Ships with iPadOS 15; Apple Support describes the platform as iPadOS", "iPadOS", key="os", note="iPadOS is the platform; iPadOS 15 was the original launch version. No current OS version is asserted."),
        nd("os_support", tech, "Apple does not publish a guaranteed iPadOS support end date on the reviewed specification page.", "End-of-support date not inferred."),
        nd("ram_capacity", tech, "Apple does not state RAM capacity in the reviewed technical specifications.", "RAM remains unrecorded; no third-party estimate substituted.", "GB"),
        nd("ram_type", tech, "Apple does not state RAM type in the reviewed technical specifications.", "Memory type remains unrecorded."),
        f("storage_capacity", tech, f"{v['storage']}GB", v["storage"], key="storageGb", unit="GB"),
        nd("storage_type", tech, "Apple does not state a flash-storage interface/type in the reviewed specification.", "Storage type not inferred."),
        f("storage_expansion", tech, "USB-C supports external storage accessories; internal capacity is 64GB or 256GB", "USB-C external storage accessories supported", note="Apple's 2021 release describes connecting external storage accessories over USB-C. This does not change the built-in storage capacity."),
        f("rear_camera_system", tech, "12MP Wide camera, ƒ/1.8; Quad-LED True Tone flash", "12 MP Wide rear camera; f/1.8; Quad-LED True Tone flash", key="rearCameraMp"),
        nd("main_camera_sensor", tech, "Apple does not identify the rear sensor manufacturer or sensor model.", "Sensor make/model not disclosed."),
        na("ultrawide_camera", tech, "No rear Ultra Wide camera is listed; the rear camera is a single 12MP Wide camera.", "The Ultra Wide camera is front-facing."),
        na("telephoto_camera", tech, "No telephoto rear camera is listed.", "Apple specifies a single Wide rear camera."),
        f("front_camera", tech, "12MP Ultra Wide camera, 122-degree field of view, ƒ/2.4", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", tech, "Rear: 4K at 24/25/30/60fps; front: 1080p at 25/30/60fps; rear slow motion 1080p at 120/240fps", "Rear 4K/60fps; front 1080p/60fps; slow motion 1080p/240fps", key="video"),
        f("battery_capacity", tech, "Built-in 19.3Wh rechargeable lithium-polymer battery; mAh not stated", 19.3, key="batteryWh", unit="Wh", note="Apple states battery energy in watt-hours, not mAh. No conversion is made without a published nominal voltage."),
        f("battery_technology", tech, "Rechargeable lithium-polymer battery", "Lithium-polymer"),
        nd("wired_charging", tech, "USB-C charging is listed; 20W USB-C adapter is included, but maximum device input wattage is not stated.", "Included adapter wattage is not used as a tablet charging-rate claim.", "W"),
        nd("wireless_charging", tech, "Wireless/reverse charging of the tablet is not specified on Apple's technical specification.", "No charging capability inferred from omission."),
        f("dimensions", tech, "195.4 × 134.8 × 6.3 mm", "195.4 x 134.8 x 6.3 mm", key="dimensions", unit="mm"),
        f("weight", tech, "Wi-Fi: 293g; Wi-Fi + Cellular: 297g", 297 if cell else 293, key="weightG", unit="g"),
        f("materials", "apple_ipad_mini6_newsroom", "100% recycled aluminum enclosure", "Aluminum enclosure", note="Apple's announcement identifies an aluminum enclosure; recycled content describes material sourcing, not a different chassis material."),
        nd("ingress_protection", tech, "Apple's reviewed specifications do not state an IP water/dust rating.", "No IP rating inferred."),
    ]
    if cell:
        rows += [
            f("sim_esim", tech, "Wi-Fi + Cellular model A2568 lists Nano-SIM and eSIM", "Nano-SIM and eSIM", key="sim"),
            f("cellular_bands", tech, "A2568 5G NR: n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n71/n77/n78/n79; FDD-LTE: 1/2/3/4/5/7/8/11/12/13/14/17/18/19/20/21/25/26/28/29/30/32/66/71; TD-LTE: 34/38/39/40/41/42/46/48; UMTS 850/900/1700-2100/1900/2100 MHz", "A2568 5G NR and LTE bands per Apple", note="Apple lists these bands for A2568. Carrier frequency support and network availability depend on the local carrier and market."),
            f("gnss", tech, "GPS/GNSS on Wi-Fi + Cellular models", "GPS/GNSS"),
            f("tablet_cellular_variant", tech, "Wi-Fi + Cellular model A2568 with 5G/LTE radios", "Wi-Fi + Cellular; 5G/LTE", key="cellular"),
        ]
    else:
        rows += [
            na("sim_esim", model_source, "Wi-Fi-only model A2567; cellular SIM/eSIM is not applicable", "Apple identifies A2567 Wi-Fi and A2568 Wi-Fi + Cellular as separate models."),
            na("cellular_bands", model_source, "Wi-Fi-only A2567 has no cellular radio", "Cellular bands are not applicable to this Wi-Fi configuration."),
            na("gnss", tech, "Apple lists GPS/GNSS only for Wi-Fi + Cellular models", "No GPS/GNSS feature is claimed for Wi-Fi-only A2567."),
            f("tablet_cellular_variant", tech, "Wi-Fi model A2567", "Wi-Fi only; no cellular modem", key="cellular"),
        ]
    rows += [
        f("wifi", tech, "Wi-Fi 6 (802.11ax), 2×2 MIMO", "Wi-Fi 6 (802.11ax), 2x2 MIMO", key="wifi"),
        f("bluetooth", tech, "Bluetooth 5.0", "Bluetooth 5.0"),
        f("usb", tech, "USB-C; USB 3.1 Gen 1 up to 5Gb/s; DisplayPort", "USB-C; USB 3.1 Gen 1 up to 5Gb/s; DisplayPort", key="ports"),
        nd("nfc", tech, "NFC is not listed in Apple's reviewed technical specification.", "NFC not inferred."),
        f("audio", tech, "Landscape stereo speakers; dual microphones", "Landscape stereo speakers; dual microphones", key="sound"),
        f("sensors", tech, "Touch ID, three-axis gyro, accelerometer, barometer and ambient light sensor", "Touch ID; three-axis gyro; accelerometer; barometer; ambient-light sensor"),
        f("tablet_stylus", tech, "Apple Pencil (2nd generation) and Apple Pencil (USB-C) supported", "Apple Pencil (2nd generation); Apple Pencil (USB-C)", key="stylus"),
        nd("tablet_keyboard", "apple_ipad_mini6_newsroom", "Apple's launch materials list Apple Pencil and Smart Folio accessories; no keyboard accessory is specified.", "No physical keyboard compatibility claim inferred from the accessory list."),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct field reviews, got {len(rows)}")
    return rows


def availability(v: dict) -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "YugaTech's 2021-10-10 report says the 2021 iPad mini was available in the Philippines and could be purchased on Apple Philippines. It lists this exact configuration's contemporaneous price but does not state the first-sale date. The reviewed PMC page is marked closed/out of delivery range.",
        "philippineAvailability": "Dated Philippine availability is supported by a 2021-10-10 local report that linked to the Apple Philippines purchase page; exact first-sale date is not recorded.",
        "observedAt": OBSERVED,
        "qualityFlag": "Exact model/configuration matching reviewed against Apple model identification and technical specifications. Philippine availability supported by a dated report. Exact first-sale date, present stock and current buyable price remain unverified. Study eligibility remains Pending.",
        "catalogModel": MODEL, "manufacturer": "Apple Inc.", "productLine": "iPad mini",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Dated Philippine availability report; not first-sale date",
        "researchNotes": f"The workbook's {MODEL} entry is matched to Apple's 2021 iPad mini (6th generation), with 64GB/256GB Wi-Fi (A2567) and Wi-Fi + Cellular (A2568) configurations. YugaTech reported availability in the Philippines on 2021-10-10 and listed all four prices, but no exact first-sale date. Pick.A.Roo displays a closed-store/out-of-range notice, so page prices are retained as non-orderable observations, not current offers. Apple does not disclose RAM or battery mAh. The official exact-family diagram is not reused because image rights are not established. Study scope remains Pending.",
        "openIssues": [
            {"issue": "Exact Philippine first-sale date is not documented", "action": "Keep the exact date blank; preserve the 2021-10-10 dated availability report."},
            {"issue": "RAM capacity/type, storage interface and current buyable stock/price remain unverified", "action": "Keep unrecorded; use only the contemporaneous historical price evidence."},
            {"issue": "Image reuse rights are not established", "action": "Keep neutral placeholder and retain the official exact-family image source for rights review."},
            {"issue": "Study eligibility remains Pending", "action": "Preserve workbook study scope."},
        ],
    }


def make_review(v: dict) -> dict:
    record = {"deviceId": DEVICE, "configurationId": v["id"], "brand": "Apple",
              "model": MODEL, "configuration": v["label"], "configurationLabel": v["label"],
              "modelCode": v["modelCode"], "sources": sources(v), "fields": make_fields(v),
              "availabilityEvidence": availability(v)}
    record["replacementVariants"] = [{"id": x["id"], "label": x["label"], "modelCode": x["modelCode"],
        "notes": "Distinct Apple storage/connectivity configuration; finish colors are not split."} for x in VARIANTS]
    return record


def price_rows() -> list[dict]:
    result = []
    for v in VARIANTS:
        cell = v["connectivity"] == "wifi-cellular"
        result.append({
            "device_id": DEVICE, "amount_php": v["historical"], "configuration_id": v["id"],
            "configuration_match": f"exact_apple_ipad_mini6_{v['storage']}gb_{'wifi_cellular' if cell else 'wifi'}_ph_2021",
            "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi + Cellular" if cell else "Wi-Fi",
            "price_type": "historical_ph_listing_price_not_confirmed_first_day_msrp",
            "source_published_at": "2021-10-10",
            "excerpt": f"YugaTech's 2021-10-10 article reporting Philippine availability lists PHP {v['historical']:,} for {v['storage']}GB {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}; exact first-sale-day MSRP is not specified.",
            "source_url": URL_PH, "source_kind": "dated_secondary_ph_market_availability_and_price",
            "observed_at": "2021-10-10", "local_availability_verified": True,
            "availability_status": "reported_available_in_ph_by_2021_10_10_exact_first_sale_unknown"})
        result.append({
            "device_id": DEVICE, "amount_php": v["listed"], "configuration_id": v["id"],
            "configuration_match": f"exact_apple_ipad_mini6_{v['storage']}gb_{'wifi_cellular' if cell else 'wifi'}_pickaroo_page_listing",
            "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi + Cellular" if cell else "Wi-Fi",
            "price_type": "retailer_page_price_store_closed_delivery_unavailable_not_buyable",
            "source_published_at": None,
            "excerpt": f"Pick.A.Roo / Power Mac Center page displays PHP {v['listed']:,} for this exact configuration with Add controls, but marks the store CLOSED and outside the selected delivery range. Not a current buyable price.",
            "source_url": URL_PICKAROO, "source_kind": "philippine_retailer_listing_not_orderable_at_observation",
            "observed_at": OBSERVED, "local_availability_verified": False,
            "availability_status": "store_closed_delivery_unavailable_current_stock_not_verified"})
    return result


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the pending workbook iPad mini 6 record; refusing unexpected scope/device.")
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

    reviews = [make_review(v) for v in VARIANTS]
    for review in reviews:
        add_review(manual, catalog, review)
    for v in VARIANTS:
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, v["id"]))
        if v["id"] != VARIANTS[0]["id"]:
            saved.pop("replacementVariants", None)
            saved.pop("replaceUnrecordedPlaceholder", None)
            saved.pop("additionalVariants", None)
        saved.update({"model": MODEL, "configuration": v["label"], "configurationLabel": v["label"], "modelCode": v["modelCode"]})
        source_updates = {source["id"]: source for source in sources(v)}
        saved["sources"] = [source_updates.get(source["id"], source) for source in saved.get("sources", [])]
    target_keys = {(DEVICE, v["id"]) for v in VARIANTS}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact-family Apple Support diagram was found, but it is not a product photograph and no permission or reusable license to republish or hotlink it is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_TECH, "assetUrl": None, "candidateAssetUrl": IMAGE_ASSET,
        "scope": "Official Apple Support diagram for iPad mini (6th generation); exact family, not specific to storage/connectivity configuration.",
        "rightsTermsUrl": None,
        "rightsCheck": "No reuse permission or license was found on the reviewed page. Do not download or hotlink.",
        "rightsCheckSourcePage": URL_TECH, "observedAt": OBSERVED,
        "altText": "Image unavailable for Apple iPad mini 6",
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
