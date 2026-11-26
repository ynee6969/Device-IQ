#!/usr/bin/env python3
"""Review the Philippine TCL 20B / 6159K record against local and manufacturer sources."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/tcl-20b-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_41c970f372aada"
MODEL_CODE = "6159K"
CONFIG = f"{DEVICE}-4gb-64gb-ph"
URL_NTC = "https://region4b.ntc.gov.ph/wp-content/uploads/2022/01/GEC_12312021.pdf"
URL_TCL_SPECS = "https://www.tcl.com/global/en/mobile/tcl-20b/specifications"
URL_TCL_PRODUCT = "https://www.tcl.com/global/en/mobile/tcl-20b"
URL_YUGATECH = "https://www.yugatech.com/mobile/tcl-20b-specs-price-philippines/"
URL_YUGATECH_PRICE_LIST = "https://www.yugatech.com/tcl-phone-price-list-philippines"
URL_MANILASHAKER = "https://manilashaker.com/tcl-20b-now-in-ph/"
URL_GSMARENA = "https://www.gsmarena.com/tcl_20b-11261.php"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-tcl-20b"
IMAGE_URL = "https://static-obg.tcl.com/content/dam/brandsite/region/global/migrate/tcl-20b/images/mobile/landing_s4_bg.png"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


def f(fid: str, sid: str, value, normalized=None, *, key: str | None = None,
      unit: str | None = None, status: str = "VERIFIED", note: str | None = None) -> dict:
    result = {"fieldId": fid, "status": status, "sourceId": sid,
              "sourceValue": value, "normalizedValue": normalized}
    if key:
        result.update({"catalogKey": key, "catalogValue": normalized})
    if unit:
        result["unit"] = unit
    if note:
        result["note"] = note
    return result


def sources() -> list[dict]:
    return [
        src("tcl20b_ph_ntc_gec_2021", "National Telecommunications Commission Region IV-B", URL_NTC,
            "Exact Philippine NTC registration model match",
            "The NTC GEC entry ESD-GEC-2106984 identifies brand/model TCL 6159K and marketing name TCL 20B; issued 29 September 2021.", "2021-09-29"),
        src("tcl20b_manufacturer_specs", "TCL Global", URL_TCL_SPECS,
            "Manufacturer specifications for the TCL 20B, including values explicitly marked for model 6159K",
            "TCL's product specifications list display, cameras, platform, 4 GB LPDDR4x / 64 GB eMMC, battery, charging, connectivity, sensors and physical data. Several network/SIM/NFC rows explicitly name model 6159K; market-wide statements are not treated as local launch proof."),
        src("tcl20b_manufacturer_product", "TCL Global", URL_TCL_PRODUCT,
            "Exact-model product identity and image asset source",
            "TCL's product page is for the TCL 20B and shows the matching curved-back device and official color names Space Grey and Nebula Purple. No reusable image license or written permission was found."),
        src("tcl20b_yugatech_ph_launch", "YugaTech Philippines", URL_YUGATECH,
            "Philippine authorized availability, 4/64 configuration, local launch price, and local color names",
            "YugaTech reports TCL Mobile Philippines announced the device available in the Philippines on 4 March 2022 through Lazada, Shopee, and authorized TCL dealer partners. It lists 4 GB/64 GB and PHP 8,190. Local article color names Purple and Black differ from TCL Global's Space Grey and Nebula Purple; keep that naming discrepancy visible.", "2022-03-04"),
        src("tcl20b_yugatech_price_history", "YugaTech Philippines", URL_YUGATECH_PRICE_LIST,
            "Dated historical Philippine price listing and current-price distinction",
            "The price list retains TCL 20B at PHP 8,190 with the verified report date 4 March 2022; this is a historical price reference and does not prove a currently orderable offer.", "2022-03-04"),
        src("tcl20b_manilashaker_ph", "ManilaShaker Philippines", URL_MANILASHAKER,
            "Independent Philippine configuration, price, and dealer-availability cross-check",
            "The March 4, 2022 report independently lists 4 GB/64 GB at PHP 8,190 and availability through local online stores and authorized partners; selected technical specifications cross-check YugaTech.", "2022-03-04"),
        src("tcl20b_gsmarena", "GSMArena", URL_GSMARENA,
            "Exact-model technical-reference lookup",
            "The exact TCL 20B product page was located. It is a global reference only; no Philippine price or availability claim is taken from it."),
        src("tcl20b_kimovil", "Kimovil", URL_KIMOVIL,
            "Independent exact-model 4 GB/64 GB technical cross-check",
            "Kimovil identifies TCL 20B Global as one 4 GB/64 GB version and provides secondary hardware details. Its international pricing, colors and market data are not used as Philippine evidence."),
    ]


def fields() -> list[dict]:
    sp = "tcl20b_manufacturer_specs"
    local = "tcl20b_yugatech_ph_launch"
    return [
        f("model_number", "tcl20b_ph_ntc_gec_2021", "NTC entry: TCL 6159K, TCL 20B", MODEL_CODE,
          note="Exact NTC row matches both the model code and marketing name."),
        f("configuration", local, "Philippine launch configuration: 4 GB RAM / 64 GB storage", "4 GB RAM / 64 GB storage",
          status="VERIFIED_SECONDARY", note="YugaTech reports the local configuration; TCL Global lists 4 GB LPDDR4x and 64 GB eMMC for the exact model family."),
        f("ram_capacity", sp, "4 GB LPDDR4x", 4, key="ramGb", unit="GB"),
        f("ram_type", sp, "LPDDR4x", "LPDDR4x"),
        f("storage_capacity", sp, "64 GB ROM; 47 GB available storage stated by TCL", 64, key="storageGb", unit="GB",
          note="Catalog stores installed capacity, not the 47 GB free-space figure."),
        f("storage_type", sp, "eMMC", "eMMC", key="storageType"),
        f("expandable_storage", sp, "MicroSD up to 512 GB; 6159K uses a hybrid second SIM / microSD slot", "microSD up to 512 GB; hybrid slot"),
        f("display_size", sp, "6.52-inch mini-notch display", 6.52, key="displayInches", unit="in"),
        f("display_technology", local, "6.52-inch IPS display", "IPS LCD", status="VERIFIED_SECONDARY",
          note="The Philippine launch report identifies IPS; TCL's specification page does not explicitly name the panel class."),
        f("display_resolution", sp, "HD+ (720 x 1600 pixels)", "720 x 1600", key="resolution"),
        f("display_refresh_rate", sp, "Refresh rate not listed in the reviewed manufacturer specification", None,
          status="PENDING_VERIFICATION", unit="Hz"),
        f("display_brightness", sp, "450 nits typical", 450, key="brightnessNits", unit="nits"),
        f("chipset", sp, "MTK6762 octa-core; Philippine launch source calls it MediaTek Helio P22", "MediaTek Helio P22 (MTK6762)", key="chipset"),
        f("cpu", sp, "4x 1.8 GHz + 4x 1.5 GHz octa-core", "4x 1.8 GHz + 4x 1.5 GHz"),
        f("gpu", sp, "IMG GE8320", "IMG PowerVR GE8320", key="gpu"),
        f("operating_system", sp, "Android 11 with TCL UI", "Android 11 / TCL UI", key="os"),
        f("global_release_date", "tcl20b_yugatech_ph_launch", "Global announcement/release date not established from the reviewed manufacturer source; Philippine coverage says it was first unveiled in Russia in December 2021", None,
          status="PENDING_VERIFICATION", note="Do not assign a global release date from a secondary database result while the manufacturer's exact release event is unconfirmed."),
        f("philippine_release_date", local, "Philippine availability announced 4 March 2022", "2022-03-04", status="VERIFIED_SECONDARY",
          note="The date is the dated Philippine announcement and availability report; NTC equipment certification predates it."),
        f("official_launch_price_php", local, "Philippine launch price PHP 8,190 for 4 GB/64 GB", 8190, unit="PHP", status="VERIFIED_SECONDARY",
          note="Historical local launch price reported on 4 March 2022, independently cross-checked by ManilaShaker; not a current offer."),
        f("current_price_php", "tcl20b_yugatech_price_history", "No current dated, orderable Philippine offer verified; the listed PHP 8,190 price is dated 4 March 2022", None,
          status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank; retain PHP 8,190 as a historical launch price only."),
        f("rear_camera_system", sp, "50 MP main + 2 MP depth", "50 MP main + 2 MP depth", key="rearCameraMp"),
        f("main_camera_sensor", sp, "50 MP, f/1.85, 1/2.8-inch sensor, 0.64 μm pixel size", "50 MP; f/1.85"),
        f("front_camera", sp, "8 MP, f/2.0", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", sp, "Rear 1080p at 30 fps; front 1080p at 30 fps", "Rear/front 1080p@30fps", key="video"),
        f("battery_capacity", sp, "4,000 mAh", 4000, key="batteryMah", unit="mAh"),
        f("wired_charging", sp, "Supported charging 18 W; TCL lists a 10 W charger in its specification table", 18, key="chargingW", unit="W",
          note="The device-supported charging rate and listed charger rating are distinct; only supported rate is stored in the numeric field."),
        f("dimensions", sp, "164.7 x 74.68 x 7.99 mm", "164.7 x 74.68 x 7.99", key="dimensions", unit="mm"),
        f("weight", sp, "178 g", 178, key="weightG", unit="g"),
        f("materials", sp, "3D PMMA back cover; frame material not specified", "3D PMMA back cover"),
        f("ingress_protection", sp, "No water/dust ingress rating recorded in the reviewed source", None, status="PENDING_VERIFICATION"),
        f("cellular_bands", sp, "6159K: 4G LTE bands 1/3/5/7/8/20/28/38/40/41; 3G 1/2/5/8; 2G 850/900/1800/1900", "4G LTE; exact bands in sourceValue", key="cellular"),
        f("sim_esim", sp, "6159K dual SIM: 1 Nano-SIM + 1 Nano-SIM or 1 microSD", "Dual Nano-SIM; hybrid second SIM/microSD", key="sim"),
        f("wifi", sp, "802.11 b/g/n, Wi-Fi Direct", "802.11 b/g/n" , key="wifi"),
        f("bluetooth", sp, "Bluetooth 5.0", "Bluetooth 5.0"),
        f("nfc", sp, "6159K model: NFC yes", "Yes", key="nfc"),
        f("gnss", sp, "GPS, A-GPS, BeiDou, Galileo, GLONASS", "GPS; A-GPS; BeiDou; Galileo; GLONASS", key="gnss"),
        f("usb", sp, "USB Type-C 2.0", "USB Type-C 2.0", key="ports"),
        f("audio", sp, "3.5 mm headset jack; one speaker; FM radio listed", "3.5 mm headset jack; speaker; FM radio", key="sound"),
        f("sensors", sp, "Accelerometer, proximity, light sensor, e-compass; rear fingerprint sensor; face unlock", "Accelerometer; proximity; light; e-compass; rear fingerprint; face unlock"),
        f("color_options", "tcl20b_yugatech_ph_launch", "Philippines: Purple, Black; TCL Global: Nebula Purple, Space Grey", None,
          status="CONFLICTING_INFORMATION", note="Names differ across the Philippine launch report and TCL Global product page; preserve the reported names without assuming the two sets map exactly."),
        f("os_support", sp, "No official support end date found in the reviewed exact-model sources", None,
          status="PENDING_VERIFICATION", note="Do not infer a support period from the Android version or brand-wide policy."),
    ]


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row["id"] == DEVICE), None)
    if not device or device.get("workbookRow") != 104 or device.get("brand") != "TCL" or device.get("model") != "20B":
        raise SystemExit("Catalog target guard failed for workbook row 104 TCL 20B")
    manual["records"] = [row for row in manual["records"] if row["deviceId"] != DEVICE]
    config = {
        "deviceId": DEVICE, "configurationId": CONFIG, "brand": "TCL", "model": "TCL 20B",
        "configuration": "4 GB RAM / 64 GB storage", "configurationLabel": "4 GB RAM / 64 GB storage",
        "modelCode": MODEL_CODE,
        "sources": sources(), "fields": fields(),
        "replacementVariants": [{
            "id": CONFIG, "label": "4 GB RAM / 64 GB storage", "modelCode": MODEL_CODE,
            "sku": None, "notes": "TCL's official product specifications identify the 6159K dual-SIM / microSD configuration."
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine authorized-channel availability reported from 4 March 2022",
            "philippineAvailability": "YugaTech reports TCL Mobile Philippines announced the TCL 20B as available in the Philippines from 4 March 2022 through Lazada, Shopee, and authorized TCL dealers. The documented Philippine configuration is 4 GB RAM / 64 GB storage, with a historical launch price of PHP 8,190. Current stock and price are not verified. TCL Global's color names differ from the Philippine launch report's color names, so no color mapping is assumed.",
            "observedAt": OBSERVED,
            "qualityFlag": "NTC TCL 6159K matches TCL 20B; one Philippine 4/64 configuration, local availability and dated historical price documented; current price, exact global release date, color-name mapping, and image reuse rights remain unresolved.",
            "catalogModel": "TCL 20B", "manufacturer": "TCL",
            "productLine": "TCL 20 Series", "modelNumber": MODEL_CODE,
            "philippineReleaseYear": 2022, "philippineDateLabel": "Philippine availability date",
            "researchNotes": "Workbook row 104 TCL 20B matches NTC GEC model 6159K and TCL Global's model-specific spec entries. YugaTech reports a single Philippine 4 GB/64 GB configuration and PHP 8,190 launch price as of 4 March 2022. The price is historical, not current. Manufacturer specifications establish most hardware, including 6159K-specific hybrid SIM/microSD, LTE bands, and NFC. Local and global color names differ; no mapping is assumed. The global announcement/release date is not set because the reviewed sources do not establish an exact primary-source release date. Current price and image reuse rights are not verified. Workbook eligibility remains Pending.",
            "openIssues": [
                {"issue": "Current dated orderable Philippine price was not verified", "action": "Keep current price blank; retain PHP 8,190 as a historical launch value."},
                {"issue": "Exact global release date is not established by the manufacturer source", "action": "Leave the global release date blank."},
                {"issue": "Color naming differs between the PH launch report and TCL Global", "action": "Preserve both source labels and do not map one name onto another."},
                {"issue": "TCL official product imagery is exact-model, but reusable permission is not recorded", "action": "Keep the neutral image placeholder."},
                {"issue": "Workbook eligibility is Pending", "action": "Preserve the existing study-scope status."},
            ],
        },
    }
    add_review(manual, catalog, config)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    manual["reviewedAt"] = OBSERVED
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "TCL Global's exact TCL 20B product page provides a model image asset, but no reusable license or written permission to republish it is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_TCL_PRODUCT, "assetUrl": IMAGE_URL,
        "scope": "Exact TCL 20B 6159K model family; manufacturer product-page image",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for TCL 20B 6159K",
    }
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "TCL", "model_name": "TCL 20B", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC GEC identifies TCL 6159K as TCL 20B; issued 29 September 2021."},
            {"device_id": DEVICE, "source_url": URL_YUGATECH, "result": "Philippine availability, one 4/64 configuration, and PHP 8,190 historical launch price reported 4 March 2022."},
            {"device_id": DEVICE, "source_url": URL_TCL_SPECS, "result": "TCL Global exact-model specifications include 6159K-specific bands, SIM configuration and NFC."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Kimovil's exact TCL 20B Global profile lists one 4 GB/64 GB model; no foreign price promoted to Philippine evidence."},
        ],
        "prices": [{
            "device_id": DEVICE, "amount_php": 8190, "configuration_id": CONFIG,
            "configuration_match": "philippine_6159k_4gb_64gb", "variant_ram_gb": 4, "variant_storage_gb": 64,
            "price_type": "historical_ph_launch_srp", "source_published_at": "2022-03-04",
            "excerpt": "YugaTech reports the TCL 20B 4 GB/64 GB at PHP 8,190 on 4 March 2022; historical launch price, not a current offer.",
            "source_url": URL_YUGATECH, "source_kind": "historical_local_price_candidate",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_price_not_current",
        }],
    }
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "TCL 20B", "workbookRow": 104, "modelCode": MODEL_CODE,
                      "configurations": 1, "sources": len(sources()), "fieldAssessments": len(fields()),
                      "currentPrice": None, "imageRights": "unestablished"}, indent=2))


if __name__ == "__main__":
    main()
