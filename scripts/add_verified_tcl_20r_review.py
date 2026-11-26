#!/usr/bin/env python3
"""Review TCL 20 R 5G model codes, Philippine configurations and source-backed fields."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/tcl-20-r-5g-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_af0706eb4c718f"
CONFIG_64 = f"{DEVICE}-t767h-4gb-64gb-ph"
CONFIG_128 = f"{DEVICE}-t767h1-4gb-128gb-ph"

URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_TCL_SPECS = "https://www.tcl.com/es/es/mobile/tcl-20r5g/specifications"
URL_TCL_PH_SUPPORT = "https://www.tcl.com/ph/en/support-mobile/model/tcl-20-r-5g"
URL_IMAGE = "https://aws-obg-image-lb-5.tcl.com/content/dam/brandsite/region/global/products/smartphones/category-display/tcl20r5g-pc.png?t=1645758481411&w=800"
URL_TCL_CZ_SPECS = "https://www.tcl.com/cz/cs/mobile/tcl-20r5g/specifications"
URL_YUGATECH = "https://www.yugatech.com/mobile/tcl-20-r-5g-price-philippines/"
URL_YUGATECH_PRICES = "https://www.yugatech.com/tcl-phone-price-list-philippines"
URL_UNBOX = "https://unbox.ph/gadget/tcl-20-r-5g-now-in-the-philippines-with-php-12k-price-tag/"
URL_MANILASHAKER = "https://manilashaker.com/tcl-20-r-5g-now-available-in-the-philippines/"
URL_NOYPIGEEKS = "https://www.noypigeeks.com/android/tcl-20-r-5g/"
URL_GIZGUIDE = "https://www.gizguide.com/2022/04/tcl-20-r-5g-ph-price-specs-official.html"
URL_GSMARENA = "https://www.gsmarena.com/tcl_20_r_is_official_with_5g_and_low_price-news-50844.php"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-tcl-20r-5g-4gb-128gb"


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
        src("tcl20r_ntc_gec", "National Telecommunications Commission", URL_NTC,
            "Philippine equipment identity check for the registered configuration",
            "The NTC 2022 GEC table lists TCL model T767H1 with marketing name TCL 20R 5G. The NTC row establishes the exact registered model and name; TCL's manufacturer specifications map T767H1 to 4 GB / 128 GB."),
        src("tcl20r_tcl_specs_es", "TCL Spain (manufacturer)", URL_TCL_SPECS,
            "Manufacturer specifications and exact T767H / T767H1 capacity mapping",
            "The product specification page maps T767H to 4 GB / 64 GB and T767H1 to 4 GB / 128 GB; the manufacturer describes the T767H 64 GB version for EU/APAC and T767H1 128 GB for EU. Shared hardware values are recorded from this page, while market-specific availability is supported separately."),
        src("tcl20r_tcl_ph_support", "TCL Philippines (manufacturer)", URL_TCL_PH_SUPPORT,
            "Exact model support identity and image source page",
            "TCL Philippines has a dedicated TCL 20 R 5G support page. Its product image asset matches the device family; reuse permission was not established, so the public catalog keeps its neutral placeholder."),
        src("tcl20r_tcl_cz_specs", "TCL Czech Republic (manufacturer)", URL_TCL_CZ_SPECS,
            "Independent regional manufacturer cross-check and conflict documentation",
            "The manufacturer page repeats the T767H / T767H1 memory mapping and shared technical specifications. It reports Bluetooth 5.2, while the TCL Spain page reports 5.1; this conflict is withheld from the catalog."),
        src("tcl20r_yugatech_ph", "YugaTech Philippines", URL_YUGATECH,
            "Philippine reported availability, 4 GB memory options, technical cross-check and launch price range",
            "Published 2 April 2022. Reports arrival at authorized TCL dealer partners, both 4 GB / 64 GB and 4 GB / 128 GB configurations, and a starting price of PHP 11,990. It does not price the 128 GB configuration separately.", "2022-04-02"),
        src("tcl20r_unbox_ph", "Unbox Philippines", URL_UNBOX,
            "Philippine 4 GB / 64 GB configuration and historical launch price cross-check",
            "Published 4 April 2022. Reports 4 GB / 64 GB and PHP 11,990 for the Philippine offering at selected authorized dealer partners; this is a dated historical launch price, not a current offer.", "2022-04-04"),
        src("tcl20r_manilashaker_ph", "ManilaShaker Philippines", URL_MANILASHAKER,
            "Independent Philippine availability and configuration cross-check",
            "Published 2 April 2022. Reports authorized dealer availability and 4 GB RAM with 64 GB / 128 GB storage options. No exact first transaction date or current offer is established.", "2022-04-02"),
        src("tcl20r_noypigeeks_ph", "NoypiGeeks Philippines", URL_NOYPIGEEKS,
            "Independent local configuration cross-check and conflicting charger claim",
            "Published 4 April 2022. Reports 4 GB / 64 GB and 4 GB / 128 GB configurations. Its article says a 15 W charger is included, in contrast to the manufacturer's listed 5 V / 2 A standard charger and other reports of 10 W; charging remains unresolved.", "2022-04-04"),
        src("tcl20r_gizguide_ph", "GIZGUIDE Philippines", URL_GIZGUIDE,
            "Conflicting local configuration claim and local availability cross-check",
            "Published 3 April 2022. Reports local authorized-channel availability but states 4 GB / 6 GB RAM and 64 GB / 128 GB storage, then details a 6 GB / 128 GB configuration. This conflicts with TCL's two model-code-specific 4 GB configurations and other Philippine reports; no unverified 6 GB variant is added.", "2022-04-03"),
        src("tcl20r_gsmarena", "GSMArena", URL_GSMARENA,
            "Exact-model global announcement, initial configuration and technical reference",
            "Published 7 September 2021. Identifies TCL 20 R as a European-market device and reports 4 GB / 64 GB, a 4,500 mAh battery, and 10 W charging; it is not used as Philippine availability or pricing evidence.", "2021-09-07"),
        src("tcl20r_kimovil", "Kimovil", URL_KIMOVIL,
            "Independent exact-model configuration and global release-month cross-check",
            "The exact TCL 20R 5G global profile lists 4 GB / 64 GB and 4 GB / 128 GB configurations and a September 2021 release month. International prices are not used as Philippine price evidence."),
        src("tcl20r_yugatech_price_history", "YugaTech Philippines", URL_YUGATECH_PRICES,
            "Dated historical Philippine starting-price listing",
            "The price list retains the TCL 20 R 5G starting price of PHP 11,990 with a reported date of 2 April 2022. This does not establish a current orderable price.", "2022-04-02"),
    ]


def fields(model_code: str, ram: int, storage: int) -> list[dict]:
    config = f"{ram} GB RAM / {storage} GB storage"
    model_field_note = (
        "TCL maps T767H1 to 4 GB / 128 GB; this exact code is also listed as TCL 20R 5G by the Philippine NTC GEC."
        if model_code == "T767H1" else
        "TCL maps T767H to 4 GB / 64 GB and identifies this memory option for EU/APAC. Philippine sources report this local configuration, though the reviewed NTC GEC row lists T767H1 only."
    )
    p = "tcl20r_tcl_specs_es"
    local = "tcl20r_yugatech_ph"
    data = [
        f("model_number", "tcl20r_ntc_gec" if model_code == "T767H1" else p,
          model_code, model_code, note=model_field_note),
        f("configuration", p, f"{model_code}: {config}", config,
          status="VERIFIED_SECONDARY", note="The manufacturer maps the exact model code to this capacity; Philippine technology publishers independently report both 4 GB storage options as locally available."),
        f("global_release_date", "tcl20r_gsmarena", "European announcement 7 September 2021; first select-market availability during September 2021", "2021-09",
          status="VERIFIED_SECONDARY", note="Month precision is retained because rollout timing differed by market."),
        f("philippine_release_date", local, "Philippine authorized-dealer availability reported 2 April 2022", "2022-04-02",
          status="VERIFIED_SECONDARY", note="This is the dated local availability report, not a confirmed first-sale transaction date."),
        f("official_launch_price_php", "tcl20r_unbox_ph" if storage == 64 else local,
          "PHP 11,990 for the 4 GB / 64 GB model" if storage == 64 else "Starting price PHP 11,990; 4 GB / 128 GB price not separately reported",
          11990 if storage == 64 else None, unit="PHP",
          status="VERIFIED_SECONDARY" if storage == 64 else "PENDING_VERIFICATION",
          note="Unbox ties PHP 11,990 to the locally reported 4 GB / 64 GB configuration. The 4 GB / 128 GB price is not inferred from a starting price."),
        f("current_price_php", "tcl20r_yugatech_price_history", "No current dated, orderable Philippine offer verified; PHP 11,990 is a 2022 historical starting/launch price", None,
          status="PENDING_VERIFICATION", unit="PHP", note="Keep the public current price blank; preserve the dated PHP 11,990 historical price in the price snapshot."),
        f("display_size", p, "6.52-inch V-notch display", 6.52, key="displayInches", unit="in"),
        f("display_technology", local, "6.52-inch HD+ IPS LCD", "IPS LCD", key="displayType", status="VERIFIED_SECONDARY"),
        f("display_resolution", p, "HD+ 720 x 1600", "720 x 1600", key="resolution"),
        f("display_refresh_rate", p, "90 Hz", 90, key="refreshHz", unit="Hz"),
        f("display_brightness", p, "500 nits peak", 500, key="brightnessNits", unit="nits"),
        f("display_protection", p, "2.5D front glass; no separate scratch-resistance rating listed", "2.5D front glass"),
        f("chipset", p, "MediaTek Dimensity 700 (MT6833)", "MediaTek Dimensity 700", key="chipset"),
        f("process_node", p, "7 nm", 7, unit="nm"),
        f("cpu", p, "2 x Cortex-A76 at 2.2 GHz + 6 x Cortex-A55 at 2.0 GHz", "2x Cortex-A76 2.2 GHz + 6x Cortex-A55 2.0 GHz", key="cpu"),
        f("gpu", p, "ARM Mali-G57 MC2", "Mali-G57 MC2", key="gpu"),
        f("operating_system", p, "Android 11 with TCL UI 3.0", "Android 11 / TCL UI 3.0", key="os"),
        f("os_support", "tcl20r_gsmarena", "TCL promised one major Android update to Android 12 and three years of quarterly security updates; TCL spec page lists security updates through August 2023", "Android 12 major update; quarterly security updates for three years (listed through August 2023)",
          status="VERIFIED_SECONDARY", note="GSMArena reports the promise from TCL at launch; TCL's regional specification page gives the security-update end month. This is a historical policy, not a statement that updates continue today."),
        f("ram_capacity", p, "4 GB LPDDR4x", 4, key="ramGb", unit="GB"),
        f("ram_type", p, "LPDDR4x", "LPDDR4x"),
        f("storage_capacity", p, f"{storage} GB ROM", storage, key="storageGb", unit="GB"),
        f("storage_type", p, "UFS 2.1", "UFS 2.1", key="storageType"),
        f("storage_expansion", p, "microSD card support up to 1 TB; hybrid SIM/microSD slot on dual-SIM model", "microSD up to 1 TB; hybrid slot"),
        f("rear_camera_system", p, "13 MP main + 2 MP macro + 2 MP depth", "13 MP main + 2 MP macro + 2 MP depth", key="rearCameraMp"),
        f("main_camera_sensor", p, "13 MP autofocus, f/2.2, 1/3-inch sensor, 1.12 μm pixel size", "13 MP; f/2.2; 1/3-inch sensor"),
        f("ultrawide_camera", p, "No ultrawide camera listed in the manufacturer triple-camera system", None, status="NOT_APPLICABLE"),
        f("telephoto_camera", p, "No telephoto camera listed in the manufacturer triple-camera system", None, status="NOT_APPLICABLE"),
        f("front_camera", p, "8 MP, f/2.0", 8, key="frontCameraMp", unit="MP"),
        f("video_recording", p, "Rear and front camera: 1080p at 30 fps", "1080p@30fps front/rear", key="video"),
        f("battery_capacity", p, "4,500 mAh typical", 4500, key="batteryMah", unit="mAh"),
        f("battery_technology", p, "Battery chemistry not listed", None, status="PENDING_VERIFICATION"),
        f("wired_charging", "tcl20r_noypigeeks_ph", "TCL lists a standard 5 V / 2 A charger (10 W); GSMArena and other local reports state 10 W; NoypiGeeks says a 15 W charger is included", None,
          status="CONFLICTING_INFORMATION", unit="W", note="The source record does not distinguish device input capability from bundled-adapter rating consistently. Keep numeric charging power unavailable."),
        f("wireless_charging", p, "Wireless charging is not listed in reviewed TCL specifications", None, status="PENDING_VERIFICATION"),
        f("dimensions", p, "164.3 x 75 x 8.99 mm", "164.3 x 75 x 8.99", key="dimensions", unit="mm",
          note="TCL manufacturer value. GIZGUIDE reports a 75.8 mm width; other local reporting and TCL list 75 mm, so the source discrepancy remains noted in the device issues."),
        f("weight", p, "186 g", 186, key="weightG", unit="g"),
        f("materials", p, "2.5D front glass; matte 2.5D PMMA/PC back", "2.5D front glass; matte PMMA/PC back"),
        f("ingress_protection", p, "No IP rating listed in reviewed TCL product specifications", None, status="PENDING_VERIFICATION"),
        f("sim_esim", local, "Dual-SIM; manufacturer describes hybrid second Nano-SIM or microSD slot for dual-SIM model", "Dual Nano-SIM; hybrid second SIM/microSD", key="sim", status="VERIFIED_SECONDARY"),
        f("cellular_bands", p, "2G GSM 850/900/1800/1900; 3G UMTS B1/2/4/5/8; 4G B1/3/5/7/8/20/26/28/32/38/40/41; 5G n1/n3/n5/n7/n8/n28/n40/n78", "2G/3G/4G/5G; exact bands in sourceValue", key="cellular"),
        f("wifi", p, "802.11 a/b/g/n/ac, 2.4 GHz and 5 GHz; Wi-Fi Direct", "802.11 a/b/g/n/ac dual-band", key="wifi"),
        f("bluetooth", "tcl20r_tcl_cz_specs", "TCL Spain and local sources report Bluetooth 5.1; TCL Czech specification page reports Bluetooth 5.2", None,
          status="CONFLICTING_INFORMATION", note="Conflicting manufacturer regional pages; withheld from catalog pending exact T767H1 regional clarification."),
        f("usb", p, "USB Type-C 2.0", "USB Type-C 2.0", key="ports"),
        f("nfc", "tcl20r_tcl_cz_specs", "TCL specification pages describe NFC as optional; Philippine launch reports list NFC", None,
          status="CONFLICTING_INFORMATION", note="Availability may be regional or configuration-dependent; no reviewed source ties NFC to each local model code."),
        f("gnss", p, "GPS, A-GPS, BeiDou, Galileo, GLONASS", "GPS; A-GPS; BeiDou; Galileo; GLONASS", key="gnss"),
        f("audio", p, "Single speaker and 3.5 mm headset jack", "Single speaker; 3.5 mm audio jack", key="sound"),
        f("sensors", p, "Accelerometer, e-compass, proximity sensor, light sensor; rear fingerprint sensor; face unlock", "Accelerometer; e-compass; proximity; light; rear fingerprint; face unlock"),
        f("color_options", local, "Lazurite Blue and Granite Grey", "Lazurite Blue; Granite Grey", status="VERIFIED_SECONDARY"),
        f("reported_configuration_conflict", "tcl20r_gizguide_ph", "One local article reports 4 GB / 6 GB RAM and 64 GB / 128 GB storage, with a detailed 6 GB / 128 GB configuration", None,
          status="CONFLICTING_INFORMATION", note="Not added as a configuration: TCL model-code specifications and multiple other Philippine reports identify only 4 GB / 64 GB and 4 GB / 128 GB. The local 6 GB report is preserved for follow-up."),
    ]
    if storage == 64:
        data.extend([
            f("model_number_crosscheck", "tcl20r_yugatech_ph", "Philippine reports identify 4 GB / 64 GB as a local configuration; the matching manufacturer code is T767H", "T767H", status="VERIFIED_SECONDARY",
              note="Manufacturer regional specifications map T767H to 4 GB / 64 GB; YugaTech and ManilaShaker separately report this capacity for the Philippine model family. NTC's reviewed GEC row lists only T767H1."),
        ])
    return data


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row["id"] == DEVICE), None)
    if not device or device.get("workbookRow") != 105 or device.get("brand") != "TCL" or device.get("model") != "20 R 5G":
        raise SystemExit("Catalog target guard failed for workbook row 105 TCL 20 R 5G")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise SystemExit("Expected the original unrecorded configuration placeholder before review")

    manual["records"] = [row for row in manual["records"] if row["deviceId"] != DEVICE]
    variant_specs = [
        {"id": CONFIG_64, "label": "4 GB RAM / 64 GB storage", "modelCode": "T767H",
         "sku": None, "notes": "TCL manufacturer model-code mapping; Philippine local reporting confirms the configuration, while NTC GEC specifically lists T767H1."},
        {"id": CONFIG_128, "label": "4 GB RAM / 128 GB storage", "modelCode": "T767H1",
         "sku": None, "notes": "TCL manufacturer model-code mapping and exact Philippine NTC GEC registration for TCL 20R 5G."},
    ]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine authorized-dealer availability reported from 2 April 2022; two 4 GB configurations are reported locally.",
        "philippineAvailability": "YugaTech and ManilaShaker reported the TCL 20 R 5G available through selected authorized TCL dealer partners on 2 April 2022; they report 4 GB / 64 GB and 4 GB / 128 GB. The NTC GEC lists T767H1 as TCL 20R 5G, and TCL maps T767H1 to 4 GB / 128 GB. Current stock and price are not verified. A separate 6 GB / 128 GB press claim conflicts with the manufacturer model-code configurations and is retained as unresolved, not added as a variant.",
        "observedAt": OBSERVED,
        "qualityFlag": "Exact TCL model family matched; T767H1 / 4-128 is NTC-listed and T767H / 4-64 is manufacturer-mapped with local publisher support. Current prices, exact first-sale day, Bluetooth/NFC/charging conflicts and reuse rights remain unresolved. Workbook scope remains Pending.",
        "catalogModel": "TCL 20 R 5G", "manufacturer": "TCL", "productLine": "TCL 20 Series",
        "philippineReleaseYear": 2022, "philippineDateLabel": "First reported Philippine authorized availability",
        "researchNotes": "Workbook row 105 was matched to TCL 20 R 5G using the NTC GEC entry T767H1 and TCL's exact model-code capacity table. TCL maps T767H to 4 GB / 64 GB and T767H1 to 4 GB / 128 GB; YugaTech, ManilaShaker and NoypiGeeks report both configurations locally. A GIZGUIDE report says 6 GB / 128 GB and is retained as a conflict without creating a third variant. PHP 11,990 is historical and tied to the 4 GB / 64 GB launch offering; current price remains blank. Bluetooth, NFC and charging details conflict across manufacturer/regional or local sources. Image reuse permission is not established. Eligibility remains Pending.",
        "openIssues": [
            {"issue": "A local GIZGUIDE report claims a 6 GB / 128 GB configuration, while manufacturer model-code specifications and other Philippine reports identify 4 GB configurations", "action": "Keep only the source-backed 4 GB / 64 GB T767H and 4 GB / 128 GB T767H1 variants; retain the 6 GB claim for further model-code/NTC verification."},
            {"issue": "Current dated, orderable Philippine prices were not verified", "action": "Keep current prices blank; retain PHP 11,990 only as historical launch pricing for the 4 GB / 64 GB configuration."},
            {"issue": "Bluetooth 5.1 and 5.2 differ across TCL regional specifications", "action": "Show no Bluetooth version until the local T767H1 specification is resolved."},
            {"issue": "NFC is called optional by TCL while Philippine articles list it without tying it to model codes", "action": "Do not assert NFC for either local configuration until model-specific confirmation is found."},
            {"issue": "Charging source reports conflict between 10 W and a bundled 15 W charger", "action": "Keep numeric charging wattage blank pending exact device input/adapter evidence."},
            {"issue": "GIZGUIDE reports device width 75.8 mm, while TCL and other local reports list 75 mm", "action": "Retain the manufacturer 75 mm value and preserve the discrepancy in source notes."},
            {"issue": "Exact first Philippine sale transaction date is not recorded", "action": "Use 2 April 2022 only as the dated report of authorized-channel availability."},
            {"issue": "TCL product image asset is exact-model but reuse terms are not established", "action": "Keep the neutral catalog placeholder and preserve the official image source URL."},
            {"issue": "Workbook eligibility is Pending", "action": "Preserve the existing study-scope status."},
        ],
    }
    shared_sources = sources()
    for index, (config_id, code, storage) in enumerate(((CONFIG_64, "T767H", 64), (CONFIG_128, "T767H1", 128))):
        item = {
            "deviceId": DEVICE, "configurationId": config_id, "brand": "TCL", "model": "TCL 20 R 5G",
            "configuration": f"4 GB RAM / {storage} GB storage",
            "modelCode": code, "sources": shared_sources, "fields": fields(code, 4, storage),
            "availabilityEvidence": availability,
        }
        if index == 0:
            item["replacementVariants"] = variant_specs
            item["replaceUnrecordedPlaceholder"] = True
        add_review(manual, catalog, item)
        if index == 0:
            # The data builder sees both replacement variants from the first
            # review row; mirror that shape here for the second review helper call.
            device["variants"] = [{"id": row["id"], "specs": {}} for row in variant_specs]

    deduplicate_target_reviews(manual, {(DEVICE, CONFIG_64), (DEVICE, CONFIG_128)})
    manual["reviewedAt"] = OBSERVED
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "TCL Philippines provides an exact TCL 20 R 5G support-page image asset, but a reusable license or permission to republish was not found. Keep the neutral placeholder.",
        "sourcePage": URL_TCL_PH_SUPPORT, "assetUrl": URL_IMAGE,
        "scope": "TCL 20 R 5G model family; official TCL Philippines product image",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for TCL 20 R 5G",
    }
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "TCL", "model_name": "TCL 20 R 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC GEC lists T767H1 as TCL 20R 5G; manufacturer maps it to 4 GB / 128 GB."},
            {"device_id": DEVICE, "source_url": URL_TCL_SPECS, "result": "TCL maps T767H to 4 GB / 64 GB and T767H1 to 4 GB / 128 GB."},
            {"device_id": DEVICE, "source_url": URL_YUGATECH, "result": "Philippine authorized-dealer availability, 4 GB / 64 GB and 4 GB / 128 GB options, dated 2 April 2022; starts at PHP 11,990."},
            {"device_id": DEVICE, "source_url": URL_GIZGUIDE, "result": "Conflicting local claim of 6 GB / 128 GB retained; no third configuration added."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Exact global profile cross-checks 4 GB / 64 GB and 4 GB / 128 GB and September 2021 release month; no foreign price used locally."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "Exact model announcement dated 7 September 2021; reports European availability and 4 GB / 64 GB baseline."},
        ],
        "prices": [{
            "device_id": DEVICE, "amount_php": 11990, "configuration_id": CONFIG_64,
            "configuration_match": "philippine_t767h_4gb_64gb", "variant_ram_gb": 4, "variant_storage_gb": 64,
            "price_type": "historical_ph_launch_price", "source_published_at": "2022-04-04",
            "excerpt": "Unbox reports the TCL 20 R 5G at PHP 11,990 in the Philippines alongside its 4 GB RAM / 64 GB storage configuration; historical 2022 launch price, not a current offer.",
            "source_url": URL_UNBOX, "source_kind": "historical_local_price_candidate",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_price_not_current",
        }],
    }
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "TCL 20 R 5G", "workbookRow": 105,
                      "configurations": ["T767H 4/64", "T767H1 4/128"],
                      "sources": len(shared_sources), "fieldAssessmentsPerConfiguration": len(fields("T767H", 4, 64)),
                      "historicalLaunchPricePhp": 11990, "currentPrice": None,
                      "unresolvedSixGbClaim": True, "imageRights": "unestablished"}, indent=2))


if __name__ == "__main__":
    main()
