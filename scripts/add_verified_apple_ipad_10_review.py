#!/usr/bin/env python3
"""Replace the iPad 10th Gen placeholder with exact PH storage/connectivity configs."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_e4a50bfd310ec0"
UNRECORDED = f"{DEVICE}-unrecorded"
MODEL = "iPad 10th Gen"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/apple-ipad-10-ph-prices-2026-11-27.json"
ARCHIVE = ROOT / "research/enrichment/superseded-model-level-reviews-2026-11-27.json"

URL_TECH = "https://support.apple.com/en-us/111840"
URL_MODEL_IDS = "https://support.apple.com/en-us/108043"
URL_NEWS = "https://www.apple.com/newsroom/2022/10/apple-unveils-completely-redesigned-ipad-in-four-vibrant-colors/"
URL_PH_PRICE = "https://www.yugatech.com/personal-computing/tablet-prices-in-the-philippines-2022/"
URL_IWAREHOUSE = "https://iwarehouse.ph/products/50-apple-ipad-10th-gen-wifi"
URL_GREENTELCOM = "https://www.greentelcom.ph/shop/tablets/apple-ipad-10th-gen-wifi-cellular-64gb/"
URL_DATABLITZ = "https://ecommerce.datablitz.com.ph/collections/ipad-10th-gen-wifi"
IMAGE_ASSET = "https://cdsassets.apple.com/live/SZLF0YNV/images/sp/111840_sp884-ipad-10gen-960.png"

VARIANTS = [
    {"storage": 64, "connectivity": "wifi", "label": "64 GB / Wi-Fi", "modelCode": "A2696", "launch": 29990, "current": 25490},
    {"storage": 256, "connectivity": "wifi", "label": "256 GB / Wi-Fi", "modelCode": "A2696", "launch": 39990, "current": None},
    {"storage": 64, "connectivity": "wifi-cellular", "label": "64 GB / Wi-Fi + Cellular", "modelCode": "A2757", "launch": 39990, "current": 34990},
    {"storage": 256, "connectivity": "wifi-cellular", "label": "256 GB / Wi-Fi + Cellular", "modelCode": "A2757", "launch": 49990, "current": None},
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
           "note": note or "Exact iPad (10th generation) model fact checked against the cited source."}
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
    rows = [
        src("apple_ipad10_tech_specs", URL_TECH, "Apple Support",
            "Exact model technical specifications and storage/cellular differences",
            "Apple lists 64GB and 256GB, A14 Bionic, display, cameras, battery energy, dimensions, weights by connectivity, wireless, ports, sensors and accessories."),
        src("apple_ipad10_model_identification", URL_MODEL_IDS, "Apple Support",
            "Exact model-number and connectivity mapping",
            "Apple identifies A2696 as iPad (10th generation) and A2757 as the Wi-Fi + Cellular configuration; capacities are 64GB and 256GB.",
            "2026-03-01"),
        src("apple_ipad10_newsroom", URL_NEWS, "Apple Newsroom",
            "Announcement, global availability schedule, product features and original OS",
            "Apple announced the model on 2022-10-18, said store availability in initial markets begins 2022-10-26, and lists the 64GB/256GB capacities, A14, cameras, Wi-Fi 6, cellular 5G and iPadOS 16 at launch.",
            "2022-10-18"),
        src("yugatech_ipad10_ph_prices", URL_PH_PRICE, "YugaTech",
            "Dated Philippine market-listing evidence and 2022 local list prices",
            "The 2022 Philippines tablet price list, published 2022-11-21, states its listed products were officially launched in the Philippines during 2022 and gives all four exact iPad 10th Gen storage/connectivity prices. It does not give an exact first-sale date.",
            "2022-11-21"),
        src("iwarehouse_ipad10_wifi64_price", URL_IWAREHOUSE, "iWarehouse Philippines",
            "Dated current local retailer listing for exact 64GB Wi-Fi configuration",
            "Product page identifies brand-new iPad 10th Gen, Silver, 64GB, Wi-Fi; cash price PHP 25,490, SRP PHP 29,990, with availability shown at one Cadiz City location. Stock is informational and should be confirmed with the store."),
        src("greentelcom_ipad10_cell64_price", URL_GREENTELCOM, "GreenTelcom Philippines",
            "Dated local retailer listing for exact 64GB Wi-Fi + Cellular configuration",
            "Product page identifies the exact 64GB Wi-Fi + Cellular model and shows PHP 34,990 against PHP 35,990 with Add to cart/Buy Now controls. The page also reports zero sold and does not explicitly confirm stock; price is a retailer listing, not an in-stock guarantee."),
        src("datablitz_ipad10_wifi_price", URL_DATABLITZ, "DataBlitz Philippines",
            "Cross-check of Wi-Fi model prices and stock labels",
            "The page lists 64GB Wi-Fi at PHP 19,950 and 256GB Wi-Fi at PHP 30,450, but both configurations are labeled Sold out. These are retained as sold-out observations and not treated as current buyable prices."),
    ]
    return rows


def make_fields(v: dict) -> list[dict]:
    cell = v["connectivity"] == "wifi-cellular"
    model_source = "apple_ipad10_model_identification"
    tech = "apple_ipad10_tech_specs"
    local = "yugatech_ipad10_ph_prices"
    current_source = ("iwarehouse_ipad10_wifi64_price" if v["storage"] == 64 and not cell
                      else "greentelcom_ipad10_cell64_price" if v["storage"] == 64 and cell
                      else "datablitz_ipad10_wifi_price" if not cell else local)
    cfg = f("configuration", tech,
            f"{v['storage']}GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}; model {v['modelCode']}",
            f"{v['storage']} GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'} / {v['modelCode']}",
            note="Storage capacity and connectivity are separate Apple-listed configurations; Apple model identifiers distinguish A2696 Wi-Fi from A2757 Wi-Fi + Cellular. Color is not split because it does not change the configuration." )
    rows = [
        f("model_number", model_source, v["modelCode"], v["modelCode"], note="Apple maps model A2696 to iPad 10th generation Wi-Fi and A2757 to Wi-Fi + Cellular; China-only model numbers are not assigned to these Philippine configurations."),
        f("global_release_date", "apple_ipad10_newsroom", "Announced 2022-10-18; stores in initial markets from 2022-10-26", "2022-10-26", note="Apple's newsroom announcement says the product was announced October 18 and store availability begins October 26 in its initial launch markets. This is not the Philippine first-sale date."),
        cfg,
        pending("philippine_release_date", local, "YugaTech lists this iPad among tablets officially launched in the Philippines during 2022, but provides no exact first-sale date.", "Keep the exact Philippine release/first-sale date blank; the source verifies only the local launch year."),
        f("official_launch_price_php", local,
          f"PHP {v['launch']:,} ({v['storage']}GB, {'Cell.' if cell else 'WiFi'}) in the 2022 Philippines tablet price list",
          v["launch"], status="VERIFIED_SECONDARY", unit="PHP",
          note="Secondary Philippine market report published 2022-11-21. The article says its list contains tablets officially launched in the Philippines during 2022, but it does not date this price to the exact launch day."),
    ]
    if v["current"] is not None:
        if not cell:
            current_note = "iWarehouse showed a brand-new 64GB Wi-Fi unit at PHP 25,490 cash price and one store location on 2026-11-27. Store page says availability is informational; confirm stock before travel. This is one retailer offer, not a nationwide price."
            current_type = "Dated Philippine retailer cash listing; one location shown, confirm stock"
        else:
            current_note = "GreenTelcom displayed PHP 34,990 (reduced from PHP 35,990) on 2026-11-27. Product page has purchase controls but reports zero sold and does not explicitly confirm stock; treat as a retailer asking price only."
            current_type = "Dated Philippine retailer promotional listing; stock unconfirmed"
        rows.append(f("current_price_php", current_source,
                       f"PHP {v['current']:,} listed for exact {v['label']}", v["current"],
                       status="VERIFIED_SECONDARY", unit="PHP", note=current_note,
                       price_condition="new", price_type=current_type, price_observed=OBSERVED))
    else:
        note = ("DataBlitz showed PHP 30,450 for 256GB Wi-Fi on 2026-11-27 but labeled it Sold out; retain only as a dated sold-out listing, not a current buyable price. No in-stock current offer verified."
                if not cell else "No exact 256GB Wi-Fi + Cellular Philippine retailer price with confirmed current stock was verified. Power Mac Center's legacy price table has expired 2024 installment terms and its linked product pages return 404, so it is not used as a current price. Keep current price blank.")
        rows.append(pending("current_price_php", current_source,
                            "No current buyable listing price verified for this exact configuration.", note, "PHP"))
    rows += [
        f("display_size", tech, "10.86-inch measured as a rectangle; 10.9-inch marketed class", 10.86, key="displayInches", unit="in", note="Apple specifies a 10.86-inch diagonal when measured as a rectangle; its product announcement markets the panel as 10.9-inch. The stored value follows Apple's measured size."),
        f("display_technology", tech, "LED-backlit Multi-Touch display with IPS technology", "LED-backlit Multi-Touch IPS LCD", key="displayType"),
        f("display_resolution", tech, "2360-by-1640 pixels", "2360 x 1640", key="resolution"),
        nd("display_refresh_rate", tech, "No display refresh rate is stated in Apple's technical specifications.", "Not disclosed by Apple; no refresh rate inferred.", "Hz"),
        f("display_brightness", tech, "500 nits", "500 nits", unit="nits"),
        f("display_protection", tech, "Fingerprint-resistant oleophobic coating", "Fingerprint-resistant oleophobic coating"),
        f("chipset", tech, "A14 Bionic chip", "Apple A14 Bionic", key="chipset"),
        nd("process_node", tech, "Apple's reviewed iPad technical specifications do not publish the semiconductor process node.", "No process-node value inferred.", "nm"),
        f("cpu", tech, "6-core CPU", "6-core CPU", key="cpu"),
        f("gpu", tech, "4-core graphics", "4-core Apple GPU", key="gpu"),
        f("operating_system", "apple_ipad10_newsroom", "Ships with iPadOS 16; Apple Support describes the platform as iPadOS", "iPadOS", key="os", note="iPadOS is the platform. iPadOS 16 is the original launch version; a current software version is not asserted."),
        nd("os_support", tech, "Apple does not publish a guaranteed end date for iPadOS support on this specification page.", "Do not infer an end-of-support date."),
        nd("ram_capacity", tech, "Apple does not state RAM capacity in the reviewed technical specifications.", "Keep RAM unrecorded; no third-party estimate substituted.", "GB"),
        nd("ram_type", tech, "Apple does not state RAM type in the reviewed technical specifications.", "Keep memory type unrecorded."),
        f("storage_capacity", tech, f"{v['storage']}GB", v["storage"], key="storageGb", unit="GB"),
        nd("storage_type", tech, "Apple does not state a flash-storage interface or type in the reviewed specifications.", "Storage interface not inferred."),
        nd("storage_expansion", tech, "Apple does not document a removable storage expansion option in the reviewed specification.", "Expansion support is not inferred from an omission."),
        f("rear_camera_system", tech, "12MP Wide camera, ƒ/1.8", "12 MP Wide rear camera; f/1.8", key="rearCameraMp"),
        nd("main_camera_sensor", tech, "Apple does not identify the rear sensor manufacturer or sensor model.", "Sensor make/model not disclosed."),
        na("ultrawide_camera", tech, "No rear Ultra Wide camera is listed; the rear camera is a single 12MP Wide camera.", "Apple lists only the Wide rear camera; the front Ultra Wide camera is separately recorded."),
        na("telephoto_camera", tech, "No telephoto rear camera is listed for this model.", "Apple lists a single Wide rear camera."),
        f("front_camera", tech, "Landscape 12MP Center Stage camera, ƒ/2.4", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", tech, "Rear: 4K at 24/25/30/60 fps; front: 1080p at 25/30/60 fps; rear slow motion up to 1080p at 240 fps", "Rear 4K/60fps; front 1080p/60fps; slow motion up to 1080p/240fps", key="video"),
        f("battery_capacity", tech, "Built-in 28.6Wh rechargeable lithium-polymer battery; mAh not specified by Apple", 28.6, key="batteryWh", unit="Wh", note="Apple reports energy in watt-hours and does not publish mAh on the reviewed page. No mAh conversion is made without a published nominal voltage."),
        f("battery_technology", tech, "Rechargeable lithium-polymer battery", "Lithium-polymer"),
        nd("wired_charging", tech, "Apple lists USB-C charging and includes a 20W USB-C adapter but does not state the tablet's maximum input wattage.", "Adapter wattage is not used as a device charging-rate claim.", "W"),
        nd("wireless_charging", tech, "Apple's technical specification lists USB-C charging and does not disclose wireless or reverse charging.", "No charging capability inferred from an omission."),
        f("dimensions", tech, "248.6 × 179.5 × 7.0 mm", "248.6 x 179.5 x 7.0 mm", key="dimensions", unit="mm"),
        f("weight", tech, "Wi-Fi: 477g; Wi-Fi + Cellular: 481g", 481 if cell else 477, key="weightG", unit="g"),
        f("materials", "iwarehouse_ipad10_wifi64_price", "Glass front, aluminum back", "Glass front; aluminum back", status="VERIFIED_SECONDARY", note="Exact model material description from an iWarehouse product page; Apple technical page does not specify chassis materials."),
        nd("ingress_protection", tech, "No IP water/dust rating is stated in Apple's reviewed iPad 10th Gen specifications.", "Do not infer an IP rating."),
    ]
    if cell:
        rows += [
            f("sim_esim", tech, "Wi-Fi + Cellular model A2757: Nano-SIM and eSIM", "Nano-SIM and eSIM", key="sim"),
            f("cellular_bands", tech, "A2757 5G NR: n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n71/n77/n78/n79; FDD-LTE: 1/2/3/4/5/7/8/11/12/13/14/17/18/19/20/21/25/26/28/29/30/32/66/71; TD-LTE: 34/38/39/40/41/42/46/48", "5G NR and LTE bands per Apple model A2757", note="Apple lists bands for A2757. Carrier deployment, feature availability and local network support depend on carrier and region."),
            f("gnss", tech, "GPS/GNSS on Wi-Fi + Cellular models", "GPS/GNSS"),
            f("tablet_cellular_variant", tech, "Wi-Fi + Cellular model A2757 with 5G/LTE radios", "Wi-Fi + Cellular; 5G/LTE", key="cellular"),
        ]
    else:
        rows += [
            na("sim_esim", model_source, "Wi-Fi-only model A2696; cellular SIM/eSIM is not applicable", "Apple identifies A2696 as Wi-Fi and A2757 as the separate cellular model."),
            na("cellular_bands", model_source, "Wi-Fi-only A2696 has no cellular radio", "5G/LTE bands are listed only for the separate cellular model."),
            na("gnss", tech, "GPS/GNSS is listed for Wi-Fi + Cellular models; not applicable to this Wi-Fi-only configuration", "Apple lists GPS/GNSS under Wi-Fi + Cellular models only."),
            f("tablet_cellular_variant", tech, "Wi-Fi model A2696", "Wi-Fi only; no cellular modem", key="cellular"),
        ]
    rows += [
        f("wifi", tech, "Wi-Fi 6 (802.11ax), 2×2 MIMO, simultaneous dual band", "Wi-Fi 6 (802.11ax), 2x2 MIMO", key="wifi"),
        f("bluetooth", tech, "Bluetooth 5.2", "Bluetooth 5.2"),
        f("usb", tech, "USB-C; USB 2.0 up to 480 Mb/s; DisplayPort output", "USB-C; USB 2.0 up to 480 Mb/s; DisplayPort", key="ports"),
        nd("nfc", tech, "NFC is not listed in the reviewed Apple specification.", "NFC support not inferred."),
        f("audio", tech, "Landscape stereo speakers; dual microphones", "Landscape stereo speakers; dual microphones", key="sound"),
        f("sensors", tech, "Touch ID, three-axis gyroscope, accelerometer, barometer and ambient-light sensor", "Touch ID; three-axis gyroscope; accelerometer; barometer; ambient-light sensor"),
        f("tablet_stylus", tech, "Apple Pencil (USB-C) and Apple Pencil (1st generation; USB-C adapter required)", "Apple Pencil (USB-C); Apple Pencil (1st generation, adapter required)", key="stylus"),
        f("tablet_keyboard", "apple_ipad10_newsroom", "Magic Keyboard Folio support; sold separately", "Apple Magic Keyboard Folio support; sold separately", key="keyboard"),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct field reviews, got {len(rows)}")
    return rows


def availability(v: dict) -> dict:
    price_note = (f"A single iWarehouse location listed the new {v['label']} at PHP {v['current']:,} on {OBSERVED}; confirm stock." if v["current"] and v["connectivity"] == "wifi"
                  else f"GreenTelcom listed {v['label']} at PHP {v['current']:,} on {OBSERVED}, but did not confirm stock." if v["current"]
                  else "No buyable exact-configuration price was verified for this variant on the observation date.")
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "YugaTech's Philippines tablet price list dated 2022-11-21 states that the listed tablets were officially launched in the Philippines during 2022 and lists all four iPad 10th Gen configurations. It does not identify the first-sale date. " + price_note,
        "philippineAvailability": "Secondary local market evidence places this exact iPad family and storage/connectivity configurations in the Philippine market by 2022-11-21. Exact first-sale date is not documented.",
        "observedAt": OBSERVED,
        "qualityFlag": "Exact model/configuration matching reviewed; local launch year supported by a dated secondary market list; exact Philippine first-sale date not verified. Current retailer listing and stock limits are stated per configuration. Study eligibility remains Pending.",
        "catalogModel": MODEL, "manufacturer": "Apple Inc.", "productLine": "iPad",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Reported Philippine launch year; exact first-sale date not recorded",
        "researchNotes": f"The workbook's {MODEL} entry is matched to Apple's 2022 iPad (10th generation), with separate 64GB/256GB Wi-Fi (A2696) and Wi-Fi + Cellular (A2757) configurations. YugaTech's 2022 PH tablet list reports the four local prices and says listed models were officially launched in the Philippines in 2022, but no exact local release date was found. Current price evidence: {price_note} Apple does not disclose RAM or mAh battery capacity. Image reuse rights are not established; neutral placeholder retained. Study scope remains Pending.",
        "openIssues": [
            {"issue": "Exact Philippine first-sale date is not documented", "action": "Keep date blank; preserve only the reported 2022 local launch year."},
            {"issue": "RAM capacity/type and storage type are not disclosed by Apple", "action": "Keep unrecorded; do not substitute third-party estimates."},
            {"issue": "Current retail prices and stock vary by exact configuration", "action": "Show only dated retailer listings with their observed stock limitations; do not generalize one variant price."},
            {"issue": "Image reuse rights are not established", "action": "Keep neutral placeholder; preserve exact-model official image source for later rights review."},
            {"issue": "Study eligibility remains Pending", "action": "Preserve workbook study scope."},
        ],
    }


def make_review(v: dict, index: int) -> dict:
    record = {"deviceId": DEVICE, "configurationId": v["id"], "brand": "Apple",
              "model": MODEL, "configuration": v["label"], "configurationLabel": v["label"],
              "modelCode": v["modelCode"], "sources": sources(v), "fields": make_fields(v),
              "availabilityEvidence": availability(v)}
    variant = {"id": v["id"], "label": v["label"], "modelCode": v["modelCode"],
               "notes": "Distinct Apple capacity/connectivity configuration. Colors are not split because they do not change the recorded configuration."}
    if index == 0:
        record["replacementVariants"] = [{"id": x["id"], "label": x["label"], "modelCode": x["modelCode"],
            "notes": "Distinct Apple capacity/connectivity configuration; color is not split."} for x in VARIANTS]
        record["replaceUnrecordedPlaceholder"] = True
    else:
        record["replacementVariants"] = [variant]
    return record


def price_rows() -> list[dict]:
    result = []
    for v in VARIANTS:
        cell = v["connectivity"] == "wifi-cellular"
        result.append({
            "device_id": DEVICE, "amount_php": v["launch"], "configuration_id": v["id"],
            "configuration_match": f"exact_apple_ipad10_{v['storage']}gb_{'wifi_cellular' if cell else 'wifi'}_ph_2022",
            "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi + Cellular" if cell else "Wi-Fi",
            "price_type": "historical_reported_ph_2022_list_price",
            "source_published_at": "2022-11-21",
            "excerpt": f"YugaTech's Philippines 2022 tablet price list gives PHP {v['launch']:,} for the {v['storage']}GB {'Cell.' if cell else 'WiFi'} option; article says listed devices were officially launched in PH during 2022 but does not give a first-sale day.",
            "source_url": URL_PH_PRICE, "source_kind": "secondary_ph_market_price_list",
            "observed_at": "2022-11-21", "local_availability_verified": True,
            "availability_status": "ph_market_list_reports_official_local_launch_in_2022_exact_day_unknown"})
        if v["current"]:
            cell_source = "GreenTelcom Philippines" if cell else "iWarehouse Philippines"
            cell_url = URL_GREENTELCOM if cell else URL_IWAREHOUSE
            if cell:
                excerpt = "PHP 34,990 promotional listing (was PHP 35,990); product page has purchase controls, reports zero sold, and does not explicitly confirm stock."
                status = "listed_stock_unconfirmed"
            else:
                excerpt = "PHP 25,490 cash price; new 64GB Wi-Fi unit shown available at one store location. The retailer warns to confirm branch stock."
                status = "single_store_location_shown_confirm_stock"
            result.append({
                "device_id": DEVICE, "amount_php": v["current"], "configuration_id": v["id"],
                "configuration_match": f"exact_apple_ipad10_{v['storage']}gb_{'wifi_cellular' if cell else 'wifi'}_retailer_listing",
                "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi + Cellular" if cell else "Wi-Fi",
                "price_type": "current_dated_local_retailer_listing",
                "source_published_at": None, "excerpt": excerpt, "source_url": cell_url,
                "source_kind": "philippine_retailer_exact_configuration_listing",
                "observed_at": OBSERVED, "local_availability_verified": not cell,
                "availability_status": status})
    result.append({
        "device_id": DEVICE, "amount_php": 30450, "configuration_id": f"{DEVICE}-256gb-wifi",
        "configuration_match": "exact_apple_ipad10_256gb_wifi_datablitz_sold_out_listing",
        "variant_storage_gb": 256, "variant_connectivity": "Wi-Fi",
        "price_type": "retailer_listing_sold_out_not_current_buyable_price",
        "source_published_at": None,
        "excerpt": "DataBlitz listed this exact 256GB Wi-Fi configuration at PHP 30,450 but marked the product sold out on the observed collection page. Not used as the catalog's current price.",
        "source_url": URL_DATABLITZ, "source_kind": "retailer_exact_configuration_sold_out_listing",
        "observed_at": OBSERVED, "local_availability_verified": False,
        "availability_status": "sold_out_at_observation_not_currently_buyable"})
    return result


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the pending workbook iPad 10th Gen record; refusing unexpected scope/device.")
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
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact-model Apple Support diagram was located. It is not a product photograph, and no permission or reusable license to republish or hotlink it is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_TECH, "assetUrl": None, "candidateAssetUrl": IMAGE_ASSET,
        "scope": "Official Apple Support diagram for iPad (10th generation); exact family match, but not a product photo and not specific to one storage/connectivity configuration.",
        "rightsTermsUrl": None,
        "rightsCheck": "No reuse permission or license for this image was found in the reviewed page. Do not download or hotlink.",
        "rightsCheckSourcePage": URL_TECH, "observedAt": OBSERVED,
        "altText": "Image unavailable for Apple iPad 10th Gen",
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
                            "historicalPhilippinePricePhp": v["launch"], "datedRetailerListingPhp": v["current"]} for v in VARIANTS],
        "reviewedConfigurations": len(reviews), "reviewedFieldsPerConfiguration": 49,
        "philippineLaunchEvidence": "YugaTech's 2022-11-21 local price list says models listed were officially launched in PH during 2022; exact first-sale date unverified",
        "image": "exact-model Apple Support diagram found; no reusable rights documented; placeholder retained",
        "eligibility": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
