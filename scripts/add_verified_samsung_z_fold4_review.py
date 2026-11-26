#!/usr/bin/env python3
"""Record exact Philippine Galaxy Z Fold4 variants and source-backed specifications."""
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
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-z-fold4-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"
DEVICE = "device_63467ee4825c94"
MODEL_CODE = "SM-F936B/DS"
URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_PH_AVAILABILITY = "https://www.samsung.com/ph/explore/entertainment/galaxy-z-fold4-new-fold-phone-2022/"
URL_PH_NEWSROOM = "https://news.samsung.com/ph/the-future-of-foldables-is-now-samsungs-galaxy-z-flip4-and-z-fold4-are-now-up-for-grabs"
URL_PH_PRODUCT = "https://www.samsung.com/ph/smartphones/galaxy-z/galaxy-z-fold4-phantom-black-256gb-sm-f936bzkdphl/buy/"
URL_SAMSUNG_PRESS = "https://samsungmobilepress.com/articles/introducing-samsung-galaxy-z-flip4-and-galaxy-z-fold4-the-most-versatile-devices-changing-the-way-we-interact-with-smartphones"
URL_YUGATECH = "https://www.yugatech.com/mobile/samsung-galaxy-z-fold4-z-flip4-price-philippines/"
URL_GSMARENA = "https://www.gsmarena.com/samsung_galaxy_z_fold4-11737.php"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-samsung-galaxy-z-fold4"
IMAGE_URL = "https://images.samsung.com/is/image/samsung/p6pim/ph/2208/gallery/ph-galaxy-z-fold4-f936-sm-f936bzkdphl-533084749?$1164_776_PNG$="

CONFIGS = [
    {"storage": 256, "price": 98990, "id": f"{DEVICE}-12gb-256gb-ph", "online": False},
    {"storage": 512, "price": 105990, "id": f"{DEVICE}-12gb-512gb-ph", "online": False},
    {"storage": 1024, "price": 119990, "id": f"{DEVICE}-12gb-1tb-ph", "online": True},
]


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
        src("samsung_fold4_ntc_2022", "National Telecommunications Commission", URL_NTC,
            "Exact Philippine equipment-registration model match",
            "The 2022 GEC identifies SAMSUNG model SM-F936B/DS as Galaxy Z Fold4.", "2022"),
        src("samsung_fold4_ph_availability", "Samsung Philippines", URL_PH_AVAILABILITY,
            "Philippine release date and local launch context",
            "Samsung Philippines states the Galaxy Z Fold4 became available from 2 September 2022. This is a local market availability date, distinct from the global announcement and selected-market release dates."),
        src("samsung_fold4_ph_newsroom", "Samsung Newsroom Philippines", URL_PH_NEWSROOM,
            "Philippine authorized availability, configuration-specific SRPs, and local colors",
            "Samsung Newsroom Philippines reports the Fold4 was orderable through Samsung, authorized stores, major retailers, and Globe and Smart partners; lists PHP 98,990 / 105,990 / 119,990 SRPs for 256 GB / 512 GB / online-exclusive 1 TB; and names local color options. The September 2022 promotions in the article have expired.", "2022-09-06"),
        src("samsung_fold4_ph_product", "Samsung Philippines Official Store", URL_PH_PRODUCT,
            "Local product identity, storage selector, exact 256 GB image asset, and current sale-state check",
            "The local product page identifies the Phantom Black 256 GB SM-F936BZKDPHL SKU, presents 12 GB/256 GB, 12 GB/512 GB and 12 GB/1 TB choices, and currently marks the product not for sale. The page image is an exact Fold4 256 GB Phantom Black image; no reusable image permission is documented."),
        src("samsung_fold4_global_specs", "Samsung Mobile Press", URL_SAMSUNG_PRESS,
            "Manufacturer launch specification table for the Galaxy Z Fold4 family",
            "Samsung's 10 August 2022 press materials list the Fold4's display panels, camera modules, 12 GB memory tiers, battery, charging, IPX8, launch OS, connectivity, SIM capabilities, colors, dimensions and weight. Market-dependent features are retained with their caveats.", "2022-08-10"),
        src("samsung_fold4_yugatech_ph", "YugaTech Philippines", URL_YUGATECH,
            "Independent Philippine launch/date and SRP cross-check",
            "YugaTech reports Philippine availability from 2 September 2022 and the three local prices. This corroborates Samsung's local launch materials; it does not establish a current offer.", "2022-08-10"),
        src("samsung_fold4_gsmarena", "GSMArena", URL_GSMARENA,
            "Independent exact-model technical cross-check",
            "The exact Galaxy Z Fold4 page is used only to cross-check the 12 GB memory family, 256/512/1 TB storage tiers, battery, camera, IPX8, and charging figures. GSMArena's international retailer prices are not Philippine prices, and dimensions are not used where source precision differs."),
        src("samsung_fold4_kimovil", "Kimovil", URL_KIMOVIL,
            "Independent model-family and regional-variant cross-check",
            "Kimovil identifies the Galaxy Z Fold4 global SM-F936B family and multiple memory/storage variants. Country-specific listing prices and regional model variants are not treated as Philippine evidence."),
    ]


