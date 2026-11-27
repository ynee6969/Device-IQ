#!/usr/bin/env python3
"""Replace the iPad A16 unconfigured placeholder with six exact PH configs."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_73e4c3a19b8741"
UNRECORDED = f"{DEVICE}-unrecorded"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST_REVIEWED = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/apple-ipad-a16-ph-prices-2026-11-27.json"
ARCHIVE = ROOT / "research/enrichment/superseded-model-level-reviews-2026-11-27.json"

URL_SPECS = "https://www.apple.com/ph/ipad-11/specs/"
URL_TECH = "https://support.apple.com/en-us/122240"
URL_BUY = "https://www.apple.com/ph/shop/buy-ipad/ipad"
URL_NEWS = "https://www.apple.com/newsroom/2025/03/apple-introduces-ipad-air-with-powerful-m3-chip-and-new-magic-keyboard/"
URL_MODEL_IDS = "https://support.apple.com/en-gb/108043"
URL_ENV = "https://www.apple.com/ph/environment/pdf/products/ipad/iPad_A16_PER_MAR2025.pdf"
URL_EU_SPECS = "https://www.apple.com/si/ipad-11/specs/"
URL_PMC_NEWS = "https://powermaccenter.com/blogs/news/power-meets-portability-discover-the-next-gen-ipad-amp-mac-at-pmc"
URL_GIZ = "https://www.gizguide.com/2025/03/ipad-2025-a16-ph-price.html"
URL_YUGA = "https://www.yugatech.com/news/ipad-air-m3-ipad-a16-now-also-available-at-power-mac-center/"
IMAGE_URL = "https://www.apple.com/v/ipad-11/specs/d/images/specs/finish__ff9ehlnqqxqy_large.jpg"

DEVICE_MODEL = "iPad (A16/11th Gen)"
VARIANTS = [
    {"storage": 128, "connectivity": "wifi", "label": "128 GB / Wi-Fi", "modelCode": "A3354", "current": 32990, "launch": 24990},
    {"storage": 256, "connectivity": "wifi", "label": "256 GB / Wi-Fi", "modelCode": "A3354", "current": 39990, "launch": 31990},
    {"storage": 512, "connectivity": "wifi", "label": "512 GB / Wi-Fi", "modelCode": "A3354", "current": 53990, "launch": 45990},
    {"storage": 128, "connectivity": "wifi-cellular", "label": "128 GB / Wi-Fi + Cellular", "modelCode": "A3355", "current": 42990, "launch": None},
    {"storage": 256, "connectivity": "wifi-cellular", "label": "256 GB / Wi-Fi + Cellular", "modelCode": "A3355", "current": 49990, "launch": None},
    {"storage": 512, "connectivity": "wifi-cellular", "label": "512 GB / Wi-Fi + Cellular", "modelCode": "A3355", "current": 63990, "launch": None},
]
for variant in VARIANTS:
    variant["id"] = f"{DEVICE}-{variant['storage']}gb-{variant['connectivity']}"
    variant["buyUrl"] = f"https://www.apple.com/ph/shop/buy-ipad/ipad/{variant['storage']}gb-blue-{variant['connectivity']}"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def common_sources(variant: dict) -> list[dict]:
    is_cell = variant["connectivity"] == "wifi-cellular"
    current_source = f"apple_ipad_a16_current_{variant['storage']}_{variant['connectivity']}"
    return [
        src("apple_ipad_a16_ph_specs", URL_SPECS, "Apple Philippines",
            "Philippine manufacturer technical specifications for display, chip, cameras, connectivity, battery, accessories and supported capacities",
            "Apple Philippines lists 128GB, 256GB and 512GB capacities; an 11-inch Liquid Retina display (10.86-inch rectangle measurement), IPS, 2360×1640 at 264ppi, A16 with 5-core CPU/4-core GPU, cameras, Wi-Fi 6, Bluetooth 5.3, cellular/eSIM details, 28.93Wh battery, USB-C, GNSS on cellular models, sensors and supported accessories."),
        src("apple_ipad_a16_support_specs", URL_TECH, "Apple Support",
            "Cross-check of detailed model specifications and Wi-Fi/cellular weights",
            "Apple's model-specific support page lists year introduced 2025; the same display, chip, camera and capacity specifications; Wi-Fi weight 477g and Wi-Fi + Cellular weight 481g; 28.93Wh lithium-polymer battery; and camera video modes."),
        src(current_source, variant["buyUrl"], "Apple Philippines Online Store",
            "Exact storage/connectivity list price and current local product listing",
            f"Apple Philippines buy page lists the {variant['label']} configuration at PHP {variant['current']:,} on {OBSERVED}. This is a dated manufacturer-store list price; stock, delivery estimate and checkout completion were not verified."),
        src("apple_ipad_a16_buy_options", URL_BUY, "Apple Philippines Online Store",
            "Cross-check of all exact configuration options, colors and prices",
            "Apple's Philippines buy page exposes all six storage/connectivity configurations: 128GB, 256GB and 512GB in Wi-Fi and Wi-Fi + Cellular. Current prices observed 2026-11-27 are PHP 32,990 / 39,990 / 53,990 for Wi-Fi and PHP 42,990 / 49,990 / 63,990 for Wi-Fi + Cellular. Four colors are available."),
        src("apple_ipad_a16_global_launch", URL_NEWS, "Apple Newsroom",
            "Manufacturer model announcement and global availability date",
            "Apple announced iPad (A16) on 2025-03-04, opened pre-orders that day, and said it would begin arriving and reach Apple Stores/authorized resellers on 2025-03-12. It lists 128GB/256GB/512GB, four colors, and Wi-Fi/Wi-Fi + Cellular versions.", "2025-03-04"),
        src("apple_ipad_a16_model_ids", URL_MODEL_IDS, "Apple Support",
            "Manufacturer model-number mapping for Wi-Fi and Wi-Fi + Cellular models",
            "Apple's model identification page maps A3354 to iPad (A16) Wi-Fi and A3355 to iPad (A16) Wi-Fi + Cellular."),
        src("apple_ipad_a16_environment", URL_ENV, "Apple",
            "Product-specific environmental report and enclosure-material evidence",
            "Apple's iPad (A16) Product Environmental Report says the enclosure uses 100% recycled aluminum and the model contains 40% recycled content. The report describes the product configuration and launch-time environmental evaluation."),
        src("apple_ipad_a16_eu_product_info", URL_EU_SPECS, "Apple Slovenia",
            "Apple EU product-information label for the exact A3354 Wi-Fi model, including ingress-protection classification",
            "The Apple EU energy/product-information label identifies iPad (A16) Wi-Fi model A3354 and lists IP42. The rating is applied only to the matching A3354 configurations; this evidence is not generalized to cellular model A3355."),
        src("apple_ipad_a16_pmc_ph_launch", URL_PMC_NEWS, "Power Mac Center",
            "Dated Philippine authorized-reseller availability report",
            "Power Mac Center's article dated 2025-05-09 says iPad (A16) is then available in Power Mac Center and The Loop stores and online. This is the first dated local authorized-retailer availability found in this review; it does not establish the earliest sale by every Philippine channel.", "2025-05-09"),
        src("apple_ipad_a16_ph_launch_prices", URL_GIZ, "GIZGUIDE",
            "Historical Philippine Apple Store launch-price report for Wi-Fi capacities",
            "Published 2025-03-05, GIZGUIDE reports Apple Philippines listing Wi-Fi iPad (A16) at PHP 24,990 (128GB), PHP 31,990 (256GB), and PHP 45,990 (512GB). It says authorized local retailers had not yet announced availability at that time; these are historical Apple PH online-list prices, not reseller stock claims.", "2025-03-05"),
        src("apple_ipad_a16_pmc_config", "https://powermaccenter.com/pages/ipad-a16", "Power Mac Center",
            "Philippine authorized-reseller product description and accessory cross-check",
            "Power Mac Center's iPad A16 page describes the 10.86-inch display, Center Stage front camera, Wi-Fi 6 and 5G and accessory compatibility; it states Apple Pencil accessories are sold separately."),
    ]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, catalog_value=None, unit: str | None = None,
      note: str | None = None, price_type: str | None = None,
      price_observed: str | None = None, listing_status: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key,
                    "catalogValue": normalized if catalog_value is None else catalog_value})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    if price_type:
        row.update({"priceType": price_type, "priceObservedAt": price_observed,
                    "priceCondition": "new"})
    if listing_status:
        row["listingStatus"] = listing_status
    return row


def nd(fid: str, sid: str, note: str, *, source_value: str | None = None,
       unit: str | None = None) -> dict:
    return f(fid, sid, source_value or note, None, status="NOT_DISCLOSED", unit=unit, note=note)


def na(fid: str, sid: str, value: str, note: str) -> dict:
    return f(fid, sid, value, None, status="NOT_APPLICABLE", note=note)


def make_fields(v: dict) -> list[dict]:
    is_cell = v["connectivity"] == "wifi-cellular"
    product_id = f"apple_ipad_a16_current_{v['storage']}_{v['connectivity']}"
    configuration = v["label"]
    model_code = v["modelCode"]
    rows = [
        f("model_number", "apple_ipad_a16_model_ids", model_code, model_code,
          note="Apple maps this model number to the matching Wi-Fi or Wi-Fi + Cellular iPad (A16) model."),
        f("global_release_date", "apple_ipad_a16_global_launch", "Global availability begins 2025-03-12", "2025-03-12", unit="date",
          note="Apple Newsroom says the A16 iPad would begin arriving to customers and reach Apple Stores/authorized resellers from March 12, 2025."),
        f("configuration", product_id, configuration, configuration,
          note="Exact capacity/connectivity option shown on Apple Philippines' current buy page; supported capacities and connectivity classes are separately identified by the manufacturer."),
        f("philippine_release_date", "apple_ipad_a16_pmc_ph_launch", "Power Mac Center says the model is now available in its Philippine stores and online on 2025-05-09", "2025-05-09", status="VERIFIED_SECONDARY", unit="date",
          note="This is the first dated local authorized-retailer availability report found in this review, not a claim that no Philippine channel sold it earlier."),
    ]
    if v["launch"] is not None:
        rows.append(f("official_launch_price_php", "apple_ipad_a16_ph_launch_prices",
            f"PHP {v['launch']:,} Philippine Apple Store Wi-Fi list price reported 2025-03-05 for {v['storage']}GB", v["launch"],
            status="VERIFIED_SECONDARY", unit="PHP",
            note="GIZGUIDE reports the Philippine Apple Store listing price on 2025-03-05. Apple Newsroom itself did not publish a Philippine peso price; the value is attributed to the contemporaneous local report."))
    else:
        rows.append(nd("official_launch_price_php", "apple_ipad_a16_global_launch",
            "No launch-period Philippine peso list price for the Wi-Fi + Cellular configuration was found in the reviewed sources.", unit="PHP"))
    rows += [
        f("current_price_php", product_id, f"PHP {v['current']:,} current Apple Philippines list price", v["current"], unit="PHP",
          price_type="Current official Apple Philippines Online Store list price", price_observed=OBSERVED,
          listing_status="Not verified",
          note=f"Apple Philippines lists {configuration} at PHP {v['current']:,} on {OBSERVED}. Inventory/checkout status was not confirmed."),
        f("display_size", "apple_ipad_a16_ph_specs", "11-inch marketed diagonal; 10.86 inches measured as a rectangle", 10.86, key="displayInches", unit="in",
          note="Apple's exact model page gives the 10.86-inch rectangular measurement and markets the display as 11-inch."),
        f("display_technology", "apple_ipad_a16_ph_specs", "LED-backlit Multi-Touch Liquid Retina display with IPS technology", "LED-backlit Multi-Touch IPS LCD", key="displayType"),
        f("display_resolution", "apple_ipad_a16_ph_specs", "2360 × 1640 pixels at 264ppi", "2360 x 1640", key="resolution"),
        nd("display_refresh_rate", "apple_ipad_a16_ph_specs", "Apple's specification page does not state a numeric refresh rate for this display.", unit="Hz"),
        f("display_brightness", "apple_ipad_a16_ph_specs", "500 nits", 500, unit="nits"),
        f("display_protection", "apple_ipad_a16_ph_specs", "Fingerprint-resistant oleophobic coating", "Fingerprint-resistant oleophobic coating"),
        f("chipset", "apple_ipad_a16_ph_specs", "Apple A16 chip", "Apple A16", key="chipset"),
        nd("process_node", "apple_ipad_a16_ph_specs", "Apple does not publish a process-node value on the reviewed exact-model specifications.", unit="nm"),
        f("cpu", "apple_ipad_a16_ph_specs", "5-core CPU", "5-core CPU", key="cpu"),
        f("gpu", "apple_ipad_a16_ph_specs", "4-core GPU", "4-core Apple GPU", key="gpu"),
        f("operating_system", "apple_ipad_a16_ph_specs", "iPadOS; launch version not stated on the current technical-specification page", "iPadOS", key="os",
          note="Apple's product-specific technical page identifies iPadOS, but does not name the factory-installed launch build."),
        nd("os_support", "apple_ipad_a16_ph_specs", "Apple does not publish a guaranteed end date or minimum duration for OS/security updates for this model."),
        nd("ram_capacity", "apple_ipad_a16_ph_specs", "Apple's product-specific technical specifications and capacity selector do not publish RAM capacity; no third-party teardown value is substituted.", unit="GB"),
        nd("ram_type", "apple_ipad_a16_ph_specs", "RAM type is not published by Apple for this model."),
        f("storage_capacity", product_id, f"{v['storage']}GB storage", v["storage"], key="storageGb", unit="GB"),
        nd("storage_type", "apple_ipad_a16_ph_specs", "Apple lists capacity but does not identify the exact installed flash-storage technology in the reviewed sources."),
        nd("storage_expansion", "apple_ipad_a16_ph_specs", "Apple specifies USB-C external display/data support but does not list an SD/microSD card expansion slot or an internal capacity-expansion feature."),
        f("rear_camera_system", "apple_ipad_a16_ph_specs", "12MP Wide rear camera, ƒ/1.8; up to 5× digital zoom", "12 MP Wide rear camera; ƒ/1.8; 5x digital zoom", key="rearCameraMp", unit="MP"),
        nd("main_camera_sensor", "apple_ipad_a16_ph_specs", "Apple does not publish the rear camera sensor manufacturer or component identifier."),
        f("ultrawide_camera", "apple_ipad_a16_pmc_config", "12MP Ultra Wide front-facing Center Stage camera; no rear ultra-wide lens is listed", "12 MP Ultra Wide front Center Stage; rear ultra-wide not listed", status="VERIFIED_SECONDARY", unit="MP",
          note="Power Mac Center calls the front-facing Center Stage module Ultra Wide. Apple lists one 12MP Wide rear camera; this field is explicitly labeled as a front camera."),
        na("telephoto_camera", "apple_ipad_a16_ph_specs", "No telephoto rear camera is listed", "The complete rear camera specification lists one 12MP Wide camera and digital zoom; no telephoto module is specified."),
        f("front_camera", "apple_ipad_a16_ph_specs", "12MP landscape Center Stage camera, ƒ/2.4", 12, key="frontCameraMp", unit="MP"),
        f("video_recording", "apple_ipad_a16_ph_specs", "Rear: 4K 24/25/30/60fps; 1080p 25/30/60fps; 720p 30/60fps; 1080p slow motion 120/240fps. Front: 1080p 25/30/60fps.",
          "Rear: 4K 24/25/30/60fps; 1080p 25/30/60fps; 720p 30/60fps; 1080p slow motion 120/240fps. Front: 1080p 25/30/60fps."),
        f("battery_capacity", "apple_ipad_a16_ph_specs", "28.93Wh built-in rechargeable lithium-polymer battery; Apple does not state an mAh value", 28.93, key="batteryWh", unit="Wh",
          note="Exact energy rating from Apple. No mAh conversion is made without a published nominal voltage."),
        f("battery_technology", "apple_ipad_a16_ph_specs", "Rechargeable lithium-polymer battery", "Lithium-polymer"),
        nd("wired_charging", "apple_ipad_a16_ph_specs", "Apple includes a 20W USB-C power adapter and lists USB-C charging, but does not publish a maximum device input-wattage rating on the reviewed specification page.", unit="W"),
        nd("wireless_charging", "apple_ipad_a16_ph_specs", "The reviewed official specifications list USB-C charging and do not disclose wireless or reverse charging."),
        f("dimensions", "apple_ipad_a16_ph_specs", "248.6 × 179.5 × 7.0mm", "248.6 x 179.5 x 7.0 mm", key="dimensions", unit="mm"),
        f("weight", "apple_ipad_a16_ph_specs", "Wi-Fi 477g; Wi-Fi + Cellular 481g", 481 if is_cell else 477, key="weightG", unit="g"),
        f("materials", "apple_ipad_a16_environment", "100% recycled aluminum enclosure and metal chassis; 15% recycled cover glass reported on Apple Philippines' product specification page", "Aluminum enclosure and metal chassis (100% recycled aluminum); cover glass (15% recycled glass)", status="VERIFIED", note="Apple's product environmental report confirms recycled aluminum in the enclosure; Apple's local technical page supplies the cover-glass recycled content."),
        f("ingress_protection", "apple_ipad_a16_eu_product_info", "IP42 on Apple EU product-information label for Wi-Fi model A3354", "IP42", status="VERIFIED", unit="IP",
          note="For the Wi-Fi A3354 variant only, Apple's EU product-information label identifies model A3354 and lists IP42. This regional manufacturer label is not generalized to A3355 cellular variants." ) if not is_cell else nd("ingress_protection", "apple_ipad_a16_ph_specs", "No IP rating for the A3355 Wi-Fi + Cellular model was found in the reviewed Philippine or manufacturer technical pages."),
    ]
    if is_cell:
        rows += [
            f("sim_esim", "apple_ipad_a16_ph_specs", "Wi-Fi + Cellular model A3355 uses eSIM; not compatible with physical SIM cards", "eSIM only; no physical SIM", key="sim"),
            f("cellular_bands", "apple_ipad_a16_ph_specs", "5G NR model A3355 bands n1/n2/n3/n5/n7/n8/n12/n14/n20/n25/n26/n28/n29/n30/n38/n40/n41/n48/n66/n70/n71/n75/n76/n77/n78/n79; FDD-LTE bands 1/2/3/4/5/7/8/11/12/13/14/17/18/19/20/21/25/26/28/29/30/32/66/71; TD-LTE bands 34/38/39/40/41/42/48", "5G NR and LTE bands listed by Apple for model A3355", note="Apple Philippines lists these bands under cellular model A3355. Carrier deployment and local band use are separate from the device's supported bands."),
            f("gnss", "apple_ipad_a16_ph_specs", "GPS/GNSS on Wi-Fi + Cellular models", "GPS/GNSS", status="VERIFIED"),
            f("tablet_cellular_variant", "apple_ipad_a16_ph_specs", "Wi-Fi + Cellular variant; supports 5G/LTE and eSIM", "Wi-Fi + Cellular 5G/LTE with eSIM", status="VERIFIED", key="cellular"),
        ]
    else:
        rows += [
            na("sim_esim", "apple_ipad_a16_ph_specs", "Wi-Fi model A3354; cellular SIM/eSIM is not applicable", "Manufacturer distinguishes A3354 Wi-Fi from the separate A3355 Wi-Fi + Cellular model."),
            na("cellular_bands", "apple_ipad_a16_ph_specs", "Wi-Fi model A3354 has no listed cellular radio", "The manufacturer lists 5G/LTE only for the separate Wi-Fi + Cellular A3355 model."),
            na("gnss", "apple_ipad_a16_ph_specs", "GPS/GNSS is listed only for Wi-Fi + Cellular models", "Apple Philippines lists digital compass/Wi-Fi/iBeacon for all models and GPS/GNSS for Wi-Fi + Cellular models."),
            f("tablet_cellular_variant", "apple_ipad_a16_ph_specs", "Wi-Fi-only variant A3354", "Wi-Fi only; no cellular modem", status="VERIFIED", key="cellular"),
        ]
    rows += [
        f("wifi", "apple_ipad_a16_ph_specs", "Wi-Fi 6 (802.11ax), 2×2 MIMO, simultaneous dual band", "Wi-Fi 6 (802.11ax), 2x2 MIMO", key="wifi"),
        f("bluetooth", "apple_ipad_a16_ph_specs", "Bluetooth 5.3", "Bluetooth 5.3"),
        f("usb", "apple_ipad_a16_ph_specs", "USB-C with USB 2.0 data up to 480Mb/s and DisplayPort support", "USB-C; USB 2.0 up to 480Mb/s; DisplayPort", key="ports"),
        nd("nfc", "apple_ipad_a16_ph_specs", "NFC is not listed in the reviewed exact-model specification."),
        f("audio", "apple_ipad_a16_ph_specs", "Landscape stereo speakers and dual microphones; an analog 3.5mm jack is not listed", "Landscape stereo speakers; dual microphones; 3.5mm jack not listed", key="sound"),
        f("sensors", "apple_ipad_a16_ph_specs", "Touch ID, three-axis gyroscope, accelerometer, barometer and ambient-light sensor", "Touch ID; three-axis gyroscope; accelerometer; barometer; ambient-light sensor"),
        f("tablet_stylus", "apple_ipad_a16_ph_specs", "Supports Apple Pencil (USB-C) and Apple Pencil (1st generation; USB-C adapter required)", "Apple Pencil (USB-C); Apple Pencil (1st generation, adapter required)", status="VERIFIED", key="stylus"),
        f("tablet_keyboard", "apple_ipad_a16_ph_specs", "Magic Keyboard Folio compatible; sold separately", "Apple Magic Keyboard Folio support; sold separately", status="VERIFIED", key="keyboard"),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct tablet field reviews, got {len(rows)}")
    return rows


def availability(v: dict) -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Apple Philippines lists this exact iPad (A16) storage/connectivity option and price. Power Mac Center reported the model available in its stores and online on 2025-05-09. Current inventory/checkout status was not verified.",
        "philippineAvailability": "First dated Philippine authorized-retailer availability report found: Power Mac Center said iPad (A16) was then available in stores and online on 2025-05-09. Apple Philippines currently lists the exact capacity/connectivity options.",
        "observedAt": OBSERVED,
        "qualityFlag": "Manually reviewed; official Apple PH storage/connectivity options, exact model numbers and dated list prices verified. Philippine reseller availability reported 2025-05-09. RAM is not disclosed. Study eligibility remains Pending.",
        "catalogModel": DEVICE_MODEL, "manufacturer": "Apple Inc.", "productLine": "iPad",
        "philippineReleaseYear": 2025,
        "philippineDateLabel": "First dated Philippine authorized-retailer availability report",
        "researchNotes": f"The workbook record {DEVICE_MODEL} is matched to Apple's iPad (A16), announced 2025-03-04 with global availability beginning 2025-03-12. Apple's Philippine store offers separate {v['label']} configurations in six total storage/connectivity combinations; this review keeps those configurations separate. Apple PH list price is PHP {v['current']:,} observed {OBSERVED}; current stock/checkout not verified. Power Mac Center reported local availability 2025-05-09. Apple does not publish RAM capacity or guaranteed OS support duration. Current device image has no documented reuse permission; neutral placeholder retained. Study scope remains Pending.",
        "openIssues": [
            {"issue": "RAM capacity is not disclosed by Apple", "action": "Keep RAM blank; do not substitute third-party teardown estimates."},
            {"issue": "Apple's current store price is listed but stock/checkout is not confirmed", "action": "Display a dated list price without an in-stock claim."},
            {"issue": "No Philippine launch-period price was found for Wi-Fi + Cellular configs", "action": "Keep the historical price blank for those three variants."},
            {"issue": "Study eligibility remains Pending", "action": "Preserve workbook scope until thesis screening rules are applied."},
            {"issue": "The official product image has no documented reuse license", "action": "Keep the neutral placeholder and preserve the source page/asset for rights review."},
        ],
    }


def make_review(v: dict, index: int) -> dict:
    record = {
        "deviceId": DEVICE, "configurationId": v["id"], "brand": "Apple",
        "model": DEVICE_MODEL, "configuration": v["label"],
        "configurationLabel": v["label"], "modelCode": v["modelCode"],
        "sources": common_sources(v), "fields": make_fields(v),
        "availabilityEvidence": availability(v),
    }
    variant = {"id": v["id"], "label": v["label"], "modelCode": v["modelCode"],
               "notes": "Distinct Apple PH storage/connectivity option. Four color choices are listed by Apple but are not split because they share the same storage/connectivity configuration."}
    if index == 0:
        record["replacementVariants"] = [{
            "id": x["id"], "label": x["label"], "modelCode": x["modelCode"],
            "notes": "Distinct Apple PH storage/connectivity option. Four color choices are listed by Apple but are not split because they share the same storage/connectivity configuration.",
        } for x in VARIANTS]
        record["replaceUnrecordedPlaceholder"] = True
    else:
        # add_review needs the replacement entry to recognize a config because
        # its in-memory catalog still has the original placeholder. The first
        # review already installs all six variants, so this marker is removed
        # from the saved later reviews below before public-catalog generation.
        record["replacementVariants"] = [variant]
    return record


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the workbook's pending Apple iPad A16 record; refusing unexpected scope/device.")
    if len(device.get("variants", [])) != 1 or device["variants"][0]["id"] != UNRECORDED:
        raise ValueError("Expected one unrecorded placeholder configuration; review before replacement.")

    # Preserve the earlier unmatched model-level candidate review before replacing
    # its unconfigured placeholder with the six exact Apple PH configurations.
    archive = json.loads(ARCHIVE.read_text(encoding="utf-8")) if ARCHIVE.exists() else {"records": []}
    archived = next((r for r in manual["records"]
                     if r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED), None)
    if archived:
        if not any(x.get("deviceId") == DEVICE and x.get("supersededConfigurationId") == UNRECORDED for x in archive["records"]):
            archive["records"].append({"deviceId": DEVICE, "model": DEVICE_MODEL,
                "supersededConfigurationId": UNRECORDED, "supersededAt": OBSERVED,
                "reason": "Replaced a model-level, unconfigured candidate review with six exact Apple PH capacity/connectivity configurations; source candidate observations remain in latest-reviewed research data.",
                "review": archived})
        manual["records"] = [r for r in manual["records"] if not (r.get("deviceId") == DEVICE and r.get("configurationId") == UNRECORDED)]
    ARCHIVE.write_text(json.dumps(archive, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reviews = [make_review(v, i) for i, v in enumerate(VARIANTS)]
    for review in reviews:
        add_review(manual, catalog, review)
    for v in VARIANTS[1:]:
        saved = next(r for r in manual["records"]
                     if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, v["id"]))
        saved.pop("replacementVariants", None)
        saved.pop("replaceUnrecordedPlaceholder", None)
        saved.pop("additionalVariants", None)
    targets = {(DEVICE, v["id"]) for v in VARIANTS}
    deduplicate_target_reviews(manual, targets)
    for v in VARIANTS:
        saved = next(r for r in manual["records"]
                     if (r.get("deviceId"), r.get("configurationId")) == (DEVICE, v["id"]))
        saved.update({"model": DEVICE_MODEL, "configuration": v["label"],
                      "configurationLabel": v["label"], "modelCode": v["modelCode"]})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Apple's exact-model Philippine specification page links to the iPad (A16) in four colors, but no reuse license, credit requirement or permission to republish/hotlink is documented. Keep the neutral placeholder.",
        "sourcePage": URL_SPECS, "assetUrl": None, "candidateAssetUrl": IMAGE_URL,
        "scope": "Official Apple Philippines iPad (A16) product montage showing the exact model in its listed colors; no single storage/connectivity configuration is visually distinguishable.",
        "rightsTermsUrl": None,
        "rightsCheck": "Reviewed the official product page and linked image. No reuse permission or license was located. Do not download or hotlink.",
        "rightsCheckSourcePage": URL_SPECS, "observedAt": OBSERVED,
        "altText": "Image unavailable for Apple iPad (A16/11th Gen)",
    }
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for v in VARIANTS:
        current_source_id = f"apple_ipad_a16_current_{v['storage']}_{v['connectivity']}"
        if v["launch"] is not None:
            prices.append({
                "device_id": DEVICE, "amount_php": v["launch"], "configuration_id": v["id"],
                "configuration_match": f"exact_ph_apple_ipad_a16_{v['storage']}gb_wifi_launch",
                "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi",
                "price_type": "historical_ph_apple_store_launch_list_price_reported",
                "source_published_at": "2025-03-05",
                "excerpt": f"GIZGUIDE reported the Apple PH store Wi-Fi {v['storage']}GB iPad (A16) at PHP {v['launch']:,} on 2025-03-05; no reseller availability was claimed in that report.",
                "source_url": URL_GIZ, "source_kind": "historical_philippine_launch_price_report",
                "observed_at": "2025-03-05", "local_availability_verified": False,
                "availability_status": "historical_official_store_price_before_dated_reseller_availability"})
        prices.append({
            "device_id": DEVICE, "amount_php": v["current"], "configuration_id": v["id"],
            "configuration_match": f"exact_apple_ph_a16_{v['storage']}gb_{v['connectivity']}",
            "variant_storage_gb": v["storage"], "variant_connectivity": v["connectivity"],
            "price_type": "current_official_ph_store_list_price",
            "source_published_at": None,
            "excerpt": f"Apple Philippines' exact {v['label']} buy page lists PHP {v['current']:,}; observed {OBSERVED}. Stock/checkout was not verified.",
            "source_url": v["buyUrl"], "source_kind": "current_manufacturer_store_listing",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "listed_not_stock_verified"})
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Apple", "model_name": DEVICE_MODEL,
                    "category": "tablets", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": s["url"],
                       "source_kind": s["purpose"], "status": "reviewed", "result": s["note"]}
                      for s in common_sources(VARIANTS[0])],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    latest = json.loads(LATEST_REVIEWED.read_text(encoding="utf-8"))
    target = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if target:
        target["status"] = "manually_reviewed"
    existing = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type")) for p in latest.get("prices", [])}
    for p in prices:
        key = (p["device_id"], p["configuration_id"], p["price_type"])
        if key not in existing:
            latest.setdefault("prices", []).append(p)
            existing.add(key)
    latest["run_at"] = OBSERVED
    LATEST_REVIEWED.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"model": DEVICE_MODEL,
        "configurations": [{"id": v["id"], "modelNumber": v["modelCode"],
                            "label": v["label"], "historicalLaunchPricePhp": v["launch"],
                            "currentOfficialListPricePhp": v["current"]} for v in VARIANTS],
        "reviewedConfigurations": len(reviews), "reviewedFieldsPerConfiguration": 49,
        "sourceCountPerConfiguration": len(common_sources(VARIANTS[0])),
        "philippineAvailabilityReport": "2025-05-09; first dated reseller confirmation found",
        "image": "exact official model montage located; rights not established; placeholder retained",
        "unconfiguredCandidateReview": "archived; latest model-level observations remain unchanged",
        "studyScope": "Pending"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
