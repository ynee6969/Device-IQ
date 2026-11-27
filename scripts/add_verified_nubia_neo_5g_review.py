#!/usr/bin/env python3
"""Record source-backed review for the ZTE nubia Neo 5G (8150N)."""
from __future__ import annotations

import json
from pathlib import Path

from add_verified_tablet_reviews import add_review, deduplicate_target_reviews

ROOT = Path(__file__).resolve().parents[1]
OBSERVED = "2026-11-27"
DEVICE = "device_03f3856685042e"
CONFIG = f"{DEVICE}-8gb-256gb"
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
IMAGES = ROOT / "research/catalog-image-unavailable.json"
LATEST_REVIEWED = ROOT / "research/enrichment/latest-reviewed-2026-11-27.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/nubia-neo-5g-ph-prices-2026-11-27.json"

URL_ZTE_GLOBAL = "https://www.ztedevices.com/en/products/smartphones/nubia/nubia-neo-5g.html"
URL_ZTE_MY = "https://www.ztedevices.com.my/nubia/nubia/nubia-neo-5g"
URL_ZTE_CERT = "https://download.ztedevices.com/bigmediafiles/device/global/certification/Smart_phone_2023/P0323_23ZTE0060_nubia_8150N/P0323_23ZTE0060_nubia_8150N_CE_DOC.pdf"
URL_GCF = "https://www.globalcertificationforum.org/pub_product/11895.html"
URL_UNISOC = "https://www.prnewswire.com/apac/news-releases/the-gaming-phone-nubia-neo-5g-launched-with-unisoc-t820-now-available-in-southeast-asia-301887151.html"
URL_THAIPR = "https://www.thaipr.net/en/it_en/3340989"
URL_REVU = "https://www.revu.com.ph/2023/09/zte-nubia-neo-5g-price-philippines/"
URL_YUGA = "https://www.yugatech.com/news/zte-nubia-neo-5g-available-in-lazada/"
URL_NOYPI = "https://www.noypigeeks.com/android/nubia-neo-5g-philippines/"
URL_GIZ = "https://www.gizguide.com/2023/09/zte-nubia-neo-5g-price-specs-official-philippines.html"
URL_UNBOX = "https://unbox.ph/gadget/zte-to-bring-nubia-neo-5g-to-the-philippines/"
URL_XATAKA = "https://www.xatakamovil.com/zte/zte-nubia-neo-5g-caracteristicas-precio-ficha-tecnica"
URL_CURRENT_CHECK = "https://www.lazada.com.ph/tag/zte-nubia-neo-5g-official-store/"
IMAGE_URL = "https://www.ztedevices.com.my/storage/products/2/page_contents/97a0aaa16359cb4ec441ae032f9c8bbd.jpg"


