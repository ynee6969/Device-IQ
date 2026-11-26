#!/usr/bin/env python3
"""Record source-matched Philippine Black Shark 4 configurations."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/black-shark-4-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_fa4c0f6cdc39f6"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_BLACKSHARK = "https://global.blackshark.com/products/black-shark-4"
URL_IMAGE = "https://global.blackshark.com/cdn/shop/files/BS4_Black_Front_01_20210310.png?v=1751451918&width=1000"
URL_NTC = "https://caraga.ntc.gov.ph/wp-content/uploads/2021/11/GEC_09302021.pdf"
URL_NTC_LATER = "https://region7.ntc.gov.ph/wp-content/uploads/2024/01/GEC_08312021.pdf"
URL_REVU_RELEASE = "https://www.revu.com.ph/2021/04/black-shark-4-first-sale-day-in-ph/"
URL_REVU_PRICE = "https://www.revu.com.ph/2021/04/black-shark-4-price-in-philippines/"
URL_YUGA = "https://www.yugatech.com/gadget-reviews/black-shark-4-review-bang-for-the-buck-gaming-phone/"
URL_GSMARENA = "https://www.gsmarena.com/xiaomi_black_shark_4-10714.php"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/xiaomi-black-shark-4"
URL_QUALCOMM = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/prod_brief_qcom_sd870_5g.pdf"
URL_KIMSTORE = "https://www.kimstore.com/products/black-shark-4?variant=46915306291451"
URL_UNBOX_PRICE = "https://unbox.ph/gadget/black-shark-4-price-philippines-official/"

CONFIGS = [
    {"ram": 6, "storage": 128, "srp": 24950, "promo": 21950, "promo_date": "2021-05-10"},
    {"ram": 8, "storage": 128, "srp": 26990, "promo": 23950, "promo_date": "2021-04-28"},
    {"ram": 12, "storage": 128, "srp": 29990, "promo": 27450, "promo_date": "2021-05-10"},
    {"ram": 12, "storage": 256, "srp": 34990, "promo": 32990, "promo_date": "2021-04-28"},
]


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("black_shark_4_global_official", "Black Shark", URL_BLACKSHARK,
           "Manufacturer model identity, product finishes, and exact-model image source page",
           "The official global page identifies Black Shark 4 and the Mirror Black and Pale Gray finishes. It does not provide a detailed specification sheet or image reuse terms."),
    source("black_shark_4_ntc_gec", "National Telecommunications Commission (NTC)", URL_NTC,
           "Philippine model-code and local distributor evidence",
           "The NTC GEC entry identifies BLACK SHARK PRS-H0 as Black Shark 4, applicant Grimalkin Corporation, issued 2021-06-24. A later regional NTC copy transcribes the code as PS-H0 (without R); the 2021 GEC entry and the device's user manual identify PRS-H0.",
           "2021-09-30"),
    source("black_shark_4_ntc_later_transcription", "NTC Region 7", URL_NTC_LATER,
           "Cross-check of a conflicting later model-code transcription",
           "This later NTC list prints PS-H0 beside Black Shark 4, omitting the R found in the NTC GEC entry. It is retained as a transcription discrepancy, not used to create a second model code.",
           "2021-08-31"),
    source("black_shark_4_user_manual_mirror", "Black Shark 4 user manual (third-party mirror)",
           "https://device.report/m/aeeedd30908b87669e21381bb1bbb2a0bfb86110109ffd2905cf39a80c24dff1_optim.pdf",
           "Corroborating model-code evidence from the device manual",
           "The mirrored Black Shark 4 user manual names the model SHARK PRS-H0. The archive is not the manufacturer host; the NTC GEC remains the primary Philippine regulatory record."),
    source("black_shark_4_ph_revu_release", "REVU Philippines", URL_REVU_RELEASE,
           "Philippine sale timing, official-store presence, and local-market model identity",
           "Published 2021-04-23 and updated 2021-04-28. REVU reports the standard Black Shark 4 in the official Philippines stores operated by local distributor Grimalkin and says it would be available locally from 2021-04-28. The article explicitly distinguishes it from the 4 Pro.",
           "2021-04-23"),
    source("black_shark_4_ph_revu_price", "REVU Philippines", URL_REVU_PRICE,
           "Exact Philippine launch SRPs and dated official-store promotion prices by configuration",
           "Published 2021-04-28. The article reports separate 6/128, 8/128, 12/128, and 12/256 listings at official Black Shark Lazada/Shopee stores. Its listed SRPs are recorded separately from the dated online launch promotions.",
           "2021-04-28"),
    source("black_shark_4_ph_unbox_price", "Unbox PH", URL_UNBOX_PRICE,
           "Independent cross-check of Philippine launch pricing and configuration set",
           "The contemporaneous launch report independently lists the four Philippine SRPs and the 6/128, 8/128, and 12/128 promotional prices. REVU is used for the 12/256 promotional figure and exact availability dates.",
           "2021-04-27"),
    source("black_shark_4_ph_yugatech", "YugaTech", URL_YUGA,
           "Philippine hands-on review and device-specific technical specifications",
           "Hands-on review corroborates the 6/8/12 GB memory family, Snapdragon 870, cameras, battery, dimensions, weight, side power/fingerprint key, audio jack, Wi-Fi 6, connectivity, and historical Philippine configuration prices. The article has an isolated 6.5-inch display typo in one paragraph; its specification block and other sources give 6.67 inches. Its polycarbonate-back finding is in conflict with glass-back listings.",
           "2021-05-19"),
    source("black_shark_4_gsmarena", "GSMArena", URL_GSMARENA,
           "Independent full device specification cross-check",
           "The exact Black Shark 4 specification page corroborates the 6.67-inch Super AMOLED panel, 144 Hz, 1080 x 2400 resolution, 4500 mAh battery, camera modules, and network/audio/sensor fields. It lists a broader global RAM/storage family; only configurations separately evidenced by Philippine sources are included in this catalog.",
           "2021-03-23"),
    source("black_shark_4_nanoreview", "NanoReview", URL_NANOREVIEW,
           "Independent technical specification cross-check for display, build, and platform",
           "The exact model page lists separate rated and HDR display brightness values, display protection, dimensions, build material, chipset process, and platform details. Materials differ from YugaTech's hands-on observation and remain unresolved.",
           "2021-03-23"),
    source("qualcomm_snapdragon_870_brief", "Qualcomm", URL_QUALCOMM,
           "Primary chipset source for CPU/GPU, 5G, Wi-Fi, and Bluetooth platform capabilities",
           "Qualcomm's Snapdragon 870 brief names Kryo 585, Adreno 650, Wi-Fi 6, Bluetooth 5.2, and the X55 5G modem. Device-specific implementation values are cross-checked with the phone sources."),
    source("black_shark_4_kimstore_current", "KIMSTORE", URL_KIMSTORE,
           "Current exact-configuration Philippine retailer listing and dated price observation",
           "Observed 2026-11-26. The listing is selected at 8 GB RAM / 128 GB storage, shows PHP 20,545, says 'Only 1 left', and allows adding to cart. The listed item condition is not stated, so no new/used condition is assigned."),
]


def field(fid: str, source_id: str, value, normalized_value, *, status="VERIFIED_SECONDARY",
          key=None, catalog_value="__normalized__", unit=None, note: str, match: str,
          price_condition="__absent__", price_type=None, price_observed_at=None,
          listing_status=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": source_id,
            "sourceValue": value, "normalizedValue": normalized_value,
            "note": note, "configurationMatch": match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized_value if catalog_value == "__normalized__" else catalog_value
    if unit:
        item["unit"] = unit
    if price_condition != "__absent__":
        item["priceCondition"] = price_condition
    if price_type is not None:
        item["priceType"] = price_type
    if price_observed_at is not None:
        item["priceObservedAt"] = price_observed_at
    if listing_status is not None:
        item["listingStatus"] = listing_status
    return item


def fields_for(config: dict) -> list[dict]:
    ram, storage = config["ram"], config["storage"]
    label = f"Philippine {ram} GB physical RAM / {storage} GB storage configuration"
    match = label
    specs = []

    def add(fid, sid, value, normalized, **kwargs):
        specs.append(field(fid, sid, value, normalized, match=match, **kwargs))

    add("model_number", "black_shark_4_ntc_gec", "SHARK PRS-H0 (NTC GEC: BLACK SHARK PRS-H0)",
        "SHARK PRS-H0", status="VERIFIED",
        note="The 2021 NTC GEC maps PRS-H0 to Black Shark 4 under Grimalkin. A later regional list omits the R (PS-H0); this is documented as a source transcription conflict." )
    add("configuration", "black_shark_4_ph_revu_price", f"{ram} GB RAM / {storage} GB storage in the Philippine official-store launch list",
        f"{ram} GB RAM / {storage} GB storage", status="VERIFIED_SECONDARY",
        note="REVU's contemporaneous Philippines launch coverage lists this exact configuration in the official Black Shark store offers. The 4 Pro and other global-only configurations are excluded.")
    add("philippine_release_date", "black_shark_4_ph_revu_release", "REVU reports Philippine availability starting April 28, 2021",
        "2021-04-28", status="VERIFIED_SECONDARY",
        note="Reported start of Philippine availability, corroborated by contemporaneous local launch coverage; not an assertion of the first individual completed transaction.")
    add("official_launch_price_php", "black_shark_4_ph_revu_price", f"PHP {config['srp']:,} launch SRP for {ram}/{storage} GB",
        config["srp"], status="VERIFIED_SECONDARY", unit="PHP",
        note="Historical Philippine launch SRP from the official-store price list. Dated promo pricing is preserved separately and neither value is presented as a current offer.")
    if ram == 8 and storage == 128:
        add("current_price_php", "black_shark_4_kimstore_current",
            "PHP 20,545; exact 8 GB / 128 GB option selected; page says one unit left and offers Add to cart; condition not stated",
            20545, status="VERIFIED_SECONDARY", unit="PHP",
            note="A live Philippine retailer listing observed 2026-11-26. The page showed one remaining unit for the exact 8/128 selection. Product condition is not stated and remains Not recorded.",
            price_condition=None,
            price_type="KIMSTORE listing observed 2026-11-26; one unit left; condition not stated",
            price_observed_at=OBSERVED, listing_status="In stock")
    else:
        add("current_price_php", "black_shark_4_kimstore_current",
            "The current KIMSTORE page's selected offer is 8 GB / 128 GB; no current price for this configuration was established",
            None, status="PENDING_VERIFICATION", unit="PHP",
            note="Do not carry the historical launch SRP or another configuration's live listing price into this configuration.")

    add("display_size", "black_shark_4_gsmarena", "6.67-inch display; REVU and official product listings also use 6.67 inches",
        6.67, status="VERIFIED_SECONDARY", key="displayInches", unit="in",
        note="GSMArena and Philippine launch coverage agree at 6.67 inches. YugaTech's specification list agrees, although one paragraph contains an isolated 6.5-inch typo.")
    add("display_technology", "black_shark_4_ph_revu_price", "6.67-inch E4 AMOLED panel; global device sources identify Super AMOLED",
        "E4 Super AMOLED", status="VERIFIED_SECONDARY", key="displayType",
        note="Philippine launch coverage identifies Samsung E4 AMOLED; GSMArena also identifies Super AMOLED.")
    add("display_resolution", "black_shark_4_gsmarena", "1080 x 2400 pixels, 20:9",
        "1080 x 2400", key="resolution", note="Exact-model specification, cross-checked against local FHD+ launch sources.")
    add("display_refresh_rate", "black_shark_4_ph_revu_price", "Up to 144 Hz refresh; 720 Hz touch sampling",
        144, key="refreshHz", unit="Hz", note="The catalog refresh-rate value is 144 Hz; 720 Hz is touch sampling and is not substituted for refresh rate.")
    add("display_brightness", "black_shark_4_nanoreview", "500 nits rated maximum; up to 1,300 nits in HDR",
        "500 nits rated; up to 1,300 nits in HDR", note="Rated and HDR values are kept distinct. GSMArena and local reports describe 1,300 nits as peak/HDR; no single peak number is substituted for the rated value.")
    add("display_protection", "black_shark_4_nanoreview", "Tempered-glass protection listed; glass maker or grade not identified",
        "Tempered glass; maker/grade not recorded", note="The protective glass type is reported without inferring a Gorilla Glass generation.")
    add("chipset", "black_shark_4_ph_revu_price", "Qualcomm SM8250-AC Snapdragon 870 5G",
        "Qualcomm Snapdragon 870 5G", key="chipset", note="The Philippines launch source identifies the standard Snapdragon 870 model, not the Snapdragon 888 Black Shark 4 Pro.")
    add("process_node", "black_shark_4_nanoreview", "7 nm lithography process",
        "7 nm", note="Chipset-level manufacturing process; this is not a claim about the full handset.")
    add("cpu", "black_shark_4_gsmarena", "Octa-core: 1 x 3.2 GHz + 3 x 2.42 GHz + 4 x 1.80 GHz Kryo 585",
        "1 x 3.2 GHz + 3 x 2.42 GHz + 4 x 1.80 GHz Kryo 585", key="cpu",
        note="Device specification cross-checked with Qualcomm's Snapdragon 870 platform brief.")
    add("gpu", "qualcomm_snapdragon_870_brief", "Adreno 650 GPU",
        "Adreno 650", key="gpu", status="VERIFIED",
        note="Qualcomm identifies Adreno 650 as the Snapdragon 870 platform GPU; device-specific sources agree.")
    add("operating_system", "black_shark_4_gsmarena", "Android 11 with Joy UI 12.5",
        "Android 11; Joy UI 12.5", key="os", note="Operating system and UI at launch; later update state is not inferred.")
    add("os_support", "black_shark_4_nanoreview", "NanoReview currently lists an update-duration claim, but no official Black Shark support commitment was located",
        None, status="PENDING_VERIFICATION", note="No manufacturer-published OS/security support duration is verified. A secondary aggregator claim is retained as a lead only.")
    add("ram_capacity", "black_shark_4_ph_revu_price", f"{ram} GB physical RAM configuration",
        ram, key="ramGb", unit="GB", note="This exact local configuration is listed in contemporaneous Philippine launch material.")
    add("ram_type", "black_shark_4_gsmarena", "LPDDR5 RAM",
        "LPDDR5", note="Memory type reported for the standard Black Shark 4 family.")
    add("storage_capacity", "black_shark_4_ph_revu_price", f"{storage} GB internal storage configuration",
        storage, key="storageGb", unit="GB", note="This exact local configuration is listed in contemporaneous Philippine launch material.")
    add("storage_type", "black_shark_4_gsmarena", "UFS 3.1 internal storage",
        "UFS 3.1", note="Storage interface reported for the standard Black Shark 4 family.")
    add("storage_expansion", "black_shark_4_ph_yugatech", "Dual-SIM tray; no microSD provision",
        "No microSD expansion", status="VERIFIED_SECONDARY",
        note="YugaTech's hands-on describes the SIM tray and explicitly reports no microSD provision; GSMArena also lists no card slot.")
    add("rear_camera_system", "black_shark_4_ph_yugatech", "48 MP main + 8 MP 120-degree ultrawide + 5 MP macro cameras",
        "48 MP main, 8 MP ultrawide, 5 MP macro", key="rearCameraMp", catalog_value=48,
        note="Three rear camera modules; the catalog numeric value represents the primary camera only.")
    add("main_camera_sensor", "black_shark_4_ph_yugatech", "Sony IMX582 Exmor RS main sensor, 48 MP",
        "Sony IMX582 Exmor RS (48 MP main)", note="Sensor model reported in YugaTech's exact-device hands-on review.")
    add("ultrawide_camera", "black_shark_4_gsmarena", "8 MP f/2.2, 120-degree field of view",
        "8 MP f/2.2, 120-degree ultrawide", note="Exact-model rear ultrawide module.")
    add("telephoto_camera", "black_shark_4_gsmarena", "No telephoto module listed; rear system is main, ultrawide, and macro",
        "No telephoto module listed", status="NOT_APPLICABLE",
        note="This is a three-camera main/ultrawide/macro array; no telephoto module is listed.")
    add("front_camera", "black_shark_4_ph_yugatech", "20 MP f/2.0 front camera",
        20, key="frontCameraMp", unit="MP", note="Exact-model front-camera specification.")
    add("video_recording", "black_shark_4_ph_yugatech", "Rear video up to 4K at 60 fps with electronic stabilization; front video up to 1080p at 30 fps",
        "Rear up to 4K/60 fps with EIS; front up to 1080p/30 fps", key="video",
        note="Maximum modes listed in the reviewed device specification; stabilization behavior differs by recording mode.")
    add("battery_capacity", "black_shark_4_ph_revu_price", "4,500 mAh dual-cell battery",
        4500, key="batteryMah", unit="mAh", note="The local source identifies a dual-cell battery; reported capacity is total capacity.")
    add("battery_technology", "black_shark_4_kimstore_current", "4,500 mAh Li-Po battery, non-removable",
        "Lithium-polymer, non-removable", note="Listed by the Philippine retailer's exact-model specification block; cell chemistry is not separately stated by the manufacturer page.")
    add("wired_charging", "black_shark_4_ph_revu_price", "USB-C wired charging up to 120 W",
        120, key="chargingW", unit="W", note="Maximum wired charging rate listed for this model. Actual charging time depends on the supplied adapter and conditions.")
    add("wireless_charging", "black_shark_4_gsmarena", "Wireless charging capability is not specified in the reviewed device sources",
        None, status="NOT_DISCLOSED", note="No wireless or reverse-wireless charging capability is claimed in the reviewed specifications.")
    add("dimensions", "black_shark_4_gsmarena", "163.8 x 76.4 x 9.9 mm",
        "163.8 x 76.4 x 9.9 mm", key="dimensions", unit="mm", note="Exact-model dimensions; YugaTech's hands-on values round to 163.83 x 76.35 x 9.9 mm.")
    add("weight", "black_shark_4_gsmarena", "210 g",
        210, key="weightG", unit="g", note="Exact-model weight; corroborated in YugaTech's hands-on review.")
    add("materials", "black_shark_4_ph_yugatech", "YugaTech hands-on reports polycarbonate rear and metal frame; NanoReview and launch coverage list glass rear",
        None, status="CONFLICTING_INFORMATION",
        note="The reviewed sources conflict on rear-panel material. No single back material is published until the conflict is resolved; YugaTech reports an all-metal frame.")
    add("ingress_protection", "black_shark_4_gsmarena", "No IP certification/rating is listed in the reviewed exact-model specifications",
        None, status="NOT_DISCLOSED", note="No IP rating is inferred from the absence of a listing; this is not described as waterproof.")
    add("sim_esim", "black_shark_4_ph_yugatech", "Dual Nano-SIM tray; eSIM support not stated",
        "Dual Nano-SIM; eSIM not recorded", key="sim", note="Only physical SIM support is recorded; eSIM support is not inferred.")
    add("cellular_bands", "black_shark_4_ph_revu_price", "5G and 4G LTE handset; exact band list for the Philippine PRS-H0 unit not established",
        "5G / 4G LTE; exact bands not recorded", key="cellular",
        note="Local coverage identifies the 5G model. The NTC GEC row includes regulatory bands but does not provide a complete 5G band table for every carrier; carrier compatibility is not inferred.")
    add("wifi", "black_shark_4_ph_yugatech", "Wi-Fi 6 (802.11 a/b/g/n/ac/ax)",
        "Wi-Fi 6 (802.11ax)", key="wifi", note="Handset-level specification; Qualcomm platform documentation corroborates Wi-Fi 6 support.")
    add("bluetooth", "black_shark_4_gsmarena", "Bluetooth 5.2",
        "Bluetooth 5.2", note="Exact-model connectivity listing; platform source also lists Bluetooth 5.2 capability.")
    add("usb", "black_shark_4_kimstore_current", "USB Type-C; data transfer protocol/version not recorded",
        "USB Type-C; protocol not recorded", key="ports", note="Connector type is recorded without inferring USB data speed.")
    add("nfc", "black_shark_4_ph_yugatech", "NFC listed",
        "Yes", note="Exact-device specification cross-check. Regional hardware may vary; this is the reviewed global/Philippine model family.")
    add("gnss", "black_shark_4_ph_yugatech", "GPS, A-GPS, Galileo, GLONASS, BeiDou, and QZSS",
        "GPS, A-GPS, Galileo, GLONASS, BeiDou, QZSS", note="Navigation systems listed for the device; no regional performance claim is implied.")
    add("audio", "black_shark_4_ph_yugatech", "Stereo speakers, 3.5 mm headphone jack, and top/bottom speaker layout",
        "Stereo speakers; 3.5 mm audio jack", key="sound", note="YugaTech's hands-on describes the separate top and bottom speakers and 3.5 mm jack.")
    add("sensors", "black_shark_4_ph_yugatech", "YugaTech hands-on places the fingerprint reader in the power button; REVU's spec list says under-display",
        None, status="CONFLICTING_INFORMATION",
        note="Fingerprint placement conflicts between contemporaneous Philippines sources. The side-mounted power-button reader is supported by YugaTech and GSMArena, but the public field remains unresolved because REVU lists under-display.")

    if len(specs) != 45:
        raise ValueError(f"Expected 45 standard phone fields, got {len(specs)}")
    return specs


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "black shark"
            or device.get("model") != "4"):
        raise ValueError("The inventory row no longer matches standard Black Shark 4")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Black Shark 4 already has a manual review; inspect it before replacing")

    records = []
    for index, config in enumerate(CONFIGS):
        ram, storage = config["ram"], config["storage"]
        config_id = f"{DEVICE}-{ram}gb-{storage}gb-ph"
        label = f"{ram} GB RAM / {storage} GB storage"
        review = {
            "deviceId": DEVICE,
            "configurationId": config_id,
            "brand": "Black Shark",
            "model": "4",
            "configuration": label,
            "configurationLabel": label,
            "sources": SOURCES,
            "fields": fields_for(config),
        }
        if index == 0:
            review["replacementVariants"] = [{
                "id": f"{DEVICE}-{item['ram']}gb-{item['storage']}gb-ph",
                "label": f"{item['ram']} GB RAM / {item['storage']} GB storage",
                "sku": None,
                "modelCode": "SHARK PRS-H0",
                "notes": "Exact Philippines launch configuration listed by REVU at the official Black Shark stores operated by Grimalkin. Kept separate from other configurations; historical SRP is not a current price.",
            } for item in CONFIGS]
            review["replaceUnrecordedPlaceholder"] = True
            review["availabilityEvidence"] = {
                "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                "availabilityStatus": "The standard Black Shark 4 was listed in official Philippines stores operated by local distributor Grimalkin, with reported local availability from April 28, 2021. NTC GEC lists model PRS-H0 under Grimalkin.",
                "philippineAvailability": "Philippine availability is supported by contemporaneous official-store listings and local launch coverage; NTC GEC separately identifies Black Shark 4 / PRS-H0 under Grimalkin Corporation.",
                "observedAt": OBSERVED,
                "manufacturer": "Black Shark",
                "productLine": "Black Shark 4 Series",
                "modelNumber": "SHARK PRS-H0",
                "philippineReleaseYear": 2021,
                "philippineDateLabel": "Reported Philippine availability date",
                "researchNotes": "This workbook row matches the standard 2021 Black Shark 4, not the Snapdragon 888 Black Shark 4 Pro. Philippine sources identify four separate configurations: 6/128, 8/128, 12/128, and 12/256. 2021 launch SRPs remain historical price evidence. On 2026-11-26, KIMSTORE listed the exact 8/128 option at PHP 20,545 with one left and Add to cart; item condition was not stated, so the catalog leaves condition Not recorded. Other configurations have no verified current offer. A 2021 NTC GEC says PRS-H0 while a later regional transcription says PS-H0. YugaTech reports a polycarbonate rear while GSMArena/NanoReview list glass, and fingerprint placement also conflicts; those fields are not silently resolved. An exact official product image was located, but reuse rights are undocumented and the neutral placeholder remains.",
                "qualityFlag": "Later NTC model-code transcription differs; build-material and fingerprint descriptions conflict; current price varies by configuration",
                "openIssues": [
                    {"issue": "Later regional NTC copy transcribes the model code as PS-H0, while the original GEC says PRS-H0", "action": "Retain SHARK PRS-H0 based on the 2021 GEC mapping and device manual; keep the transcription discrepancy visible."},
                    {"issue": "Source descriptions conflict on rear-panel material and fingerprint-reader placement", "action": "Keep both fields unresolved in the public specification audit until a primary source or direct unit evidence resolves them."},
                    {"issue": "Current price is verified only for the 8 GB / 128 GB retailer listing; that page does not state item condition", "action": "Show PHP 20,545 only for 8/128 with condition Not recorded; leave current prices blank for the other variants."},
                    {"issue": "Official manufacturer product image reuse terms are not stated", "action": "Keep the neutral placeholder until a reusable license or written permission is documented."},
                    {"issue": "First completed Philippine retail transaction date is unknown", "action": "Treat 2021-04-28 as the reported local availability date, not a verified first transaction."},
                ],
            }
        records.append(review)

    manual["records"].extend(records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact-model Black Shark 4 front product image was identified on the official global product page, but no reusable image license or written permission is recorded.",
        "sourcePage": URL_BLACKSHARK,
        "assetUrl": URL_IMAGE,
        "scope": "Exact Black Shark 4, Mirror Black finish; image does not establish a particular RAM/storage configuration",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Black Shark 4",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for config in CONFIGS:
        config_id = f"{DEVICE}-{config['ram']}gb-{config['storage']}gb-ph"
        match = f"Philippine {config['ram']} GB / {config['storage']} GB configuration"
        prices.append({
            "device_id": DEVICE, "amount_php": config["srp"],
            "configuration_id": config_id, "configuration_match": "exact",
            "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
            "price_type": "historical_ph_launch_srp", "source_published_at": "2021-04-28",
            "excerpt": f"REVU reported the Philippine launch SRP of PHP {config['srp']:,} for {match}; not a current offer.",
            "source_url": URL_REVU_PRICE, "source_kind": "historical_official_store_price_report",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
            "availability_status": "historical_ph_launch_price_not_current",
        })
        prices.append({
            "device_id": DEVICE, "amount_php": config["promo"],
            "configuration_id": config_id, "configuration_match": "exact",
            "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
            "price_type": "historical_ph_launch_online_promotion", "source_published_at": "2021-04-28",
            "excerpt": f"REVU reported a dated PHP {config['promo']:,} online launch promotion for {match}, available from {config['promo_date']}; not a current offer.",
            "source_url": URL_REVU_PRICE, "source_kind": "historical_official_store_price_report",
            "observed_at": OBSERVED_AT, "local_availability_verified": True,
            "availability_status": "dated_ph_launch_promotion_not_current",
        })
    prices.append({
        "device_id": DEVICE, "amount_php": 20545,
        "configuration_id": f"{DEVICE}-8gb-128gb-ph", "configuration_match": "exact",
        "variant_ram_gb": 8, "variant_storage_gb": 128,
        "price_type": "current_ph_retailer_listing_condition_not_stated",
        "source_published_at": None,
        "excerpt": "KIMSTORE showed PHP 20,545 for the selected 8 GB / 128 GB Black Shark 4 option, said 'Only 1 left', and exposed Add to cart. Item condition was not stated.",
        "source_url": URL_KIMSTORE, "source_kind": "retailer_price_observation",
        "observed_at": OBSERVED_AT, "local_availability_verified": True,
        "availability_status": "listed_available_now_one_unit_condition_not_stated",
    })
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Black Shark", "model_name": "4", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [], "discovery": [], "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Standard Black Shark 4 / SHARK PRS-H0; not 4 Pro",
        "configurations": [f"{c['ram']}/{c['storage']}" for c in CONFIGS],
        "reviewedFields": sum(len(r["fields"]) for r in records),
        "philippineAvailability": "reported from 2021-04-28",
        "historicalSrpsPhp": [c["srp"] for c in CONFIGS],
        "currentListing": "8/128 at PHP 20,545, one remaining; condition not stated",
        "otherCurrentPrices": "not recorded",
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
