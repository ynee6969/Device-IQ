#!/usr/bin/env python3
"""Record a source-backed Philippine review for the vivo Y36 4G (V2247)."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_d2f928e59b41f6"
CONFIG = "device_d2f928e59b41f6-auto-8gb-256gb"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "lib/catalog/image-manifest.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/vivo-y36-ph-prices-2026-11-27.json"

URL_SPECS = "https://www.vivo.com/ph/products/param/y36"
URL_OVERVIEW = "https://www.vivo.com/ph/product/productDetails?id=6429"
URL_STORE = "https://shop.vivo.com/ph/product/2058?skuId=8153"
URL_STORE_5G = "https://shop.vivo.com/ph/product/2060?skuId=8157"
URL_PH_LAUNCH = "https://www.vivoglobal.ph/vivo-y36-now-available-in-ph-with-newest-ambassador-anne-curtis/"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/vivo-y36"
URL_YUGA = "https://www.yugatech.com/mobile/vivo-y36-specs-price-philippines/"
URL_UNBOX = "https://unbox.ph/gadget/phones/vivo-y36-4g-specs-and-price-philippines/"
URL_ID_ANNOUNCE = "https://www.vivo.com/id/about-vivo/news/y36-series"
URL_ID_SALE = "https://www.vivo.com/id/about-vivo/news/y36-selling"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/6-series/snapdragon-680-4g-mobile-platform"
URL_TRA = "https://www.tra.gov.eg/wp-content/uploads/2025/09/Type-Approved-List.pdf"
URL_GSMARENA = "https://www.gsmarena.com/vivo_y36-12374.php"
URL_IMAGE = "https://commons.wikimedia.org/wiki/File:VIVO_Y36%EF%BC%882024%E5%B9%B42%E6%9C%8820%E6%97%A5%EF%BC%89.jpg"
IMAGE_ASSET = "https://upload.wikimedia.org/wikipedia/commons/f/f2/VIVO_Y36%EF%BC%882024%E5%B9%B42%E6%9C%8820%E6%97%A5%EF%BC%89.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("vivo_y36_ph_specs", URL_SPECS, "vivo Philippines", "Manufacturer specifications and exact PH configuration",
        "The Philippine specification page lists 8GB+256GB, Snapdragon 680, Funtouch OS 13/Android 13, display, cameras, dimensions, battery, card slots, local LTE bands and connectivity. Checked 2026-11-27."),
    src("vivo_y36_ph_overview", URL_OVERVIEW, "vivo Philippines", "Manufacturer product overview",
        "Local overview identifies 90Hz refresh, 650-nit High Brightness Mode, 240Hz touch sampling, 200% Audio Booster, IP54 caveat, colors, variant-specific marketed glass finishes, and 8GB software-extended RAM. Checked 2026-11-27."),
    src("vivo_y36_ph_store", URL_STORE, "vivo Philippines E-Store", "Exact local 4G SKU and dated listed price",
        "Checked 2026-11-27. Selected Meteor Black Y36 8GB+256GB (4G), SKU X1, listed at PHP 10,999 including taxes. The page does not establish stock or checkout availability."),
    src("vivo_y36_ph_spec_price", URL_SPECS, "vivo Philippines", "Manufacturer page price reference",
        "The Philippine specifications page simultaneously lists PHP 11,999 for 8GB+256GB; recorded separately from the lower selected E-Store listing price. Neither page establishes stock."),
    src("vivo_y36_ph_5g_store", URL_STORE_5G, "vivo Philippines E-Store", "Cross-check against a separate, excluded model",
        "The separate Y36 5G store listing has Dimensity 6020 and a 5G label. It is not merged into this Snapdragon 680 Y36 4G workbook record."),
    src("vivo_y36_ph_newsroom", URL_PH_LAUNCH, "vivo Philippines newsroom", "Philippine launch and local availability",
        "The vivo Philippines newsroom states that the Y36 launched locally on 2023-07-15 and identifies Snapdragon 680. Used for local availability, not to infer an exact launch transaction time.", "2023-07-15"),
    src("vivo_y36_ptg_ph", URL_PTG, "Pinoy Techno Guide", "Philippine release, launch price and exact-market specification cross-check",
        "Local Y36 entry dated 2023-07-15 lists PHP 12,999, 8GB/256GB, 4G, 90Hz/650-nit display, microSD expansion, camera, audio, NFC and battery details.", "2023-07-15"),
    src("vivo_y36_yugatech_ph", URL_YUGA, "YugaTech", "Contemporaneous Philippine launch and specification cross-check",
        "Local article dated 2023-07-15 corroborates the PH price/configuration and lists display, cameras, IP54 and other details; it reports Bluetooth 5.0 and a Fluorite AG Glass back.", "2023-07-15"),
    src("vivo_y36_unbox_ph", URL_UNBOX, "UNBOX PH", "Philippine configuration and specification cross-check",
        "Article dated 2023-07-03 explicitly names the Y36 4G and its PH 8GB/256GB configuration; it lists LPDDR4X RAM, UFS 2.2 storage and PHP 12,999 availability starting 2023-07-15. It differs from vivo's Bluetooth 5.1 and material description.", "2023-07-03"),
    src("vivo_y36_id_announcement", URL_ID_ANNOUNCE, "vivo Indonesia", "Manufacturer model-family announcement",
        "Official announcement dated 2023-05-25 covers the Y36 and separately identifies Y36 5G. It is announcement timing, not sale availability.", "2023-05-25"),
    src("vivo_y36_id_sale", URL_ID_SALE, "vivo Indonesia", "Manufacturer evidence of model availability for sale",
        "Official article dated 2023-06-05 says the Y36 was available in Indonesia in Glitter Aqua and Meteor Black. This is the earliest identified official sale-availability date, not a claim of the first worldwide sale.", "2023-06-05"),
    src("qualcomm_snapdragon_680", URL_QUALCOMM, "Qualcomm", "Chipset-manufacturer specifications",
        "Confirms Snapdragon 680's 6nm process, Kryo 265 CPU, Adreno 610 GPU and chipset-level CPU clock. Device configuration claims are not inferred from chipset capability."),
    src("vivo_y36_tra_model_code", URL_TRA, "Egyptian National Telecom Regulatory Authority", "Regulatory model-code identity cross-check",
        "The type-approved equipment list pairs VIVO V2247 with Y36. This corroborates model identity only and is not Philippine market evidence.", "2025-09-01"),
    src("vivo_y36_gsmarena", URL_GSMARENA, "GSMArena", "Independent exact-model identity and secondary specification cross-check",
        "Identifies the Snapdragon 680 Y36 as model V2247 and notes that NFC availability depends on market/region. Used only for model identity/context where local pages do not disclose a detail."),
    src("vivo_y36_commons_image", URL_IMAGE, "Wikimedia Commons / メイド理世", "Exact model image identity and reuse terms",
        "Photo is titled and categorized as vivo Y36 and shows the Y36 name on the handset/store display. The pictured Chinese retail unit shows OriginOS 3 and an unverified regional configuration; it is a model-level image, not a claim that it depicts the Philippine Funtouch OS SKU. CC BY-SA 4.0 permits reuse with attribution, license link and share-alike terms."),
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
        row["priceType"] = price_type
        row["priceObservedAt"] = price_observed
        row["priceCondition"] = price_condition or "new"
    if listing_status:
        row["listingStatus"] = listing_status
    return row


def nd(fid: str, sid: str, description: str, note: str | None = None) -> dict:
    return f(fid, sid, description, None, status="NOT_DISCLOSED",
             note=note or "The reviewed sources do not publish this exact Y36 4G value; it remains blank rather than inferred.")


def na(fid: str, sid: str, description: str, note: str) -> dict:
    return f(fid, sid, description, None, status="NOT_APPLICABLE", note=note)


def conflict(fid: str, sid: str, description: str, evidence: list[dict], note: str) -> dict:
    row = f(fid, sid, description, None, status="CONFLICTING_INFORMATION", note=note)
    row["candidateEvidence"] = evidence
    return row


def ev(value: str, url: str, source_kind: str, excerpt: str, match: str) -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": match, "reviewStatus": "CONFLICTING_INFORMATION"}


def fields() -> list[dict]:
    bluetooth = conflict(
        "bluetooth", "vivo_y36_ph_specs",
        "vivo Philippines lists Bluetooth 5.1; local Philippine specification pages from PTG and YugaTech list Bluetooth 5.0.",
        [ev("Bluetooth 5.1", URL_SPECS, "manufacturer_primary_philippines", "Connectivity: Bluetooth 5.1", "Philippine Y36 8GB+256GB page"),
         ev("Bluetooth 5.0", URL_PTG, "secondary_philippines", "Bluetooth 5.0", "Philippine Y36 listing"),
         ev("Bluetooth 5.0", URL_YUGA, "secondary_philippines", "Bluetooth 5.0", "Philippine Y36 launch specification")],
        "Local sources disagree. The source values are preserved for review; the public normalized field remains blank until the discrepancy is resolved.")
    materials = conflict(
        "materials", "vivo_y36_ph_specs",
        "vivo's Philippine pages describe 2.5D glass and color-specific glass finishes; PTG describes a glass front with a polycarbonate back.",
        [ev("2.5D glass; overview names Glitter Aqua Crystal Glass and Meteor Black Fluorite AG Glass", URL_SPECS, "manufacturer_primary_philippines", "Material: 2.5D glass; color-specific finish details appear on the official overview.", "Philippine Y36 colors"),
         ev("Glass front, polycarbonate back", URL_PTG, "secondary_philippines", "Build Materials: Glass front, Polycarbonate back", "Philippine Y36 listing"),
         ev("Fluorite AG Glass back panel", URL_YUGA, "secondary_philippines", "Fluorite AG Glass (back panel)", "Philippine Y36 launch specification")],
        "Body/back material descriptions are inconsistent or imprecise across sources. Kept unresolved rather than combining marketing terms with contradictory construction claims.")
    rows = [
        f("model_number", "vivo_y36_tra_model_code", "VIVO V2247 [Y36]; GSMArena also identifies the Snapdragon 680 Y36 as V2247", "V2247", status="VERIFIED_SECONDARY",
          note="Model code corroborated by a regulatory listing and an independent exact-model page. Philippine vivo pages identify the 4G configuration but do not publish the code."),
        f("global_release_date", "vivo_y36_id_sale", "vivo Indonesia reported the Y36 available for purchase in Glitter Aqua and Meteor Black on 2023-06-05", "2023-06-05",
          note="Earliest manufacturer sale-availability date located in this review; it is not represented as the first sale worldwide."),
        f("configuration", "vivo_y36_ph_store", "Selected Y36 Meteor Black 8GB+256GB (4G), SKU X1; separate Y36 5G is a different store listing", "8 GB RAM / 256 GB storage",
          note="Exact Philippine 4G configuration matched. The Y36 5G uses a separate listing/chipset and is not merged. vivo's additional 8 GB Extended RAM is software-backed and not counted as installed RAM."),
        f("philippine_release_date", "vivo_y36_ph_newsroom", "vivo Philippines newsroom says the Y36 launched in the Philippines on 2023-07-15", "2023-07-15", status="VERIFIED_SECONDARY",
          note="Official local newsroom announcement corroborates local launch and availability; no exact first-sale transaction time is claimed."),
        f("official_launch_price_php", "vivo_y36_ptg_ph", "PHP 12,999 Philippine official launch price for the vivo Y36 8GB/256GB 4G", 12999, status="VERIFIED_SECONDARY", unit="PHP",
          price_type="Historical Philippine launch price", price_observed="2023-07-15",
          note="Contemporaneous Philippine reporting; UNBOX PH independently identifies the 4G 8GB/256GB SKU and PHP 12,999 price."),
        f("current_price_php", "vivo_y36_ph_store", "PHP 10,999 including taxes; selected Y36 Meteor Black 8GB+256GB (4G), SKU X1; checked 2026-11-27", 10999, unit="PHP",
          price_type="Current official e-store listing price", price_observed=OBSERVED,
          price_condition="new", listing_status="Not verified",
          note="Dated price on the exact official PH e-store 4G SKU. Stock/checkout availability is not stated. The separate official PH product-specification page lists PHP 11,999 for the same memory configuration; that reference price is stored separately and the difference is not treated as an in-stock claim."),
        f("display_size", "vivo_y36_ph_specs", "6.64-inch", 6.64, key="displayInches", unit="in"),
        f("display_technology", "vivo_y36_ptg_ph", "IPS LCD", "IPS LCD", status="VERIFIED_SECONDARY", key="displayType",
          note="vivo's PH specifications identify LCD; PTG and YugaTech identify the panel as IPS LCD."),
        f("display_resolution", "vivo_y36_ph_specs", "2388 × 1080 (FHD+)", "1080 x 2388", key="resolution"),
        f("display_refresh_rate", "vivo_y36_ph_overview", "90 Hz refresh rate", "90", key="refreshHz", unit="Hz"),
        f("display_brightness", "vivo_y36_ph_overview", "650 nits High Brightness Mode", 650, unit="nits",
          note="Recorded using the manufacturer's term High Brightness Mode; not relabeled as sustained full-screen brightness."),
        nd("display_protection", "vivo_y36_ph_specs", "The reviewed Philippine specification page does not identify a named display cover-glass or protection standard."),
        f("chipset", "vivo_y36_ph_specs", "Qualcomm Snapdragon 680", "Qualcomm Snapdragon 680 (6 nm)", key="chipset",
          note="vivo Philippines confirms Snapdragon 680; Qualcomm confirms this platform's 6nm process."),
        f("process_node", "qualcomm_snapdragon_680", "Snapdragon 680 process technology: 6 nm", 6, unit="nm"),
        f("cpu", "vivo_y36_ptg_ph", "Octa-core: 4× Kryo 265 Gold up to 2.4 GHz + 4× Kryo 265 Silver up to 1.9 GHz", "4x Kryo 265 Gold @ 2.4GHz + 4x Kryo 265 Silver @ 1.9GHz",
          key="cpu", catalog_value="Octa Core CPU4x Kryo 265 Gold @ 2.4GHz + 4x Kryo 265 Silver @ 1.9GHz",
          status="VERIFIED_SECONDARY", note="Exact Y36 4G architecture as reported by the Philippine spec source; Qualcomm independently confirms Kryo 265 and a maximum CPU frequency of 2.4 GHz."),
        f("gpu", "qualcomm_snapdragon_680", "Qualcomm Adreno 610", "Adreno 610", key="gpu"),
        f("operating_system", "vivo_y36_ph_specs", "Funtouch OS 13 (based on Android 13)", "Android 13 with Funtouch OS 13", key="os"),
        nd("os_support", "vivo_y36_ph_specs", "No OS or security update support period is stated in the reviewed Philippine product material."),
        f("ram_capacity", "vivo_y36_ph_store", "8 GB installed RAM; up to 8 GB Extended RAM is software-backed", 8, key="ramGb", unit="GB",
          note="Physical configuration remains 8 GB. The manufacturer explicitly says extended RAM is software-realized; it is not counted as installed memory."),
        f("ram_type", "vivo_y36_unbox_ph", "8 GB LPDDR4X RAM", "LPDDR4X", status="VERIFIED_SECONDARY",
          note="Exact PH Y36 4G configuration as reported by UNBOX PH; vivo's local parameter page does not name the RAM type."),
        f("storage_capacity", "vivo_y36_ph_store", "256 GB", 256, key="storageGb", unit="GB"),
        f("storage_type", "vivo_y36_unbox_ph", "256 GB UFS 2.2 storage", "UFS 2.2", status="VERIFIED_SECONDARY",
          note="Exact PH Y36 4G configuration as reported by UNBOX PH; vivo's local parameter page does not name the storage type."),
        f("storage_expansion", "vivo_y36_ptg_ph", "Dedicated microSD expansion up to 1 TB", "Dedicated microSD up to 1 TB", status="VERIFIED_SECONDARY",
          note="The official PH specification confirms a separate microSD slot; PTG provides the 1 TB maximum."),
        f("rear_camera_system", "vivo_y36_ph_specs", "Rear: 50 MP main camera + 2 MP Bokeh camera", "50 MP main + 2 MP Bokeh", key="rearCameraMp", catalog_value=50, unit="MP",
          note="Manufacturer PH specification. The catalog numeric summary stores the main camera resolution only."),
        nd("main_camera_sensor", "vivo_y36_ph_specs", "The manufacturer specifies camera resolutions and apertures but does not name the camera sensor model."),
        na("ultrawide_camera", "vivo_y36_ph_specs", "The documented Philippine rear-camera setup lists 50 MP main and 2 MP Bokeh cameras; no ultrawide module is listed.", "Not applicable to the documented PH rear-camera setup; no ultrawide module is listed."),
        na("telephoto_camera", "vivo_y36_ph_specs", "The documented Philippine rear-camera setup lists 50 MP main and 2 MP Bokeh cameras; no telephoto module is listed.", "Not applicable to the documented PH rear-camera setup; no telephoto module is listed."),
        f("front_camera", "vivo_y36_ph_specs", "Front camera: 16 MP", 16, key="frontCameraMp", unit="MP"),
        f("video_recording", "vivo_y36_ptg_ph", "Up to 1080p video recording; frame rate not stated", "Up to 1080p video recording", key="video",
          status="VERIFIED_SECONDARY", note="The Philippine manufacturer page lists the MP4 container but not recording resolution or frame rate; PTG reports up to 1080p."),
        f("battery_capacity", "vivo_y36_ph_specs", "5000 mAh typical; 4900 mAh rated", 5000, key="batteryMah", unit="mAh",
          note="The manufacturer overview gives both figures; 5000 mAh is the typical-capacity value, not the rated capacity."),
        f("battery_technology", "vivo_y36_ptg_ph", "Li-Po battery; non-removable", "Li-Po; non-removable", status="VERIFIED_SECONDARY",
          note="Philippine secondary specification; vivo's local product page does not state battery chemistry or serviceability."),
        f("wired_charging", "vivo_y36_ph_specs", "44 W FlashCharge", 44, key="chargingW", unit="W"),
        nd("wireless_charging", "vivo_y36_ph_specs", "Wireless and reverse wireless charging are not specified in the reviewed manufacturer material; no unsupported 0 W value is assigned."),
        f("dimensions", "vivo_y36_ph_specs", "164.06 × 76.17 × 8.07 mm", "164.06 x 76.17 x 8.07 mm", key="dimensions", unit="mm"),
        f("weight", "vivo_y36_ph_specs", "202 g", 202, key="weightG", unit="g"),
        materials,
        f("ingress_protection", "vivo_y36_ph_overview", "IP54 dust and water ingress protection under normal use; vivo states the Y36 is not a professional waterproof phone", "IP54", note="Preserve vivo's normal-use caveat; do not describe the phone as waterproof."),
        f("sim_esim", "vivo_y36_ph_specs", "2 nano-SIM slots + 1 microSD; Dual SIM Dual Standby; eSIM not listed", "Dual nano-SIM, DSDS + dedicated microSD; eSIM not recorded", key="sim"),
        f("cellular_bands", "vivo_y36_ph_specs", "2G GSM 850/900/1800 MHz; 3G WCDMA B1/B5/B8; 4G FDD-LTE B1/B3/B5/B7/B8/B20/B28; TDD-LTE B38/B40/B41", "4G FDD B1/B3/B5/B7/B8/B20/B28; TDD B38/B40/B41; 3G B1/B5/B8; 2G GSM 850/900/1800", key="cellular"),
        f("wifi", "vivo_y36_ph_specs", "Wi-Fi 2.4 GHz / 5 GHz; PTG lists 802.11 b/g/n/ac", "Wi-Fi 802.11 b/g/n/ac, dual-band", key="wifi"),
        bluetooth,
        f("usb", "vivo_y36_ph_specs", "USB Type-C; OTG supported; transfer standard not stated", "USB Type-C; OTG supported", key="ports"),
        f("nfc", "vivo_y36_ptg_ph", "NFC: No in the Philippine Y36 listing; GSMArena notes NFC availability is market-dependent", "No NFC listed for the Philippine configuration", status="VERIFIED_SECONDARY",
          note="PH-specific secondary source lists no NFC. GSMArena's exact-model page says NFC is market/region-dependent, so its global statement is not applied to this PH configuration."),
        f("gnss", "vivo_y36_ph_specs", "GPS, BeiDou, GLONASS, Galileo and QZSS", "GPS, BeiDou, GLONASS, Galileo, QZSS"),
        f("audio", "vivo_y36_ptg_ph", "3.5 mm audio jack; 200% speaker volume with Audio Booster", "3.5 mm audio jack; Audio Booster up to 200% speaker volume", status="VERIFIED_SECONDARY", key="sound"),
        f("sensors", "vivo_y36_ph_specs", "Accelerometer, ambient light sensor, proximity sensor, e-compass, fingerprint sensor and gyroscope", "Accelerometer; ambient light; proximity; e-compass; fingerprint; gyroscope",
          note="Manufacturer PH specifications list all six sensors; local YugaTech/ PTG sources identify the fingerprint reader as side-mounted."),
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
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != CONFIG:
        raise ValueError("Unexpected workbook Y36 configuration set; review matching before proceeding.")

    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "vivo",
        "model": "Y36 4G",
        "configuration": "8 GB RAM / 256 GB storage",
        "configurationLabel": "8 GB RAM / 256 GB storage (4G, SKU X1)",
        "modelCode": "V2247",
        "sku": "X1",
        "sources": SOURCES,
        "fields": fields(),
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Verified Philippine availability: vivo Y36 4G (V2247), 8 GB / 256 GB; vivo Philippines newsroom reports launch on 2023-07-15. Current E-Store stock is not verified.",
            "philippineAvailability": "Verified Philippine availability: vivo Y36 4G, 8 GB / 256 GB; reported local launch 2023-07-15.",
            "observedAt": OBSERVED,
            "qualityFlag": "Manually reviewed; exact PH 4G configuration matched; stock, two source conflicts and thesis eligibility remain unresolved.",
            "catalogModel": "Y36 4G",
            "manufacturer": "vivo",
            "productLine": "Y",
            "modelNumber": "V2247",
            "philippineReleaseYear": 2023,
            "philippineDateLabel": "Reported Philippine launch date",
            "researchNotes": "Workbook row 166 labeled Y36 is matched to the Philippine vivo Y36 4G, model V2247, with one 8 GB / 256 GB configuration. The official PH e-store separately lists Y36 5G with a different chipset; that record is excluded from this match. The Commons photo labels the handset Y36 but shows a Chinese-market OriginOS 3 retail unit, so it is a model-level image only. Workbook study scope remains Pending.",
            "openIssues": [
                {"issue": "Current E-Store stock and checkout availability are not stated", "action": "Show PHP 10,999 as a dated listed price, not an in-stock offer."},
                {"issue": "The PH manufacturer parameter page lists PHP 11,999 while the selected E-Store SKU lists PHP 10,999", "action": "Keep both source-context prices in dated price evidence and identify the E-Store value as the observed SKU listing."},
                {"issue": "Local Bluetooth versions and rear-material descriptions conflict across sources", "action": "Leave both normalized values blank and expose their cited candidate evidence."},
                {"issue": "Study eligibility remains Pending", "action": "Keep workbook eligibility unchanged until the thesis screening rule is applied."},
            ],
        },
    }
    add_review(manual, catalog, review)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    saved_review = next(row for row in manual["records"]
                        if row.get("deviceId") == DEVICE and row.get("configurationId") == CONFIG)
    saved_review.update({"model": "Y36 4G", "configuration": "8 GB RAM / 256 GB storage",
                         "configurationLabel": "8 GB RAM / 256 GB storage (4G, SKU X1)"})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    image = images.get(DEVICE)
    if not image or image.get("sourcePage") != URL_IMAGE or image.get("credit") != "メイド理世 (Wikimedia Commons)":
        raise ValueError("The expected Y36 Commons image is missing or has changed; refusing to attach an unreviewed asset.")
    image.update({
        "scope": "Model-level Y36 image; Philippine variant not established",
        "usageTerms": "Creative Commons Attribution-Share Alike 4.0",
        "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
        "changes": "Converted to WebP for catalog delivery; no subject editing. Source photo labels the handset vivo Y36 and shows OriginOS 3 in a Chinese retail setting; it does not establish the Philippine firmware/configuration.",
        "rightsCheckedAt": OBSERVED,
    })
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 12999, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_y36_4g_v2247_8gb_256gb",
         "variant_ram_gb": 8, "variant_storage_gb": 256,
         "price_type": "historical_ph_launch_suggested_retail_price",
         "source_published_at": "2023-07-15",
         "excerpt": "Contemporaneous Philippine Y36 4G coverage reports PHP 12,999 for the 8 GB / 256 GB configuration.",
         "source_url": URL_PTG, "source_kind": "historical_local_launch_price_report",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 11999, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_y36_4g_8gb_256gb_manufacturer_parameter_page",
         "variant_ram_gb": 8, "variant_storage_gb": 256,
         "price_type": "current_official_parameter_page_reference_price",
         "source_published_at": None,
         "excerpt": "The official Philippine Y36 parameter page lists PHP 11,999 for 8GB+256GB when checked 2026-11-27; it is a product-page reference price, not a stock/checkout claim.",
         "source_url": URL_SPECS, "source_kind": "manufacturer_parameter_page_price",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "manufacturer_page_price_stock_not_verified"},
        {"device_id": DEVICE, "amount_php": 10999, "configuration_id": CONFIG,
         "configuration_match": "exact_selected_ph_y36_4g_8gb_256gb_meteor_black_sku_x1",
         "variant_ram_gb": 8, "variant_storage_gb": 256,
         "price_type": "current_official_e_store_list_price",
         "source_published_at": None,
         "excerpt": "Official PH e-store selected Y36 Meteor Black 8GB+256GB (4G), SKU X1 at PHP 10,999 including taxes on 2026-11-27; stock/checkout availability was not stated.",
         "source_url": URL_STORE, "source_kind": "current_official_store_listing",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "listed_stock_not_verified"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "vivo", "model_name": "Y36 4G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": item["url"], "source_kind": item["purpose"], "status": "reviewed", "result": item["note"]} for item in SOURCES],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    statuses = {}
    for row in review["fields"]:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    print(json.dumps({
        "workbookRow": 166, "model": "vivo Y36 4G", "modelNumber": "V2247",
        "configuration": review["configurationLabel"], "reviewedFields": len(review["fields"]),
        "fieldStatuses": statuses, "sources": len(SOURCES),
        "philippineLaunchDate": "2023-07-15", "launchPricePhp": 12999,
        "currentEStoreListingPhp": 10999, "manufacturerPagePricePhp": 11999,
        "stock": "not verified", "image": "model-level licensed Y36 image retained; regional firmware/configuration noted",
        "studyScope": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
