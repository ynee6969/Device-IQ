#!/usr/bin/env python3
"""Record source-backed field reviews for the ABC TECH X10 tablet family."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST_REVIEWED = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/abc-tech-x10-family-ph-prices-2026-11-27.json"

URL_X10 = "https://abctech.ph/products/abc-tech-x10"
URL_X10_PLUS = "https://abctech.ph/products/abc-tech-x10-plus"
URL_HOME = "https://abctech.ph/"
URL_LAUNCH = "https://abctech.ph/blogs/news/abc-tech-hub-grand-launching"
URL_GIZ = "https://www.gizguide.com/2023/08/abc-tech-x8-x10-x10plus-ph.html"
URL_UNBOX = "https://unboxdiaries.com/abc-tech-launches-new-x8-x10-and-x10-plus-tablets/"
URL_PHILSTAR = "https://www.philstar.com/gadgets/2023/08/31/2292766/review-filipino-made-educational-tablet-delivers-world-class-performance/amp"
URL_KEYBOARD = "https://abctech.ph/products/key-touch-docking-keyboard"

DEVICES = [
    {
        "deviceId": "device_2d3b3b3ff3d487", "row": 170, "workbookModel": "X10",
        "model": "X10 Study Buddy Tablet", "sku": "X10-CB-10I-464",
        "configId": "device_2d3b3b3ff3d487-4gb-64gb",
        "label": "4 GB RAM / 64 GB storage",
        "productUrl": URL_X10,
        "imageUrl": "https://cdn.shopify.com/s/files/1/0775/9314/9734/files/X10CHILD_2048x2048.jpg?v=1691222934",
        "price": 8499, "ram": 4, "storage": 64, "display": 10.1,
        "battery": 6000, "rear": 13, "dimensions": "235 × 155 mm; thickness not recorded",
        "launchCameraNote": "The manufacturer-published launch story and Unbox Diaries list 8MP front / 13MP rear; GIZGUIDE's table lists 5MP front, conflicting with its own launch summary and the manufacturer. The manufacturer's exact-model statement is retained with the secondary table discrepancy noted.",
    },
    {
        "deviceId": "device_01ffae05ba688a", "row": 171, "workbookModel": "X10+",
        "model": "X10 Plus Study Buddy Tablet", "sku": "X10P-CB-10I-8128",
        "configId": "device_01ffae05ba688a-8gb-128gb",
        "label": "8 GB RAM / 128 GB storage",
        "productUrl": URL_X10_PLUS,
        "imageUrl": "https://abctech.ph/cdn/shop/files/X10PLUSCHARCOALBLACK_1024x1024_crop_center.png?v=1743659254",
        "price": 11499, "ram": 8, "storage": 128, "display": 10.4,
        "battery": 7000, "rear": 13, "dimensions": "240 × 155 mm; thickness not recorded",
        "launchCameraNote": "The manufacturer-published launch story lists 8MP front / 13MP rear; GIZGUIDE's detailed table lists 5MP front, conflicting with its own launch summary and the manufacturer. The manufacturer's exact-model statement is retained with the secondary table discrepancy noted.",
    },
]


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      price_type: str | None = None, price_observed: str | None = None,
      listing_status: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
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


def nd(fid: str, sid: str, note: str) -> dict:
    return f(fid, sid, note, None, status="NOT_DISCLOSED", note=note)


def na(fid: str, sid: str, value: str, note: str) -> dict:
    return f(fid, sid, value, None, status="NOT_APPLICABLE", note=note)


def evidence(value: str, url: str, publisher: str, excerpt: str,
             config_match: str) -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": publisher,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": config_match,
            "reviewStatus": "CONFLICTING_INFORMATION"}


def conflict(fid: str, sid: str, description: str,
             candidates: list[dict], note: str, key: str | None = None) -> dict:
    row = f(fid, sid, description, None, status="CONFLICTING_INFORMATION",
            key=key, note=note)
    row["candidateEvidence"] = candidates
    return row


def sources_for(d: dict) -> list[dict]:
    x10 = d["workbookModel"] == "X10"
    product_id = "abc_x10_official_product" if x10 else "abc_x10p_official_product"
    model = d["model"]
    return [
        src(product_id, d["productUrl"], "ABC Tech Ventures Inc.",
            "Exact manufacturer product page, SKU, current list price and product configuration",
            f"Official ABC Tech Philippines page identifies {model}, manufacturer SKU {d['sku']},  {d['ram']}GB RAM / {d['storage']}GB storage, Android 12, a {d['display']}-inch TN/IPS display advertised at 1200×2000, 13MP rear and 8MP front cameras, {d['battery']}mAh battery, expandable storage (up to {'256' if x10 else '512'}GB), GPS, Wi-Fi and Bluetooth. It lists PHP {d['price']:,}, offers Add to Cart and Philippine shipping estimates; live stock/checkout was not verified."),
        src("abc_x10_home", URL_HOME, "ABC Tech Ventures Inc.",
            "Official brand catalog and cross-check of model naming, display, RAM/storage and battery",
            "The official home page lists separate X10 and X10 Plus models; X10 is shown as 10.1-inch / 4+64GB / 6,000mAh and X10 Plus as 10.4-inch / 8+128GB / 7,000mAh. The home page lists current store prices PHP 8,499 and PHP 11,499, respectively."),
        src("abc_x10_launch", URL_LAUNCH, "ABC Tech Ventures Inc. / MB TechNews",
            "Manufacturer-hosted Philippine release date and launch configuration",
            "The manufacturer-hosted story is dated 2023-07-28 and says ABC Tech released the X8, X10 and X10 Plus on July 28. It identifies the X10 as a 10.1-inch / 64GB tablet and the X10 Plus as a 10.4-inch / 128GB upgrade. It says the higher models have an 8MP front and 13MP rear camera. It does not state an international launch date or a launch price.", "2023-07-28"),
        src("abc_x10_gizguide", URL_GIZ, "GIZGUIDE",
            "Philippine launch-price and independent technical cross-check",
            "Published 2023-08-15. Reports launch-period prices of PHP 8,499 (X10) and PHP 11,499 (X10 Plus). Its X10 prose and table disagree on front camera (8MP vs 5MP); the table reports 1280×800 while the manufacturer says 1200×2000. Its X10 Plus prose and table disagree on chipset (T616 vs SC9863), GPU (Mali-G52 MP2 vs PowerVR GE8320), front camera (8MP vs 5MP), display size (10.4 vs 10-inch), and display pixels are 2000×1200. These internal disagreements are retained in review notes rather than silently collapsed.", "2023-08-15"),
        src("abc_x10_unbox", URL_UNBOX, "Unbox Diaries",
            "Independent Philippine launch coverage and configuration cross-check",
            "Published 2023-08-01. Reports X10 as 10.1-inch, 4GB/64GB, Android 12, 6,000mAh, 13MP rear / 8MP front, PHP 8,499; reports X10 Plus as 10.4-inch, 8GB/128GB, Android 12, 7,000mAh, 13MP rear / 8MP front, PHP 11,499. It does not provide exact product SKUs or display pixel resolution.", "2023-08-01"),
        src("abc_x10_philstar", URL_PHILSTAR, "Philstar.com",
            "Independent Philippine review and X10/X10 Plus model distinction",
            "Published 2023-08-31. Reviews the ABC Tech X10 at PHP 8,499 and identifies its 10.1-inch / 64GB configuration; distinguishes the X10 Plus as the larger 10.4-inch / 128GB model. The review does not verify the exact manufacturer SKU.", "2023-08-31"),
        src("abc_x10_keyboard", URL_KEYBOARD, "ABC Tech Ventures Inc.",
            "Exact tablet compatibility for the optional docking-keyboard accessory",
            "Official Key Touch Docking Keyboard page (SKU DK-BK-X10) explicitly offers selectable ABC TECH X10 and X10 Plus sizes. This verifies a compatible keyboard accessory, not that a keyboard is included with every tablet sale."),
    ]


def field_rows(d: dict) -> list[dict]:
    x10 = d["workbookModel"] == "X10"
    product = "abc_x10_official_product" if x10 else "abc_x10p_official_product"
    launch_price_source = "abc_x10_gizguide"
    match = d["configId"]
    rows = [
        f("model_number", product, f"Manufacturer SKU {d['sku']}", d["sku"], status="VERIFIED",
          note="Official product page identifies this exact SKU. The workbook has no regulatory model number; SKU is retained as the manufacturer identifier."),
        nd("global_release_date", product, "A global/international first-release date was not found. The dated evidence establishes the Philippine release only."),
        f("configuration", product, d["label"], d["label"], status="VERIFIED",
          note="Memory configuration is stated on the exact official SKU page and is kept separate from the X10 Plus record."),
        f("philippine_release_date", "abc_x10_launch", "Released in the Philippines on July 28, 2023", "2023-07-28",
          status="VERIFIED_SECONDARY", note="The manufacturer-hosted Philippine launch story explicitly states ABC Tech released the X8, X10 and X10 Plus on July 28, 2023.", unit="date"),
        f("official_launch_price_php", launch_price_source,
          f"PHP {d['price']:,} reported in 2023 Philippine launch coverage", d["price"],
          status="VERIFIED_SECONDARY", unit="PHP",
          note="Launch-period price reported by Philippine coverage published 2023-08-15 and independently corroborated by Unbox Diaries (2023-08-01). The manufacturer-hosted release story does not state a launch price; this is not represented as a directly sourced manufacturer announcement."),
        f("current_price_php", product, f"PHP {d['price']:,} listed on the official ABC Tech Philippines product page", d["price"],
          status="VERIFIED", unit="PHP", price_type="Official Philippine manufacturer-store list price",
          price_observed=OBSERVED, listing_status="Not verified",
          note=f"Observed {OBSERVED} on the official exact-SKU page. Add to Cart and Philippine delivery estimates are shown; current stock and checkout completion were not verified."),
        f("display_size", product, f"{d['display']}-inch display", d["display"], key="displayInches", unit="in",
          note="The exact manufacturer product page and manufacturer-hosted launch story agree on this marketed diagonal; Unbox Diaries independently reports the same size."),
        conflict("display_technology", product, "Manufacturer wording: TN/IPS; Philippine coverage describes IPS",
                 [evidence("TN/IPS", d["productUrl"], "ABC Tech Ventures Inc.", "The exact product description labels the panel ‘TN/IPS’.", match),
                  evidence("IPS", URL_GIZ, "GIZGUIDE", "The Philippine specifications describe an LCD IPS panel.", match),
                  evidence("IPS", URL_UNBOX, "Unbox Diaries", "The launch coverage describes an IPS display.", match)],
                 "The manufacturer uses an ambiguous TN/IPS label while Philippine coverage calls it IPS. Exact panel technology is unresolved; no normalized panel type is asserted.", key="displayType"),
    ]
    if x10:
        rows.append(conflict("display_resolution", product,
            "Manufacturer lists 1200×2000; GIZGUIDE table lists 1280×800",
            [evidence("1200×2000", URL_X10, "ABC Tech Ventures Inc.", "Exact-SKU description states 10.1-inch 1200×2000 TN/IPS.", match),
             evidence("1280×800", URL_GIZ, "GIZGUIDE", "2023 technical table states 10-inch 1280×800 HD+ IPS.", match)],
            "The primary product page and a contemporaneous Philippine specification table disagree on pixel dimensions. Leave resolution blank pending an exact-SKU specification sheet.", key="resolution"))
    else:
        rows.append(f("display_resolution", product, "1200×2000 pixels (manufacturer orientation)", "1200x2000",
            status="VERIFIED", key="resolution",
            note="Official exact-SKU description gives 1200×2000. GIZGUIDE's table lists 2000×1200, the same pixel dimensions in reversed orientation; no different count is asserted."))
    rows += [
        nd("display_refresh_rate", product, "No refresh-rate value is stated on the reviewed exact-SKU or Philippine launch sources."),
        nd("display_brightness", product, "No numeric brightness value is stated on the reviewed exact-SKU or Philippine launch sources."),
        nd("display_protection", product, "The reviewed sources do not identify a screen-glass protection brand or standard."),
    ]
    if x10:
        rows += [
            f("chipset", "abc_x10_gizguide", "MediaTek MT6762 / Helio P22 octa-core", "MediaTek MT6762 (Helio P22)", status="VERIFIED_SECONDARY", key="chipset",
              note="GIZGUIDE identifies MT6762/Helio P22 for the X10. The manufacturer's product page does not name the chipset."),
            f("process_node", "abc_x10_gizguide", "12nm process reported for MT6762", 12, status="VERIFIED_SECONDARY", unit="nm",
              note="Reported in the model-specific Philippine technical table; manufacturer does not state the tablet's chip process."),
            f("cpu", "abc_x10_gizguide", "MT6762 8-core, up to 2.0GHz", "Octa-core up to 2.0GHz", status="VERIFIED_SECONDARY", key="cpu"),
            f("gpu", "abc_x10_gizguide", "PowerVR GE8320", "PowerVR GE8320", status="VERIFIED_SECONDARY", key="gpu"),
        ]
    else:
        rows += [
            f("chipset", product, "T616 octa-core solution", "UNISOC T616", status="VERIFIED", key="chipset",
              note="The exact manufacturer product page identifies the T616. GIZGUIDE's introductory summary agrees, but its detailed table says SC9863; the conflicting secondary table value is documented in the source notes and not substituted for the exact-SKU manufacturer value."),
            nd("process_node", product, "The exact tablet page does not state a chip process node; secondary descriptions of the T616 family were not treated as proof of this configuration."),
            f("cpu", product, "T616 octa-core solution; core layout and clock speed not stated", "Octa-core; core layout and frequency not recorded", status="VERIFIED", key="cpu"),
            conflict("gpu", "abc_x10_gizguide", "GIZGUIDE reports Mali-G52 MP2 in its summary but PowerVR GE8320 in its detailed table",
                [evidence("Mali-G52 MP2", URL_GIZ, "GIZGUIDE", "Introductory model summary attributes Mali-G52 MP2 to T616.", match),
                 evidence("PowerVR GE8320", URL_GIZ, "GIZGUIDE", "Detailed X10 Plus table attributes PowerVR GE8320 to SC9863.", match)],
                "The official tablet page does not name a GPU, and the Philippine coverage is internally contradictory. Leave the device GPU blank.", key="gpu"),
        ]
    rows += [
        f("operating_system", product, "Android 12", "Android 12", key="os"),
        nd("os_support", product, "No guaranteed Android-version or security-update policy was found for this exact SKU."),
        f("ram_capacity", product, f"{d['ram']}GB RAM", d["ram"], key="ramGb", unit="GB"),
        nd("ram_type", product, "The exact tablet RAM generation/type is not stated in reviewed sources."),
        f("storage_capacity", product, f"{d['storage']}GB internal storage", d["storage"], key="storageGb", unit="GB"),
        nd("storage_type", product, "The exact installed flash-storage type is not stated; platform capabilities are not treated as proof of device configuration."),
        f("storage_expansion", product, f"Expandable storage up to {'256' if x10 else '512'}GB", f"microSD expansion up to {'256' if x10 else '512'} GB", status="VERIFIED", key="storageExpansion",
          note="Maximum expansion is stated on the exact official product page; the precise card format and whether the slot is shared are not stated."),
        f("rear_camera_system", product, "13MP rear camera", "13 MP rear camera", key="rearCameraMp", unit="MP"),
        nd("main_camera_sensor", product, "Camera sensor make/model and lens aperture are not stated in reviewed sources."),
        na("ultrawide_camera", "abc_x10_launch", "Not applicable to the documented one-rear-camera system", "Manufacturer-hosted launch coverage describes the higher X10 models as having dual cameras: one front-facing and one rear-facing. No separate ultrawide module is listed."),
        na("telephoto_camera", "abc_x10_launch", "Not applicable to the documented one-rear-camera system", "Manufacturer-hosted launch coverage describes the higher X10 models as having dual cameras: one front-facing and one rear-facing. No separate telephoto module is listed."),
        f("front_camera", product, "8MP front camera", 8, key="frontCameraMp", unit="MP", note=d["launchCameraNote"]),
        nd("video_recording", product, "Supported camera recording resolutions and frame rates are not published in the reviewed sources."),
        f("battery_capacity", product, f"{d['battery']}mAh, 3.7V", d["battery"], key="batteryMah", unit="mAh"),
        nd("battery_technology", product, "Battery chemistry, rated watt-hours and removability are not stated."),
        f("wired_charging", "abc_x10_gizguide", "10W standard charging", 10, status="VERIFIED_SECONDARY", key="chargingW", unit="W"),
        nd("wireless_charging", product, "Wireless or reverse charging is not listed in the reviewed exact-SKU specifications."),
        f("dimensions", product, d["dimensions"], d["dimensions"], key="dimensions", unit="mm",
          note="Official page gives height and width only. Thickness and orientation of the second manufacturer axis are not further specified."),
        nd("weight", product, "Exact-SKU weight is not published in the reviewed sources."),
        nd("materials", product, "Frame and rear-cover composition are not identified. Descriptions of finish are not treated as material evidence."),
        nd("ingress_protection", "abc_x10_launch", "No IP rating or standardized ingress-protection test/certification is given. The manufacturer-hosted launch story uses waterproof/dustproof language without a rating."),
        f("sim_esim", "abc_x10_gizguide", "Dual-SIM 4G LTE reported; eSIM not recorded", "Dual SIM; eSIM not recorded", status="VERIFIED_SECONDARY", key="sim"),
        nd("cellular_bands", "abc_x10_gizguide", "Philippine coverage reports 4G LTE but does not list supported LTE frequency bands."),
        f("wifi", "abc_x10_gizguide", "Wi-Fi 4 (802.11 b/g/n) reported", "Wi-Fi 4 (802.11 b/g/n)", status="VERIFIED_SECONDARY", key="wifi"),
        f("bluetooth", "abc_x10_gizguide", "Bluetooth 5.0 reported", "Bluetooth 5.0", status="VERIFIED_SECONDARY"),
        f("usb", "abc_x10_gizguide", "USB Type-C connector; data protocol not stated", "USB Type-C; data protocol not recorded", status="VERIFIED_SECONDARY", key="ports"),
        nd("nfc", product, "NFC is not listed in the exact-SKU or reviewed Philippine specifications."),
        f("gnss", product, "GPS", "GPS", status="VERIFIED", note="GPS is stated on the exact product page; other satellite constellations are not specified."),
        f("audio", "abc_x10_gizguide", "Built-in speaker/microphone and 3.5mm audio jack reported", "Built-in speaker and microphone; 3.5mm audio jack", status="VERIFIED_SECONDARY", key="sound"),
        f("sensors", "abc_x10_gizguide", "Accelerometer, light, orientation, proximity, gyroscope, sound and magnetic sensors reported", "Accelerometer; light; orientation; proximity; gyroscope; sound; magnetic", status="VERIFIED_SECONDARY"),
        nd("tablet_stylus", product, "Dedicated active-stylus support and a compatible stylus are not identified on the exact product page."),
        f("tablet_keyboard", "abc_x10_keyboard", "Optional Key Touch Docking Keyboard DK-BK-X10 has separate X10 and X10 Plus fit options", "Optional compatible DK-BK-X10 docking keyboard; not confirmed included", status="VERIFIED", key="keyboard",
          note="Official accessory page lists ABC TECH X10 and X10 Plus as separate selectable fits. It does not establish that the keyboard is bundled with the tablet."),
        f("tablet_cellular_variant", "abc_x10_gizguide", "4G LTE dual-SIM configuration reported; no separate Wi-Fi-only SKU located", "4G LTE dual-SIM reported; Wi-Fi-only variant not located", status="VERIFIED_SECONDARY", key="cellular"),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct tablet field reviews, got {len(rows)}")
    return rows


def make_review(d: dict) -> dict:
    product = "abc_x10_official_product" if d["workbookModel"] == "X10" else "abc_x10p_official_product"
    replacement = {"id": d["configId"], "label": d["label"], "sku": d["sku"],
                   "modelCode": d["sku"],
                   "notes": "Manufacturer SKU from ABC Tech's official exact product page; eligibility remains Pending."}
    return {
        "deviceId": d["deviceId"], "configurationId": d["configId"],
        "brand": "ABC TECH", "model": d["model"], "configuration": d["label"],
        "configurationLabel": d["label"], "modelCode": d["sku"], "sku": d["sku"],
        "replacementVariants": [replacement], "replaceUnrecordedPlaceholder": True,
        "sources": sources_for(d), "fields": field_rows(d),
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": f"Philippine release verified from the manufacturer-hosted 2023 launch story and an exact ABC Tech Philippines store SKU. Current list price PHP {d['price']:,} was observed {OBSERVED}; stock/checkout not confirmed.",
            "philippineAvailability": f"ABC Tech's manufacturer-hosted Philippine story states this model was released July 28, 2023. Exact official Philippine store listing observed {OBSERVED}.",
            "observedAt": OBSERVED,
            "qualityFlag": "Manually reviewed; exact manufacturer SKU, memory configuration and Philippine launch date verified. Manufacturer store list price dated; stock not checked. Display/camera/source discrepancies remain documented; eligibility remains Pending.",
            "catalogModel": d["model"], "manufacturer": "ABC Tech Ventures Inc.",
            "productLine": "Study Buddy", "modelNumber": d["sku"],
            "philippineReleaseYear": 2023,
            "philippineDateLabel": "Manufacturer-reported Philippine release date",
            "researchNotes": f"Workbook row {d['row']} ({d['workbookModel']}) is matched to ABC Tech Ventures Inc. {d['model']} exact manufacturer SKU {d['sku']} ({d['label']}). It remains a distinct device from the {'X10 Plus' if d['workbookModel'] == 'X10' else 'X10'} and retains study scope Pending. Philippine release is stated as 2023-07-28 in the manufacturer-hosted story. The current exact-SKU page lists PHP {d['price']:,}; checkout/stock not confirmed. Conflicts or source inconsistencies are explicitly retained in per-field evidence. The official product image is an exact-model match but its reuse permission is undocumented, so a neutral placeholder remains.",
            "openIssues": [
                {"issue": "Study eligibility remains Pending", "action": "Preserve the workbook's selected scope until study screening rules are applied."},
                {"issue": "Official product page lists a current price but stock/checkout is not confirmed", "action": "Keep the dated list price without representing the tablet as in stock."},
                {"issue": "The product image's reuse/license terms are undocumented", "action": "Keep the neutral placeholder and record the exact official image URL for rights review."},
                {"issue": "Manufacturer and local sources disagree or use ambiguous wording on some specifications", "action": "Use exact-SKU primary evidence where clear; leave truly conflicting normalized values blank and retain candidate evidence."},
            ],
        },
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    reviews = [make_review(d) for d in DEVICES]
    for review, d in zip(reviews, DEVICES):
        device = next((x for x in catalog if x.get("id") == d["deviceId"]), None)
        if not device or device.get("scopeStatus") != "Pending":
            raise ValueError(f"Expected workbook's pending ABC TECH {d['workbookModel']} tablet; refusing unexpected scope/device.")
        if len(device.get("variants", [])) != 1 or device["variants"][0]["id"] != f"{d['deviceId']}-unrecorded":
            raise ValueError(f"Expected one unrecorded placeholder configuration for {d['deviceId']}.")
        add_review(manual, catalog, review)
    target_keys = {(d["deviceId"], d["configId"]) for d in DEVICES}
    deduplicate_target_reviews(manual, target_keys)
    for d in DEVICES:
        saved = next(r for r in manual["records"]
                     if (r.get("deviceId"), r.get("configurationId")) == (d["deviceId"], d["configId"]))
        saved.update({"model": d["model"], "configuration": d["label"],
                      "configurationLabel": d["label"], "sku": d["sku"],
                      "modelCode": d["sku"]})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    for d in DEVICES:
        images[d["deviceId"]] = {
            "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
            "reason": "An exact-model image is linked from ABC Tech's official product page, but no image reuse license, credit requirement or permission to republish/hotlink is documented. Keep the neutral placeholder.",
            "sourcePage": d["productUrl"], "assetUrl": None,
            "candidateAssetUrl": d["imageUrl"],
            "scope": f"Exact official ABC TECH {d['model']} charcoal-black product image associated with SKU {d['sku']} through its official product page.",
            "rightsTermsUrl": None,
            "rightsCheck": "Reviewed the official exact-SKU page and linked image. No reuse permission or license was located. Do not download or hotlink.",
            "rightsCheckSourcePage": d["productUrl"], "observedAt": OBSERVED,
            "altText": f"Image unavailable for ABC TECH {d['model']}",
        }
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for d in DEVICES:
        prices.extend([
            {"device_id": d["deviceId"], "amount_php": d["price"],
             "configuration_id": d["configId"],
             "configuration_match": f"exact_ph_abc_tech_{d['workbookModel'].lower().replace('+', 'plus')}_{d['sku'].lower()}_{d['ram']}gb_{d['storage']}gb",
             "variant_ram_gb": d["ram"], "variant_storage_gb": d["storage"],
             "price_type": "historical_ph_launch_price_reported",
             "source_published_at": "2023-08-15",
             "excerpt": f"GIZGUIDE reports PHP {d['price']:,} for ABC TECH {d['workbookModel']} in Philippine launch coverage published 2023-08-15; Unbox Diaries independently reports the same amount on 2023-08-01.",
             "source_url": URL_GIZ, "source_kind": "historical_local_launch_price_report",
             "observed_at": "2023-08-15", "local_availability_verified": True,
             "availability_status": "historical_launch_price_not_current"},
            {"device_id": d["deviceId"], "amount_php": d["price"],
             "configuration_id": d["configId"],
             "configuration_match": f"exact_official_sku_{d['sku'].lower()}_{d['ram']}gb_{d['storage']}gb",
             "variant_ram_gb": d["ram"], "variant_storage_gb": d["storage"],
             "price_type": "current_official_ph_product_page_list_price",
             "source_published_at": None,
             "excerpt": f"ABC Tech exact SKU {d['sku']} product page lists PHP {d['price']:,} and shows Add to Cart on {OBSERVED}; stock/checkout was not verified.",
             "source_url": d["productUrl"], "source_kind": "current_manufacturer_store_listing",
             "observed_at": OBSERVED, "local_availability_verified": True,
             "availability_status": "listed_not_stock_verified"},
        ])
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 2,
        "models": [{"device_id": d["deviceId"], "brand": "ABC TECH",
                    "model_name": d["model"], "category": "tablets",
                    "status": "manually_reviewed"} for d in DEVICES],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": d["deviceId"], "source_url": s["url"],
                       "source_kind": s["purpose"], "status": "reviewed", "result": s["note"]}
                      for d, review in zip(DEVICES, reviews) for s in review["sources"]],
        "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    latest = json.loads(LATEST_REVIEWED.read_text(encoding="utf-8"))
    for d in DEVICES:
        target = next((row for row in latest.get("models", []) if row.get("device_id") == d["deviceId"]), None)
        if target:
            target["status"] = "manually_reviewed"
    existing_price_keys = {(p.get("device_id"), p.get("configuration_id"), p.get("price_type")) for p in latest.get("prices", [])}
    for p in prices:
        key = (p["device_id"], p["configuration_id"], p["price_type"])
        if key not in existing_price_keys:
            latest.setdefault("prices", []).append(p)
            existing_price_keys.add(key)
    latest["run_at"] = OBSERVED
    LATEST_REVIEWED.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = []
    for review, d in zip(reviews, DEVICES):
        counts: dict[str, int] = {}
        for row in review["fields"]:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        result.append({"workbookRow": d["row"], "model": d["model"],
                       "manufacturerSku": d["sku"], "configuration": d["label"],
                       "reviewedFields": len(review["fields"]), "fieldStatuses": counts,
                       "sources": len(review["sources"]), "philippineReleaseDate": "2023-07-28",
                       "historicalLaunchPricePhp": d["price"], "currentOfficialListPricePhp": d["price"],
                       "stock": "not verified", "image": "exact official image located; rights not established; placeholder retained",
                       "studyScope": "Pending"})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
