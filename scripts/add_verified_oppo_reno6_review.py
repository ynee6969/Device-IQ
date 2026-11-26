#!/usr/bin/env python3
"""Add a source-backed Philippine review for the OPPO Reno6 workbook row."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/oppo-reno6-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_97f548edfe54b5"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_OPPO_PH = "https://www.oppo.com/ph/newsroom/press/oppo-reno6-launch/"
URL_OPPO_SPECS = "https://www.oppo.com/en/smartphones/series-reno/reno6-5g/specs/"
URL_OPPO_PRODUCT = "https://www.oppo.com/en/smartphones/series-reno/reno6-5g/"
URL_NTC = "https://www.ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/GEC-2009-2021-Updated-.pdf"
URL_YUGA_LAUNCH = "https://www.yugatech.com/mobile/oppo-reno6-6z-5g-specs-price-philippines/"
URL_YUGA_HANDS_ON = "https://www.yugatech.com/mobile/oppo-reno6-5g-specs-price-hands-on-philippines/"
URL_MANILASHAKER = "https://manilashaker.com/oppo-reno6-5g-now-officially-available-in-the-philippines/"
URL_MEDIATEK = "https://www.mediatek.com/products/laptops-and-tablets/tablets/mediatek-dimensity-900"
URL_GSMARENA = "https://www.gsmarena.com/oppo_reno6_5g-10932.php"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-oppo-reno-6-in"
URL_NANOREVIEW = "https://nanoreview.net/en/soc/mediatek-dimensity-900"
URL_LAHATDITO = "https://www.lahatdito.com.ph/product/Oppo-Reno6-Smartphone--5G-8128GB-x2lQ7"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None, source_kind: str | None = None) -> dict:
    result = {"id": sid, "publisher": publisher, "url": url,
             "publicationDate": publication_date, "accessDate": OBSERVED,
             "purpose": purpose, "note": note}
    if source_kind:
        result["sourceKind"] = source_kind
    return result


SOURCES = [
    source("reno6_oppo_ph_launch", "OPPO Philippines", URL_OPPO_PH,
           "Official Philippine launch, configuration, color, availability, and launch price evidence",
           "OPPO's local announcement separates Reno6 5G from Reno6 Z 5G, states the 5G model's PHP 26,999 price and 8 GB / 128 GB configuration, and says it would be available from August 28, 2021. It names Aurora and Stellar Black as colors. The release also identifies the Dimensity 900, 4,300 mAh battery, and 65 W SuperVOOC 2.0.",
           "2021-08-06"),
    source("reno6_oppo_global_specs", "OPPO Global", URL_OPPO_SPECS,
           "Exact model-code and manufacturer specifications for Reno6 5G CPH2251",
           "OPPO identifies this specification page as Reno6 5G (CPH2251), with 8 GB / 128 GB, LPDDR4X, display, camera/video, chipset, battery, connectivity, OS, sensors, and dimensions. It says external memory is not supported. Its listed image assets are reference images; no reuse license is stated."),
    source("reno6_oppo_product", "OPPO Global", URL_OPPO_PRODUCT,
           "Official exact-model product imagery reference and product overview",
           "The product page is for OPPO Reno6 5G. It depicts the exact model, but its product imagery is not accompanied by a reusable image license or permission statement."),
    source("reno6_ntc_gec", "National Telecommunications Commission (NTC), Philippines", URL_NTC,
           "Philippine equipment-conformity record for model CPH2251",
           "The NTC GEC table lists OPPO CPH2251 with marketing name OPPO Reno6 5G; the grant was issued July 6, 2021 to Emerald Wireless Tech Inc. The same table separately lists CPH2237 as Reno6 Z 5G, which is not merged into this record."),
    source("reno6_yugatech_launch", "YugaTech Philippines", URL_YUGA_LAUNCH,
           "Contemporaneous Philippine launch configuration, price, availability, and spec cross-check",
           "The Philippine launch report identifies Reno6 5G (8 GB / 128 GB) at PHP 26,999, with availability scheduled for August 28, 2021. It distinguishes the Reno6 Z 5G and gives local device details. It does not establish a present-day price." ,
           "2021-08-06"),
    source("reno6_yugatech_hands_on", "YugaTech Philippines", URL_YUGA_HANDS_ON,
           "Independent exact-model technical cross-check and storage-expansion discrepancy",
           "The hands-on identifies the Reno6 5G and lists core specifications. In one passage it describes a tray for two SIMs and microSD, conflicting with OPPO's exact CPH2251 specification that says external memory is not supported. The conflict is retained. Its pre-launch global configuration list is not treated as evidence of additional Philippine configurations.",
           "2021-07-27"),
    source("reno6_manilashaker_launch", "ManilaShaker Philippines", URL_MANILASHAKER,
           "Independent local availability and technical cross-check",
           "Published August 27, 2021, it reports Philippine availability beginning August 28 and PHP 26,999 for Reno6 5G. It corroborates 8 GB / 128 GB and several specifications. Its text says Mali-G78 MC4; OPPO's model-specific page and MediaTek's chipset documentation identify Mali-G68 MC4, so the latter is retained and the secondary typo is documented.",
           "2021-08-27"),
    source("reno6_mediatek_dimensity900", "MediaTek", URL_MEDIATEK,
           "Primary Dimensity 900 CPU, GPU, process-node, and platform evidence",
           "MediaTek specifies TSMC 6 nm, two Cortex-A78 cores up to 2.4 GHz, six Cortex-A55 cores up to 2 GHz, and Mali-G68 MC4. These are chipset-family specifications; OPPO identifies Dimensity 900 in CPH2251."),
    source("reno6_gsmarena", "GSMArena", URL_GSMARENA,
           "Secondary exact-model release-date and specification cross-check",
           "GSMArena's exact Reno6 5G record (phone ID 10932) search result reports release on June 11, 2021. A direct page fetch returned HTTP 402 during review, so no additional values were extracted from the page."),
    source("reno6_kimovil", "Kimovil", URL_KIMOVIL,
           "Secondary model alias, configuration, and release-month cross-check",
           "Kimovil lists CPH2251 / Reno6 5G as an alias and gives a May 2021 release month, while its configuration section separates China and International entries. Because that month does not match GSMArena's June 11 release date and the page groups region variants, it is not used to assign one exact global release date."),
    source("reno6_nanoreview_dimensity900", "NanoReview", URL_NANOREVIEW,
           "Secondary Dimensity 900 architecture cross-check",
           "NanoReview independently lists the chipset's 6 nm process and 2x Cortex-A78 / 6x Cortex-A55 layout. Benchmark scores and device-performance ratings are not copied into DeviceIQ."),
    source("reno6_lahatdito_offer", "LahatDito Philippines marketplace / Gadget Shop", URL_LAHATDITO,
           "Exact title/configuration current-price candidate review",
           "The marketplace page title says Reno6 5G 8+128 GB and displays PHP 32,518, in-stock text, and 300 available units. The search/browser snapshot was last crawled about 10 months before this review; seller authorization, current orderability, and item condition were not independently confirmed. The amount is retained as a stale candidate, not a current catalog price.",
           source_kind="marketplace_candidate"),
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
    match = "Philippine OPPO Reno6 5G (CPH2251), 8 GB RAM / 128 GB storage; Aurora or Stellar Black"
    out: list[dict] = []

    def add(fid, sid, value, normalized, *, status="VERIFIED", key=None,
            catalog_value=None, unit=None, note, price_type=None):
        out.append(field(fid, sid, value, normalized, status=status, key=key,
                         catalog_value=catalog_value, unit=unit, note=note,
                         configuration_match=match, price_type=price_type))

    add("model_number", "reno6_ntc_gec", "NTC lists OPPO CPH2251 as OPPO Reno6 5G; OPPO's specification page labels Reno6 5G as CPH2251", "CPH2251", note="Exact product identity is corroborated by the Philippine NTC entry and the manufacturer's model-specific specification page. NTC separately lists CPH2237 as Reno6 Z 5G.")
    add("global_release_date", "reno6_gsmarena", "GSMArena's CPH2251 Reno6 5G record reports release June 11, 2021; Kimovil groups the CPH2251/international entry under a May 2021 release month; OPPO's reviewed product pages give no global date", None, status="CONFLICTING_INFORMATION", note="The exact day and month-level secondary dates differ, and the Kimovil profile groups regional configurations. Leave one global release date unset; Philippine availability is separately documented as August 28, 2021.")
    add("configuration", "reno6_oppo_ph_launch", "OPPO Philippines lists Reno6 5G at 8 GB RAM / 128 GB storage in Aurora or Stellar Black", "8 GB RAM / 128 GB storage; Aurora / Stellar Black", note="The local OPPO announcement states the Philippine configuration and colors. This row is matched to CPH2251 Reno6 5G; Reno6 Z 5G and non-Philippine configurations remain separate.")
    add("philippine_release_date", "reno6_oppo_ph_launch", "OPPO Philippines says Reno6 5G would be available from August 28, 2021", "2021-08-28", note="Official local availability date. OPPO's August announcement gives Reno6 Z 5G a separate August 14 date.")
    add("official_launch_price_php", "reno6_oppo_ph_launch", "Official Philippine launch price for Reno6 5G: PHP 26,999", 26999, unit="PHP", note="Historical local launch price for the 8 GB / 128 GB CPH2251 configuration; this is not a current offer.")
    add("current_price_php", "reno6_lahatdito_offer", "Marketplace page shows PHP 32,518 for a Reno6 5G 8+128 GB listing, but its captured page was last crawled about 10 months earlier; seller authorization, condition, and current orderability are unconfirmed", 32518, status="PENDING_VERIFICATION", unit="PHP", note="Stale marketplace candidate only. Keep the catalog's current price blank until a dated, presently orderable Philippine offer and item condition are independently confirmed.", price_type="stale_marketplace_offer_candidate")
    add("display_size", "reno6_oppo_global_specs", "6.4-inch display", 6.4, key="displayInches", unit="in", note="Manufacturer's CPH2251 specification. Local coverage sometimes prints 6.43 inches; OPPO's documented 6.4-inch value is used consistently.")
    add("display_technology", "reno6_oppo_global_specs", "AMOLED (rigid screen)", "AMOLED", key="displayType", note="Manufacturer specification.")
    add("display_resolution", "reno6_oppo_global_specs", "FHD+ 1080 × 2400", "2400 x 1080", key="resolution", note="Manufacturer specification; catalog convention records height by width.")
    add("display_refresh_rate", "reno6_oppo_global_specs", "Maximum 90 Hz; selectable 90 Hz or 60 Hz", 90, key="refreshHz", unit="Hz", note="Manufacturer specification.")
    add("display_brightness", "reno6_oppo_global_specs", "430 nits typical; 600 nits typical in sunlight; 750 nits local peak", "430 nits typical; 600 nits sunlight typical maximum; 750 nits local peak", note="Manufacturer distinguishes typical, sunlight, and local peak figures; they are not collapsed into one brightness number.")
    add("display_protection", "reno6_manilashaker_launch", "ManilaShaker reports Corning Gorilla Glass 5 on the front; OPPO's reviewed spec page does not name the cover-glass generation", "Corning Gorilla Glass 5 (front; secondary report)", status="VERIFIED_SECONDARY", note="Secondary Philippine report only. No claim is made about rear-glass protection or the frame.")
    add("chipset", "reno6_oppo_global_specs", "MediaTek Dimensity 900", "MediaTek Dimensity 900", key="chipset", note="Manufacturer identifies this chipset for Reno6 5G CPH2251.")
    add("process_node", "reno6_mediatek_dimensity900", "TSMC 6 nm process for the MediaTek Dimensity 900", "6 nm (TSMC)", unit="nm", note="Chipset-vendor specification, applied to the phone's manufacturer-identified Dimensity 900 platform.")
    add("cpu", "reno6_mediatek_dimensity900", "Octa-core: 2x Arm Cortex-A78 up to 2.4 GHz + 6x Arm Cortex-A55 up to 2.0 GHz", "8-core: 2x Cortex-A78 up to 2.4 GHz + 6x Cortex-A55 up to 2.0 GHz", key="cpu", note="MediaTek platform specifications. These are chipset CPU details, not a measured benchmark.")
    add("gpu", "reno6_oppo_global_specs", "OPPO and MediaTek list Arm Mali-G68 MC4; ManilaShaker's local article says Mali-G78 MC4", "Arm Mali-G68 MC4", key="gpu", note="The manufacturer and SoC vendor agree on Mali-G68 MC4. ManilaShaker's Mali-G78 entry is retained here as a documented secondary-source typo rather than copied into the catalog.")
    add("operating_system", "reno6_oppo_global_specs", "ColorOS 11.3 based on Android 11", "ColorOS 11.3 (Android 11)", key="os", note="Launch-era OS specification, not a claim about the version currently installed on every unit.")
    add("os_support", "reno6_oppo_global_specs", "No model-specific update duration or end-of-support date is stated on the reviewed manufacturer page", None, status="NOT_DISCLOSED", note="No upgrade commitment, delivered upgrade history, or support end date is inferred.")
    add("ram_capacity", "reno6_oppo_global_specs", "8 GB RAM", 8, key="ramGb", unit="GB", note="Matches the sole Philippine 8 GB / 128 GB configuration stated by OPPO Philippines.")
    add("ram_type", "reno6_oppo_global_specs", "LPDDR4X at 2133 MHz, 2 × 16-bit", "LPDDR4X", key="ramType", note="Manufacturer specification.")
    add("storage_capacity", "reno6_oppo_global_specs", "128 GB ROM", 128, key="storageGb", unit="GB", note="Exact Philippine configuration confirmed in OPPO's local launch release.")
    add("storage_type", "reno6_manilashaker_launch", "ManilaShaker reports 128 GB UFS 2.1 for the local Reno6 5G", "UFS 2.1", status="VERIFIED_SECONDARY", note="Secondary Philippine report tied to the exact local 8 GB / 128 GB device; OPPO's reviewed spec page does not state the storage interface.")
    add("storage_expansion", "reno6_oppo_global_specs", "OPPO's exact CPH2251 spec says external memory is not supported; YugaTech's hands-on describes a tray accepting two Nano-SIM cards and a microSD card", None, status="CONFLICTING_INFORMATION", note="The source claims conflict. Do not show a definitive expandable-storage value until the CPH2251 Philippine variant is resolved.")
    add("rear_camera_system", "reno6_oppo_global_specs", "64 MP main + 8 MP ultrawide + 2 MP macro", "64 MP main + 8 MP ultrawide + 2 MP macro", key="rearCameraMp", catalog_value=64, note="Manufacturer lists three rear modules; the catalog numeric field represents the main-camera resolution.")
    add("main_camera_sensor", "reno6_oppo_global_specs", "64 MP main camera, f/1.7, 81° FOV, 6P lens, AF; sensor make/model not stated", "64 MP main, f/1.7, 81° FOV; sensor model not disclosed", note="Manufacturer specification; no sensor identity or sensor size is inferred.")
    add("ultrawide_camera", "reno6_oppo_global_specs", "8 MP ultrawide, f/2.2, 120° FOV, 5P lens", "8 MP ultrawide, f/2.2, 120° FOV", note="Manufacturer specification.")
    add("telephoto_camera", "reno6_oppo_global_specs", "The complete rear-camera list contains main, ultrawide, and macro modules; no telephoto module is listed", "No telephoto camera listed", status="NOT_APPLICABLE", note="The manufacturer's complete three-module list does not include a telephoto camera.")
    add("front_camera", "reno6_oppo_global_specs", "32 MP front camera, f/2.4, 85° FOV", 32, key="frontCameraMp", unit="MP", note="Manufacturer specification; numeric catalog field records resolution.")
    add("video_recording", "reno6_oppo_global_specs", "Rear: 4K 30 fps; 1080p 30/60 fps; 720p 30/60 fps. Front: 1080p or 720p at 30 fps", "Rear 4K30, 1080p30/60, 720p30/60; front 1080p/720p30", key="video", note="Manufacturer's listed modes and frame rates.")
    add("battery_capacity", "reno6_oppo_global_specs", "4,300 mAh / 16.64 Wh typical; two series-connected cells", 4300, key="batteryMah", unit="mAh", note="Manufacturer's typical capacity; the local OPPO release confirms the 4,300 mAh capacity.")
    add("battery_technology", "reno6_gsmarena", "GSMArena identifies a non-removable Li-Po battery; OPPO lists capacity but not chemistry on its spec page", "Lithium-polymer; secondary source", status="VERIFIED_SECONDARY", note="Chemistry is taken from the exact-model secondary listing, not inferred from capacity or charging behavior.")
    add("wired_charging", "reno6_oppo_ph_launch", "65 W SuperVOOC 2.0", 65, key="chargingW", unit="W", note="OPPO Philippines confirms the local model's wired charging rate and protocol.")
    add("wireless_charging", "reno6_oppo_global_specs", "Wireless and reverse wireless charging are not stated on the reviewed manufacturer specification page", None, status="NOT_DISCLOSED", note="Silence is not interpreted as a confirmed hardware absence.")
    add("dimensions", "reno6_oppo_global_specs", "About 156.8 × 72.1 × 7.59 mm", "156.8 x 72.1 x 7.59 mm", key="dimensions", unit="mm", note="Manufacturer says dimensions may vary by configuration and measurement.")
    add("weight", "reno6_oppo_global_specs", "About 182 g", 182, key="weightG", unit="g", note="Manufacturer says weight may vary by configuration and measurement.")
    add("materials", "reno6_manilashaker_launch", "ManilaShaker reports Gorilla Glass 5 on the front; rear-cover and frame materials are not established by the reviewed sources", None, status="NOT_DISCLOSED", note="Front display protection is recorded separately. Rear and frame materials remain blank.")
    add("ingress_protection", "reno6_oppo_global_specs", "No IP rating or water-resistance certification is stated on the reviewed manufacturer page", None, status="NOT_DISCLOSED", note="No protection rating is inferred.")
    add("sim_esim", "reno6_oppo_global_specs", "Dual Nano-SIM supported; eSIM is not stated", "Dual Nano-SIM; eSIM not disclosed", key="sim", note="Manufacturer specification.")
    add("cellular_bands", "reno6_oppo_global_specs", "2G GSM 850/900/1800/1900; 3G WCDMA 1/2/4/5/6/8/19; 4G TD-LTE 38/39/40/41 and FDD 1/2/3/4/5/7/8/12/17/18/19/20/26/28/66; 5G NR n1/n3/n5/n7/n8/n20/n28/n38/n40/n41/n66/n77/n78", "2G/3G/4G/5G bands as listed by OPPO for CPH2251", key="cellular", note="Manufacturer's model-page bands. This list does not guarantee carrier compatibility or service availability in the Philippines.")
    add("wifi", "reno6_oppo_global_specs", "Wi-Fi 6 (802.11ax), Wi-Fi 5 (802.11ac), 802.11a/b/g/n; 2.4/5.1/5.8 GHz; Wi-Fi Display/tethering; 2×2 MIMO and MU-MIMO", "Wi-Fi 6 (802.11ax), dual-band", key="wifi", note="Manufacturer specification.")
    add("bluetooth", "reno6_oppo_global_specs", "Bluetooth 5.2; SBC, AAC, aptX, LDAC, LHDC", "Bluetooth 5.2", note="Manufacturer specification.")
    add("usb", "reno6_oppo_global_specs", "USB Type-C, USB 2.0, OTG; Type-C earphone support", "USB Type-C (USB 2.0, OTG); Type-C audio", key="ports", note="Manufacturer specification. No 3.5 mm-jack claim is added.")
    add("nfc", "reno6_oppo_global_specs", "NFC supports Android Beam, UICC, HCE, and NFC-SIM functions", "NFC supported", note="Manufacturer specification for model CPH2251.")
    add("gnss", "reno6_oppo_global_specs", "BeiDou, GPS, GLONASS, Galileo, and QZSS; A-GPS, Wi-Fi, mobile-network, and electronic-compass positioning also listed", "BeiDou, GPS, GLONASS, Galileo, QZSS", note="Manufacturer specification.")
    add("audio", "reno6_oppo_global_specs", "Type-C earphone support; loudspeaker channel configuration is not stated on the manufacturer specification page", "Type-C audio; speaker configuration not disclosed", note="No stereo-speaker or 3.5 mm-jack claim is inferred.")
    add("sensors", "reno6_oppo_global_specs", "Geomagnetic, color-temperature, on-screen proximity, on-screen optical, accelerometer, gravity, gyroscope, and pedometer sensors", "Geomagnetic, color temperature, proximity, optical, accelerometer, gravity, gyroscope, pedometer", note="Manufacturer specification.")

    if len(out) != 46:
        raise ValueError(f"Expected 46 reviewed phone fields, got {len(out)}")
    source_ids = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in out} - source_ids)
    if missing:
        raise ValueError(f"Fields reference undefined sources: {missing}")
    return out


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "OPPO Philippines announced the Reno6 5G for official Philippine availability beginning August 28, 2021; the NTC lists CPH2251 as Reno6 5G. Workbook eligibility remains Pending.",
        "philippineAvailability": "OPPO Philippines announced Reno6 5G separately from Reno6 Z 5G and stated local availability beginning August 28, 2021. The NTC GEC list identifies CPH2251 as OPPO Reno6 5G. The workbook's unsuffixed Reno6 row is matched to CPH2251 Reno6 5G using this local evidence; Reno6 Z 5G (CPH2237) is not merged.",
        "observedAt": OBSERVED,
        "manufacturer": "OPPO",
        "catalogModel": "Reno6 5G",
        "productLine": "OPPO Reno6 5G",
        "modelNumber": "CPH2251",
        "philippineReleaseYear": 2021,
        "philippineDateLabel": "Official Philippine availability start date",
        "researchNotes": "Matched to OPPO Reno6 5G (CPH2251), separate from Reno6 Z 5G (CPH2237). Philippine configuration: 8 GB / 128 GB; scope remains Pending. Current price, global release date, storage expansion, and image reuse remain unresolved.",
        "qualityFlag": "Reno6 5G (CPH2251) matched; storage expansion, global date, current price, and image reuse unresolved.",
        "openIssues": [
            {"issue": "Workbook label is unsuffixed Reno6", "action": "Display as Reno6 5G (CPH2251), supported by OPPO Philippines and NTC; keep Reno6 Z 5G (CPH2237) separate."},
            {"issue": "Global release date differs between GSMArena and Kimovil and the manufacturer does not state an exact global date", "action": "Leave the exact global release date blank and preserve both secondary source statements."},
            {"issue": "OPPO says external memory is not supported; a YugaTech hands-on describes a microSD card tray", "action": "Keep expandable-storage status unresolved until the Philippines CPH2251 configuration is confirmed."},
            {"issue": "LahatDito price page was last crawled about 10 months before review; current offer, condition, and seller authorization are unconfirmed", "action": "Retain PHP 32,518 as a stale candidate only; do not show a catalog current price."},
            {"issue": "Exact product images appear on OPPO's page without a reusable license", "action": "Use the neutral placeholder unless documented image-use permission is established."},
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
            or device.get("model") != "Reno6"):
        raise ValueError("Inventory row no longer matches OPPO Reno6")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("OPPO Reno6 already has a manual review; inspect before replacing")

    variant = {
        "id": f"{DEVICE}-8gb-128gb-ph",
        "label": "8 GB RAM / 128 GB storage",
        "sku": None,
        "modelCode": "CPH2251",
        "notes": "Philippine OPPO Reno6 5G configuration. Available colors: Aurora and Stellar Black.",
        "workbookRow": 26,
    }
    record = {
        "deviceId": DEVICE,
        "configurationId": variant["id"],
        "brand": "OPPO",
        "model": "Reno6",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "sources": SOURCES,
        "fields": fields_for(),
        "availabilityEvidence": availability_evidence(),
        "replacementVariants": [variant],
        "replaceUnrecordedPlaceholder": True,
    }
    manual["records"].append(record)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "OPPO's official Reno6 5G CPH2251 product page shows exact-model images, but does not state a reusable image license or grant permission. No image is embedded.",
        "sourcePage": URL_OPPO_PRODUCT,
        "assetUrl": None,
        "scope": "Exact OPPO Reno6 5G CPH2251; official page shows Aurora and Stellar Black product images",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for OPPO Reno6 5G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    config_id = variant["id"]
    prices = [
        {"device_id": DEVICE, "amount_php": 26999, "configuration_id": config_id,
         "configuration_match": "exact", "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "historical_ph_official_launch_price", "source_published_at": "2021-08-06",
         "excerpt": "OPPO Philippines announced Reno6 5G 8 GB / 128 GB at PHP 26,999, available from August 28, 2021.",
         "source_url": URL_OPPO_PH, "source_kind": "manufacturer_ph_launch_price",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 32518, "configuration_id": config_id,
         "configuration_match": "exact_model_and_memory_title_condition_not_stated_stale_page_snapshot",
         "variant_ram_gb": 8, "variant_storage_gb": 128,
         "price_type": "stale_marketplace_offer_candidate", "source_published_at": None,
         "excerpt": "LahatDito listing title says OPPO Reno6 5G 8+128 GB and showed PHP 32,518 / in-stock text / 300 available, but the page snapshot was last crawled about 10 months before review. Item condition, seller authorization, and current orderability are unverified.",
         "source_url": URL_LAHATDITO, "source_kind": "stale_marketplace_price_candidate_not_verified",
         "observed_at": OBSERVED_AT, "local_availability_verified": False,
         "availability_status": "stale_snapshot_condition_and_current_stock_unverified"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "OPPO", "model_name": "Reno6 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_OPPO_PH, "result": "Official Philippine launch reference confirms PHP 26,999 for 8 GB / 128 GB; historical launch price only."},
            {"device_id": DEVICE, "source_url": URL_LAHATDITO, "result": "Exact-title 8+128 marketplace page displays PHP 32,518 and in-stock text, but page snapshot is about 10 months old; not accepted as current."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "OPPO Reno6 workbook row -> Philippine OPPO Reno6 5G / CPH2251; Reno6 Z 5G remains separate",
        "configuration": variant["label"],
        "reviewedFields": len(record["fields"]),
        "philippineAvailability": "2021-08-28",
        "officialLaunchPricePhp": 26999,
        "currentPrice": "blank; stale PHP 32,518 marketplace candidate retained for audit",
        "image": "neutral placeholder; reuse rights not established",
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
