#!/usr/bin/env python3
"""Review the Infinix ZERO 30 workbook row against the Philippine 4G model."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/infinix-zero-30-4g-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_d14dd9dfdf860b"
CONFIG = f"{DEVICE}-ph-x6731b-8gb-256gb"

URL_INFINIX = "https://wap.id.infinixmobility.com/specs/zero-30"
URL_INFINIX_GLOBAL = "https://www.infinixmobility.com/zero-30"
URL_INFINIX_DECLARATION = "https://www.infinixmobility.com/declaration_pdf/20231215/X6731B_C_Declaration_of_conformity.pdf"
URL_YUGA_PH = "https://www.yugatech.com/news/infinix-zero-30-4g-specs-price-philippines/"
URL_YUGA_ROUNDUP = "https://specs.yugatech.com/news/smartphones-launched-in-the-philippines-december-2023/"
URL_GIZGUIDE = "https://www.gizguide.com/2023/12/infinix-zero-30-4g-price-specs-official-ph.html"
URL_REVU = "https://www.revu.com.ph/2023/12/infinix-zero-30-price-philippines/"
URL_TECHPINAS = "https://www.techpinas.com/2023/12/Infinix-ZERO-30-4G.html"
URL_YUGA_SPECS = "https://www.yugatech.com/spec/infinix-zero-30-4g/"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("infinix_zero30_official_specs", "Infinix Indonesia (manufacturer)", URL_INFINIX,
        "Manufacturer specifications for exact model X6731B",
        "Official Infinix product specifications identify ZERO 30 4G model X6731B and publish its dimensions, weight, colors, chipset/CPU/GPU, display, camera sensors and modes, RAM/storage types, battery, SIM, Wi-Fi 5, USB-C/OTG, NFC, IP54, sensors, and XOS 13 / Android 13. Region-specific network bands are not copied into the Philippine record.",
        None),
    src("infinix_zero30_official_declaration", "Infinix Mobility Limited (manufacturer)", URL_INFINIX_DECLARATION,
        "Manufacturer model-code corroboration",
        "Infinix's declaration of conformity identifies model number X6731B. It does not establish Philippine retail availability or an exact local SKU.",
        "2023-12-15"),
    src("infinix_zero30_yugatech_ph", "YugaTech Philippines", URL_YUGA_PH,
        "Exact 4G model Philippine launch, 8/256 local configuration, SRP and first-sale offer",
        "Published 3 December 2023. Explicitly names the ZERO 30 4G; lists 8 GB physical RAM / 256 GB storage, 108 MP rear main camera, 50 MP front camera, and says first TikTok Shop sale was scheduled for 4 December at PHP 8,999, with a PHP 9,999 Lazada listing described as likely SRP. The page says Wi-Fi 6, which conflicts with Infinix's exact X6731B page (Wi-Fi 5); the manufacturer value is used.",
        "2023-12-03"),
    src("infinix_zero30_revu_ph", "Revu Philippines", URL_REVU,
        "Philippine 4G identity, launch offer and SRP corroboration",
        "Published 2 December 2023. Says the 4G version of ZERO 30 would first be available on Infinix Mobile's TikTok Shop on 4 December for PHP 8,999 instead of the PHP 9,999 suggested retail price, then on Lazada, Shopee and retail stores. Confirms this record is the 4G model rather than ZERO 30 5G.",
        "2023-12-02"),
    src("infinix_zero30_techpinas_ph", "TechPinas Philippines", URL_TECHPINAS,
        "Exact-model code, Philippine release date, hands-on technical cross-check, dimensions and material observations",
        "Published 9 December 2023. Identifies Infinix ZERO 30 4G and model X6731B; reports Philippine market debut on 4 December 2023, PHP 9,999 SRP and PHP 8,999 introductory TikTok Shop price. Provides hands-on display, camera/video, storage interface, battery, dimensions, weight, audio and sensor details. Material descriptions can vary by finish and are not collapsed into one public claim.",
        "2023-12-09"),
    src("infinix_zero30_gizguide_ph", "GizGuide Philippines", URL_GIZGUIDE,
        "Philippine launch, local availability and hardware cross-check; source discrepancy review",
        "Published 4 December 2023. Identifies the 4G variant, PHP 9,999 SRP, local e-commerce availability and early-bird sale. The article's narrative contains an anomalous 200 MP camera claim while its headline and other exact-model sources identify 108 MP; the 200 MP figure is rejected. It also describes the 4G phone's Wi-Fi as dual-band without a version.",
        "2023-12-04"),
    src("infinix_zero30_yugatech_roundup", "YugaSpecs / YugaTech", URL_YUGA_ROUNDUP,
        "Philippine public-debut date cross-check",
        "Published 31 December 2023. Lists Infinix Zero 30 4G as debuting in the Philippines on 3 December 2023. Contemporaneous first-sale reports and TechPinas instead identify 4 December as the initial sale/market debut date; this source is retained to show the one-day announcement/debut discrepancy.",
        "2023-12-31"),
    src("infinix_zero30_yugatech_specs", "YugaTech Philippines", URL_YUGA_SPECS,
        "Exact 4G model specification cross-check",
        "YugaTech's exact-model specification record lists 108 MP + 2 MP + 2 MP rear cameras, 50 MP front camera, 8 GB / 256 GB, Wi-Fi 6, NFC, 4G LTE, and other model features. Its Wi-Fi 6 value conflicts with the Infinix exact X6731B page; manufacturer Wi-Fi 5 is used.",
        None),
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
    rows = [
        f("model_number", "infinix_zero30_official_specs", "Infinix ZERO 30 4G model X6731B", "X6731B",
          status="VERIFIED", note="Exact model code appears on Infinix's manufacturer specification page and declaration of conformity."),
        f("global_release_date", "infinix_zero30_official_specs",
          "No exact global first-sale date is stated on the reviewed Infinix X6731B specification page.", None,
          status="NOT_DISCLOSED", note="The 4G model is described as a separate product from ZERO 30 5G; no announcement date is substituted for an exact first global release date."),
        f("configuration", "infinix_zero30_yugatech_ph", "Philippine ZERO 30 4G configuration: 8 GB physical RAM / 256 GB storage", "8 GB RAM / 256 GB storage",
          status="VERIFIED_SECONDARY", note="Contemporaneous Philippine coverage identifies this local 4G configuration. The additional 8 GB is extended memory, not physical RAM."),
        f("philippine_release_date", "infinix_zero30_revu_ph",
          "Infinix Mobile's first-sale reports specify 4 December 2023; TechPinas reports the same market debut. YugaSpecs' year-end roundup lists a 3 December debut.",
          "2023-12-04", status="VERIFIED_SECONDARY",
          note="Stored as the reported first online-sale date (4 December), supported by contemporaneous Revu, YugaTech, GizGuide and TechPinas coverage. YugaSpecs gives 3 December as the debut date; exact first transaction time is not independently established."),
        f("official_launch_price_php", "infinix_zero30_revu_ph",
          "PHP 9,999 suggested retail price for the Philippine ZERO 30 4G 8 GB / 256 GB configuration", 9999,
          unit="PHP", status="VERIFIED_SECONDARY",
          note="Contemporaneous Philippine coverage identifies PHP 9,999 as SRP. PHP 8,999 was an advertised first-sale promotion, not the regular SRP or a current offer.",
          price_type="historical_ph_suggested_retail_price", price_observed="2023-12-02"),
        f("current_price_php", "infinix_zero30_yugatech_ph",
          "Reviewed Philippine prices are dated December 2023 launch reports; no current dated, orderable 8 GB / 256 GB offer was verified.", None,
          status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank. PHP 9,999 SRP and PHP 8,999 first-sale promotion are historical."),
        f("display_size", "infinix_zero30_official_specs", "6.78-inch display", 6.78, key="displayInches", unit="in", status="VERIFIED"),
        f("display_technology", "infinix_zero30_official_specs", "Flexible AMOLED, LTPS, curved display", "Curved LTPS AMOLED", key="displayType", status="VERIFIED"),
        f("display_resolution", "infinix_zero30_official_specs", "FHD+ 1080 x 2400 pixels", "1080 x 2400", key="resolution", status="VERIFIED"),
        f("display_refresh_rate", "infinix_zero30_official_specs", "60 Hz / 120 Hz; 120 Hz maximum", 120, key="refreshHz", unit="Hz", status="VERIFIED",
          note="Catalog value is the published maximum; Infinix also lists 60 Hz operation."),
        f("display_brightness", "infinix_zero30_official_specs", "950 nits peak", 950, unit="nits", status="VERIFIED"),
        f("display_protection", "infinix_zero30_official_specs", "Corning Gorilla Glass 5", "Corning Gorilla Glass 5", status="VERIFIED"),
        f("chipset", "infinix_zero30_official_specs", "MediaTek Helio G99", "MediaTek Helio G99", key="chipset", status="VERIFIED"),
        f("process_node", "infinix_zero30_official_specs", "6 nm", 6, unit="nm", status="VERIFIED"),
        f("cpu", "infinix_zero30_official_specs", "Octa-core: 2 x Cortex-A76 at 2.2 GHz + 6 x Cortex-A55 at 2.0 GHz", "2x Cortex-A76 2.2 GHz + 6x Cortex-A55 2.0 GHz", key="cpu", status="VERIFIED"),
        f("gpu", "infinix_zero30_official_specs", "Arm Mali-G57 MC2", "Arm Mali-G57 MC2", key="gpu", status="VERIFIED"),
        f("operating_system", "infinix_zero30_official_specs", "XOS 13 based on Android 13", "Android 13 / XOS 13", key="os", status="VERIFIED"),
        f("os_support", "infinix_zero30_official_specs", "No published OS/security support period was found in reviewed manufacturer material", None, status="NOT_DISCLOSED"),
        f("ram_capacity", "infinix_zero30_official_specs", "8 GB RAM; up to 8 GB extended RAM", 8, key="ramGb", unit="GB", status="VERIFIED",
          note="Only the 8 GB installed RAM is shown as catalog RAM; extended/virtual memory is excluded."),
        f("ram_type", "infinix_zero30_official_specs", "LPDDR4X", "LPDDR4X", status="VERIFIED"),
        f("storage_capacity", "infinix_zero30_official_specs", "256 GB ROM", 256, key="storageGb", unit="GB", status="VERIFIED"),
        f("storage_type", "infinix_zero30_official_specs", "UFS 2.2", "UFS 2.2", status="VERIFIED"),
        f("storage_expansion", "infinix_zero30_yugatech_ph", "No card slot / microSD expansion", "No microSD card slot", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", "infinix_zero30_official_specs", "108 MP main (ISOCELL HM6, f/1.75, PDAF) + 2 MP + 2 MP; Philippine reports identify main OIS and macro/depth auxiliary roles", "108 MP main OIS + 2 MP macro + 2 MP depth", key="rearCameraMp", unit="MP", status="VERIFIED_SECONDARY", catalog_value=108,
          note="The manufacturer X6731B page lists a 108 MP main module and two 2 MP modules. One GizGuide article paragraph says 200 MP; that conflicts with the manufacturer, YugaTech and Revu and is not used."),
        f("main_camera_sensor", "infinix_zero30_official_specs", "108 MP Samsung ISOCELL HM6, 1/1.67-inch, 6P lens, PDAF; f/1.75", "Samsung ISOCELL HM6; 108 MP; f/1.75; PDAF", status="VERIFIED"),
        f("ultrawide_camera", "infinix_zero30_official_specs", "Complete listed rear system is 108 MP + 2 MP + 2 MP; no ultrawide module is listed", None, status="NOT_APPLICABLE"),
        f("telephoto_camera", "infinix_zero30_official_specs", "Complete listed rear system is 108 MP + 2 MP + 2 MP; no telephoto module is listed", None, status="NOT_APPLICABLE"),
        f("front_camera", "infinix_zero30_official_specs", "50 MP Samsung ISOCELL JN1, f/2.45, PDAF", 50, key="frontCameraMp", unit="MP", status="VERIFIED"),
        f("video_recording", "infinix_zero30_official_specs", "Rear and front: 2K 30 fps, 1080p 30/60 fps; 720p 30 fps and 720p 120 fps slow motion", "2K@30; 1080p@30/60; 720p@30; 720p@120 slow motion", key="video", status="VERIFIED"),
        f("battery_capacity", "infinix_zero30_official_specs", "5,000 mAh typical capacity", 5000, key="batteryMah", unit="mAh", status="VERIFIED"),
        f("battery_technology", "infinix_zero30_techpinas_ph", "Li-Po, non-removable battery", "Li-Po; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", "infinix_zero30_official_specs", "45 W wired charging; 11 V / 4.1 A or 10 V / 4.5 A; 75% in 30 minutes advertised", 45, key="chargingW", unit="W", status="VERIFIED"),
        f("wireless_charging", "infinix_zero30_official_specs", "Wireless and reverse wireless charging are not stated in the reviewed manufacturer specifications", None, status="NOT_DISCLOSED"),
        f("dimensions", "infinix_zero30_official_specs", "164.52 x 75 x 7.9 mm", "164.52 x 75 x 7.9 mm", key="dimensions", unit="mm", status="VERIFIED"),
        f("weight", "infinix_zero30_official_specs", "182 g", 182, key="weightG", unit="g", status="VERIFIED"),
        f("materials", "infinix_zero30_techpinas_ph", "Local reports describe a glass front and a leather-like rear finish; another local report describes a glass/plastic body. Frame and color-specific back material are not consistently established.", None,
          status="CONFLICTING_INFORMATION", note="Material descriptions vary by source/finish; keep body materials blank rather than generalizing across the three colors."),
        f("ingress_protection", "infinix_zero30_official_specs", "IP54 splash, water and dust resistance; manufacturer says laboratory tested", "IP54", status="VERIFIED"),
        f("sim_esim", "infinix_zero30_official_specs", "Dual nano-SIM; eSIM is not listed", "Dual nano-SIM; eSIM not recorded", key="sim", status="VERIFIED"),
        f("cellular_bands", "infinix_zero30_yugatech_ph", "4G LTE / 3G / 2G; exact Philippine carrier band list not recorded in local launch material", "4G LTE; exact PH bands not recorded", key="cellular", status="VERIFIED_SECONDARY",
          note="This is the ZERO 30 4G model X6731B. No 5G support is assigned. Manufacturer Indonesia bands are not treated as a Philippine band list."),
        f("wifi", "infinix_zero30_official_specs", "Infinix X6731B manufacturer page lists Wi-Fi 5 (802.11 a/b/g/n/ac); YugaTech describes it as Wi-Fi 6", "Wi-Fi 5 (802.11 a/b/g/n/ac)", key="wifi", status="VERIFIED",
          note="Use the manufacturer specification for exact model X6731B; the Philippine YugaTech article's Wi-Fi 6 claim conflicts and is not adopted."),
        f("bluetooth", "infinix_zero30_official_specs", "Bluetooth support is listed, but the manufacturer's model page does not state the version", None, status="NOT_DISCLOSED"),
        f("usb", "infinix_zero30_official_specs", "USB Type-C, OTG supported; data standard/version not listed", "USB Type-C; OTG; data version not recorded", key="ports", status="VERIFIED"),
        f("nfc", "infinix_zero30_official_specs", "NFC supported", True, status="VERIFIED"),
        f("gnss", "infinix_zero30_official_specs", "GPS navigation supported; other satellite constellations are not listed on the reviewed manufacturer page", "GPS; other GNSS constellations not recorded", status="VERIFIED"),
        f("audio", "infinix_zero30_official_specs", "Type-C earphone output; DTS and Hi-Res Audio; local coverage reports stereo speakers with JBL tuning; no 3.5 mm jack", "USB-C audio; stereo speakers; JBL tuning; DTS/Hi-Res; no 3.5 mm jack", key="sound", status="VERIFIED_SECONDARY"),
        f("sensors", "infinix_zero30_official_specs", "G-sensor, e-compass, gyroscope, light sensor, proximity sensor, in-display fingerprint; Z-axis linear motor", "G-sensor; e-compass; gyroscope; light; proximity; in-display fingerprint; Z-axis motor", status="VERIFIED"),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone fields, got {len(rows)}")
    source_ids = {source["id"] for source in SOURCES}
    missing_sources = sorted({item["sourceId"] for item in rows} - source_ids)
    if missing_sources:
        raise ValueError(f"Fields reference undefined sources: {missing_sources}")
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine first online sale was reported for 4 December 2023 through Infinix Mobile's TikTok Shop; PHP 9,999 SRP and a PHP 8,999 introductory offer were reported at launch. Current stock and price are unknown.",
        "philippineAvailability": "The workbook's unsuffixed ZERO 30 row is matched to the Philippine ZERO 30 4G, model X6731B. Revu, YugaTech, GizGuide and TechPinas distinguish this 4G model from ZERO 30 5G and report a 4 December 2023 first online-sale/debut date with an 8 GB / 256 GB configuration. YugaSpecs' later roundup lists a 3 December debut, so 4 December is recorded as the reported first sale date; the exact first transaction is not established. Historical PHP 9,999 SRP and PHP 8,999 promotional pricing are not current prices.",
        "observedAt": OBSERVED,
        "manufacturer": "Infinix Mobility Limited",
        "catalogModel": "ZERO 30 4G",
        "productLine": "ZERO Series",
        "modelNumber": "X6731B",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Reported Philippine first-sale date",
        "researchNotes": "Workbook row 143 lists Infinix ZERO 30 without a 4G/5G suffix. Exact Philippine launch coverage identifies the 4G model X6731B and its 8 GB / 256 GB local configuration. ZERO 30 5G is a separate model and was not merged into this record. Current price and stock are unknown; workbook eligibility remains Pending.",
        "qualityFlag": "Matched unsuffixed workbook name to Philippine ZERO 30 4G / X6731B using contemporaneous local launch evidence. The separate 5G model is not included. Current price, global first-sale date, finish-specific body materials, exact Philippine carrier bands, and image reuse remain unresolved.",
        "openIssues": [
            {"issue": "The workbook name omits the 4G/5G suffix", "action": "Use the Philippine ZERO 30 4G X6731B match from exact local launch sources; keep ZERO 30 5G separate."},
            {"issue": "YugaSpecs lists a 3 December debut while contemporaneous first-sale reports say 4 December", "action": "Label 4 December as the reported first online sale date; do not claim an exact first transaction."},
            {"issue": "One GizGuide paragraph says 200 MP, conflicting with Infinix, YugaTech and Revu's 108 MP exact-model specification", "action": "Use the manufacturer's X6731B value of 108 MP and retain the contradictory article note."},
            {"issue": "YugaTech reports Wi-Fi 6 while the Infinix X6731B page lists Wi-Fi 5", "action": "Use the exact-model manufacturer specification: Wi-Fi 5."},
            {"issue": "Body material reports vary with finish and source", "action": "Leave the single materials field unresolved; do not assign one finish's material to all colors."},
            {"issue": "No current dated, orderable Philippine offer or current stock was verified", "action": "Keep the current price and stock blank; retain only historical launch pricing."},
            {"issue": "Exact product images are available on manufacturer and Philippine pages but no reuse permission is recorded", "action": "Continue using the neutral placeholder until rights are documented."},
            {"issue": "Workbook eligibility remains Pending", "action": "Preserve the existing study-scope status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 143
            or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "infinix"
            or device.get("model", "").casefold() not in {"zero 30", "zero 30 4g"}):
        raise ValueError("Catalog target guard failed for workbook row 143 Infinix ZERO 30")
    if device.get("scopeStatus") != "Pending":
        raise ValueError(f"Expected Pending scope; refusing to alter workbook eligibility: {device.get('scopeStatus')}")
    existing_variants = device.get("variants", [])
    if len(existing_variants) != 1 or existing_variants[0].get("id") not in {f"{DEVICE}-unrecorded", CONFIG}:
        raise ValueError("Expected either the original placeholder or this reviewed ZERO 30 4G configuration")

    variant = {
        "id": CONFIG,
        "label": "8 GB RAM / 256 GB storage",
        "modelCode": "X6731B",
        "sku": None,
        "notes": "Philippine sources match this record to the 4G model X6731B, not ZERO 30 5G. 8 GB is physical RAM; up to 8 GB Extended RAM is virtual. Colors reported locally: Sunset Gold, Misty Green, Pearly White. Current price/stock not verified.",
        "workbookRow": 143,
    }
    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "Infinix",
        "model": "ZERO 30 4G",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "modelCode": "X6731B",
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
        "reason": "Exact Infinix ZERO 30 4G / X6731B product images are shown on Infinix and Philippine launch pages, but a reusable license or written permission to republish is not recorded. Keep the neutral placeholder.",
        "sourcePage": URL_INFINIX,
        "relatedSourcePages": [URL_YUGA_PH, URL_TECHPINAS],
        "assetUrl": None,
        "scope": "Exact Infinix ZERO 30 4G / X6731B; Philippine 8 GB / 256 GB configuration",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Infinix ZERO 30 4G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {
            "device_id": DEVICE, "amount_php": 9999, "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_x6731b_8gb_256gb_configuration",
            "variant_ram_gb": 8, "variant_storage_gb": 256,
            "price_type": "historical_ph_launch_srp", "source_published_at": "2023-12-02",
            "excerpt": "Revu reports PHP 9,999 as the Philippine suggested retail price for ZERO 30 4G; YugaTech and TechPinas also report PHP 9,999.",
            "source_url": URL_REVU, "source_kind": "historical_local_price_report",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_launch_srp_not_current",
        },
        {
            "device_id": DEVICE, "amount_php": 8999, "configuration_id": CONFIG,
            "configuration_match": "exact_philippine_x6731b_8gb_256gb_configuration",
            "variant_ram_gb": 8, "variant_storage_gb": 256,
            "price_type": "historical_first_sale_promotion", "source_published_at": "2023-12-02",
            "excerpt": "PHP 8,999 was announced as the first Infinix TikTok Shop sale price for 4 December 2023, instead of the PHP 9,999 SRP. It is retained as a historical promotion, not a current offer.",
            "source_url": URL_REVU, "source_kind": "historical_advertised_price_report",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_first_sale_offer_not_current",
        },
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Infinix", "model_name": "ZERO 30 4G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_INFINIX, "result": "Manufacturer specification page identifies ZERO 30 4G model X6731B and exact hardware details."},
            {"device_id": DEVICE, "source_url": URL_YUGA_PH, "result": "Philippine launch source identifies the 4G configuration, 8/256 memory, PHP 9,999 likely SRP and advertised PHP 8,999 first sale on 4 December."},
            {"device_id": DEVICE, "source_url": URL_REVU, "result": "Confirms 4G identity, 4 December first online sale, PHP 9,999 SRP and PHP 8,999 introductory promotion."},
            {"device_id": DEVICE, "source_url": URL_TECHPINAS, "result": "Exact-model hands-on report maps X6731B to ZERO 30 4G, reports local release on 4 December 2023 and detailed specs."},
            {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "Local launch corroboration; article's 200 MP statement conflicts with manufacturer and multiple exact-model sources reporting 108 MP."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "model": "Infinix ZERO 30 4G", "workbookRow": 143, "modelCode": "X6731B",
        "configuration": variant["label"], "reviewedFields": len(review["fields"]),
        "verifiedFields": sum(row["status"] in {"VERIFIED", "VERIFIED_SECONDARY"} for row in review["fields"]),
        "notDisclosedFields": sum(row["status"] == "NOT_DISCLOSED" for row in review["fields"]),
        "conflictingFields": sum(row["status"] == "CONFLICTING_INFORMATION" for row in review["fields"]),
        "launchSrpPhp": 9999, "firstSalePromotionPhp": 8999,
        "currentPrice": None, "scopeStatus": "Pending",
        "imageStatus": "REUSE_RIGHTS_NOT_ESTABLISHED",
    }, indent=2))


if __name__ == "__main__":
    main()
