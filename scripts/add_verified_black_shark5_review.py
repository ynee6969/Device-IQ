#!/usr/bin/env python3
"""Add a source-backed Philippine review for the standard Black Shark 5."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/black-shark-5-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_a9d69522a3d0fe"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_OFFICIAL = "https://global.blackshark.com/products/black-shark-5"
URL_IMAGE = "https://global.blackshark.com/cdn/shop/files/5-Mirror-Black-back.png?v=1750929394&width=1000"
URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_MANUAL = "https://drv.dns-shop.ru/drivers%2FManuals%2FB%2Fblack-shark-5_instrukcia_230604_20022025.pdf"
URL_FCC = "https://fccid.io/m/bb15278ddda91619447401bb44747e13cf0a90a231a5feee1d40b14370dd656a.pdf"
URL_YUGA = "https://www.yugatech.com/mobile/black-shark-5-pro-now-official-price-philippines/"
URL_REVU = "https://www.revu.com.ph/2022/06/black-shark-5-pro-price-philippines/"
URL_GSMARENA = "https://www.gsmarena.com/xiaomi_black_shark_5-11454.php"
URL_QUALCOMM = "https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/prod_brief_qcom_sd870_5g.pdf"
URL_BERMOR = "https://bermorzone.com.ph/shop/gadgets/mobile-phones/xiaomi-black-shark-5-8gb-12gb128gb-256gb-gray-black/"
URL_ALT_SPECS = "https://blackshark.gg/pages/specs-blackshark5"
URL_ALT_TERMS = "https://blackshark.gg/pages/terms-of-service"

CONFIGS = [
    {"ram": 8, "storage": 128, "srp": 26999, "promo": 25999, "current": 24995, "regular": 27000},
    {"ram": 12, "storage": 256, "srp": 34999, "promo": 33999, "current": 32450, "regular": 35000},
]


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("black_shark_5_global_product", "Black Shark (Global)", URL_OFFICIAL,
           "Manufacturer product identity, color options, and exact-model image source page",
           "The product page names Black Shark 5 and lists Mirror Black and Explorer Grey. An exact Mirror Black product image is available from its CDN. The page does not state image reuse permission; the asset is therefore not embedded."),
    source("black_shark_5_ntc_gec", "National Telecommunications Commission (NTC)", URL_NTC,
           "Philippine GEC record for the SHARK PAR-H0 radio model code",
           "The 2022 NTC GEC list contains two BLACK SHARK entries for SHARK PAR-H0. It does not name the marketing model in those rows. The model name is matched through the device manual and manufacturer page, not inferred from the code alone.",
           "2022"),
    source("black_shark_5_manual_mirror", "Black Shark 5 user manual (manufacturer manual mirrored by DNS-Shop)", URL_MANUAL,
           "Model-code, SIM/port layout, and user-facing hardware control evidence",
           "The manual identifies the handset as Black Shark 5, model SHARK PAR-H0, and its diagram labels the side power/fingerprint key, dual gaming triggers, SIM tray, and USB Type-C port. The PDF is mirrored by a retailer rather than hosted on the manufacturer domain."),
    source("black_shark_5_fcc_report", "FCC test report for Blackshark Technologies (Nanchang) Co., Ltd.", URL_FCC,
           "Corroborating manufacturer and model-code identity",
           "The certification report names Blackshark Technologies (Nanchang) Co., Ltd., BLACK SHARK, and model SHARK PAR-H0. It is hosted by FCC ID rather than the manufacturer; the NTC list remains the Philippine regulatory record.",
           "2022-03-28"),
    source("black_shark_5_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Contemporaneous Philippine launch, official sale timing, variants, prices, and local technical specifications",
           "Published June 27, 2022. YugaTech reports the standard Black Shark 5 (not 5 Pro) going on sale from July 2, local official-store and pop-up channels, 8/128 and 12/256 GB configurations, launch SRPs and early-bird offers, Snapdragon 870, display, cameras, battery, and connectivity.",
           "2022-06-27"),
    source("black_shark_5_revu_ph", "REVU Philippines", URL_REVU,
           "Independent contemporaneous confirmation of Philippine sale channels, launch date, configurations, and prices",
           "Published June 26, 2022. REVU reports official Black Shark Shopee Philippines and SM City North EDSA pop-up availability beginning July 2, the two standard-model Philippine configurations, SRPs, and the July 2–18 PHP 1,000 offer.",
           "2022-06-26"),
    source("black_shark_5_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-family technical specification cross-check; not used to claim Philippine SKU availability",
           "The exact Black Shark 5 specification page reports the 6.67-inch 144 Hz AMOLED display, Snapdragon 870, global memory/storage family, cameras, battery, dimensions, weight, and connectivity. It gives model code SHARK PAR-A0, which differs from the PH GEC/manual SHARK PAR-H0; its global band table and model code are not assigned to the Philippine configuration.",
           "2022-03-30"),
    source("qualcomm_sd870_brief", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 870 platform specifications",
           "Qualcomm's Snapdragon 870 brief corroborates the platform CPU/GPU family and Wi-Fi 6, Bluetooth 5.2, and 5G capabilities. Device-level values are taken from handset-specific sources.",
           "2021-01-19"),
    source("black_shark_5_bermor_listing", "Bermor Techzone", URL_BERMOR,
           "Dated exact-configuration Philippine retailer price and listing-stock observation",
           "Observed November 26, 2026. The page's live variation data maps 8+128 GB in Grey and Black to PHP 24,995 (regular PHP 27,000), and 12GB+256GB in Grey and Black to PHP 32,450 (regular PHP 35,000); all four variations are marked active, visible, and in stock at the online warehouse. The listing does not expressly identify item condition, so condition remains Not recorded."),
    source("black_shark_5_alt_specs_conflict", "Black Shark specification page at blackshark.gg", URL_ALT_SPECS,
           "Preserve conflicting technical claims for review; not adopted as a verified value",
           "This page identifies Snapdragon 870 but lists Adreno 660, an internally incompatible GPU pairing, and camera values that disagree with Philippine launch coverage and GSMArena (8 MP ultrawide, 5 MP macro, and 20 MP selfie). Its Bluetooth and audio details also disagree. The claims are kept as conflict evidence, not accepted silently."),
    source("black_shark_5_alt_terms", "Black Shark Global Store terms (blackshark.gg)", URL_ALT_TERMS,
           "Check for reuse/republishing terms associated with the alternate Black Shark specification host",
           "The site's terms prohibit infringing intellectual-property rights but do not provide an explicit license for reusing the product image. Rights to embed the official global CDN image remain unestablished."),
]


def field(fid: str, source_id: str, value, normalized_value, *, status="VERIFIED_SECONDARY",
          key=None, catalog_value="__normalized__", unit=None, note: str, configurationMatch=None,
          price_condition="__absent__", price_type=None, price_observed_at=None,
          listing_status=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": source_id,
            "sourceValue": value, "normalizedValue": normalized_value, "note": note}
    if configurationMatch:
        item["configurationMatch"] = configurationMatch
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
    match = f"Philippine {ram} GB RAM / {storage} GB storage configuration"
    out = []

    def add(fid, sid, value, normalized, **kwargs):
        out.append(field(fid, sid, value, normalized, configurationMatch=match, **kwargs))

    add("model_number", "black_shark_5_ntc_gec", "SHARK PAR-H0; NTC 2022 GEC lists BLACK SHARK SHARK PAR-H0",
        "SHARK PAR-H0", status="VERIFIED", note="The NTC GEC lists the code and the matching Black Shark 5 user manual explicitly pairs it with this marketing model. GSMArena lists PAR-A0 for a global/regional variant; that code is not substituted for the PH GEC/manual code.")
    add("global_release_date", "black_shark_5_gsmarena", "GSMArena reports release on April 4, 2022; announced March 30, 2022",
        "2022-04-04", status="VERIFIED_SECONDARY", note="Global-family release date from an exact Black Shark 5 technical record. This is separate from the reported Philippine official sale start of July 2, 2022 and does not claim the first individual sale.")
    add("configuration", "black_shark_5_yugatech_ph", f"{ram} GB + {storage} GB Philippine official-store configuration",
        f"{ram} GB RAM / {storage} GB storage", status="VERIFIED_SECONDARY", note="This exact pair is listed in contemporaneous Philippine launch coverage and matches the retailer selector. Black Shark 5 Pro and global-only memory pairings are excluded.")
    add("philippine_release_date", "black_shark_5_revu_ph", "Official Philippine sale begins July 2, 2022",
        "2022-07-02", status="VERIFIED_SECONDARY", note="The official local sale start is reported by contemporaneous Philippine coverage. It is not a claim about the first individual completed transaction.")
    add("official_launch_price_php", "black_shark_5_yugatech_ph", f"PHP {config['srp']:,} Philippine launch SRP for {ram}/{storage} GB",
        config["srp"], status="VERIFIED_SECONDARY", unit="PHP", note="Historical Philippine launch SRP, corroborated by REVU. The July 2–18 early-bird promo is recorded separately; neither historical value is treated as today's offer.")
    add("current_price_php", "black_shark_5_bermor_listing",
        f"PHP {config['current']:,} sale listing (regular PHP {config['regular']:,}); exact {ram}/{storage} GB options shown in stock online; condition not stated",
        config["current"], status="VERIFIED_SECONDARY", unit="PHP", price_condition=None,
        price_type=f"Bermor Techzone observed {OBSERVED}; sale price, exact {ram}/{storage} GB selection, stock shown; condition not stated",
        price_observed_at=OBSERVED,
        listing_status="In stock",
        note="Dated Philippine retailer price from exact variant-level listing data. The page says online warehouse stock is available for both colors; condition is not explicitly stated and remains Not recorded.")
    add("display_size", "black_shark_5_yugatech_ph", "6.67-inch AMOLED display", 6.67, key="displayInches", unit="in", note="Philippine launch source and GSMArena agree on 6.67 inches.")
    add("display_technology", "black_shark_5_yugatech_ph", "AMOLED", "AMOLED", key="displayType", note="The local launch source identifies an AMOLED panel; the source does not specify E4 in this entry.")
    add("display_resolution", "black_shark_5_yugatech_ph", "FHD+ 2400 x 1080 pixels", "1080 x 2400", key="resolution", note="FHD+ resolution from Philippine launch specifications.")
    add("display_refresh_rate", "black_shark_5_yugatech_ph", "144 Hz refresh rate; 720 Hz touch sampling", 144, key="refreshHz", unit="Hz", note="The catalog value is screen refresh rate. 720 Hz is touch sampling and is not substituted for it.")
    add("display_brightness", "black_shark_5_gsmarena", "1300 nits peak brightness", 1300, status="VERIFIED_SECONDARY", unit="nits", note="Listed as peak brightness by GSMArena; it is not a rated sustained brightness value.")
    add("display_protection", "black_shark_5_gsmarena", "Panel protection is not identified in the reviewed exact-model specification", None, status="NOT_DISCLOSED", note="No protective-glass brand or grade is inferred.")
    add("chipset", "black_shark_5_yugatech_ph", "Qualcomm Snapdragon 870 5G", "Qualcomm Snapdragon 870 5G", key="chipset", note="Philippine launch coverage identifies the standard Black Shark 5 processor, distinguishing it from the 5 Pro's Snapdragon 8 Gen 1.")
    add("process_node", "black_shark_5_gsmarena", "7 nm process", "7 nm", note="Chipset process reported for the Snapdragon 870 platform, not a handset manufacturing process.")
    add("cpu", "black_shark_5_gsmarena", "Octa-core: 1 x 3.2 GHz + 3 x 2.42 GHz + 4 x 1.80 GHz Kryo 585", "1 x 3.2 GHz + 3 x 2.42 GHz + 4 x 1.80 GHz Kryo 585", key="cpu", note="Exact-model CPU layout; Qualcomm's Snapdragon 870 brief corroborates the Kryo 585 CPU family.")
    add("gpu", "qualcomm_sd870_brief", "Adreno 650", "Adreno 650", status="VERIFIED", key="gpu", note="Qualcomm identifies Adreno 650 for Snapdragon 870. The alternate blackshark.gg page says Adreno 660, inconsistent with the chip and Qualcomm source; that error is not adopted.")
    add("operating_system", "black_shark_5_yugatech_ph", "Joy UI 13 based on Android 12", "Android 12; Joy UI 13", key="os", note="Launch software only; later update status is not inferred.")
    add("os_support", "black_shark_5_global_product", "No manufacturer-published OS/security support duration identified", None, status="NOT_DISCLOSED", note="No update-duration promise is published in the reviewed source set.")
    add("ram_capacity", "black_shark_5_yugatech_ph", f"{ram} GB LPDDR5 configuration", ram, key="ramGb", unit="GB", note="Exact physical memory size is in the Philippine launch configuration list.")
    add("ram_type", "black_shark_5_yugatech_ph", "LPDDR5", "LPDDR5", note="Memory type in Philippine launch specifications.")
    add("storage_capacity", "black_shark_5_yugatech_ph", f"{storage} GB UFS 3.1 configuration", storage, key="storageGb", unit="GB", note="Exact Philippine configuration capacity.")
    add("storage_type", "black_shark_5_yugatech_ph", "UFS 3.1", "UFS 3.1", note="Internal storage standard listed in local launch specifications.")
    add("storage_expansion", "black_shark_5_gsmarena", "GSMArena lists no card slot for model SHARK PAR-A0; the reviewed PH SHARK PAR-H0 sources do not establish an expansion slot", None, status="PENDING_VERIFICATION", note="The global reference uses a different model code, so no microSD conclusion is transferred to the PH model without an exact regional source.")
    add("rear_camera_system", "black_shark_5_alt_specs_conflict", "YugaTech and GSMArena: 64 MP main + 13 MP ultrawide + 2 MP macro; blackshark.gg: 64 MP main + 8 MP ultrawide + 5 MP macro", None, status="CONFLICTING_INFORMATION", key="rearCameraMp", catalog_value=None, note="Main camera resolution agrees at 64 MP, but the ultrawide and macro resolutions conflict. The catalog's primary-camera number is cleared until this exact model's camera configuration is resolved.")
    add("main_camera_sensor", "black_shark_5_gsmarena", "CMOS sensor model is not stated in the reviewed exact-model sources", None, status="NOT_DISCLOSED", note="The 64 MP resolution is not treated as a sensor model or sensor part number.")
    add("ultrawide_camera", "black_shark_5_alt_specs_conflict", "YugaTech/GSMArena: 13 MP f/2.4, 120 degree; blackshark.gg: 8 MP f/2.2, 120 degree", None, status="CONFLICTING_INFORMATION", note="The source set gives two different ultrawide resolutions and apertures; no single value is presented as settled.")
    add("telephoto_camera", "black_shark_5_gsmarena", "No telephoto camera listed in the three-camera system", "No telephoto module listed", status="NOT_APPLICABLE", note="The reported rear array comprises main, ultrawide, and macro cameras; no telephoto module is listed.")
    add("front_camera", "black_shark_5_alt_specs_conflict", "YugaTech/GSMArena: 16 MP; blackshark.gg: 20 MP", None, status="CONFLICTING_INFORMATION", key="frontCameraMp", catalog_value=None, note="The front camera resolution conflicts between the local launch specification and the alternate technical page. The catalog numeric value remains blank.")
    add("video_recording", "black_shark_5_gsmarena", "GSMArena lists rear video up to 4K/60 fps and 1080p/960 fps and front video up to 1080p/30 fps for SHARK PAR-A0; the PH PAR-H0 video modes are not established", None, status="PENDING_VERIFICATION", note="The global technical reference uses a different model code and its camera specifications conflict with the Philippine launch source; its video modes are not transferred to the PH variant.")
    add("battery_capacity", "black_shark_5_yugatech_ph", "4,650 mAh dual-cell battery", 4650, key="batteryMah", unit="mAh", note="Total rated capacity in local launch specifications; the source describes a dual-cell arrangement.")
    add("battery_technology", "black_shark_5_gsmarena", "Li-Po, non-removable", "Lithium-polymer, non-removable", note="Battery chemistry and serviceability as listed by GSMArena.")
    add("wired_charging", "black_shark_5_yugatech_ph", "Up to 120 W wired charging", 120, key="chargingW", unit="W", note="Maximum wired charging rating from local launch specifications.")
    add("wireless_charging", "black_shark_5_gsmarena", "No wireless charging capability listed", None, status="NOT_DISCLOSED", note="Wireless charging is not listed in the reviewed specification; no capability is inferred.")
    add("dimensions", "black_shark_5_yugatech_ph", "163.8 x 76.3 x 10 mm", "163.8 x 76.3 x 10 mm", key="dimensions", unit="mm", note="YugaTech and GSMArena report these rounded dimensions. The alternate page gives about 9.9 mm depth; this is a small rounding/measurement difference and is noted rather than presented as a separate local variant.")
    add("weight", "black_shark_5_yugatech_ph", "218 g", 218, key="weightG", unit="g", note="Philippine launch specification reports 218 g; the alternate source describes approximate 220 g and warns that actual measurements vary.")
    add("materials", "black_shark_5_gsmarena", "GSMArena lists glass front/back and aluminum frame for SHARK PAR-A0; PH PAR-H0 material is not specified by the reviewed local source", None, status="PENDING_VERIFICATION", note="The global technical reference uses a different model code. Materials are not transferred to the PH configuration without matching local evidence.")
    add("ingress_protection", "black_shark_5_gsmarena", "No IP rating listed in the reviewed exact-model sources", None, status="NOT_DISCLOSED", note="An IP certification is not inferred from absence of a listed rating.")
    add("sim_esim", "black_shark_5_yugatech_ph", "Dual-SIM; SIM size and eSIM support are not stated in Philippine launch coverage", "Dual SIM; SIM size/eSIM not recorded", key="sim", note="The local source confirms dual-SIM. Nano-SIM and eSIM details are left unrecorded for the Philippine PAR-H0 configuration.")
    add("cellular_bands", "black_shark_5_yugatech_ph", "5G and 4G LTE; exact SHARK PAR-H0 band list not published in the cited local source", "5G / 4G LTE; exact local bands not recorded", key="cellular", note="Local launch coverage confirms 5G/LTE. GSMArena's band list is for model SHARK PAR-A0 and is not substituted for the PH GEC/manual PAR-H0 model.")
    add("wifi", "black_shark_5_yugatech_ph", "Wi-Fi 6", "Wi-Fi 6 (802.11ax)", key="wifi", note="Wi-Fi 6 appears in Philippine launch specifications; Qualcomm's platform brief confirms the chipset supports this standard.")
    add("bluetooth", "black_shark_5_yugatech_ph", "Bluetooth 5.2; blackshark.gg lists Bluetooth 5.0", None, status="CONFLICTING_INFORMATION", note="The local launch source and Qualcomm platform brief identify Bluetooth 5.2, but the alternate Black Shark specifications page says 5.0. The catalog field remains blank pending an exact-model primary clarification.")
    add("usb", "black_shark_5_manual_mirror", "USB Type-C port; data-transfer protocol not stated in the manual", "USB Type-C; protocol not recorded", key="ports", note="Connector type only; no USB generation or data rate is inferred.")
    add("nfc", "black_shark_5_yugatech_ph", "NFC listed", "Yes", note="NFC appears in Philippine launch specifications.")
    add("gnss", "black_shark_5_yugatech_ph", "GPS, A-GPS, GLONASS, Galileo, BeiDou, and QZSS", "GPS, A-GPS, GLONASS, Galileo, BeiDou, QZSS", note="Navigation systems listed in local launch specifications.")
    add("audio", "black_shark_5_alt_specs_conflict", "GSMArena: stereo speakers, no 3.5 mm jack; blackshark.gg: 3.5 mm jack listed", None, status="CONFLICTING_INFORMATION", key="sound", catalog_value=None, note="The reviewed sources disagree on the 3.5 mm jack. Stereo-speaker support is consistent, but the catalog audio field stays blank rather than making an unqualified statement.")
    add("sensors", "black_shark_5_manual_mirror", "Manual diagram identifies the side power button as fingerprint lock; other sensor list is not recorded for PH model SHARK PAR-H0", "Side-mounted fingerprint reader; other sensors not recorded", status="VERIFIED_SECONDARY", note="The manual's model-specific diagram confirms the side fingerprint reader. Remaining sensors are not transferred from a GSMArena record using the different SHARK PAR-A0 code.")

    if len(out) != 46:
        raise ValueError(f"Expected 46 reviewed phone fields including global release date, got {len(out)}")
    return out


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "black shark"
            or device.get("model") != "5"):
        raise ValueError("The inventory row no longer matches standard Black Shark 5")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Black Shark 5 already has a manual review; inspect it before replacing")

    records = []
    for index, config in enumerate(CONFIGS):
        ram, storage = config["ram"], config["storage"]
        config_id = f"{DEVICE}-{ram}gb-{storage}gb-ph"
        label = f"{ram} GB RAM / {storage} GB storage"
        review = {
            "deviceId": DEVICE,
            "configurationId": config_id,
            "brand": "Black Shark",
            "model": "5",
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
                "modelCode": "SHARK PAR-H0",
                "notes": "Exact Philippine launch configuration reported by YugaTech and REVU and matched to the active Bermor variation. Kept separate from the other local configuration; current listing condition is not stated.",
            } for item in CONFIGS]
            review["replaceUnrecordedPlaceholder"] = True
            review["availabilityEvidence"] = {
                "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                "availabilityStatus": "Philippine official sale reported from July 2, 2022 through Black Shark's official Shopee Philippines store and pop-up booth; NTC's 2022 GEC lists BLACK SHARK SHARK PAR-H0.",
                "philippineAvailability": "The standard Black Shark 5 was announced for local sale in official Black Shark Philippines channels. YugaTech and REVU report July 2, 2022; NTC lists its SHARK PAR-H0 code. This verifies Philippine availability of the model family and the two launch configurations, while the workbook's scope status remains Pending.",
                "observedAt": OBSERVED,
                "manufacturer": "Black Shark",
                "productLine": "Black Shark 5 Series",
                "modelNumber": "SHARK PAR-H0",
                "philippineReleaseYear": 2022,
                "philippineDateLabel": "Reported Philippine official sale date",
                "researchNotes": "Matched to the standard Black Shark 5, not Black Shark 5 Pro. The NTC 2022 GEC lists BLACK SHARK SHARK PAR-H0 and the model manual names PAR-H0; GSMArena uses PAR-A0 for a separate global/regional code, whose band table is not used for the PH unit. YugaTech and REVU support two local RAM/storage variants: 8/128 and 12/256, with launch SRPs PHP 26,999 and PHP 34,999 and early-bird prices PHP 25,999 and PHP 33,999 (July 2–18, 2022). On 2026-11-26 Bermor showed both exact RAM/storage configurations active and in stock at its online warehouse, with listed sale prices PHP 24,995 and PHP 32,450; condition is not stated. Camera sensor details, Bluetooth version, and the audio jack conflict between reviewed sources and remain unresolved. An exact official Black Shark product image was located, but reuse terms are not established, so the neutral placeholder remains. The inventory scope label is retained as Pending.",
                "qualityFlag": "Camera, Bluetooth, and audio source conflicts; image reuse rights not established; workbook scope remains Pending",
                "openIssues": [
                    {"issue": "Rear camera source conflict: local launch coverage/GSMArena report 13 MP ultrawide + 2 MP macro, while blackshark.gg reports 8 MP + 5 MP", "action": "Keep rear camera field and primary-camera catalog number blank until an exact-model primary source resolves the conflict."},
                    {"issue": "Front camera source conflict: 16 MP versus 20 MP", "action": "Keep the public numeric front-camera field blank pending verification."},
                    {"issue": "Bluetooth version and 3.5 mm audio jack differ between reviewed sources", "action": "Preserve both claims in the audit and leave these catalog values unresolved."},
                    {"issue": "Bermor listing does not explicitly state item condition", "action": "Show the exact observed prices and stock state with condition Not recorded."},
                    {"issue": "Exact official product image reuse license is not recorded", "action": "Keep the neutral placeholder until usage permission is documented."},
                    {"issue": "Workbook eligibility/scope status remains Pending", "action": "Do not change study eligibility based only on Philippine availability evidence."},
                ],
            }
        records.append(review)

    manual["records"].extend(records)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact Black Shark 5 Mirror Black image is available from the manufacturer product page, but no reusable image license or written permission is recorded.",
        "sourcePage": URL_OFFICIAL,
        "assetUrl": URL_IMAGE,
        "scope": "Exact Black Shark 5, Mirror Black finish; image does not establish a RAM/storage configuration",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Black Shark 5",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = []
    for config in CONFIGS:
        variant_id = f"{DEVICE}-{config['ram']}gb-{config['storage']}gb-ph"
        label = f"Philippine {config['ram']} GB / {config['storage']} GB configuration"
        prices.extend([
            {
                "device_id": DEVICE, "amount_php": config["srp"], "configuration_id": variant_id,
                "configuration_match": "exact", "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
                "price_type": "historical_ph_launch_srp", "source_published_at": "2022-06-27",
                "excerpt": f"YugaTech reported PHP {config['srp']:,} Philippine launch SRP for {label}; not a current offer.",
                "source_url": URL_YUGA, "source_kind": "historical_ph_launch_price_report", "observed_at": OBSERVED_AT,
                "local_availability_verified": True, "availability_status": "historical_ph_launch_srp_not_current",
            },
            {
                "device_id": DEVICE, "amount_php": config["promo"], "configuration_id": variant_id,
                "configuration_match": "exact", "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
                "price_type": "historical_ph_early_bird_promotion", "source_published_at": "2022-06-27",
                "excerpt": f"YugaTech reported PHP {config['promo']:,} early-bird price for {label}, offered July 2–18, 2022; not a current offer.",
                "source_url": URL_YUGA, "source_kind": "dated_ph_launch_promotion", "observed_at": OBSERVED_AT,
                "local_availability_verified": True, "availability_status": "dated_ph_promotion_not_current",
            },
            {
                "device_id": DEVICE, "amount_php": config["current"], "regular_price_php": config["regular"],
                "configuration_id": variant_id, "configuration_match": "exact",
                "variant_ram_gb": config["ram"], "variant_storage_gb": config["storage"],
                "color_options": ["Grey", "Black"], "price_type": "current_ph_retailer_sale_listing_condition_not_stated",
                "source_published_at": None,
                "excerpt": f"Bermor variation data observed {OBSERVED}: {label}, PHP {config['current']:,} sale (regular PHP {config['regular']:,}); Grey and Black variations show active/in-stock online warehouse status. Condition not stated.",
                "source_url": URL_BERMOR, "source_kind": "retailer_price_observation", "observed_at": OBSERVED_AT,
                "local_availability_verified": True, "availability_status": "listed_in_stock_online_warehouse_condition_not_stated",
            },
        ])
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Black Shark", "model_name": "5", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [], "discovery": [], "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Black Shark 5 / SHARK PAR-H0; not Black Shark 5 Pro",
        "configurations": [f"{c['ram']}/{c['storage']}" for c in CONFIGS],
        "reviewedFields": sum(len(r["fields"]) for r in records),
        "philippineAvailability": "official local sale reported from 2022-07-02",
        "historicalSrpsPhp": [c["srp"] for c in CONFIGS],
        "currentPricesPhp": [c["current"] for c in CONFIGS],
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
