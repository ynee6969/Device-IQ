#!/usr/bin/env python3
"""Add a source-backed Philippine review for the Moto G50 inventory row."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/moto-g50-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_195cb093808ae0"
OLD_CONFIG = f"{DEVICE}-unrecorded"

URL_GLOBAL = "https://motorolanews.com/blazing-fast-5g-speed-with-the-new-moto-g50-5g/"
URL_MOTO_DOC = "https://en-us.support.motorola.com/app/answers/detail/a_id/167829/~/declarations-of-conformity"
URL_NTC_GEC = "https://caraga.ntc.gov.ph/wp-content/uploads/2021/11/GEC_09302021.pdf"
URL_MOTO_SUPPORT = "https://en-us.support.motorola.com/app/answers/detail/a_id/160450/p/689"
URL_MOTO_MANUAL = "https://help.motorola.com/hc/3255/12/pdf/help-moto-g50-5g-12-global-en-us.pdf"
URL_YUGA = "https://www.yugatech.com/mobile/motorola-moto-g50-5g-specs-price-philippines-2/"
URL_UNBOX = "https://unbox.ph/gadget/motorola-announces-official-price-for-the-moto-g50-5g-in-the-philippines/"
URL_GIZGUIDE = "https://www.gizguide.com/2021/08/moto-g50-5g-price-specs-ph.html"
URL_MEDIATEK = "https://i.mediatek.com/dimensity-700"
URL_GIGAHERTZ = "https://www.gigahertz.com.ph/products/motorola-moto-g50-5g"
URL_IMAGE = "https://www.gigahertz.com.ph/cdn/shop/files/CEL-LENOVOMOTOG505GPAR70005PH_4_128GB_METEORITEGRAY.jpg?v=1730777829&width=1080"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("moto_g50_5g_motorola_global", "Motorola News", URL_GLOBAL,
           "Manufacturer global introduction, product-family technical facts, and global date",
           "Motorola's August 20, 2021 press release introduces the moto g50 5G and describes its 90 Hz 6.5-inch HD+ display, 48 MP triple-camera system, 5,000 mAh battery, Android 11, Dimensity 700, LPDDR4X, UFS 2.2, and storage/microSD options. Regional features and the Philippine 4/128 GB launch configuration are checked against local sources.",
           "2021-08-20"),
    source("moto_g50_5g_motorola_doc", "Motorola Support", URL_MOTO_DOC,
           "Manufacturer mapping between the XT2149-1 model code and moto g50 5G",
           "Motorola's declarations of conformity list XT2149-1 as moto g50 5G and separately identify XT2137-1 as moto g50. This distinction is central to matching the Philippine Dimensity 700 device to the workbook's shorter Moto G50 label."),
    source("moto_g50_5g_ntc_gec", "National Telecommunications Commission (NTC)", URL_NTC_GEC,
           "Philippine Grant of Equipment Conformity record for XT2149-1",
           "The 2021 NTC GEC lists Motorola XT2149-1 as a smartphone/mobile phone under Motorola Mobility LLC, record ESD-GEC-2106805, dated July 6, 2021. The GEC row supplies regulatory model-code evidence; Motorola's DoC supplies the marketing-name mapping.",
           "2021-07-06"),
    source("moto_g50_5g_motorola_support", "Motorola Support", URL_MOTO_SUPPORT,
           "Exact-model hardware layout and port/sensor confirmation",
           "Motorola's moto g50 5G support page labels the SIM/SD tray, proximity sensor, Google Assistant button, side fingerprint/power key, rear macro/main/depth cameras, 3.5 mm headset jack, USB-C connector, and speaker."),
    source("moto_g50_5g_motorola_manual", "Motorola Support", URL_MOTO_MANUAL,
           "Manufacturer user's guide for model-specific hardware and use",
           "Motorola's model-specific user guide illustrates the SIM/SD tray, fingerprint/power key, rear camera roles, USB-C port, speaker, and headset jack. It does not state a Philippine cellular-band table or a formal IP rating."),
    source("moto_g50_5g_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine-market availability, exact local configuration, historical price, and local specifications",
           "Published August 30, 2021. YugaTech says the Moto G50 5G is available in the Philippines and lists the 4/128 GB configuration at PHP 10,495, plus local display, chipset, camera, connectivity, battery, dimensions, weight, and color specifications.",
           "2021-08-30"),
    source("moto_g50_5g_unbox_ph", "Unbox PH", URL_UNBOX,
           "Independent Philippine launch/date and official price confirmation",
           "Published August 30, 2021. Unbox reports the Moto G50 5G's Philippine price and local 4/128 GB specification; it distinguishes the Philippine Dimensity 700 variant from the earlier Snapdragon 480 Moto G50.",
           "2021-08-30"),
    source("moto_g50_5g_gizguide_ph", "GizGuide Philippines", URL_GIZGUIDE,
           "Contemporaneous local launch, price, build, colors, and specification cross-check",
           "Published August 30, 2021. GizGuide reports the Philippine launch, PHP 10,495 price, Meteorite Grey and Green colors, glasstic construction, display, chipset, camera, RAM/storage, and battery details.",
           "2021-08-30"),
    source("mediatek_dimensity_700", "MediaTek", URL_MEDIATEK,
           "Primary Dimensity 700 process, CPU, and GPU platform specifications",
           "MediaTek lists the Dimensity 700 as a 7 nm platform with 2 Cortex-A76 cores up to 2.2 GHz, 6 Cortex-A55 cores up to 2.0 GHz, and Mali-G57 MC2 graphics. These are chipset-level properties, not independent proof of the handset's local SKU."),
    source("moto_g50_5g_gigahertz_ph", "GigaHertz Philippines", URL_GIGAHERTZ,
           "Dated exact-variant Philippine retailer price and branch pickup availability",
           "Observed November 26, 2026. The selected listing is Motorola Moto G50 5G, Gray, 4 GB RAM + 128 GB storage at PHP 10,899; pickup is shown available at multiple Philippine branches. Condition is not stated. The listing's lower technical-specification table links to and reproduces a different Motorola handset's data, so this source is used only for the selected title, configuration, price, and branch availability—not for device specifications."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, catalog_value="__normalized__", unit=None, note: str,
          configuration_match: str,
          price_condition="__absent__", price_type=None,
          price_observed_at=None, listing_status=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": configuration_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value == "__normalized__" else catalog_value
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


def fields_for() -> list[dict]:
    match = "Philippine XT2149-1 launch configuration: 4 GB RAM / 128 GB storage"
    out = []

    def add(fid, sid, value, normalized, **kwargs):
        out.append(field(fid, sid, value, normalized, configuration_match=match, **kwargs))

    add("model_number", "moto_g50_5g_ntc_gec", "NTC GEC: Motorola XT2149-1; Motorola DoC maps XT2149-1 to moto g50 5G", "XT2149-1", status="VERIFIED", note="Philippine GEC model code and manufacturer marketing-name mapping agree. Motorola lists XT2137-1 separately as the non-5G moto g50.")
    add("global_release_date", "moto_g50_5g_motorola_global", "Motorola introduced the moto g50 5G globally on August 20, 2021", "2021-08-20", status="VERIFIED", note="Manufacturer announcement date; this is distinct from the reported Philippine launch/availability date of August 30, 2021.")
    add("configuration", "moto_g50_5g_yugatech_ph", "Philippine launch configuration: 4 GB RAM / 128 GB storage", "4 GB RAM / 128 GB storage", status="VERIFIED_SECONDARY", note="This is the configuration reported for the local Moto G50 5G launch and selected independently on the dated GigaHertz listing. It is not merged with the separate XT2137-1 Moto G50 variant.")
    add("philippine_release_date", "moto_g50_5g_yugatech_ph", "YugaTech reports the Moto G50 5G was available in the Philippines in its August 30, 2021 article", "2021-08-30", status="VERIFIED_SECONDARY", note="Contemporaneous local report date and availability statement; not a claim about the first individual sale transaction.")
    add("official_launch_price_php", "moto_g50_5g_unbox_ph", "Philippine launch price PHP 10,495 for 4 GB / 128 GB", 10495, unit="PHP", status="VERIFIED_SECONDARY", note="Historical Philippine price corroborated by YugaTech and GizGuide; it is not a current price.")
    add("current_price_php", "moto_g50_5g_gigahertz_ph", "Selected Gray 4 GB / 128 GB GigaHertz listing PHP 10,899; pickup available at multiple branches; condition not stated", 10899, unit="PHP", status="VERIFIED_SECONDARY", price_condition=None, price_type=f"GigaHertz Philippines selected-variant listing observed {OBSERVED}; condition not stated", price_observed_at=OBSERVED, listing_status="In stock", note="Dated exact-configuration offer. The retailer's product page shows branch pickup availability for the selected item; its technical-specification section contains mismatched data and is not used for specifications.")
    add("display_size", "moto_g50_5g_yugatech_ph", "6.5-inch display", 6.5, key="displayInches", unit="in", note="Philippine-market specifications give a 6.5-inch Max Vision panel.")
    add("display_technology", "moto_g50_5g_yugatech_ph", "IPS LCD display", "IPS LCD", key="displayType", note="Local specification identifies the panel as IPS LCD.")
    add("display_resolution", "moto_g50_5g_yugatech_ph", "HD+ 1600 x 720 pixels", "720 x 1600", key="resolution", note="Exact resolution from the Philippine launch specification.")
    add("display_refresh_rate", "moto_g50_5g_yugatech_ph", "90 Hz refresh rate", 90, key="refreshHz", unit="Hz", note="Manufacturer and local Philippine sources both describe a 90 Hz panel.")
    add("display_brightness", "moto_g50_5g_motorola_global", "No peak or typical brightness figure stated in the reviewed manufacturer or local launch pages", None, status="NOT_DISCLOSED", note="No brightness value is inferred from panel type or marketing descriptions.")
    add("display_protection", "moto_g50_5g_motorola_manual", "Display protection material or grade not stated in the reviewed manufacturer manual", None, status="NOT_DISCLOSED", note="No Gorilla Glass or other protective material is assumed.")
    add("chipset", "moto_g50_5g_yugatech_ph", "MediaTek Dimensity 700 5G", "MediaTek Dimensity 700", key="chipset", note="The Philippine XT2149-1 device uses Dimensity 700. The earlier Moto G50 XT2137-1 is a different Snapdragon 480 product and is not substituted.")
    add("process_node", "mediatek_dimensity_700", "7 nm process", "7 nm", status="VERIFIED", unit="nm", note="MediaTek's primary platform specification; chipset property, not a phone manufacturing process.")
    add("cpu", "mediatek_dimensity_700", "Octa-core: 2 x Cortex-A76 up to 2.2 GHz + 6 x Cortex-A55 up to 2.0 GHz", "2 x Cortex-A76 up to 2.2 GHz + 6 x Cortex-A55 up to 2.0 GHz", key="cpu", status="VERIFIED", note="MediaTek's primary Dimensity 700 specification.")
    add("gpu", "moto_g50_5g_yugatech_ph", "Arm Mali-G57 MC2", "Mali-G57 MC2", key="gpu", note="Local launch specification names this GPU; MediaTek's platform page independently confirms the chipset GPU family.")
    add("operating_system", "moto_g50_5g_motorola_global", "Android 11 at launch", "Android 11", key="os", status="VERIFIED", note="Motorola's manufacturer introduction identifies Android 11 as the launch software.")
    add("os_support", "moto_g50_5g_motorola_support", "No model-specific OS or security update duration found in reviewed support sources", None, status="NOT_DISCLOSED", note="No duration or upgrade promise is asserted.")
    add("ram_capacity", "moto_g50_5g_yugatech_ph", "4 GB RAM", 4, key="ramGb", unit="GB", note="Exact Philippine launch configuration.")
    add("ram_type", "moto_g50_5g_motorola_global", "LPDDR4X memory", "LPDDR4X", status="VERIFIED", note="Motorola's manufacturer product introduction names LPDDR4X; the exact PH capacity remains sourced from YugaTech.")
    add("storage_capacity", "moto_g50_5g_yugatech_ph", "128 GB storage", 128, key="storageGb", unit="GB", note="Exact Philippine launch configuration.")
    add("storage_type", "moto_g50_5g_motorola_global", "UFS 2.2 2-lane storage", "UFS 2.2", status="VERIFIED", note="Manufacturer product introduction names UFS 2.2; the 128 GB capacity is the local configuration.")
    add("storage_expansion", "moto_g50_5g_yugatech_ph", "microSD card support up to 1 TB in a hybrid SIM tray", "microSD up to 1 TB; hybrid tray", status="VERIFIED_SECONDARY", note="Philippine launch source states up to 1 TB; Motorola's user guide confirms the shared SIM/SD tray. A second active SIM and microSD card cannot both use the hybrid tray at the same time.")
    add("rear_camera_system", "moto_g50_5g_yugatech_ph", "48 MP f/1.7 main + 2 MP f/2.4 macro + 2 MP f/2.4 depth", "48 MP main + 2 MP macro + 2 MP depth", key="rearCameraMp", catalog_value=48, note="Local Philippine configuration's three listed rear modules; the catalog's numeric rear-camera filter represents the main camera resolution.")
    add("main_camera_sensor", "moto_g50_5g_motorola_global", "Motorola describes a 48 MP Quad Pixel sensor; no sensor part number is stated", "48 MP Quad Pixel sensor; part number not recorded", status="VERIFIED", note="No exact sensor manufacturer or part number is inferred.")
    add("ultrawide_camera", "moto_g50_5g_yugatech_ph", "No ultrawide camera is listed in the three-module local rear-camera system", "No ultrawide module listed", status="NOT_APPLICABLE", note="The local specification lists main, macro, and depth modules only.")
    add("telephoto_camera", "moto_g50_5g_yugatech_ph", "No telephoto camera is listed in the three-module local rear-camera system", "No telephoto module listed", status="NOT_APPLICABLE", note="The local specification lists main, macro, and depth modules only.")
    add("front_camera", "moto_g50_5g_yugatech_ph", "13 MP f/2.2 front camera", 13, key="frontCameraMp", unit="MP", note="Local Philippine launch specification.")
    add("video_recording", "moto_g50_5g_motorola_support", "Specific rear and front video resolution/frame-rate modes are not listed in the reviewed manufacturer support source", None, status="NOT_DISCLOSED", note="No recording modes are inferred from the image sensor or chipset capability.")
    add("battery_capacity", "moto_g50_5g_yugatech_ph", "5,000 mAh battery", 5000, key="batteryMah", unit="mAh", note="Manufacturer and Philippine launch sources report 5,000 mAh.")
    add("battery_technology", "moto_g50_5g_motorola_global", "Cell chemistry and internal battery construction not stated in the reviewed manufacturer source", None, status="NOT_DISCLOSED", note="No lithium-polymer or cell-layout detail is inferred.")
    add("wired_charging", "moto_g50_5g_yugatech_ph", "15 W wired charging", 15, key="chargingW", unit="W", note="Philippine-market specification.")
    add("wireless_charging", "moto_g50_5g_motorola_manual", "Wireless or reverse charging not stated in the reviewed model manual", None, status="NOT_DISCLOSED", note="No support is assumed from silence in the manual.")
    add("dimensions", "moto_g50_5g_yugatech_ph", "167 x 76.4 x 9.26 mm", "167 x 76.4 x 9.26 mm", key="dimensions", unit="mm", note="Local launch specification corroborated by contemporaneous Philippine coverage and exact XT2149-1 technical references.")
    add("weight", "moto_g50_5g_yugatech_ph", "206 g", 206, key="weightG", unit="g", note="Local launch specification corroborated by exact-model technical references.")
    add("materials", "moto_g50_5g_gizguide_ph", "3D curved glasstic exterior; specific frame material not stated", "3D curved glasstic exterior; frame material not recorded", note="Local launch coverage uses the term glasstic; frame material is left unspecified.")
    add("ingress_protection", "moto_g50_5g_yugatech_ph", "Water-repellent design is mentioned; no formal IP rating is given", "Water-repellent design; IP rating not recorded", status="VERIFIED_SECONDARY", note="A design description is not converted into an IP certification.")
    add("sim_esim", "moto_g50_5g_yugatech_ph", "Dual Nano-SIM; microSD uses the hybrid SIM/SD tray; eSIM not stated", "Dual Nano-SIM; hybrid SIM/SD tray; eSIM not recorded", key="sim", note="Local source and Motorola hardware guide support dual SIM and shared tray; no eSIM support is claimed.")
    add("cellular_bands", "moto_g50_5g_yugatech_ph", "4G LTE and 5G; exact Philippine XT2149-1 cellular band set not established", "4G LTE / 5G; exact local bands not recorded", key="cellular", note="Local source confirms network generations. Regional band lists are not substituted for the Philippine unit.")
    add("wifi", "moto_g50_5g_yugatech_ph", "Wi-Fi 802.11 a/b/g/n/ac", "Wi-Fi 5 (802.11 a/b/g/n/ac)", key="wifi", note="Local model specification identifies Wi-Fi 5 capability.")
    add("bluetooth", "moto_g50_5g_yugatech_ph", "Bluetooth 5.0", "Bluetooth 5.0", note="Philippine launch specification.")
    add("usb", "moto_g50_5g_motorola_support", "USB-C port for charging and data; exact USB data generation not stated", "USB-C; data generation not recorded", key="ports", status="VERIFIED", note="Motorola support confirms USB-C charging/data port without a protocol generation.")
    add("nfc", "moto_g50_5g_yugatech_ph", "NFC listed", "Yes", note="Philippine launch specification.")
    add("gnss", "moto_g50_5g_yugatech_ph", "GPS, A-GPS, LTEPP", "GPS, A-GPS, LTEPP", note="Only the location systems named by the local source are recorded.")
    add("audio", "moto_g50_5g_motorola_support", "Single speaker and 3.5 mm headset jack", "Single speaker; 3.5 mm headset jack", key="sound", status="VERIFIED", note="Motorola's hardware page/manual shows the speaker and headset jack; local launch coverage also lists the 3.5 mm jack.")
    add("sensors", "moto_g50_5g_motorola_support", "Proximity sensor and side-mounted fingerprint sensor are identified; full sensor list not recorded", "Proximity sensor; side fingerprint reader; other sensors not recorded", status="VERIFIED", note="Model-specific Motorola hardware guide confirms these controls/sensors; no complete sensor inventory is inferred.")

    if len(out) != 46:
        raise ValueError(f"Expected 46 reviewed phone fields, got {len(out)}")
    return out


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "motorola"
            or device.get("model") != "Moto G50"):
        raise ValueError("Inventory row no longer matches Motorola Moto G50")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != OLD_CONFIG:
        raise ValueError("Expected the original unrecorded configuration placeholder")
    if any(row.get("deviceId") == DEVICE for row in manual.get("records", [])):
        raise ValueError("Moto G50 already has a manual review; inspect it before replacing")

    config_id = f"{DEVICE}-4gb-128gb-ph"
    label = "4 GB RAM / 128 GB storage"
    review = {
        "deviceId": DEVICE, "configurationId": config_id,
        "brand": "Motorola", "model": "Moto G50",
        "configuration": label, "configurationLabel": label,
        "sources": SOURCES, "fields": fields_for(),
        "replacementVariants": [{
            "id": config_id, "label": label, "sku": None,
            "modelCode": "XT2149-1",
            "notes": "Philippine Moto G50 5G launch configuration. Motorola identifies XT2149-1 as moto g50 5G; NTC GEC records this model code in the Philippines. Distinct from the earlier XT2137-1 Moto G50 with Snapdragon 480.",
        }],
        "replaceUnrecordedPlaceholder": True,
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Philippine availability reported August 30, 2021; NTC GEC records Motorola XT2149-1 and Motorola maps XT2149-1 to moto g50 5G.",
            "philippineAvailability": "YugaTech and other Philippine launch coverage report the Moto G50 5G with 4 GB RAM / 128 GB storage available locally at PHP 10,495. NTC GEC confirms Philippine conformity record ESD-GEC-2106805 for XT2149-1; Motorola's DoC maps XT2149-1 to moto g50 5G. The workbook row's shorter Moto G50 label is retained while the Philippine model match is explicitly identified as Moto G50 5G. Workbook scope remains Pending.",
            "observedAt": OBSERVED,
            "manufacturer": "Motorola Mobility",
            "productLine": "Moto G50 5G",
            "modelNumber": "XT2149-1",
            "philippineReleaseYear": 2021,
            "philippineDateLabel": "Reported Philippine launch/availability date",
            "researchNotes": "The workbook row is labeled Moto G50. Philippine launch sources identify the locally available device as Moto G50 5G, 4 GB / 128 GB, MediaTek Dimensity 700. Motorola's official DoC maps XT2149-1 to moto g50 5G and separately maps XT2137-1 to the non-5G-suffixed moto g50; the NTC GEC records Philippine model XT2149-1. This review therefore matches the workbook row to the specific Philippine Moto G50 5G record and does not import the Snapdragon 480 specification of XT2137-1. Motorola's global introduction was August 20, 2021; local sources report availability and PHP 10,495 launch pricing on August 30. On November 26, 2026, GigaHertz showed the exact Gray 4/128 selection for PHP 10,899 with pickup available at multiple Philippine branches; item condition was not stated. The retailer's technical details below the offer contain a different phone's specifications and are excluded from this review. An exact-model product image is available on the retailer page, but reuse permission is not stated; the neutral placeholder remains. The inventory scope label stays Pending.",
            "qualityFlag": "Philippine model matched as Moto G50 5G / XT2149-1; current listing condition not stated; image reuse rights not established; workbook scope remains Pending",
            "openIssues": [
                {"issue": "Workbook label omits the 5G suffix; the Philippines launch model is XT2149-1 Moto G50 5G, distinct from XT2137-1 Moto G50", "action": "Keep the regional model-code mapping and processor distinction visible in product details."},
                {"issue": "GigaHertz does not state the condition of its selected 4/128 listing", "action": "Keep condition as Not recorded while showing the dated exact-variant price and branch pickup status."},
                {"issue": "GigaHertz technical-specification table contains another handset's data", "action": "Use that page only for its exact selected title, configuration, price, and local pickup availability; do not use it for specifications."},
                {"issue": "The GigaHertz product image has no stated reusable-image license", "action": "Keep the neutral placeholder unless image reuse permission is documented."},
                {"issue": "An exact Philippine cellular-band set and model-specific software-update duration were not found", "action": "Leave those fields unrecorded rather than substituting a regional band table or assuming an update policy."},
                {"issue": "Workbook eligibility remains Pending", "action": "Do not change the study scope status based on local availability evidence."},
            ],
        },
    }
    manual["records"].append(review)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "An exact Motorola Moto G50 5G 4 GB / 128 GB Meteorite Gray image is available on the retailer page, but no reusable image license or permission is stated.",
        "sourcePage": URL_GIGAHERTZ, "assetUrl": URL_IMAGE,
        "scope": "Exact Moto G50 5G / XT2149-1, Meteorite Gray; listing configuration is 4 GB RAM / 128 GB storage",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Motorola Moto G50",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 10495, "configuration_id": config_id,
         "configuration_match": "exact", "variant_ram_gb": 4, "variant_storage_gb": 128,
         "price_type": "historical_ph_launch_price", "source_published_at": "2021-08-30",
         "excerpt": "Philippine launch reports list PHP 10,495 for the Moto G50 5G 4 GB / 128 GB configuration; historical price, not a current offer.",
         "source_url": URL_YUGA, "source_kind": "historical_ph_launch_price_report",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_ph_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 10899,
         "configuration_id": config_id, "configuration_match": "exact",
         "variant_ram_gb": 4, "variant_storage_gb": 128,
         "price_type": "current_ph_retailer_listing_condition_not_stated",
         "source_published_at": None,
         "excerpt": "GigaHertz selected Gray 4 GB RAM / 128 GB Storage listing was PHP 10,899; pickup available at multiple Philippine branches. Item condition not stated.",
         "source_url": URL_GIGAHERTZ, "source_kind": "exact_variant_ph_retailer_price_observation",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "pickup_available_at_listed_ph_branches"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Motorola", "model_name": "Moto G50", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [], "discovery": [], "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "modelMatch": "Moto G50 workbook row -> Philippine Moto G50 5G / XT2149-1",
        "configuration": "4/128 GB",
        "reviewedFields": len(review["fields"]),
        "globalAnnouncement": "2021-08-20",
        "philippineAvailability": "2021-08-30",
        "launchPricePhp": 10495,
        "currentPricePhp": 10899,
        "currentPriceCondition": "not stated",
        "image": unavailable[DEVICE]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
