#!/usr/bin/env python3
"""Add source-reviewed Xiaomi Pad 6S Pro PH configurations and price evidence."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_0a08afaa2bffa0"
UNRECORDED = f"{DEVICE}-unrecorded"
MODEL = "Xiaomi Pad 6S Pro"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/xiaomi-pad-6s-pro-ph-prices-2026-11-27.json"

URL_GLOBAL_SPECS = "https://www.mi.com/global/product/xiaomi-pad-6s-pro-124/specs/"
URL_GLOBAL_PRODUCT = "https://www.mi.com/global/product/xiaomi-pad-6s-pro-124/"
URL_PH_FAQ = "https://www.mi.com/ph/support/faq/details/KA-118747/"
URL_SIM_FAQ = "https://www.mi.com/global/support/faq/details/KA-535907/"
URL_ANNUAL_REPORT = "https://ir.mi.com/system/files-encrypted/nasdaq_kms/assets/2024/04/25/5-36-08/2023%20Annual%20Report.pdf"
URL_YUGATECH = "https://www.yugatech.com/news/xiaomi-pad-6s-pro-lands-in-ph-sets-new-bar-for-tablets/"
URL_REVU = "https://www.revu.com.ph/2024/05/xiaomi-pad-6s-pro-12-4-price-philippines/"
URL_GIZGUIDE = "https://www.gizguide.com/2024/05/xiaomi-pad-6s-pro-ph-price.html"
URL_IWAREHOUSE = "https://iwarehouse.ph/products?brand=17"
URL_HOMECREDIT = "https://shoppingmall.homecredit.ph/brand/xiaomi-installment-loans"
URL_PRICEME = "https://ph.priceme.com/Xiaomi-Pad-6S-Pro-12.4in-8GB-256GB/p-923275422.aspx?sort=rating"
URL_GIGAHERTZ = "https://www.gigahertz.com.ph/products/xiaomi-pad-6s-pro-12-4"
URL_COMMONS_IMAGE = "https://commons.wikimedia.org/wiki/File:Xiaomi_Pad_6S_Pro.jpg"

VARIANTS = [
    {"ram": 8, "storage": 256, "label": "8 GB / 256 GB / Wi-Fi", "id": f"{DEVICE}-8gb-256gb-wifi",
     "launch": 33999, "current": 22999, "current_source": "iwarehouse_pad_6s_pro_listing",
     "current_note": "iWarehouse currently lists the exact 8 GB / 256 GB model at PHP 22,999 cash and says it is available at one location. Its stock notice says counts are informational and not reserved; call the store before visiting. Product condition is not stated."},
    {"ram": 12, "storage": 512, "label": "12 GB / 512 GB / Wi-Fi", "id": f"{DEVICE}-12gb-512gb-wifi",
     "launch": 39999, "current": 39999, "current_source": "homecredit_pad_6s_pro_listing",
     "current_note": "Home Credit's current Xiaomi listing shows the exact 12 GB / 512 GB tablet at PHP 39,999 with an installment purchase path. The page does not confirm physical inventory, immediate checkout, or product condition."},
]


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def sources() -> list[dict]:
    return [
        src("xiaomi_pad_6s_pro_global_specs", URL_GLOBAL_SPECS, "Xiaomi Global",
            "Manufacturer specifications for exact Xiaomi Pad 6S Pro 12.4 model",
            "Exact product specifications: display, chipset, memory configurations, cameras, battery, charging, USB, Wi-Fi, Bluetooth, NFC tag support, sensors, and launch operating system."),
        src("xiaomi_pad_6s_pro_global_product", URL_GLOBAL_PRODUCT, "Xiaomi Global",
            "Manufacturer product and accessory support page",
            "Product page identifies the Xiaomi Pad 6S Pro 12.4, Wi-Fi 7, six speakers, Dolby Vision/Atmos, 120W charging, battery, Xiaomi Focus Pen, and Touchpad Keyboard support."),
        src("xiaomi_pad_6s_pro_ph_faq", URL_PH_FAQ, "Xiaomi Philippines Support",
            "Manufacturer FAQ for hardware and connectivity details",
            "Official FAQ provides the 8/256 and 12/512 options, CPU/GPU details, battery min/typ values, camera sensors, storage expansion, charging, wireless charging, connectivity, audio, USB, sensors, body materials, and IP52 statement."),
        src("xiaomi_pad_6s_pro_sim_faq", URL_SIM_FAQ, "Xiaomi Global Support",
            "Manufacturer confirmation of cellular / SIM configuration",
            "The Xiaomi support FAQ explicitly says this model has no SIM slot and is designed for Wi-Fi-only connectivity."),
        src("xiaomi_pad_6s_pro_annual_report", URL_ANNUAL_REPORT, "Xiaomi Corporation",
            "Manufacturer annual report documenting launch month",
            "Xiaomi's 2023 Annual Report says it launched Xiaomi Pad 6S Pro 12.4 in February 2024; the Xiaomi support FAQ separately lists March 25, 2024 as a launch time, so an exact global release date is withheld.", "2024-04-25"),
        src("xiaomi_pad_6s_pro_xiaomi_faq_launch", URL_PH_FAQ, "Xiaomi Philippines Support",
            "Manufacturer FAQ launch-date statement retained for conflict review",
            "The FAQ's answer says the launch time was 03/25/2024 but does not specify whether that means global or Philippine retail launch. It conflicts with Xiaomi's annual report month and Philippine availability reports dated May 2; no exact local first-sale date is inferred."),
        src("xiaomi_pad_6s_pro_yugatech_ph", URL_YUGATECH, "YugaTech",
            "Dated Philippine launch availability, launch pricing, configuration, and image candidate",
            "Published 2024-05-02; says the Pad 6S Pro arrives in the Philippines, identifies 8/256 at PHP 33,999 and 12/512 at PHP 39,999, and reports May 3-9 promotional prices of PHP 31,199 and PHP 37,199. Also displays an exact-model product photograph; republication rights were not found.", "2024-05-02"),
        src("xiaomi_pad_6s_pro_revu_ph", URL_REVU, "REVU Philippines",
            "Independent Philippine launch-price cross-check and promotion conflict evidence",
            "Published 2024-05-02 and reports the same two launch prices/configurations. Its early-bird report gives PHP 31,999/PHP 37,999 through May 4 and an additional PHP 800 discount on May 5, differing from YugaTech's May 3-9 price window; both are retained as reported promotion observations, not reconciled into one offer.", "2024-05-02"),
        src("xiaomi_pad_6s_pro_gizguide_ph", URL_GIZGUIDE, "GIZGUIDE",
            "Independent Philippine availability, price, and configuration cross-check",
            "Published 2024-05-02; reports the model officially available in the Philippines and gives both local configurations, launch prices, and early-bird prices." , "2024-05-02"),
        src("iwarehouse_pad_6s_pro_listing", URL_IWAREHOUSE, "iWarehouse Philippines",
            "Current local cash-price and branch-availability observation for 8/256 GB",
            "As observed 2026-11-27, iWarehouse lists Xiaomi Pad 6S Pro Graphite Gray, 8GB/256GB, PHP 22,999 cash, available at one location. The site says stock is informational and not reserved and advises calling first; condition and exact branch stock are not specified."),
        src("homecredit_pad_6s_pro_listing", URL_HOMECREDIT, "Home Credit Shopping Mall Philippines",
            "Current exact-configuration retailer price listing for 12/512 GB",
            "As observed 2026-11-27, the live Xiaomi listing shows the 12GB/512GB Pad 6S Pro at PHP 39,999 and provides an installment purchase route. It does not establish condition or branch-level stock; retained as a dated listed price, not guaranteed availability."),
        src("priceme_pad_6s_pro_8_256", URL_PRICEME, "PriceMe Philippines",
            "Historical exact-configuration retailer quote and price trend",
            "PriceMe's history records Gigahertz at PHP 35,199 on 2026-05-06 for Xiaomi Pad 6S Pro 12.4 8GB/256GB. Gigahertz's current product page marks the item sold out, so the May quote is historical only."),
        src("gigahertz_pad_6s_pro_listing", URL_GIGAHERTZ, "Gigahertz Philippines",
            "Exact-model retailer specification and stock-state cross-check",
            "The product page identifies the exact 8/256 and 12/512 configurations and detailed specifications, but its 8/256 selection shows PHP 35,199 and Sold out / pickup unavailable. It is not treated as a current buyable offer."),
        src("xiaomi_pad_6s_pro_commons_image", URL_COMMONS_IMAGE, "Wikimedia Commons / 茅野ふたば",
            "Licensed exact-model image and attribution record",
            "Exact-model store-display photograph, visually checked against the Xiaomi Pad 6S Pro label. Creator credit is 茅野ふたば; Creative Commons Attribution-ShareAlike 4.0. The local WebP is a format conversion without subject edits; manifest preserves asset URL, credit, license, and source page."),
    ]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      candidate_evidence=None, **extra) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized,
           "note": note or "Exact Xiaomi Pad 6S Pro model checked against the cited source."}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if candidate_evidence:
        row["candidateEvidence"] = candidate_evidence
    row.update(extra)
    return row


def nd(fid: str, sid: str, value: str, note: str, unit: str | None = None) -> dict:
    return f(fid, sid, value, None, status="NOT_DISCLOSED", unit=unit, note=note)


def na(fid: str, sid: str, value: str, note: str) -> dict:
    return f(fid, sid, value, None, status="NOT_APPLICABLE", note=note)


def pending(fid: str, sid: str, value: str, note: str, unit: str | None = None,
            candidate_evidence=None) -> dict:
    return f(fid, sid, value, None, status="PENDING_VERIFICATION", unit=unit,
             note=note, candidate_evidence=candidate_evidence)


def conflict(fid: str, sid: str, value: str, note: str, candidates: list[dict], unit=None) -> dict:
    return f(fid, sid, value, None, status="CONFLICTING_INFORMATION", unit=unit,
             note=note, candidate_evidence=candidates)


def evidence(value: str, url: str, source_kind: str, excerpt: str,
             review_status: str = "CONFLICTING_INFORMATION", local=False) -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": "exact Xiaomi Pad 6S Pro model",
            "reviewStatus": review_status, "localAvailabilityVerified": local}


def make_fields(v: dict) -> list[dict]:
    config = f"{v['ram']} GB RAM / {v['storage']} GB storage / Wi-Fi-only"
    conf_evidence = [
        evidence("Xiaomi launch coverage identifies 8GB+256GB and 12GB+512GB Philippine configurations.", URL_YUGATECH,
                 "dated_philippine_launch_report", "Two PH configurations: 8GB+256GB and 12GB+512GB.", "VERIFIED_SECONDARY", True),
        evidence("Xiaomi global specs list 8GB+256GB and 12GB+512GB LPDDR5X/UFS 4.0 options.", URL_GLOBAL_SPECS,
                 "manufacturer_global_specs", "8GB+256GB, 12GB+512GB LPDDR5X RAM + UFS 4.0 storage.", "VERIFIED", False),
    ]
    global_date = conflict(
        "global_release_date", "xiaomi_pad_6s_pro_annual_report",
        "Xiaomi's annual report says launched in February 2024; Xiaomi support FAQ lists launch time 03/25/2024.",
        "The manufacturer gives two different launch timings. The annual report supports February 2024 at month precision, while the FAQ gives March 25 without defining market or launch event. Keep the exact global release date unresolved.",
        [evidence("February 2024", URL_ANNUAL_REPORT, "manufacturer_annual_report", "In February 2024, we launched the Xiaomi Pad 6S Pro 12.4.", "CONFLICTING_INFORMATION"),
         evidence("March 25, 2024", URL_PH_FAQ, "manufacturer_support_faq", "The launch time is 03/25/2024.", "CONFLICTING_INFORMATION")], "date")
    ph_date = conflict(
        "philippine_release_date", "xiaomi_pad_6s_pro_xiaomi_faq_launch",
        "Xiaomi Philippines Support says launch time 03/25/2024; Philippine launch coverage says the device arrived / was officially available on 2024-05-02.",
        "The Xiaomi FAQ does not identify the launch market/event. Local technology outlets reported Philippine availability on May 2, 2024. Preserve the conflicting date evidence and keep exact Philippine first-sale date blank; availability by May 2 is separately documented.",
        [evidence("March 25, 2024", URL_PH_FAQ, "manufacturer_support_faq", "FAQ answer: launch time is 03/25/2024; market scope not stated.", "CONFLICTING_INFORMATION", False),
         evidence("May 2, 2024", URL_YUGATECH, "dated_philippine_launch_report", "The Xiaomi Pad 6S Pro finally arrives in the Philippines.", "CONFLICTING_INFORMATION", True),
         evidence("May 2, 2024", URL_GIZGUIDE, "dated_philippine_launch_report", "The Xiaomi Pad 6S Pro 12.4 is now officially available in the Philippines.", "CONFLICTING_INFORMATION", True)], "date")

    current_field = f(
        "current_price_php", v["current_source"],
        v["current_note"], v["current"], status="VERIFIED_SECONDARY", unit="PHP",
        note="Dated retailer listing observed 2026-11-27 for the exact configuration. Listing/price provenance is retained; stock or condition is not guaranteed.",
        priceCondition="Not stated", priceType="Dated retailer listing",
        priceObservedAt=OBSERVED, listingStatus="Not verified")
    launch_price = f(
        "official_launch_price_php", "xiaomi_pad_6s_pro_yugatech_ph",
        f"Philippine launch coverage reports PHP {v['launch']:,} for {v['label']}.", v["launch"],
        status="VERIFIED_SECONDARY", unit="PHP",
        note="YugaTech and REVU independently report this configuration-specific Philippine launch price on 2024-05-02. Primary Xiaomi Philippine price markup was not located; the amount is retained as a secondary-reported launch SRP, not primary-source pricing.")

    rows = [
        pending("model_number", "xiaomi_pad_6s_pro_global_specs",
                "Reviewed Xiaomi global and Philippine specs identify the product family but do not state a regulatory or regional model number.",
                "Exact model number remains not recorded; do not assign a regional code based on a different market."),
        global_date,
        f("configuration", "xiaomi_pad_6s_pro_global_specs", config, config,
          note="This exact RAM/storage configuration is listed by Xiaomi globally and by Philippine launch coverage. Both local variants are Wi-Fi-only; accessories and color names are not separate configurations.", candidate_evidence=conf_evidence),
        ph_date,
        launch_price,
        current_field,
        f("display_size", "xiaomi_pad_6s_pro_global_specs", "12.4-inch diagonal", 12.4, key="displayInches", unit="in"),
        f("display_technology", "xiaomi_pad_6s_pro_global_specs", "LCD display", "LCD", key="displayType"),
        f("display_resolution", "xiaomi_pad_6s_pro_global_specs", "3048 × 2032 pixels, 294 ppi", "3048 x 2032", key="resolution"),
        f("display_refresh_rate", "xiaomi_pad_6s_pro_global_specs", "144Hz AdaptiveSync; listed automatic rates 30/48/50/60/90/120/144Hz", 144, key="refreshHz", unit="Hz"),
        f("display_brightness", "xiaomi_pad_6s_pro_global_specs", "700 nits typical; 900 nits High Brightness Mode", "700 nits typical; 900 nits HBM", unit="nits"),
        f("display_protection", "xiaomi_pad_6s_pro_global_specs", "Xiaomi global specs list DCI-P3, Dolby Vision, HDR10, DC dimming and TÜV display certifications; Xiaomi PH FAQ adds full lamination and an oleophobic layer.", "Fully laminated; oleophobic; DCI-P3; HDR10/Dolby Vision; DC dimming; TÜV low-blue-light/flicker-free/circadian certifications",
          candidate_evidence=[evidence("The screen is fully laminated and has an oleophobic layer.", URL_PH_FAQ, "manufacturer_ph_support_faq", "Xiaomi PH FAQ: the screen supports full laminating and has an oleophobic layer.", "VERIFIED")]),
        f("chipset", "xiaomi_pad_6s_pro_global_specs", "Snapdragon 8 Gen 2 Mobile Platform", "Qualcomm Snapdragon 8 Gen 2", key="chipset"),
        f("process_node", "xiaomi_pad_6s_pro_ph_faq", "4nm TSMC N4 manufacturing process", 4, unit="nm"),
        f("cpu", "xiaomi_pad_6s_pro_ph_faq", "8-core CPU, up to 3.19GHz; TSMC N4", "8-core CPU; up to 3.19GHz", key="cpu"),
        f("gpu", "xiaomi_pad_6s_pro_ph_faq", "Adreno 740 at 680MHz", "Adreno 740", key="gpu"),
        f("operating_system", "xiaomi_pad_6s_pro_revu_ph", "REVU reports Android 14-based Xiaomi HyperOS at local launch; Xiaomi's global specs call it Xiaomi HyperOS, Android U.", "Xiaomi HyperOS (Android 14 at launch)", key="os",
          status="VERIFIED_SECONDARY", note="REVU's Philippine launch coverage identifies Android 14-based HyperOS; Xiaomi's global spec says Xiaomi HyperOS, Android U. This records launch software only, not the currently installed version.",
          candidate_evidence=[evidence("Xiaomi HyperOS, Android U.", URL_GLOBAL_SPECS, "manufacturer_global_specs", "Operating System: Xiaomi HyperOS, Android U.", "VERIFIED")]),
        nd("os_support", "xiaomi_pad_6s_pro_ph_faq", "No guaranteed OS/security-support end date or update duration is published in the reviewed Xiaomi product specifications.", "Support duration and end date remain unrecorded; not inferred."),
        f("ram_capacity", "xiaomi_pad_6s_pro_global_specs", f"{v['ram']}GB RAM", v["ram"], key="ramGb", unit="GB"),
        f("ram_type", "xiaomi_pad_6s_pro_global_specs", "LPDDR5X", "LPDDR5X"),
        f("storage_capacity", "xiaomi_pad_6s_pro_global_specs", f"{v['storage']}GB", v["storage"], key="storageGb", unit="GB"),
        f("storage_type", "xiaomi_pad_6s_pro_global_specs", "UFS 4.0", "UFS 4.0"),
        f("storage_expansion", "xiaomi_pad_6s_pro_ph_faq", "Xiaomi explicitly says no expandable storage.", "No microSD / expandable internal storage"),
        f("rear_camera_system", "xiaomi_pad_6s_pro_global_specs", "50MP main camera + 2MP depth camera", "50MP main + 2MP depth", key="rearCameraMp", unit="MP"),
        f("main_camera_sensor", "xiaomi_pad_6s_pro_ph_faq", "S5KJN1 / JN1, 1/2.76-inch, f/1.8, 0.64μm pixels", "S5KJN1 / JN1; 1/2.76-inch; f/1.8"),
        na("ultrawide_camera", "xiaomi_pad_6s_pro_global_specs", "The manufacturer lists a main rear camera and a depth camera; it does not list a rear ultra-wide camera.", "No rear ultra-wide camera listed; the second rear module is a depth camera."),
        na("telephoto_camera", "xiaomi_pad_6s_pro_global_specs", "The manufacturer lists a main rear camera and a depth camera; it does not list a rear telephoto camera.", "No rear telephoto camera listed."),
        f("front_camera", "xiaomi_pad_6s_pro_global_specs", "32MP OV32D, f/2.2", 32, key="frontCameraMp", unit="MP"),
        f("video_recording", "xiaomi_pad_6s_pro_ph_faq", "Rear: 4K 30/60fps, 1080p 30/60fps, 720p 30fps; front: 1080p 30/60fps, 720p 30fps", "Rear 4K/60fps; front 1080p/60fps", key="video"),
        f("battery_capacity", "xiaomi_pad_6s_pro_global_specs", "10,000mAh typical / 9,800mAh minimum device capacity", 10000, key="batteryMah", unit="mAh",
          note="Xiaomi states device-level capacity as 10,000mAh typical and 9,800mAh minimum. Cell-level figures are 5,000mAh typical / 4,900mAh minimum and are not substituted for device-level capacity."),
        nd("battery_technology", "xiaomi_pad_6s_pro_ph_faq", "Xiaomi identifies the battery supplier (ATL) and high-voltage design but does not disclose battery chemistry in the reviewed FAQ.", "Battery chemistry not inferred."),
        f("wired_charging", "xiaomi_pad_6s_pro_global_specs", "120W Xiaomi HyperCharge", 120, key="chargingW", unit="W"),
        f("wireless_charging", "xiaomi_pad_6s_pro_ph_faq", "Xiaomi explicitly says wireless charging and reverse wireless charging are not supported.", "No wireless charging; no reverse wireless charging"),
        f("dimensions", "xiaomi_pad_6s_pro_global_specs", "278.70 × 191.58 × 6.26 mm", "278.70 x 191.58 x 6.26 mm", key="dimensions", unit="mm"),
        f("weight", "xiaomi_pad_6s_pro_global_specs", "590g", 590, key="weightG", unit="g"),
        f("materials", "xiaomi_pad_6s_pro_global_product", "Metal body; Xiaomi FAQ specifies metal middle bezel; back-cover material not separately identified.", "Metal body / metal middle bezel; back material not separately stated"),
        f("ingress_protection", "xiaomi_pad_6s_pro_ph_faq", "Xiaomi FAQ states IP52 waterproof level and notes water/dust damage is not covered by warranty.", "IP52"),
        f("sim_esim", "xiaomi_pad_6s_pro_sim_faq", "No SIM-card slot; Wi-Fi-only model, with no mobile-network data function.", "Wi-Fi only; no SIM/eSIM cellular service", key="sim"),
        na("cellular_bands", "xiaomi_pad_6s_pro_sim_faq", "Xiaomi confirms no SIM slot and no cellular/mobile-network data support.", "Cellular bands are not applicable to this Wi-Fi-only tablet."),
        f("wifi", "xiaomi_pad_6s_pro_global_specs", "Wi-Fi 7 (802.11a/b/g/n/ac/ax), 2.4GHz and 5GHz; MIMO, Wi-Fi Direct and Miracast", "Wi-Fi 7; dual band; MIMO", key="wifi"),
        f("bluetooth", "xiaomi_pad_6s_pro_global_specs", "Bluetooth 5.3; AAC, LDAC, LHDC 5.0, LC3 and Auracast", "Bluetooth 5.3"),
        f("usb", "xiaomi_pad_6s_pro_global_specs", "USB Type-C; USB 3.2 Gen 1 up to 5Gbps; Xiaomi PH FAQ confirms OTG and DP_OUT", "USB-C; USB 3.2 Gen 1 up to 5Gbps; OTG; DisplayPort output", key="ports",
          candidate_evidence=[evidence("USB Type-C supports OTG and DP_OUT.", URL_PH_FAQ, "manufacturer_ph_support_faq", "Xiaomi PH FAQ: OTG supported; wired video output supports DP_OUT.", "VERIFIED")]),
        pending("nfc", "xiaomi_pad_6s_pro_ph_faq", "Global Xiaomi materials list NFC tag support, but Xiaomi states NFC availability may differ by region.", "Keep PH NFC support unresolved; a global feature statement does not verify the Philippine variant."),
        nd("gnss", "xiaomi_pad_6s_pro_sim_faq", "Reviewed Wi-Fi-only manufacturer specifications do not state built-in GNSS/GPS availability for this configuration.", "GNSS remains not recorded; do not infer presence or absence from Wi-Fi-only status."),
        f("audio", "xiaomi_pad_6s_pro_ph_faq", "Six speakers; Type-C analog/digital wired headphone output; no 3.5mm jack stated", "Six speakers; USB-C audio output; no 3.5mm jack listed", key="sound"),
        f("sensors", "xiaomi_pad_6s_pro_global_specs", "G-sensor, gyroscope, light sensor, proximity sensor, e-compass, fingerprint sensor, hall sensor, flicker sensor, color-temperature sensor", "Accelerometer; gyroscope; light; proximity; compass; fingerprint; hall; flicker; color-temperature"),
        f("tablet_stylus", "xiaomi_pad_6s_pro_global_product", "Supports Xiaomi Focus Pen; sold separately in the Philippine launch report", "Xiaomi Focus Pen support; sold separately"),
        f("tablet_keyboard", "xiaomi_pad_6s_pro_global_product", "Supports Xiaomi Pad 6S Pro Touchpad Keyboard; accessory sold separately in PH launch coverage", "Xiaomi Pad 6S Pro Touchpad Keyboard support; sold separately"),
        f("tablet_cellular_variant", "xiaomi_pad_6s_pro_sim_faq", "Wi-Fi-only; no SIM slot or mobile data", "Wi-Fi only; no cellular modem", key="cellular"),
    ]
    if len(rows) != 49 or len({row["fieldId"] for row in rows}) != 49:
        raise ValueError(f"Expected 49 distinct tablet field reviews, got {len(rows)}")
    return rows


def availability() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine launch coverage reported the Xiaomi Pad 6S Pro officially available by 2024-05-02. Exact first sale date remains unresolved because Xiaomi's FAQ gives an ambiguous 2024-03-25 launch time.",
        "philippineAvailability": "Philippine availability reported by 2024-05-02; exact first authorized sale date unresolved.",
        "observedAt": OBSERVED,
        "qualityFlag": "Exact Philippine 8/256 and 12/512 Wi-Fi configurations and dated historical launch prices reviewed. Global and Philippine FAQ launch dates conflict in scope/timing; exact first-sale date, model number, region-specific NFC availability, and some current stock/condition details remain unresolved. Workbook eligibility remains Pending.",
        "catalogModel": MODEL, "manufacturer": "Xiaomi Corporation", "productLine": "Pad 6S Pro 12.4",
        "philippineReleaseYear": 2024,
        "philippineDateLabel": "Philippine availability reported by 2024-05-02; first-sale date unresolved",
        "researchNotes": "The exact model matches Xiaomi Pad 6S Pro 12.4. Philippine launch coverage supports two Wi-Fi configurations: 8/256 and 12/512. Xiaomi global specifications confirm the shared technical platform and Xiaomi's global support FAQ explicitly confirms no SIM slot. Local launch prices were PHP 33,999 and PHP 39,999. Current retailer listings observed 2026-11-27 show PHP 22,999 for 8/256 at iWarehouse (one listed location, stock not reserved) and PHP 39,999 for 12/512 at Home Credit (installment path shown, branch stock/condition not confirmed). A Gigahertz/PriceMe 8/256 observation of PHP 35,199 on 2026-05-06 is retained as historical; Gigahertz now marks it sold out. Xiaomi annual report says launched in February 2024 while an official FAQ gives March 25 without clarifying market; local coverage reports PH availability by May 2. Exact model number and first authorized local-sale date are not inferred. Xiaomi global and PH color names differ in sources; colors do not split hardware variants. The exact-model Wikimedia Commons photograph is cached in the project under CC BY-SA 4.0 with creator credit and license links in the image manifest. Study scope remains Pending.",
        "openIssues": [
            {"issue": "Manufacturer launch timing differs between annual report and support FAQ", "action": "Keep exact global release date unresolved and preserve both source statements."},
            {"issue": "Official FAQ launch date is not geographically scoped; Philippine coverage reports availability by 2024-05-02", "action": "Keep exact Philippine first-sale date blank; retain dated local availability evidence."},
            {"issue": "No regional / regulatory model number found", "action": "Do not infer a model code from another market."},
            {"issue": "Current retailer stock and product condition are not confirmed", "action": "Treat dated prices as retailer listings; iWarehouse advises calling because stock is not reserved."},
            {"issue": "Philippine NFC support is not established", "action": "Keep NFC unresolved because Xiaomi says regional availability may differ."},
            {"issue": "The licensed Commons image is a store-display photograph and may show accessories", "action": "Keep it labeled as a product image and preserve its creator credit, CC BY-SA 4.0 link, and unchanged-subject edit note in the image manifest."},
            {"issue": "Study scope is Pending in the source workbook", "action": "Preserve the workbook's eligibility status."},
        ],
    }


def make_review(v: dict, first: bool) -> dict:
    record = {"deviceId": DEVICE, "configurationId": v["id"], "brand": "Xiaomi",
              "model": MODEL, "configuration": v["label"], "configurationLabel": v["label"],
              "sources": sources(), "fields": make_fields(v), "availabilityEvidence": availability()}
    if first:
        record["replacementVariants"] = [
            {"id": item["id"], "label": item["label"],
             "notes": "Exact Philippine RAM/storage configuration; Wi-Fi-only is confirmed by Xiaomi; accessory and color are not separate configurations."}
            for item in VARIANTS]
        record["replaceUnrecordedPlaceholder"] = True
    else:
        record["replacementVariants"] = [{"id": v["id"], "label": v["label"],
             "notes": "Exact Philippine RAM/storage configuration; Wi-Fi-only is confirmed by Xiaomi."}]
    return record


def price_rows() -> list[dict]:
    out = []
    for v in VARIANTS:
        config = f"exact_{v['ram']}gb_{v['storage']}gb_wifi"
        common = {"device_id": DEVICE, "configuration_id": v["id"],
                  "configuration_match": config, "variant_ram_gb": v["ram"],
                  "variant_storage_gb": v["storage"], "variant_connectivity": "Wi-Fi-only"}
        out.extend([
            {**common, "amount_php": v["launch"], "price_type": "reported_ph_launch_srp_not_current_offer",
             "source_published_at": "2024-05-02", "observed_at": "2024-05-02",
             "source_url": URL_YUGATECH, "source_kind": "dated_philippine_launch_price_report",
             "local_availability_verified": True, "availability_status": "reported_ph_available_by_2024_05_02",
             "excerpt": f"YugaTech reports PHP {v['launch']:,} launch price for exact {v['label']} configuration; not a current price."},
            {**common, "amount_php": v["launch"], "price_type": "reported_ph_launch_srp_cross_check_not_current_offer",
             "source_published_at": "2024-05-02", "observed_at": "2024-05-02",
             "source_url": URL_REVU, "source_kind": "dated_philippine_launch_price_cross_check",
             "local_availability_verified": True, "availability_status": "reported_ph_available_by_2024_05_02",
             "excerpt": f"REVU reports the same PHP {v['launch']:,} launch price for exact {v['label']} configuration; not a current price."},
            {**common, "amount_php": 31199 if v["ram"] == 8 else 37199,
             "price_type": "historical_shopee_promo_yugatech_report_window_conflicts_with_revu",
             "source_published_at": "2024-05-02", "observed_at": "2024-05-03",
             "source_url": URL_YUGATECH, "source_kind": "dated_philippine_promo_price_report",
             "local_availability_verified": True, "availability_status": "reported_promo_window_2024_05_03_to_2024_05_09_not_current",
             "excerpt": f"YugaTech reported PHP {31199 if v['ram'] == 8 else 37199:,} for {v['label']} from May 3-9, 2024. REVU describes different early-bird pricing dates/amounts; this source-specific quote is retained, not generalized."},
            {**common, "amount_php": 31999 if v["ram"] == 8 else 37999,
             "price_type": "historical_shopee_early_bird_revu_report_conflicts_with_yugatech_window",
             "source_published_at": "2024-05-02", "observed_at": "2024-05-03",
             "source_url": URL_REVU, "source_kind": "dated_philippine_promo_price_report_with_conflicting_window",
             "local_availability_verified": True, "availability_status": "reported_early_bird_through_2024_05_04_not_current",
             "excerpt": f"REVU reported PHP {31999 if v['ram'] == 8 else 37999:,} through May 4, 2024 and an additional PHP 800 discount on May 5. YugaTech lists PHP {31199 if v['ram'] == 8 else 37199:,} for May 3-9; conflicting source terms are preserved."},
            {**common, "amount_php": v["current"],
             "price_type": "current_dated_retailer_listing_not_guaranteed_orderable_or_new",
             "source_published_at": None, "observed_at": OBSERVED,
             "source_url": URL_IWAREHOUSE if v["ram"] == 8 else URL_HOMECREDIT,
             "source_kind": "current_philippine_retailer_listing_stock_or_condition_not_confirmed",
             "local_availability_verified": False,
             "availability_status": "listed_on_2026_11_27_stock_or_orderability_not_confirmed",
             "excerpt": v["current_note"]},
        ])
    # Later exact 8/256 retailer quote. Gigahertz subsequently marked the item sold out.
    v = VARIANTS[0]
    out.append({"device_id": DEVICE, "amount_php": 35199, "configuration_id": v["id"],
                "configuration_match": "exact_8gb_256gb_wifi", "variant_ram_gb": 8,
                "variant_storage_gb": 256, "variant_connectivity": "Wi-Fi-only",
                "price_type": "historical_gigahertz_quote_sold_out_when_rechecked",
                "source_published_at": "2026-05-06", "observed_at": "2026-05-06",
                "source_url": URL_PRICEME, "source_kind": "philippine_price_aggregator_dated_retailer_quote",
                "local_availability_verified": False,
                "availability_status": "dated_2026_05_06_price_quote_gigahertz_current_page_sold_out",
                "excerpt": "PriceMe records Gigahertz at PHP 35,199 on 2026-05-06 for Xiaomi Pad 6S Pro 12.4 8GB/256GB. Rechecked Gigahertz page shows PHP 35,199 but Sold out / pickup unavailable."})
    return out


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the Pending workbook Xiaomi Pad 6S Pro record; refusing unexpected scope/device.")
    current_ids = {v.get("id") for v in device.get("variants", [])}
    expected_ids = {v["id"] for v in VARIANTS}
    replacing = current_ids == {UNRECORDED}
    already_integrated = current_ids == expected_ids
    if not (replacing or already_integrated):
        raise ValueError(f"Unexpected Xiaomi Pad 6S Pro configurations; refusing: {sorted(current_ids)}")

    for index, variant in enumerate(VARIANTS):
        # Keep the replacement instruction in the first review record because
        # catalog generation always starts from the unchanged workbook's
        # unconfigured placeholder, even when this review script is rerun.
        add_review(manual, catalog, make_review(variant, first=(index == 0)))
    deduplicate_target_reviews(manual, {(DEVICE, v["id"]) for v in VARIANTS})
    for variant in VARIANTS:
        saved = next(r for r in manual["records"] if r.get("deviceId") == DEVICE and r.get("configurationId") == variant["id"])
        if variant["id"] != VARIANTS[0]["id"]:
            for key in ("replacementVariants", "replaceUnrecordedPlaceholder", "additionalVariants"):
                saved.pop(key, None)
        saved.update({"brand": "Xiaomi", "model": MODEL, "configuration": variant["label"],
                      "configurationLabel": variant["label"]})
        source_updates = {s["id"]: s for s in sources()}
        saved["sources"] = [source_updates.get(s["id"], s) for s in saved.get("sources", [])]
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    # The image manifest already contains an exact-model Wikimedia Commons
    # photograph under CC BY-SA 4.0 with creator credit and visible site
    # attribution. Do not also mark this licensed image as unavailable.
    images.pop(DEVICE, None)
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = price_rows()
    snapshot = {"run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
                "models": [{"device_id": DEVICE, "brand": "Xiaomi", "model_name": MODEL,
                            "category": "tablets", "status": "manually_reviewed"}],
                "fetches": [], "observations": [],
                "discovery": [{"device_id": DEVICE, "source_url": s["url"], "source_kind": s["purpose"],
                               "status": "reviewed", "result": s["note"]} for s in sources()],
                "prices": prices}
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

    print(json.dumps({"model": MODEL, "configurations": [
        {"id": v["id"], "configuration": v["label"], "launchPricePhp": v["launch"],
         "currentListedPricePhp": v["current"], "currentPriceCondition": "Not stated",
         "listingStatus": "Not verified"} for v in VARIANTS],
        "reviewedConfigurations": len(VARIANTS), "reviewedFieldsPerConfiguration": 49,
        "philippineAvailability": "reported by 2024-05-02; exact first-sale date unresolved",
        "dateConflicts": "manufacturer annual report February vs FAQ March 25; local arrival reports May 2",
        "historicalPriceObservations": len(prices),
        "image": "exact-model Commons image retained with CC BY-SA 4.0 and creator attribution",
        "eligibility": "Pending"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
