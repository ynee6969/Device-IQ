#!/usr/bin/env python3
"""Record source-backed review for the ABC TECH X8 Study Buddy tablet."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_87e79ad13fe93b"
CONFIG = f"{DEVICE}-2gb-32gb"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST_REVIEWED = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/abc-tech-x8-ph-prices-2026-11-27.json"

URL_PRODUCT = "https://abctech.ph/products/abc-tech-x8"
URL_HOME = "https://abctech.ph/"
URL_LAUNCH = "https://abctech.ph/blogs/news/abc-tech-hub-grand-launching"
URL_GIZ = "https://www.gizguide.com/2023/08/abc-tech-x8-x10-x10plus-ph.html"
URL_UNBOX = "https://unboxdiaries.com/abc-tech-launches-new-x8-x10-and-x10-plus-tablets/"
URL_MB = "https://www.curlydianne.com/2023/07/abc-tech-affordable-tablets/"
URL_PHILSTAR = "https://qa.philstar.com/business/technology/2023/05/19/2267477/ndc-taps-filipino-tablet-provider-digitize-pinoy-students/amp"
URL_UNISOC = "https://www.unisoc.com/en/product/SmartPhone/9863A"
IMAGE_URL = "https://abctech.ph/cdn/shop/files/X8CHARCOALBLACK_1024x1024_crop_center.png?v=1743659224"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("abc_x8_official_product", URL_PRODUCT, "ABC Tech Ventures Inc.",
        "Manufacturer product page, exact model/SKU, current listing price and primary specifications",
        "The ABC Tech product page identifies ABC TECH X8 Study Buddy Tablet, SKU X8-CB-8I-232, current listed price PHP 4,899, 8-inch display, 2GB RAM, 32GB storage, 9863 octa-core solution, Android 12, 800×1280 TN/IPS display, GPS, 5MP front camera, 8MP rear camera, 4000mAh battery and 195×120mm body dimensions (thickness not given). Add-to-cart is shown; stock/checkout was not confirmed."),
    src("abc_x8_official_home", URL_HOME, "ABC Tech Ventures Inc.",
        "Official brand identity, catalog and Philippine selling channels",
        "Official site advertises ABC TECH X8 with an 8-inch IPS display, 2GB+32GB and 4000mAh; lists the X8 at PHP 4,899 and offers delivery to NCR, Luzon, Visayas and Mindanao. The site's second product description says TN/IPS, so display type remains unresolved."),
    src("abc_x8_official_launch", URL_LAUNCH, "ABC Tech Ventures Inc. / MB TechNews",
        "Manufacturer-published Philippine product launch and launch configuration",
        "Company blog dated 2023-07-28 says ABC Tech released its X8, X10 and X10 Plus tablet line on July 28. It identifies X8 as 8 inches, 32GB storage, 8MP rear and 5MP front camera. It is a company-hosted launch story authored by MB TechNews.", "2023-07-28"),
    src("abc_x8_gizguide_ph", URL_GIZ, "GIZGUIDE",
        "Contemporaneous Philippine price and technical cross-check",
        "Article dated 2023-08-15 reports the X8 at PHP 5,999, 8-inch IPS panel, 1920×1200 resolution, UNISOC SC9863, 2GB/32GB, 4000mAh with 10W charge, Android 12, Wi-Fi 4, 4G LTE, Bluetooth 5.0, dual SIM, USB-C, headphone jack and listed sensors. Its reported pixel resolution conflicts with the manufacturer's current 800×1280 product description.", "2023-08-15"),
    src("abc_x8_unbox_ph", URL_UNBOX, "Unbox Diaries",
        "Independent Philippine launch, configuration and price cross-check",
        "Article dated 2023-08-01 reports the ABC Tech X8 at 8 inches, IPS, 2GB/32GB, Android 12, 4000mAh, 8MP rear, 5MP front and PHP 5,999. It does not publish exact display pixels or a model SKU.", "2023-08-01"),
    src("abc_x8_mb_launch", URL_MB, "Curlydianne / MB TechNews",
        "Philippine launch story and exact camera/configuration cross-check",
        "Article dated 2023-07-30 identifies ABC Tech Ventures Inc. and the X8 as its newly launched 8-inch, 32GB tablet with 8MP rear and 5MP front camera. It does not provide a model SKU or full hardware table.", "2023-07-30"),
    src("abc_x8_company_philstar", URL_PHILSTAR, "Philstar.com",
        "Independent company and Philippine-market identity verification",
        "Philstar's 2023-05-19 profile identifies ABC Tech Ventures, its tablet business and Philippine educational-market activity. It says the brand planned a July release of its then-new general-public tablet line. This company-level coverage does not independently specify the X8 hardware.", "2023-05-19"),
    src("abc_x8_unisoc_chipset", URL_UNISOC, "UNISOC",
        "Primary chipset specification cross-check",
        "UNISOC's official SC9863A page lists an octa-core Cortex-A55 CPU up to 1.6GHz, 28nm process options, PowerVR GE8322 GPU, LPDDR3/LPDDR4X support, eMMC 5.1 support, LTE, GNSS, Wi-Fi b/g/n and Bluetooth 4.2. These are component capabilities, not proof that every option or radio is configured in the X8."),
]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      catalog_value=None, price_type: str | None = None,
      price_observed: str | None = None, price_condition: str | None = None,
      listing_status: str | None = None) -> dict:
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
                    "priceCondition": price_condition or "new"})
    if listing_status:
        row["listingStatus"] = listing_status
    return row


def nd(fid: str, sid: str, description: str, note: str | None = None) -> dict:
    return f(fid, sid, description, None, status="NOT_DISCLOSED",
             note=note or "The reviewed exact-model sources do not publish this value; it remains blank rather than inferred.")


def na(fid: str, sid: str, description: str, note: str) -> dict:
    return f(fid, sid, description, None, status="NOT_APPLICABLE", note=note)


def ev(value: str, url: str, source_kind: str, excerpt: str, match: str) -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": match, "reviewStatus": "CONFLICTING_INFORMATION"}


def conflict(fid: str, sid: str, description: str, evidence: list[dict], note: str,
             key: str | None = None) -> dict:
    row = f(fid, sid, description, None, status="CONFLICTING_INFORMATION",
            key=key, catalog_value=None, note=note)
    row["candidateEvidence"] = evidence
    return row


def fields() -> list[dict]:
    resolution = conflict(
        "display_resolution", "abc_x8_official_product",
        "The manufacturer's product page states 800×1280; GIZGUIDE reports 1920×1200 for the X8.",
        [ev("800 × 1280", URL_PRODUCT, "manufacturer_primary", "Official product description: 8.0-inch 800x1280 TN/IPS display.", "X8-CB-8I-232 product listing"),
         ev("1920 × 1200", URL_GIZ, "secondary_philippines", "GIZGUIDE X8 specifications list FHD 1920 x 1200.", "ABC TECH X8 launch article")],
        "The direct product page and 2023 launch coverage disagree on exact pixel dimensions. No resolution is published to the catalog until the exact panel is independently verified.", key="resolution")
    display_type = conflict(
        "display_technology", "abc_x8_official_product",
        "ABC Tech's product description says TN/IPS; the same brand homepage and Philippine launch coverage call the screen IPS.",
        [ev("TN/IPS (unspecified panel type)", URL_PRODUCT, "manufacturer_primary", "The official X8 page says 800x1280 TN/IPS display.", "X8-CB-8I-232 product listing"),
         ev("IPS", URL_HOME, "manufacturer_primary", "ABC Tech homepage promotes the X8 as an 8-inch IPS display.", "X8 product tile"),
         ev("IPS", URL_GIZ, "secondary_philippines", "GIZGUIDE reports an 8-inch IPS screen.", "ABC TECH X8 launch article")],
        "The company publishes both a combined TN/IPS description and an IPS-only tile. The exact panel technology for SKU X8-CB-8I-232 is not resolved.", key="displayType")
    rows = [
        f("model_number", "abc_x8_official_product", "Manufacturer SKU X8-CB-8I-232", "X8-CB-8I-232", status="VERIFIED",
          note="This is the official merchant SKU printed on the manufacturer's X8 product page; no separate regulatory model number was found."),
        f("global_release_date", "abc_x8_official_launch", "ABC Tech states the X8 line was released in the Philippines on 2023-07-28", "2023-07-28", status="VERIFIED",
          note="The manufacturer-hosted announcement is the product's first documented release date; no separate earlier foreign-market launch was found."),
        f("configuration", "abc_x8_official_product", "2GB RAM / 32GB storage", "2 GB RAM / 32 GB storage",
          note="The official X8 SKU page and launch reports identify 2GB RAM and 32GB storage; no alternate memory configuration is attached to this workbook record."),
        f("philippine_release_date", "abc_x8_official_launch", "ABC Tech's manufacturer-hosted announcement reports its X8 line released on 2023-07-28", "2023-07-28", status="VERIFIED",
          note="Manufacturer-hosted Philippine release announcement dated 2023-07-28; the same line also appears in Philippine launch coverage."),
        f("official_launch_price_php", "abc_x8_gizguide_ph", "PHP 5,999 reported for ABC TECH X8 at Philippine launch", 5999, status="VERIFIED_SECONDARY", unit="PHP",
          price_type="Historical Philippine launch price", price_observed="2023-08-15",
          note="GIZGUIDE and Unbox Diaries both reported PHP 5,999 in their 2023 launch coverage. This is a historical launch price, not today's listing."),
        f("current_price_php", "abc_x8_official_product", "Official ABCTechph product page lists PHP 4,899 for SKU X8-CB-8I-232; add-to-cart is shown, but checkout stock was not verified", 4899, status="VERIFIED", unit="PHP",
          price_type="Current official Philippine manufacturer-store list price", price_observed=OBSERVED,
          note="Observed on 2026-11-27 on ABC Tech's official exact-SKU page. Page shows Add to Cart and nationwide delivery estimates; actual stock/checkout completion was not verified.", listing_status="Not verified"),
        f("display_size", "abc_x8_official_product", "8.0-inch tablet display", 8.0, key="displayInches", unit="in"),
        display_type,
        resolution,
        nd("display_refresh_rate", "abc_x8_official_product", "No refresh-rate value is stated on the official product page or reviewed Philippine launch sources."),
        nd("display_brightness", "abc_x8_official_product", "No numeric display brightness value is published in the reviewed X8 sources."),
        nd("display_protection", "abc_x8_official_product", "No named display cover-glass protection is stated on the reviewed X8 sources."),
        f("chipset", "abc_x8_unisoc_chipset", "Manufacturer lists a 9863 octa-core solution; GIZGUIDE identifies it as UNISOC SC9863", "UNISOC SC9863", key="chipset", status="VERIFIED_SECONDARY",
          note="ABC Tech's official page says 9863; the Philippine launch report identifies the component as UNISOC SC9863. The exact suffix/revision is not stated for the tablet SKU."),
        f("process_node", "abc_x8_unisoc_chipset", "UNISOC SC9863A process options include 28nm HPC+; GIZGUIDE reports 28nm for the X8", 28, unit="nm", status="VERIFIED_SECONDARY",
          note="The chipset manufacturer's page lists 28nm HPC+/22nm process options for the SC9863A family; local X8 coverage reports 28nm. The tablet source identifies 9863 without a suffix."),
        f("cpu", "abc_x8_unisoc_chipset", "Octa-core Arm Cortex-A55, up to 1.6GHz", "8x Cortex-A55 up to 1.6GHz", key="cpu", status="VERIFIED_SECONDARY"),
        f("gpu", "abc_x8_unisoc_chipset", "Imagination PowerVR GE8322, up to 550MHz", "PowerVR GE8322", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", "abc_x8_official_product", "Android 12", "Android 12", key="os"),
        nd("os_support", "abc_x8_official_product", "No published X8 OS/security update schedule or guaranteed support period was found."),
        f("ram_capacity", "abc_x8_official_product", "2GB RAM", 2, key="ramGb", unit="GB"),
        nd("ram_type", "abc_x8_unisoc_chipset", "The chipset supports multiple memory types, but the X8 SKU's actual RAM type is not disclosed."),
        f("storage_capacity", "abc_x8_official_product", "32GB storage", 32, key="storageGb", unit="GB"),
        nd("storage_type", "abc_x8_official_product", "The official X8 page does not identify the installed flash-storage type; chipset storage support is not treated as proof of device configuration."),
        nd("storage_expansion", "abc_x8_official_product", "MicroSD/expandable storage support and maximum capacity are not stated on the reviewed exact-SKU page."),
        f("rear_camera_system", "abc_x8_official_product", "Single 8MP rear camera", "8 MP rear camera", key="rearCameraMp", catalog_value=8, unit="MP"),
        nd("main_camera_sensor", "abc_x8_official_product", "The camera sensor supplier and exact sensor part number are not disclosed."),
        na("ultrawide_camera", "abc_x8_official_launch", "The official launch story identifies one 8MP rear camera and does not list an ultrawide module.", "Not applicable to the documented single-camera rear system; no ultrawide camera is listed."),
        na("telephoto_camera", "abc_x8_official_launch", "The official launch story identifies one 8MP rear camera and does not list a telephoto module.", "Not applicable to the documented single-camera rear system; no telephoto camera is listed."),
        f("front_camera", "abc_x8_official_product", "5MP front camera", 5, key="frontCameraMp", unit="MP"),
        nd("video_recording", "abc_x8_official_product", "The reviewed X8 product sources do not state supported camera recording resolutions or frame rates."),
        f("battery_capacity", "abc_x8_official_product", "3.7V 4000mAh battery", 4000, key="batteryMah", unit="mAh"),
        nd("battery_technology", "abc_x8_official_product", "Battery chemistry and removability are not identified in the official product specification."),
        f("wired_charging", "abc_x8_gizguide_ph", "10W standard charging reported by GIZGUIDE", 10, key="chargingW", unit="W", status="VERIFIED_SECONDARY"),
        nd("wireless_charging", "abc_x8_official_product", "Wireless or reverse charging is not listed in the reviewed X8 sources."),
        f("dimensions", "abc_x8_official_product", "195mm high × 120mm wide; thickness not recorded", "195 × 120 × thickness not recorded", key="dimensions", unit="mm"),
        nd("weight", "abc_x8_official_product", "The official X8 page and Philippine launch sources do not publish device weight."),
        nd("materials", "abc_x8_official_product", "The frame and rear-cover material composition is not stated in the reviewed product sources."),
        nd("ingress_protection", "abc_x8_official_launch", "The launch story uses general water/dust-durability language for the tablet line but does not publish an IP rating or standardized test basis."),
        f("sim_esim", "abc_x8_gizguide_ph", "Dual-SIM LTE tablet reported; eSIM is not recorded", "Dual SIM; eSIM not recorded", key="sim", status="VERIFIED_SECONDARY"),
        nd("cellular_bands", "abc_x8_gizguide_ph", "4G LTE is reported, but the X8 SKU's supported LTE frequency bands are not published in the reviewed sources."),
        f("wifi", "abc_x8_gizguide_ph", "Wi-Fi 4 (802.11 b/g/n) reported; the official page says Wi-Fi", "Wi-Fi 4 (802.11 b/g/n)", key="wifi", status="VERIFIED_SECONDARY"),
        f("bluetooth", "abc_x8_gizguide_ph", "Bluetooth 5.0 reported in Philippine launch specifications", "Bluetooth 5.0", status="VERIFIED_SECONDARY",
          note="GIZGUIDE reports Bluetooth 5.0. UNISOC lists Bluetooth 4.2 as a chipset capability; an external radio implementation could differ, so the chipset sheet alone is not used to override the tablet listing."),
        f("usb", "abc_x8_gizguide_ph", "USB Type-C connector; data version is not recorded", "USB Type-C; data version not recorded", key="ports", status="VERIFIED_SECONDARY"),
        nd("nfc", "abc_x8_official_product", "NFC is not listed on the official X8 product page or reviewed launch specifications."),
        f("gnss", "abc_x8_official_product", "GPS supported; other satellite systems are not listed", "GPS; other systems not recorded", status="VERIFIED_SECONDARY"),
        f("audio", "abc_x8_gizguide_ph", "Built-in speakers and microphones; 3.5mm audio jack", "Built-in speakers and microphone; 3.5mm audio jack", key="sound", status="VERIFIED_SECONDARY"),
        f("sensors", "abc_x8_gizguide_ph", "Accelerometer, light, orientation, proximity, gyroscope, sound and magnetic sensors reported", "Accelerometer; light; orientation; proximity; gyroscope; sound; magnetic", status="VERIFIED_SECONDARY"),
        nd("tablet_stylus", "abc_x8_official_product", "No dedicated active-stylus support or compatible pen is specified on the exact X8 product page."),
        nd("tablet_keyboard", "abc_x8_official_product", "The brand sells general keyboard accessories, but exact X8 compatibility is not established in the reviewed sources."),
        f("tablet_cellular_variant", "abc_x8_gizguide_ph", "4G LTE dual-SIM configuration reported; no separate Wi-Fi-only X8 configuration was located", "4G LTE dual SIM; no Wi-Fi-only SKU identified", status="VERIFIED_SECONDARY",
          note="The workbook record is matched to the cellular 2GB/32GB X8 listing; the inventory does not identify a separate Wi-Fi-only variant."),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct tablet field reviews, got {len(rows)}")
    return rows


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the workbook's pending ABC TECH X8 tablet; refusing unexpected scope/device.")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != f"{DEVICE}-unrecorded":
        raise ValueError("Expected one unrecorded placeholder configuration; review before replacing it.")

    replacement = {"id": CONFIG, "label": "2 GB RAM / 32 GB storage (4G LTE)",
                   "modelCode": "X8-CB-8I-232", "notes": "Exact product SKU from ABC Tech's official page. The manufacturer SKU, not an independently verified regulatory model number, is shown."}
    review = {
        "deviceId": DEVICE, "configurationId": CONFIG, "brand": "ABC TECH",
        "model": "X8 Study Buddy Tablet", "configuration": "2 GB RAM / 32 GB storage",
        "configurationLabel": replacement["label"], "modelCode": "X8-CB-8I-232",
        "replacementVariants": [replacement], "replaceUnrecordedPlaceholder": True,
        "sources": SOURCES, "fields": fields(),
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Verified Philippine launch and current manufacturer-store listing: ABC TECH X8 Study Buddy Tablet (official SKU X8-CB-8I-232), 2GB/32GB. ABC Tech's site lists PHP 4,899 when checked 2026-11-27; add-to-cart is shown, but stock/checkout was not verified.",
            "philippineAvailability": "Verified Philippine release of ABC TECH X8 Study Buddy Tablet, 2GB/32GB, dated 2023-07-28; exact-SKU listing remains on the official Philippine site.",
            "observedAt": OBSERVED,
            "qualityFlag": "Manually reviewed; exact manufacturer SKU, 2GB/32GB configuration and Philippine availability verified; panel technology/resolution unresolved; current official listed price observed; stock not confirmed.",
            "catalogModel": "X8 Study Buddy Tablet",
            "manufacturer": "ABC Tech Ventures Inc.",
            "productLine": "Study Buddy",
            "modelNumber": "X8-CB-8I-232",
            "philippineReleaseYear": 2023,
            "philippineDateLabel": "Manufacturer-reported Philippine release date",
            "researchNotes": "Workbook row 169 labeled ABC TECH X8 is matched to the Filipino-owned ABC Tech Ventures Inc. product named X8 Study Buddy Tablet and official SKU X8-CB-8I-232. The verified configuration is 2GB RAM/32GB storage with dual-SIM LTE reported by local coverage. The manufacturer page's current display pixel resolution and panel type conflict with a 2023 local specification listing; both fields remain blank and cited. The official page lists PHP 4,899, but current stock/checkout is not verified. An exact official product image is identified, but reuse permission is undocumented, so the neutral placeholder remains. Study scope remains Pending.",
            "openIssues": [
                {"issue": "Manufacturer and Philippine media reports conflict on exact pixel resolution", "action": "Keep normalized resolution blank and retain both source values."},
                {"issue": "Manufacturer pages say TN/IPS or IPS; exact panel technology on this SKU is unclear", "action": "Keep normalized panel type blank until the manufacturer identifies the SKU's panel."},
                {"issue": "Current official listed price is PHP 4,899, but stock/checkout was not confirmed", "action": "Display the dated official listing price without an in-stock claim."},
                {"issue": "Study eligibility remains Pending", "action": "Keep workbook eligibility unchanged until the study screening rule is applied."},
                {"issue": "Official product imagery has no documented reuse license", "action": "Keep the neutral unavailable-image placeholder and preserve the source asset URL for rights review."},
            ],
        },
    }
    manual["records"] = [row for row in manual["records"]
                         if not (row.get("deviceId") == DEVICE and row.get("configurationId") == CONFIG)]
    add_review(manual, catalog, review)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    saved = next(row for row in manual["records"]
                 if row.get("deviceId") == DEVICE and row.get("configurationId") == CONFIG)
    saved.update({"model": "X8 Study Buddy Tablet", "configuration": "2 GB RAM / 32 GB storage",
                  "configurationLabel": replacement["label"]})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "ABC Tech's official product page links to an exact X8 Study Buddy Tablet image, but no image reuse license or permission to republish/hotlink is documented. Keep the neutral placeholder.",
        "sourcePage": URL_PRODUCT,
        "assetUrl": None,
        "candidateAssetUrl": IMAGE_URL,
        "scope": "Official ABC TECH X8 Study Buddy Tablet product image, charcoal-black product listing; exact SKU association is through the official product page.",
        "rightsTermsUrl": None,
        "rightsCheck": "Reviewed the official product page and linked image. No image reuse license or credit/permission terms were found on the product page. Do not download or hotlink.",
        "rightsCheckSourcePage": URL_PRODUCT,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for ABC TECH X8 Study Buddy Tablet",
    }
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 5999, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_abc_tech_x8_x8_cb_8i_232_2gb_32gb",
         "variant_ram_gb": 2, "variant_storage_gb": 32,
         "price_type": "historical_ph_launch_price_reported",
         "source_published_at": "2023-08-15",
         "excerpt": "GIZGUIDE reports the ABC TECH X8 at PHP 5,999 in its 2023 Philippine launch/specification coverage; Unbox Diaries independently reports the same launch price.",
         "source_url": URL_GIZ, "source_kind": "historical_local_launch_price_report",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 4899, "configuration_id": CONFIG,
         "configuration_match": "exact_official_sku_X8_CB_8I_232_2gb_32gb",
         "variant_ram_gb": 2, "variant_storage_gb": 32,
         "price_type": "current_official_ph_product_page_list_price",
         "source_published_at": None,
         "excerpt": "ABC Tech's exact SKU X8-CB-8I-232 product page lists PHP 4,899 and shows Add to Cart on 2026-11-27; stock/checkout was not verified.",
         "source_url": URL_PRODUCT, "source_kind": "current_manufacturer_store_listing",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "listed_not_stock_verified"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "ABC TECH", "model_name": "X8 Study Buddy Tablet", "category": "tablets", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": item["url"], "source_kind": item["purpose"], "status": "reviewed", "result": item["note"]} for item in SOURCES],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    latest = json.loads(LATEST_REVIEWED.read_text(encoding="utf-8"))
    target = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if target:
        target["status"] = "manually_reviewed"
    latest["run_at"] = OBSERVED
    LATEST_REVIEWED.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for row in review["fields"]:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"workbookRow": 169, "model": "ABC TECH X8 Study Buddy Tablet",
                      "manufacturerSku": "X8-CB-8I-232", "configuration": replacement["label"],
                      "reviewedFields": len(review["fields"]), "fieldStatuses": counts,
                      "sources": len(SOURCES), "philippineReleaseDate": "2023-07-28",
                      "historicalLaunchPricePhp": 5999, "currentOfficialListPricePhp": 4899,
                      "stock": "not verified", "image": "exact official image located; reuse rights not established; placeholder retained",
                      "studyScope": "Pending"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
