#!/usr/bin/env python3
"""Record sourced Philippine launch evidence for OPPO Reno8 5G (workbook row 89)."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/oppo-reno8-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_61b7b139393500"
CONFIG = f"{DEVICE}-8gb-256gb-ph-launch"
MODEL_CODE = "CPH2359"

URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_OPPO_PH = "https://www.oppo.com/ph/smartphones/series-reno/reno8-5g/specs/"
URL_OPPO_UK = "https://www.oppo.com/uk/smartphones/series-reno/reno8-5g/specs/"
URL_OPPO_INDIA = "https://www.oppo.com/in/newsroom/press/oppo-unveils-reno8-series-in-india/"
URL_PTG_LAUNCH = "https://www.pinoytechnoguide.com/2022/09/oppo-reno8-series-5g-officially-launched-philippines.html"
URL_PTG_SPECS = "https://www.pinoytechnoguide.com/smartphones/oppo-reno8-5g"
URL_YUGA = "https://www.yugatech.com/mobile/oppo-reno8-5g-reno8-z-5g-priced-in-the-philippines/"
URL_2ND_OPINION = "https://2ndopinion.ph/be-the-first-to-experience-the-oppo-reno8-series-5g-available-for-pre-order-now/"
URL_NANO = "https://nanoreview.net/en/phone/oppo-reno-8"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-oppo-reno8"
URL_GSMARENA = "https://www.gsmarena.com/oppo_reno8-11684.php"
URL_MEDIATEK = "https://www.mediatek.com/products/smartphones-2/mediatek-dimensity-1300"
URL_IMAGE = "https://www.oppo.com/content/dam/oppo/common/mkt/specs/reno8-5g/reno8-5g-newcolor-860_720-1.png"


def source(source_id, publisher, url, purpose, note, publication_date=None):
    return {
        "id": source_id,
        "publisher": publisher,
        "url": url,
        "publicationDate": publication_date,
        "accessDate": OBSERVED,
        "purpose": purpose,
        "note": note,
    }


sources = [
    source("oppo_reno8_ntc", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and model-code match",
           "The 2022 NTC GEC lists OPPO model CPH2359 as OPPO Reno8 5G. It also contains a second CPH2457 entry labeled Reno8 5G; that code is not used for this match because OPPO's exact CPH2359 product page and the local launch coverage identify the 5G product as CPH2359."),
    source("oppo_reno8_ph_specs", "OPPO Philippines", URL_OPPO_PH,
           "Primary Philippine exact-model specifications, imagery, and current product page",
           "OPPO's Philippine product specification page identifies Reno8 5G as CPH2359 and provides display, cameras, chipset, battery, charging, connectivity, sensors, and dimensions. Its currently indexed page lists 12 GB + 256 GB and Shimmer Black / Sunkissed Beige, unlike the contemporaneous 2022 Philippine launch sources (8 GB + 256 GB; Shimmer Black / Shimmer Gold). This discrepancy is retained; the current page does not establish a dated 2022 second local configuration."),
    source("oppo_reno8_uk_specs", "OPPO United Kingdom", URL_OPPO_UK,
           "Primary exact-model family specifications and configuration cross-check",
           "OPPO's exact CPH2359 specification page lists 8 GB + 256 GB, LPDDR4x, UFS 3.1, Shimmer Black / Shimmer Gold, and the handset hardware. This supports the 8/256 model configuration but is not used as Philippine sales evidence."),
    source("oppo_reno8_india_launch", "OPPO India", URL_OPPO_INDIA,
           "Manufacturer announcement date and global model-family cross-check",
           "OPPO announced the Reno8 5G in India on July 18, 2022. The India-market specification is 8 GB / 128 GB; it is cited only for the dated manufacturer launch, not for the Philippine configuration.", "2022-07-18"),
    source("oppo_reno8_ptg_launch", "Pinoy Techno Guide", URL_PTG_LAUNCH,
           "Philippine launch date, availability, official price, and local hardware",
           "Published September 1, 2022. Reports OPPO Philippines officially launched Reno8 5G locally, identifies 8 GB RAM / 256 GB storage, PHP 27,999 official price, and availability through OPPO stores, authorized retailers, telco partners, and official online shops. It distinguishes Reno8 5G from Reno8 Z 5G.", "2022-09-01"),
    source("oppo_reno8_ptg_specs", "Pinoy Techno Guide", URL_PTG_SPECS,
           "Local launch price and Philippine technical configuration cross-check",
           "The Reno8 5G page reports PHP 27,999, 8 GB RAM, 256 GB storage, Dimensity 1300, 50+8+2 MP rear cameras, 32 MP front camera, 4,500 mAh, 80 W, Wi-Fi 6, and Bluetooth 5.3. Its prose calls storage expandable while its specification table says no expansion; the storage-expansion field remains unresolved.", "2022-08-23"),
    source("oppo_reno8_yugatech", "YugaTech Philippines", URL_YUGA,
           "Philippine launch pricing, pre-order timing, and local configuration cross-check",
           "Published September 1, 2022. Reports PHP 27,999 and pre-orders from September 1 to 8, 2022; lists the Reno8 5G with 8 GB LPDDR4x RAM, 256 GB UFS 3.1 storage, Dimensity 1300, 4,500 mAh battery, and local 80 W charging. Price is historical, not current.", "2022-09-01"),
    source("oppo_reno8_2ndopinion", "2nd Opinion Philippines", URL_2ND_OPINION,
           "Philippine preorder and hardware cross-check",
           "Reports the Reno8 5G preorder period and 8 GB RAM / 256 GB storage, Dimensity 1300, ColorOS 12.1, 4,500 mAh battery, 80 W charging, Shimmer Gold, and Shimmer Black.", "2022-09-01"),
    source("oppo_reno8_nanoreview", "NanoReview", URL_NANO,
           "Secondary processor, display, camera, battery, and connectivity cross-check",
           "Exact Reno8 model-family page used to cross-check Dimensity 1300 architecture, Mali-G77 MC9, Wi-Fi 6, Bluetooth 5.3, camera suite, and battery. Its generic release date, performance scores, ratings, and global price are not treated as Philippine facts; regional differences are noted."),
    source("oppo_reno8_kimovil", "Kimovil", URL_KIMOVIL,
           "Secondary exact global configuration and hardware cross-check",
           "The Reno8 Global 8 GB / 256 GB listing corroborates the configuration and selected hardware fields. Kimovil's seller prices are international and are not used as current Philippine prices."),
    source("oppo_reno8_gsmarena", "GSMArena", URL_GSMARENA,
           "Secondary exact model-number family and technical cross-check",
           "Exact CPH2359 family page used to cross-check release timing, bands, body, display, chipset, memory, and interface. Regional and rounded specification differences are not silently applied to the Philippine launch configuration."),
    source("oppo_reno8_mediatek", "MediaTek", URL_MEDIATEK,
           "Primary Dimensity 1300 platform reference",
           "MediaTek platform material is used only for chipset process and platform facts; handset specifications remain attributed to OPPO and model-specific sources."),
]

def field(field_id, status, source_id, source_value, normalized_value, note,
          catalog_key=None, catalog_value=None, unit=None):
    item = {
        "fieldId": field_id,
        "status": status,
        "sourceId": source_id,
        "sourceValue": source_value,
        "normalizedValue": normalized_value,
        "note": note,
        "configurationMatch": "OPPO Reno8 5G CPH2359; Philippine 2022 launch listing, 256 GB storage",
    }
    if catalog_key is not None:
        item["catalogKey"] = catalog_key
        item["catalogValue"] = catalog_value
    if unit is not None:
        item["unit"] = unit
    return item


fields = [
    field("model_number", "VERIFIED", "oppo_reno8_ntc", "NTC GEC lists OPPO CPH2359 as OPPO Reno8 5G", MODEL_CODE,
          "Exact NTC model-code match corroborated by OPPO Philippines's CPH2359 product page."),
    field("global_release_date", "VERIFIED", "oppo_reno8_india_launch", "OPPO India announced Reno8 5G on July 18, 2022", "2022-07-18",
          "Manufacturer announcement date for the model family; launch dates vary by market. The India-market storage SKU is not transferred to the Philippine record."),
    field("configuration", "VERIFIED_SECONDARY", "oppo_reno8_ptg_launch", "Philippine launch coverage lists 8 GB RAM / 256 GB storage; OPPO UK exact CPH2359 page also lists 8/256", "8 GB RAM / 256 GB storage; Shimmer Black and Shimmer Gold reported at launch",
          "The dated Philippine launch configuration is 8/256 and is corroborated by OPPO's exact CPH2359 UK specifications. The current OPPO Philippines page lists 12/256 for CPH2359 and Sunkissed Beige; it does not date that configuration or explain the RAM difference, so no additional Philippine variant is inferred."),
    field("philippine_release_date", "VERIFIED_SECONDARY", "oppo_reno8_ptg_launch", "OPPO Philippines launch/pre-orders began September 1, 2022; pre-order period ran through September 8", "2022-09-01",
          "Uses the first dated Philippine official-channel preorder/launch date, not a claim that every retail unit was delivered that day."),
    field("official_launch_price_php", "VERIFIED_SECONDARY", "oppo_reno8_yugatech", "Official Philippine price PHP 27,999 for OPPO Reno8 5G; Pinoy Techno Guide independently reports the same price", 27999,
          "Historical launch SRP for the local Reno8 5G offer. It is not a current price.", unit="PHP",),
    field("current_price_php", "PENDING_VERIFICATION", "oppo_reno8_yugatech", "No current dated, orderable Philippine offer was verified", None,
          "Keep blank; the 2022 SRP and international Kimovil offers are not current Philippine prices.", unit="PHP"),
    field("display_size", "VERIFIED", "oppo_reno8_ph_specs", "6.4-inch display", 6.4,
          "Manufacturer exact CPH2359 page and Philippine launch reporting agree.", "displayInches", 6.4, "inches"),
    field("display_technology", "VERIFIED", "oppo_reno8_ph_specs", "AMOLED (rigid screen)", "AMOLED",
          "OPPO Philippine exact-model specifications.", "displayType", "AMOLED"),
    field("display_resolution", "VERIFIED", "oppo_reno8_ph_specs", "FHD 2400 × 1080", "2400 x 1080",
          "Manufacturer exact-model resolution.", "resolution", "2400 x 1080", "pixels"),
    field("display_refresh_rate", "VERIFIED", "oppo_reno8_ph_specs", "Maximum 90 Hz", 90,
          "OPPO notes that refresh rate may vary by mode and app.", "refreshHz", 90, "Hz"),
    field("display_brightness", "VERIFIED", "oppo_reno8_ph_specs", "430 nits typical; 600 nits HBM; 800 nits peak", "430 nits typical; 600 nits HBM; 800 nits peak",
          "Manufacturer-published levels; keep their measurement modes distinct.", unit="nits"),
    field("display_protection", "VERIFIED", "oppo_reno8_ph_specs", "Corning Gorilla Glass 5 cover glass", "Corning Gorilla Glass 5",
          "OPPO lists the display cover glass; this does not assert protection for other body surfaces."),
    field("chipset", "VERIFIED", "oppo_reno8_ph_specs", "MediaTek Dimensity 1300", "MediaTek Dimensity 1300",
          "OPPO Philippine page and local launch sources identify the same SoC.", "chipset", "MediaTek Dimensity 1300"),
    field("process_node", "VERIFIED_SECONDARY", "oppo_reno8_nanoreview", "Dimensity 1300 is manufactured on TSMC 6 nm process", 6,
          "Chip platform process, not a claim about the handset's overall fabrication.", unit="nm"),
    field("cpu", "VERIFIED_SECONDARY", "oppo_reno8_nanoreview", "1x Cortex-A78 at 3.0 GHz + 3x Cortex-A78 at 2.6 GHz + 4x Cortex-A55 at 2.0 GHz", "1x Cortex-A78 3.0 GHz + 3x Cortex-A78 2.6 GHz + 4x Cortex-A55 2.0 GHz",
          "NanoReview's exact chipset architecture cross-check; OPPO lists 1+3+4 cores and maximum 3.0 GHz.", "cpu", "1x Cortex-A78 3.0 GHz + 3x Cortex-A78 2.6 GHz + 4x Cortex-A55 2.0 GHz"),
    field("gpu", "VERIFIED", "oppo_reno8_ph_specs", "ARM Mali-G77 MC9 graphics", "Arm Mali-G77 MC9",
          "The GPU model is agreed by OPPO and secondary references; clock frequency reports differ (OPPO 866 MHz, NanoReview 886 MHz) and is not stored.", "gpu", "Arm Mali-G77 MC9"),
    field("gpu_clock", "CONFLICTING_INFORMATION", "oppo_reno8_ph_specs", "OPPO lists 866 MHz; NanoReview lists 886 MHz", None,
          "Do not normalize a GPU clock until the source discrepancy is resolved.", unit="MHz"),
    field("operating_system", "VERIFIED_SECONDARY", "oppo_reno8_ptg_launch", "ColorOS 12.1 based on Android 12 at Philippine launch", "ColorOS 12.1 based on Android 12",
          "Launch software version, not a claim about current installed software.", "os", "ColorOS 12.1 based on Android 12"),
    field("os_support", "PENDING_VERIFICATION", "oppo_reno8_ph_specs", "Current supported update policy for the Philippine CPH2359 was not established", None,
          "Do not infer update duration from generic brand policies."),
    field("ram_capacity", "CONFLICTING_INFORMATION", "oppo_reno8_ph_specs", "2022 Philippine launch sources and OPPO UK exact CPH2359 page list 8 GB; current OPPO Philippines CPH2359 page lists 12 GB", None,
          "The 2022 launch config remains described as 8/256 in the variant label and dated evidence. The current Philippine page's 12/256 listing has no effective date or explanation (for example, memory expansion versus a later SKU), so the normalized hardware RAM field is blank pending resolution.", unit="GB"),
    field("ram_type", "VERIFIED", "oppo_reno8_uk_specs", "LPDDR4x", "LPDDR4x",
          "OPPO exact CPH2359 model page; the Philippine current page also lists LPDDR4x."),
    field("storage_capacity", "VERIFIED_SECONDARY", "oppo_reno8_ptg_launch", "Philippine launch coverage lists 256 GB; exact CPH2359 manufacturer page lists 256 GB", 256,
          "Local launch and manufacturer exact-model specifications agree.", "storageGb", 256, "GB"),
    field("storage_type", "VERIFIED", "oppo_reno8_uk_specs", "UFS 3.1", "UFS 3.1",
          "OPPO exact CPH2359 specifications.", "storageType", "UFS 3.1"),
    field("storage_expansion", "CONFLICTING_INFORMATION", "oppo_reno8_ptg_specs", "Pinoy Techno Guide's prose says expandable, while its spec table says no expansion; other exact-model listings indicate no card slot", None,
          "The conflict is internal to one source and corroboration is not definitive; leave the expansion field blank."),
    field("rear_camera_system", "VERIFIED", "oppo_reno8_ph_specs", "50 MP main + 8 MP wide-angle + 2 MP macro", "50 MP main + 8 MP ultra-wide + 2 MP macro",
          "Manufacturer exact CPH2359 page and local launch coverage agree.", "rearCameraMp", "50 + 8 + 2 MP"),
    field("main_camera_sensor", "VERIFIED", "oppo_reno8_ph_specs", "Sony IMX766 50 MP, f/1.8", "Sony IMX766 50 MP, f/1.8",
          "OPPO lists the sensor model, aperture, and lens details."),
    field("ultrawide_camera", "VERIFIED", "oppo_reno8_ph_specs", "8 MP wide-angle camera, f/2.2, 112-degree field of view", "8 MP ultra-wide, f/2.2, 112° FOV",
          "Manufacturer exact-model camera specification."),
    field("macro_camera", "VERIFIED", "oppo_reno8_ph_specs", "2 MP macro camera", "2 MP macro",
          "Manufacturer exact-model camera specification."),
    field("front_camera", "VERIFIED", "oppo_reno8_ph_specs", "Sony IMX709 32 MP, f/2.4", 32,
          "Manufacturer exact CPH2359 page.", "frontCameraMp", 32, "MP"),
    field("video_recording", "VERIFIED", "oppo_reno8_ph_specs", "Rear up to 4K at 30 fps; front up to 1080p at 30 fps", "Rear 4K@30fps; front 1080p@30fps",
          "OPPO exact-model video modes; do not transfer modes from Pro or Z variants.", "video", "Rear 4K@30fps; front 1080p@30fps"),
    field("battery_capacity", "VERIFIED", "oppo_reno8_ph_specs", "2 × 2200 mAh rated (4400 mAh total); 2 × 2250 mAh typical (4500 mAh total)", 4500,
          "Catalog capacity uses the manufacturer's typical 4500 mAh total; rated total is 4400 mAh.", "batteryMah", 4500, "mAh (typical)"),
    field("battery_technology", "VERIFIED_SECONDARY", "oppo_reno8_gsmarena", "Non-removable Li-Po battery", "Li-Po; non-removable",
          "Secondary exact-model specification; OPPO publishes capacity but not the chemistry label."),
    field("wired_charging", "VERIFIED", "oppo_reno8_ph_specs", "80W SUPERVOOC; OPPO notes up to 80W at 220V and lower output in some regions", 80,
          "OPPO exact-model and local launch coverage both list 80 W. Philippine mains voltage is compatible with the manufacturer's 220 V 80 W condition; actual charging may vary.", "chargingW", 80, "W"),
    field("wireless_charging", "VERIFIED_SECONDARY", "oppo_reno8_gsmarena", "No wireless charging listed for the exact CPH2359 model", "Not supported",
          "Exact-model technical listing does not include wireless charging; this is not a charging-power value.", "wirelessChargingW", None),
    field("dimensions", "VERIFIED", "oppo_reno8_ph_specs", "About 160.0 × 73.4 × 7.67 mm", "About 160.0 x 73.4 x 7.67 mm",
          "Manufacturer dimensions are approximate. Some secondary pages round/review the height as 160.6 mm.", "dimensions", "About 160.0 x 73.4 x 7.67 mm", "mm"),
    field("weight", "VERIFIED", "oppo_reno8_ph_specs", "About 179 g", 179,
          "Manufacturer and local sources agree; OPPO notes manufacturing and measurement variation.", "weightG", 179, "g"),
    field("materials", "CONFLICTING_INFORMATION", "oppo_reno8_ptg_specs", "Pinoy Techno Guide reports glass front/back and polycarbonate frame; GSMArena reports glass front and plastic back/frame", None,
          "Body-material descriptions conflict; only the front cover glass is independently specified by OPPO, so no normalized body materials are recorded."),
    field("ingress_protection", "PENDING_VERIFICATION", "oppo_reno8_ph_specs", "No ingress-protection rating found on the reviewed manufacturer page or local launch sources", None,
          "Keep IP rating blank; no inference from general splash resistance or model-family pages."),
    field("sim_esim", "VERIFIED", "oppo_reno8_ph_specs", "Dual SIM supported; Nano-USIM; eSIM not listed", "Dual Nano-SIM; eSIM not recorded",
          "OPPO exact-model page lists two SIM support and Nano-USIM; no eSIM claim is made.", "sim", "Dual Nano-SIM; eSIM not recorded"),
    field("cellular_bands", "VERIFIED", "oppo_reno8_ph_specs", "Manufacturer CPH2359 bands: GSM 850/900/1800/1900; WCDMA 1/2/4/5/6/8/19; LTE TDD 38/39/40/41 and FDD 1/2/3/4/5/7/8/12/17/18/19/20/26/28; 5G n1/3/5/7/8/20/28/38/40/41/77/78", "Manufacturer-published CPH2359 2G/3G/4G/5G bands; carrier support not independently tested",
          "Band table is from OPPO Philippines for CPH2359; OPPO notes actual network availability depends on local carriers.", "cellular", "Manufacturer-published CPH2359 2G/3G/4G/5G bands; carrier support not independently tested"),
    field("wifi", "VERIFIED", "oppo_reno8_ph_specs", "Wi-Fi 6 (802.11ax), dual-band", "Wi-Fi 6, dual-band",
          "OPPO Philippines exact-model specifications.", "wifi", "Wi-Fi 6, dual-band"),
    field("bluetooth", "VERIFIED", "oppo_reno8_ph_specs", "Bluetooth 5.3, Bluetooth Low Energy", "Bluetooth 5.3",
          "OPPO Philippines exact-model specifications."),
    field("usb", "VERIFIED", "oppo_reno8_ph_specs", "USB Type-C; USB OTG supported; interface version not specified by OPPO", "USB Type-C; OTG",
          "Do not infer a USB generation from connector type alone.", "ports", "USB Type-C; OTG"),
    field("nfc", "VERIFIED", "oppo_reno8_ph_specs", "NFC card read/write and NFC-SIM/HCE support", "Yes",
          "Manufacturer exact CPH2359 specification."),
    field("gnss", "VERIFIED", "oppo_reno8_ph_specs", "GPS, A-GPS, BeiDou, GLONASS, Galileo, QZSS", "GPS, A-GPS, BeiDou, GLONASS, Galileo, QZSS",
          "Manufacturer exact-model location specification.", "gnss", "GPS, A-GPS, BeiDou, GLONASS, Galileo, QZSS"),
    field("audio", "VERIFIED_SECONDARY", "oppo_reno8_gsmarena", "No 3.5 mm headphone jack; USB Type-C audio", "USB Type-C audio; no 3.5 mm jack",
          "No speaker channel configuration is recorded because secondary pages differ.", "sound", "USB Type-C audio; no 3.5 mm jack"),
    field("sensors", "VERIFIED", "oppo_reno8_ph_specs", "Geomagnetic, light, on-screen proximity and optical, accelerometer, gravity, gyroscope sensors; in-display fingerprint", "Geomagnetic; light; on-screen proximity and optical; accelerometer; gravity; gyroscope; in-display fingerprint",
          "OPPO exact CPH2359 page lists these sensors and the optical fingerprint reader."),
    field("colors", "CONFLICTING_INFORMATION", "oppo_reno8_ptg_launch", "2022 PH launch: Shimmer Black and Shimmer Gold; current OPPO PH page: Shimmer Black and Sunkissed Beige", None,
          "The names may reflect regional naming or a later color option, but equivalence is not established. The variant label preserves the 2022 launch wording and the alternate name is documented here."),
]

configuration_label = "256 GB storage (2022 launch sources: 8 GB RAM; current OPPO PH page lists 12 GB RAM; Shimmer Black / Shimmer Gold at launch)"
notes = (
    "NTC and OPPO exact-model pages identify CPH2359 as Reno8 5G. Philippine launch sources document 8 GB / 256 GB and PHP 27,999 from September 1, 2022. OPPO UK's CPH2359 page also lists 8/256, while OPPO Philippines's currently indexed page lists 12/256 and Sunkissed Beige; the effective date/meaning of that current listing is unresolved, so the catalog RAM field remains blank and no second local configuration is inferred. Current price is not verified."
)


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    existing_reviews = [r for r in manual["records"] if r.get("deviceId") == DEVICE]
    if existing_reviews:
        raise SystemExit(f"Manual review already exists for {DEVICE}; refusing duplicate append")
    device = next((r for r in catalog if r.get("id") == DEVICE), None)
    if not device or device.get("workbookRow") != 89 or device.get("model") != "Reno8":
        raise SystemExit("Catalog target guard failed for workbook row 89 OPPO Reno8")

    review = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "OPPO",
        "model": "Reno8",
        "configuration": configuration_label,
        "configurationLabel": configuration_label,
        "modelCode": MODEL_CODE,
        "sources": sources,
        "fields": fields,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine launch and preorder coverage identifies OPPO stores, authorized retailers, telco partners, and official online shops; NTC lists exact model CPH2359 as Reno8 5G.",
            "philippineAvailability": "OPPO Reno8 5G CPH2359 was officially launched in the Philippines with preorder coverage starting September 1, 2022. Local launch sources report an 8 GB / 256 GB offer at PHP 27,999 in Shimmer Black and Shimmer Gold. OPPO's current Philippine page lists a 12 GB / 256 GB configuration and Sunkissed Beige for CPH2359; timing and configuration meaning are unresolved. Current stock and price are not verified.",
            "observedAt": OBSERVED,
            "manufacturer": "OPPO",
            "catalogModel": "Reno8",
            "productLine": "Reno8 Series",
            "modelNumber": MODEL_CODE,
            "philippineReleaseYear": 2022,
            "philippineDateLabel": "Philippine launch and preorder date",
            "researchNotes": notes + " Workbook eligibility remains Pending.",
            "qualityFlag": "Exact CPH2359 match; Philippine launch/date/SRP and 256 GB storage verified; RAM and color listings differ between contemporaneous launch sources and the current OPPO Philippines product page; current price unverified; expansion and body-material conflicts retained; image reuse rights not established; study eligibility remains Pending.",
            "openIssues": [
                {"issue": "Current OPPO Philippines exact-model page lists 12 GB + 256 GB while contemporaneous Philippine launch sources and OPPO UK's CPH2359 page list 8 GB + 256 GB", "action": "Keep the 2022 launch hardware RAM field unresolved until OPPO clarifies whether the current listing is a later physical-memory variant or includes another RAM convention; do not add an undated second local SKU."},
                {"issue": "Current OPPO Philippines page says Sunkissed Beige while 2022 local launch sources say Shimmer Gold", "action": "Preserve the dated 2022 color name and do not assume the names describe the same finish."},
                {"issue": "Expansion support is inconsistent within the local specification source", "action": "Keep storage expansion blank until exact CPH2359 documentation resolves it."},
                {"issue": "Body-material reports conflict on rear cover and frame materials", "action": "Keep body materials blank; retain only the manufacturer-specified display cover glass."},
                {"issue": "Current dated/orderable Philippine price was not verified", "action": "Keep current price blank and preserve PHP 27,999 as a historical launch SRP only."},
                {"issue": "Exact official product imagery is available but permission or reusable terms are not recorded", "action": "Keep the neutral placeholder until image reuse is authorized."},
                {"issue": "The NTC table also labels CPH2457 as Reno8 5G, while the CPH2359 match is independently corroborated", "action": "Do not merge CPH2457 into this record; review it against the inventory's separate Reno8 Z or 4G records if present."},
                {"issue": "Workbook eligibility is Pending", "action": "Preserve the study's Pending status."},
            ],
        },
        "replacementVariants": [{
            "id": CONFIG,
            "label": configuration_label,
            "sku": None,
            "modelCode": MODEL_CODE,
            "notes": notes + " Launch price PHP 27,999 is historical; current price not verified.",
            "workbookRow": 89,
        }],
        "replaceUnrecordedPlaceholder": True,
    }
    manual["records"].append(review)

    device["manufacturer"] = "OPPO"
    device["productLine"] = "Reno8 Series"
    device["modelNumber"] = MODEL_CODE
    device["releaseDate"] = "2022-07-18"
    device["philippineAvailabilityDate"] = "2022-09-01"
    device["philippineDateLabel"] = "Philippine launch and preorder date"
    device["philippineReleaseYear"] = 2022
    device["localEvidenceObservedAt"] = OBSERVED
    device["verificationStatus"] = "VERIFIED_AUTHORIZED_AVAILABILITY"
    device["scopeStatus"] = "Pending"
    device["qualityFlag"] = review["availabilityEvidence"]["qualityFlag"]
    device["exclusionReason"] = None
    device["exclusionEvidence"] = None
    device["philippineAvailability"] = review["availabilityEvidence"]["philippineAvailability"]
    device["availabilityStatus"] = review["availabilityEvidence"]["availabilityStatus"]
    device["discontinued"] = None
    device["researchNotes"] = notes
    device["openIssues"] = review["availabilityEvidence"]["openIssues"]
    device["sources"] = [
        {"organization": s["publisher"], "url": s["url"], "observedAt": OBSERVED,
         "publishedAt": s["publicationDate"], "purpose": s["purpose"], "note": s["note"]}
        for s in sources
    ]

    specs = {
        "displayInches": 6.4,
        "displayType": "AMOLED",
        "resolution": "2400 x 1080",
        "refreshHz": 90,
        "chipset": "MediaTek Dimensity 1300",
        "cpu": "1x Cortex-A78 3.0 GHz + 3x Cortex-A78 2.6 GHz + 4x Cortex-A55 2.0 GHz",
        "gpu": "Arm Mali-G77 MC9",
        "os": "ColorOS 12.1 based on Android 12",
        "ramGb": None,
        "storageGb": 256,
        "storageType": "UFS 3.1",
        "rearCameraMp": "50 + 8 + 2 MP",
        "frontCameraMp": 32,
        "video": "Rear 4K@30fps; front 1080p@30fps",
        "batteryMah": 4500,
        "chargingW": 80,
        "wirelessChargingW": None,
        "dimensions": "About 160.0 x 73.4 x 7.67 mm",
        "weightG": 179,
        "sim": "Dual Nano-SIM; eSIM not recorded",
        "cellular": "Manufacturer-published CPH2359 2G/3G/4G/5G bands; carrier support not independently tested",
        "wifi": "Wi-Fi 6, dual-band",
        "bluetooth": "Bluetooth 5.3",
        "ports": "USB Type-C; OTG",
        "gnss": "GPS, A-GPS, BeiDou, GLONASS, Galileo, QZSS",
        "sound": "USB Type-C audio; no 3.5 mm jack",
    }
    spec_sources = {
        "displayInches": URL_OPPO_PH, "displayType": URL_OPPO_PH,
        "resolution": URL_OPPO_PH, "refreshHz": URL_OPPO_PH,
        "chipset": URL_OPPO_PH, "cpu": URL_NANO, "gpu": URL_OPPO_PH,
        "os": URL_PTG_LAUNCH, "storageGb": URL_PTG_LAUNCH,
        "storageType": URL_OPPO_UK, "rearCameraMp": URL_OPPO_PH,
        "frontCameraMp": URL_OPPO_PH, "video": URL_OPPO_PH,
        "batteryMah": URL_OPPO_PH, "chargingW": URL_OPPO_PH,
        "dimensions": URL_OPPO_PH, "weightG": URL_OPPO_PH,
        "sim": URL_OPPO_PH, "cellular": URL_OPPO_PH,
        "wifi": URL_OPPO_PH, "bluetooth": URL_OPPO_PH,
        "ports": URL_OPPO_PH, "gnss": URL_OPPO_PH,
        "sound": URL_GSMARENA,
    }
    device["variants"] = [{
        "id": CONFIG,
        "label": configuration_label,
        "specs": specs,
        "specSources": spec_sources,
        "pricePhp": None,
        "priceCondition": None,
        "priceType": None,
        "priceObservedAt": None,
        "priceSourceUrl": None,
        "listingStatus": "Historical Philippine launch configuration; current listing not verified",
        "notes": notes,
        "sku": None,
        "modelCode": MODEL_CODE,
        "workbookRow": 89,
    }]
    device["imageId"] = DEVICE

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "OPPO's official CPH2359 page contains an exact-model product image, but no reusable image license or written permission to copy/embed is recorded in the project.",
        "sourcePage": URL_OPPO_PH,
        "assetUrl": URL_IMAGE,
        "scope": "Exact OPPO Reno8 5G model CPH2359; official page image depicts product, not a confirmed local color name",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for OPPO Reno8 5G CPH2359",
    }

    price_snapshot = {
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "OPPO", "model_name": "Reno8", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC GEC lists OPPO model CPH2359 as Reno8 5G; separate CPH2457 line is not merged."},
            {"device_id": DEVICE, "source_url": URL_PTG_LAUNCH, "result": "Philippine launch/preorder starts September 1, 2022; reported 8/256 local configuration and PHP 27,999 SRP."},
            {"device_id": DEVICE, "source_url": URL_OPPO_PH, "result": "OPPO exact Philippine CPH2359 product page has specs and image; current page's 12/256 config differs from the 2022 launch record."},
            {"device_id": DEVICE, "source_url": URL_OPPO_UK, "result": "OPPO exact CPH2359 specification page independently lists 8/256, LPDDR4x and UFS 3.1."},
        ],
        "prices": [
            {"device_id": DEVICE, "amount_php": 27999, "configuration_id": CONFIG,
             "configuration_match": "philippine_launch_cph2359_256gb_ram_listing_discrepancy_retained",
             "variant_ram_gb": None, "variant_storage_gb": 256,
             "price_type": "historical_ph_launch_srp", "source_published_at": "2022-09-01",
             "excerpt": "Historical Philippine launch SRP: OPPO Reno8 5G CPH2359, 256 GB storage; local launch sources list 8 GB RAM while current OPPO PH page lists 12 GB; not a current price.",
             "source_url": URL_PTG_LAUNCH, "source_kind": "historical_local_price_candidate",
             "observed_at": OBSERVED_AT, "local_availability_verified": True,
             "availability_status": "historical_price_not_current"},
            {"device_id": DEVICE, "amount_php": 27999, "configuration_id": CONFIG,
             "configuration_match": "philippine_launch_cph2359_256gb_ram_listing_discrepancy_retained",
             "variant_ram_gb": None, "variant_storage_gb": 256,
             "price_type": "historical_ph_launch_srp", "source_published_at": "2022-09-01",
             "excerpt": "Historical PHP 27,999 Philippine SRP independently listed for OPPO Reno8 5G; not a current price.",
             "source_url": URL_YUGA, "source_kind": "historical_local_price_candidate",
             "observed_at": OBSERVED_AT, "local_availability_verified": True,
             "availability_status": "historical_price_not_current"},
        ],
    }

    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(price_snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Reviewed {DEVICE}: CPH2359, row 89, {len(fields)} field assessments, {len(sources)} sources")


if __name__ == "__main__":
    main()
