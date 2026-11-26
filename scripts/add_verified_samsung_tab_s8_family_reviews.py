#!/usr/bin/env python3
"""Review exact Philippine Samsung Galaxy Tab S8 family SKUs and evidence."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews, f, pending, src

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGE_UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/samsung-galaxy-tab-s8-family-ph-prices-2026-11-26.json"
OBSERVED = "2026-11-26"

SOURCES = {
    "global_launch": src(
        "samsung_tab_s8_global_launch",
        "https://www.samsungmobilepress.com/articles/after-record-breaking-preorders-samsung-announces-global-availability-of-new-galaxy-s22-series-and-galaxy-tab-s8-series",
        "Official Samsung global announcement and initial global availability",
        "Samsung Mobile Press says the series was announced on 9 February 2022 and began availability in markets worldwide on 25 February 2022. The global availability date is recorded separately from the Philippine preorder date.",
        publisher="Samsung Mobile Press", published="2022-02-25",
    ),
    "global_specs": src(
        "samsung_tab_s8_official_family_specs",
        "https://www.samsung.com/uk/support/mobile-devices/galaxy-tab-s8-vs-s8-vs-s8-ultra-comparison/",
        "Official Samsung comparison for shared model-family specifications",
        "Samsung's comparison page reports its technical table as correct as of February 2022 and distinguishes Wi-Fi and 5G model weights and connectivity. Accessed 2026-11-26.",
        publisher="Samsung UK",
    ),
    "global_newsroom": src(
        "samsung_tab_s8_global_newsroom",
        "https://news.samsung.com/global/breaking-the-rules-with-galaxy-tab-s8-series-the-biggest-boldest-most-versatile-galaxy-tablet-ever",
        "Official Samsung product announcement: design materials and launch features",
        "Samsung's Galaxy Tab S8 series announcement describes Armor Aluminum casing and the family design; used for model-family material information.",
        publisher="Samsung Global Newsroom", published="2022-02-09",
    ),
    "global_wifi_specs": src(
        "samsung_tab_s8_official_wifi_spec_sheet",
        "https://image-us.samsung.com/SamsungUS/samsungbusiness/pdfs/spec-sheet/Galaxy_Tab_S8_S8plus_Spec_Sheet_Wi-Fi.pdf",
        "Official Samsung Wi-Fi specifications for Galaxy Tab S8 and S8+",
        "Samsung product sheet lists the Snapdragon 8 Gen 1, CPU configuration, launch OS, memory, storage, microSD, display and other Wi-Fi model specifications. Used only for shared hardware facts, not as Philippine SKU evidence.",
        publisher="Samsung Electronics America",
        published="2022-02",
    ),
    "ph_launch": src(
        "samsung_tab_s8_yugatech_ph_launch",
        "https://www.yugatech.com/personal-computing/samsung-galaxy-tab-s8-ultra-full-specs-price-philippines/",
        "Independent Philippine launch coverage: local preorder, availability, configuration and price claims",
        "YugaTech's 9 February 2022 launch report lists 8/256 Wi-Fi and 5G Tab S8, 8/256 5G S8+, and 12/256 5G S8 Ultra with PHP prices; it says preorder began 9 February and broad retail availability began 4 March 2022.",
        publisher="YugaTech", published="2022-02-09",
    ),
    "alt_launch": src(
        "samsung_tab_s8_gizguide_ph_launch",
        "https://www.gizguide.com/2022/02/samsung-galaxy-tab-s8-series-launch.html",
        "Independent Philippine launch report reviewed for competing base Tab S8 configuration claims",
        "GizGuide lists the base Tab S8 as 8/128 at PHP 41,990 and 12/256 at PHP 49,990. Those additional configuration claims do not identify Philippine Samsung SKU codes and are retained as unresolved candidate evidence, not added as verified local configurations.",
        publisher="GizGuide", published="2022-02-09",
    ),
    "ntc": src(
        "samsung_tab_s8_ntc_2022_gec",
        "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf",
        "Philippine type approval cross-check for 5G model codes",
        "The NTC 2022 GEC lists SM-X706B as Galaxy Tab S8 5G, SM-X806B as Galaxy Tab S8+ 5G, and SM-X906B as Galaxy Tab S8 Ultra 5G. It is regulatory identity evidence, not proof of retail sale by itself.",
        publisher="National Telecommunications Commission Philippines",
    ),
}

MODEL_PAGES = {
    "s8_wifi": {
        "url": "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s8-wifi-pink-gold-256gb-sm-x700nidbxtc/",
        "publisher": "Samsung Philippines",
        "purpose": "Official Philippine Galaxy Tab S8 Wi-Fi SKU, configuration, product details and specifications",
        "note": "Exact Samsung Philippines product page for SM-X700NIDBXTC, Galaxy Tab S8 Wi-Fi, 8 GB RAM / 256 GB storage.",
    },
    "s8_5g": {
        "url": "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s8-5g-silver-256gb-sm-x706bzsbxtc/",
        "publisher": "Samsung Philippines",
        "purpose": "Official Philippine Galaxy Tab S8 5G SKU, configuration, product details and specifications",
        "note": "Exact Samsung Philippines product page for SM-X706BZSBXTC, Galaxy Tab S8 5G, 8 GB RAM / 256 GB storage.",
    },
    "s8plus_5g": {
        "url": "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s8-plus-5g-graphite-256gb-sm-x806bzabxtc/",
        "publisher": "Samsung Philippines",
        "purpose": "Official Philippine Galaxy Tab S8+ 5G SKU, configuration, product details and specifications",
        "note": "Exact Samsung Philippines product page for SM-X806BZABXTC, Galaxy Tab S8+ 5G, 8 GB RAM / 256 GB storage.",
    },
    "s8ultra_5g": {
        "url": "https://www.samsung.com/ph/tablets/galaxy-tab-s/galaxy-tab-s8-ultra-5g-graphite-256gb-sm-x906bzaextc/",
        "publisher": "Samsung Philippines",
        "purpose": "Official Philippine Galaxy Tab S8 Ultra 5G SKU, configuration, product details and specifications",
        "note": "Exact Samsung Philippines product page for SM-X906BZAEXTC, Galaxy Tab S8 Ultra 5G, 12 GB RAM / 256 GB storage.",
    },
}

DEVICE_META = {
    "device_211eea228c21fc": {"model": "Galaxy Tab S8", "image": "device_211eea228c21fc"},
    "device_104702347ea1db": {"model": "Galaxy Tab S8+", "image": "device_104702347ea1db"},
    "device_b1f198b69a803a": {"model": "Galaxy Tab S8 Ultra", "image": "device_b1f198b69a803a"},
}

CONFIGS = [
    {
        "deviceId": "device_211eea228c21fc", "configurationId": "device_211eea228c21fc-sm-x700-8gb-256gb-wifi-ph",
        "model": "Galaxy Tab S8", "page": "s8_wifi", "modelCode": "SM-X700", "sku": "SM-X700NIDBXTC",
        "ram": 8, "storage": 256, "network": "Wi-Fi", "cellular": "Wi-Fi only",
        "label": "8 GB RAM / 256 GB storage · Wi-Fi", "price": 41990, "weight": 503,
        "battery": 8000, "display": 11.0, "resolution": "2560 x 1600", "panel": "TFT",
        "dimensions": "165.3 x 253.8 x 6.3 mm", "camera_front": "12 MP ultra-wide",
        "extra_candidate": True,
    },
    {
        "deviceId": "device_211eea228c21fc", "configurationId": "device_211eea228c21fc-sm-x706b-8gb-256gb-5g-ph",
        "model": "Galaxy Tab S8", "page": "s8_5g", "modelCode": "SM-X706B", "sku": "SM-X706BZSBXTC",
        "ram": 8, "storage": 256, "network": "5G", "cellular": "5G cellular",
        "label": "8 GB RAM / 256 GB storage · 5G", "price": 49990, "weight": 507,
        "battery": 8000, "display": 11.0, "resolution": "2560 x 1600", "panel": "TFT",
        "dimensions": "165.3 x 253.8 x 6.3 mm", "camera_front": "12 MP ultra-wide",
        "extra_candidate": True,
    },
    {
        "deviceId": "device_104702347ea1db", "configurationId": "device_104702347ea1db-sm-x806b-8gb-256gb-5g-ph",
        "model": "Galaxy Tab S8+", "page": "s8plus_5g", "modelCode": "SM-X806B", "sku": "SM-X806BZABXTC",
        "ram": 8, "storage": 256, "network": "5G", "cellular": "5G cellular",
        "label": "8 GB RAM / 256 GB storage · 5G", "price": 63990, "weight": 572,
        "battery": 10090, "display": 12.4, "resolution": "2800 x 1752", "panel": "Super AMOLED",
        "dimensions": "185 x 285 x 5.7 mm", "camera_front": "12 MP ultra-wide",
        "extra_candidate": False,
    },
    {
        "deviceId": "device_b1f198b69a803a", "configurationId": "device_b1f198b69a803a-sm-x906b-12gb-256gb-5g-ph",
        "model": "Galaxy Tab S8 Ultra", "page": "s8ultra_5g", "modelCode": "SM-X906B", "sku": "SM-X906BZAEXTC",
        "ram": 12, "storage": 256, "network": "5G", "cellular": "5G cellular",
        "label": "12 GB RAM / 256 GB storage · 5G", "price": 77990, "weight": 728,
        "battery": 11200, "display": 14.6, "resolution": "2960 x 1848", "panel": "Super AMOLED",
        "dimensions": "208.6 x 326.4 x 5.5 mm", "camera_front": "12 MP wide + 12 MP ultra-wide",
        "extra_candidate": False,
    },
]


def model_source_for(key: str):
    row = MODEL_PAGES[key]
    return src(
        f"samsung_{key}_ph_specs", row["url"], row["purpose"], row["note"],
        publisher=row["publisher"],
    )


def add_conflicting_variant_claims(review_fields: list[dict]) -> None:
    field = next(row for row in review_fields if row["fieldId"] == "configuration")
    field["note"] = (
        "The exact Philippine Samsung SKU page verifies this 8 GB / 256 GB local configuration. "
        "GizGuide's February 2022 launch report separately lists 8/128 and 12/256 Tab S8 variants; "
        "no matching Philippine Samsung SKU was found for those extra claims, so they are retained "
        "as unresolved evidence and are not added as local configurations."
    )
    field["candidateEvidence"] = [
        {
            "value": "Samsung Galaxy Tab S8 8 GB / 128 GB; PHP 41,990",
            "unit": None,
            "sourceUrl": SOURCES["alt_launch"]["url"],
            "sourceKind": "independent_ph_reference",
            "observedAt": OBSERVED,
            "excerpt": "Samsung Galaxy Tab S8 8GB/128GB - PHP 41,990",
            "configurationMatch": "unmatched_additional_local_configuration_claim",
            "reviewStatus": "PENDING_VERIFICATION",
            "localAvailabilityVerified": False,
        },
        {
            "value": "Samsung Galaxy Tab S8 12 GB / 256 GB; PHP 49,990",
            "unit": None,
            "sourceUrl": SOURCES["alt_launch"]["url"],
            "sourceKind": "independent_ph_reference",
            "observedAt": OBSERVED,
            "excerpt": "Samsung Galaxy Tab S8 12GB/256GB - PHP 49,990",
            "configurationMatch": "unmatched_additional_local_configuration_claim",
            "reviewStatus": "PENDING_VERIFICATION",
            "localAvailabilityVerified": False,
        },
    ]


def review_records():
    launch_date = "2022-02-09"
    global_date = "2022-02-25"
    records = []
    for config in CONFIGS:
        device_id = config["deviceId"]
        spec_id = f"samsung_{config['page']}_ph_specs"
        sources = [
            model_source_for(config["page"]), SOURCES["global_launch"], SOURCES["global_newsroom"], SOURCES["global_specs"],
            SOURCES["global_wifi_specs"], SOURCES["ph_launch"], SOURCES["alt_launch"], SOURCES["ntc"],
        ]
        sources_by_id = {source["id"]: source for source in sources}
        fields = [
            f("model_number", spec_id, config["modelCode"], config["modelCode"],
              note="Samsung model code matched to the exact Philippine product page and local SKU."),
            f("configuration", spec_id, f"{config['ram']} GB RAM / {config['storage']} GB storage; {config['network']}", config["label"],
              note="Exact Philippine Samsung SKU page identifies the listed memory, storage and connectivity configuration."),
            f("global_release_date", "samsung_tab_s8_global_launch",
              "Announced 2022-02-09; global market availability began 2022-02-25", global_date,
              note="Samsung's global press notice says the family began availability in markets worldwide on 25 February 2022; the 9 February announcement date is retained in the source note."),
            f("philippine_release_date", "samsung_tab_s8_yugatech_ph_launch",
              "Philippine preorder began 2022-02-09; broad retail availability began 2022-03-04", launch_date,
              status="VERIFIED_SECONDARY", note="Local preorder launch date, not an exact first-sale transaction. The same source states broad availability through Samsung stores and authorized retailers from 4 March 2022."),
            f("display_size", spec_id, f"{config['display']} inches", config["display"], key="displayInches", unit="in"),
            f("display_technology", spec_id, config["panel"], config["panel"], key="displayType"),
            f("display_resolution", spec_id, config["resolution"], config["resolution"], key="resolution"),
            f("display_refresh_rate", "samsung_tab_s8_official_family_specs", "120 Hz", 120, key="refreshHz", unit="Hz"),
            f("chipset", "samsung_tab_s8_official_family_specs", "Snapdragon 8 Gen 1 (SM8450)", "Qualcomm Snapdragon 8 Gen 1", key="chipset"),
            f("process_node", "samsung_tab_s8_official_family_specs", "4 nm", 4, unit="nm"),
            f("cpu", "samsung_tab_s8_official_family_specs", "Octa-core: 1x 2.99 GHz, 3x 2.4 GHz, 4x 1.7 GHz", "Octa-core, 1 × 2.99 GHz + 3 × 2.4 GHz + 4 × 1.7 GHz"),
            f("operating_system", "samsung_tab_s8_official_family_specs", "Android 12; One UI 4.1", "Android 12 (One UI 4.1)", key="os"),
            f("ram_capacity", spec_id, f"{config['ram']} GB", config["ram"], key="ramGb", unit="GB"),
            f("storage_capacity", spec_id, f"{config['storage']} GB", config["storage"], key="storageGb", unit="GB"),
            f("storage_expansion", spec_id, "MicroSD up to 1 TB", "microSD supported up to 1 TB"),
            f("rear_camera_system", spec_id, "13 MP main camera + 6 MP ultra-wide rear camera", "13 MP autofocus main + 6 MP ultra-wide", key="rearCameraMp"),
            f("ultrawide_camera", spec_id, "6 MP ultra-wide rear camera", "6 MP ultra-wide rear camera"),
            f("telephoto_camera", spec_id, "Official rear camera specification lists a 13 MP main and 6 MP ultra-wide module only", "No telephoto rear camera", status="NOT_APPLICABLE"),
            f("front_camera", spec_id, config["camera_front"], config["camera_front"], key="frontCameraMp", unit="MP",
              note="For the Ultra, the catalog's numeric frontCameraMp field represents the primary 12 MP module; the review records both front modules."),
            f("video_recording", spec_id, "UHD 4K (3840 × 2160) at 30 fps", "Rear video up to 4K/30 fps", key="video"),
            f("battery_capacity", spec_id, f"{config['battery']:,} mAh typical", config["battery"], key="batteryMah", unit="mAh",
              note="Samsung identifies this as a typical capacity; its published rated/minimum capacity is lower."),
            f("wired_charging", "samsung_tab_s8_official_family_specs", "45 W Super Fast Charging", 45, key="chargingW", unit="W"),
            f("wireless_charging", "samsung_tab_s8_official_family_specs", "Wireless charging not supported", "Not supported"),
            f("dimensions", "samsung_tab_s8_official_family_specs", config["dimensions"], config["dimensions"], key="dimensions", unit="mm"),
            f("weight", spec_id, f"{config['weight']} g", config["weight"], key="weightG", unit="g"),
            f("materials", "samsung_tab_s8_global_newsroom", "Armor Aluminum casing/frame", "Armor Aluminum casing/frame"),
            f("ingress_protection", "samsung_tab_s8_official_family_specs", "No IP certification / no protection listed", "No IP rating stated"),
            f("sim_esim", spec_id if config["network"] == "5G" else "samsung_tab_s8_official_family_specs",
              "Single nano-SIM (4FF), tray shared with microSD" if config["network"] == "5G" else "Wi-Fi-only model; no SIM", "Single nano-SIM and microSD shared tray" if config["network"] == "5G" else "No SIM; Wi-Fi only", key="sim"),
            f("cellular_bands", spec_id,
              "2G GSM 850/900/1800/1900; 3G UMTS bands 1/2/4/5/8; 4G FDD LTE bands 1/2/3/4/5/7/8/12/13/17/20/25/26/28/32/66; TDD LTE 38/40/41; 5G Sub-6 FDD n1/3/5/7/8/20/28/66 and TDD n38/40/41/77/78" if config["network"] == "5G" else "Not applicable: Wi-Fi-only model",
              "Philippine model's listed 2G/3G/4G LTE and 5G Sub-6 bands" if config["network"] == "5G" else "Not applicable: Wi-Fi-only model",
              status="VERIFIED" if config["network"] == "5G" else "NOT_APPLICABLE"),
            f("tablet_cellular_variant", spec_id, config["cellular"], config["cellular"], key="cellular"),
            f("wifi", spec_id, "Wi-Fi 6E; 802.11 a/b/g/n/ac/ax, 2.4/5/6 GHz", "Wi-Fi 6E", key="wifi"),
            f("bluetooth", spec_id, "Bluetooth 5.2", "Bluetooth 5.2"),
            f("usb", spec_id, "USB Type-C; USB 3.2 Gen 1", "USB Type-C, USB 3.2 Gen 1", key="ports"),
            f("nfc", spec_id, "NFC: No", "No NFC"),
            f("gnss", spec_id, "GPS, GLONASS, BeiDou, Galileo, QZSS", "GPS, GLONASS, BeiDou, Galileo, QZSS"),
            f("audio", spec_id, "Quad speakers tuned by AKG; Dolby Atmos", "Quad speakers; AKG tuning; Dolby Atmos", key="sound"),
            f("sensors", spec_id, "Accelerometer, fingerprint sensor, gyro sensor, geomagnetic sensor, Hall sensor, light sensor", "Accelerometer; fingerprint; gyroscope; geomagnetic; Hall; light sensors"),
            f("tablet_stylus", spec_id, "S Pen included in box", "S Pen included"),
            f("tablet_keyboard", spec_id, "Book Cover Keyboard accessory supported; sold separately as standard", "Book Cover Keyboard supported; sold separately", key="keyboard",
              note="Accessory compatibility is distinct from the time-limited local preorder promotions that bundled selected keyboards."),
        ]
        # The catalog stores the primary front-camera megapixel count as a
        # number; the audit retains the source's fuller module description.
        next(row for row in fields if row["fieldId"] == "front_camera")["catalogValue"] = 12
        next(row for row in fields if row["fieldId"] == "rear_camera_system")["catalogValue"] = 13

        fields.extend([
            f("official_launch_price_php", "samsung_tab_s8_yugatech_ph_launch",
              f"PHP {config['price']:,} launch price for the exact {config['label']} configuration",
              config["price"], status="VERIFIED_SECONDARY", unit="PHP",
              note="Historical Philippine launch price reported by YugaTech on 9 February 2022. This is not a current offer."),
            pending("current_price_php", spec_id,
                    "No dated current Philippine price was displayed in the consulted Samsung product listing.",
                    "Current price remains unrecorded; the official product information page is not a dated, currently purchasable offer. Historical launch price is kept in its separate field.", "PHP"),
        ])

        if config["extra_candidate"]:
            add_conflicting_variant_claims(fields)

        replacement_variants = [
            {"id": c["configurationId"], "label": c["label"], "sku": c["sku"], "modelCode": c["modelCode"],
             "notes": "Exact Philippines Samsung product page identifies the local configuration."}
            for c in CONFIGS if c["deviceId"] == device_id
        ]
        item = {
            "deviceId": device_id, "configurationId": config["configurationId"],
            "brand": "Samsung", "model": config["model"], "configuration": config["label"],
            "modelCode": config["modelCode"], "sku": config["sku"],
            "sources": list(sources_by_id.values()), "fields": fields,
            "replacementVariants": replacement_variants,
            "availabilityEvidence": {
                "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                "availabilityStatus": "Philippine launch reported; preorder began 2022-02-09 and authorized retail availability began 2022-03-04.",
                "philippineAvailability": "Samsung Philippines lists an exact local SKU. YugaTech reports Samsung Store and authorized dealer availability from 2022-03-04. This verifies a Philippine market configuration, not a current stock or price guarantee.",
                "observedAt": OBSERVED,
                "philippineReleaseYear": 2022,
                "philippineDateLabel": "Philippine preorder launch",
                "catalogModel": config["model"],
                "qualityFlag": "Local model and configuration reviewed; workbook selected-scope status remains Pending.",
                "openIssues": [
                    {"issue": "The inventory workbook's selected-scope status is Pending.", "action": "Retain Pending; availability research does not authorize eligibility changes."},
                    {"issue": "No dated current Philippine price is established.", "action": "Keep the current price blank and display the dated historical launch price separately."},
                ],
            },
        }
        records.append(item)
    return records


def price_snapshot():
    prices = []
    for config in CONFIGS:
        prices.append({
            "device_id": config["deviceId"], "configuration_id": config["configurationId"],
            "amount_php": config["price"], "variant_ram_gb": config["ram"],
            "variant_storage_gb": config["storage"], "configuration_match": config["label"],
            "price_type": "historical_ph_launch_price", "source_published_at": "2022-02-09",
            "excerpt": f"YugaTech reports PHP {config['price']:,} for {config['model']} {config['label']}; historical launch price, not a current offer.",
            "source_url": SOURCES["ph_launch"]["url"], "source_kind": "historical_local_price_candidate",
            "observed_at": OBSERVED, "local_availability_verified": True,
            "availability_status": "historical_price_not_current", "review_status": "VERIFIED_SECONDARY",
        })
    return {
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 3,
        "models": [
            {"device_id": device_id, "brand": "Samsung", "model_name": meta["model"],
             "category": "tablets", "status": "manually_reviewed"}
            for device_id, meta in DEVICE_META.items()
        ],
        "fetches": [], "observations": [],
        "discovery": [
            {"device_id": config["deviceId"], "source_url": MODEL_PAGES[config["page"]]["url"],
             "result": f"Official Samsung Philippines SKU {config['sku']} matched to {config['label']}."}
            for config in CONFIGS
        ] + [
            {"device_id": "device_211eea228c21fc", "source_url": SOURCES["alt_launch"]["url"],
             "result": "GizGuide lists additional 8/128 and 12/256 base Tab S8 claims without exact Philippine SKUs; these remain unresolved and are not added as configurations."},
            {"device_id": "device_211eea228c21fc", "source_url": SOURCES["ntc"]["url"],
             "result": "NTC 2022 GEC model-code match checked for the three 5G models; regulatory evidence is not treated as sale evidence."},
        ],
        "prices": prices,
    }


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    records = review_records()
    variants_replaced = set()
    for item in records:
        add_review(manual, catalog, item)
        if item["deviceId"] in variants_replaced:
            stored = next(r for r in manual["records"]
                          if r["deviceId"] == item["deviceId"] and r["configurationId"] == item["configurationId"])
            stored.pop("replacementVariants", None)
        else:
            variants_replaced.add(item["deviceId"])
    deduplicate_target_reviews(manual, {(r["deviceId"], r["configurationId"]) for r in records})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICE_SNAPSHOT.write_text(json.dumps(price_snapshot(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    unavailable = json.loads(IMAGE_UNAVAILABLE.read_text(encoding="utf-8"))
    for device_id in ("device_104702347ea1db", "device_b1f198b69a803a"):
        current = unavailable.get(device_id, {})
        current.update({
            "status": "REUSE_PERMISSION_REQUIRED",
            "reason": "Samsung Philippines has an exact-model product image, but Samsung's site terms do not establish a license to republish that image in this catalog. The neutral placeholder remains until reuse permission is secured.",
            "sourcePage": MODEL_PAGES["s8plus_5g" if device_id == "device_104702347ea1db" else "s8ultra_5g"]["url"],
            "assetUrl": None,
            "scope": "Exact model",
            "rightsTermsUrl": "https://www.samsung.com/ph/business/info/legal/",
            "observedAt": OBSERVED,
            "altText": f"Image unavailable for {DEVICE_META[device_id]['model']}",
        })
        unavailable[device_id] = current
    IMAGE_UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"tabletModelsReviewed": len(DEVICE_META), "exactPhilippineConfigurations": len(records),
                      "reviewedAt": OBSERVED, "selectedScopeChanged": False}, indent=2))


if __name__ == "__main__":
    main()
