#!/usr/bin/env python3
"""Review vivo V23 5G (V2130), local configurations, price and image provenance."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/vivo-v23-5g-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_768d170ed1109b"
CONFIG_8_128 = f"{DEVICE}-v2130-8gb-128gb-ph-spec"
CONFIG_12_256 = f"{DEVICE}-v2130-12gb-256gb-ph"

URL_NTC = "https://www.ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/GEC-2009-2021-Updated-.pdf"
URL_VIVO_PH_PRODUCT = "https://www.vivo.com/ph/product/productDetails?id=3996"
URL_VIVO_PH_SPECS = "https://www.vivo.com/ph/products/param/v235g?id=3996"
URL_VIVO_PH_LAUNCH_VIDEO = "https://www.youtube.com/watch?v=kF9JLqeClDg"
URL_VIVO_PH_AVAILABLE_VIDEO = "https://www.youtube.com/watch?v=jxZRHzV2PHU"
URL_PTG = "https://www.pinoytechnoguide.com/smartphones/vivo-v23-5g/amp"
URL_YUGATECH = "https://www.yugatech.com/mobile/vivo-v23-5g-v23e-specs-price-philippines/"
URL_YUGATECH_PRICE_LIST = "https://www.yugatech.com/mobile/smartphone-price-list-philippines-2022/"
URL_REVU = "https://www.revu.com.ph/2022/02/vivo-v23-5g-vivo-v23e-ph-price-available/"
URL_GSMARENA_REVIEW = "https://www.gsmarena.com/vivo_v23-review-2368.php"
URL_GSMARENA_SPECS = "https://www.gsmarena.com/compare.php3?idPhone1=11308"
URL_GSMARENA_UPDATE = "https://www.gsmarena.com/vivo_v23_receives_android_14_update-news-62012.php"
URL_KIMOVIL_12_256 = "https://www.kimovil.com/es/donde-comprar-vivo-v23-5g-12gb-256gb"
URL_KIMOVIL_8_128 = "https://www.kimovil.com/es/donde-comprar-vivo-v23-5g-in"
IMAGE_BLACK = "https://asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1641524135486/34c7c3d66fd6378d71d51e69e53745e9.png"
IMAGE_GOLD = "https://asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1641524142571/fdeb40a1fcbbabf8a2d40825804cccac.png"


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
        src("vivo_v23_ntc_gec", "National Telecommunications Commission", URL_NTC,
            "Exact Philippine model-code match",
            "The NTC 2009-2021 GEC table lists Smart Phone, vivo V2130, marketing name V23 5G. This ties the local certification record to the exact model family."),
        src("vivo_v23_ph_specs", "vivo Philippines (manufacturer)", URL_VIVO_PH_SPECS,
            "Official Philippine model specifications, supported RAM/storage choices, color-specific dimensions and connectivity",
            "The vivo Philippines V23 5G specifications page lists 8 GB / 128 GB and 12 GB / 256 GB, Dimensity 920, Funtouch OS 12, 4,200 mAh, 44 W, and local connectivity details. It lists Stardust Black and Sunshine Gold, whose published dimensions and weights differ."),
        src("vivo_v23_ph_product", "vivo Philippines (manufacturer)", URL_VIVO_PH_PRODUCT,
            "Official Philippine product identity and model image page",
            "Official vivo Philippines product page names the model V23 5G. Its linked official product images match the Stardust Black and Sunshine Gold finishes; reuse rights were not established."),
        src("vivo_v23_ph_announcement", "vivo Philippines (official channel)", URL_VIVO_PH_LAUNCH_VIDEO,
            "Official Philippine launch-date announcement",
            "Published 26 January 2022. vivo Philippines' announcement video says the V23 Series 5G launches online on 12 February 2022; this establishes the announced launch date, not an exact first transaction.", "2022-01-26"),
        src("vivo_v23_ph_available", "vivo Philippines (official channel)", URL_VIVO_PH_AVAILABLE_VIDEO,
            "Official Philippine post-launch availability confirmation",
            "Published 21 February 2022. vivo Philippines states that the V23 Series 5G is now available and points to official online stores and retail locations.", "2022-02-21"),
        src("vivo_v23_ptg_ph", "Pinoy Techno Guide Philippines", URL_PTG,
            "Philippine price, 12 GB / 256 GB launch configuration, availability and exact-model spec cross-check",
            "Published 12 February 2022. Lists V23 5G at PHP 27,999 as its official Philippine price, identifies 12 GB / 256 GB, and reports it available through vivo stores, authorized dealers and online shops.", "2022-02-12"),
        src("vivo_v23_yugatech_ph", "YugaTech Philippines", URL_YUGATECH,
            "Independent Philippine launch, price and specification cross-check",
            "Published 4 February 2022. Reports the local launch and PHP 27,999 for 12 GB / 256 GB. Its general specification block also mentions 8 GB / 128 GB; retail availability of that configuration is not separately confirmed there.", "2022-02-04"),
        src("vivo_v23_revu_ph", "Revu Philippines", URL_REVU,
            "Philippine launch configuration and price cross-check",
            "Published 4 February 2022. Says the lone V23 5G variant launching locally was 12 GB / 256 GB at PHP 27,999. This conflicts with the vivo Philippines specification page, which also lists 8 GB / 128 GB; the latter's local retail status remains unresolved.", "2022-02-04"),
        src("vivo_v23_gsmarena", "GSMArena", URL_GSMARENA_REVIEW,
            "Exact V23 5G technical reference and global configuration cross-check",
            "GSMArena's review is for the non-Pro vivo V23 5G. It reports the 8/128 and 12/256 variants, Android 12, display, camera and battery details. Its global specifications are not treated as Philippine sale evidence.", "2022-01-26"),
        src("vivo_v23_gsmarena_specs", "GSMArena", URL_GSMARENA_SPECS,
            "Exact-model global release timing and hardware reference",
            "The GSMArena V23 5G specification entry identifies announcement on 5 January 2022 and release on 19 January 2022. Global release timing does not establish Philippine availability."),
        src("vivo_v23_gsmarena_android14", "GSMArena", URL_GSMARENA_UPDATE,
            "Later global Android update event",
            "Published 14 March 2024. Reports rollout of Funtouch OS 14 based on Android 14 for vivo V23. This is an observed global update, not a future update guarantee or proof of Philippine rollout timing.", "2024-03-14"),
        src("vivo_v23_kimovil_12_256", "Kimovil", URL_KIMOVIL_12_256,
            "Exact 12 GB / 256 GB global technical cross-check",
            "The exact 12 GB / 256 GB page maps the model to V2130 and lists 12 GB LPDDR4X, 256 GB UFS 3.1, and other hardware. Its international pricing and regional NFC status are not used as Philippine evidence."),
        src("vivo_v23_kimovil_8_128", "Kimovil", URL_KIMOVIL_8_128,
            "Exact 8 GB / 128 GB global variant cross-check",
            "The exact 8 GB / 128 GB page maps the V23 5G model to V2130. Its international pricing is not used as Philippine evidence."),
        src("vivo_v23_yugatech_price_list", "YugaTech Philippines", URL_YUGATECH_PRICE_LIST,
            "Dated 2022 Philippine price-list entry; historical versus current-price distinction",
            "The 2022 price list records vivo V23 5G at PHP 27,999 with a February launch month. This is historical context, not a current orderable offer.", "2022-02-04"),
    ]


def fields(ram: int, storage: int) -> list[dict]:
    cfg = f"{ram} GB RAM / {storage} GB storage"
    variant_source = "vivo_v23_kimovil_8_128" if storage == 128 else "vivo_v23_kimovil_12_256"
    local_status = "VERIFIED_SECONDARY" if storage == 256 else "CONFLICTING_INFORMATION"
    local_note = (
        "PTG and YugaTech list this 12 GB / 256 GB local launch configuration and Revu independently reports it as the local launch SKU."
        if storage == 256 else
        "The manufacturer Philippines page lists 8 GB / 128 GB, but Revu reports 12 GB / 256 GB as the lone local launch variant. Keep this manufacturer-listed configuration separate and label Philippine retail availability unresolved."
    )
    p = "vivo_v23_ph_specs"
    local = "vivo_v23_ptg_ph"
    data = [
        f("model_number", "vivo_v23_ntc_gec", "NTC entry: vivo V2130, V23 5G", "V2130",
          note="The NTC GEC maps the exact model code to V23 5G; vivo Philippines' product page uses the same V23 5G name."),
        f("configuration", p, cfg, cfg, note="The official vivo Philippines product specifications list this exact RAM / storage combination."),
        f("philippine_configuration_availability", "vivo_v23_revu_ph",
          "12 GB / 256 GB is reported as the lone local launch SKU; vivo Philippines' product specifications also list 8 GB / 128 GB",
          "confirmed local launch SKU" if storage == 256 else None,
          status=local_status, note=local_note),
        f("global_release_date", "vivo_v23_gsmarena_specs", "Announced 5 January 2022; released 19 January 2022", "2022-01-19",
          status="VERIFIED_SECONDARY", note="The normalized date is the reported initial release date, not the earlier announcement date."),
        f("philippine_release_date", "vivo_v23_ph_announcement",
          "vivo Philippines announced a 12 February 2022 local launch; PTG reported availability on that date" if storage == 256 else "No configuration-specific Philippine sale date verified; 12 February 2022 evidence pertains to the model launch / 12 GB / 256 GB SKU",
          "2022-02-12" if storage == 256 else None,
          status="VERIFIED_SECONDARY" if storage == 256 else "PENDING_VERIFICATION",
          note="The date is the announced and reported model launch, not a verified first-sale transaction time. It is not copied to the 8 GB / 128 GB configuration."),
        f("official_launch_price_php", local, "PHP 27,999 for the 12 GB / 256 GB Philippine launch SKU" if storage == 256 else "No Philippine launch price verified for 8 GB / 128 GB",
          27999 if storage == 256 else None, unit="PHP",
          status="VERIFIED_SECONDARY" if storage == 256 else "PENDING_VERIFICATION",
          note="The PHP 27,999 historical launch price is specifically associated with 12 GB / 256 GB. It is not copied to the 8 GB / 128 GB configuration."),
        f("current_price_php", "vivo_v23_yugatech_price_list", "No current dated, orderable Philippine offer verified; PHP 27,999 is the 2022 launch price", None,
          status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank and retain the price only as a dated historical snapshot."),
        f("display_size", p, "6.44-inch display", 6.44, key="displayInches", unit="in"),
        f("display_technology", p, "AMOLED", "AMOLED", key="displayType"),
        f("display_resolution", p, "2400 x 1080 FHD+", "1080 x 2400", key="resolution"),
        f("display_refresh_rate", "vivo_v23_gsmarena", "90 Hz", 90, key="refreshHz", unit="Hz", status="VERIFIED_SECONDARY"),
        f("display_brightness", p, "Peak brightness not listed in the reviewed manufacturer Philippines specifications", None, status="PENDING_VERIFICATION", unit="nits"),
        f("display_protection", "vivo_v23_gsmarena", "Schott Xensation Up protective glass reported for the exact V23 5G", "Schott Xensation Up", status="VERIFIED_SECONDARY"),
        f("chipset", p, "MediaTek Dimensity 920", "MediaTek Dimensity 920", key="chipset"),
        f("process_node", variant_source, "6 nm", 6, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", variant_source, "2 x Cortex-A78 at 2.5 GHz + 6 x Cortex-A55 at 2.0 GHz", "2x Cortex-A78 2.5 GHz + 6x Cortex-A55 2.0 GHz", key="cpu", status="VERIFIED_SECONDARY"),
        f("gpu", variant_source, "Arm Mali-G68 MC4", "Mali-G68 MC4", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", "vivo_v23_gsmarena", "Android 12 with Funtouch OS 12 at launch", "Android 12 / Funtouch OS 12", key="os", status="VERIFIED_SECONDARY"),
        f("os_support", "vivo_v23_gsmarena_android14", "Funtouch OS 14 based on Android 14 was reported rolling out globally in March 2024", "Android 14 / Funtouch OS 14 rollout reported 2024-03",
          status="VERIFIED_SECONDARY", note="This records an observed global update only; it is not a future support promise or a Philippines-specific rollout confirmation."),
        f("ram_capacity", p, f"{ram} GB RAM", ram, key="ramGb", unit="GB"),
        f("ram_type", variant_source, "LPDDR4X", "LPDDR4X", status="VERIFIED_SECONDARY"),
        f("storage_capacity", p, f"{storage} GB ROM", storage, key="storageGb", unit="GB"),
        f("storage_type", variant_source, "UFS 3.1", "UFS 3.1", key="storageType", status="VERIFIED_SECONDARY"),
        f("storage_expansion", variant_source, "No microSD expansion listed for this V2130 configuration", "No microSD expansion", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", p, "64 MP main autofocus + 8 MP ultrawide + 2 MP macro", "64 MP main + 8 MP ultrawide + 2 MP macro", key="rearCameraMp"),
        f("main_camera_sensor", p, "64 MP AF main camera, f/1.89; sensor part number not stated by vivo", "64 MP AF; f/1.89; sensor part number not recorded"),
        f("ultrawide_camera", p, "8 MP rear ultrawide, f/2.2", "8 MP rear ultrawide; f/2.2"),
        f("telephoto_camera", p, "No telephoto camera listed in vivo's triple rear-camera system", None, status="NOT_APPLICABLE"),
        f("front_camera", p, "50 MP autofocus main selfie + 8 MP ultrawide selfie", 50, key="frontCameraMp", unit="MP"),
        f("video_recording", "vivo_v23_ptg_ph", "Rear and front video up to 4K at 30 fps", "Front/rear 4K@30fps", key="video", status="VERIFIED_SECONDARY"),
        f("battery_capacity", p, "4,200 mAh typical", 4200, key="batteryMah", unit="mAh"),
        f("battery_technology", variant_source, "Li-ion polymer; non-removable", "Li-ion polymer; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", p, "44 W FlashCharge (11 V / 4 A)", 44, key="chargingW", unit="W"),
        f("wireless_charging", p, "Wireless charging is not listed in the reviewed manufacturer specifications", None, status="PENDING_VERIFICATION"),
        f("dimensions", p, "Stardust Black: 157.20 x 72.42 x 7.39 mm; Sunshine Gold: 157.20 x 72.42 x 7.55 mm",
          "Stardust Black 157.20 x 72.42 x 7.39 mm; Sunshine Gold 157.20 x 72.42 x 7.55 mm", key="dimensions", unit="mm",
          note="Both color-specific measurements are preserved instead of collapsing different finishes to one dimension."),
        f("weight", p, "Stardust Black: 179 g; Sunshine Gold: 181 g", "179 g Stardust Black; 181 g Sunshine Gold", key="weightG", unit="g",
          note="Both color-specific weights are preserved; the gold finish is 2 g heavier."),
        f("materials", "vivo_v23_gsmarena", "Glass front and back; aluminum frame; Sunshine Gold rear glass uses color-changing Fluorite AG finish", "Glass front/back; aluminum frame; color-changing gold finish", status="VERIFIED_SECONDARY"),
        f("ingress_protection", "vivo_v23_kimovil_12_256", "Kimovil reports IP65, but vivo's reviewed official specifications do not list an IP rating", None,
          status="CONFLICTING_INFORMATION", note="No IP rating is shown in vivo's product specifications; the international Kimovil profile's IP65 claim is not adopted for the Philippine model."),
        f("sim_esim", p, "Dual Nano-SIM, dual standby; no eSIM field in the vivo Philippines specification", "Dual Nano-SIM; eSIM not recorded"),
        f("cellular_bands", p, "2G GSM B2/B3/B5/B8; 3G WCDMA B1/B2/B4/B5/B8; 4G FDD B1/B2/B3/B4/B5/B7/B8/B12/B17/B18/B19/B20/B26/B28/B32; 4G TDD B38/B39/B40/B41; 5G n1/n3/n5/n7/n8/n20/n28/n38/n40/n41/n77/n78", "2G/3G/4G/5G; exact bands in sourceValue", key="cellular"),
        f("wifi", p, "Dual-band Wi-Fi, 2.4 GHz and 5 GHz; 802.11 standard not stated on vivo PH page", "Dual-band 2.4 / 5 GHz; Wi-Fi standard not recorded", key="wifi"),
        f("bluetooth", p, "Bluetooth 5.2", "Bluetooth 5.2"),
        f("usb", p, "USB Type-C", "USB Type-C", key="ports"),
        f("nfc", p, "NFC supported on the vivo Philippines specification page", "Yes", key="nfc",
          note="Local manufacturer page says NFC is supported. A Kimovil international configuration says No; that regional secondary value is not used to override the Philippine product page."),
        f("gnss", p, "GPS, BeiDou, GLONASS, Galileo and QZSS", "GPS; BeiDou; GLONASS; Galileo; QZSS", key="gnss"),
        f("audio", "vivo_v23_gsmarena", "Hi-Res Audio; USB-C audio; no 3.5 mm jack reported", "Hi-Res Audio; USB-C; no 3.5 mm jack", key="sound", status="VERIFIED_SECONDARY"),
        f("sensors", p, "Accelerometer, ambient-light sensor, proximity sensor, e-compass, in-display fingerprint sensor, gyroscope", "Accelerometer; ambient light; proximity; e-compass; in-display fingerprint; gyroscope"),
        f("color_options", p, "Stardust Black and Sunshine Gold", "Stardust Black; Sunshine Gold"),
    ]
    if storage == 128:
        data.append(f("local_configuration_issue", "vivo_v23_revu_ph",
                      "The PH product specs list 8 GB / 128 GB; Revu reports 12 GB / 256 GB as the lone local launch variant",
                      None, status="CONFLICTING_INFORMATION",
                      note="Keep 8 GB / 128 GB as a manufacturer-listed configuration, but do not claim it was sold locally or assign it the launch price."))
    return data


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row["id"] == DEVICE), None)
    if not device or device.get("workbookRow") != 106 or device.get("brand") != "vivo" or device.get("model") != "V23":
        raise SystemExit("Catalog target guard failed for workbook row 106 vivo V23")
    if len(device.get("variants", [])) != 1 or not device["variants"][0]["id"].endswith("-unrecorded"):
        raise SystemExit("Expected the original unrecorded configuration placeholder before review")

    manual["records"] = [row for row in manual["records"] if row["deviceId"] != DEVICE]
    variant_specs = [
        {"id": CONFIG_8_128, "label": "8 GB RAM / 128 GB storage", "modelCode": "V2130", "sku": None,
         "notes": "Listed on the official vivo Philippines specification page. Local press coverage conflicts on whether this configuration was sold at the 2022 launch; current retail availability and price are not verified."},
        {"id": CONFIG_12_256, "label": "12 GB RAM / 256 GB storage", "modelCode": "V2130", "sku": None,
         "notes": "Philippine launch configuration reported at PHP 27,999; current price is not verified."},
    ]
    availability = {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Official vivo Philippines V23 5G page and authorized-store launch reports establish local model availability from February 2022; 12 GB / 256 GB is the price-verified launch SKU.",
        "philippineAvailability": "NTC lists vivo V2130 as V23 5G. vivo Philippines product specifications list 8 GB / 128 GB and 12 GB / 256 GB. Philippine launch coverage and the dated PHP 27,999 price consistently establish 12 GB / 256 GB; Revu describes it as the lone launch configuration, so local sale/price for 8 GB / 128 GB remains unresolved. Current stock and price are not verified.",
        "observedAt": OBSERVED,
        "qualityFlag": "Workbook row 106 matched to NTC model V2130 / V23 5G. Both RAM/storage options are listed by vivo Philippines; Philippine launch price and local sale evidence are clear for 12/256 only. Current price, 8/128 retail availability, exact current OS policy, brightness, ingress rating and image reuse rights remain unresolved. Workbook scope remains Pending.",
        "catalogModel": "V23 5G", "manufacturer": "vivo", "productLine": "V Series",
        "modelNumber": "V2130", "philippineReleaseYear": 2022,
        "philippineDateLabel": "Official Philippine launch date",
        "researchNotes": "Workbook row 106 vivo V23 maps exactly to the Philippine NTC V2130 entry named V23 5G. vivo's Philippine specification page lists 8 GB / 128 GB and 12 GB / 256 GB; the local launch evidence and PHP 27,999 price specifically establish 12 GB / 256 GB, while Revu calls that the sole launch variant. The 8 GB / 128 GB variant remains visible as manufacturer-listed with unresolved Philippine retail availability and no assigned price. PHP 27,999 is historical, not current. Color-specific body dimensions and weights are kept separately. Official product images match both finishes, but reuse permission is not recorded. Workbook eligibility remains Pending.",
        "openIssues": [
            {"issue": "vivo PH lists 8 GB / 128 GB, while a Philippine launch report says 12 GB / 256 GB was the lone local SKU", "action": "Keep 8 GB / 128 GB separate and visible as manufacturer-listed; do not claim local sale or copy the 12 GB / 256 GB price."},
            {"issue": "No current dated, orderable Philippine price verified", "action": "Keep current price blank; preserve PHP 27,999 only as historical 12 GB / 256 GB launch pricing."},
            {"issue": "Dimensions and weight differ between Stardust Black and Sunshine Gold", "action": "Display both color-specific values instead of one collapsed measurement."},
            {"issue": "Kimovil's international 12 GB / 256 GB page says NFC is absent and claims IP65, while vivo PH lists NFC and no IP rating", "action": "Use vivo's Philippine NFC specification; leave IP rating unresolved."},
            {"issue": "No exact NanoReview V23 5G page was located in this research pass", "action": "Use the exact vivo, NTC, GSMArena and Kimovil records that were verified; do not add a generic NanoReview link as model evidence."},
            {"issue": "vivo official product imagery is exact-model, but image reuse rights are not established", "action": "Keep the neutral image placeholder and retain both official asset URLs."},
            {"issue": "Workbook eligibility is Pending", "action": "Preserve the existing study-scope status."},
        ],
    }

    reviewed_sources = sources()
    for index, (config_id, ram, storage) in enumerate(((CONFIG_8_128, 8, 128), (CONFIG_12_256, 12, 256))):
        item = {
            "deviceId": DEVICE, "configurationId": config_id, "brand": "vivo", "model": "V23 5G",
            "configuration": f"{ram} GB RAM / {storage} GB storage", "modelCode": "V2130",
            "sources": reviewed_sources, "fields": fields(ram, storage),
            "availabilityEvidence": availability,
        }
        if index == 0:
            item["replacementVariants"] = variant_specs
            item["replaceUnrecordedPlaceholder"] = True
        add_review(manual, catalog, item)
        if index == 0:
            device["variants"] = [{"id": row["id"], "specs": {}} for row in variant_specs]

    deduplicate_target_reviews(manual, {(DEVICE, CONFIG_8_128), (DEVICE, CONFIG_12_256)})
    manual["reviewedAt"] = OBSERVED
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "The official vivo Philippines product/specification pages link images that match both V23 5G finishes, but a reusable license or permission to republish was not found. Keep the neutral placeholder.",
        "sourcePage": URL_VIVO_PH_SPECS, "assetUrl": IMAGE_BLACK,
        "relatedAssetUrls": [IMAGE_GOLD],
        "scope": "vivo V23 5G V2130; official Stardust Black and Sunshine Gold product images",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for vivo V23 5G",
    }
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "vivo", "model_name": "V23 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC GEC lists V2130 as vivo V23 5G."},
            {"device_id": DEVICE, "source_url": URL_VIVO_PH_SPECS, "result": "vivo Philippines lists 8/128 and 12/256 configurations; actual local launch SKU evidence is strongest for 12/256."},
            {"device_id": DEVICE, "source_url": URL_PTG, "result": "PTG reports PHP 27,999 official Philippine price for 12/256 and local store availability on 12 February 2022."},
            {"device_id": DEVICE, "source_url": URL_REVU, "result": "Revu reports 12/256 as the lone local launch variant; 8/128 PH retail availability remains unresolved."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA_REVIEW, "result": "Exact-model review cross-checks global platform, display, camera, battery and configurations."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL_12_256, "result": "Exact 12/256 profile confirms V2130 and UFS 3.1; international NFC/IP assertions are not used to override local manufacturer specifications."},
        ],
        "prices": [{
            "device_id": DEVICE, "amount_php": 27999, "configuration_id": CONFIG_12_256,
            "configuration_match": "philippine_v2130_12gb_256gb", "variant_ram_gb": 12, "variant_storage_gb": 256,
            "price_type": "historical_ph_launch_price", "source_published_at": "2022-02-12",
            "excerpt": "Pinoy Techno Guide reports the vivo V23 5G 12 GB / 256 GB at PHP 27,999 as its official Philippine price on 12 February 2022; historical launch price, not a current offer.",
            "source_url": URL_PTG, "source_kind": "historical_local_price_candidate",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_price_not_current",
        }],
    }
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "vivo V23 5G", "workbookRow": 106, "modelCode": "V2130",
                      "configurations": ["8 GB / 128 GB (local sale unresolved)", "12 GB / 256 GB (local launch verified)"],
                      "sources": len(reviewed_sources), "fieldAssessmentsPerConfiguration": [len(fields(8, 128)), len(fields(12, 256))],
                      "historicalPricePhp": 27999, "currentPrice": None, "imageRights": "unestablished"}, indent=2))


if __name__ == "__main__":
    main()
