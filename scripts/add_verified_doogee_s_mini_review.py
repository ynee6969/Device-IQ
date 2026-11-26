#!/usr/bin/env python3
"""Record an exact-model, Philippine-market review for DOOGEE S mini."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/doogee-s-mini-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_64797b9452613a"
CONFIG = f"{DEVICE}-ph-8gb-256gb"

URL_YUGA_PH = "https://www.yugatech.com/smartphones/doogee-s-mini-specs-price-philippines/"
URL_YUGA_GLOBAL = "https://www.yugatech.com/news/doogee-smini-officially-released/"
URL_YUGA_ROUNDUP = "https://specs.yugatech.com/news/smartphones-launched-in-the-philippines-december-2023/"
URL_GIZGUIDE = "https://www.gizguide.com/2023/12/doogee-smini-official-price-specs-ph.html"
URL_REVU = "https://www.revu.com.ph/2023/12/doogee-s-mini-price-philippines/"
URL_FCC = "https://fccid.io/2AX4YSMINI"
URL_DOOGEE_PARTS = "https://care.doogee.com/spare-form?part_id=2119"
URL_DOOGEE_VIDEO = "https://www.youtube.com/watch?v=iBsySd2h8tE"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("doogee_smini_yugatech_ph", "YugaTech Philippines", URL_YUGA_PH,
        "Exact-model Philippine specifications, reported local market date, introduction price, and first advertised 12.12 offer",
        "Published 9 December 2023. Names DOOGEE S mini, reports that it arrived in the Philippine market on that date, lists 8 GB physical RAM / 256 GB storage and the core hardware, and states a PHP 13,999 introductory price plus an upcoming PHP 12,699 TikTok Shop 12.12 promotion. The promotion is an advertised offer, not a verified completed transaction.",
        "2023-12-09"),
    src("doogee_smini_yugatech_global", "YugaTech Philippines", URL_YUGA_GLOBAL,
        "Global announcement context and exact-model cross-check",
        "Published 30 October 2023. Describes the DOOGEE Smini as unveiled and reports it available through AliExpress, Amazon, and DOOGEEMall, while explicitly saying there was no Philippine launch news at that time. This does not establish an exact global first-sale date.",
        "2023-10-30"),
    src("doogee_smini_yugatech_ph_roundup", "YugaSpecs / YugaTech", URL_YUGA_ROUNDUP,
        "Independent Philippine market-entry date cross-check",
        "Published 31 December 2023. Lists the DOOGEE S mini among smartphones brought to the Philippine market on 9 December 2023.",
        "2023-12-31"),
    src("doogee_smini_gizguide_ph", "GizGuide Philippines", URL_GIZGUIDE,
        "Philippine availability and price corroboration; exact-model hardware cross-check",
        "Published 1 December 2023. Reports DOOGEE's Philippine pricing and availability announcement, PHP 13,999 introductory price, and PHP 12,699 12.12 TikTok Shop offer. Provides model-specific display, processor/GPU, memory, cameras, battery, connectivity, sensors, dimensions, and weight. Its article image matches the named Smini, but reuse permission is not stated.",
        "2023-12-01"),
    src("doogee_smini_revu_ph", "Revu Philippines", URL_REVU,
        "Philippine launch-price and promotion corroboration",
        "Published 8 December 2023. Reports PHP 13,999 as the local official price and PHP 12,699 as a scheduled 12.12 TikTok Shop offer; describes the offer as upcoming, so the promotional amount is not treated as a verified transaction or current price.",
        "2023-12-08"),
    src("doogee_smini_fcc", "FCC equipment authorization record", URL_FCC,
        "Manufacturer and exact model-code identity",
        "FCC ID 2AX4YSMINI identifies Shenzhen DOOGEE Hengtong Technology Co., Ltd. as grantee and SMINI as product code/model. This is a global certification identity record, not Philippine type approval or sale evidence.",
        "2023-10-23"),
    src("doogee_smini_official_parts", "DOOGEE Care (manufacturer service site)", URL_DOOGEE_PARTS,
        "Manufacturer configuration cross-check",
        "DOOGEE Care's S MINI spare-part record identifies an SMINI mainboard with 8 GB RAM + 256 GB ROM. This corroborates the physical 8/256 configuration; it does not independently establish a Philippine retail SKU.",
        None),
    src("doogee_smini_official_video", "DOOGEE official YouTube channel", URL_DOOGEE_VIDEO,
        "Manufacturer-published exact-model design and hardware cross-check",
        "Official DOOGEE Smini introduction video, published 26 November 2023, identifies the 4.5-inch qHD+ IPS display, 50 MP + 2 MP macro cameras, 3,000 mAh battery, and 133.0 x 60.0 x 13.5 mm dimensions. Its publication date is not treated as a release date.",
        "2023-11-26"),
]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED_SECONDARY",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      catalog_value=None, price_type: str | None = None,
      price_observed: str | None = None) -> dict:
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
    return row


def fields() -> list[dict]:
    fields = [
        f("model_number", "doogee_smini_official_parts", "DOOGEE Care service-parts model: SMINI", "SMINI",
          status="VERIFIED", note="The manufacturer's service-parts record uses SMINI; the FCC equipment record independently maps product code SMINI to this DOOGEE smartphone."),
        f("global_release_date", "doogee_smini_yugatech_global",
          "YugaTech reported the model unveiled on 30 October 2023 and globally orderable by then; no exact first global release date was found.", None,
          status="NOT_DISCLOSED", note="An announcement and evidence of availability by a later date do not establish the exact initial global release date."),
        f("configuration", "doogee_smini_official_parts", "DOOGEE Care SMINI mainboard: 8 GB RAM + 256 GB ROM; YugaTech reports the same Philippine configuration.",
          "8 GB RAM / 256 GB storage", status="VERIFIED",
          note="The manufacturer's service-parts listing confirms the physical 8/256 configuration, and Philippine launch coverage names it. The additional 7 GB is extended/virtual memory, not additional physical RAM."),
        f("philippine_release_date", "doogee_smini_yugatech_ph_roundup",
          "DOOGEE S mini brought to the Philippine market on 9 December 2023; YugaTech's model-specific launch page is dated the same day.",
          "2023-12-09", status="VERIFIED_SECONDARY",
          note="This is the reported market-entry date. Exact first transaction and the precise first authorized sale timestamp were not independently documented."),
        f("official_launch_price_php", "doogee_smini_revu_ph",
          "PHP 13,999 official local price / introductory price for DOOGEE S mini, reported 8 December 2023.", 13999,
          unit="PHP", status="VERIFIED_SECONDARY",
          note="Historical Philippine introductory price reported contemporaneously by Revu, GizGuide, and YugaTech. It is not a current price.",
          price_type="historical_ph_intro_price", price_observed="2023-12-08"),
        f("current_price_php", "doogee_smini_yugatech_ph",
          "Reviewed Philippine prices are dated December 2023 launch reports; no current dated and orderable Philippine offer was verified.", None,
          status="PENDING_VERIFICATION", unit="PHP",
          note="Keep current price blank. PHP 13,999 is a historical intro price; PHP 12,699 was an advertised 12.12 promotion, not a verified current offer."),
        f("display_size", "doogee_smini_yugatech_ph", "4.5-inch display", 4.5, key="displayInches", unit="in"),
        f("display_technology", "doogee_smini_yugatech_ph", "qHD+ IPS TFT display", "IPS TFT LCD", key="displayType"),
        f("display_resolution", "doogee_smini_yugatech_ph", "480 x 1170 pixels", "480 x 1170", key="resolution"),
        f("display_refresh_rate", "doogee_smini_revu_ph", "60 Hz", 60, unit="Hz", key="refreshHz", status="VERIFIED_SECONDARY"),
        f("display_brightness", "doogee_smini_yugatech_ph", "No brightness value in reviewed exact-model specifications", None,
          status="NOT_DISCLOSED", unit="nits"),
        f("display_protection", "doogee_smini_yugatech_ph", "No cover-glass type or display protection rating in reviewed exact-model specifications", None,
          status="NOT_DISCLOSED"),
        f("chipset", "doogee_smini_yugatech_ph", "MediaTek Helio G99", "MediaTek Helio G99", key="chipset"),
        f("process_node", "doogee_smini_yugatech_ph", "6 nm", 6, unit="nm"),
        f("cpu", "doogee_smini_yugatech_ph", "Octa-core, maximum clock speed 2.2 GHz", "Octa-core up to 2.2 GHz", key="cpu"),
        f("gpu", "doogee_smini_gizguide_ph", "Mali-G57 MC2", "Mali-G57 MC2", key="gpu"),
        f("operating_system", "doogee_smini_yugatech_ph", "Android 13", "Android 13", key="os"),
        f("os_support", "doogee_smini_yugatech_ph", "No software update or security support policy was found in the reviewed sources", None,
          status="NOT_DISCLOSED"),
        f("ram_capacity", "doogee_smini_official_parts", "8 GB physical RAM; separate 7 GB extended memory is reported", 8,
          key="ramGb", unit="GB", status="VERIFIED",
          note="Catalog RAM is physical memory only. The 7 GB extended/virtual-memory marketing figure is not added to installed RAM."),
        f("ram_type", "doogee_smini_official_parts", "RAM type not identified by the manufacturer parts record or reviewed local specifications", None,
          status="NOT_DISCLOSED"),
        f("storage_capacity", "doogee_smini_official_parts", "256 GB ROM / internal storage", 256,
          key="storageGb", unit="GB", status="VERIFIED"),
        f("storage_type", "doogee_smini_yugatech_ph", "Internal storage interface/type not identified", None, status="NOT_DISCLOSED"),
        f("storage_expansion", "doogee_smini_yugatech_ph", "microSD support up to 2 TB", "microSD up to 2 TB"),
        f("rear_camera_system", "doogee_smini_yugatech_ph", "50 MP f/1.8 main camera + 2 MP macro camera", "50 MP main f/1.8 + 2 MP macro", key="rearCameraMp", unit="MP", catalog_value=50),
        f("main_camera_sensor", "doogee_smini_yugatech_ph", "Main camera is listed as 50 MP f/1.8 autofocus; sensor part/model number is not stated", "50 MP f/1.8 AF; sensor model not recorded"),
        f("ultrawide_camera", "doogee_smini_yugatech_ph", "The complete reported rear camera system is 50 MP main + 2 MP macro; no ultrawide module is listed", None,
          status="NOT_APPLICABLE"),
        f("telephoto_camera", "doogee_smini_yugatech_ph", "The complete reported rear camera system is 50 MP main + 2 MP macro; no telephoto module is listed", None,
          status="NOT_APPLICABLE"),
        f("front_camera", "doogee_smini_yugatech_ph", "8 MP selfie camera", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", "doogee_smini_yugatech_ph", "Video recording modes and maximum resolution were not listed in reviewed exact-model sources", None,
          status="NOT_DISCLOSED"),
        f("battery_capacity", "doogee_smini_yugatech_ph", "3,000 mAh", 3000, key="batteryMah", unit="mAh"),
        f("battery_technology", "doogee_smini_yugatech_ph", "Battery chemistry and replaceability were not stated in reviewed exact-model sources", None,
          status="NOT_DISCLOSED"),
        f("wired_charging", "doogee_smini_yugatech_ph", "18 W charging", 18, key="chargingW", unit="W"),
        f("wireless_charging", "doogee_smini_yugatech_ph", "Wireless and reverse charging are not stated in the reviewed sources", None,
          status="NOT_DISCLOSED"),
        f("dimensions", "doogee_smini_official_video", "133.0 x 60.0 x 13.5 mm", "133.0 x 60.0 x 13.5 mm", key="dimensions", unit="mm",
          status="VERIFIED", note="Dimensions are also reported by YugaTech Philippines."),
        f("weight", "doogee_smini_yugatech_ph", "155 g", 155, key="weightG", unit="g"),
        f("materials", "doogee_smini_yugatech_ph", "Frame and back materials were not stated in the reviewed exact-model sources", None,
          status="NOT_DISCLOSED"),
        f("ingress_protection", "doogee_smini_gizguide_ph", "IP68, IP69K, and MIL-STD-810H ratings/compliance are reported for the model", "IP68; IP69K; MIL-STD-810H reported",
          status="VERIFIED_SECONDARY", note="These are manufacturer/launch-coverage claims as reported by the cited Philippine source; independent durability test results were not reviewed."),
        f("sim_esim", "doogee_smini_gizguide_ph", "Hybrid dual nano-SIM / microSD tray; eSIM support not stated", "Hybrid dual nano-SIM / microSD; eSIM not recorded", key="sim"),
        f("cellular_bands", "doogee_smini_yugatech_ph", "4G LTE; model-specific supported band list was not published in the reviewed Philippine specifications", "4G LTE; exact bands not recorded", key="cellular"),
        f("wifi", "doogee_smini_yugatech_ph", "Wi-Fi 802.11ac/a/b/g/n", "802.11 a/b/g/n/ac", key="wifi"),
        f("bluetooth", "doogee_smini_yugatech_ph", "Bluetooth 5.2", "Bluetooth 5.2"),
        f("usb", "doogee_smini_yugatech_ph", "USB Type-C; USB data version and OTG support not stated", "USB Type-C; data version not recorded", key="ports"),
        f("nfc", "doogee_smini_yugatech_ph", "NFC supported", True),
        f("gnss", "doogee_smini_yugatech_ph", "GPS, GLONASS, Galileo, BeiDou, and AGPS", "GPS; GLONASS; Galileo; BeiDou; AGPS"),
        f("audio", "doogee_smini_yugatech_ph", "Headphone jack, speaker layout, and audio codecs not identified in reviewed exact-model specifications", None,
          status="NOT_DISCLOSED"),
        f("sensors", "doogee_smini_gizguide_ph", "Accelerometer, light, orientation, proximity, gyroscope, sound, and magnetic sensors; side fingerprint reader is reported", "Accelerometer; light; orientation; proximity; gyroscope; sound; magnetic; side fingerprint reader"),
    ]
    if len(fields) != 46:
        raise ValueError(f"Expected 46 smartphone fields, got {len(fields)}")
    source_ids = {source["id"] for source in SOURCES}
    missing_sources = sorted({item["sourceId"] for item in fields} - source_ids)
    if missing_sources:
        raise ValueError(f"Fields reference undefined sources: {missing_sources}")
    return fields


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine launch and initial market entry reported on 9 December 2023. Contemporaneous coverage reported the official PHP 13,999 introductory price and a scheduled 12.12 TikTok Shop promotion. Current stock and price are unknown.",
        "philippineAvailability": "Philippine launch coverage from GizGuide (1 December), Revu (8 December), and YugaTech (9 December 2023) identifies the exact DOOGEE S mini and the DOOGEE Philippines launch offer. YugaTech's year-end market roundup reports arrival on 9 December. The local 8 GB / 256 GB configuration is documented. The exact first authorized-sale transaction is not established; the PHP 12,699 12.12 promotion is retained only as an advertised historical offer, not a completed or current price.",
        "observedAt": OBSERVED,
        "manufacturer": "Shenzhen DOOGEE Hengtong Technology Co., Ltd.",
        "catalogModel": "S mini",
        "modelNumber": "SMINI",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Reported Philippine market-entry date",
        "researchNotes": "Workbook row 135 matched to DOOGEE S mini / FCC product code SMINI. DOOGEE Care lists the 8 GB + 256 GB mainboard, and Philippine launch coverage identifies the same physical configuration. Historical PHP 13,999 introductory pricing is confirmed in contemporaneous local reporting. Current price and current stock are not verified. The workbook scope status remains Pending.",
        "qualityFlag": "Exact model and Philippine 8 GB / 256 GB configuration reviewed. Local launch and historical introductory price are supported by contemporaneous Philippine coverage; current price, exact global first-sale date, and image reuse remain unresolved.",
        "openIssues": [
            {"issue": "Exact global first-sale date was not established", "action": "Keep the global release-date field blank; do not substitute the announcement date."},
            {"issue": "No current dated, orderable Philippine price or stock status was verified", "action": "Keep current price and stock blank; retain the launch price and scheduled 12.12 offer as historical evidence only."},
            {"issue": "The PHP 12,699 12.12 amount was announced before the event", "action": "Treat it as an advertised promotion, not a verified completed sale."},
            {"issue": "Exact first authorized-sale transaction time is not recorded", "action": "Describe 9 December 2023 as a reported market-entry date."},
            {"issue": "Exact-model photos appear in manufacturer and Philippine product coverage, but image reuse permission is not recorded", "action": "Keep the neutral image placeholder until reuse rights are documented."},
            {"issue": "Workbook eligibility remains Pending", "action": "Preserve the existing study-scope status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 135
            or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "doogee"
            or device.get("model", "").casefold() != "s mini"):
        raise ValueError("Catalog target guard failed for workbook row 135 DOOGEE S mini")
    if device.get("scopeStatus") != "Pending":
        raise ValueError(f"Expected Pending scope; refusing to alter workbook eligibility: {device.get('scopeStatus')}")
    existing_variants = device.get("variants", [])
    if (len(existing_variants) != 1
            or existing_variants[0].get("id") not in {f"{DEVICE}-unrecorded", CONFIG}):
        raise ValueError("Expected either the original placeholder or this reviewed S mini configuration")

    variant = {
        "id": CONFIG,
        "label": "8 GB RAM / 256 GB storage",
        "modelCode": "SMINI",
        "sku": None,
        "notes": "Philippine launch reporting identifies this configuration. The 7 GB Extended RAM figure is virtual/extended memory and is not part of the 8 GB physical RAM value. The phone also has a secondary 7-segment rear display. Current stock and price are not verified.",
        "workbookRow": 135,
    }
    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "DOOGEE",
        "model": "S mini",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "modelCode": "SMINI",
        "replacementVariants": [variant],
        "replaceUnrecordedPlaceholder": True,
        "sources": SOURCES,
        "fields": fields(),
        "availabilityEvidence": availability_evidence(),
    }
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].append(review)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact DOOGEE S mini image is shown in Philippine launch coverage and on the official DOOGEE product/media channels, but a reusable license or written republishing permission is not recorded. Keep the neutral placeholder.",
        "sourcePage": URL_YUGA_PH,
        "relatedSourcePages": [URL_GIZGUIDE, URL_DOOGEE_VIDEO],
        "assetUrl": None,
        "scope": "Exact DOOGEE S mini; Philippine 8 GB / 256 GB configuration",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for DOOGEE S mini",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {
            "device_id": DEVICE, "amount_php": 13999, "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_8gb_256gb_configuration",
            "variant_ram_gb": 8, "variant_storage_gb": 256,
            "price_type": "historical_ph_intro_price", "source_published_at": "2023-12-08",
            "excerpt": "Revu reported PHP 13,999 as DOOGEE S mini's official Philippine introductory price. YugaTech and GizGuide also reported the same price.",
            "source_url": URL_REVU, "source_kind": "historical_local_price_report",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_intro_price_not_current",
        },
        {
            "device_id": DEVICE, "amount_php": 12699, "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_8gb_256gb_configuration",
            "variant_ram_gb": 8, "variant_storage_gb": 256,
            "price_type": "historical_advertised_12_12_promotion", "source_published_at": "2023-12-08",
            "excerpt": "A PHP 12,699 TikTok Shop 12.12 price was announced in advance; the cited report describes it as an upcoming offer, not a verified completed transaction.",
            "source_url": URL_REVU, "source_kind": "historical_advertised_price_candidate",
            "observed_at": OBSERVED, "local_availability_verified": False,
            "availability_status": "advertised_offer_not_transaction_verified",
        },
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "DOOGEE", "model_name": "S mini", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_FCC, "result": "FCC record identifies the manufacturer and SMINI product/model code."},
            {"device_id": DEVICE, "source_url": URL_DOOGEE_PARTS, "result": "DOOGEE Care identifies an SMINI 8 GB + 256 GB mainboard."},
            {"device_id": DEVICE, "source_url": URL_YUGA_PH, "result": "Exact-model Philippine launch page reports 8/256, local availability on 9 December 2023, and PHP 13,999 intro pricing."},
            {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "Corroborates Philippine launch offer and detailed Smini hardware."},
            {"device_id": DEVICE, "source_url": URL_YUGA_GLOBAL, "result": "Global unveiling coverage predates local launch but does not establish exact first global sale date."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "model": "DOOGEE S mini", "workbookRow": 135, "modelCode": "SMINI",
        "configuration": variant["label"], "reviewedFields": len(review["fields"]),
        "verifiedFields": sum(row["status"] in {"VERIFIED", "VERIFIED_SECONDARY"} for row in review["fields"]),
        "notDisclosedFields": sum(row["status"] == "NOT_DISCLOSED" for row in review["fields"]),
        "launchPricePhp": 13999, "currentPrice": None, "scopeStatus": "Pending",
        "imageStatus": "REUSE_RIGHTS_NOT_ESTABLISHED",
    }, indent=2))


if __name__ == "__main__":
    main()
