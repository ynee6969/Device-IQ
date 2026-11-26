#!/usr/bin/env python3
"""Add exact-variant Philippine reviews for the OnePlus Nord 2 workbook row."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/oneplus-nord-2-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_15827b1eab335d"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_ONEPLUS_PRESS = "https://www.oneplus.com/global/press/press-release/OnePlus-Nord-2-5G-The-Next-Big-Step"
URL_ONEPLUS_SPECS = "https://www.oneplus.com/no/nord-2-5g/specs"
URL_ONEPLUS_MANUAL = "https://service.oneplus.com/content/dam/support/user-manuals/common/OnePlus_Nord_2_User_Manual_EN.pdf"
URL_NTC_AUG = "https://region7.ntc.gov.ph/wp-content/uploads/2024/01/GEC_08312021.pdf"
URL_NTC_SEPT = "https://caraga.ntc.gov.ph/wp-content/uploads/2021/11/GEC_09302021.pdf"
URL_YUGA = "https://www.yugatech.com/news/oneplus-nord-2-5g-specs-price-now-official/"
URL_MANILASHAKER = "https://manilashaker.com/oneplus-nord-2-5g-officially-launched-price-and-specifications/"
URL_MEDIATEK = "https://i.mediatek.com/dimensity-1200"
URL_DIGITALWALKER = "https://digitalwalker.ph/collections/oneplus/products/oneplus-nord-2"
URL_SHOPEE = "https://shopee.ph/OnePlus-Nord-2-%28DN2103%29-Dual-SIm-Nano-SIM-5G-12GB-256GB-Media-Tek-Dimensity-1200-AI-6.43-inch-Display-i.92926624.20934641209"
URL_IMAGE = "https://oasis.opstatics.com/content/dam/oasis/page/2021/ebba/spec/nord2_Gray_Sierra.png"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("nord2_oneplus_global_press", "OnePlus", URL_ONEPLUS_PRESS,
           "Manufacturer launch release, global model specifications, and software-update commitment",
           "OnePlus's press release is dated July 21, 2021. It identifies the Nord 2 5G's Dimensity 1200-AI platform, 50 MP Sony IMX766 main camera with OIS, 8 MP ultrawide, 32 MP selfie camera, 4,500 mAh battery, Warp Charge 65, OxygenOS 11.3, and a plan for two years of major Android updates plus three years of security updates. The update statement records the launch commitment, not a claim that each update was delivered.",
           "2021-07-21"),
    source("nord2_oneplus_official_specs", "OnePlus Support", URL_ONEPLUS_SPECS,
           "Manufacturer specifications for display, exact configurations, cameras, battery, connectivity, ports, sensors, and audio",
           "OnePlus's Nord 2 5G specifications page gives configuration ranges and product details. Its Norway path is regional; the Philippine DN2103 match is established separately by the local NTC record. Market-specific band activation and local carrier support are not inferred from the page alone."),
    source("nord2_oneplus_manual", "OnePlus Support", URL_ONEPLUS_MANUAL,
           "Manufacturer user manual for water-resistance wording and device operation",
           "The model-specific manual says the device is designed for water resistance under certain conditions and cautions against excessive submersion. It does not provide a formal IP rating."),
    source("nord2_ntc_aug_gec", "National Telecommunications Commission (NTC), Region VII", URL_NTC_AUG,
           "Philippine GEC evidence for DN2103 / Nord 2 5G and local applicant",
           "The NTC table lists ONEPLUS DN2103 / NORD 2 5G, applicant Digits Trading Corp, as a smartphone issued July 30, 2021. The table labels the record ESD-GEC-2106881."),
    source("nord2_ntc_sept_gec", "National Telecommunications Commission (NTC), Caraga", URL_NTC_SEPT,
           "Independent NTC copy cross-check for the Philippine DN2103 model",
           "This NTC copy also lists ONEPLUS DN2103 / NORD 2 5G for Digits Trading Corp, dated July 30, 2021, but shows ESD-GEC-2106851 rather than ESD-GEC-2106881. The model-code and marketing-name row agrees; the grant-number discrepancy is preserved rather than silently resolved."),
    source("nord2_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine launch date, preorder seller, exact local configurations/colors, launch prices, and local specification cross-check",
           "Published July 23, 2021. YugaTech reports the Nord 2 5G's Philippine unveiling and preorder through Digital Walker. It identifies Blue Haze 8 GB/128 GB at PHP 21,990 and Gray Sierra 12 GB/256 GB at PHP 25,990, along with the local specification list." ,
           "2021-07-23"),
    source("nord2_manilashaker_ph", "ManilaShaker Philippines", URL_MANILASHAKER,
           "Contemporaneous Philippine price/configuration, launch timing, and build cross-check",
           "Published July 24, 2021. ManilaShaker independently reports the two Philippine launch configurations and prices, preorder availability at Digital Walker, and Gorilla Glass 5 front/back construction. No frame material is asserted from this source.",
           "2021-07-24"),
    source("nord2_mediatek_dimensity1200", "MediaTek", URL_MEDIATEK,
           "Primary Dimensity 1200 platform process, CPU architecture, and GPU details",
           "MediaTek describes the Dimensity 1200 family as a 6 nm platform with Cortex-A78/Cortex-A55 CPU cores and Mali-G77 MC9 graphics. These are chipset-family specifications; the local phone's Dimensity 1200-AI identity is separately confirmed by OnePlus and Philippine launch sources."),
    source("nord2_digitalwalker_product", "Digital Walker Philippines", URL_DIGITALWALKER,
           "Current check of the Philippine product page linked from the 2021 launch source",
           "The Digital Walker Nord 2 product URL linked by YugaTech returned HTTP 404 when checked on November 26, 2026. This is evidence that the old page is unavailable, not proof that the model is discontinued or that no other seller has stock."),
    source("nord2_shopee_candidate", "Shopee Philippines marketplace / T&L Telecom Philippines", URL_SHOPEE,
           "Review of a present search-result marketplace price candidate for the 12 GB/256 GB model",
           "The listing title identifies Nord 2 DN2103 12 GB/256 GB and the result shows PHP 22,885 after voucher, but also marks it Sold Out. Its delivery estimate was November 2-9, 2026, already past at the November 26 review date; seller authorization, condition, and current purchasability are not established. The amount is retained only as a rejected stale/sold-out candidate, not a current price."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, catalog_value="__normalized__", unit=None, note: str,
          configuration_match: str, price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": configuration_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value == "__normalized__" else catalog_value
    if unit:
        item["unit"] = unit
    if price_type is not None:
        item["priceType"] = price_type
    return item


def fields_for(label: str, ram: int, storage: int, color: str,
               launch_price: int, *, current_source: str, current_value: str,
               current_status="UNAVAILABLE_AFTER_RESEARCH", current_normalized=None) -> list[dict]:
    match = f"Philippine OnePlus Nord 2 5G DN2103: {ram} GB RAM / {storage} GB storage / {color}"
    out = []

    def add(fid, sid, value, normalized, **kwargs):
        out.append(field(fid, sid, value, normalized,
                         configuration_match=match, **kwargs))

    add("model_number", "nord2_ntc_aug_gec", "NTC lists ONEPLUS DN2103 / NORD 2 5G for Digits Trading Corp; OnePlus official Nord 2 page matches the product family", "DN2103", status="VERIFIED", note="Exact Philippine model-code/marketing-name match. NTC record copies disagree on grant number (ESD-GEC-2106881 vs ESD-GEC-2106851); both show DN2103 / Nord 2 5G and July 30, 2021.")
    add("global_release_date", "nord2_oneplus_global_press", "OnePlus manufacturer press release dated July 21, 2021", "2021-07-21", status="VERIFIED", note="Uses the manufacturer press-release date. The Philippine seller announcement/preorder date was July 23, 2021.")
    add("configuration", "nord2_yugatech_ph", f"Philippine launch configuration: {ram} GB RAM / {storage} GB storage / {color}", f"{ram} GB RAM / {storage} GB storage / {color}", status="VERIFIED_SECONDARY", note="YugaTech maps this RAM/storage configuration to this Philippine color; the second local configuration is retained as a separate variant.")
    add("philippine_release_date", "nord2_yugatech_ph", "YugaTech reports Philippine unveiling and Digital Walker preorder beginning July 23, 2021", "2021-07-23", status="VERIFIED_SECONDARY", note="Reported local launch/preorder start date, not a claim about the first completed retail sale.")
    add("official_launch_price_php", "nord2_yugatech_ph", f"Philippine launch price PHP {launch_price:,} for {ram} GB / {storage} GB {color}", launch_price, unit="PHP", status="VERIFIED_SECONDARY", note="Historical Philippine launch price for this exact configuration; not a current offer.")
    add("current_price_php", current_source, current_value, current_normalized,
        status=current_status, unit="PHP" if current_normalized is not None else None,
        price_type="Shopee display price after voucher; sold out and stale; rejected as current price" if current_normalized is not None else None,
        note="No verified, currently purchasable Philippine offer for this exact configuration was found. The historical Digital Walker product URL now returns 404. A sold-out, stale marketplace result is retained only as a pending candidate, not as a current price.")
    add("display_size", "nord2_oneplus_official_specs", "6.43-inch display measured diagonally in the full rectangle", 6.43, key="displayInches", unit="in", status="VERIFIED", note="OnePlus lists 6.43 inches full-rectangle; its note gives 6.22 inches accounting for rounded corners.")
    add("display_technology", "nord2_oneplus_official_specs", "Fluid AMOLED", "Fluid AMOLED", key="displayType", status="VERIFIED", note="Manufacturer specification.")
    add("display_resolution", "nord2_oneplus_official_specs", "2400 x 1080 pixels, 20:9, 410 ppi", "1080 x 2400", key="resolution", status="VERIFIED", note="OnePlus product specification.")
    add("display_refresh_rate", "nord2_oneplus_official_specs", "90 Hz refresh rate", 90, key="refreshHz", unit="Hz", status="VERIFIED", note="Manufacturer specification.")
    add("display_brightness", "nord2_oneplus_official_specs", "No numeric typical or peak brightness value stated on the reviewed OnePlus specification page", None, status="NOT_DISCLOSED", note="No brightness value is inferred from display type or marketing language.")
    add("display_protection", "nord2_manilashaker_ph", "Corning Gorilla Glass 5 on the front", "Corning Gorilla Glass 5", status="VERIFIED_SECONDARY", note="Contemporaneous Philippine specification reports Gorilla Glass 5 on front and back; this field records the front display protection only.")
    add("chipset", "nord2_oneplus_global_press", "MediaTek Dimensity 1200-AI", "MediaTek Dimensity 1200-AI", key="chipset", status="VERIFIED", note="Manufacturer launch release; Philippine coverage reports the same chipset.")
    add("process_node", "nord2_mediatek_dimensity1200", "MediaTek Dimensity 1200 platform uses a 6 nm process", "6 nm", unit="nm", status="VERIFIED", note="Chipset process specification, not a handset fabrication claim.")
    add("cpu", "nord2_mediatek_dimensity1200", "Octa-core: 1 x Cortex-A78 up to 3.0 GHz + 3 x Cortex-A78 up to 2.6 GHz + 4 x Cortex-A55 up to 2.0 GHz", "1 x Cortex-A78 3.0 GHz + 3 x Cortex-A78 2.6 GHz + 4 x Cortex-A55 2.0 GHz", key="cpu", status="VERIFIED", note="MediaTek Dimensity 1200 platform specification; the phone's AI-tuned model name is separately listed by OnePlus.")
    add("gpu", "nord2_oneplus_official_specs", "ARM Mali-G77 MC9", "ARM Mali-G77 MC9", key="gpu", status="VERIFIED", note="OnePlus lists Mali-G77 MC9 for the handset; MediaTek identifies the same graphics family for Dimensity 1200.")
    add("operating_system", "nord2_oneplus_official_specs", "OxygenOS 11.3 based on Android 11 at launch", "OxygenOS 11.3 (Android 11)", key="os", status="VERIFIED", note="Manufacturer specification at launch; later software versions are not represented as the shipped OS.")
    add("os_support", "nord2_oneplus_global_press", "OnePlus promised two years of major Android updates and three years of security updates at launch", "Launch commitment: 2 years of major Android updates + 3 years of security updates", status="VERIFIED", note="Manufacturer's launch commitment; this record does not assert that every update was delivered to every regional SKU.")
    add("ram_capacity", "nord2_yugatech_ph", f"{ram} GB RAM", ram, key="ramGb", unit="GB", note="Exact Philippine launch configuration.")
    add("ram_type", "nord2_oneplus_official_specs", "LPDDR4X RAM", "LPDDR4X", status="VERIFIED", note="OnePlus lists LPDDR4X for its Nord 2 configurations.")
    add("storage_capacity", "nord2_yugatech_ph", f"{storage} GB storage", storage, key="storageGb", unit="GB", note="Exact Philippine launch configuration.")
    add("storage_type", "nord2_oneplus_official_specs", "UFS 3.1 storage", "UFS 3.1", status="VERIFIED", note="Manufacturer specification.")
    add("storage_expansion", "nord2_oneplus_official_specs", "No microSD or expandable-storage specification stated on the reviewed manufacturer pages", None, status="NOT_DISCLOSED", note="Silence is not treated as proof that a specific expansion path is impossible.")
    add("rear_camera_system", "nord2_oneplus_official_specs", "50 MP Sony IMX766 main with OIS + 8 MP ultrawide + 2 MP monochrome", "50 MP main + 8 MP ultrawide + 2 MP monochrome", key="rearCameraMp", catalog_value=50, status="VERIFIED", note="OnePlus's official specification gives the three camera roles; the catalog numeric field represents main-camera megapixels.")
    add("main_camera_sensor", "nord2_oneplus_official_specs", "50 MP Sony IMX766, f/1.88, optical image stabilization", "Sony IMX766, 50 MP, OIS", status="VERIFIED", note="Manufacturer specification; no separate sensor die-size measurement is recorded.")
    add("ultrawide_camera", "nord2_oneplus_official_specs", "8 MP ultrawide, 119.7-degree field of view, f/2.25, EIS", "8 MP ultrawide, 119.7-degree FOV", status="VERIFIED", note="Manufacturer specification.")
    add("telephoto_camera", "nord2_oneplus_official_specs", "No telephoto module; third rear lens is a 2 MP monochrome camera", "No telephoto camera listed", status="NOT_APPLICABLE", note="OnePlus identifies the third rear lens as monochrome, not telephoto.")
    add("front_camera", "nord2_oneplus_official_specs", "32 MP Sony IMX615, f/2.45", 32, key="frontCameraMp", unit="MP", status="VERIFIED", note="Manufacturer specification; this numeric field records resolution only.")
    add("video_recording", "nord2_oneplus_official_specs", "Rear: 4K 30 fps; 1080p 30/60 fps; 720p 30/60 fps; slow motion 1080p 120 fps and 720p 240 fps. Front: 1080p 30 fps and 720p 30 fps.", "Rear 4K30; 1080p30/60; 720p30/60; slow motion 1080p120/720p240. Front 1080p30/720p30.", status="VERIFIED", note="Mode and frame-rate combinations from the manufacturer specification.")
    add("battery_capacity", "nord2_oneplus_official_specs", "4,500 mAh typical dual-cell battery", 4500, key="batteryMah", unit="mAh", status="VERIFIED", note="OnePlus lists 4,500 mAh typical capacity; performance may vary.")
    add("battery_technology", "nord2_oneplus_official_specs", "Dual-cell battery; cell chemistry not stated", "Dual-cell; chemistry not recorded", status="VERIFIED", note="Only the manufacturer-published cell arrangement is recorded; lithium-polymer chemistry is not inferred.")
    add("wired_charging", "nord2_oneplus_global_press", "Warp Charge 65", 65, key="chargingW", unit="W", status="VERIFIED", note="Manufacturer launch release and specification list 65 W Warp Charge.")
    add("wireless_charging", "nord2_oneplus_official_specs", "Wireless or reverse charging support not specified in reviewed manufacturer materials", None, status="NOT_DISCLOSED", note="No support or absence is inferred from silence.")
    add("dimensions", "nord2_oneplus_official_specs", "159.12 x 73.31 x 8.25 mm", "159.12 x 73.31 x 8.25 mm", key="dimensions", unit="mm", status="VERIFIED", note="Manufacturer product specification.")
    add("weight", "nord2_oneplus_official_specs", "189 g; manufacturer notes measurement may vary by configuration/process", 189, key="weightG", unit="g", status="VERIFIED", note="Manufacturer product specification.")
    add("materials", "nord2_manilashaker_ph", "Gorilla Glass 5 front and back; frame material not recorded", "Gorilla Glass 5 front/back; frame not recorded", status="VERIFIED_SECONDARY", note="Contemporaneous Philippine coverage reports front/back glass protection. No frame material is inferred.")
    add("ingress_protection", "nord2_oneplus_manual", "OnePlus says the device is designed for water resistance under certain conditions; no formal IP rating is stated", "Water resistance under certain conditions; IP rating not recorded", status="VERIFIED", note="Manufacturer manual wording is not converted to an IP certification or immersion guarantee.")
    add("sim_esim", "nord2_oneplus_official_specs", "Dual nano-SIM slot; eSIM support not stated", "Dual nano-SIM; eSIM not recorded", key="sim", status="VERIFIED", note="Manufacturer lists two nano-SIM slots; eSIM is left unrecorded.")
    add("cellular_bands", "nord2_oneplus_official_specs", "4G LTE FDD B1/2/3/4/5/7/8/12/17/18/19/20/26/28/38/32/34/39/40/41/66; 5G NSA N1/3/7/8/20/28/38/41/78; 5G SA N1/3/7/20/28/78/41/8", "LTE FDD B1/2/3/4/5/7/8/12/17/18/19/20/26/28/38/32/34/39/40/41/66; NR NSA N1/3/7/8/20/28/38/41/78; NR SA N1/3/7/20/28/78/41/8", key="cellular", status="VERIFIED", note="OnePlus publishes these bands for its Nord 2 5G specifications page. It cautions network availability varies by carrier; the local NTC GEC's radio ranges are not treated as carrier-band validation.")
    add("wifi", "nord2_oneplus_official_specs", "Wi-Fi 802.11 a/b/g/n/ac/ax, 2.4/5 GHz, 2x2 MIMO", "Wi-Fi 6 (802.11ax), dual-band 2x2 MIMO", key="wifi", status="VERIFIED", note="Manufacturer specification.")
    add("bluetooth", "nord2_oneplus_official_specs", "Bluetooth 5.2; aptX, aptX HD, LDAC, AAC support listed", "Bluetooth 5.2", status="VERIFIED", note="Manufacturer specification.")
    add("usb", "nord2_oneplus_official_specs", "USB 2.0 Type-C; included Warp Type-C cable supports USB 2.0", "USB 2.0 Type-C", key="ports", status="VERIFIED", note="Manufacturer specification; charging power and data standard are separate capabilities.")
    add("nfc", "nord2_oneplus_official_specs", "NFC enabled", "Yes", status="VERIFIED", note="Manufacturer specification.")
    add("gnss", "nord2_oneplus_official_specs", "GPS, GLONASS, Galileo, BeiDou, NavIC", "GPS, GLONASS, Galileo, BeiDou, NavIC", status="VERIFIED", note="Manufacturer specification.")
    add("audio", "nord2_oneplus_official_specs", "Dual stereo speakers; noise-cancellation support", "Dual stereo speakers; noise-cancellation support", key="sound", status="VERIFIED", note="Manufacturer specification; this does not imply an included headset.")
    add("sensors", "nord2_oneplus_official_specs", "In-display fingerprint sensor, accelerometer, electronic compass, gyroscope, ambient-light sensor, SAR sensor, proximity sensor", "In-display fingerprint; accelerometer; electronic compass; gyroscope; ambient light; SAR; proximity", status="VERIFIED", note="Full sensor list as published by OnePlus.")

    if len(out) != 46:
        raise ValueError(f"Expected 46 reviewed phone fields, got {len(out)}")
    return out


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine launch and Digital Walker preorder reported July 23, 2021; NTC records local DN2103 equipment conformity for Digits Trading Corp. No currently purchasable exact-variant local price was verified.",
        "philippineAvailability": "YugaTech reports the OnePlus Nord 2 5G's Philippine unveiling and preorder at Digital Walker beginning July 23, 2021, with two exact local configurations: 8 GB / 128 GB Blue Haze at PHP 21,990 and 12 GB / 256 GB Gray Sierra at PHP 25,990. NTC records DN2103 / Nord 2 5G for Digits Trading Corp. Two NTC report copies disagree on the grant number (2106881 vs 2106851), while the model code, marketing name, applicant, and issue date agree. Workbook scope remains Pending.",
        "observedAt": OBSERVED,
        "manufacturer": "OnePlus",
        "productLine": "OnePlus Nord 2 5G",
        "modelNumber": "DN2103",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Reported Philippine launch/preorder start date",
        "researchNotes": "The workbook label OnePlus Nord 2 matches the Philippine-market Nord 2 5G model DN2103. OnePlus's manufacturer press release is dated July 21, 2021; local launch coverage reports preorder starting July 23. NTC records model DN2103 as Nord 2 5G for Digits Trading Corp on July 30, but two regional NTC report copies differ on the grant number (ESD-GEC-2106881 vs ESD-GEC-2106851), so both are retained as a source discrepancy. Philippine launch evidence supports two separate variants, Blue Haze 8/128 GB at PHP 21,990 and Gray Sierra 12/256 GB at PHP 25,990. OnePlus's published specification page provides detailed model specifications, while MediaTek supplies chipset-level process/CPU details. The Digital Walker URL linked from the 2021 article returned 404 on November 26, 2026. A Shopee result for DN2103 12/256 listed PHP 22,885 after voucher but marked the item Sold Out and displayed a stale November 2-9 delivery estimate; it is not treated as a current purchasable price. Current exact-variant prices remain Not recorded. The OnePlus product page links a Gray Sierra image, but reuse permission is not stated; the neutral placeholder remains. Workbook scope stays Pending.",
        "qualityFlag": "Philippine DN2103 model and two launch configurations verified; current purchasable prices not found; grant-number discrepancy retained; image reuse rights not established; workbook scope remains Pending",
        "openIssues": [
            {"issue": "NTC source copies label the DN2103 GEC record as both ESD-GEC-2106881 and ESD-GEC-2106851", "action": "Preserve both source references and do not silently choose a grant number; the DN2103 / Nord 2 5G identity is consistent."},
            {"issue": "No current purchasable price was established for either Philippine configuration", "action": "Keep current price blank; preserve the sold-out marketplace price only as a rejected, stale candidate."},
            {"issue": "The Shopee result is sold out and its displayed delivery window was already past at review time; item condition and seller authorization are unstated", "action": "Do not present PHP 22,885 as a current offer or use it for active price filtering."},
            {"issue": "The exact Digital Walker product page linked from the launch report now returns 404", "action": "Do not infer product discontinuation from the unavailable page alone."},
            {"issue": "OnePlus official Nord 2 image is associated with the Gray Sierra product page but has no stated reuse terms", "action": "Keep the neutral placeholder unless image reuse permission is documented."},
            {"issue": "Workbook scope/eligibility remains Pending", "action": "Preserve Pending and follow the existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "oneplus"
            or device.get("model") != "Nord 2"):
        raise ValueError("Inventory row no longer matches OnePlus Nord 2")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("OnePlus Nord 2 already has a manual review; inspect before replacing")

    variants = [
        {"id": f"{DEVICE}-8gb-128gb-ph", "label": "8 GB RAM / 128 GB storage — Blue Haze",
         "ram": 8, "storage": 128, "color": "Blue Haze", "price": 21990},
        {"id": f"{DEVICE}-12gb-256gb-ph", "label": "12 GB RAM / 256 GB storage — Gray Sierra",
         "ram": 12, "storage": 256, "color": "Gray Sierra", "price": 25990},
    ]
    evidence = availability_evidence()
    review_records = []
    for index, variant in enumerate(variants):
        current_source = "nord2_digitalwalker_product" if index == 0 else "nord2_shopee_candidate"
        current_value = (
            "No current exact 8 GB / 128 GB purchasable offer found; linked Digital Walker product page returned 404 on November 26, 2026"
            if index == 0 else
            "Shopee result showed PHP 22,885 after voucher for 12 GB / 256 GB DN2103 but marked Sold Out with a past delivery window; rejected as current price"
        )
        record = {
            "deviceId": DEVICE, "configurationId": variant["id"],
            "brand": "OnePlus", "model": "Nord 2",
            "configuration": variant["label"], "configurationLabel": variant["label"],
            "sources": SOURCES, "fields": fields_for(
                variant["label"], variant["ram"], variant["storage"], variant["color"],
                variant["price"], current_source=current_source, current_value=current_value,
                current_status="PENDING_VERIFICATION" if index == 1 else "UNAVAILABLE_AFTER_RESEARCH",
                current_normalized=22885 if index == 1 else None),
            "availabilityEvidence": evidence,
        }
        if index == 0:
            record["replacementVariants"] = [
                {"id": item["id"], "label": item["label"], "sku": None,
                 "modelCode": "DN2103",
                 "notes": f"Philippine launch variant: {item['color']}, {item['ram']} GB RAM / {item['storage']} GB storage. Model code DN2103."}
                for item in variants
            ]
            record["replaceUnrecordedPlaceholder"] = True
        review_records.append(record)

    manual["records"].extend(review_records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "OnePlus's official Nord 2 5G specifications page links a Gray Sierra product image, but no reusable image license or permission is stated. No image is embedded.",
        "sourcePage": URL_ONEPLUS_SPECS, "assetUrl": URL_IMAGE,
        "scope": "Exact OnePlus Nord 2 5G model, Gray Sierra color; image shown on OnePlus official model specifications page",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for OnePlus Nord 2",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 21990,
         "configuration_id": variants[0]["id"], "configuration_match": "exact",
         "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "historical_ph_launch_list_price",
         "source_published_at": "2021-07-23",
         "excerpt": "Philippine launch price PHP 21,990 for 8 GB / 128 GB Blue Haze.",
         "source_url": URL_YUGA, "source_kind": "historical_ph_launch_price_report",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 25990,
         "configuration_id": variants[1]["id"], "configuration_match": "exact",
         "variant_ram_gb": 12, "variant_storage_gb": 256,
         "price_type": "historical_ph_launch_list_price",
         "source_published_at": "2021-07-23",
         "excerpt": "Philippine launch price PHP 25,990 for 12 GB / 256 GB Gray Sierra.",
         "source_url": URL_YUGA, "source_kind": "historical_ph_launch_price_report",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 22885,
         "configuration_id": variants[1]["id"], "configuration_match": "exact_configuration_but_sold_out_and_stale",
         "variant_ram_gb": 12, "variant_storage_gb": 256,
         "price_type": "rejected_sold_out_marketplace_candidate_after_voucher",
         "source_published_at": None,
         "excerpt": "Shopee result displayed PHP 22,885 after voucher for DN2103 12 GB / 256 GB, but marked Sold Out and showed a November 2-9 delivery estimate already past at review time; not treated as current or purchasable. Condition and seller authorization not established.",
         "source_url": URL_SHOPEE, "source_kind": "sold_out_marketplace_price_candidate_not_current",
         "observed_at": OBSERVED_AT, "local_availability_verified": False,
         "availability_status": "sold_out_stale_listing_price_not_current"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "OnePlus", "model_name": "Nord 2", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": URL_DIGITALWALKER,
                       "result": "HTTP 404 on 2026-11-26; unavailable page is not proof of discontinuation"}],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "OnePlus Nord 2 workbook row -> Philippine Nord 2 5G / DN2103",
        "configurations": [v["label"] for v in variants],
        "reviewedFields": sum(len(x["fields"]) for x in review_records),
        "globalManufacturerRelease": "2021-07-21",
        "philippineLaunchPreorder": "2021-07-23",
        "launchPricesPhp": [v["price"] for v in variants],
        "currentPrices": "not recorded; only a sold-out stale marketplace candidate found",
        "image": unavailable[DEVICE]["status"],
        "scopeStatus": "Pending",
    }, indent=2))


if __name__ == "__main__":
    main()