def src(sid: str, url: str, publisher: str, purpose: str, note: str,
        published: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": published, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    src("nubia_neo_zte_certificate", URL_ZTE_CERT, "ZTE Corporation",
        "Manufacturer declaration of conformity and model identity",
        "ZTE's signed declaration identifies product model nubia 8150N, MyOS13.0.0_8150N_AS1 and hardware version zatA; dated 2023-06-08. It establishes manufacturer model/software identity, not Philippine availability.", "2023-06-08"),
    src("nubia_neo_zte_global_product", URL_ZTE_GLOBAL, "ZTE Devices",
        "Official product overview and feature identity",
        "ZTE's official product page identifies the nubia Neo 5G, UNISOC T820, dual-SIM 5G, 22.5W charging, gaming features and design. Detailed specifications are cross-checked against ZTE's regional specification page."),
    src("nubia_neo_zte_malaysia_specs", URL_ZTE_MY, "ZTE Devices Malaysia",
        "Manufacturer specifications for the exact 8150N product family",
        "Official ZTE Malaysia page lists 8GB+10GB Fusion RAM (18GB advertised total), 256GB storage, UNISOC T820, Android 13, 6.6-inch FHD 120Hz display, 8MP front and 50MP+2MP rear cameras, 4500mAh battery, 22.5W charging, 163.7×75×7.98mm, dual SIM, dual-band Wi-Fi and NFC. Regional listing is not treated as proof of Philippine price or availability."),
    src("nubia_neo_gcf_model", URL_GCF, "Global Certification Forum",
        "Independent model-name, manufacturer and certified network-band match",
        "GCF entry 11895 maps ZTE Corporation model nubia 8150N to marketing name nubia Neo 5G and lists certified cellular bands. Certification date 2023-11-25. Band data describes the certified model and does not guarantee Philippine carrier compatibility.", "2023-11-25"),
    src("nubia_neo_unisoc_chipset", URL_UNISOC, "UNISOC via PR Newswire",
        "Chipset architecture and Southeast Asian launch timing",
        "UNISOC release dated 2023-07-27 states ZTE had launched the nubia Neo 5G in Southeast Asia and details the T820: 1× Cortex-A76 at 2.7GHz, 3× Cortex-A76 at 2.3GHz, 4× Cortex-A55 at 2.1GHz, Mali-G57 MP4 up to 850MHz and 6nm EUV process.", "2023-07-27"),
    src("nubia_neo_thai_launch", URL_THAIPR, "ZTE Device Thailand via ThaiPR.NET",
        "Earliest regional preorder month cross-check",
        "ZTE Device Thailand said preorders for the nubia Neo 5G would be available through online channels in June 2023. This establishes month-level regional preorder timing, not an exact first-sale day.", "2023-06"),
    src("nubia_neo_revu_ph", URL_REVU, "REVU Philippines",
        "Contemporaneous Philippine official-store sale, list price, promotion and configuration",
        "Article dated 2023-09-06 reports a live-sale observation of ZTE Philippines selling the nubia Neo 5G on TikTok Shop: PHP 9,999 list price and limited-time PHP 8,599 promotional price. It identifies 8GB physical RAM, 256GB storage, 8MP selfie camera, 50MP rear camera, 4500mAh battery and 22.5W charge.", "2023-09-06"),
    src("nubia_neo_yugatech_ph", URL_YUGA, "YugaTech",
        "Philippine marketplace listing, configuration and detailed specifications",
        "Article dated 2023-09-14 reports the 8GB/256GB nubia Neo 5G listed in Lazada Philippines for PHP 9,799. Its prose states 6.6-inch 120Hz IPS LCD and 8MP front camera; its spec table gives 6.73-inch, 2408×1080, LPDDR5x and UFS 3.1, so inconsistent entries from that page are not silently combined.", "2023-09-14"),
    src("nubia_neo_noypi_ph", URL_NOYPI, "NoypiGeeks",
        "Philippine price and independent specification cross-check",
        "Article dated 2023-09-11 reports PHP 9,999 SRP, 8GB/256GB, 6.6-inch FHD+ 120Hz display, 13MP front camera, 4500mAh and 22.5W. Its front-camera value conflicts with ZTE's product page and other contemporaneous PH launch sources; that field remains unresolved.", "2023-09-11"),
    src("nubia_neo_gizguide_ph", URL_GIZ, "GIZGUIDE",
        "Philippine retail pricing and local product specifications",
        "Article dated 2023-09-09 reports PHP 9,999 in ZTE's TikTok Shop listing, 6.67-inch/2400×1080/120Hz display, 8GB/256GB, 8MP front camera, 4500mAh and 22.5W. This pixel resolution conflicts with YugaTech's spec table.", "2023-09-09"),
    src("nubia_neo_unbox_prerelease", URL_UNBOX, "Unbox.ph",
        "Pre-release reporting retained to distinguish provisional estimates from final specifications",
        "August 2023 preview described 13MP selfie camera, 5000mAh and 33W charging before Philippine retail availability. These pre-release estimates are superseded by later ZTE product specifications and contemporaneous PH retail sources, and are not used as final configuration values.", "2023-08-28"),
    src("nubia_neo_xataka_specs", URL_XATAKA, "Xataka Móvil",
        "Independent exact-model specification and physical-weight cross-check",
        "Article dated 2024-02-13 identifies the nubia Neo 5G 8GB/256GB, lists a 189g weight, 6.6-inch LCD 120Hz display, 8MP front camera, 50MP+2MP rear cameras, Android 13, 4500mAh and 22.5W charging. It does not establish Philippine pricing or configuration-specific local availability.", "2024-02-13"),
    src("nubia_neo_current_listing_check", URL_CURRENT_CHECK, "Lazada Philippines",
        "Current exact-model price research",
        "Checked 2026-11-27. The current nubia official-store search results show newer Neo 5-series models, but no exact older nubia Neo 5G (8150N) listing or current PHP price. No current price is asserted from this non-matching search page."),
]


