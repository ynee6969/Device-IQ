#!/usr/bin/env python3
"""Record sourced Philippine configuration evidence for Nokia X30 5G."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE_IMAGES = ROOT / "research/catalog-image-unavailable.json"
PRICE_SNAPSHOT = ROOT / "research/enrichment/nokia-x30-5g-ph-price-candidate-2026-11-26.json"
OBSERVED = "2026-11-26"
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
DEVICE = "device_71110a4a38ebff"
OLD_CONFIG = f"{DEVICE}-unrecorded"
CONFIG = f"{DEVICE}-8gb-256gb-ph"

URL_HMD_SPECS = "https://www.hmd.com/en_in/nokia-x-30/specs"
URL_HMD_PRESS = "https://www.hmd.com/en_eg/press/nokia-x30-press-release"
URL_HMD_GUIDE = "https://www.hmd.com/en_int/support/nokia-x30-5g-user-guide/keys-and-parts"
URL_NTC = "https://ntc.gov.ph/wp-content/uploads/2024/TYPE%20APPROVED/TA_2022_4col_%28GEC%29.pdf"
URL_YUGA = "https://www.yugatech.com/mobile/nokia-x30-5g-launches-in-the-philippines-priced/"
URL_HUNGRY = "https://hungrygeeks.com.ph/nokia-x30-5g-now-in-ph-priced-at-php-27990/"
URL_UNBOX = "https://unbox.ph/news/nokia-x30-now-in-the-philippines-with-premium-price-tag/"
URL_NOYPI = "https://www.noypigeeks.com/promos/nokia-x30-5g-price-drop/"
URL_QUALCOMM = "https://www.qualcomm.com/smartphones/products/6-series/snapdragon-695-5g-mobile-platform"
URL_NANOREVIEW = "https://nanoreview.net/en/soc/qualcomm-snapdragon-695"
URL_KIMOVIL = "https://www.kimovil.com/en/where-to-buy-nokia-x30-5g-8gb-256gb"
URL_GSMARENA = "https://www.gsmarena.com/nokia_x30-11831.php"


def source(sid: str, publisher: str, url: str, purpose: str, note: str,
           publication_date: str | None = None) -> dict:
    return {"id": sid, "publisher": publisher, "url": url,
            "publicationDate": publication_date, "accessDate": OBSERVED,
            "purpose": purpose, "note": note}


SOURCES = [
    source("nokia_x30_hmd_specs", "HMD Global / Nokia", URL_HMD_SPECS,
           "Primary exact-model specifications for TA-1450",
           "HMD's India specification page identifies model TA-1450 and lists the 8 GB / 256 GB configuration. It documents display, cameras, connectivity, battery, Android 12, IP67, dimensions, weight, materials, networks, audio, and sensors. The regional page does not establish local Philippine operator compatibility or local sale by itself."),
    source("nokia_x30_hmd_launch", "HMD Global", URL_HMD_PRESS,
           "Primary global launch date and launch support/material claims",
           "Published September 1, 2022; HMD says the phone launches and is available from that day in global 6/128 GB and 8/256 GB configurations. This is the global launch date; GSMArena separately records September 21 as retail release. HMD's launch release promises three OS upgrades, while its current TA-1450 specifications page says two; keep update count unresolved. The press release describes 100% recycled aluminium frame and 65% recycled plastic back." ,
           "2022-09-01"),
    source("nokia_x30_hmd_user_guide", "HMD Global", URL_HMD_GUIDE,
           "Primary model-family and SIM/eSIM support documentation",
           "HMD's X30 5G guide page links instructions for using eSIM and identifies the X30 5G family. The reviewed support content does not establish which SIM tray/eSIM combination shipped in the Philippine 8/256 GB sale unit."),
    source("nokia_x30_ntc_gec", "National Telecommunications Commission Philippines", URL_NTC,
           "Philippine equipment registration and model-code cross-check",
           "NTC's 2022 GEC equipment list includes Nokia TA-1450. HMD's exact-model technical specifications page identifies the same code. Registration supports local equipment identity, but does not independently prove a specific retail configuration."),
    source("nokia_x30_yugatech_ph", "YugaTech Philippines", URL_YUGA,
           "Philippine release date, local configuration, launch price, and specifications",
           "Published October 28, 2022. Reports official Philippine release, the 8 GB / 256 GB variant at PHP 27,990, Cloudy Blue, and October 28 availability through authorized online retailers and stores. Also lists local specifications. Its claims of UFS 3.0 and hybrid microSD conflict with other device references, so those fields remain unresolved.",
           "2022-10-28"),
    source("nokia_x30_hungrygeeks_ph", "HungryGeeks Philippines", URL_HUNGRY,
           "Contemporaneous Philippine sale date and exact retail configuration cross-check",
           "Published October 26, 2022. Says the device had officially arrived in the Philippines, PHP 27,990, and that authorized nationwide retailers would start carrying it on October 28. The local spec list corroborates 8/256 GB, Snapdragon 695, Android 12, cameras, battery, and IP67.",
           "2022-10-26"),
    source("nokia_x30_unbox_ph", "Unbox Philippines", URL_UNBOX,
           "Independent Philippine launch and technical cross-check",
           "Published October 26, 2022. Reports Philippine availability from October 28 at PHP 27,990 and 8 GB / 256 GB. Its article has inconsistent details: prose says IP57 while its specification list says IP67; it also lists Bluetooth 5.0 while HMD and YugaTech list 5.1. Manufacturer specifications and corroborating local sources are preferred for those fields; the discrepancies are retained here.",
           "2022-10-26"),
    source("nokia_x30_noypigeeks_ph", "NoypiGeeks Philippines", URL_NOYPI,
           "Dated historical local price change and exact configuration cross-check",
           "Published June 5, 2023. Reports 8 GB / 256 GB and a reduction from the PHP 27,990 launch price to PHP 18,990. This is a historical price observation and is not represented as current or orderable.",
           "2023-06-05"),
    source("nokia_x30_qualcomm_695", "Qualcomm", URL_QUALCOMM,
           "Primary Snapdragon 695 chipset/platform details",
           "Qualcomm specifies Snapdragon 695 5G, 6 nm process, Kryo 660 CPU up to 2.2 GHz, and Adreno 619 GPU. Platform capabilities are not substituted for handset-specific claims."),
    source("nokia_x30_nanoreview_695", "NanoReview", URL_NANOREVIEW,
           "Independent chipset architecture cross-check",
           "Lists Snapdragon 695 with two Kryo 660 Gold/Cortex-A78 cores up to 2.2 GHz and six Kryo 660 Silver/Cortex-A55 cores up to 1.8 GHz, 6 nm, and Adreno 619. This is chipset-level information, not a handset benchmark."),
    source("nokia_x30_kimovil", "Kimovil", URL_KIMOVIL,
           "Exact-model and global 8 GB / 256 GB configuration cross-check",
           "The exact X30 5G 8/256 page lists the international model and core hardware. Kimovil reports UFS 3.0 and microSD, while a Nokia datasheet transcription elsewhere lists UFS 2.2 and GSMArena says there is no card slot. These disagreements are not used to assert Philippine-specific storage type or expansion."),
    source("nokia_x30_gsmarena", "GSMArena", URL_GSMARENA,
           "Exact-model global release and independent specifications cross-check",
           "Lists global announcement on September 1 and retail release on September 21, 2022; the device is described with 6/128 and 8/256 options, IP67, no card slot, and nano-SIM/eSIM or dual nano-SIM variants. The release date represents its retail-status entry, distinct from HMD's official global launch/availability date."),
]


def field(fid: str, sid: str, value, normalized, *, status="VERIFIED_SECONDARY",
          key=None, unit=None, note: str, config_match: str,
          catalog_value=None, price_type=None) -> dict:
    item = {"fieldId": fid, "status": status, "sourceId": sid,
            "sourceValue": value, "normalizedValue": normalized,
            "note": note, "configurationMatch": config_match}
    if key:
        item["catalogKey"] = key
        item["catalogValue"] = normalized if catalog_value is None else catalog_value
    if unit:
        item["unit"] = unit
    if price_type:
        item["priceType"] = price_type
    return item


def fields_for() -> list[dict]:
    config = "Philippine Nokia X30 5G, 8 GB RAM / 256 GB storage"
    rows = [
        field("model_number", "nokia_x30_ntc_gec", "NTC lists Nokia model TA-1450; HMD identifies TA-1450 on its Nokia X30 5G specification page", "TA-1450", status="VERIFIED", note="Exact model-code match between the Philippine NTC 2022 GEC and HMD's TA-1450 specifications page; local launch coverage identifies the marketed model as Nokia X30 5G.", config_match="Nokia X30 5G TA-1450, locally marketed 8 GB / 256 GB variant"),
        field("global_release_date", "nokia_x30_hmd_launch", "HMD announced launch and global availability on September 1, 2022; GSMArena lists retail release September 21", "2022-09-01", status="VERIFIED", note="Use HMD's primary global launch/availability date. GSMArena's September 21 entry appears to represent later retail release; the dates are distinguished rather than silently conflated.", config_match="Global Nokia X30 5G model"),
        field("configuration", "nokia_x30_yugatech_ph", "Nokia X30 5G Philippine retail version, 8 GB RAM / 256 GB storage", "8 GB RAM / 256 GB storage", status="VERIFIED_SECONDARY", note="YugaTech identifies the local priced variant as 8/256 GB; HMD specs and the global release confirm this as a genuine X30 configuration. The global 6/128 option is not added as a Philippine variant because no local source establishes its sale.", config_match=config),
        field("philippine_release_date", "nokia_x30_hungrygeeks_ph", "Local launch report says the phone had arrived by October 26, 2022; authorized online and physical retail availability started October 28", "2022-10-28", status="VERIFIED_SECONDARY", note="October 28 is the reported start of authorized nationwide retail availability, not merely the earlier October 26 announcement/report date.", config_match="Philippine Nokia X30 5G launch; local 8 GB / 256 GB configuration"),
        field("official_launch_price_php", "nokia_x30_yugatech_ph", "PHP 27,990 launch price for the Nokia X30 5G 8 GB / 256 GB", 27990, status="VERIFIED_SECONDARY", unit="PHP", note="Historical Philippine launch price for the exact local configuration; not a current offer.", config_match=config, price_type="historical_ph_launch_price"),
        field("current_price_php", "nokia_x30_noypigeeks_ph", "Reviewed local price sources are dated 2022–2023; no current dated and orderable Philippine offer was verified", None, status="PENDING_VERIFICATION", unit="PHP", note="Keep current price blank. Preserve PHP 27,990 launch pricing and the dated PHP 18,990 2023 promotion as historical only.", config_match=config, price_type="no_current_offer_verified"),
        field("display_size", "nokia_x30_hmd_specs", "6.43-inch AMOLED display", 6.43, status="VERIFIED", key="displayInches", unit="in", note="HMD's TA-1450 specification and Philippine launch sources agree.", config_match=config),
        field("display_technology", "nokia_x30_hmd_specs", "AMOLED", "AMOLED", status="VERIFIED", key="displayType", note="HMD and Philippine launch coverage identify the AMOLED panel.", config_match=config),
        field("display_resolution", "nokia_x30_hmd_specs", "FHD+ 1080 x 2400 pixels", "1080 x 2400", status="VERIFIED", key="resolution", note="HMD lists 1080 x 2400; local launch sources describe the same FHD+ resolution.", config_match=config),
        field("display_refresh_rate", "nokia_x30_hmd_specs", "90 Hz", 90, status="VERIFIED", key="refreshHz", unit="Hz", note="HMD lists a 90 Hz refresh rate.", config_match=config),
        field("display_brightness", "nokia_x30_hmd_specs", "400 nits typical; 700 nits peak", 400, status="VERIFIED", unit="nits", note="HMD specifies both values; catalog numeric stores typical brightness and preserves the peak value in the source text.", config_match=config),
        field("display_protection", "nokia_x30_hmd_specs", "Corning Gorilla Glass Victus", "Corning Gorilla Glass Victus", status="VERIFIED", note="HMD's exact TA-1450 page identifies the cover glass; Philippine launch coverage corroborates it.", config_match=config),
        field("chipset", "nokia_x30_hmd_specs", "Qualcomm Snapdragon 695 5G", "Qualcomm Snapdragon 695 5G", status="VERIFIED", key="chipset", note="HMD and local launch sources identify Snapdragon 695 5G.", config_match=config),
        field("process_node", "nokia_x30_qualcomm_695", "6 nm process", 6, status="VERIFIED", unit="nm", note="Qualcomm's product page identifies the Snapdragon 695 as a 6 nm platform.", config_match=config),
        field("cpu", "nokia_x30_nanoreview_695", "2x Kryo 660 Gold / Cortex-A78 up to 2.2 GHz + 6x Kryo 660 Silver / Cortex-A55 up to 1.8 GHz", "2x Cortex-A78 2.2 GHz + 6x Cortex-A55 1.8 GHz", status="VERIFIED_SECONDARY", key="cpu", note="NanoReview's chipset-level core breakdown; Qualcomm confirms Kryo 660 and up to 2.2 GHz. This does not represent a measured handset performance score.", config_match=config),
        field("gpu", "nokia_x30_qualcomm_695", "Qualcomm Adreno 619", "Qualcomm Adreno 619", status="VERIFIED", key="gpu", note="Qualcomm identifies the Snapdragon 695 GPU as Adreno 619; HMD and YugaTech agree.", config_match=config),
        field("operating_system", "nokia_x30_hmd_specs", "Android 12 at launch", "Android 12", status="VERIFIED", key="os", note="HMD's exact model specification and Philippine launch coverage identify Android 12 at launch; later updates are not substituted.", config_match=config),
        field("os_support", "nokia_x30_hmd_launch", "HMD's launch release promises 3 OS upgrades; current HMD TA-1450 specification page lists 2 OS upgrades", None, status="CONFLICTING_INFORMATION", note="Manufacturer launch and current regional product pages disagree. Leave the promised OS-upgrade count unresolved; the global launch also promised three years of security updates.", config_match="TA-1450 model; HMD global launch policy conflicts with current HMD India specification page"),
        field("ram_capacity", "nokia_x30_yugatech_ph", "8 GB RAM in the Philippine 8 GB / 256 GB variant", 8, status="VERIFIED_SECONDARY", key="ramGb", unit="GB", note="Exact Philippine-priced variant from YugaTech, matched to HMD's 8 GB / 256 GB model configuration.", config_match=config),
        field("ram_type", "nokia_x30_hmd_specs", "RAM technology not stated on the reviewed exact-model manufacturer page", None, status="NOT_DISCLOSED", unit="", note="Do not infer the RAM standard from chipset or model family.", config_match=config),
        field("storage_capacity", "nokia_x30_yugatech_ph", "256 GB internal storage in the Philippine 8 GB / 256 GB variant", 256, status="VERIFIED_SECONDARY", key="storageGb", unit="GB", note="Exact local retail configuration confirmed by YugaTech and matched to the HMD product specification.", config_match=config),
        field("storage_type", "nokia_x30_yugatech_ph", "YugaTech and Kimovil list UFS 3.0 for 256 GB; a Nokia datasheet transcription lists UFS 2.2", None, status="CONFLICTING_INFORMATION", note="The 256 GB storage technology is inconsistent across exact-model sources. Do not publish a UFS version until HMD or the Philippine unit resolves the discrepancy.", config_match="Nokia X30 5G 8 GB / 256 GB; exact variant storage type disputed"),
        field("storage_expansion", "nokia_x30_yugatech_ph", "YugaTech and Kimovil report a hybrid microSD slot; GSMArena says there is no card slot; HMD guide does not resolve it", None, status="CONFLICTING_INFORMATION", note="Keep external storage support blank because reviewed sources disagree and the HMD guide does not document microSD support.", config_match="Nokia X30 5G TA-1450; storage expansion unresolved"),
        field("rear_camera_system", "nokia_x30_hmd_specs", "Dual rear system: 50 MP main with OIS and 13 MP 123-degree ultrawide", "50 MP main OIS + 13 MP ultrawide", status="VERIFIED", note="HMD's exact-model specification describes both rear modules and their roles; local YugaTech corroborates the configuration.", config_match=config),
        field("main_camera_sensor", "nokia_x30_hmd_specs", "50 MP main, f/1.9, OIS, 1/1.57-inch sensor format; no sensor manufacturer/model stated", "50 MP, f/1.9, OIS, 1/1.57-inch", status="VERIFIED", note="Record optical details from HMD; do not infer a named sensor model.", config_match=config),
        field("ultrawide_camera", "nokia_x30_hmd_specs", "13 MP ultrawide, 123-degree field of view, f/2.4", "13 MP, 123-degree FOV, f/2.4", status="VERIFIED", note="HMD's exact-model rear camera specification; local launch sources agree on resolution and role.", config_match=config),
        field("telephoto_camera", "nokia_x30_hmd_specs", "HMD specifies a two-module rear camera system and lists no telephoto module", "No telephoto module listed", status="VERIFIED", note="The manufacturer lists both rear modules and neither is telephoto.", config_match=config),
        field("front_camera", "nokia_x30_hmd_specs", "16 MP front camera, f/2.4", 16, status="VERIFIED", key="frontCameraMp", unit="MP", note="HMD's exact-model specification identifies 16 MP; Philippine launch sources agree.", config_match=config),
        field("video_recording", "nokia_x30_hmd_specs", "Specific rear and front video resolution/frame-rate modes not stated in the reviewed manufacturer page", None, status="NOT_DISCLOSED", note="Do not infer video modes from the chipset's supported capture capabilities.", config_match=config),
        field("battery_capacity", "nokia_x30_hmd_specs", "4200 mAh non-removable battery", 4200, status="VERIFIED", key="batteryMah", unit="mAh", note="HMD and Philippine launch sources agree on rated capacity.", config_match=config),
        field("battery_technology", "nokia_x30_hmd_specs", "Battery chemistry not disclosed; HMD states non-removable", None, status="NOT_DISCLOSED", note="Do not infer lithium chemistry from product class.", config_match=config),
        field("wired_charging", "nokia_x30_hmd_specs", "33 W wired fast charging; QC 3.0, PD 3.0, PPS", 33, status="VERIFIED", key="chargingW", unit="W", note="HMD lists 33 W and supported charging standards; supplied charger availability is separate (33 W charger sold separately at global launch).", config_match=config),
        field("wireless_charging", "nokia_x30_hmd_specs", "Wireless or reverse wireless charging is not listed in the reviewed manufacturer specification", None, status="NOT_DISCLOSED", note="Omission is not recorded as a confirmed unsupported feature.", config_match=config),
        field("dimensions", "nokia_x30_hmd_specs", "158.9 x 73.9 x 7.99 mm", "158.9 x 73.9 x 7.99 mm", status="VERIFIED", key="dimensions", unit="mm", note="HMD exact-model measurement; Philippine sources round the depth to 8.0 mm.", config_match=config),
        field("weight", "nokia_x30_hmd_specs", "185 g", 185, status="VERIFIED", key="weightG", unit="g", note="HMD exact-model weight; Philippine sources agree.", config_match=config),
        field("materials", "nokia_x30_hmd_specs", "Front Gorilla Glass Victus; frame 100% recycled aluminium; back 65% recycled plastic (64.5% on current specification page)", "Gorilla Glass Victus front; 100% recycled aluminium frame; 64.5% recycled plastic back", status="VERIFIED", note="HMD's specifications page states 64.5% recycled plastic in back; the launch release rounds this to 65%. Materials are documented as manufacturer's claims.", config_match=config),
        field("ingress_protection", "nokia_x30_hmd_specs", "IP67 on HMD specs and YugaTech; Unbox article prose says IP57 but its own spec list says IP67", "IP67", status="VERIFIED", note="HMD's TA-1450 specification and multiple local/exact-model sources say IP67. Unbox contains an internal typo/inconsistency (IP57 in prose, IP67 in specs); the consistent manufacturer and local specification evidence supports IP67.", config_match=config),
        field("sim_esim", "nokia_x30_hmd_specs", "HMD lists NFC + eSIM; GSMArena lists nano-SIM/eSIM or dual nano-SIM; YugaTech calls local slot hybrid dual SIM", None, status="CONFLICTING_INFORMATION", note="SIM/eSIM and physical slot arrangement varies by regional model; local configuration applicability is not resolved. Do not publish an inferred SIM layout.", config_match="Nokia X30 TA-1450; Philippine SIM tray/eSIM configuration unresolved"),
        field("cellular_bands", "nokia_x30_hmd_specs", "TA-1450: GSM 850/900/1800/1900; WCDMA B1/B5/B8; LTE B1/2/3/4/5/7/8/12/17/20/28/32/38/39/40/41; 5G n1/3/5/7/8/28/38/40/41/77/78", "GSM 850/900/1800/1900; WCDMA B1/B5/B8; LTE B1/2/3/4/5/7/8/12/17/20/28/32/38/39/40/41; 5G n1/3/5/7/8/28/38/40/41/77/78", status="VERIFIED", key="cellular", note="HMD's exact TA-1450 page lists these radio bands; NTC registration ties TA-1450 to a Philippine equipment record. Band support does not guarantee carrier certification or coverage.", config_match=config),
        field("wifi", "nokia_x30_hmd_specs", "Dual-band 2.4/5 GHz 802.11 a/b/g/n/ac/ax-ready; local launch coverage calls it Wi-Fi 6", "Wi-Fi 6 (802.11ax-ready), dual-band", status="VERIFIED", key="wifi", note="HMD lists ax-ready dual-band Wi-Fi; local launch sources report Wi-Fi 6.", config_match=config),
        field("bluetooth", "nokia_x30_hmd_specs", "Bluetooth 5.1 in HMD exact TA-1450 specifications and YugaTech; Unbox says 5.0", "Bluetooth 5.1", status="VERIFIED", note="HMD's exact model specification and YugaTech agree on 5.1. Unbox reports 5.0 in one list; the manufacturer value takes precedence and the discrepancy remains documented.", config_match=config),
        field("usb", "nokia_x30_hmd_specs", "USB Type-C, USB 2.0, OTG", "USB Type-C; USB 2.0; OTG", status="VERIFIED", key="ports", note="HMD specifies connector, interface, and OTG support.", config_match=config),
        field("nfc", "nokia_x30_hmd_specs", "NFC supported", "Yes", status="VERIFIED", note="HMD exact TA-1450 specification and Philippine launch reports identify NFC support.", config_match=config),
        field("gnss", "nokia_x30_hmd_specs", "GPS/AGPS, GLONASS, BeiDou, Galileo L1/L5 dual-band", "GPS, A-GPS, GLONASS, BeiDou, Galileo L1/L5", status="VERIFIED", key="gnss", note="HMD's exact-model navigation listing; no unsupported system is inferred.", config_match=config),
        field("audio", "nokia_x30_hmd_specs", "One speaker, two microphones; OZO Spatial Audio capture and aptX HD/Classic/Adaptive", "Single speaker; dual microphones; OZO audio capture; aptX HD/Classic/Adaptive", status="VERIFIED", key="sound", note="HMD lists one speaker and two microphones plus audio capture and codec features.", config_match=config),
        field("sensors", "nokia_x30_hmd_specs", "Accelerometer, ambient light sensor, e-compass, gyroscope, proximity sensor; under-display fingerprint sensor", "Accelerometer, ambient light, e-compass, gyroscope, proximity, under-display fingerprint", status="VERIFIED", note="HMD exact-model specification lists the sensors and fingerprint reader.", config_match=config),
    ]
    if len(rows) != 46:
        raise ValueError(f"Expected 46 smartphone field records, got {len(rows)}")
    source_ids = {item["id"] for item in SOURCES}
    missing = sorted({item["sourceId"] for item in rows} - source_ids)
    if missing:
        raise ValueError(f"Fields reference undefined sources: {missing}")
    return rows


def availability_evidence() -> dict:
    return {
        "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
        "availabilityStatus": "Philippine reporting says authorized retail availability for the 8 GB / 256 GB variant began October 28, 2022. Workbook eligibility remains Pending.",
        "philippineAvailability": "Philippine launch coverage reports the Nokia X30 5G 8 GB / 256 GB variant at PHP 27,990 and identifies authorized online and nationwide physical retail availability beginning October 28, 2022. The NTC 2022 GEC lists Nokia TA-1450, which matches HMD's exact-model code. This confirms reported historical Philippine availability, not present-day stock or orderability.",
        "observedAt": OBSERVED,
        "manufacturer": "HMD Global Oy (Nokia brand licensee)",
        "catalogModel": "Nokia X30 5G",
        "productLine": "Nokia X-series",
        "modelNumber": "TA-1450",
        "philippineReleaseYear": 2022,
        "philippineDateLabel": "Reported authorized Philippine retail availability date",
        "researchNotes": "Workbook row 82 'X30 5G' matches Nokia X30 5G. HMD lists model TA-1450; the same Nokia model code appears in the Philippine NTC GEC. Philippine launch reporting identifies one local retail configuration, 8 GB / 256 GB, first available through authorized retailers on October 28, 2022 at PHP 27,990. HMD's global launch date was September 1, 2022. Current Philippine price remains blank; PHP 18,990 is preserved as a June 2023 historical price observation. Storage type, microSD support, SIM/eSIM layout, and OS-upgrade count remain unresolved source conflicts. Workbook eligibility remains Pending.",
        "qualityFlag": "Exact Nokia X30 5G model and TA-1450 registration matched; local 8 GB / 256 GB availability and launch price verified from Philippine launch sources; current price unavailable; storage type, expansion, SIM/eSIM, and OS-support claims unresolved; eligibility remains Pending.",
        "openIssues": [
            {"issue": "HMD's current TA-1450 specs list two OS upgrades while its global launch release promises three", "action": "Keep OS-upgrade count unresolved until HMD clarifies regional policy."},
            {"issue": "YugaTech/Kimovil say 256 GB UFS 3.0 but a Nokia datasheet transcription says UFS 2.2", "action": "Keep storage technology blank pending authoritative clarification."},
            {"issue": "YugaTech/Kimovil report a microSD slot but GSMArena says no card slot", "action": "Keep storage expansion blank."},
            {"issue": "Physical SIM and eSIM combinations differ among model references", "action": "Keep Philippine SIM/eSIM configuration blank until a local TA-1450 unit or authoritative regional documentation is checked."},
            {"issue": "Only historical Philippine prices were verified", "action": "Keep current price blank; retain dated launch and June 2023 price observations."},
            {"issue": "HMD and Philippine news pages contain exact product images but no documented reusable license was found", "action": "Keep the neutral image placeholder until reuse rights are documented."},
            {"issue": "Workbook eligibility is Pending", "action": "Preserve the study's Pending status."},
        ],
    }


def main() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unavailable = json.loads(UNAVAILABLE_IMAGES.read_text(encoding="utf-8"))
    device = next((row for row in catalog if row.get("id") == DEVICE), None)
    if (not device or device.get("category") != "smartphones"
            or device.get("brand", "").casefold() != "nokia"
            or device.get("model", "").casefold() not in {"x30 5g", "nokia x30 5g"}):
        raise ValueError("Inventory row no longer matches Nokia X30 5G")
    variant_ids = {variant.get("id") for variant in device.get("variants", [])}
    if variant_ids - {OLD_CONFIG, CONFIG}:
        raise ValueError(f"Unexpected Nokia X30 5G configurations: {sorted(variant_ids)}")

    variant = {"id": CONFIG, "label": "8 GB RAM / 256 GB storage", "sku": None,
               "modelCode": "TA-1450",
               "notes": "Philippine launch sources report this exact local configuration at PHP 27,990 and availability through authorized retailers from October 28, 2022. A dated PHP 18,990 promotion was reported June 5, 2023. Current price is not verified. Storage type, expansion and SIM layout remain unresolved.",
               "workbookRow": 82}
    record = {
        "deviceId": DEVICE,
        "configurationId": CONFIG,
        "brand": "Nokia",
        "model": "X30 5G",
        "configuration": variant["label"],
        "configurationLabel": variant["label"],
        "modelCode": "TA-1450",
        "sources": SOURCES,
        "fields": fields_for(),
        "availabilityEvidence": availability_evidence(),
        "replacementVariants": [variant],
        "replaceUnrecordedPlaceholder": True,
    }
    manual["records"] = [row for row in manual.get("records", []) if row.get("deviceId") != DEVICE]
    manual["records"].append(record)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unavailable[DEVICE] = {
        "status": "REUSE_RIGHTS_NOT_ESTABLISHED",
        "reason": "Exact Nokia X30 5G product images are available on HMD and Philippine technology pages, but no reusable license or permission to copy/embed is recorded. Keep the neutral placeholder.",
        "sourcePage": URL_HMD_SPECS,
        "assetUrl": None,
        "scope": "Nokia X30 5G; Philippine 8 GB / 256 GB variant",
        "rightsTermsUrl": None,
        "observedAt": OBSERVED,
        "altText": "Image unavailable for Nokia X30 5G",
    }
    UNAVAILABLE_IMAGES.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prices = [
        {"device_id": DEVICE, "amount_php": 27990, "configuration_id": CONFIG,
         "configuration_match": "exact_philippine_8gb_256gb_configuration", "variant_ram_gb": 8,
         "variant_storage_gb": 256, "price_type": "historical_ph_launch_price",
         "source_published_at": "2022-10-28",
         "excerpt": "Philippine launch coverage lists PHP 27,990 for the Nokia X30 5G 8 GB / 256 GB; authorized nationwide retailers were reported to begin availability October 28, 2022.",
         "source_url": URL_YUGA, "source_kind": "historical_local_launch_price",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_launch_price_not_current"},
        {"device_id": DEVICE, "amount_php": 18990, "configuration_id": CONFIG,
         "configuration_match": "exact_philippine_8gb_256gb_configuration", "variant_ram_gb": 8,
         "variant_storage_gb": 256, "price_type": "historical_ph_price_promotion",
         "source_published_at": "2023-06-05",
         "excerpt": "NoypiGeeks reported a PHP 9,000 reduction from PHP 27,990 to PHP 18,990 for Nokia X30 5G, 8 GB RAM / 256 GB storage. Historical promotional price; no current availability inferred.",
         "source_url": URL_NOYPI, "source_kind": "dated_local_price_promotion",
         "observed_at": OBSERVED_AT, "local_availability_verified": True,
         "availability_status": "historical_promotion_not_current"},
    ]
    PRICE_SNAPSHOT.write_text(json.dumps({
        "run_at": OBSERVED_AT,
        "inventory_count": 456,
        "selected_count": 1,
        "models": [{"device_id": DEVICE, "brand": "Nokia", "model_name": "Nokia X30 5G", "category": "smartphones", "status": "manually_reviewed"}],
        "fetches": [],
        "observations": [],
        "discovery": [
            {"device_id": DEVICE, "source_url": URL_YUGA, "result": "YugaTech reports the official Philippine 8 GB / 256 GB X30 5G release at PHP 27,990 with authorized retail availability from October 28, 2022."},
            {"device_id": DEVICE, "source_url": URL_NTC, "result": "NTC's 2022 GEC includes Nokia TA-1450; HMD's exact-model specifications page identifies the same model code."},
            {"device_id": DEVICE, "source_url": URL_HMD_PRESS, "result": "HMD launched Nokia X30 5G globally September 1, 2022; it states availability from that day. GSMArena separately lists September 21 as retail release."},
            {"device_id": DEVICE, "source_url": URL_NOYPI, "result": "NoypiGeeks reported a dated June 5, 2023 historical price change from PHP 27,990 to PHP 18,990 for the 8 GB / 256 GB model."},
            {"device_id": DEVICE, "source_url": URL_HMD_SPECS, "result": "HMD's TA-1450 specifications support core hardware fields; its OS-upgrade count conflicts with the launch release and storage expansion is not specified."},
            {"device_id": DEVICE, "source_url": URL_KIMOVIL, "result": "Exact global 8/256 model page used only as a cross-check; disputed UFS type and microSD claims are not treated as settled local facts."},
        ],
        "prices": prices,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "modelMatch": "Workbook row 82 Nokia X30 5G -> HMD/Nokia TA-1450",
        "philippineConfiguration": variant["label"],
        "launchPricePhp": 27990,
        "historicalPricePhp": 18990,
        "philippineAvailabilityDate": "2022-10-28",
        "globalLaunchDate": "2022-09-01",
        "reviewedFields": len(record["fields"]),
        "currentPrice": "blank; no current orderable offer verified",
        "image": "neutral placeholder; reuse rights not established",
        "unresolved": ["storage type", "microSD support", "SIM/eSIM layout", "OS-upgrade count"],
        "scopeStatus": "Pending",
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
