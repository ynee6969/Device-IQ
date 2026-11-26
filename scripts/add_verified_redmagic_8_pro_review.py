#!/usr/bin/env python3
"""Review the Philippine REDMAGIC 8 Pro and its exact memory configurations."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/redmagic-8-pro-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_504422c5fc36f4"
MATTE = f"{DEVICE}-ph-12gb-256gb-matte"
VOID = f"{DEVICE}-ph-16gb-512gb-void"

URL_SPECS = "https://eu.redmagic.gg/pages/redmagic-8-pro-specs"
URL_GLOBAL_ANNOUNCEMENT = "https://global.redmagic.gg/blogs/news/the-redmagic-8-pro-is-almost-here"
URL_GLOBAL_SALE = "https://global.redmagic.gg/blogs/news/the-redmagic-8-pro-a-gaming-revolution"
URL_MANUAL = "https://manuals.plus/m/6fff331b1f28c822c826e465c7bd3d6ef4651ab7c5a014167ad6df113f2039c7_optim.pdf"
URL_UNBOX = "https://unbox.ph/gadget/red-magic-8-pro-official-in-the-philippines/"
URL_TECHNOBABOY = "https://www.technobaboy.com/2023/02/21/zte-redmagic-8-pro-gaming-phone-price-philippines/"
URL_YUGA = "https://www.yugatech.com/news/redmagic-8-pro-now-available-in-the-philippines/"
URL_GIZGUIDE = "https://www.gizguide.com/2023/08/redmagic-8-pro-digital-walker.html"
URL_GSMARENA = "https://www.gsmarena.com/nubia_red_magic_8_pro-review-2520.php"
URL_NANOREVIEW = "https://nanoreview.net/en/phone/zte-nubia-red-magic-8-pro"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-nubia-Red-Magic-8-Pro"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("redmagic8_global_specs", "REDMAGIC (manufacturer)", URL_SPECS,
        "Manufacturer specifications for REDMAGIC 8 Pro global model",
        "The manufacturer page lists the global Matte 12/256 and Void 16/512 configurations, dimensions, display, Snapdragon platform, memory, cameras, battery, network bands, connectivity and sensors. Regional Philippine radio approval is not established by this page."),
    src("redmagic8_global_announcement", "REDMAGIC (manufacturer)", URL_GLOBAL_ANNOUNCEMENT,
        "Global announcement date and global configuration naming",
        "REDMAGIC's global article dated 16 January 2023 previews the device and states that it would go on sale on 2 February 2023. The article distinguishes Matte 12/256 from Void 16/512.", "2023-01-16"),
    src("redmagic8_global_sale", "REDMAGIC (manufacturer)", URL_GLOBAL_SALE,
        "First global sale date and international configuration cross-check",
        "Manufacturer's global launch article says sales began 2 February 2023; Matte is 12/256 and Void is 16/512. Global USD prices are not treated as Philippine prices.", "2023-02-02"),
    src("redmagic8_user_guide", "Nubia Technology manufacturer user guide (copy hosted by Manuals.plus)", URL_MANUAL,
        "Manufacturer-authored regulatory guide for global model code",
        "The guide identifies radio model NX729J and hardware version NX729J_V1AMB. This supports the international model code only; it is not an NTC Philippines certification or proof of the exact code on a local retail unit."),
    src("redmagic8_ph_unbox", "UNBOX PH", URL_UNBOX,
        "Philippine official-launch coverage, configurations and local prices",
        "Published 21 February 2023. Reports official Philippine availability through local channels and prices of PHP 43,990 for 12/256 and PHP 53,990 for 16/512. These conflict slightly with other local reports and are retained as dated historical price observations, not current prices.", "2023-02-21"),
    src("redmagic8_ph_technobaboy", "Technobaboy Philippines", URL_TECHNOBABOY,
        "Independent Philippine launch, hardware and price cross-check",
        "Published 21 February 2023. Reports local launch, 12/256 and 16/512 configurations and prices of PHP 42,999 and PHP 53,999. The 2 MP rear module is described as macro, unlike UNBOX PH's depth description.", "2023-02-21"),
    src("redmagic8_ph_yugatech", "YugaTech Philippines", URL_YUGA,
        "Local retail availability at Digital Walker, exact configurations and prices",
        "Published 26 August 2023. Reports the phone available at Digital Walker, 12/256 Matte at PHP 42,999, and 16/512 Void/Titanium at PHP 53,999. The price is a historical local retail report, not a current offer.", "2023-08-26"),
    src("redmagic8_ph_gizguide", "GizGuide Philippines", URL_GIZGUIDE,
        "Digital Walker availability, local Titanium configuration and pricing cross-check",
        "Published 23 August 2023. Reports Digital Walker availability, 12/256 Matte at PHP 42,999 and 16/512 Titanium at PHP 53,999. Its spec summary has a conflicting RAM typo; configuration matching follows the local price/availability statements and manufacturer configuration table.", "2023-08-23"),
    src("redmagic8_gsmarena", "GSMArena", URL_GSMARENA,
        "International 12/256 review configuration and independent hardware cross-check",
        "GSMArena's 16 January 2023 review unit is the international Matte 12/256, 6000 mAh, 65 W version. Its global review supports CPU, display, camera, audio, connectivity and no microSD, but does not establish Philippine price or local regulatory status.", "2023-01-16"),
    src("redmagic8_nanoreview", "NanoReview", URL_NANOREVIEW,
        "Independent chipset and technical cross-check",
        "Exact-model profile cross-checks Snapdragon 8 Gen 2, 4 nm process, CPU/GPU architecture, display, battery and network data. The default profile shows another memory variant; its RAM/storage selection is not used as Philippine SKU evidence."),
    src("redmagic8_kimovil", "Kimovil", URL_KIMOVIL,
        "Global configuration comparison only",
        "Kimovil lists global 12/256 and 16/512 separately from China-market 8/128, 8/256 and other 165 W variants. Used only to guard against mixing Chinese Pro/Pro+ specifications into the international Philippine configurations."),
]
S = {item["id"]: item["id"] for item in SOURCES}


def f(fid: str, sid: str, value, normalized=None, *, key: str | None = None,
      unit: str | None = None, status: str = "VERIFIED", note: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    return row


def prices_for(config: str) -> list[dict]:
    all_prices = [
        (MATTE, 12, 256, 42999, "2023-02-21", URL_TECHNOBABOY, "Technobaboy reports PHP 42,999 for the 12/256 model at Philippine launch."),
        (MATTE, 12, 256, 43990, "2023-02-21", URL_UNBOX, "UNBOX PH reports PHP 43,990 official local price for 12/256."),
        (MATTE, 12, 256, 42999, "2023-08-26", URL_YUGA, "YugaTech reports the 12/256 Matte at PHP 42,999 through Digital Walker."),
        (MATTE, 12, 256, 42999, "2023-08-23", URL_GIZGUIDE, "GizGuide reports the 12/256 Matte at PHP 42,999 through Digital Walker."),
        (VOID, 16, 512, 53990, "2023-02-21", URL_UNBOX, "UNBOX PH reports PHP 53,990 official local price for 16/512."),
        (VOID, 16, 512, 53999, "2023-08-26", URL_YUGA, "YugaTech reports the 16/512 Void/Titanium at PHP 53,999 through Digital Walker."),
        (VOID, 16, 512, 53999, "2023-08-23", URL_GIZGUIDE, "GizGuide reports the 16/512 Titanium at PHP 53,999 through Digital Walker."),
    ]
    return [{
        "device_id": DEVICE, "amount_php": amount, "configuration_id": cid,
        "configuration_match": "exact_philippine_configuration",
        "variant_ram_gb": ram, "variant_storage_gb": storage,
        "price_type": "historical_ph_launch_or_retail_price",
        "source_published_at": published,
        "excerpt": excerpt, "source_url": url,
        "source_kind": "historical_local_price_observation",
        "observed_at": OBSERVED, "local_availability_verified": True,
        "availability_status": "historical_price_not_current",
    } for cid, ram, storage, amount, published, url, excerpt in all_prices if cid == config]


def fields(config: str, ram: int, storage: int, label: str) -> list[dict]:
    price_candidates = prices_for(config)
    price_evidence = [{
        "value": f"PHP {p['amount_php']:,}", "sourceUrl": p["source_url"],
        "sourceKind": "independent_ph_reference", "observedAt": OBSERVED,
        "excerpt": p["excerpt"], "configurationMatch": label,
        "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True,
    } for p in price_candidates if p["source_published_at"] == "2023-02-21"]
    rows = [
        f("model_number", S["redmagic8_user_guide"],
          "Manufacturer-authored guide lists REDMAGIC 8 Pro radio model NX729J (hardware NX729J_V1AMB); Philippine NTC listing for this model was not located.",
          "NX729J", status="VERIFIED_SECONDARY",
          note="NX729J is the manufacturer global model code; do not treat this as confirmation of a Philippine NTC certificate or local box SKU."),
        f("global_release_date", S["redmagic8_global_sale"],
          "REDMAGIC says global sale began 2 February 2023; product introduction was announced 16 January 2023.",
          "2023-02-02", note="Records the first global sale date; the 16 January announcement is preserved separately in source notes."),
        f("configuration", S["redmagic8_global_specs"], label, label),
        f("philippine_release_date", S["redmagic8_ph_unbox"],
          "Philippine official launch reported 21 February 2023; Digital Walker store availability was reported in August 2023.",
          "2023-02-21", status="VERIFIED_SECONDARY",
          note="The date is the earliest corroborated Philippine official launch report, not an exact first-sale transaction."),
        f("official_launch_price_php", S["redmagic8_ph_unbox"],
          "Local launch sources conflict: " + "; ".join(p["excerpt"] for p in price_candidates),
          None, status="CONFLICTING_INFORMATION", unit="PHP",
          note="Do not select a single launch SRP while contemporaneous Philippine sources report different values."),
        f("current_price_php", S["redmagic8_ph_yugatech"],
          "Reviewed evidence is historical; no dated, orderable Philippine offer for this exact configuration was verified on 26 November 2026.",
          None, status="PENDING_VERIFICATION", unit="PHP",
          note="Keep current catalog price blank; retain historical price observations by source and date."),
        f("display_size", S["redmagic8_global_specs"], "6.8 inches", 6.8, key="displayInches", unit="in"),
        f("display_technology", S["redmagic8_global_specs"], "AMOLED", "AMOLED", key="displayType"),
        f("display_resolution", S["redmagic8_global_specs"], "1116 x 2480 pixels", "1116 x 2480", key="resolution"),
        f("display_refresh_rate", S["redmagic8_global_specs"], "Up to 120 Hz", 120, key="refreshHz", unit="Hz"),
        f("display_brightness", S["redmagic8_global_specs"], "1300 nits maximum brightness", 1300, unit="nits"),
        f("display_protection", S["redmagic8_global_specs"], "Corning Gorilla Glass; NanoReview identifies Gorilla Glass 5", "Corning Gorilla Glass 5", status="VERIFIED_SECONDARY"),
        f("chipset", S["redmagic8_global_specs"], "Qualcomm Snapdragon 8 Gen 2", "Qualcomm Snapdragon 8 Gen 2", key="chipset"),
        f("process_node", S["redmagic8_nanoreview"], "Snapdragon 8 Gen 2 fabricated on TSMC 4 nm process", 4, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", S["redmagic8_nanoreview"], "Octa-core: 1x Cortex-X3 up to 3.2 GHz + 2x Cortex-A715 up to 2.8 GHz + 2x Cortex-A710 up to 2.8 GHz + 3x Cortex-A510 up to 2.0 GHz", "1x Cortex-X3 3.2 GHz + 2x Cortex-A715 2.8 GHz + 2x Cortex-A710 2.8 GHz + 3x Cortex-A510 2.0 GHz", status="VERIFIED_SECONDARY"),
        f("gpu", S["redmagic8_global_specs"], "Adreno GPU; exact model Adreno 740 cross-checked by GSMArena", "Adreno 740", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", S["redmagic8_global_specs"], "REDMAGIC OS 6.0 based on Android 13", "Android 13 with REDMAGIC OS 6.0", key="os"),
        f("os_support", S["redmagic8_global_specs"], "No guaranteed OS-upgrade or security-update duration stated in reviewed manufacturer materials; official update log exists.", None, status="NOT_DISCLOSED"),
        f("ram_capacity", S["redmagic8_global_specs"], f"{ram} GB LPDDR5X RAM in the {label} global configuration", ram, key="ramGb", unit="GB"),
        f("ram_type", S["redmagic8_global_specs"], "LPDDR5X", "LPDDR5X", key="ramType"),
        f("storage_capacity", S["redmagic8_global_specs"], f"{storage} GB UFS 4.0 storage in the {label} global configuration", storage, key="storageGb", unit="GB"),
        f("storage_type", S["redmagic8_global_specs"], "UFS 4.0", "UFS 4.0", key="storageType"),
        f("storage_expansion", S["redmagic8_gsmarena"], "No microSD card slot", "No microSD slot", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", S["redmagic8_global_specs"], "50 MP + 8 MP + 2 MP rear camera system. The manufacturer page gives resolutions; local reports disagree whether the 2 MP module is macro or depth.", "50 MP main + 8 MP ultra-wide + 2 MP module; module role unresolved", status="VERIFIED_SECONDARY",
          note="Resolution/count are supported by the manufacturer; the final module role is deliberately not assigned because Philippine sources conflict."),
        f("main_camera_sensor", S["redmagic8_global_specs"], "50 MP Samsung GN5, 1/1.57-inch sensor, f/1.88", "50 MP Samsung GN5; 1/1.57 in; f/1.88"),
        f("ultrawide_camera", S["redmagic8_global_specs"], "8 MP ultra-wide camera, 120-degree field of view, f/2.2", "8 MP; 120 degrees; f/2.2"),
        f("telephoto_camera", S["redmagic8_global_specs"], "Manufacturer lists a three-module 50/8/2 MP rear array and no telephoto camera", "No telephoto module listed", status="NOT_APPLICABLE"),
        f("front_camera", S["redmagic8_global_specs"], "16 MP second-generation under-display camera", 16, key="frontCameraMp", unit="MP"),
        f("video_recording", S["redmagic8_global_specs"], "Rear: up to 8K/30, 4K/30 or 60, 1080p/30 or 60, 720p/30; front: 1080p/30 or 60 reported by GSMArena", "Rear up to 8K/30; 4K/60; 1080p/60. Front 1080p/60", key="video", status="VERIFIED_SECONDARY"),
        f("battery_capacity", S["redmagic8_global_specs"], "6000 mAh dual-cell battery", 6000, key="batteryMah", unit="mAh"),
        f("battery_technology", S["redmagic8_nanoreview"], "Lithium-polymer (Li-Po); non-removable", "Li-Po; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", S["redmagic8_global_specs"], "65 W quick charging for global version", 65, key="chargingW", unit="W"),
        f("wireless_charging", S["redmagic8_nanoreview"], "Wireless charging: No", "No wireless charging", status="VERIFIED_SECONDARY"),
        f("dimensions", S["redmagic8_global_specs"], "Manufacturer lists 163.98 x 76.35 x 9.47 mm; GSMArena lists 164.0 x 76.4 x 8.9 mm.", None, status="CONFLICTING_INFORMATION", unit="mm",
          note="The recorded depth conflicts materially between the manufacturer and GSMArena international review; withhold dimensions pending resolution.",
        ),
        f("weight", S["redmagic8_global_specs"], "228 g", 228, key="weightG", unit="g"),
        f("materials", S["redmagic8_global_specs"], "Metal middle frame and glass rear cover", "Metal frame; glass rear"),
        f("ingress_protection", S["redmagic8_gsmarena"], "No ingress-protection rating listed for this model", "No IP rating listed", status="VERIFIED_SECONDARY"),
        f("sim_esim", S["redmagic8_global_specs"], "Dual nano-SIM; eSIM is not listed by the manufacturer", "Dual nano-SIM; eSIM not recorded"),
        f("cellular_bands", S["redmagic8_global_specs"], "Global page: 2G GSM 2/3/5/8; 3G WCDMA 1/2/4/5/6/8/19; LTE FDD 1/2/3/4/5/7/8/12/17/18/19/20/26/28A/28B/66 and TDD 34/38/39/40/41; 5G SA/NSA bands listed by manufacturer. Philippine SKU-specific band approval not confirmed.", "5G SA/NSA; global bands per manufacturer; Philippine SKU-specific compatibility not confirmed", key="cellular"),
        f("wifi", S["redmagic8_global_specs"], "Wi-Fi 7 802.11b/g/n/ac/ax/be, tri-band 2.4/5/6 GHz", "Wi-Fi 7; tri-band 2.4/5/6 GHz", key="wifi"),
        f("bluetooth", S["redmagic8_global_specs"], "Bluetooth 5.3", "Bluetooth 5.3"),
        f("usb", S["redmagic8_global_specs"], "USB 3.1 Type-C with DisplayPort output; converter required for HDMI", "USB Type-C 3.1; DisplayPort output", key="ports"),
        f("nfc", S["redmagic8_global_specs"], "NFC: Yes", "Yes"),
        f("gnss", S["redmagic8_global_specs"], "GPS and AGPS listed by manufacturer; GSMArena also lists GLONASS, BDS, Galileo and QZSS", "GPS; AGPS; additional GNSS not specified in manufacturer page", key="gnss", status="VERIFIED_SECONDARY"),
        f("audio", S["redmagic8_gsmarena"], "Stereo speakers and 3.5 mm headphone jack", "Stereo speakers; 3.5 mm jack", key="sound", status="VERIFIED_SECONDARY"),
        f("sensors", S["redmagic8_global_specs"], "Under-display fingerprint, G-sensor, electronic compass, gyroscope, proximity, ambient-light sensor and sensor hub", "Under-display fingerprint; accelerometer; compass; gyroscope; proximity; ambient light; sensor hub"),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field assessments, got {len(rows)}")
    rows[4]["candidateEvidence"] = price_evidence
    rows[5]["candidateEvidence"] = [{
        "value": p["excerpt"], "sourceUrl": p["source_url"],
        "sourceKind": "historical_local_price", "observedAt": OBSERVED,
        "excerpt": p["excerpt"], "configurationMatch": label,
        "reviewStatus": "PENDING_VERIFICATION", "localAvailabilityVerified": True,
    } for p in price_candidates]
    rows[23]["candidateEvidence"] = [
        {"value": "2 MP macro module reported", "sourceUrl": URL_TECHNOBABOY,
         "sourceKind": "independent_ph_reference", "observedAt": OBSERVED,
         "excerpt": "Technobaboy describes the 2 MP rear camera as macro.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
        {"value": "2 MP depth sensor reported", "sourceUrl": URL_UNBOX,
         "sourceKind": "independent_ph_reference", "observedAt": OBSERVED,
         "excerpt": "UNBOX PH describes the 2 MP rear camera as a depth sensor.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
    ]
    rows[33]["candidateEvidence"] = [
        {"value": "9.47 mm", "sourceUrl": URL_SPECS, "sourceKind": "manufacturer_global",
         "observedAt": OBSERVED, "excerpt": "Manufacturer specification table lists 163.98 x 76.35 x 9.47 mm.",
         "configurationMatch": label, "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
        {"value": "8.9 mm", "sourceUrl": URL_GSMARENA, "sourceKind": "independent_global_review",
         "observedAt": OBSERVED, "excerpt": "GSMArena lists 164.0 x 76.4 x 8.9 mm for the international 12/256 review unit.",
         "configurationMatch": "international Matte 12 GB / 256 GB", "reviewStatus": "CONFLICTING_INFORMATION", "localAvailabilityVerified": True},
    ]
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_OFFICIAL_LAUNCH",
        "availabilityStatus": "Philippine launch coverage dated 21 February 2023 identifies the REDMAGIC 8 Pro as officially available through local channels. Digital Walker retail availability was separately reported in August 2023. Current stock and price are not verified.",
        "philippineAvailability": "UNBOX PH and Philippine technology outlets reported the REDMAGIC 8 Pro as officially launched in the Philippines on 21 February 2023. Later YugaTech and GizGuide reporting identified Digital Walker retail availability. The local 12/256 Matte and 16/512 Void/Titanium configurations match the international REDMAGIC 8 Pro, not the China-market 8/128 or Pro+ variants. Local launch-price reports conflict and are preserved as historical observations. The NX729J model code is supported by the global manufacturer user guide, but a Philippine NTC record tying it to a local unit was not located.",
        "observedAt": OBSERVED,
        "manufacturer": "ZTE nubia (REDMAGIC)",
        "catalogModel": "8 Pro",
        "productLine": "REDMAGIC 8 series",
        "modelNumber": "NX729J",
        "philippineReleaseYear": 2023,
        "philippineDateLabel": "Philippine official launch reported 21 February 2023; Digital Walker retail availability reported in August 2023",
        "researchNotes": "Workbook row 160 REDMAGIC 8 Pro matches the global model sold through Philippine local channels in two exact configurations: Matte 12 GB / 256 GB and Void 16 GB / 512 GB; later Philippine retailer reports also mention a Titanium 16/512 option. The global model was announced 16 January 2023 and global sale began 2 February. Philippine launch coverage is dated 21 February. Local reports disagree on launch prices (PHP 42,999 vs PHP 43,990 for 12/256; PHP 53,999 vs PHP 53,990 for 16/512) and on whether the 2 MP rear module is macro or depth. Manufacturer and GSMArena dimensions disagree on depth; dimensions withheld. Current local price is not verified. Manufacturer guide identifies global code NX729J, but Philippine NTC registration of this specific model was not located. Image reuse rights were not established. Workbook study scope remains Pending.",
        "qualityFlag": "Philippine official launch verified; exact 12/256 Matte and 16/512 Void/Titanium configurations supported. Historical local prices and 2 MP camera role conflict; body depth conflicts; current price and Philippine NTC linkage unverified; image reuse rights not established; study scope remains Pending.",
        "openIssues": [
            {"issue": "Philippine launch reports conflict on local price for both configurations", "action": "Retain source-specific dated historical price candidates and leave current catalog price blank."},
            {"issue": "Local sources call the 2 MP camera module macro or depth", "action": "Keep its role unresolved while retaining manufacturer-confirmed rear camera resolutions."},
            {"issue": "Manufacturer and GSMArena list different body depth", "action": "Leave the catalog dimensions blank until an exact-unit or region-specific source resolves the conflict."},
            {"issue": "NX729J is a global manufacturer code; a Philippine NTC record tied to this device was not found", "action": "Do not claim Philippine type approval or local box-code confirmation."},
            {"issue": "Manufacturer product imagery is visible but no reuse license or written permission was found", "action": "Retain the neutral placeholder and exact-model image source-page metadata."},
            {"issue": "Workbook study scope is Pending", "action": "Preserve the supplied scope status; availability verification does not change eligibility."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("workbookRow") != 160 or device.get("category") != "smartphones"
            or device.get("brand") != "REDMAGIC" or device.get("model") != "8 Pro"):
        raise ValueError("Workbook row 160 guard failed; expected REDMAGIC 8 Pro smartphone")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("REDMAGIC 8 Pro already has manual-review rows; refusing duplicate replacement")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise ValueError("Expected the original unrecorded-configuration placeholder before review")

    matte = {"id": MATTE, "label": "12 GB RAM / 256 GB storage · Matte",
             "sku": None, "modelCode": "NX729J",
             "notes": "International Matte configuration; Philippine launch sources verify this local memory/storage configuration. Local price reports conflict; current price not verified."}
    void = {"id": VOID, "label": "16 GB RAM / 512 GB storage · Void (Titanium also reported locally)",
            "sku": None, "modelCode": "NX729J",
            "notes": "International Void configuration; Philippine retail reports also identify a Titanium 16/512 version. Local price reports conflict; current price not verified."}
    add_review(manual, catalog, {
        "deviceId": DEVICE, "configurationId": MATTE, "brand": "REDMAGIC", "model": "8 Pro",
        "configuration": matte["label"], "modelCode": "NX729J", "sku": None,
        "sources": SOURCES, "fields": fields(MATTE, 12, 256, matte["label"]),
        "availabilityEvidence": availability_evidence(),
        "replacementVariants": [matte, void], "replaceUnrecordedPlaceholder": True,
    })
    # The catalog helper has not yet materialized review variants; seed only its
    # in-memory lookup so the second configuration can receive its own field audit.
    device["variants"] = [{"id": MATTE, "specs": {}}, {"id": VOID, "specs": {}}]
    add_review(manual, catalog, {
        "deviceId": DEVICE, "configurationId": VOID, "brand": "REDMAGIC", "model": "8 Pro",
        "configuration": void["label"], "modelCode": "NX729J", "sku": None,
        "sources": SOURCES, "fields": fields(VOID, 16, 512, void["label"]),
    })
    target_keys = {(DEVICE, MATTE), (DEVICE, VOID)}
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "REDMAGIC's official global product/specification page shows the exact REDMAGIC 8 Pro and configuration-specific designs, but no reusable license or written permission to copy or hotlink was identified. Keep the neutral placeholder.",
        "sourcePage": URL_SPECS, "assetUrl": None,
        "scope": "Exact REDMAGIC 8 Pro global design; Philippine 12/256 Matte and 16/512 Void/Titanium configurations",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for REDMAGIC 8 Pro",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [*prices_for(MATTE), *prices_for(VOID)]
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "REDMAGIC", "model_name": "8 Pro", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_SPECS, "result": "Manufacturer global specs confirm Matte 12/256 and Void 16/512, hardware, cameras, battery, connectivity and sensors."},
            {"device_id": DEVICE, "source_url": URL_GLOBAL_ANNOUNCEMENT, "result": "Official global announcement dated 16 January 2023; sale date given as 2 February."},
            {"device_id": DEVICE, "source_url": URL_UNBOX, "result": "Philippine launch coverage dated 21 February identifies local channels, both configs and local prices; values conflict with other PH sources."},
            {"device_id": DEVICE, "source_url": URL_TECHNOBABOY, "result": "Philippine launch article corroborates 12/256 and 16/512, records different local price values and calls the 2 MP module macro."},
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech reports Digital Walker availability and both configurations/colors in August 2023; historical price observations retained."},
            {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "GizGuide reports Digital Walker availability, Titanium 16/512, prices, and a camera module label; its RAM specification summary contains a typo."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "Exact international 12/256 review cross-checks hardware, but differs from manufacturer page on body depth; the dimensions field is withheld."},
            {"device_id": DEVICE, "source_url": URL_NANOREVIEW, "result": "Chipset CPU/GPU, process, battery and general hardware cross-check; not used as PH configuration proof."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Global 12/256 and 16/512 are listed separately from China-market 8 GB and Pro+ configurations."},
            {"device_id": DEVICE, "source_url": URL_MANUAL, "result": "Manufacturer-authored user guide copy identifies international model NX729J; no Philippine NTC record tying this code to the local unit found."},
        ],
        "prices": prices,
    }
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "workbookRow": 160, "device": "REDMAGIC 8 Pro",
        "configurations": [matte["label"], void["label"]],
        "reviewedFields": 46, "reviewedConfigurationFieldRows": 92,
        "sources": len(SOURCES), "historicalPriceObservations": len(prices),
        "globalSale": "2023-02-02", "philippineLaunchReport": "2023-02-21",
        "currentPrice": None, "cameraModuleRole": "conflicting",
        "dimensions": "conflicting; withheld", "imageRights": "not established; placeholder retained",
        "scopeStatus": "Pending",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
