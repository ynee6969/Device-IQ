#!/usr/bin/env python3
"""Record a source-backed Philippine review for the vivo Y27 4G (V2249)."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_6f256573a0fb54"
CONFIG = "device_6f256573a0fb54-auto-6gb-128gb"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/vivo-y27-ph-prices-2026-11-27.json"

URL_SPECS = "https://www.vivo.com/ph/products/param/y27"
URL_OVERVIEW = "https://www.vivo.com/ph/products/y27"
URL_STORE = "https://shop.vivo.com/ph/product/2061?skuId=8160"
URL_GLOBAL_LAUNCH = "https://vivonewsroom.in/press-release/vivo-launches-y27-with-stylish-design-and-44w-flashcharge/"
URL_PH_LAUNCH = "https://www.technobaboy.com/2023/08/22/vivo-y27-price-philippines/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/vivo-y27/amp"
URL_GSMARENA = "https://www.gsmarena.com/vivo_y27-12430.php"
URL_MEDIATEK = "https://www.mediatek.com/products/smartphones/mediatek-helio-g85"
URL_MEDIATEK_PDF = "https://i.mediatek.com/hubfs/MediaTek-Helio-G85-Infographic.pdf?hsLang=en"
URL_TRA = "https://www.tra.gov.eg/wp-content/uploads/2025/09/Type-Approved-List.pdf"
URL_PRICE_DROP = "https://technology.inquirer.net/131278/price-drop-alert-vivo-y27-now-more-affordable-at-php-7999"
URL_IMAGE_PAGE = "https://www.vivo.com/tr/products/param/y27"
IMAGE_URL = "https://de-gdpr-exstatic-vivofs.vivo.com/sFhAQhTYYDsNOJz1/1690190469584/f033c326e5a8d2c58bb240f08fbc02dc.png"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("vivo_y27_ph_specs", URL_SPECS, "vivo Philippines", "Manufacturer specifications",
        "Philippine Y27 specification page; the online store separately distinguishes 4G and 5G selections."),
    src("vivo_y27_ph_overview", URL_OVERVIEW, "vivo Philippines", "Manufacturer product overview",
        "Official Y27 overview confirms local color/design, display brightness, battery, charging, extended RAM and IP54 caveats."),
    src("vivo_y27_ph_store", URL_STORE, "vivo Philippines E-Store", "Exact Philippine SKU, specification and dated price",
        "Checked 2026-11-27. The selected item is Sea Blue, 6 GB + 128 GB (4G), SKU X1, listed at PHP 7,999; the page does not state stock."),
    src("vivo_y27_global_launch", URL_GLOBAL_LAUNCH, "vivo India Newsroom", "Manufacturer launch announcement",
        "Official release dated 2023-07-20 says the Y27 6 GB + 128 GB went on sale in India that day; this is not Philippine availability evidence.",
        "2023-07-20"),
    src("vivo_y27_ph_launch", URL_PH_LAUNCH, "Technobaboy", "Contemporaneous Philippine launch and local configuration",
        "Reports a Philippine launch on 2023-08-19 at PHP 8,999 and a 6 GB + 128 GB 4G LTE variant; it also identifies the 2 MP module as depth. Its OIS claim is not carried without manufacturer confirmation.",
        "2023-08-22"),
    src("vivo_y27_ptg_ph", URL_PTG, "Pinoy Techno Guide", "Philippine price, advertised early-bird date and specifications",
        "Philippine Y27 page dated 2023-08-14 reports the 6 GB / 128 GB model, PHP 8,999 official price, an early-bird offer starting 2023-08-15, microSD expansion and supporting specifications.",
        "2023-08-14"),
    src("vivo_y27_gsmarena", URL_GSMARENA, "GSMArena", "Independent exact-model specification cross-check",
        "Identifies the vivo Y27 as model V2249 and provides display, connectivity, audio and release details. Used only for exact-model facts not fully stated by the Philippine product page."),
    src("vivo_y27_tra_model_code", URL_TRA, "Egyptian National Telecom Regulatory Authority", "Regulatory model-code cross-check",
        "Type-approved equipment list pairs VIVO V2249 with Y27. This supports model identity only, not Philippine market eligibility.",
        "2025-09-01"),
    src("mediatek_helio_g85", URL_MEDIATEK, "MediaTek", "Chipset specifications",
        "Manufacturer chipset page lists the Helio G85 CPU architecture, GPU, memory interface capability, Wi-Fi and positioning capabilities; device-specific implementation is not inferred from chipset maxima."),
    src("mediatek_helio_g85_pdf", URL_MEDIATEK_PDF, "MediaTek", "Chipset process node cross-check",
        "Official Helio G85 infographic lists a 12 nm manufacturing process."),
    src("vivo_y27_price_drop", URL_PRICE_DROP, "INQUIRER BrandRoom", "Historical Philippine price change",
        "Vivo-supplied BrandRoom article reports the Y27 price drop to PHP 7,999 in January 2024; retained as a historical snapshot, not as a current stock claim.",
        "2024-01-15"),
    src("vivo_y27_image_page", URL_IMAGE_PAGE, "vivo Türkiye", "Exact-model image identity review",
        "Official product page image depicts the Y27 4G in Sea Blue. The asset is not copied or hotlinked because this product-page image has no documented reuse permission."),
]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      catalog_value=None,
      price_type: str | None = None, price_observed: str | None = None,
      price_condition: str | None = None, listing_status: str | None = None) -> dict:
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
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed
        row["priceCondition"] = price_condition or "new"
    if listing_status:
        row["listingStatus"] = listing_status
    return row


def nd(fid: str, sid: str, description: str, note: str | None = None) -> dict:
    return f(fid, sid, description, None, status="NOT_DISCLOSED",
             note=note or "No exact Y27 4G value was published in the reviewed manufacturer and accepted reference material; left blank." )


def na(fid: str, sid: str, description: str, note: str) -> dict:
    return f(fid, sid, description, None, status="NOT_APPLICABLE", note=note)


def fields() -> list[dict]:
    material_conflict = f(
        "materials", "vivo_y27_ph_store",
        "Philippine store lists body material as 2.5D Plastic; vivo India's launch release describes a 2.5D glass body/glass finishes.", None,
        status="CONFLICTING_INFORMATION",
        note="Regional manufacturer descriptions conflict. The exact frame/back material of the Philippine SKU is not resolved, so no material value is published.",
    )
    material_conflict["candidateEvidence"] = [
        {"value": "2.5D Plastic", "sourceUrl": URL_STORE, "sourceKind": "manufacturer_primary_philippines",
         "observedAt": OBSERVED, "excerpt": "Material: 2.5D Plastic", "configurationMatch": "exact Y27 4G product listing",
         "reviewStatus": "CONFLICTING_INFORMATION"},
        {"value": "2.5D glass body design; glass finishes", "sourceUrl": URL_GLOBAL_LAUNCH,
         "sourceKind": "manufacturer_primary_india", "observedAt": OBSERVED,
         "excerpt": "vivo India launch copy describes the Y27 as a 2.5D glass body design with glass finishes.",
         "configurationMatch": "same model family, different regional launch page",
         "reviewStatus": "CONFLICTING_INFORMATION"},
    ]
    rows = [
        f("model_number", "vivo_y27_tra_model_code", "VIVO V2249 / Y27", "V2249",
          status="VERIFIED_SECONDARY", note="The workbook's Y27 record matches the 4G model V2249; the separate Y27 5G option is not merged into this record."),
        f("global_release_date", "vivo_y27_global_launch", "vivo India announced sale availability on 2023-07-20", "2023-07-20",
          note="This is the manufacturer's first identified sale date in India, not a claim that every market launched simultaneously."),
        f("configuration", "vivo_y27_ph_store", "6GB+128GB (4G); selected Y27 Sea Blue 6GB+128GB (4G), SKU X1", "6 GB RAM / 128 GB storage",
          note="Exact Philippine 4G SKU matched. The separate 6GB+128GB (5G) selector is excluded; up to 6 GB extended RAM is software memory, not a second physical-RAM variant."),
        f("philippine_release_date", "vivo_y27_ph_launch", "Launched in the Philippines on August 19, 2023; PTG separately reported an online early-bird offer starting August 15, 2023.", "2023-08-19",
          status="VERIFIED_SECONDARY", note="Stored as the reported Philippine launch date. The earlier PTG date refers to an advertised online promotion; the two reports are not treated as contradictory."),
        f("official_launch_price_php", "vivo_y27_ph_launch", "PHP 8,999 at the Philippine launch for the 6 GB / 128 GB Y27", 8999,
          status="VERIFIED_SECONDARY", unit="PHP", price_type="historical_ph_launch_suggested_retail_price",
          price_observed="2023-08-19", note="Contemporaneous Philippine launch coverage reports PHP 8,999. This is historical launch pricing, not the current listing."),
        f("current_price_php", "vivo_y27_ph_store", "PHP 7,999 incl. taxes; selected Sea Blue, 6GB+128GB (4G), SKU X1; observed 2026-11-27", 7999,
          unit="PHP", price_type="current_official_store_list_price", price_observed=OBSERVED,
          price_condition="new", listing_status="Not verified",
          note="Dated official e-store list price for the exact 4G configuration. The page did not establish stock or checkout availability; do not label as in stock."),
        f("display_size", "vivo_y27_ph_specs", "6.64-inch", 6.64, key="displayInches", unit="in"),
        f("display_technology", "vivo_y27_gsmarena", "IPS LCD", "IPS LCD", status="VERIFIED_SECONDARY", key="displayType",
          note="The Philippine manufacturer page specifies LCD; exact-model secondary references further identify IPS LCD."),
        f("display_resolution", "vivo_y27_ph_specs", "2388 × 1080 (FHD+)", "1080 x 2388", key="resolution"),
        f("display_refresh_rate", "vivo_y27_gsmarena", "60 Hz", "60", status="VERIFIED_SECONDARY", key="refreshHz", unit="Hz"),
        f("display_brightness", "vivo_y27_ph_overview", "600 nits local peak brightness", 600, unit="nits",
          note="vivo describes this as local peak brightness; it is not relabeled as a full-screen sustained brightness."),
        nd("display_protection", "vivo_y27_ph_specs", "Screen protection is not specified on the reviewed Philippine Y27 specification page."),
        f("chipset", "vivo_y27_ph_specs", "MediaTek Helio G85", "MediaTek Helio G85", key="chipset"),
        f("process_node", "mediatek_helio_g85_pdf", "12 nm", 12, unit="nm"),
        f("cpu", "mediatek_helio_g85", "2× Arm Cortex-A75 up to 2.0 GHz + 6× Arm Cortex-A55 up to 1.8 GHz", "2x Cortex-A75 up to 2.0 GHz + 6x Cortex-A55 up to 1.8 GHz",
          key="cpu", note="MediaTek's Helio G85 specifications; the Y27 chipset itself is confirmed by vivo Philippines."),
        f("gpu", "mediatek_helio_g85", "Arm Mali-G52 MC2", "Arm Mali-G52 MC2", key="gpu"),
        f("operating_system", "vivo_y27_ph_specs", "Funtouch OS 13 (based on Android 13)", "Android 13 / Funtouch OS 13", key="os"),
        nd("os_support", "vivo_y27_ph_specs", "No published OS or security update support period was found in the reviewed manufacturer material."),
        f("ram_capacity", "vivo_y27_ph_store", "6 GB installed RAM; up to 6 GB Extended RAM is software-based", 6, key="ramGb", unit="GB",
          note="Catalog RAM is the physical 6 GB configuration only. vivo's 6 GB Extended RAM is software-backed and is not added to installed RAM."),
        nd("ram_type", "vivo_y27_ph_specs", "The installed RAM type for the Y27 4G is not specified; chipset memory capabilities are not treated as proof of the device's installed RAM type."),
        f("storage_capacity", "vivo_y27_ph_store", "128 GB", 128, key="storageGb", unit="GB"),
        nd("storage_type", "vivo_y27_ph_specs", "The type of internal 128 GB storage is not specified for this configuration."),
        f("storage_expansion", "vivo_y27_ptg_ph", "Expandable by microSD card up to 1 TB", "microSD card up to 1 TB", status="VERIFIED_SECONDARY",
          note="The Philippine manufacturer spec confirms the dedicated microSD slot; PTG provides the 1 TB maximum."),
        f("rear_camera_system", "vivo_y27_global_launch", "50 MP main camera + 2 MP bokeh camera; Philippine launch coverage describes the auxiliary module as depth", "50 MP main + 2 MP bokeh/depth auxiliary camera",
          status="VERIFIED_SECONDARY", key="rearCameraMp", catalog_value=50, unit="MP",
          note="The two-module 50+2 MP system is confirmed. The catalog's numeric rear-camera summary stores the main sensor resolution (50 MP). OIS is omitted because it is not confirmed by manufacturer specifications."),
        nd("main_camera_sensor", "vivo_y27_ph_specs", "The manufacturer specifies camera resolution and aperture but does not name the main camera sensor model."),
        na("ultrawide_camera", "vivo_y27_global_launch", "The published rear camera system lists a 50 MP main module and a 2 MP bokeh/depth auxiliary module; no ultrawide module is listed.", "Not applicable to the documented two-camera rear system; no ultrawide camera is listed."),
        na("telephoto_camera", "vivo_y27_global_launch", "The published rear camera system lists a 50 MP main module and a 2 MP bokeh/depth auxiliary module; no telephoto module is listed.", "Not applicable to the documented two-camera rear system; no telephoto camera is listed."),
        f("front_camera", "vivo_y27_ph_specs", "Front camera: 8 MP, f/2.0", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", "vivo_y27_ptg_ph", "Up to 1080p video recording", "Up to 1080p; frame rate not recorded", status="VERIFIED_SECONDARY", key="video",
          note="The manufacturer page lists MP4 video recording but not resolution; PTG gives up to 1080p. No frame rate is inferred."),
        f("battery_capacity", "vivo_y27_ph_specs", "5000 mAh (typical)", 5000, key="batteryMah", unit="mAh"),
        nd("battery_technology", "vivo_y27_ph_specs", "Battery chemistry and serviceability are not specified in the reviewed manufacturer material."),
        f("wired_charging", "vivo_y27_ph_specs", "44 W FlashCharge", 44, key="chargingW", unit="W"),
        nd("wireless_charging", "vivo_y27_ph_specs", "Wireless or reverse charging is not specified in the reviewed manufacturer material; no unsupported 0 W value is assigned."),
        f("dimensions", "vivo_y27_ph_store", "164.06 × 76.17 × 8.07 mm", "164.06 x 76.17 x 8.07 mm", key="dimensions", unit="mm"),
        f("weight", "vivo_y27_ph_store", "190 g", 190, key="weightG", unit="g"),
        material_conflict,
        f("ingress_protection", "vivo_y27_ph_overview", "IP54 dust and water resistance; vivo says the phone is not professional waterproof equipment and the rating applies under normal use.", "IP54", note="Preserve the manufacturer's normal-use caveat; do not describe the phone as waterproof."),
        f("sim_esim", "vivo_y27_ph_specs", "1 nano-SIM + 1 nano-SIM + 1 microSD; Dual SIM Dual Standby; eSIM not listed", "Dual nano-SIM, dual standby + microSD; eSIM not recorded", key="sim",
          note="This is the Y27 4G card-slot layout. It is kept distinct from the 5G selection on the store page."),
        f("cellular_bands", "vivo_y27_ph_specs", "2G GSM 850/900/1800 MHz; 3G WCDMA B1/B5/B8; 4G FDD-LTE B1/B3/B5/B7/B8/B20/B28; 4G TDD-LTE B38/B40/B41", "2G GSM 850/900/1800; 3G B1/B5/B8; 4G FDD B1/B3/B5/B7/B8/B20/B28; TDD B38/B40/B41", key="cellular"),
        f("wifi", "vivo_y27_ph_specs", "Wi-Fi 2.4 GHz / 5 GHz", "Dual-band Wi-Fi (2.4 GHz / 5 GHz)", key="wifi"),
        f("bluetooth", "vivo_y27_ph_specs", "Bluetooth 5.0", "Bluetooth 5.0"),
        f("usb", "vivo_y27_ph_specs", "Type-C; OTG supported; data transfer standard not stated", "USB Type-C; OTG supported; data standard not recorded", key="ports"),
        f("nfc", "vivo_y27_gsmarena", "NFC: No", "No NFC", status="VERIFIED_SECONDARY", note="Exact-model secondary specification. The reviewed Philippine manufacturer table does not separately list NFC."),
        f("gnss", "vivo_y27_ph_specs", "GPS, BeiDou, GLONASS, Galileo and QZSS", "GPS, BeiDou, GLONASS, Galileo, QZSS"),
        f("audio", "vivo_y27_ptg_ph", "3.5 mm audio jack; speaker configuration not recorded", "3.5 mm headphone jack; speaker configuration not recorded", status="VERIFIED_SECONDARY", key="sound"),
        f("sensors", "vivo_y27_ph_specs", "Accelerometer, ambient light sensor, proximity sensor, e-compass and side-mounted fingerprint sensor", "Accelerometer; ambient light; proximity; e-compass; side fingerprint"),
    ]
    if len(rows) != 46 or len({row["fieldId"] for row in rows}) != 46:
        raise ValueError(f"Expected 46 distinct field reviews, got {len(rows)}")
    return rows


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device:
        raise ValueError(f"Workbook device is missing from the public catalog: {DEVICE}")
    if device.get("scopeStatus") != "Pending":
        raise ValueError(f"Expected Pending study scope; refusing to change it: {device.get('scopeStatus')}")
    if len(device.get("variants", [])) != 1:
        raise ValueError("Expected one workbook Y27 configuration; refusing to merge or split variants automatically.")
    if device["variants"][0].get("id") != CONFIG:
        raise ValueError("Unexpected Y27 configuration ID; review the workbook-to-catalog match first.")

    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "vivo",
        "model": "Y27 4G",
        "configuration": "6 GB RAM / 128 GB storage",
        "configurationLabel": "6 GB RAM / 128 GB storage (4G)",
        "modelCode": "V2249",
        "sku": "X1",
        "sources": SOURCES,
        "fields": fields(),
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Contemporaneous Philippine coverage reports the Y27 4G launched on 2023-08-19 at PHP 8,999 and available from vivo's website and physical stores. PTG reported an official online early-bird offer starting 2023-08-15. Current stock is not verified.",
            "philippineAvailability": "Verified Philippine availability: vivo Y27 4G (V2249), 6 GB / 128 GB; local launch reported 2023-08-19.",
            "observedAt": OBSERVED,
            "qualityFlag": "Manually reviewed; exact PH 4G configuration matched; current stock and study eligibility remain unresolved.",
            "catalogModel": "Y27 4G",
            "manufacturer": "vivo",
            "productLine": "Y",
            "modelNumber": "V2249",
            "philippineReleaseYear": 2023,
            "philippineDateLabel": "Reported Philippine launch date",
            "researchNotes": "Workbook row 165 labeled Y27 is matched to the Philippine vivo Y27 4G, model V2249, with one 6 GB / 128 GB configuration. The official store also displays a distinct 5G selector; that model is not merged here. Workbook study scope remains Pending.",
            "openIssues": [
                {"issue": "Current store stock is not stated", "action": "Show the 2026-11-27 listed price as a dated observation, not as an in-stock offer."},
                {"issue": "Study eligibility remains Pending", "action": "Keep workbook eligibility unchanged until the thesis screening rule is applied."},
                {"issue": "Regional body-material descriptions conflict", "action": "Leave material composition unresolved in the public spec audit."},
            ],
        },
    }
    add_review(manual, catalog, review)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    saved_review = next(row for row in manual["records"]
                        if row.get("deviceId") == DEVICE and row.get("configurationId") == CONFIG)
    saved_review["model"] = "Y27 4G"
    saved_review["configuration"] = "6 GB RAM / 128 GB storage"
    saved_review["configurationLabel"] = "6 GB RAM / 128 GB storage (4G)"
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact vivo Y27 4G Sea Blue image is present on the official vivo Türkiye product page, but the Philippine catalog's permission to republish or hotlink that product-page image is not documented. Keep the neutral placeholder.",
        "sourcePage": URL_IMAGE_PAGE,
        "assetUrl": None,
        "candidateAssetUrl": IMAGE_URL,
        "scope": "Exact vivo Y27 4G (V2249), Sea Blue; image identity matches the model, but reuse rights are not established.",
        "rightsTermsUrl": None,
        "rightsCheck": "The vivo Newsroom download notice on the India launch release is limited to newsroom media assets and requires agreement at download; it does not establish reuse permission for this separate vivo.com product-page image. No download gate was bypassed.",
        "rightsCheckSourcePage": URL_GLOBAL_LAUNCH,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for vivo Y27 4G",
    }
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {
            "device_id": DEVICE, "amount_php": 8999, "configuration_id": CONFIG,
            "configuration_match": "exact_ph_y27_4g_v2249_6gb_128gb",
            "variant_ram_gb": 6, "variant_storage_gb": 128,
            "price_type": "historical_ph_launch_suggested_retail_price",
            "source_published_at": "2023-08-22",
            "excerpt": "Philippine launch coverage reports the 6 GB / 128 GB Y27 at PHP 8,999; the article says the model launched on 2023-08-19.",
            "source_url": URL_PH_LAUNCH, "source_kind": "historical_local_launch_price_report",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_launch_price_not_current",
        },
        {
            "device_id": DEVICE, "amount_php": 7999, "configuration_id": CONFIG,
            "configuration_match": "exact_ph_y27_4g_v2249_6gb_128gb",
            "variant_ram_gb": 6, "variant_storage_gb": 128,
            "price_type": "historical_price_drop_report",
            "source_published_at": "2024-01-15",
            "excerpt": "INQUIRER BrandRoom reported a vivo Y27 price reduction to PHP 7,999 in January 2024.",
            "source_url": URL_PRICE_DROP, "source_kind": "historical_local_price_report",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_price_not_current",
        },
        {
            "device_id": DEVICE, "amount_php": 7999, "configuration_id": CONFIG,
            "configuration_match": "exact_selected_ph_y27_4g_v2249_6gb_128gb_sku_x1",
            "variant_ram_gb": 6, "variant_storage_gb": 128,
            "price_type": "current_official_store_list_price",
            "source_published_at": None,
            "excerpt": "Official Philippine e-store showed PHP 7,999 incl. taxes for selected Y27 Sea Blue 6GB+128GB (4G), SKU X1, on 2026-11-27; stock was not stated.",
            "source_url": URL_STORE, "source_kind": "current_official_store_listing",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "listed_stock_not_verified",
        },
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "vivo", "model_name": "Y27 4G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": item["url"], "result": item["note"]} for item in SOURCES],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    statuses = {}
    for row in review["fields"]:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    print(json.dumps({
        "workbookRow": 165, "model": "vivo Y27 4G", "modelNumber": "V2249",
        "configuration": review["configurationLabel"], "reviewedFields": len(review["fields"]),
        "fieldStatuses": statuses, "sources": len(SOURCES),
        "philippineLaunchDate": "2023-08-19", "launchPricePhp": 8999,
        "currentListedPricePhp": 7999, "stock": "not verified",
        "image": "exact manufacturer image found; placeholder retained because reuse rights are not established",
        "studyScope": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
