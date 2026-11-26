#!/usr/bin/env python3
"""Review Nokia T10 global configurations, PH availability, specs, price and image rights."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/nokia-t10-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_122fb62b2868fc"
CONFIG_3_32 = f"{DEVICE}-wifi-3gb-32gb-global"
CONFIG_4_64 = f"{DEVICE}-lte-4gb-64gb-ph"

URL_HMD_SPECS = "https://www.hmd.com/en_int/nokia-t-10/specs"
URL_HMD_PRODUCT = "https://www.hmd.com/en_int/nokia-t-10"
URL_HMD_LAUNCH = "https://www.hmd.com/en_int/press/nokia-8210-2660-5710-t10-press-release"
URL_HMD_GUIDE = "https://www.hmd.com/en_int/support/nokia-t10-user-guide/insert-cards?locale=en-USA"
URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_YUGATECH = "https://www.yugatech.com/personal-computing/nokia-t10-t21-tablet-priced-in-the-philippines/"
URL_NOYPI = "https://www.noypigeeks.com/android/nokia-t10-t21-philippines/"
URL_TECHNOBABOY = "https://www.technobaboy.com/2022/12/21/nokia-t10-nokia-t21-budget-tablets-price-philippines/"
URL_GSMARENA = "https://www.gsmarena.com/nokia_t10-11669.php"
URL_GSMARENA_LAUNCH = "https://www.gsmarena.com/nokia_t10_is_an_affordable_8_tablet_with_lte_and_octacore_chipset-news-55014.php"
URL_KIMOVIL = "https://www.kimovil.com/es/donde-comprar-nokia-t10"
URL_NOTEBOOKCHECK = "https://www.notebookcheck.net/Nokia-T10-Android-12-tablet-introduced-for-US-159-with-LTE-connectivity-and-second-screen-support-when-paired-to-a-Windows-PC.634511.0.html"
URL_NOTEBOOKCHECK_REVIEW = "https://www.notebookcheck.com/Test-Nokia-T10-Tablet-Handliches-Pad-mit-Update-Versprechen.682197.0.html"
URL_CLUBIC = "https://www.clubic.com/pro/entreprises/nokia/test-produit-441858-test-nokia-t10-une-tablette-8-pouces-low-cost-sans-pretention-et-sans-surprises.html"
URL_HMD_DATASHEET = "https://jmcomms.com/wp-content/uploads/2022/07/Nokia-T10-data-sheet.pdf"
URL_PTG_NOKIA = "https://www.pinoytechnoguide.com/brand/nokia"
IMAGE_ASSET = "https://cdn.sanity.io/images/nsyec4mj/production/09fa93cd86409cd2b8b807a6c16b3c616ac7e21d-2373x4000.png?auto=format&h=330&q=80&w=195"


def src(sid: str, publisher: str, url: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("nokia_t10_hmd_specs", "HMD Global (manufacturer)", URL_HMD_SPECS,
        "Official Nokia T10 specifications, supported memory choices, and exact-model image",
        "HMD lists the T10 hardware and 3/32 plus 4/64 memory capacities, display, cameras, connectivity, 5,250 mAh battery, 10 W charging, IPX2 rating, Android 12, materials, and supported memory-card size. Its global page is not Philippine SKU evidence."),
    src("nokia_t10_hmd_product", "HMD Global (manufacturer)", URL_HMD_PRODUCT,
        "Official product identity, discontinuation state, and image page",
        "HMD identifies the Nokia T10; the product imagery matches the Ocean Blue Nokia T10. Image reuse permission was not located."),
    src("nokia_t10_hmd_launch", "HMD Global (manufacturer)", URL_HMD_LAUNCH,
        "Global announcement date and update policy",
        "HMD announced Nokia T10 on 12 July 2022 and stated two Android OS upgrades and three years of monthly security updates from global launch.", "2022-07-12"),
    src("nokia_t10_hmd_guide", "HMD Global (manufacturer)", URL_HMD_GUIDE,
        "Regional model code and SIM tray support",
        "HMD's Nokia T10 guide maps TA-1503 to the exact T10 model family and documents a nano-SIM plus memory-card tray for TA-1503. The page does not establish the memory configuration for that code."),
    src("nokia_t10_ntc_gec", "National Telecommunications Commission", URL_NTC,
        "Philippine equipment certification model code",
        "The 2022 NTC GEC lists NOKIA tablet computer TA-1503. The separate HMD T10 guide includes TA-1503 among Nokia T10 codes, supporting the exact model match; the NTC row alone does not state the trade name."),
    src("nokia_t10_yugatech_ph", "YugaTech Philippines", URL_YUGATECH,
        "Philippine launch, 4 GB / 64 GB local configuration, historic price and local spec cross-check",
        "Published 16 December 2022. Reports Philippine launch, PHP 9,690 for the 4 GB / 64 GB configuration, authorized sales channels, and core specifications. Treat the price as historical, not current.", "2022-12-16"),
    src("nokia_t10_noypigeeks_ph", "NoypiGeeks Philippines", URL_NOYPI,
        "Independent Philippine availability, local configuration, and historical price cross-check",
        "Published 16 December 2022. Reports Nokia T10 in the Philippines with 4 GB / 64 GB and PHP 9,690; it does not establish an exact first-sale transaction date.", "2022-12-16"),
    src("nokia_t10_technobaboy_ph", "Technobaboy Philippines", URL_TECHNOBABOY,
        "Local LTE SKU, price, and specification cross-check; discrepancy audit",
        "Published 21 December 2022. Identifies the locally available LTE/voice-calling 4 GB / 64 GB model at PHP 9,690. Its article reports 5,280 mAh and NFC; these differ from the HMD battery specification and Kimovil NFC entry, so the battery uses the manufacturer value with the conflict noted and NFC remains unresolved.", "2022-12-21"),
    src("nokia_t10_gsmarena", "GSMArena", URL_GSMARENA,
        "Exact-model global technical and configuration cross-check",
        "The exact Nokia T10 page lists model configurations, chipset, display, camera, battery, and other hardware. Global configurations are not treated as Philippine sale evidence."),
    src("nokia_t10_gsmarena_launch", "GSMArena", URL_GSMARENA_LAUNCH,
        "Exact-model launch and Wi-Fi / LTE configuration cross-check",
        "Published 12 July 2022. Reports the global Nokia T10 launch, 3/32 GB Wi-Fi model at launch, and additional LTE/4 GB/64 GB choices by market.", "2022-07-12"),
    src("nokia_t10_kimovil", "Kimovil", URL_KIMOVIL,
        "Exact Nokia T10 global configuration and connectivity cross-check",
        "Exact Nokia T10 profile lists 3/32 and 4/64 versions. Kimovil reports NFC absent; its international profile is not Philippine availability evidence."),
    src("nokia_t10_notebookcheck", "Notebookcheck", URL_NOTEBOOKCHECK,
        "Independent exact-model hardware and display cross-check",
        "Exact Nokia T10 launch coverage identifies the device and hardware. Its display-brightness claim differs from other published values; retain the differing measurements without selecting a single normalized value.", "2022-07-12"),
    src("nokia_t10_notebookcheck_review", "Notebookcheck", URL_NOTEBOOKCHECK_REVIEW,
        "Independent exact-model product review and display measurement",
        "Notebookcheck's Nokia T10 review describes its IPS display and reports its measured/claimed brightness context. It is not a Philippine SKU source."),
    src("nokia_t10_clubic_review", "Clubic", URL_CLUBIC,
        "Independent exact-model display measurement cross-check",
        "Clubic reports an average 360 cd/m² and peak 450 cd/m². These figures differ from Notebookcheck's 400 cd/m² value and are not collapsed into one number."),
    src("nokia_t10_hmd_datasheet", "HMD Global (manufacturer datasheet; mirrored copy)", URL_HMD_DATASHEET,
        "Manufacturer launch datasheet cross-check for display brightness and technical details",
        "The HMD-branded Nokia T10 launch datasheet states 360 nits typical and 450 nits boost. The PDF is available through a third-party mirror, not HMD's own host."),
    src("nokia_t10_ptg_archive", "Pinoy Techno Guide Philippines", URL_PTG_NOKIA,
        "Check for exact-model Philippine page availability",
        "The reviewed Nokia brand archive does not list an exact Nokia T10 page. No generic PTG record or other model was substituted as evidence."),
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


def fields(config: str) -> list[dict]:
    local = config == "4/64"
    sid_specs = S["nokia_t10_hmd_specs"]
    sid_local = S["nokia_t10_yugatech_ph"]
    sid_secondary = S["nokia_t10_gsmarena"]
    sid_launch = S["nokia_t10_gsmarena_launch"]
    sid_global = S["nokia_t10_hmd_launch"]
    sid = lambda field_id: sid_specs
    rows = [
        f("model_number", S["nokia_t10_ntc_gec"] if local else S["nokia_t10_hmd_guide"],
          "NTC GEC lists Nokia TA-1503 as a tablet; HMD T10 guide includes TA-1503 among Nokia T10 codes" if local else "HMD T10 guide covers multiple T10 codes, but this global 3/32 configuration is not mapped to one exact code",
          "TA-1503" if local else None, status="VERIFIED" if local else "PENDING_VERIFICATION",
          note="The local model-code match is a two-source identity chain; the code-to-memory pair is not specified on HMD's guide." if local else "Do not assign a regional code to the global 3/32 configuration without an exact source."),
        f("global_release_date", sid_secondary, "Announced 12 July 2022; GSMArena reports initial release on 20 August 2022", "2022-08-20",
          status="VERIFIED_SECONDARY", note="Catalog date uses the reported initial release date; HMD's official announcement occurred earlier on 12 July 2022."),
        f("configuration", S["nokia_t10_yugatech_ph"] if local else S["nokia_t10_gsmarena_launch"],
          "4 GB RAM / 64 GB storage; Philippine launch reports identify LTE with voice calling" if local else "3 GB RAM / 32 GB storage; global Wi-Fi configuration reported at launch",
          "4 GB RAM / 64 GB storage" if local else "3 GB RAM / 32 GB storage",
          status="VERIFIED_SECONDARY" if local else "VERIFIED_SECONDARY"),
        f("philippine_release_date", sid_local,
          "Local reports published 16 December 2022 state the T10 is now in the Philippines; exact first-sale date is not reported" if local else "No Philippine sale evidence found for the global 3 GB / 32 GB configuration",
          "2022-12-16" if local else None, status="VERIFIED_SECONDARY" if local else "PENDING_VERIFICATION",
          note="This is the dated report establishing availability by that date, not a verified first-sale timestamp." if local else "The local 4 GB / 64 GB evidence is not copied to the separate global configuration."),
        f("official_launch_price_php", sid_local,
          "PHP 9,690 reported for Philippine 4 GB / 64 GB LTE model" if local else "No Philippine launch price verified for 3 GB / 32 GB",
          9690 if local else None, unit="PHP", status="VERIFIED_SECONDARY" if local else "PENDING_VERIFICATION",
          note="Historical launch price from local launch coverage; not a current offer." if local else "Do not copy the local LTE SKU price to the global 3/32 configuration."),
        f("current_price_php", S["nokia_t10_hmd_product"], "No current dated, orderable Philippine offer verified; HMD's page shows this model discontinued in the checked market page", None,
          status="PENDING_VERIFICATION", unit="PHP", note="Current Philippine price remains blank. Discontinuation on an HMD regional page does not establish local stock status."),
        f("display_size", sid_specs, "8 inches", 8, key="displayInches", unit="in"),
        f("display_technology", sid_local, "8-inch IPS LCD", "IPS LCD", key="displayType", status="VERIFIED_SECONDARY"),
        f("display_resolution", sid_specs, "800 x 1280 pixels (portrait orientation)", "1280 x 800", key="resolution"),
        f("display_refresh_rate", sid_specs, "Refresh rate not stated in HMD's reviewed specifications", None, status="NOT_DISCLOSED"),
        f("display_brightness", S["nokia_t10_hmd_datasheet"],
          "Published values differ: Notebookcheck reports 400 cd/m²; Clubic reports 360 cd/m² average and 450 cd/m² peak; HMD launch datasheet reports 360 typical / 450 boost",
          None, status="CONFLICTING_INFORMATION", unit="nits",
          note="Different reported metrics/values are retained; no single brightness number is written to the catalog."),
        f("display_protection", sid_specs, "Display cover-glass protection not specified in the reviewed HMD specs", None, status="NOT_DISCLOSED"),
        f("chipset", sid_specs, "Unisoc T606", "Unisoc T606", key="chipset"),
        f("process_node", sid_secondary, "Unisoc T606 reported on 12 nm process", 12, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", sid_secondary, "Octa-core: 2 x Cortex-A75 at 1.6 GHz + 6 x Cortex-A55 at 1.6 GHz", "2x Cortex-A75 1.6 GHz + 6x Cortex-A55 1.6 GHz", status="VERIFIED_SECONDARY"),
        f("gpu", sid_local, "Mali-G57 MP1", "Mali-G57 MP1", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", sid_specs, "Android 12 at launch", "Android 12", key="os"),
        f("os_support", sid_global, "Two Android OS upgrades and three years of monthly security updates from global launch", "2 Android OS upgrades; 3 years security updates", status="VERIFIED"),
        f("ram_capacity", sid_local if local else sid_specs, "4 GB RAM" if local else "3 GB RAM", 4 if local else 3, key="ramGb", unit="GB"),
        f("ram_type", sid_specs, "RAM technology not stated in reviewed HMD specs", None, status="NOT_DISCLOSED"),
        f("storage_capacity", sid_local if local else sid_specs, "64 GB internal storage" if local else "32 GB internal storage", 64 if local else 32, key="storageGb", unit="GB"),
        f("storage_type", sid_specs, "Internal flash storage type not stated in reviewed HMD specs", None, status="NOT_DISCLOSED"),
        f("storage_expansion", S["nokia_t10_hmd_guide"], "microSD support up to 512 GB", "microSD up to 512 GB"),
        f("rear_camera_system", sid_specs, "Single 8 MP autofocus main rear camera with LED flash", "Single 8 MP autofocus main + LED flash"),
        f("main_camera_sensor", sid_specs, "Sensor manufacturer/model not stated", None, status="NOT_DISCLOSED"),
        f("ultrawide_camera", sid_specs, "HMD lists one rear camera module; no ultrawide camera listed", "No ultrawide camera listed", status="NOT_APPLICABLE"),
        f("telephoto_camera", sid_specs, "HMD lists one rear camera module; no telephoto camera listed", "No telephoto camera listed", status="NOT_APPLICABLE"),
        f("front_camera", sid_specs, "2 MP fixed-focus front camera", 2, key="frontCameraMp", unit="MP"),
        f("video_recording", sid_specs, "Video resolution and frame-rate modes not stated on reviewed HMD specifications", None, status="NOT_DISCLOSED"),
        f("battery_capacity", sid_specs, "HMD lists 5,250 mAh; one local article reports 5,280 mAh", 5250, key="batteryMah", unit="mAh",
          note="Catalog retains HMD's manufacturer figure of 5,250 mAh. Technobaboy's local article gives 5,280 mAh; the discrepancy is recorded and may be an article error, not silently ignored."),
        f("battery_technology", sid_specs, "Non-removable battery; chemistry not specified by HMD", "Non-removable; chemistry not recorded"),
        f("wired_charging", sid_specs, "10 W charging", 10, key="chargingW", unit="W"),
        f("wireless_charging", sid_specs, "Wireless charging not listed in reviewed manufacturer specifications", None, status="NOT_DISCLOSED"),
        f("dimensions", sid_specs, "208 x 123.2 x 9 mm", "208 x 123.2 x 9 mm", key="dimensions", unit="mm"),
        f("weight", sid_specs, "375 g", 375, key="weightG", unit="g"),
        f("materials", sid_specs, "Polycarbonate back; frame material not separately specified", "Polycarbonate back; frame not recorded"),
        f("ingress_protection", sid_specs, "IPX2", "IPX2"),
        f("sim_esim", S["nokia_t10_hmd_guide"] if local else sid_launch,
          "Nano-SIM tray for TA-1503; eSIM not stated" if local else "The 3 GB / 32 GB global Wi-Fi configuration is reported as Wi-Fi-only",
          "Nano-SIM; eSIM not recorded" if local else "No cellular SIM on Wi-Fi-only configuration",
          status="VERIFIED" if local else "VERIFIED_SECONDARY"),
        f("cellular_bands", sid_local if local else sid_launch,
          "4G LTE with voice calling; exact Philippine TA-1503 band set not established" if local else "Wi-Fi-only 3 GB / 32 GB configuration; no cellular radio",
          "4G LTE with voice calling; exact Philippine bands not recorded" if local else "Wi-Fi-only", key="cellular",
          status="VERIFIED_SECONDARY" if local else "VERIFIED_SECONDARY",
          note="Do not project HMD's global International/LATAM band tables onto the Philippine TA-1503 without a code-specific local band record." if local else None),
        f("wifi", sid_specs, "802.11 a/b/g/n/ac; dual-band 2.4 / 5 GHz", "Wi-Fi 5 (802.11ac), dual-band", key="wifi"),
        f("bluetooth", sid_specs, "Bluetooth 5.0", "Bluetooth 5.0"),
        f("usb", sid_specs, "USB Type-C 2.0 with OTG", "USB Type-C; USB 2.0; OTG", key="ports"),
        f("nfc", S["nokia_t10_technobaboy_ph"],
          "Technobaboy lists NFC; Kimovil lists NFC absent; HMD does not specify NFC", None,
          status="CONFLICTING_INFORMATION", note="NFC remains blank because the reviewed local secondary source and global profile conflict and HMD's page does not resolve it."),
        f("gnss", sid_specs, "GPS, GLONASS, Galileo; A-GPS is listed for 4G variants", "GPS; GLONASS; Galileo; A-GPS (4G variant)"),
        f("audio", sid_specs, "Two stereo speakers with OZO Playback; 3.5 mm headphone jack", "Stereo speakers; OZO Playback; 3.5 mm jack", key="sound"),
        f("sensors", sid_specs,
          "Accelerometer and ambient-light sensor; proximity sensor is stated for 4G voice variants" if local else "Accelerometer and ambient-light sensor; proximity sensor limited to 4G voice variants",
          "Accelerometer; ambient light; proximity sensor (4G voice variant)" if local else "Accelerometer; ambient light"),
        f("tablet_stylus", sid_specs, "Stylus support or compatibility not stated in reviewed HMD materials", None, status="NOT_DISCLOSED"),
        f("tablet_keyboard", sid_specs, "Keyboard support or compatibility not stated in reviewed HMD materials", None, status="NOT_DISCLOSED"),
        f("tablet_cellular_variant", sid_local if local else sid_launch,
          "Philippine 4 GB / 64 GB model is LTE with voice calling" if local else "Global 3 GB / 32 GB launch configuration reported Wi-Fi-only",
          "4G LTE with voice calling; exact Philippine bands not recorded" if local else "Wi-Fi-only", key="cellular",
          status="VERIFIED_SECONDARY"),
        f("philippine_configuration_availability", sid_local,
          "4 GB / 64 GB LTE with voice calling reported available through Philippine Nokia stores and authorized retailers" if local else "No source reviewed establishes Philippine retail sale of 3 GB / 32 GB",
          "Reported locally available by 16 December 2022" if local else None,
          status="VERIFIED_SECONDARY" if local else "PENDING_VERIFICATION",
          note="Workbook scope remains Pending. The global 3/32 configuration stays visible, with Philippine availability unverified." if not local else "This verifies the local variant at model/configuration level; exact first sale remains unknown."),
    ]
    return rows


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((d for d in catalog if d["id"] == DEVICE), None)
    if not device or device.get("workbookRow") != 119 or device.get("brand") != "Nokia" or device.get("model") != "T10":
        raise SystemExit("Catalog target guard failed for workbook row 119 Nokia T10")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise SystemExit("Expected the original unrecorded configuration placeholder before review")
    if any(row.get("deviceId") == DEVICE for row in manual["records"]):
        raise SystemExit("Nokia T10 already has manual review rows; refusing duplicate replacement")

    variant_defs = [
        {"id": CONFIG_3_32, "label": "3 GB RAM / 32 GB storage (global Wi-Fi configuration; Philippine sale unverified)",
         "modelCode": None, "sku": None,
         "notes": "Exact global T10 configuration; no Philippine sale or price evidence found for this version."},
        {"id": CONFIG_4_64, "label": "4 GB RAM / 64 GB storage; LTE with voice calling (Philippine configuration)",
         "modelCode": "TA-1503", "sku": None,
         "notes": "Philippine launch reports identify this LTE/voice-calling configuration at PHP 9,690 in December 2022; current price is not verified."},
    ]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine launch reporting confirms the Nokia T10 4 GB / 64 GB LTE voice-calling configuration was available through Nokia stores and authorized resellers by 16 December 2022. The separate 3 GB / 32 GB global Wi-Fi configuration has no verified local sale evidence.",
        "philippineAvailability": "NTC lists Nokia tablet code TA-1503; HMD's T10 user guide includes TA-1503 among Nokia T10 codes. Philippine launch reporting identifies the 4 GB / 64 GB LTE voice-calling version at PHP 9,690. This establishes historical local availability for that configuration, not current stock or exact first sale. The global 3 GB / 32 GB Wi-Fi configuration remains Philippine-unverified.",
        "observedAt": OBSERVED,
        "manufacturer": "HMD Global Oy (Nokia brand licensee)",
        "catalogModel": "T10",
        "productLine": "Nokia T-series tablets",
        "modelNumber": "TA-1503",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Reported Philippine availability by 16 December 2022",
        "researchNotes": "Workbook row 119 Nokia T10 matches HMD's exact model family. NTC lists TA-1503 as a Nokia tablet and HMD's T10 user guide maps that code to the Nokia T10. Local press confirms 4 GB / 64 GB LTE with voice calling at PHP 9,690 by December 2022. The separate global 3 GB / 32 GB Wi-Fi configuration is kept as its own visible record variant, without Philippine availability or price claims. A 5,280 mAh local report conflicts with HMD's 5,250 mAh specification; NFC reports conflict; brightness figures vary. Current price and image reuse rights are unresolved. Workbook eligibility remains Pending.",
        "qualityFlag": "Exact T10 model family and TA-1503 code matched; Philippine 4 GB / 64 GB LTE configuration and historical price supported by local reports; 3 GB / 32 GB Philippine sale unverified; battery, NFC and brightness discrepancies documented; current price and image reuse rights unresolved; study scope remains Pending.",
        "openIssues": [
            {"issue": "No exact first authorized sale date is documented", "action": "Retain the reported local availability-by date and year; do not label it the first sale."},
            {"issue": "Philippine sale of global 3 GB / 32 GB configuration is unverified", "action": "Keep it as a separate global configuration with no local price or eligibility claim."},
            {"issue": "Only historical PHP 9,690 price is verified", "action": "Keep current price blank and date the historical 4 GB / 64 GB observation."},
            {"issue": "Battery capacity is 5,250 mAh on HMD specs and 5,280 mAh in one local article", "action": "Use HMD's 5,250 mAh value and preserve the discrepancy in field notes."},
            {"issue": "NFC listings conflict and HMD does not resolve them", "action": "Leave NFC blank."},
            {"issue": "Published display brightness values do not align", "action": "Keep a conflict note and do not publish one normalized brightness value."},
            {"issue": "Exact-model HMD image is visible, but reuse permission is not established", "action": "Retain the neutral placeholder and source metadata."},
            {"issue": "No exact Nokia T10 page was found in the reviewed Pinoy Techno Guide archive or NanoReview", "action": "Use exact HMD, NTC, GSMArena, Kimovil and local Philippine reporting; do not substitute generic pages."},
            {"issue": "Workbook eligibility remains Pending", "action": "Preserve the supplied study-scope status."},
        ],
    }

    target_keys = {(DEVICE, CONFIG_3_32), (DEVICE, CONFIG_4_64)}
    for index, (config_id, config_name, label) in enumerate((
        (CONFIG_3_32, "3/32", variant_defs[0]["label"]),
        (CONFIG_4_64, "4/64", variant_defs[1]["label"]),
    )):
        item = {
            "deviceId": DEVICE, "configurationId": config_id, "brand": "Nokia", "model": "T10",
            "configuration": label, "modelCode": "TA-1503" if config_name == "4/64" else None,
            "sources": SOURCES, "fields": fields(config_name),
            "availabilityEvidence": availability,
        }
        if index == 0:
            item["replacementVariants"] = variant_defs
            item["replaceUnrecordedPlaceholder"] = True
        add_review(manual, catalog, item)
        if index == 0:
            device["variants"] = [{"id": row["id"], "specs": {}} for row in variant_defs]

    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "HMD's product/specification page links an exact Ocean Blue Nokia T10 image, but a reusable license or permission to republish was not found. Keep the neutral placeholder.",
        "sourcePage": URL_HMD_PRODUCT, "assetUrl": IMAGE_ASSET,
        "scope": "Nokia T10 Ocean Blue; model family includes local TA-1503 4 GB / 64 GB LTE configuration",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Nokia T10",
    }
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Nokia", "model_name": "T10", "category": "tablets", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC 2022 GEC lists Nokia TA-1503 as a tablet; HMD T10 guide lists TA-1503 as a Nokia T10 code."},
            {"device_id": DEVICE, "source_url": URL_YUGATECH, "result": "Philippine report identifies 4 GB / 64 GB T10 at PHP 9,690 in December 2022."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA_LAUNCH, "result": "Exact global 3 GB / 32 GB Wi-Fi and 4G variants; global sales and local sale are kept distinct."},
            {"device_id": DEVICE, "source_url": URL_HMD_SPECS, "result": "Manufacturer specifications cover product hardware, two RAM and storage capacities, Wi-Fi, optional 4G, battery and build."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Exact global T10 profile confirms 3/32 and 4/64; NFC no claim conflicts with a local report and remains unresolved."},
            {"device_id": DEVICE, "source_url": URL_PTG_NOKIA, "result": "Reviewed PTG Nokia archive; no exact T10 page found."},
        ],
        "prices": [{
            "device_id": DEVICE, "amount_php": 9690, "configuration_id": CONFIG_4_64,
            "configuration_match": "philippine_TA-1503_LTE_4gb_64gb", "variant_ram_gb": 4, "variant_storage_gb": 64,
            "price_type": "historical_ph_launch_price", "source_published_at": "2022-12-16",
            "excerpt": "YugaTech and NoypiGeeks report the Nokia T10 4 GB / 64 GB at PHP 9,690 in Philippine launch coverage dated 16 December 2022; historical price, not a current offer.",
            "source_url": URL_YUGATECH, "source_kind": "historical_local_price_candidate",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_price_not_current",
        }],
    }
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "Nokia T10", "workbookRow": 119, "modelCode": "TA-1503",
                      "configurations": ["3 GB / 32 GB global Wi-Fi; local sale unverified", "4 GB / 64 GB LTE voice local SKU"],
                      "sources": len(SOURCES), "fieldAssessmentsPerConfiguration": [len(fields("3/32")), len(fields("4/64"))],
                      "historicalPricePhp": 9690, "currentPrice": None, "imageRights": "unestablished"}, indent=2))


if __name__ == "__main__":
    main()