def shared_fields() -> list[dict]:
    sp = "samsung_fold4_global_specs"
    gs = "samsung_fold4_gsmarena"
    return [
        f("model_number", "samsung_fold4_ntc_2022", "Philippine NTC model SM-F936B/DS", MODEL_CODE,
          note="NTC's 2022 GEC marketing-name column directly identifies this model code as Galaxy Z Fold4."),
        f("display_size", sp, "Main screen 7.6 in; cover screen 6.2 in", 7.6,
          key="displayInches", unit="in", note="The public numeric field stores the main screen diagonal; the separate cover screen size is preserved in sourceValue."),
        f("display_technology", sp, "Dynamic AMOLED 2X main and cover displays", "Dynamic AMOLED 2X", key="displayType"),
        f("display_resolution", sp, "Main: 2176 x 1812; cover: 2316 x 904", "Main 2176 x 1812; cover 2316 x 904", key="resolution"),
        f("display_refresh_rate", sp, "Main adaptive 1–120 Hz; cover adaptive 48–120 Hz", 120, key="refreshHz", unit="Hz",
          note="Catalog numeric value is the maximum refresh rate. The two panels have different adaptive ranges."),
        f("display_brightness", sp, "Samsung describes the main display as brighter; this table gives no numeric brightness", None,
          status="PENDING_VERIFICATION", unit="nits", note="No numeric brightness value is recorded because the reviewed primary launch specification does not give one."),
        f("chipset", sp, "Qualcomm Snapdragon 8+ Gen 1 Mobile Platform", "Qualcomm Snapdragon 8+ Gen 1", key="chipset"),
        f("cpu", sp, "4 nm octa-core application processor", "Octa-core, 4 nm", key="cpu"),
        f("gpu", gs, "Adreno 730", "Qualcomm Adreno 730", key="gpu", status="VERIFIED_SECONDARY",
          note="Secondary exact-model reference; Samsung's launch page does not enumerate the GPU separately."),
        f("operating_system", sp, "Android 12L with One UI 4.1.1 at launch", "Android 12L / One UI 4.1.1", key="os"),
        f("rear_camera_system", sp, "50 MP wide + 12 MP ultra-wide + 10 MP telephoto", "50 MP wide + 12 MP ultra-wide + 10 MP telephoto", key="rearCameraMp",
          note="The public field retains all rear cameras as text; Samsung's camera table provides each module separately."),
        f("main_camera_sensor", sp, "50 MP wide; Dual Pixel AF, OIS, f/1.8", "50 MP; Dual Pixel AF; OIS; f/1.8"),
        f("ultrawide_camera", sp, "12 MP, f/2.2, 123-degree field of view", "12 MP; f/2.2; 123°"),
        f("telephoto_camera", sp, "10 MP, PDAF, OIS, f/2.4; 3x optical zoom", "10 MP; PDAF; OIS; f/2.4; 3x optical zoom"),
        f("front_camera", sp, "10 MP cover camera plus 4 MP under-display camera", "10 MP cover + 4 MP under-display", key="frontCameraMp",
          note="Numeric catalog field stores the cover selfie camera; source value retains the separate under-display camera."),
        f("storage_type", gs, "UFS 3.1", "UFS 3.1", key="storageType", status="VERIFIED_SECONDARY",
          note="Exact-model secondary cross-check; Samsung's reviewed launch table does not name the flash storage standard."),
        f("battery_capacity", sp, "4,400 mAh typical dual battery; 4,275 mAh rated minimum", 4400, key="batteryMah", unit="mAh",
          note="Samsung distinguishes typical and minimum rated capacities; catalog stores the stated typical value."),
        f("wired_charging", sp, "Super Fast Charging with 25 W adapter or higher; adapter sold separately", 25, key="chargingW", unit="W"),
        f("wireless_charging", sp, "Fast Wireless Charging 2.0; Wireless PowerShare", "Fast wireless charging; reverse wireless charging"),
        f("wireless_charging_watts", gs, "15 W fast wireless charging", 15, key="wirelessChargingW", unit="W", status="VERIFIED_SECONDARY",
          note="GSMArena exact-model cross-check; Samsung's press materials name Fast Wireless Charging 2.0 without a watt figure."),
        f("dimensions", sp, "Folded 67.1 x 155.1 x 15.8–14.2 mm; unfolded 130.1 x 155.1 x 6.3 mm", "Folded 67.1 x 155.1 x 15.8–14.2 mm; unfolded 130.1 x 155.1 x 6.3 mm", key="dimensions", unit="mm"),
        f("weight", sp, "263 g", 263, key="weightG", unit="g"),
        f("materials", sp, "Armor Aluminum frame and hinge cover; Gorilla Glass Victus+ on cover screen and rear glass", "Armor Aluminum; Gorilla Glass Victus+ cover/rear; reinforced foldable main panel"),
        f("ingress_protection", sp, "IPX8 water resistance; not dust-resistant", "IPX8; not dust-resistant"),
        f("cellular_bands", sp, "5G and LTE; network support varies by market and carrier", "5G; LTE", key="cellular"),
        f("sim_esim", sp, "Up to two Nano-SIM cards and one eSIM; availability varies by region and carrier", "Up to 2 Nano-SIM + 1 eSIM; regional support varies", key="sim"),
        f("wifi", sp, "Wi-Fi 6E (802.11 a/b/g/n/ac/ax); availability varies by market", "Wi-Fi 6E", key="wifi"),
        f("bluetooth", sp, "Bluetooth 5.2", "Bluetooth 5.2"),
        f("nfc", sp, "Not enumerated in the reviewed exact-model launch specification", None, status="PENDING_VERIFICATION",
          note="This is left blank; no regional NFC claim was promoted from an unrelated variant."),
        f("sensors", sp, "Side capacitive fingerprint, accelerometer, barometer, gyro, geomagnetic, Hall, proximity, light", "Side fingerprint; accelerometer; barometer; gyroscope; geomagnetic; Hall; proximity; light"),
        f("video_recording", sp, "No maximum recording mode specified in the reviewed launch specification table", None,
          status="PENDING_VERIFICATION", note="Video resolution and frame rates remain blank pending an exact regional primary specification."),
        f("os_support", sp, "No support end date stated in the launch specification", None, status="PENDING_VERIFICATION",
          note="A current support period is not inferred from later update availability or generic Samsung policy."),
    ]


