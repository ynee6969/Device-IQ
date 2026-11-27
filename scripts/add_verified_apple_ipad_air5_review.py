#!/usr/bin/env python3
"""Replace iPad Air 5's unconfigured placeholder with exact 2022 variants."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_a9930490a861ed"
UNRECORDED = f"{DEVICE}-unrecorded"
MODEL = "iPad Air 5th Gen"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/apple-ipad-air5-ph-prices-2026-11-27.json"
ARCHIVE = ROOT / "research/enrichment/superseded-model-level-reviews-2026-11-27.json"

URL_TECH = "https://support.apple.com/en-ph/111887"
URL_MODEL_IDS = "https://support.apple.com/en-us/108043"
URL_NEWS = "https://www.apple.com/newsroom/2022/03/apple-introduces-the-most-powerful-and-versatile-ipad-air-ever/"
URL_ENV = "https://www.apple.com/ph/environment/pdf/products/ipad/iPad_Air_PER_March2022.pdf"
URL_PH_PRICE = "https://www.technobaboy.com/2022/03/09/ipad-air-5-2022-official-now-comes-with-m1-chip-5g-price-in-the-philippines/"
URL_PH_AVAILABLE = "https://www.spot.ph/shopping/the-latest-shopping/89068/apple-ipad-air-5-now-available-in-the-philippines-official-prices-a5092-20220419"
URL_PH_PREORDER = "https://www.gadgetpilipinas.net/2022/04/5th-gen-ipad-air-ph-beyond-the-box/"
URL_PH_REPRICE = "https://www.yugatech.com/personal-computing/apple-increases-ipad-air-5th-gen-ipad-9th-gen-prices-in-the-philippines/"
URL_PMC_LIST = "https://powermaccenter.com/pages/installment-options"
URL_ISTORE_LISTING = "https://istore.ph/products/ipad-air-5th-generation"
IMAGE_URL = "https://cdsassets.apple.com/live/7WUAS350/images/ipad/ipad-air-5th-gen-colors.png"

PRICES_LAUNCH = {
    (64, "wifi"): 35990,
    (256, "wifi"): 44990,
    (64, "wifi-cellular"): 44990,
    (256, "wifi-cellular"): 53990,
}
PRICES_REVISED_2022 = {
    (64, "wifi"): 39990,
    (256, "wifi"): 49990,
    (64, "wifi-cellular"): 49990,
    (256, "wifi-cellular"): 59990,
}
PRICES_PMC_UNDATED = {
    (64, "wifi"): 41490,
    (256, "wifi"): 50490,
    (64, "wifi-cellular"): 50490,
    (256, "wifi-cellular"): 59490,
}
VARIANTS: list[dict] = []
for storage in (64, 256):
    for connectivity in ("wifi", "wifi-cellular"):
        cell = connectivity == "wifi-cellular"
        code = "A2588" if not cell else "A2589 / A2591"
        label = f"{storage} GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}"
        VARIANTS.append({
            "storage": storage, "connectivity": connectivity, "cellular": cell,
            "modelCode": code, "label": label,
            "historical": PRICES_LAUNCH[(storage, connectivity)],
            "revised": PRICES_REVISED_2022[(storage, connectivity)],
            "pmcListed": PRICES_PMC_UNDATED[(storage, connectivity)],
            "id": f"{DEVICE}-{storage}gb-{connectivity}",
        })


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None,
      note: str | None = None, candidate_evidence=None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized,
           "note": note or "Exact iPad Air (5th generation) specification checked against the cited manufacturer source."}
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
        src("apple_ipad_air5_specs", URL_TECH, "Apple Support",
            "Manufacturer technical specifications for iPad Air (5th generation)",
            "Apple lists 2022, 64GB/256GB, 10.9-inch Liquid Retina display, M1 and 8GB RAM, cameras/video, battery energy, Wi-Fi/Bluetooth, A2589 cellular bands, USB-C, physical measurements, sensors and Apple Pencil support."),
        src("apple_ipad_air5_model_ids", URL_MODEL_IDS, "Apple Support",
            "Manufacturer model-number and capacity identification",
            "Apple maps A2588 to iPad Air (5th generation) and A2589/A2591 to Wi-Fi + Cellular; Apple lists 64GB and 256GB. The PH price articles do not expose the suffix printed on a locally sold unit."),
        src("apple_ipad_air5_announcement", URL_NEWS, "Apple Newsroom",
            "Product announcement, initial global availability, launch software and accessory support",
            "Apple announced the M1 iPad Air on 2022-03-08, opened orders 2022-03-11, and announced in-store availability from 2022-03-18. It describes 5G cellular models, iPadOS 15, accessories and product features.", "2022-03-08"),
        src("apple_ipad_air5_environment", URL_ENV, "Apple",
            "Product-specific environmental report and material composition",
            "Apple's March 2022 iPad Air Product Environmental Report documents the 5th-generation model and its enclosure materials."),
        src("technobaboy_ipad_air5_ph_prices", URL_PH_PRICE, "Technobaboy",
            "Dated Philippine launch-period configuration price report",
            "Published 2022-03-09, lists the four 64GB/256GB Wi-Fi/cellular PH prices one day after Apple announced the model. This is a secondary dated price report; it does not independently establish the exact first PH sale date or first-day official MSRP.", "2022-03-09"),
        src("gadgetpilipinas_ipad_air5_ph_preorder", URL_PH_PREORDER, "Gadget Pilipinas / Beyond the Box",
            "Dated authorized-retailer PH preorder evidence",
            "Published 2022-04-01, reports Beyond the Box preorders through that evening and quotes SRP of PHP 37,990/46,990 by capacity. Its table does not identify Wi-Fi versus cellular, and these amounts differ from the 2022-03-09 and 2022-04-19 Philippine configuration reports; preserve them as configuration-ambiguous retailer price evidence.", "2022-04-01"),
        src("spot_ipad_air5_ph_availability_prices", URL_PH_AVAILABLE, "Spot.ph",
            "Dated report that exact PH configurations were available and local price list",
            "Published 2022-04-19, says iPad Air 5 was available in the Philippines from Apple's website, Power Mac Center's website and retailers nationwide; lists all four storage/connectivity prices. This supports availability by the publication date, not the first-sale date.", "2022-04-19"),
        src("yugatech_ipad_air5_ph_price_increase", URL_PH_REPRICE, "YugaTech",
            "Dated Philippine retail price-increase report with prior and revised configuration prices",
            "Published 2022-10-25, reports that PH retail prices changed from PHP 35,990/44,990 Wi-Fi and 44,990/53,990 Wi-Fi + Cellular to PHP 39,990/49,990 Wi-Fi and 49,990/59,990 Wi-Fi + Cellular for 64GB/256GB respectively.", "2022-10-25"),
        src("powermaccenter_ipad_air5_price_table", URL_PMC_LIST, "Power Mac Center",
            "Exact configuration price table observation; not treated as current buyable price",
            "The page's installment table displays retail prices for all four Air 5 configurations. Its linked installment validity text refers to 2024 and the page does not expose stock/orderability for these legacy models, so the listed values are retained as an undated stale page observation only."),
        src("istore_ipad_air5_listing", URL_ISTORE_LISTING, "iStore Philippines",
            "Exact-family retailer listing and stock-state cross-check",
            "The product page identifies iPad Air (5th Generation), 64GB, Wi-Fi and shows Sold out. Page price markup is ambiguous; no amount is promoted as a reliable current price."),
    ]


def make_fields(v: dict) -> list[dict]:
    cell = v["cellular"]
    code = v["modelCode"]
    model_field = f("model_number", "apple_ipad_air5_model_ids", code, code,
        note=("Apple maps A2588 to the Wi-Fi model. The workbook's PH unit suffix is not supplied, so this is the Apple global Wi-Fi model mapping, not a verified local part number." if not cell else
              "Apple identifies A2589 and A2591 as Wi-Fi + Cellular iPad Air (5th generation) models. The cited local price/availability sources do not identify which printed part-number suffix was sold in the Philippines."))
    model_field["replaceExisting"] = True
    configuration = f("configuration", "apple_ipad_air5_specs",
        f"10.9-inch / 8GB RAM / {v['storage']}GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'} / {code}",
        f"10.9-inch / 8 GB RAM / {v['storage']} GB / {'Wi-Fi + Cellular' if cell else 'Wi-Fi'}",
        note="Apple lists 64GB and 256GB capacities, a single 8GB RAM amount, and separate Wi-Fi/cellular model numbers. Finish colors are not separate technical configurations. The PH-specific part-number suffix is not given in local sources.")
    configuration["replaceExisting"] = True
    philippine_date = pending(
        "philippine_release_date", "spot_ipad_air5_ph_availability_prices",
        "Beyond the Box preorder was reported on 2022-04-01; Spot.ph reported the device available in the Philippines on 2022-04-19. Neither source establishes the first authorized sale date.",
        "Do not treat preorder opening or the first located availability report as the actual first-sale date. Keep the release-date field blank; dated PH availability by 2022-04-19 is separately recorded.")
    philippine_date["replaceExisting"] = True
    official_price = pending(
        "official_launch_price_php", "technobaboy_ipad_air5_ph_prices",
        f"A Philippine article published 2022-03-09 reports PHP {v['historical']:,} for {v['label']}; primary Apple or retailer documentation confirming first-day official MSRP was not located.",
        "Keep the official-launch-MSRP field blank. Retain dated PH configuration prices as secondary historical observations, not a verified first-day official MSRP.", "PHP")
    official_price["replaceExisting"] = True
    current_price = pending(
        "current_price_php", "istore_ipad_air5_listing",
        "The reviewed iStore Philippines exact-family listing shows Sold out; the page's price markup is ambiguous. The Power Mac Center table does not verify stock/orderability and contains installment terms that expired in 2024.",
        "No current buyable price verified. Keep the catalog's current price empty and retain any dated or stale retailer-page observations outside numeric current-price filtering.", "PHP")
    current_price["replaceExisting"] = True

    rows = [
        model_field,
        f("global_release_date", "apple_ipad_air5_announcement",
          "Apple announced 2022-03-08; orders began 2022-03-11 and initial in-store availability was announced for 2022-03-18.",
          "2022-03-18", unit="date",
          note="Apple's launch release sets in-store availability from 2022-03-18. This is the announced initial global date, not the Philippine first-sale date."),
        configuration,
        philippine_date,
        official_price,
        current_price,
        f("display_size", "apple_ipad_air5_specs", "10.9-inch diagonal; 10.86 inches when measured as a rectangle", 10.9, key="displayInches", unit="in",
          note="Apple markets the panel as 10.9-inch; it specifies 10.86 inches when the rounded-corner panel is measured diagonally as a rectangle. Catalog stores the marketed screen size."),
        f("display_technology", "apple_ipad_air5_specs", "Liquid Retina, LED-backlit Multi-Touch display with IPS technology", "Liquid Retina LED-backlit IPS LCD", key="displayType"),
        f("display_resolution", "apple_ipad_air5_specs", "2360 × 1640 pixels at 264 ppi", "2360 x 1640", key="resolution"),
        nd("display_refresh_rate", "apple_ipad_air5_specs", "Apple's iPad Air 5 technical specifications do not state a display refresh-rate value.", "Refresh rate remains unrecorded; it is not inferred from the absence of ProMotion.", "Hz"),
        f("display_brightness", "apple_ipad_air5_specs", "500 nits", "500 nits", unit="nits"),
        f("display_protection", "apple_ipad_air5_specs", "P3 wide color, True Tone, fully laminated, anti-reflective and fingerprint-resistant oleophobic coatings", "P3; True Tone; fully laminated; anti-reflective; oleophobic coating"),
        f("chipset", "apple_ipad_air5_specs", "Apple M1 chip", "Apple M1", key="chipset"),
        nd("process_node", "apple_ipad_air5_specs", "Apple's reviewed iPad Air 5 specifications do not disclose a semiconductor fabrication node.", "No process node inferred from other M1 products or secondary estimates.", "nm"),
        f("cpu", "apple_ipad_air5_specs", "8-core CPU: 4 performance cores and 4 efficiency cores", "8-core CPU (4 performance + 4 efficiency)", key="cpu"),
        f("gpu", "apple_ipad_air5_specs", "8-core GPU", "8-core Apple GPU", key="gpu"),
        f("operating_system", "apple_ipad_air5_announcement", "Ships with iPadOS 15", "iPadOS 15", key="os",
          note="Apple's announcement describes iPadOS 15 at launch. This is not a claim about a current installed OS version."),
        nd("os_support", "apple_ipad_air5_specs", "Apple does not publish a guaranteed support end date for this iPadOS device.", "Support duration/end date not inferred."),
        f("ram_capacity", "apple_ipad_air5_specs", "8GB RAM", 8, key="ramGb", unit="GB",
          note="Apple lists 8GB RAM for the model; this amount applies to both supported storage capacities."),
        nd("ram_type", "apple_ipad_air5_specs", "Apple does not identify the RAM technology/type in the reviewed specification.", "Memory type not inferred."),
        f("storage_capacity", "apple_ipad_air5_specs", f"{v['storage']}GB", v["storage"], key="storageGb", unit="GB"),
        nd("storage_type", "apple_ipad_air5_specs", "Apple does not state the internal flash-storage interface or type.", "Storage type not inferred."),
        nd("storage_expansion", "apple_ipad_air5_specs", "Apple's reviewed specifications do not identify a memory-card slot or explicitly document internal-storage expansion.", "Do not infer removable or expandable storage from the USB-C port."),
        f("rear_camera_system", "apple_ipad_air5_specs", "12MP Wide rear camera, ƒ/1.8, 5× digital zoom, five-element lens, Focus Pixels autofocus, Smart HDR 3", "12MP Wide rear camera, f/1.8", key="rearCameraMp", unit="MP"),
        nd("main_camera_sensor", "apple_ipad_air5_specs", "Apple does not disclose the main camera sensor manufacturer or part number.", "Sensor make/model not inferred."),
        na("ultrawide_camera", "apple_ipad_air5_specs", "Apple lists one rear 12MP Wide camera; the Ultra Wide module is front-facing.", "No rear Ultra Wide camera is specified."),
        na("telephoto_camera", "apple_ipad_air5_specs", "Apple lists one rear Wide camera and no rear telephoto module.", "No telephoto camera is specified."),
        f("front_camera", "apple_ipad_air5_specs", "12MP Ultra Wide front camera, ƒ/2.4, 122° field of view", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", "apple_ipad_air5_specs", "Rear: 4K at 24/25/30/60fps; 1080p at 25/30/60fps; 720p at 30fps; 1080p slow motion at 120/240fps. Front: 1080p at 25/30/60fps.", "Rear 4K/60fps; front 1080p/60fps; slow motion 1080p/240fps", key="video"),
        f("battery_capacity", "apple_ipad_air5_specs", "Built-in 28.6Wh rechargeable lithium-polymer battery; mAh is not published", 28.6, key="batteryWh", unit="Wh",
          note="Apple publishes watt-hours, not mAh. No mAh conversion is made without a published nominal voltage."),
        f("battery_technology", "apple_ipad_air5_specs", "Rechargeable lithium-polymer battery", "Lithium-polymer"),
        f("wired_charging", "apple_ipad_air5_specs", "USB-C charging; a 20W USB-C power adapter is included. Maximum device input wattage is not stated.", "USB-C charging; 20W adapter included; max device input not stated"),
        nd("wireless_charging", "apple_ipad_air5_specs", "Apple's reviewed specifications do not state wireless or reverse charging support.", "Charging capability is not inferred from omission."),
        f("dimensions", "apple_ipad_air5_specs", "247.6 × 178.5 × 6.1 mm", "247.6 x 178.5 x 6.1 mm", key="dimensions", unit="mm"),
        f("weight", "apple_ipad_air5_specs", f"{'Wi-Fi + Cellular' if cell else 'Wi-Fi'} model: {462 if cell else 461}g", 462 if cell else 461, key="weightG", unit="g"),
        f("materials", "apple_ipad_air5_environment", "Apple's March 2022 product environmental report identifies the iPad Air (5th generation) enclosure material.", "Aluminum enclosure", note="Model-specific material is documented in Apple's product environmental report; recycled-content details are retained in the source record."),
        nd("ingress_protection", "apple_ipad_air5_specs", "Apple's reviewed technical specifications do not state an IP ingress-protection rating.", "No IP rating inferred."),
    ]
    if cell:
        rows += [
            f("sim_esim", "apple_ipad_air5_specs", "Nano-SIM and eSIM", "Nano-SIM and eSIM", key="sim"),
            pending("cellular_bands", "apple_ipad_air5_specs",
                "Apple publishes a 5G/LTE/UMTS band table for model A2589; Apple also identifies A2591 as a Wi-Fi + Cellular variant but the reviewed spec does not give A2591's band table. The PH article does not specify the local part-number suffix.",
                "Keep exact PH/A2591 band coverage unresolved. Do not automatically transfer A2589's table to A2591 or treat the listed bands as proof of a Philippine SKU."),
            f("gnss", "apple_ipad_air5_specs", "GPS/GNSS is listed for Wi-Fi + Cellular models", "GPS/GNSS"),
            f("tablet_cellular_variant", "apple_ipad_air5_specs", "Wi-Fi + Cellular; 5G NR and LTE cellular data", "Wi-Fi + Cellular; 5G/LTE", key="cellular"),
        ]
    else:
        rows += [
            na("sim_esim", "apple_ipad_air5_model_ids", "Wi-Fi-only model A2588; SIM/eSIM is not applicable", "Apple identifies cellular models separately as A2589/A2591."),
            na("cellular_bands", "apple_ipad_air5_model_ids", "Wi-Fi-only A2588 has no cellular radio", "Cellular bands are not applicable to this Wi-Fi configuration."),
            nd("gnss", "apple_ipad_air5_specs", "Apple lists GPS/GNSS for Wi-Fi + Cellular models, but does not list built-in GPS/GNSS for the Wi-Fi configuration.", "Do not claim GNSS on Wi-Fi A2588."),
            f("tablet_cellular_variant", "apple_ipad_air5_specs", "Wi-Fi model A2588", "Wi-Fi only; no cellular modem", key="cellular"),
        ]
    rows += [
        f("wifi", "apple_ipad_air5_specs", "802.11ax Wi-Fi 6; dual band (2.4/5GHz); HT80 with MIMO", "Wi-Fi 6 (802.11ax); dual band; MIMO", key="wifi"),
        f("bluetooth", "apple_ipad_air5_specs", "Bluetooth 5.0", "Bluetooth 5.0"),
        f("usb", "apple_ipad_air5_specs", "USB-C with charging, native DisplayPort and USB 3.1 Gen 2 up to 10Gb/s", "USB-C; USB 3.1 Gen 2 up to 10Gb/s; DisplayPort", key="ports"),
        nd("nfc", "apple_ipad_air5_specs", "Apple does not list NFC in the reviewed iPad Air 5 specification.", "NFC remains unrecorded; absence from this spec sheet is not treated as an explicit no."),
        f("audio", "apple_ipad_air5_specs", "Stereo speakers and dual microphones", "Stereo speakers; dual microphones", key="sound"),
        f("sensors", "apple_ipad_air5_specs", "Touch ID, three-axis gyro, accelerometer, barometer, ambient light sensor; digital compass and iBeacon micro-location", "Touch ID; gyro; accelerometer; barometer; ambient-light sensor; digital compass; iBeacon"),
        f("tablet_stylus", "apple_ipad_air5_specs", "Apple Pencil (2nd generation) and Apple Pencil (USB-C) supported", "Apple Pencil (2nd generation); Apple Pencil (USB-C)", key="stylus"),
        f("tablet_keyboard", "apple_ipad_air5_announcement", "Compatible with Magic Keyboard and Smart Keyboard Folio", "Magic Keyboard; Smart Keyboard Folio", key="keyboard"),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct field reviews, got {len(rows)}")
    return rows


def availability(v: dict) -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Dated Philippine evidence: Beyond the Box preorder reported by 2022-04-01 and availability at Apple Philippines, Power Mac Center and retailers nationwide reported by Spot.ph on 2022-04-19. Exact first-sale date is not documented.",
        "philippineAvailability": "Philippine preorder evidence by 2022-04-01 and local availability reported by 2022-04-19; neither source establishes the first authorized sale date.",
        "observedAt": OBSERVED,
        "qualityFlag": "Exact Apple storage, RAM, connectivity and model-family configurations reviewed. Dated Philippine availability and historical prices are sourced. Exact first-sale date, Philippine part-number suffix, current buyable price and A2591 cellular band table remain unresolved. Workbook study eligibility remains Pending.",
        "catalogModel": MODEL, "manufacturer": "Apple Inc.", "productLine": "iPad Air",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Reported Philippine availability by 2022-04-19; first sale date unknown",
        "researchNotes": "Workbook row 112 is matched to Apple's iPad Air (5th generation, 2022). The catalog exposes four distinct 64GB/256GB Wi-Fi/Wi-Fi + Cellular configurations; the five finishes do not create separate hardware configurations. Apple maps Wi-Fi to A2588 and cellular to A2589/A2591, but Philippine price reports do not identify the unit's part-number suffix. Local sources report preorder availability by 2022-04-01 and retail availability by 2022-04-19. Prices are preserved as dated launch-period, October 2022 revised, and Power Mac Center page observations; no 2026 orderable stock was verified. Battery is retained in Apple's stated Wh, not converted to mAh. A matching Apple Support family illustration is preserved only as an image candidate because reuse rights were not established. Study scope remains Pending.",
        "openIssues": [
            {"issue": "Exact first Philippine sale date is not documented", "action": "Keep the date blank; retain dated preorder and by-date availability evidence."},
            {"issue": "Philippine part-number suffix is not stated in local reports", "action": "Do not claim A2588/A2589/A2591 as a confirmed PH SKU."},
            {"issue": "Current new buyable price/stock is unverified", "action": "Keep current price blank; do not treat sold-out pages or stale price tables as live offers."},
            {"issue": "A2591 cellular band table is not shown on the reviewed Apple specification page", "action": "Keep exact A2591/PH band coverage pending."},
            {"issue": "Image reuse rights are not established", "action": "Keep neutral placeholder and retain exact-family Apple image candidate for rights review."},
            {"issue": "Study eligibility remains Pending", "action": "Preserve workbook study scope."},
        ],
    }


def make_review(v: dict, index: int) -> dict:
    record = {"deviceId": DEVICE, "configurationId": v["id"], "brand": "Apple",
              "model": MODEL, "configuration": v["label"], "configurationLabel": v["label"],
              "modelCode": v["modelCode"], "sources": sources(v), "fields": make_fields(v),
              "availabilityEvidence": availability(v)}
    if index == 0:
        record["replacementVariants"] = [
            {"id": item["id"], "label": item["label"], "modelCode": item["modelCode"],
             "notes": "Distinct Apple storage/connectivity configuration; available finish colors are not split into separate device records."}
            for item in VARIANTS]
        record["replaceUnrecordedPlaceholder"] = True
    else:
        record["replacementVariants"] = [{
            "id": v["id"], "label": v["label"], "modelCode": v["modelCode"],
            "notes": "Distinct Apple storage/connectivity configuration; available finish colors are not split into separate device records."}]
    return record


def price_rows() -> list[dict]:
    result = []
    for v in VARIANTS:
        exact = f"exact_ipad_air5_{v['storage']}gb_{v['connectivity']}"
        for amount, source_url, date, source_kind, price_type, verified, availability_status, note in [
            (v["historical"], URL_PH_PRICE, "2022-03-09", "dated_secondary_ph_launch_period_price_report",
             "historical_ph_reported_price_not_first_day_msrp", False,
             "preorder_period_price_report_local_first_sale_not_yet_established",
             "Technobaboy reported this exact configuration's Philippine price before the announced local retail-availability window."),
            (v["historical"], URL_PH_AVAILABLE, "2022-04-19", "dated_secondary_ph_availability_and_price_report",
             "historical_ph_reported_price_not_current_offer", True,
             "reported_available_in_ph_by_2022_04_19_exact_first_sale_unknown",
             "Spot.ph reported local availability and this exact storage/connectivity price on 2022-04-19; not a current offer."),
            (v["revised"], URL_PH_REPRICE, "2022-10-25", "dated_secondary_ph_price_change_report",
             "historical_ph_revised_retail_price_not_current_offer", True,
             "reported_ph_retail_price_on_2022_10_25_current_stock_unknown",
             "YugaTech reports this revised PH retail price after the October 2022 price increase."),
            (v["pmcListed"], URL_PMC_LIST, None, "philippine_authorized_retailer_page_observation",
             "undated_retailer_table_price_terms_expired_not_current_buyable", False,
             "page_observed_2026_11_27_terms_expired_stock_not_verified",
             "Power Mac Center page displays this exact retail price, but its installment validity text refers to 2024 and page does not confirm stock/orderability."),
        ]:
            result.append({
                "device_id": DEVICE, "amount_php": amount, "configuration_id": v["id"],
                "configuration_match": exact,
                "variant_storage_gb": v["storage"],
                "variant_connectivity": "Wi-Fi + Cellular" if v["cellular"] else "Wi-Fi",
                "variant_model_number": v["modelCode"],
                "price_type": price_type, "source_published_at": date,
                "excerpt": f"{note} Amount: PHP {amount:,} for {v['label']}.",
                "source_url": source_url, "source_kind": source_kind,
                "observed_at": date or OBSERVED,
                "local_availability_verified": verified,
                "availability_status": availability_status,
            })
    for storage, amount in ((64, 37990), (256, 46990)):
        result.append({
            "device_id": DEVICE, "amount_php": amount, "configuration_id": None,
            "configuration_match": f"storage_only_{storage}gb_connectivity_not_disclosed_beyond_the_box_preorder",
            "variant_storage_gb": storage, "variant_connectivity": None,
            "price_type": "authorized_retailer_preorder_srp_connectivity_unspecified_conflicts_with_ph_reports",
            "source_published_at": "2022-04-01",
            "excerpt": f"Gadget Pilipinas reports Beyond the Box preorder SRP of PHP {amount:,} for {storage}GB iPad Air 5. The article's table does not specify Wi-Fi or cellular, and the amount differs from other dated PH price reports; not assigned to a specific connectivity configuration or treated as current price.",
            "source_url": URL_PH_PREORDER,
            "source_kind": "dated_authorized_retailer_preorder_report_configuration_ambiguous",
            "observed_at": "2022-04-01", "local_availability_verified": False,
            "availability_status": "authorized_retailer_preorder_reported_first_sale_unknown",
        })
    return result


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the pending workbook iPad Air 5 record; refusing unexpected scope/device.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {v["id"] for v in VARIANTS}
    replacing_placeholder = len(current_ids) == 1 and current_ids == {UNRECORDED}
    updating_integrated = current_ids == expected_ids
    if not (replacing_placeholder or updating_integrated):
        raise ValueError("Expected either the original unrecorded placeholder or the exact four integrated variants; refusing unexpected configurations.")

    archive = json.loads(ARCHIVE.read_text(encoding="utf-8")) if ARCHIVE.exists() else {"records": []}
    old = next((r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED), None)
    if old:
        exists = any(r.get("deviceId") == DEVICE and r.get("supersededConfigurationId") == UNRECORDED for r in archive["records"])
        if not exists:
            archive["records"].append({"deviceId": DEVICE, "model": MODEL,
                "supersededConfigurationId": UNRECORDED, "supersededAt": OBSERVED,
                "reason": "Replaced the model-level record with four exact Apple storage/connectivity configurations; the original 13-field review and source observations are preserved in this archive.",
                "review": old})
        manual["records"] = [r for r in manual["records"] if not (r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED)]
    ARCHIVE.write_text(json.dumps(archive, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for index, variant in enumerate(VARIANTS):
        add_review(manual, catalog, make_review(variant, index))
    targets = {(DEVICE, v["id"]) for v in VARIANTS}
    deduplicate_target_reviews(manual, targets)
    for variant in VARIANTS:
        saved = next(r for r in manual["records"] if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, variant["id"]))
        if variant["id"] != VARIANTS[0]["id"]:
            saved.pop("replacementVariants", None)
            saved.pop("replaceUnrecordedPlaceholder", None)
            saved.pop("additionalVariants", None)
        saved.update({"model": MODEL, "configuration": variant["label"],
                      "configurationLabel": variant["label"], "modelCode": variant["modelCode"]})
        source_updates = {source["id"]: source for source in sources(variant)}
        saved["sources"] = [source_updates.get(source["id"], source) for source in saved.get("sources", [])]
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Apple Support provides an exact-family iPad Air (5th generation) illustration, but no permission or reusable license to republish or hotlink it is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_MODEL_IDS, "assetUrl": None, "candidateAssetUrl": IMAGE_URL,
        "scope": "Apple Support product identification illustration for iPad Air (5th generation), shown in multiple finishes; exact family but not a storage/connectivity-specific unit.",
        "publisher": "Apple", "rightsTermsUrl": None,
        "rightsCheck": "No reuse permission or license was found on the reviewed Apple Support page. Do not download or hotlink.",
        "rightsCheckSourcePage": URL_MODEL_IDS, "observedAt": OBSERVED,
        "altText": "Image unavailable for Apple iPad Air 5th Gen",
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
    known = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type"),
              p.get("source_url"), p.get("configuration_match")) for p in latest.get("prices", [])}
    for price in prices:
        key = (price["device_id"], price["configuration_id"], price["price_type"],
               price["source_url"], price["configuration_match"])
        if key not in known:
            latest.setdefault("prices", []).append(price)
            known.add(key)
    latest["run_at"] = OBSERVED
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "model": MODEL,
        "configurations": [{"id": v["id"], "modelNumber": v["modelCode"], "label": v["label"],
                            "historicalPhilippinePricePhp": v["historical"],
                            "october2022RevisedPricePhp": v["revised"], "currentBuyablePricePhp": None}
                           for v in VARIANTS],
        "reviewedConfigurations": len(VARIANTS), "reviewedFieldsPerConfiguration": 49,
        "philippineAvailability": "preorders reported by 2022-04-01 and retail availability reported by 2022-04-19; exact first-sale date unknown",
        "prices": "dated launch-period, retailer-preorder, October 2022 and stale PMC page observations; ambiguous retailer prices kept unassigned; no current buyable offer verified",
        "image": "exact-family Apple Support candidate retained; reuse rights not established; neutral placeholder kept",
        "eligibility": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