def f(fid: str, sid: str, value, normalized=None, *, status="VERIFIED",
      key: str | None = None, unit: str | None = None, note: str | None = None,
      catalog_value=None, price_type: str | None = None,
      price_observed: str | None = None, price_condition: str | None = None) -> dict:
    row = {"fieldId": fid, "status": status, "sourceId": sid,
           "sourceValue": value, "normalizedValue": normalized}
    if key:
        row.update({"catalogKey": key,
                    "catalogValue": normalized if catalog_value is None else catalog_value})
    if unit:
        row["unit"] = unit
    if note:
        row["note"] = note
    if price_type:
        row.update({"priceType": price_type, "priceObservedAt": price_observed,
                    "priceCondition": price_condition or "new"})
    return row


def nd(fid: str, sid: str, description: str, note: str | None = None) -> dict:
    return f(fid, sid, description, None, status="NOT_DISCLOSED",
             note=note or "The reviewed exact-model sources do not publish this value; it remains blank rather than inferred.")


def na(fid: str, sid: str, description: str, note: str) -> dict:
    return f(fid, sid, description, None, status="NOT_APPLICABLE", note=note)


def ev(value: str, url: str, source_kind: str, excerpt: str, match: str) -> dict:
    return {"value": value, "sourceUrl": url, "sourceKind": source_kind,
            "observedAt": OBSERVED, "excerpt": excerpt,
            "configurationMatch": match, "reviewStatus": "CONFLICTING_INFORMATION"}


def conflict(fid: str, sid: str, description: str, evidence: list[dict], note: str,
             key: str | None = None) -> dict:
    row = f(fid, sid, description, None, status="CONFLICTING_INFORMATION",
            key=key, catalog_value=None, note=note)
    row["candidateEvidence"] = evidence
    return row