def build_records() -> list[dict]:
    source_rows = sources()
    shared = shared_fields()
    result = []
    replacement = [{
        "id": item["id"], "label": f"12 GB RAM / {item['storage'] // 1024} TB storage" if item["storage"] == 1024 else f"12 GB RAM / {item['storage']} GB storage",
        "modelCode": MODEL_CODE, "sku": None,
        "notes": ("Online-exclusive Philippine 1 TB capacity; color-specific SKU not assigned."
                  if item["online"] else "Philippine configuration; color-specific SKU not assigned."),
    } for item in CONFIGS]
    for i, item in enumerate(CONFIGS):
        storage = item["storage"]
        label = f"12 GB RAM / {storage // 1024} TB storage" if storage == 1024 else f"12 GB RAM / {storage} GB storage"
        fields = [
            f("configuration", "samsung_fold4_ph_product", label,
              note="Samsung Philippines lists this exact RAM/storage tier in its local product selector."),
            f("ram_capacity", "samsung_fold4_ph_product", "12 GB RAM", 12, key="ramGb", unit="GB"),
            f("storage_capacity", "samsung_fold4_ph_product", f"{storage} GB internal storage", storage, key="storageGb", unit="GB"),
            f("global_release_date", "samsung_fold4_global_specs", "Announced 10 August 2022; general availability began 26 August in selected countries", "2022-08-26",
              note="Manufacturer-reported general-availability date for selected countries, not the Philippine release date."),
            f("philippine_release_date", "samsung_fold4_ph_availability", "Samsung Philippines reports launch availability beginning 2 September 2022", "2022-09-02",
              note="Philippine local availability; preorder and global announcement dates are recorded separately in sources."),
            f("official_launch_price_php", "samsung_fold4_ph_newsroom", f"Philippine SRP for {storage} GB: PHP {item['price']:,}", item["price"], unit="PHP",
              note="Historical September 2022 Philippine SRP published by Samsung Newsroom Philippines; not a current offer."),
            f("current_price_php", "samsung_fold4_ph_product", "No current dated, orderable Philippine offer verified; page states not for sale", None,
              status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank. The 2022 SRP is historical, not a current price."),
            *shared,
        ]
        review = {
            "deviceId": DEVICE, "configurationId": item["id"], "brand": "Samsung",
            "model": "Galaxy Z Fold4", "configuration": label, "configurationLabel": label,
            "modelCode": MODEL_CODE, "sources": source_rows, "fields": fields,
            "availabilityEvidence": {
                "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                "availabilityStatus": "Philippine official and authorized-channel availability documented from 2 September 2022",
                "philippineAvailability": (
                    "Samsung Philippines lists a 2 September 2022 local release. Samsung Newsroom confirms the device was available through Samsung, authorized stores, major retailers, and telco partners. "
                    "The documented local configurations are 12 GB/256 GB (PHP 98,990), 12 GB/512 GB (PHP 105,990), and online-exclusive 12 GB/1 TB (PHP 119,990), all historical launch SRPs. Samsung lists Gray Green and Phantom Black locally and an online-exclusive Beige 256 GB option; storage/color pairings are not inferred beyond those explicit statements. Current stock and price are not verified."
                ),
                "observedAt": OBSERVED,
                "qualityFlag": "Exact NTC SM-F936B/DS match; three Philippine storage tiers and historical SRPs documented; current price and image reuse rights unresolved; study scope remains Pending.",
                "catalogModel": "Galaxy Z Fold4",
                "manufacturer": "Samsung Electronics Co., Ltd.",
                "productLine": "Galaxy Z Series",
                "modelNumber": MODEL_CODE,
                "philippineReleaseYear": 2022,
                "philippineDateLabel": "Philippine local release date",
                "researchNotes": (
                    "Workbook row 101's Samsung Z Fold4 claim matches NTC GEC model SM-F936B/DS. Samsung Philippines documents a 2 September 2022 local launch and three configurations: 12/256 at PHP 98,990, 12/512 at PHP 105,990, and online-exclusive 12/1 TB at PHP 119,990. These are historical SRPs, not current offers. Samsung lists Gray Green and Phantom Black locally and an online-exclusive Beige 256 GB option; storage/color pairings are not inferred beyond explicit statements. Exact-model technical specifications are sourced to Samsung's launch table, with secondary GSMArena cross-checks kept identified as such. Current price is blank because the local product page says not for sale and no current dated offer was verified. Product image reuse rights are not established, so the neutral placeholder remains. Workbook eligibility remains Pending."
                ),
                "openIssues": [
                    {"issue": "No current dated, orderable Philippine price was verified", "action": "Keep all current-price fields blank; retain launch SRPs as historical evidence."},
                    {"issue": "Samsung's exact product image is available, but reuse permission is not recorded", "action": "Keep the neutral placeholder until a reusable license or written permission is established."},
                    {"issue": "Numeric display brightness, NFC, video recording modes, and support end date are not established by the reviewed exact-model primary specifications", "action": "Show these fields as not recorded until exact-model evidence is found."},
                    {"issue": "Workbook study scope is Pending", "action": "Preserve the original workbook eligibility status."},
                ],
            },
        }
        if i == 0:
            review["replacementVariants"] = replacement
            review["replaceUnrecordedPlaceholder"] = True
        result.append(review)
    return result


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    images = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row["id"] == DEVICE), None)
    if not device or device.get("workbookRow") != 101 or device.get("model") not in {"Z Fold4", "Galaxy Z Fold4"}:
        raise SystemExit("Catalog target guard failed for workbook row 101 Samsung Z Fold4")
    items = build_records()
    target_keys = {(item["deviceId"], item["configurationId"]) for item in items}
    manual["records"] = [row for row in manual["records"] if row["deviceId"] != DEVICE]
    for index, item in enumerate(items):
        add_review(manual, catalog, item)
        if index == 0 and item.get("replacementVariants"):
            device["variants"] = [
                {"id": variant["id"], "label": variant["label"], "specs": {},
                 "sku": variant.get("sku"), "modelCode": variant.get("modelCode")}
                for variant in item["replacementVariants"]
            ]
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Samsung Philippines provides an exact Galaxy Z Fold4 Phantom Black 256 GB product image, but the project has no reusable license or written permission to republish it. Keep the neutral placeholder.",
        "sourcePage": URL_PH_PRODUCT, "assetUrl": IMAGE_URL,
        "scope": "Exact Galaxy Z Fold4 model, Phantom Black 256 GB image; not a color-specific claim for other variants",
        "rightsTermsUrl": None, "observedAt": OBSERVED,
        "altText": "Image unavailable for Samsung Galaxy Z Fold4",
    }
    prices = []
    for item in CONFIGS:
        prices.append({
            "device_id": DEVICE, "amount_php": item["price"], "configuration_id": item["id"],
            "configuration_match": f"philippine_sm-f936b-ds_12gb_{item['storage']}gb",
            "variant_ram_gb": 12, "variant_storage_gb": item["storage"],
            "price_type": "historical_ph_launch_srp", "source_published_at": "2022-09-06",
            "excerpt": f"Samsung Newsroom Philippines lists the Galaxy Z Fold4 {item['storage']} GB configuration at PHP {item['price']:,} SRP in September 2022; historical, not current.",
            "source_url": URL_PH_NEWSROOM, "source_kind": "historical_local_price_candidate",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_price_not_current",
        })
    snapshot = {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Samsung", "model_name": "Galaxy Z Fold4", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "2022 NTC GEC lists SM-F936B/DS as Samsung Galaxy Z Fold4."},
            {"device_id": DEVICE, "source_url": URL_PH_NEWSROOM, "result": "Samsung Newsroom Philippines confirms local authorized-channel availability and three launch SRPs; 1 TB is online exclusive."},
            {"device_id": DEVICE, "source_url": URL_SAMSUNG_PRESS, "result": "Samsung Mobile Press supplies exact family technical specifications; market-specific variation caveats are retained."},
            {"device_id": DEVICE, "source_url": URL_GSMARENA, "result": "GSMArena exact-model technical cross-check; international prices and unresolved regional details are not promoted as Philippine data."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Kimovil exact model-family variant cross-check only; no Philippine pricing inferred."},
        ],
        "prices": prices,
    }
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE_IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": "Samsung Galaxy Z Fold4", "workbookRow": 101,
                      "configurations": len(CONFIGS), "sources": len(sources()),
                      "fieldAssessmentsPerConfiguration": len(build_records()[0]["fields"]),
                      "currentPrices": None, "imageRights": "unestablished"}, indent=2))


if __name__ == "__main__":
    main()
