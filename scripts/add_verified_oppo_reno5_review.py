#!/usr/bin/env python3
"""Add a sourced Philippine review for the OPPO Reno5 workbook row."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/oppo-reno5-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_914fe6b0343102"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_OPPO_PH_AVAILABLE = "https://www.oppo.com/ph/newsroom/press/oppo-reno5-4g-5g-officially-available-philippines/"
URL_OPPO_PH_PREORDER = "https://www.oppo.com/ph/newsroom/press/oppo-reno5-preorder/"
URL_OPPO_SPECS = "https://www.oppo.com/en/smartphones/series-reno/reno5-4g/specs/"
URL_OPPO_PRODUCT = "https://www.oppo.com/en/smartphones/series-reno/reno5-4g/"
URL_NTC_GEC = "https://www.ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/GEC-2009-2021-Updated-.pdf"
URL_YUGA_LAUNCH = "https://www.yugatech.com/mobile/oppo-reno5-4g-5g-philippines-price/"
URL_YUGA_PRICE_LIST = "https://www.yugatech.com/mobile/smartphones-price-list-2021-philippines/"
URL_OPPO_PRICE_DROP = "https://www.oppo.com/ph/newsroom/press/oppo-reno5-4g-and-a15s-price-drop/"
URL_PTG_PRICE_LIST = "https://www.pinoytechnoguide.com/pricelists/oppo"
URL_GREENTELCOM_PRODUCT = "https://www.greentelcom.ph/shop/smartphones/oppo-reno5-4g-8gb-128gb/"
URL_GREENTELCOM_STOCK = "https://www.greentelcom.ph/product-tag/reno5-4g/"
URL_SHOPPABLE = "https://business.shoppable.ph/oppo-b.515/oppo-reno5-4g-cph2159-or-643-amoled-display-or-8gb-ram-128gb-storage-or-64mp-quad-camera-p.26191"
URL_GSMARENA = "https://www.gsmarena.com/compare.php3?idPhone1=10654"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-oppo-reno5"
URL_NANOREVIEW = "https://nanoreview.net/en/soc/qualcomm-snapdragon-720g"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/7-series/snapdragon-720g-mobile-platform"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("oppo_ph_available", "OPPO Philippines", URL_OPPO_PH_AVAILABLE,
           "Official Philippine release and availability evidence for both Reno5 4G and Reno5 5G",
           "OPPO states the Reno5 series became officially available in the Philippines on February 20, 2021, and lists separate 4G and 5G models with different prices and camera specifications.",
           "2021-02-20"),
    source("oppo_ph_preorder", "OPPO Philippines", URL_OPPO_PH_PREORDER,
           "Official preorder dates, launch prices, colors, and local availability date",
           "The Philippine release says preorder ran through February 19, 2021; reserved units could be claimed from February 20. It lists Reno5 4G at PHP 18,999 and colors Fantasy Silver / Starry Black, separately from Reno5 5G.",
           "2021-02-11"),
    source("oppo_global_specs", "OPPO Global", URL_OPPO_SPECS,
           "Manufacturer model-code match and detailed technical specifications for Reno5 4G",
           "OPPO identifies the product as Reno5 4G (CPH2159) and lists the 8 GB / 128 GB configuration, display, cameras, CPU/GPU, battery, bands, connectivity, sensors, operating system, and dimensions. The page does not state a global announcement date or software-support duration."),
    source("oppo_global_product", "OPPO Global", URL_OPPO_PRODUCT,
           "Manufacturer product page and exact-model image reference",
           "The product page is explicitly for OPPO Reno5 4G and describes its camera, display, charging, and audio features. Product pictures are marked for reference; the page does not grant image reuse rights."),
    source("oppo_ntc_gec", "National Telecommunications Commission (NTC), Philippines", URL_NTC_GEC,
           "Philippine equipment-conformity listing for OPPO model CPH2159",
           "The NTC list contains OPPO CPH2159. The same table separately names CPH2145 as Reno5 5G. OPPO's own specification page maps CPH2159 to Reno5 4G; the NTC row itself does not supply a marketing name for CPH2159."),
    source("oppo_yugatech_launch", "YugaTech Philippines", URL_YUGA_LAUNCH,
           "Contemporaneous Philippine launch report and exact memory / price configuration cross-check",
           "Published February 10, 2021. YugaTech reports the local Reno5 4G at 8 GB / 128 GB for PHP 18,999 and Reno5 5G as a separate 8 GB / 128 GB model at PHP 23,999; both were scheduled for Philippine availability from February 20.",
           "2021-02-10"),
    source("oppo_yugatech_price_list", "YugaTech Philippines", URL_YUGA_PRICE_LIST,
           "Year-end 2021 Philippine launch list cross-check",
           "Published January 18, 2021 and updated as of December 19, 2021. The list identifies Reno5 4G at PHP 18,999 with Snapdragon 720G and 8 GB / 128 GB, and lists Reno5 5G separately.",
           "2021-01-18"),
    source("oppo_official_price_drop", "OPPO Philippines", URL_OPPO_PRICE_DROP,
           "Historical official 2021 promotional price",
           "OPPO reported a temporary PHP 2,000 price reduction for Reno5 4G, from PHP 18,999 to PHP 16,999, with the offer ending July 31, 2021. This is historical, not a current offer."),
    source("oppo_ptg_price_list", "Pinoy Techno Guide", URL_PTG_PRICE_LIST,
           "Current price-guide candidate cross-check, not a seller offer",
           "The OPPO Philippines price-list page currently displays Reno5 4G at PHP 18,990. The page is a price guide, not a live seller listing, and does not establish stock, condition, or orderability."),
    source("oppo_greentelcom_product", "GreenTelcom Philippines", URL_GREENTELCOM_PRODUCT,
           "Retail listing candidate for exact 8 GB / 128 GB Reno5 4G",
           "The product page displays PHP 13,990 and add-to-cart / buy buttons for Reno5 4G 8 GB / 128 GB, but its current stock state is not explicit on that page."),
    source("oppo_greentelcom_stock", "GreenTelcom Philippines", URL_GREENTELCOM_STOCK,
           "Stock-status cross-check for GreenTelcom Reno5 4G listing",
           "The store's Reno5 4G category page marks its listing out of stock. That conflicts with the product page's purchase buttons, so the PHP 13,990 amount is not accepted as a confirmed purchasable offer."),
    source("oppo_shoppable_listing", "Shoppable Philippines", URL_SHOPPABLE,
           "Exact-model new-condition marketplace SRP candidate",
           "The page identifies CPH2159, 8 GB / 128 GB and displays SRP PHP 15,679 VAT-inclusive with condition New, but requires a request for quote and does not establish an exact checkout price or stock."),
    source("oppo_gsmarena_specs", "GSMArena", URL_GSMARENA,
           "Independent exact-model specifications cross-check",
           "GSMArena's Reno5 4G specification page identifies model CPH2159 and lists release timing, microSDXC, Wi-Fi, NFC, and hardware details. Manufacturer values remain primary where available; conflicts are retained."),
    source("oppo_kimovil_profile", "Kimovil", URL_KIMOVIL,
           "Secondary model-alias and configuration cross-check",
           "Kimovil aliases the Reno5 as CPH2159 and lists one 8 GB / 128 GB configuration. Its price module returned a zero-value placeholder and is not used as a price."),
    source("oppo_nanoreview_720g", "NanoReview", URL_NANOREVIEW,
           "Secondary Snapdragon 720G chipset profile reference",
           "Used only as a supplemental chipset cross-check; no benchmark score or inferred phone performance rating is added to the catalog."),
    source("oppo_qualcomm_720g", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 720G platform specifications",
           "Qualcomm lists the Kryo 465 CPU family, up to 2.3 GHz, Adreno 618 GPU, and 8 nm process node for Snapdragon 720G."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED",
          key=None, catalog_value=None, unit=None, note: str,
          configuration_match: str, price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": configuration_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        item["unit"] = unit
    if price_type is not None:
        item["priceType"] = price_type
    return item


def fields_for() -> list[dict]:
    match = "Philippine OPPO Reno5 4G (CPH2159), 8 GB RAM / 128 GB storage; Fantasy Silver and Starry Black colors"
    out: list[dict] = []

    def add(fid, sid, value, normalized, *, status="VERIFIED", key=None,
            catalog_value=None, unit=None, note, price_type=None):
        out.append(field(fid, sid, value, normalized, status=status, key=key,
                         catalog_value=catalog_value, unit=unit, note=note,
                         configuration_match=match, price_type=price_type))

    add("model_number", "oppo_ntc_gec", "NTC lists OPPO CPH2159; OPPO's model-specific page identifies Reno5 4G as CPH2159", "CPH2159", note="Exact model-code match supported by the NTC listing and OPPO's own Reno5 4G specification page. The NTC table separately lists CPH2145 as Reno5 5G.")
    add("global_release_date", "oppo_gsmarena_specs", "GSMArena lists announced December 31, 2020 and released January 9, 2021; Kimovil gives December 2020; OPPO's reviewed pages do not state a global date", None, status="CONFLICTING_INFORMATION", note="The model-specific secondary sources use different date labels/months, and the manufacturer pages do not resolve them. Leave one global release date unset; the Philippine availability date is separately verified as February 20, 2021.")
    add("configuration", "oppo_yugatech_launch", "Reno5 4G: 8 GB RAM / 128 GB storage; Fantasy Silver or Starry Black", "8 GB RAM / 128 GB storage; Fantasy Silver / Starry Black", status="VERIFIED_SECONDARY", note="Contemporaneous Philippine coverage gives the exact local memory configuration. OPPO's local page and global specification page corroborate the Reno5 4G identity and available colors. Colors share the same recorded memory configuration.")
    add("philippine_release_date", "oppo_ph_available", "OPPO Philippines states Reno5 4G was officially available in the Philippines starting February 20, 2021", "2021-02-20", note="Official Philippine availability date. OPPO's February 11 preorder notice says reservations could be claimed from February 20.")
    add("official_launch_price_php", "oppo_yugatech_launch", "Reno5 4G 8 GB / 128 GB Philippine launch price PHP 18,999; OPPO's local release confirms PHP 18,999 for the 4G model", 18999, status="VERIFIED_SECONDARY", unit="PHP", note="Historical launch list price for the exact local 8 GB / 128 GB Reno5 4G configuration; not a current offer.")
    add("current_price_php", "oppo_shoppable_listing", "Shoppable page displays SRP PHP 15,679 VAT-inclusive, condition New, for CPH2159 8 GB / 128 GB, but requires a quote; other current references show PHP 13,990 with stock unclear and a PHP 18,990 price-guide figure", 15679, status="PENDING_VERIFICATION", unit="PHP", note="Candidate only. Shoppable requires an RFQ; GreenTelcom's PHP 13,990 product page conflicts with its category page marking the model out of stock; Pinoy Techno Guide is a price list rather than a seller. No current purchasable price is verified, so the public catalog price stays blank.", price_type="Displayed SRP on new-condition RFQ listing; orderability and checkout price unverified")
    add("display_size", "oppo_global_specs", "6.4-inch display measured diagonally as a full rectangle", 6.4, key="displayInches", unit="in", note="Manufacturer-listed full-rectangle size; visible area is smaller around the rounded corners and camera cutout.")
    add("display_technology", "oppo_global_specs", "AMOLED rigid-screen panel", "AMOLED", key="displayType", note="Manufacturer specification.")
    add("display_resolution", "oppo_global_specs", "2400 x 1080 pixels, FHD+", "2400 x 1080", key="resolution", note="Manufacturer specification.")
    add("display_refresh_rate", "oppo_global_specs", "Maximum 90 Hz; selectable 90 Hz or 60 Hz", 90, key="refreshHz", unit="Hz", note="Manufacturer specification; lower selectable mode is 60 Hz.")
    add("display_brightness", "oppo_global_specs", "430 nits typical; up to 600 nits in sunlight (both stated as typical measurements)", "430 nits typical; 600 nits sunlight typical maximum", unit="nits", note="Values are retained with OPPO's typical-measurement wording.")
    add("display_protection", "oppo_gsmarena_specs", "GSMArena lists Corning Gorilla Glass 3; a Philippine retailer independently lists the same", "Corning Gorilla Glass 3", status="VERIFIED_SECONDARY", note="Secondary specifications agree; OPPO's reviewed spec sheet does not name a protection grade.")
    add("chipset", "oppo_global_specs", "Qualcomm Snapdragon 720G", "Qualcomm Snapdragon 720G", key="chipset", note="Manufacturer specification; Qualcomm platform page independently confirms the platform identity.")
    add("process_node", "oppo_qualcomm_720g", "Qualcomm Snapdragon 720G process node: 8 nm", "8 nm", unit="nm", note="Chipset-level manufacturer specification; this is not a separate measurement of the complete phone.")
    add("cpu", "oppo_qualcomm_720g", "Kryo 465 CPU, up to 2.3 GHz; OPPO lists an eight-core CPU", "Octa-core Qualcomm Kryo 465, up to 2.3 GHz", key="cpu", note="Qualcomm identifies Kryo 465 and maximum clock; OPPO specifies eight CPU cores. No unverified core-cluster breakdown is added.")
    add("gpu", "oppo_qualcomm_720g", "Qualcomm Adreno 618", "Qualcomm Adreno 618", key="gpu", note="Qualcomm and OPPO both identify Adreno 618.")
    add("operating_system", "oppo_global_specs", "ColorOS 11.1 based on Android 11.0", "ColorOS 11.1 (Android 11)", key="os", note="Launch-era manufacturer specification; not presented as a current installed version on every device.")
    add("os_support", "oppo_gsmarena_specs", "GSMArena records an Android 12 / ColorOS 12 upgrade path; OPPO's reviewed pages do not state an update commitment or support duration", "Android 12 / ColorOS 12 upgrade path reported by GSMArena; support duration not disclosed", status="VERIFIED_SECONDARY", note="This secondary database entry records an update path, not a promise that every regional unit received it or a support-end date.")
    add("ram_capacity", "oppo_global_specs", "8 GB RAM", 8, key="ramGb", unit="GB", note="The reviewed global specification page lists 8 GB RAM for this model configuration; local YugaTech coverage matches it.")
    add("ram_type", "oppo_global_specs", "LPDDR4x at 1866 MHz", "LPDDR4X", key="ramType", note="Manufacturer specification.")
    add("storage_capacity", "oppo_global_specs", "128 GB ROM", 128, key="storageGb", unit="GB", note="Exact Philippine configuration is cross-checked by contemporaneous local coverage.")
    add("storage_type", "oppo_global_specs", "Storage interface/type is not stated on the reviewed manufacturer specification page", None, status="NOT_DISCLOSED", note="No storage technology is inferred.")
    add("storage_expansion", "oppo_gsmarena_specs", "GSMArena lists a dedicated microSDXC slot; OPPO states external memory is supported", "Dedicated microSDXC slot; maximum capacity not recorded", status="VERIFIED_SECONDARY", note="The exact-model GSMArena entry specifies microSDXC, while OPPO independently confirms external-memory support. No maximum card capacity is inferred.")
    add("rear_camera_system", "oppo_global_specs", "64 MP main + 8 MP ultrawide + 2 MP macro + 2 MP monochrome", "64 MP main + 8 MP ultrawide + 2 MP macro + 2 MP monochrome", key="rearCameraMp", catalog_value=64, note="Manufacturer lists all four rear cameras; the catalog's numeric rear-camera field represents the main camera resolution.")
    add("main_camera_sensor", "oppo_global_specs", "64 MP main camera, f/1.7; sensor manufacturer/model not specified", "64 MP main, f/1.7; sensor model not disclosed", note="Manufacturer specification; no sensor identity or sensor size is inferred.")
    add("ultrawide_camera", "oppo_global_specs", "8 MP ultrawide, f/2.2, 119-degree field of view", "8 MP ultrawide, 119-degree FOV", note="Manufacturer specification.")
    add("telephoto_camera", "oppo_global_specs", "No telephoto module is listed; rear cameras are main, ultrawide, macro, and monochrome", "No telephoto camera listed", status="NOT_APPLICABLE", note="The manufacturer's four-camera list identifies the other modules; this is not a telephoto specification.")
    add("front_camera", "oppo_global_specs", "44 MP front camera, f/2.4", 44, key="frontCameraMp", unit="MP", note="Manufacturer specification; the numeric catalog field records resolution only.")
    add("video_recording", "oppo_global_specs", "Rear: 4K 30 fps; 1080p 30/60 fps; 720p 30/60 fps; slow motion 1080p 120/480 fps and 720p 240/960 fps. Front: 1080p/720p 30 fps; slow motion 1080p 120 fps and 720p 240 fps.", "Rear 4K30; 1080p30/60; 720p30/60; slow motion 1080p120/480 and 720p240/960. Front 1080p/720p30; slow motion 1080p120/720p240.", key="video", note="Mode and frame-rate values copied from OPPO's published specification; the very high slow-motion rates are retained as listed by the manufacturer.")
    add("battery_capacity", "oppo_global_specs", "4,220 mAh / 16.33 Wh minimum; 4,310 mAh / 16.67 Wh typical", 4310, key="batteryMah", unit="mAh", note="Catalog numeric value is the manufacturer's typical 4,310 mAh capacity; minimum capacity is also preserved in the field evidence.")
    add("battery_technology", "oppo_global_specs", "Lithium-ion polymer battery", "Lithium-ion polymer", note="Manufacturer specification.")
    add("wired_charging", "oppo_global_specs", "50 W Flash Charge; supplied 65 W adapter supports the phone's 50 W rate", 50, key="chargingW", unit="W", note="Phone charging rate is 50 W; the included adapter's 65 W rating is not substituted for the phone's maximum charge rate.")
    add("wireless_charging", "oppo_global_specs", "Wireless and reverse wireless charging are not stated on the reviewed manufacturer pages", None, status="NOT_DISCLOSED", note="No wireless-charging capability or absence is inferred from silence.")
    add("dimensions", "oppo_global_specs", "159.1 x 73.3 mm; 7.7 mm (Starry Black) or 7.8 mm (Fantasy Silver)", "159.1 x 73.3 x 7.7–7.8 mm", key="dimensions", unit="mm", note="Manufacturer lists color-specific thickness. The recorded colors are the Philippine color options.")
    add("weight", "oppo_global_specs", "About 171 g; OPPO notes variation by configuration, production, and measurement", 171, key="weightG", unit="g", note="Manufacturer specification.")
    add("materials", "oppo_global_specs", "Frame and back-cover materials are not stated on the reviewed manufacturer specification page", None, status="NOT_DISCLOSED", note="Display-glass protection is separately recorded from the retailer source; no frame or rear-cover material is inferred.")
    add("ingress_protection", "oppo_global_specs", "No IP rating or water-resistance certification stated on the reviewed manufacturer pages", None, status="NOT_DISCLOSED", note="No ingress rating or protection claim is inferred.")
    add("sim_esim", "oppo_global_specs", "Dual Nano-SIM supported; eSIM support not stated", "Dual Nano-SIM; eSIM not disclosed", key="sim", note="Manufacturer lists Nano-SIM support for both SIM slots; eSIM remains unrecorded.")
    add("cellular_bands", "oppo_global_specs", "2G GSM 850/900/1800/1900 MHz; 3G WCDMA bands 1/5/8; 4G FDD bands 1/3/5/7/8/20/28; 4G TD-LTE bands 38/40/41 (194 MHz)", "4G LTE; FDD 1/3/5/7/8/20/28; TDD 38/40/41; WCDMA 1/5/8; GSM 850/900/1800/1900", key="cellular", note="Manufacturer-published bands for the CPH2159 model. Carrier compatibility or local coverage is not inferred from the band list.")
    add("wifi", "oppo_gsmarena_specs", "GSMArena lists Wi-Fi 802.11 a/b/g/n/ac; OPPO lists 2.4 GHz and 5 GHz WLAN frequencies", "Wi-Fi 5 (802.11 a/b/g/n/ac), dual-band", key="wifi", status="VERIFIED_SECONDARY", note="Wi-Fi standard cross-checked with a secondary specification database; the manufacturer page provides supported frequency bands.")
    add("bluetooth", "oppo_global_specs", "Bluetooth 5.1; SBC, AAC, aptX HD, and LDAC codecs listed", "Bluetooth 5.1", note="Manufacturer specification.")
    add("usb", "oppo_global_specs", "USB Type-C, USB 2.0; USB OTG supported; 3.5 mm earphone jack", "USB Type-C (USB 2.0, OTG); 3.5 mm jack", key="ports", note="Manufacturer specification.")
    add("nfc", "oppo_global_specs", "OPPO states NFC is not supported; GSMArena lists NFC as present but market/region dependent", None, status="CONFLICTING_INFORMATION", note="The manufacturer and secondary model page conflict, with GSMArena noting regional variation. The Philippine CPH2159 NFC state is unresolved; do not display a definitive yes/no.")
    add("gnss", "oppo_global_specs", "GPS, BeiDou, GLONASS, Galileo, and QZSS; A-GPS, Wi-Fi, mobile-network, and electronic-compass positioning also listed", "GPS, BeiDou, GLONASS, Galileo, QZSS", note="Manufacturer specification.")
    add("audio", "oppo_gsmarena_specs", "GSMArena lists a loudspeaker and 3.5 mm jack; OPPO product page advertises Dolby Atmos; channel layout is not stated", "Loudspeaker; Dolby Atmos; 3.5 mm audio jack; channel layout not disclosed", key="sound", status="VERIFIED_SECONDARY", note="Speaker presence is secondary-source evidence; OPPO confirms Dolby Atmos and the headphone jack. No stereo-speaker claim is made.")
    add("sensors", "oppo_global_specs", "Geomagnetic sensor, proximity sensor, optical sensor, accelerometer, gravity sensor, gyroscope, and pedometer", "Geomagnetic, proximity, optical, accelerometer, gravity, gyroscope, pedometer", note="Full sensor list published by OPPO.")

    if len(out) != 46:
        raise ValueError(f"Expected 46 reviewed phone fields, got {len(out)}")
    source_ids = {item["id"] for item in SOURCES}
    missing_sources = sorted({item["sourceId"] for item in out} - source_ids)
    if missing_sources:
        raise ValueError(f"Missing source definitions: {missing_sources}")
    return out


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "OPPO Philippines reported official Reno5 4G availability beginning February 20, 2021; NTC lists model CPH2159 for Philippine OPPO Mobile Technology Inc. Workbook eligibility remains Pending.",
        "philippineAvailability": "OPPO Philippines states the Reno5 4G was officially available locally from February 20, 2021, and its NTC listing includes CPH2159. OPPO's model page identifies CPH2159 as Reno5 4G. The same Philippine release describes Reno5 5G separately; that model is not merged into this workbook's generic Reno5 row.",
        "observedAt": OBSERVED,
        "manufacturer": "OPPO",
        "catalogModel": "Reno5 4G",
        "productLine": "OPPO Reno5 4G",
        "modelNumber": "CPH2159",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Official Philippine availability start date",
        "researchNotes": "The workbook's raw claim lists only 'Reno5' and contains no source URL or connectivity suffix. OPPO's model-specific page calls the base product OPPO Reno5 4G and identifies it as CPH2159; the Philippine NTC list includes CPH2159, while separately naming CPH2145 as Reno5 5G. OPPO Philippines independently confirms that Reno5 4G and Reno5 5G were distinct Philippine products, so their specifications and prices are not combined. The 4G model's exact local configuration is 8 GB / 128 GB, with Fantasy Silver and Starry Black color options. OPPO says local availability began February 20, 2021; YugaTech reports the PHP 18,999 launch price. A 2021 official OPPO promotion temporarily lowered the price to PHP 16,999 through July 31, 2021. GSMArena reports an announcement on December 31, 2020 and a release on January 9, 2021, while Kimovil gives December 2020; OPPO's reviewed pages provide no global date, so no single date is assigned. OPPO says CPH2159 lacks NFC, while GSMArena's entry lists NFC as region-dependent; local NFC remains unresolved. GSMArena records an Android 12 / ColorOS 12 upgrade path, but OPPO does not state a software-support duration. Current price references conflict or are not checkout offers: Shoppable displays a new-condition SRP but requires a quote, GreenTelcom's product price conflicts with its category's out-of-stock label, and Pinoy Techno Guide is a price list rather than a seller. Current purchasable price remains unverified and blank. OPPO's official product page has exact-model images, but no reusable image permission was established; the neutral placeholder remains. Workbook scope stays Pending.",
        "qualityFlag": "Reno5 4G (CPH2159) matched; current price and image reuse are unverified.",
        "openIssues": [
            {"issue": "The original workbook claim says only Reno5 and does not give a model code or 4G/5G suffix", "action": "Match the base Reno5 label to OPPO's CPH2159 Reno5 4G page; preserve Reno5 5G (CPH2145) as a separate model and do not merge its fields."},
            {"issue": "Current price sources do not establish a single purchasable in-stock offer", "action": "Keep current price blank; retain exact-configuration price references as dated candidates with their stock/quote limitations."},
            {"issue": "OPPO's official page depicts the exact Reno5 4G, but image reuse permission is not stated", "action": "Keep the neutral placeholder until permitted use or written permission is documented."},
            {"issue": "Global date and NFC differ across secondary/model-region references; OPPO does not publish a global release date", "action": "Leave global date and Philippine NFC status unresolved; retain the source disagreement rather than choosing one value."},
            {"issue": "Workbook scope/eligibility remains Pending", "action": "Preserve Pending and follow the existing study eligibility rules."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "oppo"
            or device.get("model") != "Reno5"):
        raise ValueError("Inventory row no longer matches OPPO Reno5")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("OPPO Reno5 already has a manual review; inspect before replacing")

    variant = {
        "id": f"{DEVICE}-8gb-128gb-ph",
        "label": "8 GB RAM / 128 GB storage",
        "sku": None,
        "modelCode": "CPH2159",
        "notes": "Philippine OPPO Reno5 4G configuration. Available colors: Fantasy Silver and Starry Black; colors use this same memory configuration.",
        "workbookRow": 25,
    }
    evidence = availability_evidence()
    record = {
        "deviceId": DEVICE,
        "configurationId": variant["id"],
        "brand": "OPPO",
        "model": "Reno5",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "sources": SOURCES,
        "fields": fields_for(),
        "availabilityEvidence": evidence,
        "replacementVariants": [variant],
        "replaceUnrecordedPlaceholder": True,
    }
    manual["records"].append(record)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "OPPO's official Reno5 4G product page shows exact-model images, but the page marks pictures as references and does not state a reusable image license or permission. No image is embedded.",
        "sourcePage": URL_OPPO_PRODUCT,
        "assetUrl": None,
        "scope": "Exact OPPO Reno5 4G CPH2159 model; Fantasy Silver / Starry Black images are shown on the official model page",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for OPPO Reno5",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    config_id = variant["id"]
    prices = [
        {"device_id": DEVICE, "amount_php": 18999, "configuration_id": config_id,
         "configuration_match": "exact", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "historical_ph_launch_list_price", "source_published_at": "2021-02-10",
         "excerpt": "Reno5 4G 8 GB / 128 GB Philippine launch price PHP 18,999.",
         "source_url": URL_YUGA_LAUNCH, "source_kind": "historical_ph_launch_price_report",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 16999, "configuration_id": None,
         "configuration_match": "Reno5 4G model-level price; RAM/storage not repeated in promo source", "variant_ram_gb": None, "variant_storage_gb": None,
         "price_type": "historical_official_ph_promo_price", "source_published_at": None,
         "excerpt": "OPPO announced Reno5 4G at PHP 16,999 from its PHP 18,999 price during a promotion ending July 31, 2021; memory configuration is not repeated in that promotion page.",
         "source_url": URL_OPPO_PRICE_DROP, "source_kind": "historical_manufacturer_promotion",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_promotion_not_current"},
        {"device_id": DEVICE, "amount_php": 15679, "configuration_id": config_id,
         "configuration_match": "exact_model_memory_configuration_condition_new_quote_only", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "displayed_srp_new_condition_rfq_only_candidate", "source_published_at": None,
         "excerpt": "Shoppable displays SRP PHP 15,679 VAT-inclusive for OPPO Reno5 4G CPH2159, 8 GB / 128 GB, condition New; a quote is required and stock/checkout price are not confirmed.",
         "source_url": URL_SHOPPABLE, "source_kind": "marketplace_rfq_price_candidate_not_verified",
         "observed_at": OBSERVED_AT, "local_availability_verified": False,
         "availability_status": "quote_required_stock_not_verified"},
        {"device_id": DEVICE, "amount_php": 13990, "configuration_id": config_id,
         "configuration_match": "exact_model_memory_configuration_stock_conflict", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "displayed_retailer_price_stock_unverified_candidate", "source_published_at": None,
         "excerpt": "GreenTelcom product page displays PHP 13,990 and purchase buttons, but its Reno5 4G category page marks the model out of stock; not treated as purchasable.",
         "source_url": URL_GREENTELCOM_PRODUCT, "source_kind": "retailer_listing_price_stock_conflict",
         "observed_at": OBSERVED_AT, "local_availability_verified": False,
         "availability_status": "product_stock_conflict_not_verified"},
        {"device_id": DEVICE, "amount_php": 18990, "configuration_id": config_id,
         "configuration_match": "exact_model_price_guide_no_seller_offer", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "price_guide_reference_not_store_offer", "source_published_at": None,
         "excerpt": "Pinoy Techno Guide's OPPO price list displays Reno5 4G at PHP 18,990; the guide does not establish live stock, condition, or an orderable seller offer.",
         "source_url": URL_PTG_PRICE_LIST, "source_kind": "philippine_price_guide_candidate",
         "observed_at": OBSERVED_AT, "local_availability_verified": False,
         "availability_status": "price_guide_only_not_verified_offer"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "OPPO", "model_name": "Reno5", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_SHOPPABLE, "result": "Exact new-condition listing displays SRP but requires quote; current checkout amount and stock not confirmed."},
            {"device_id": DEVICE, "source_url": URL_GREENTELCOM_PRODUCT, "result": "Exact 8 GB / 128 GB product page displays PHP 13,990; category page says out of stock, so not accepted as purchasable."},
            {"device_id": DEVICE, "source_url": URL_PTG_PRICE_LIST, "result": "Price guide lists PHP 18,990; no live seller inventory or checkout offer established."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "OPPO Reno5 workbook row -> Philippine OPPO Reno5 4G / CPH2159; Reno5 5G remains separate",
        "configuration": variant["label"],
        "reviewedFields": len(record["fields"]),
        "philippineAvailability": "2021-02-20",
        "historicalLaunchPricePhp": 18999,
        "currentPrice": "not verified; exact-model candidate prices preserved in audit",
        "image": unavailable[DEVICE]["status"],
        "scopeStatus": "Pending",
    }, indent=2))


if __name__ == "__main__":
    main()