def fields() -> list[dict]:
    resolution = conflict(
        "display_resolution", "nubia_neo_gizguide_ph",
        "Philippine sources list both 2400×1080 and 2408×1080; ZTE specifies only FHD.",
        [ev("2400 × 1080", URL_GIZ, "secondary_philippines", "GIZGUIDE reports FHD+ 2400 x 1080.", "nubia Neo 5G Philippine retail listing"),
         ev("2408 × 1080", URL_YUGA, "secondary_philippines", "YugaTech spec table reports 1080 x 2408.", "nubia Neo 5G Philippine Lazada listing")],
        "Exact pixel dimensions conflict between contemporaneous local specification listings. The manufacturer page confirms FHD only, so exact resolution is withheld.", key="resolution")
    ram_type = conflict(
        "ram_type", "nubia_neo_yugatech_ph",
        "YugaTech reports LPDDR5x while REVU lists LPDDR4X; ZTE does not state RAM type.",
        [ev("LPDDR5x", URL_YUGA, "secondary_philippines", "YugaTech specification table says 8GB LPDDR5x.", "8GB/256GB Philippine listing"),
         ev("LPDDR4X", URL_REVU, "secondary_philippines", "REVU specification table says 8GB LPDDR4X.", "8GB/256GB Philippine official-store sale")],
        "Local sources conflict on physical RAM generation; manufacturer documentation does not resolve it. The catalog records installed capacity only.", key="ramType")
    front_camera = conflict(
        "front_camera", "nubia_neo_revu_ph",
        "ZTE's manufacturer specification and several local reports state 8MP; NoypiGeeks reports 13MP.",
        [ev("8 MP", URL_ZTE_MY, "manufacturer_primary_regional", "Official ZTE product specification lists an 8MP front camera.", "Official nubia Neo 5G product page; model 8150N"),
         ev("8 MP", URL_REVU, "secondary_philippines", "Contemporaneous PH sale report says 8MP selfie sensor.", "8GB/256GB PH sale"),
         ev("8 MP", URL_YUGA, "secondary_philippines", "YugaTech prose and spec list say 8MP front camera.", "8GB/256GB Lazada PH listing"),
         ev("13 MP", URL_NOYPI, "secondary_philippines", "NoypiGeeks lists a 13MP front camera.", "PH listing dated 2023-09-11"),
         ev("13 MP", URL_UNBOX, "secondary_prerelease", "August pre-release preview estimated 13MP selfie camera.", "Pre-release PH preview; not confirmed final hardware")],
        "The published final manufacturer specification and multiple launch reports support 8MP, but a post-launch local source reports 13MP. Keep the normalized catalog value blank until the regional hardware is confirmed.", key="frontCameraMp")
    rows = [
        f("model_number", "nubia_neo_gcf_model", "ZTE manufacturer model nubia 8150N; GCF maps it to marketing name nubia Neo 5G", "8150N", status="VERIFIED_SECONDARY",
          note="ZTE's signed declaration names nubia 8150N; GCF independently maps model 8150N to nubia Neo 5G."),
        f("global_release_date", "nubia_neo_thai_launch", "ZTE Thailand announced online preorders in June 2023; UNISOC reported Southeast Asian launch on 2023-07-27", "2023-06", status="VERIFIED_SECONDARY",
          note="Month-level earliest regional preorder timing only; the first retail-sale day was not established. The July 2023 UNISOC release confirms subsequent Southeast Asian launch activity."),
        f("configuration", "nubia_neo_revu_ph", "Philippine ZTE shop listing: 8GB physical RAM / 256GB storage; up to 10GB additional Fusion/Dynamic RAM is software-backed", "8 GB RAM / 256 GB storage",
          note="All reviewed PH availability sources identify 8GB/256GB. The advertised 18GB total includes up to 10GB virtual/Fusion RAM and is not a second physical-RAM configuration."),
        f("philippine_release_date", "nubia_neo_revu_ph", "REVU observed ZTE Philippines selling the phone in a live TikTok Shop event on 2023-09-06; first exact day of sale is not otherwise established", "2023-09-06", status="VERIFIED_SECONDARY",
          note="This is the earliest verified Philippine sale observation located, not a claim that no earlier transaction occurred."),
        f("official_launch_price_php", "nubia_neo_revu_ph", "PHP 9,999 listed price on the official ZTE Philippines TikTok Shop live sale", 9999, status="VERIFIED_SECONDARY", unit="PHP",
          price_type="Historical Philippine official-store launch/list price", price_observed="2023-09-06",
          note="REVU's contemporaneous report observed ZTE Philippines selling the exact 8GB/256GB model at PHP 9,999. The report also records a time-limited PHP 8,599 promotion; neither is a current price."),
        f("current_price_php", "nubia_neo_current_listing_check", "No current Philippine price for exact model 8150N was located; current official-store search results show newer Neo 5-series models", None,
          status="UNAVAILABLE_AFTER_RESEARCH", unit="PHP",
          note="Checked 2026-11-27. Historical PH price observations remain dated and are not displayed as current. No current exact-model stock/list price is verified."),
        f("display_size", "nubia_neo_zte_malaysia_specs", "6.6-inch FHD display; local reports say 6.6 or 6.67 inches, while a YugaTech spec-table entry says 6.73 inches despite that article's prose saying 6.6 inches", 6.6, key="displayInches", unit="in",
          note="The official product page and multiple article prose descriptions use 6.6 inches. The 6.73-inch figure appears only in a local spec-table entry that conflicts with its own article prose; retained here as a source discrepancy rather than silently treated as another variant."),
        f("display_technology", "nubia_neo_gizguide_ph", "IPS LCD display", "IPS LCD", key="displayType", status="VERIFIED_SECONDARY"),
        resolution,
        f("display_refresh_rate", "nubia_neo_zte_malaysia_specs", "120Hz refresh rate", 120, key="refreshHz", unit="Hz"),
        nd("display_brightness", "nubia_neo_zte_malaysia_specs", "No numeric peak or typical brightness value is published; generic screen-brightening claims are not converted into a nit value."),
        f("display_protection", "nubia_neo_yugatech_ph", "Asahi Glass protection reported by YugaTech; not separately specified on ZTE's product page", "Asahi Glass", status="VERIFIED_SECONDARY"),
        f("chipset", "nubia_neo_zte_malaysia_specs", "UNISOC T820 5G platform", "UNISOC T820", key="chipset"),
        f("process_node", "nubia_neo_unisoc_chipset", "UNISOC T820 uses a 6nm EUV process", 6, unit="nm", status="VERIFIED_SECONDARY"),
        f("cpu", "nubia_neo_unisoc_chipset", "1× Cortex-A76 up to 2.7GHz + 3× Cortex-A76 up to 2.3GHz + 4× Cortex-A55 up to 2.1GHz", "1x Cortex-A76 @ 2.7GHz + 3x Cortex-A76 @ 2.3GHz + 4x Cortex-A55 @ 2.1GHz", key="cpu", status="VERIFIED_SECONDARY"),
        f("gpu", "nubia_neo_unisoc_chipset", "Arm Mali-G57 MP4, up to 850MHz", "Arm Mali-G57 MP4", key="gpu", status="VERIFIED_SECONDARY"),
        f("operating_system", "nubia_neo_zte_certificate", "MyOS 13.0.0 on Android 13", "Android 13 with MyOS 13", key="os", note="ZTE's 8150N certificate identifies MyOS 13.0.0; ZTE regional product specifications identify Android 13."),
        nd("os_support", "nubia_neo_zte_global_product", "No published exact model OS/security-update schedule or guaranteed support period was found."),
        f("ram_capacity", "nubia_neo_zte_malaysia_specs", "8GB installed physical RAM plus up to 10GB Fusion RAM", 8, key="ramGb", unit="GB",
          note="Catalog capacity is physical RAM only; virtual/Fusion RAM is not counted as installed memory."),
        ram_type,
        f("storage_capacity", "nubia_neo_zte_malaysia_specs", "256GB internal storage", 256, key="storageGb", unit="GB"),
        f("storage_type", "nubia_neo_yugatech_ph", "UFS 3.1 storage reported for the 8GB/256GB Philippine listing", "UFS 3.1", status="VERIFIED_SECONDARY"),
        f("storage_expansion", "nubia_neo_noypi_ph", "MicroSD expansion reported; maximum supported card capacity is not recorded by the manufacturer source reviewed", "microSD expansion reported; maximum capacity not recorded", status="VERIFIED_SECONDARY"),
        f("rear_camera_system", "nubia_neo_zte_malaysia_specs", "50MP main + 2MP secondary rear camera", "50 MP main + 2 MP secondary", key="rearCameraMp", catalog_value=50, unit="MP"),
        nd("main_camera_sensor", "nubia_neo_zte_global_product", "The exact main-camera sensor manufacturer and part number are not disclosed in the reviewed manufacturer and PH launch sources."),
        na("ultrawide_camera", "nubia_neo_zte_malaysia_specs", "The manufacturer lists a 50MP+2MP dual-rear-camera system and does not list an ultrawide module.", "Not applicable to the documented dual-camera configuration; no ultrawide lens is listed."),
        na("telephoto_camera", "nubia_neo_zte_malaysia_specs", "The manufacturer lists a 50MP+2MP dual-rear-camera system and does not list a telephoto module.", "Not applicable to the documented dual-camera configuration; no telephoto lens is listed."),
        front_camera,
        f("video_recording", "nubia_neo_yugatech_ph", "Rear video recording up to 1080p at 30fps", "1080p at 30fps", status="VERIFIED_SECONDARY", key="video"),
        f("battery_capacity", "nubia_neo_zte_malaysia_specs", "4500mAh battery", 4500, key="batteryMah", unit="mAh"),
        f("battery_technology", "nubia_neo_yugatech_ph", "Li-Ion 4500mAh non-removable battery", "Li-Ion; non-removable", status="VERIFIED_SECONDARY"),
        f("wired_charging", "nubia_neo_zte_malaysia_specs", "22.5W fast charging", 22.5, key="chargingW", unit="W"),
        nd("wireless_charging", "nubia_neo_zte_global_product", "Wireless and reverse charging are not listed in the reviewed manufacturer specifications."),
        f("dimensions", "nubia_neo_zte_malaysia_specs", "163.7 × 75 × 7.98mm", "163.7 × 75 × 7.98", key="dimensions", unit="mm"),
        f("weight", "nubia_neo_xataka_specs", "189g", 189, unit="g", status="VERIFIED_SECONDARY"),
        nd("materials", "nubia_neo_zte_malaysia_specs", "Frame and rear-cover material composition is not disclosed in the reviewed manufacturer specifications."),
        nd("ingress_protection", "nubia_neo_zte_malaysia_specs", "No IP ingress-protection rating is listed in the reviewed manufacturer or launch sources."),
        f("sim_esim", "nubia_neo_zte_malaysia_specs", "Dual SIM and 5G dual-SIM support; eSIM is not listed", "Dual SIM; eSIM not recorded", key="sim", status="VERIFIED_SECONDARY"),
        f("cellular_bands", "nubia_neo_gcf_model", "GCF-certified 5G NSA n1/n3/n28/n78; LTE FDD bands 1/3/7/8/20/28 and LTE TDD band 38", "5G NSA n1/n3/n28/n78; LTE FDD 1/3/7/8/20/28; LTE TDD 38", key="cellular", status="VERIFIED_SECONDARY",
          note="Exact 8150N model certification data. The certification record does not establish that every listed band is enabled on a Philippine carrier or a PH-specific firmware variant."),
        f("wifi", "nubia_neo_zte_malaysia_specs", "Dual-band Wi-Fi at 2.4GHz and 5GHz; YugaTech lists 802.11ac", "Dual-band Wi-Fi (2.4GHz/5GHz; 802.11ac reported)", key="wifi", status="VERIFIED_SECONDARY"),
        f("bluetooth", "nubia_neo_yugatech_ph", "Bluetooth 5.2", "Bluetooth 5.2", status="VERIFIED_SECONDARY"),
        f("usb", "nubia_neo_yugatech_ph", "USB Type-C connector; USB data version not specified in the cited local listing", "USB Type-C; data version not recorded", key="ports", status="VERIFIED_SECONDARY"),
        f("nfc", "nubia_neo_zte_malaysia_specs", "NFC supported", "NFC supported", status="VERIFIED_SECONDARY"),
        f("gnss", "nubia_neo_yugatech_ph", "GPS with GLONASS, Galileo and BeiDou", "GPS, GLONASS, Galileo, BeiDou", status="VERIFIED_SECONDARY"),
        f("audio", "nubia_neo_noypi_ph", "3.5mm headphone jack and single loudspeaker; DTS:X Ultra is listed by ZTE", "3.5mm headphone jack; mono speaker; DTS:X Ultra", status="VERIFIED_SECONDARY", key="sound"),
        f("sensors", "nubia_neo_zte_malaysia_specs", "Side-mounted fingerprint sensor; other sensors are not listed on the reviewed product page", "Side-mounted fingerprint sensor; others not recorded", status="VERIFIED_SECONDARY"),
    ]
    if len(rows) != 46 or len({row["fieldId"] for row in rows}) != 46:
        raise ValueError(f"Expected 46 distinct field reviews, got {len(rows)}")
    return rows


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if not device or device.get("scopeStatus") != "Pending":
        raise ValueError("Expected the workbook's pending nubia Neo 5G record; refusing unexpected scope/device.")
    if len(device.get("variants", [])) != 1 or device["variants"][0].get("id") != f"{DEVICE}-unrecorded":
        raise ValueError("Expected one unrecorded placeholder configuration; review before replacing it.")

    replacement = {"id": CONFIG, "label": "8 GB RAM / 256 GB storage (5G)",
                   "modelCode": "8150N", "notes": "The verified Philippine listing identifies 8GB physical RAM and 256GB storage. Up to 10GB Fusion RAM is software-backed and not a separate installed-RAM configuration."}
    review = {
        "deviceId": DEVICE, "configurationId": CONFIG, "brand": "ZTE",
        "model": "nubia Neo 5G", "configuration": "8 GB RAM / 256 GB storage",
        "configurationLabel": replacement["label"], "modelCode": "8150N",
        "replacementVariants": [replacement], "replaceUnrecordedPlaceholder": True,
        "sources": SOURCES, "fields": fields(),
        "availabilityEvidence": {
            "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
            "availabilityStatus": "Verified historical Philippine sale: ZTE Philippines was observed selling nubia Neo 5G (8150N), 8GB/256GB, on its TikTok Shop on 2023-09-06. Current stock and price are not verified.",
            "philippineAvailability": "Verified historical Philippine sale of the ZTE nubia Neo 5G 8GB/256GB configuration, documented in September 2023.",
            "observedAt": OBSERVED,
            "qualityFlag": "Manually reviewed; 8GB/256GB PH configuration and historical sale verified; current price unavailable; exact display resolution, RAM type and front camera remain conflicted.",
            "catalogModel": "nubia Neo 5G",
            "manufacturer": "ZTE Corporation",
            "productLine": "nubia Neo",
            "modelNumber": "8150N",
            "philippineReleaseYear": 2023,
            "philippineDateLabel": "First verified Philippine sale observation",
            "researchNotes": "Workbook row 168 is matched to ZTE manufacturer model nubia 8150N, which GCF identifies as the nubia Neo 5G. Contemporaneous Philippine sources identify one 8GB physical RAM / 256GB storage configuration. Virtual/Fusion RAM is not a separate variant. Historical PH sale and price evidence are preserved with dates; current PH price/stock is not established. Image shown on official ZTE product page is an exact model-level candidate, but image reuse permission is undocumented, so retain the neutral placeholder. Study scope remains Pending.",
            "openIssues": [
                {"issue": "Current Philippine price and stock were not found for the older 8150N model", "action": "Keep current price blank; preserve only dated 2023 Philippine price observations."},
                {"issue": "Sources disagree on exact display pixel resolution", "action": "Keep the normalized pixel dimensions blank; retain FHD only as the manufacturer description."},
                {"issue": "Local sources disagree on physical RAM generation and front-camera resolution", "action": "Keep both normalized fields blank and expose their source evidence."},
                {"issue": "Study eligibility remains Pending", "action": "Keep inventory eligibility unchanged until the study screening rule is applied."},
                {"issue": "Official exact-model product imagery is visible, but no reuse license or permission was found", "action": "Keep the neutral unavailable-image placeholder and preserve the candidate image URL for rights review."},
            ],
        },
    }
    # Replace this exact reviewed configuration as a whole so reruns cannot
    # preserve a stale field decision or discard a newly documented conflict.
    manual["records"] = [row for row in manual["records"]
                         if not (row.get("deviceId") == DEVICE and row.get("configurationId") == CONFIG)]
    add_review(manual, catalog, review)
    deduplicate_target_reviews(manual, {(DEVICE, CONFIG)})
    saved = next(row for row in manual["records"]
                 if row.get("deviceId") == DEVICE and row.get("configurationId") == CONFIG)
    saved.update({"model": "nubia Neo 5G", "configuration": "8 GB RAM / 256 GB storage",
                  "configurationLabel": replacement["label"]})
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    images = json.loads(IMAGES.read_text(encoding="utf-8"))
    images[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "The official ZTE product page for nubia Neo 5G links to an exact-model product image, but no reuse license or permission to republish/hotlink it was documented. Keep the neutral placeholder.",
        "sourcePage": URL_ZTE_MY,
        "assetUrl": None,
        "candidateAssetUrl": IMAGE_URL,
        "scope": "Official ZTE Malaysia nubia Neo 5G product image; model-level match; the pictured color and PH configuration are not established by the asset itself.",
        "rightsTermsUrl": None,
        "rightsCheck": "Reviewed the official ZTE product page and linked asset. No image reuse license or permission was found. Do not download or hotlink; no access controls were bypassed.",
        "rightsCheckSourcePage": URL_ZTE_MY,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for ZTE nubia Neo 5G",
    }
    IMAGES.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 9999, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_nubia_neo_5g_8150n_8gb_256gb",
         "variant_ram_gb": 8, "variant_storage_gb": 256,
         "price_type": "historical_ph_official_store_list_price",
         "source_published_at": "2023-09-06",
         "excerpt": "REVU observed ZTE Philippines selling the 8GB/256GB nubia Neo 5G on TikTok Shop at PHP 9,999 list price.",
         "source_url": URL_REVU, "source_kind": "historical_local_official_store_price",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_list_price_not_current"},
        {"device_id": DEVICE, "amount_php": 8599, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_nubia_neo_5g_8150n_8gb_256gb",
         "variant_ram_gb": 8, "variant_storage_gb": 256,
         "price_type": "historical_limited_time_official_store_promotion",
         "source_published_at": "2023-09-06",
         "excerpt": "REVU recorded a time-limited PHP 8,599 TikTok Shop offer during the official ZTE Philippines live sale; the report described it as a limited-time promotion.",
         "source_url": URL_REVU, "source_kind": "historical_local_promotion",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_limited_promotion_not_current"},
        {"device_id": DEVICE, "amount_php": 9799, "configuration_id": CONFIG,
         "configuration_match": "exact_ph_nubia_neo_5g_8150n_8gb_256gb",
         "variant_ram_gb": 8, "variant_storage_gb": 256,
         "price_type": "historical_ph_marketplace_listing_price",
         "source_published_at": "2023-09-14",
         "excerpt": "YugaTech reported the exact 8GB/256GB nubia Neo 5G listing at PHP 9,799 on Lazada Philippines on 2023-09-14.",
         "source_url": URL_YUGA, "source_kind": "historical_local_marketplace_listing",
         "observed_at": OBSERVED, "local_availability_verified": True,
         "availability_status": "historical_listing_not_current"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED, "inventory_count": 456, "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "ZTE", "model_name": "nubia Neo 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [], "observations": [],
        "discovery": [{"device_id": DEVICE, "source_url": item["url"], "source_kind": item["purpose"], "status": "reviewed", "result": item["note"]} for item in SOURCES],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    latest = json.loads(LATEST_REVIEWED.read_text(encoding="utf-8"))
    target = next((row for row in latest.get("models", []) if row.get("device_id") == DEVICE), None)
    if target:
        target["status"] = "manually_reviewed"
    latest["run_at"] = OBSERVED
    LATEST_REVIEWED.write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for row in review["fields"]:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"workbookRow": 168, "model": "ZTE nubia Neo 5G", "modelNumber": "8150N",
                      "configuration": replacement["label"], "reviewedFields": len(review["fields"]),
                      "fieldStatuses": counts, "sources": len(SOURCES),
                      "philippineSaleObservation": "2023-09-06", "historicalListPricePhp": 9999,
                      "historicalPromoPricePhp": 8599, "historicalLazadaPricePhp": 9799,
                      "currentPhpPrice": "not found", "image": "exact official candidate found; reuse rights not established; placeholder retained",
                      "studyScope": "Pending"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
