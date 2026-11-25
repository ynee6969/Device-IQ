#!/usr/bin/env python3
"""Add exact-model Xiaomi/Redmi phone evidence from manufacturer sources.

Technical facts are taken from Xiaomi specification/support pages. A global or
regional specification page does not establish Philippine availability or a
Philippine price. Those fields are changed only where a Philippine page or an
active, exact-configuration local campaign supports the claim.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from add_verified_tablet_reviews import add_review, deduplicate_target_reviews, f, src  # noqa: E402

MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-26"

# The values below are transcribed from the exact official pages named here.
# Model-level facts are shared across configurations unless the official page
# says otherwise. Configurations and PH pricing are kept variant-specific.
MODELS = [
    {
        "brand": "Xiaomi", "model": "14", "url": "https://www.mi.com/global/product/xiaomi-14/specs/",
        "configs": [(12, 256), (12, 512)],
        "facts": {
            "display_size": ("6.36 inches", 6.36, "displayInches", "in"),
            "display_technology": ("AMOLED", "AMOLED", "displayType", None),
            "display_resolution": ("2670 x 1200", "2670 x 1200", "resolution", None),
            "display_refresh_rate": ("Dynamic 1–120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("1000 nits HBM typical; 3000 nits peak", "1000 nits HBM typical; 3000 nits peak", None, "nits"),
            "display_protection": ("Xiaomi-custom C8 display panel", "Xiaomi-custom C8 display panel", None, None),
            "chipset": ("Snapdragon 8 Gen 3 Mobile Platform", "Snapdragon 8 Gen 3", "chipset", None),
            "process_node": ("4 nm", 4, None, "nm"),
            "cpu": ("8-core: 1x Cortex-X4 up to 3.3 GHz, 3x Cortex-A720 up to 3.2 GHz, 2x Cortex-A720 up to 3.0 GHz, 2x Cortex-A520 up to 2.3 GHz", "8-core CPU; exact core configuration listed in official source", "cpu", None),
            "gpu": ("Qualcomm Adreno GPU", "Adreno GPU", "gpu", None),
            "rear_camera_system": ("50 MP main + 50 MP telephoto + 50 MP ultra-wide", 50, "rearCameraMp", "MP"),
            "front_camera": ("32 MP", 32, "frontCameraMp", "MP"),
            "video_recording": ("Rear up to 8K/24 fps and 4K/60 fps; front up to 4K/60 fps", "Rear up to 8K/24 fps and 4K/60 fps; front up to 4K/60 fps", "video", None),
            "battery_capacity": ("4610 mAh typical", 4610, "batteryMah", "mAh"),
            "wired_charging": ("90 W HyperCharge", 90, "chargingW", "W"),
            "dimensions": ("152.8 x 71.5 x 8.20 mm", "152.8 x 71.5 x 8.20 mm", "dimensions", "mm"),
            "weight": ("193 g", 193, "weightG", "g"),
            "operating_system": ("Xiaomi HyperOS", "Xiaomi HyperOS", "os", None),
            "rear_camera_sensor": ("Main camera: Light Fusion 900; 1/1.31-inch sensor", "Main camera Light Fusion 900; 1/1.31-inch sensor", None, None),
            "sim_esim": ("Dual SIM; nano-SIM and eSIM availability depends on region/carrier", "Dual SIM; eSIM depends on region/carrier", "sim", None),
            "wifi": ("Wi-Fi 7 capability; availability may vary by region", "Wi-Fi 7; regional availability applies", "wifi", None),
            "bluetooth": ("Bluetooth 5.4", "Bluetooth 5.4", None, None),
            "nfc": ("NFC: Yes; availability may vary by market", "Yes; market availability may vary", None, None),
            "audio": ("Stereo speakers; Dolby Atmos", "Stereo speakers; Dolby Atmos", "sound", None),
            "usb": ("USB-C 3.2 Gen 1", "USB-C 3.2 Gen 1", "ports", None),
        },
    },
    {
        "brand": "Xiaomi", "model": "15", "url": "https://www.mi.com/global/product/xiaomi-15/specs/",
        "local_url": "https://www.mi.com/ph/product/xiaomi-15/specs/", "configs": [(12, 256), (12, 512)],
        "facts": {
            "display_size": ("6.36 inches", 6.36, "displayInches", "in"),
            "display_technology": ("AMOLED", "AMOLED", "displayType", None),
            "display_resolution": ("2670 x 1200", "2670 x 1200", "resolution", None),
            "display_refresh_rate": ("1–120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("3200 nits peak, covering 25% display area", "3200 nits peak (25% display area)", None, "nits"),
            "chipset": ("Snapdragon 8 Elite Mobile Platform", "Snapdragon 8 Elite", "chipset", None),
            "process_node": ("3 nm", 3, None, "nm"),
            "cpu": ("8-core: 2x Prime up to 4.32 GHz + 6x Performance up to 3.53 GHz", "8-core CPU; 2 Prime + 6 Performance cores", "cpu", None),
            "gpu": ("Adreno GPU", "Adreno GPU", "gpu", None),
            "ram_type": ("LPDDR5X 8533 Mbps", "LPDDR5X 8533 Mbps", "ramType", None),
            "storage_type": ("UFS 4.0", "UFS 4.0", "storageType", None),
            "rear_camera_system": ("50 MP main + 50 MP telephoto + 50 MP ultra-wide", 50, "rearCameraMp", "MP"),
            "front_camera": ("32 MP", 32, "frontCameraMp", "MP"),
            "video_recording": ("Rear up to 8K/30 fps; front up to 4K/60 fps", "Rear up to 8K/30 fps; front up to 4K/60 fps", "video", None),
            "battery_capacity": ("5240 mAh typical", 5240, "batteryMah", "mAh"),
            "wired_charging": ("90 W HyperCharge", 90, "chargingW", "W"),
            "dimensions": ("152.3 x 71.2 x 8.08 mm (Black, White, Green); 8.48 mm thickness (Liquid Silver)", "152.3 x 71.2 x 8.08 mm; Liquid Silver 8.48 mm thick", "dimensions", "mm"),
            "weight": ("191 g (Black, White, Green); 192 g (Liquid Silver)", "191–192 g depending on finish", None, "g"),
            "operating_system": ("Xiaomi HyperOS 2", "Xiaomi HyperOS 2", "os", None),
            "sim_esim": ("Dual nano-SIM or nano-SIM + eSIM; regional/carrier availability applies", "Dual nano-SIM or nano-SIM + eSIM; regional/carrier availability applies", "sim", None),
            "cellular_bands": ("5G SA/NSA and 4G LTE; bands listed on the official source page", "5G SA/NSA and 4G LTE; consult source for supported bands", "cellular", None),
            "wifi": ("Wi-Fi 7 capability; availability may vary by region", "Wi-Fi 7; regional availability applies", "wifi", None),
            "bluetooth": ("Bluetooth 6.0", "Bluetooth 6.0", None, None),
            "nfc": ("NFC: Yes", "Yes", None, None),
            "audio": ("Stereo speakers; Dolby Atmos; Hi-Res Audio", "Stereo speakers; Dolby Atmos; Hi-Res Audio", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
            "ingress_protection": ("IP68", "IP68", None, None),
        },
    },
    {
        "brand": "Xiaomi", "model": "15 Ultra", "url": "https://www.mi.com/global/product/xiaomi-15-ultra/specs/",
        "local_url": "https://www.mi.com/ph/product/xiaomi-15-ultra/specs/", "configs": [(16, 512), (16, 1024)],
        "facts": {
            "display_size": ("6.73 inches", 6.73, "displayInches", "in"),
            "display_technology": ("AMOLED", "AMOLED", "displayType", None),
            "display_resolution": ("3200 x 1440", "3200 x 1440", "resolution", None),
            "display_refresh_rate": ("1–120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("3200 nits peak", "3200 nits peak", None, "nits"),
            "chipset": ("Snapdragon 8 Elite Mobile Platform", "Snapdragon 8 Elite", "chipset", None),
            "process_node": ("3 nm", 3, None, "nm"),
            "cpu": ("8-core: 2x Prime up to 4.32 GHz + 6x Performance up to 3.53 GHz", "8-core CPU; 2 Prime + 6 Performance cores", "cpu", None),
            "gpu": ("Adreno GPU", "Adreno GPU", "gpu", None),
            "ram_type": ("LPDDR5X 8533 Mbps", "LPDDR5X 8533 Mbps", "ramType", None),
            "storage_type": ("UFS 4.1", "UFS 4.1", "storageType", None),
            "rear_camera_system": ("50 MP main + 200 MP ultra telephoto + 50 MP floating telephoto + 50 MP ultra-wide", 50, "rearCameraMp", "MP"),
            "front_camera": ("32 MP", 32, "frontCameraMp", "MP"),
            "video_recording": ("Rear up to 8K/30 fps; front up to 4K/60 fps", "Rear up to 8K/30 fps; front up to 4K/60 fps", "video", None),
            "battery_capacity": ("5410 mAh typical", 5410, "batteryMah", "mAh"),
            "wired_charging": ("90 W HyperCharge", 90, "chargingW", "W"),
            "dimensions": ("161.3 x 75.3 x 9.35 mm (Black/White); 9.48 mm thickness (Silver Chrome)", "161.3 x 75.3 x 9.35 mm; Silver Chrome 9.48 mm thick", "dimensions", "mm"),
            "weight": ("226 g (Black/White); 229 g (Silver Chrome)", "226–229 g depending on finish", None, "g"),
            "operating_system": ("Xiaomi HyperOS 2", "Xiaomi HyperOS 2", "os", None),
            "sim_esim": ("Dual nano-SIM or nano-SIM + eSIM; regional/carrier availability applies", "Dual nano-SIM or nano-SIM + eSIM; regional/carrier availability applies", "sim", None),
            "cellular_bands": ("5G SA/NSA and 4G LTE; bands listed on the official source page", "5G SA/NSA and 4G LTE; consult source for supported bands", "cellular", None),
            "wifi": ("Wi-Fi 7 capability; availability may vary by region", "Wi-Fi 7; regional availability applies", "wifi", None),
            "bluetooth": ("Bluetooth 6.0", "Bluetooth 6.0", None, None),
            "nfc": ("NFC: Yes", "Yes", None, None),
            "audio": ("Stereo speakers; Dolby Atmos; Hi-Res Audio", "Stereo speakers; Dolby Atmos; Hi-Res Audio", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
            "ingress_protection": ("IP68", "IP68", None, None),
        },
    },
    {
        "brand": "Xiaomi", "model": "15T", "url": "https://www.mi.com/ph/product/xiaomi-15t/specs/",
        "local_url": "https://www.mi.com/ph/product/xiaomi-15t/", "faq_url": "https://www.mi.com/ph/support/faq/details/KA-607966/", "configs": [(12, 256), (12, 512)],
        "facts": {
            "display_size": ("6.83 inches", 6.83, "displayInches", "in"),
            "display_technology": ("AMOLED", "AMOLED", "displayType", None),
            "display_resolution": ("2772 x 1280", "2772 x 1280", "resolution", None),
            "display_refresh_rate": ("Up to 120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("3200 nits peak over 25% display area", "3200 nits peak over 25% display area", None, "nits"),
            "display_protection": ("Corning Gorilla Glass 7i", "Corning Gorilla Glass 7i", None, None),
            "chipset": ("MediaTek Dimensity 8400-Ultra", "MediaTek Dimensity 8400-Ultra", "chipset", None),
            "process_node": ("4 nm", 4, None, "nm"),
            "cpu": ("8-core: 1x Cortex-A725 up to 3.25 GHz + 3x Cortex-A725 up to 3.0 GHz + 4x Cortex-A725 up to 2.1 GHz", "8-core CPU; Cortex-A725 configuration listed in official source", "cpu", None),
            "gpu": ("Mali-G720", "Mali-G720", "gpu", None),
            "ram_type": ("LPDDR5X 8533 Mbps", "LPDDR5X 8533 Mbps", "ramType", None),
            "storage_type": ("UFS 4.1", "UFS 4.1", "storageType", None),
            "rear_camera_system": ("50 MP main + 50 MP telephoto + 12 MP ultra-wide", 50, "rearCameraMp", "MP"),
            "front_camera": ("32 MP", 32, "frontCameraMp", "MP"),
            "video_recording": ("Rear up to 4K/60 fps; front up to 4K/30 fps", "Rear up to 4K/60 fps; front up to 4K/30 fps", "video", None),
            "battery_capacity": ("5500 mAh typical", 5500, "batteryMah", "mAh"),
            "wired_charging": ("67 W HyperCharge", 67, "chargingW", "W"),
            "dimensions": ("163.2 x 78.0 x 7.50 mm", "163.2 x 78.0 x 7.50 mm", "dimensions", "mm"),
            "weight": ("194 g", 194, "weightG", "g"),
            "operating_system": ("Xiaomi HyperOS 2", "Xiaomi HyperOS 2", "os", None),
            "sim_esim": ("Dual nano-SIM or nano-SIM + eSIM; eSIM availability depends on region/carrier", "Dual SIM; eSIM availability depends on region/carrier", "sim", None),
            "cellular_bands": ("5G SA/NSA and 4G LTE; bands listed on the official Philippine source page", "5G SA/NSA and 4G LTE; consult source for supported bands", "cellular", None),
            "wifi": ("Wi-Fi 6E; capabilities may vary by region/network", "Wi-Fi 6E; regional capability applies", "wifi", None),
            "bluetooth": ("Bluetooth 6.0", "Bluetooth 6.0", None, None),
            "nfc": ("NFC: Yes", "Yes", None, None),
            "audio": ("Dual speakers; Dolby Atmos; Hi-Res Audio", "Dual speakers; Dolby Atmos; Hi-Res Audio", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
            "ingress_protection": ("IP68", "IP68", None, None),
        },
    },
    {
        "brand": "Xiaomi", "model": "15T Pro", "url": "https://www.mi.com/ph/product/xiaomi-15t-pro/specs/",
        "local_url": "https://www.mi.com/ph/product/xiaomi-15t-pro/", "configs": [(12, 256), (12, 512)],
        "facts": {
            "display_size": ("6.83 inches", 6.83, "displayInches", "in"),
            "display_technology": ("AMOLED", "AMOLED", "displayType", None),
            "display_resolution": ("2772 x 1280", "2772 x 1280", "resolution", None),
            "display_refresh_rate": ("Up to 144 Hz", 144, "refreshHz", "Hz"),
            "display_brightness": ("3200 nits peak over 25% display area", "3200 nits peak over 25% display area", None, "nits"),
            "display_protection": ("Corning Gorilla Glass 7i", "Corning Gorilla Glass 7i", None, None),
            "chipset": ("MediaTek Dimensity 9400+", "MediaTek Dimensity 9400+", "chipset", None),
            "process_node": ("3 nm", 3, None, "nm"),
            "cpu": ("8-core: 1x Cortex-X925 up to 3.73 GHz + 3x Cortex-X4 up to 3.3 GHz + 4x Cortex-A720 up to 2.4 GHz", "8-core CPU; exact core configuration listed in official source", "cpu", None),
            "gpu": ("Immortalis-G925 MC12", "Immortalis-G925 MC12", "gpu", None),
            "ram_type": ("LPDDR5X", "LPDDR5X", "ramType", None),
            "storage_type": ("UFS 4.1", "UFS 4.1", "storageType", None),
            "rear_camera_system": ("50 MP main + 50 MP 5x telephoto + 12 MP ultra-wide", 50, "rearCameraMp", "MP"),
            "front_camera": ("32 MP", 32, "frontCameraMp", "MP"),
            "video_recording": ("Rear up to 8K/30 fps; front up to 4K/30 fps", "Rear up to 8K/30 fps; front up to 4K/30 fps", "video", None),
            "battery_capacity": ("5500 mAh typical", 5500, "batteryMah", "mAh"),
            "wired_charging": ("90 W HyperCharge", 90, "chargingW", "W"),
            "dimensions": ("162.7 x 77.9 x 7.96 mm", "162.7 x 77.9 x 7.96 mm", "dimensions", "mm"),
            "weight": ("210 g", 210, "weightG", "g"),
            "operating_system": ("Xiaomi HyperOS 2", "Xiaomi HyperOS 2", "os", None),
            "sim_esim": ("Dual nano-SIM or nano-SIM + eSIM; eSIM availability depends on region/carrier", "Dual SIM; eSIM availability depends on region/carrier", "sim", None),
            "cellular_bands": ("5G SA/NSA and 4G LTE; bands listed on the official Philippine source page", "5G SA/NSA and 4G LTE; consult source for supported bands", "cellular", None),
            "wifi": ("Wi-Fi 7 capability; availability may vary by region", "Wi-Fi 7; regional availability applies", "wifi", None),
            "bluetooth": ("Bluetooth 6.0", "Bluetooth 6.0", None, None),
            "nfc": ("NFC: Yes", "Yes", None, None),
            "audio": ("Dual speakers; Dolby Atmos; Hi-Res Audio", "Dual speakers; Dolby Atmos; Hi-Res Audio", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
            "ingress_protection": ("IP68", "IP68", None, None),
        },
    },
    {
        "brand": "Redmi", "model": "12C", "url": "https://www.mi.com/sg/product/redmi-12c/specs/",
        "configs": [(3, 32), (3, 64), (4, 64), (4, 128), (6, 128)],
        "facts": {
            "display_size": ("6.71 inches", 6.71, "displayInches", "in"),
            "display_resolution": ("1650 x 720", "1650 x 720", "resolution", None),
            "display_technology": ("Dot Drop display", "Dot Drop display", "displayType", None),
            "display_brightness": ("500 nits typical", "500 nits typical", None, "nits"),
            "chipset": ("MediaTek Helio G85", "MediaTek Helio G85", "chipset", None),
            "process_node": ("12 nm", 12, None, "nm"),
            "cpu": ("Octa-core up to 2.0 GHz", "Octa-core up to 2.0 GHz", "cpu", None),
            "gpu": ("Mali-G52 MC2", "Mali-G52 MC2", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("eMMC 5.1", "eMMC 5.1", "storageType", None),
            "storage_expansion": ("Expandable storage up to 1 TB", "microSD expansion up to 1 TB", None, None),
            "rear_camera_system": ("50 MP main camera and auxiliary QVGA lens", 50, "rearCameraMp", "MP"),
            "front_camera": ("5 MP", 5, "frontCameraMp", "MP"),
            "video_recording": ("Rear and front up to 1080p/30 fps", "Rear and front up to 1080p/30 fps", "video", None),
            "battery_capacity": ("5000 mAh typical", 5000, "batteryMah", "mAh"),
            "wired_charging": ("10 W fast charging", 10, "chargingW", "W"),
            "dimensions": ("168.76 x 76.41 x 8.77 mm", "168.76 x 76.41 x 8.77 mm", "dimensions", "mm"),
            "weight": ("192 g", 192, "weightG", "g"),
            "operating_system": ("MIUI 13 based on Android 12", "MIUI 13 based on Android 12", "os", None),
            "sim_esim": ("Dual SIM + microSD", "Dual SIM + microSD", "sim", None),
            "cellular_bands": ("4G LTE, 3G WCDMA and 2G GSM; bands listed on source page", "4G LTE/3G/2G; consult source for supported bands", "cellular", None),
            "wifi": ("802.11a/b/g/n/ac", "Wi-Fi 5 (802.11ac)", "wifi", None),
            "bluetooth": ("Bluetooth 5.1", "Bluetooth 5.1", None, None),
            "audio": ("3.5 mm headphone jack", "3.5 mm headphone jack", "sound", None),
            "usb": ("Micro USB", "Micro USB", "ports", None),
        },
    },
    {
        "brand": "Redmi", "model": "13C", "url": "https://www.mi.com/in/product/redmi-13c/specs/",
        "faq_url": "https://www.mi.com/global/support/faq/details/KA-47262/", "configs": [(4, 128), (6, 128), (8, 256)],
        "facts": {
            "display_size": ("6.74 inches", 6.74, "displayInches", "in"),
            "display_resolution": ("1600 x 720", "1600 x 720", "resolution", None),
            "display_technology": ("Dot Drop display", "Dot Drop display", "displayType", None),
            "display_refresh_rate": ("Up to 90 Hz", 90, "refreshHz", "Hz"),
            "display_brightness": ("450 nits typical; 600 nits HBM", "450 nits typical; 600 nits HBM", None, "nits"),
            "display_protection": ("Corning Gorilla Glass", "Corning Gorilla Glass", None, None),
            "chipset": ("MediaTek Helio G85", "MediaTek Helio G85", "chipset", None),
            "process_node": ("12 nm", 12, None, "nm"),
            "cpu": ("Octa-core: Cortex-A75 up to 2.0 GHz + Cortex-A55 up to 1.8 GHz", "Octa-core; Cortex-A75/A55 up to 2.0 GHz", "cpu", None),
            "gpu": ("Mali-G52 MC2", "Mali-G52 MC2", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("eMMC 5.1", "eMMC 5.1", "storageType", None),
            "rear_camera_system": ("50 MP main + 2 MP macro + auxiliary lens", 50, "rearCameraMp", "MP"),
            "front_camera": ("8 MP", 8, "frontCameraMp", "MP"),
            "video_recording": ("Rear and front up to 1080p/30 fps", "Rear and front up to 1080p/30 fps", "video", None),
            "battery_capacity": ("5000 mAh typical", 5000, "batteryMah", "mAh"),
            "wired_charging": ("18 W fast charging", 18, "chargingW", "W"),
            "dimensions": ("168 x 78 x 8.09 mm", "168 x 78 x 8.09 mm", "dimensions", "mm"),
            "weight": ("192 g", 192, "weightG", "g"),
            "operating_system": ("MIUI 14 based on Android 13", "MIUI 14 based on Android 13", "os", None),
            "sim_esim": ("Dual SIM + microSD", "Dual SIM + microSD", "sim", None),
            "cellular_bands": ("4G LTE, 3G WCDMA and 2G GSM; bands listed on source page", "4G LTE/3G/2G; consult source for supported bands", "cellular", None),
            "wifi": ("802.11a/b/g/n/ac", "Wi-Fi 5 (802.11ac)", "wifi", None),
            "bluetooth": ("Bluetooth 5.3", "Bluetooth 5.3", None, None),
            "audio": ("3.5 mm headphone jack", "3.5 mm headphone jack", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
        },
    },
    {
        "brand": "Redmi", "model": "13", "url": "https://www.mi.com/global/product/redmi-13/specs/",
        "faq_url": "https://www.mi.com/ph/support/faq/details/KA-206710/", "configs": [(6, 128), (8, 128), (8, 256)],
        "facts": {
            "display_size": ("6.79 inches", 6.79, "displayInches", "in"),
            "display_technology": ("DotDisplay", "DotDisplay", "displayType", None),
            "display_resolution": ("2460 x 1080", "2460 x 1080", "resolution", None),
            "display_refresh_rate": ("Up to 90 Hz", 90, "refreshHz", "Hz"),
            "display_brightness": ("450 nits typical; 550 nits HBM", "450 nits typical; 550 nits HBM", None, "nits"),
            "display_protection": ("Corning Gorilla Glass 3", "Corning Gorilla Glass 3", None, None),
            "chipset": ("MediaTek Helio G91-Ultra", "MediaTek Helio G91-Ultra", "chipset", None),
            "process_node": ("12 nm", 12, None, "nm"),
            "cpu": ("Octa-core: 2x Cortex-A75 up to 2.0 GHz + 6x Cortex-A55 up to 1.8 GHz", "Octa-core; 2x A75 + 6x A55", "cpu", None),
            "gpu": ("Mali-G52 MC2", "Mali-G52 MC2", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("eMMC 5.1", "eMMC 5.1", "storageType", None),
            "storage_expansion": ("Expandable storage up to 1 TB", "microSD expansion up to 1 TB", None, None),
            "rear_camera_system": ("108 MP main + 2 MP macro", 108, "rearCameraMp", "MP"),
            "front_camera": ("13 MP", 13, "frontCameraMp", "MP"),
            "video_recording": ("Rear and front up to 1080p/30 fps", "Rear and front up to 1080p/30 fps", "video", None),
            "battery_capacity": ("5030 mAh typical", 5030, "batteryMah", "mAh"),
            "wired_charging": ("33 W fast charging", 33, "chargingW", "W"),
            "dimensions": ("168.6 x 76.28 x 8.3 mm", "168.6 x 76.28 x 8.3 mm", "dimensions", "mm"),
            "weight": ("205 g", 205, "weightG", "g"),
            "operating_system": ("Xiaomi HyperOS", "Xiaomi HyperOS", "os", None),
            "sim_esim": ("SIM 1 + hybrid SIM/microSD slot", "Dual SIM via hybrid slot; microSD shares slot", "sim", None),
            "cellular_bands": ("4G LTE, 3G WCDMA and 2G GSM; bands listed on official source", "4G LTE/3G/2G; consult source for supported bands", "cellular", None),
            "wifi": ("2.4 GHz and 5 GHz Wi-Fi; 802.11 a/b/g/n/ac", "Wi-Fi 5 (802.11ac)", "wifi", None),
            "bluetooth": ("Bluetooth 5.4", "Bluetooth 5.4", None, None),
            "nfc": ("NFC: Yes; availability varies by market", "Yes; market availability may vary", None, None),
            "audio": ("3.5 mm headphone jack", "3.5 mm headphone jack", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
        },
    },
    {
        "brand": "Redmi", "model": "14C", "url": "https://www.mi.com/ph/product/redmi-14-c/specs/",
        "local_url": "https://www.mi.com/ph/product/redmi-14-c/", "configs": [(4, 128), (6, 128), (8, 256)],
        "facts": {
            "display_size": ("6.88 inches", 6.88, "displayInches", "in"),
            "display_technology": ("Dot Drop display", "Dot Drop display", "displayType", None),
            "display_resolution": ("1640 x 720", "1640 x 720", "resolution", None),
            "display_refresh_rate": ("Up to 120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("450 nits typical; 600 nits HBM", "450 nits typical; 600 nits HBM", None, "nits"),
            "chipset": ("MediaTek Helio G81-Ultra", "MediaTek Helio G81-Ultra", "chipset", None),
            "cpu": ("Octa-core: Cortex-A75 + Cortex-A55, up to 2.0 GHz", "Octa-core up to 2.0 GHz", "cpu", None),
            "gpu": ("Mali-G52 MC2", "Mali-G52 MC2", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("eMMC 5.1", "eMMC 5.1", "storageType", None),
            "rear_camera_system": ("50 MP main camera and auxiliary lens", "50 MP main camera; auxiliary lens", "rearCameraMp", "MP"),
            "front_camera": ("13 MP", 13, "frontCameraMp", "MP"),
            "video_recording": ("Rear and front up to 1080p/30 fps", "Rear and front up to 1080p/30 fps", "video", None),
            "battery_capacity": ("5160 mAh typical", 5160, "batteryMah", "mAh"),
            "wired_charging": ("18 W fast charging", 18, "chargingW", "W"),
            "dimensions": ("171.88 x 77.8 x 8.22 mm", "171.88 x 77.8 x 8.22 mm", "dimensions", "mm"),
            "weight": ("204 g (Starry Blue), 207 g (Sage Green), 211 g (Midnight Black/Dreamy Purple)", "204–211 g depending on color", None, "g"),
            "operating_system": ("Xiaomi HyperOS", "Xiaomi HyperOS", "os", None),
            "sim_esim": ("Dual SIM + microSD", "Dual SIM + microSD", "sim", None),
            "cellular_bands": ("4G LTE, 3G WCDMA and 2G GSM; bands listed on official page", "4G LTE/3G/2G; consult source for supported bands", "cellular", None),
            "wifi": ("2.4 GHz and 5 GHz Wi-Fi", "Dual-band 2.4/5 GHz Wi-Fi", "wifi", None),
            "bluetooth": ("Bluetooth 5.4", "Bluetooth 5.4", None, None),
            "audio": ("3.5 mm headphone jack", "3.5 mm headphone jack", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
        },
    },
    {
        "brand": "Redmi", "model": "15C", "url": "https://www.mi.com/global/product/redmi-15c/specs/",
        "local_url": "https://www.mi.com/ph/product/redmi-15c/", "configs": [(4, 128), (4, 256), (6, 128), (8, 256)],
        "facts": {
            "display_size": ("6.9 inches", 6.9, "displayInches", "in"),
            "display_technology": ("IPS LCD", "IPS LCD", "displayType", None),
            "display_resolution": ("1600 x 720", "1600 x 720", "resolution", None),
            "display_refresh_rate": ("Up to 120 Hz", 120, "refreshHz", "Hz"),
            "chipset": ("MediaTek Helio G81-Ultra", "MediaTek Helio G81-Ultra", "chipset", None),
            "cpu": ("Octa-core: Cortex-A75 + Cortex-A55, up to 2.0 GHz", "Octa-core up to 2.0 GHz", "cpu", None),
            "gpu": ("Mali-G52 MC2", "Mali-G52 MC2", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("eMMC 5.1", "eMMC 5.1", "storageType", None),
            "storage_expansion": ("microSD expansion up to 1 TB", "microSD expansion up to 1 TB", None, None),
            "rear_camera_system": ("50 MP AI dual camera system", 50, "rearCameraMp", "MP"),
            "battery_capacity": ("6000 mAh typical", 6000, "batteryMah", "mAh"),
            "wired_charging": ("33 W turbo charging", 33, "chargingW", "W"),
            "operating_system": ("Xiaomi HyperOS 2", "Xiaomi HyperOS 2", "os", None),
            "ingress_protection": ("IP64", "IP64", None, None),
        },
    },
    {
        "brand": "Redmi", "model": "Note 14", "url": "https://www.mi.com/ph/product/redmi-note-14/specs/",
        "local_url": "https://www.mi.com/ph/product/redmi-note-14/", "configs": [(6, 128), (8, 128), (8, 256)],
        "facts": {
            "display_size": ("6.67 inches", 6.67, "displayInches", "in"),
            "display_technology": ("AMOLED", "AMOLED", "displayType", None),
            "display_resolution": ("2400 x 1080", "2400 x 1080", "resolution", None),
            "display_refresh_rate": ("Up to 120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("1200 nits HBM typical; 1800 nits peak", "1200 nits HBM typical; 1800 nits peak", None, "nits"),
            "display_protection": ("Corning Gorilla Glass 5", "Corning Gorilla Glass 5", None, None),
            "chipset": ("MediaTek Helio G99-Ultra", "MediaTek Helio G99-Ultra", "chipset", None),
            "process_node": ("6 nm", 6, None, "nm"),
            "cpu": ("Octa-core up to 2.2 GHz", "Octa-core up to 2.2 GHz", "cpu", None),
            "gpu": ("Mali-G57 MC2", "Mali-G57 MC2", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("UFS 2.2", "UFS 2.2", "storageType", None),
            "rear_camera_system": ("108 MP main + 2 MP depth + 2 MP macro", "108 MP main, 2 MP depth, 2 MP macro", "rearCameraMp", "MP"),
            "front_camera": ("20 MP", 20, "frontCameraMp", "MP"),
            "video_recording": ("Rear up to 1080p/60 fps; front up to 1080p/30 fps", "Rear up to 1080p/60 fps; front up to 1080p/30 fps", "video", None),
            "battery_capacity": ("5500 mAh typical", 5500, "batteryMah", "mAh"),
            "wired_charging": ("33 W turbo charging", 33, "chargingW", "W"),
            "dimensions": ("163.25 x 76.55 x 8.16 mm", "163.25 x 76.55 x 8.16 mm", "dimensions", "mm"),
            "weight": ("196.5 g", 196.5, "weightG", "g"),
            "operating_system": ("Xiaomi HyperOS", "Xiaomi HyperOS", "os", None),
            "sim_esim": ("SIM 1 + hybrid SIM/microSD; dual standby", "Dual SIM via hybrid slot; microSD shares slot", "sim", None),
            "cellular_bands": ("4G LTE/3G/2G; supported bands listed on the official PH page", "4G LTE/3G/2G; consult source for supported bands", "cellular", None),
            "wifi": ("802.11 a/b/g/n/ac; 2.4/5 GHz", "Wi-Fi 5 (802.11ac)", "wifi", None),
            "bluetooth": ("Bluetooth 5.3", "Bluetooth 5.3", None, None),
            "nfc": ("NFC: Yes; feature may vary by market", "Yes; market availability may vary", None, None),
            "audio": ("Dual speakers; Dolby Atmos; 3.5 mm headphone jack", "Dual speakers; Dolby Atmos; 3.5 mm headphone jack", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
            "ingress_protection": ("IP54", "IP54", None, None),
        },
        "promo": {"config": (6, 128), "price": 7999, "srp": 9499,
                  "url": "https://www.mi.com/ph/support/terms/11-11-mega-sale/"},
    },
    {
        "brand": "Redmi", "model": "Note 14 5G", "url": "https://www.mi.com/global/product/redmi-note-14-5g/specs/",
        "configs": [(6, 128), (8, 256), (12, 512)],
        "facts": {
            "display_size": ("6.67 inches", 6.67, "displayInches", "in"),
            "display_technology": ("AMOLED", "AMOLED", "displayType", None),
            "display_resolution": ("2400 x 1080", "2400 x 1080", "resolution", None),
            "display_refresh_rate": ("Up to 120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("1200 nits HBM; 2100 nits peak", "1200 nits HBM; 2100 nits peak", None, "nits"),
            "display_protection": ("Corning Gorilla Glass 5", "Corning Gorilla Glass 5", None, None),
            "chipset": ("MediaTek Dimensity 7025-Ultra", "MediaTek Dimensity 7025-Ultra", "chipset", None),
            "process_node": ("6 nm", 6, None, "nm"),
            "cpu": ("Octa-core up to 2.5 GHz", "Octa-core up to 2.5 GHz", "cpu", None),
            "gpu": ("IMG BXM-8-256", "IMG BXM-8-256", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("UFS 2.2", "UFS 2.2", "storageType", None),
            "storage_expansion": ("microSD expansion up to 1 TB", "microSD expansion up to 1 TB", None, None),
            "rear_camera_system": ("108 MP main + 8 MP ultra-wide + 2 MP macro", 108, "rearCameraMp", "MP"),
            "front_camera": ("20 MP", 20, "frontCameraMp", "MP"),
            "video_recording": ("Rear and front up to 1080p/30 fps", "Rear and front up to 1080p/30 fps", "video", None),
            "battery_capacity": ("5110 mAh typical", 5110, "batteryMah", "mAh"),
            "wired_charging": ("45 W turbo charging", 45, "chargingW", "W"),
            "dimensions": ("162.4 x 75.7 x 7.99 mm", "162.4 x 75.7 x 7.99 mm", "dimensions", "mm"),
            "weight": ("190 g", 190, "weightG", "g"),
            "operating_system": ("Xiaomi HyperOS", "Xiaomi HyperOS", "os", None),
            "sim_esim": ("SIM 1 + hybrid SIM/microSD; dual standby", "Dual SIM via hybrid slot; microSD shares slot", "sim", None),
            "cellular_bands": ("5G/4G/3G/2G; bands listed on official source page", "5G/4G/3G/2G; consult source for supported bands", "cellular", None),
            "wifi": ("802.11a/b/g/n/ac; dual-band", "Wi-Fi 5 (802.11ac)", "wifi", None),
            "bluetooth": ("Bluetooth 5.3", "Bluetooth 5.3", None, None),
            "audio": ("Dual speakers; Dolby Atmos; 3.5 mm headphone jack", "Dual speakers; Dolby Atmos; 3.5 mm headphone jack", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
            "ingress_protection": ("IP64", "IP64", None, None),
        },
    },
    {
        "brand": "Redmi", "model": "Note 14 Pro 5G", "url": "https://www.mi.com/global/product/redmi-note-14-pro-5g/specs/",
        "configs": [(8, 256), (12, 256), (12, 512)],
        "facts": {
            "display_size": ("6.67 inches", 6.67, "displayInches", "in"),
            "display_technology": ("CrystalRes AMOLED", "CrystalRes AMOLED", "displayType", None),
            "display_resolution": ("2712 x 1220", "2712 x 1220", "resolution", None),
            "display_refresh_rate": ("Up to 120 Hz", 120, "refreshHz", "Hz"),
            "display_brightness": ("3000 nits peak", "3000 nits peak", None, "nits"),
            "display_protection": ("Corning Gorilla Glass Victus 2", "Corning Gorilla Glass Victus 2", None, None),
            "chipset": ("MediaTek Dimensity 7300-Ultra", "MediaTek Dimensity 7300-Ultra", "chipset", None),
            "process_node": ("4 nm", 4, None, "nm"),
            "cpu": ("Octa-core up to 2.5 GHz", "Octa-core up to 2.5 GHz", "cpu", None),
            "gpu": ("Mali-G615 MC2", "Mali-G615 MC2", "gpu", None),
            "ram_type": ("LPDDR4X", "LPDDR4X", "ramType", None),
            "storage_type": ("UFS 2.2", "UFS 2.2", "storageType", None),
            "rear_camera_system": ("200 MP main with OIS + 8 MP ultra-wide + 2 MP macro", 200, "rearCameraMp", "MP"),
            "front_camera": ("20 MP", 20, "frontCameraMp", "MP"),
            "video_recording": ("Rear up to 4K/30 fps; front up to 1080p/60 fps", "Rear up to 4K/30 fps; front up to 1080p/60 fps", "video", None),
            "battery_capacity": ("5110 mAh typical", 5110, "batteryMah", "mAh"),
            "wired_charging": ("45 W turbo charging", 45, "chargingW", "W"),
            "dimensions": ("162.33 x 74.42 x 8.40 mm (most colors); Lavender Purple 8.55 mm thick", "162.33 x 74.42 x 8.40 mm; Lavender Purple 8.55 mm thick", "dimensions", "mm"),
            "weight": ("190 g", 190, "weightG", "g"),
            "operating_system": ("Xiaomi HyperOS", "Xiaomi HyperOS", "os", None),
            "sim_esim": ("Dual nano-SIM or nano-SIM + eSIM; eSIM varies by region/carrier", "Dual SIM; eSIM availability depends on region/carrier", "sim", None),
            "cellular_bands": ("5G/4G/3G/2G; bands listed on official source page", "5G/4G/3G/2G; consult source for supported bands", "cellular", None),
            "wifi": ("Wi-Fi 6/5/4 and 802.11a/b/g", "Wi-Fi 6", "wifi", None),
            "bluetooth": ("Bluetooth 5.4", "Bluetooth 5.4", None, None),
            "nfc": ("NFC: Yes; availability may vary by market", "Yes; market availability may vary", None, None),
            "audio": ("Dual speakers; Dolby Atmos", "Dual speakers; Dolby Atmos", "sound", None),
            "usb": ("USB Type-C", "USB Type-C", "ports", None),
            "ingress_protection": ("IP68", "IP68", None, None),
        },
    },
]


def configuration_from_label(label: str):
    match = re.search(r"(\d+)\s*GB\s*RAM\s*/\s*(\d+)\s*GB\s*storage", label, re.I)
    return (int(match.group(1)), int(match.group(2))) if match else None


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    device_by_identity = {(d["brand"], d["model"]): d for d in catalog if d.get("recordType") == "device"}
    records = []
    for model in MODELS:
        device = device_by_identity.get((model["brand"], model["model"]))
        if not device:
            raise ValueError(f"Exact workbook model missing: {model['brand']} {model['model']}")
        spec_id = f"xiaomi_{re.sub(r'[^a-z0-9]+', '_', model['brand'].lower() + '_' + model['model'].lower()).strip('_')}_official_specs"
        source_list = [src(spec_id, model["url"], "Manufacturer product specifications",
                           "Technical facts transcribed from the exact Xiaomi/Redmi model specification page. Regional configuration availability and Philippine release date are not inferred from a global or third-country spec page.",
                           publisher="Xiaomi" if "/ph/" not in model["url"] else "Xiaomi Philippines")]
        local_id = None
        if model.get("local_url"):
            local_id = f"xiaomi_{re.sub(r'[^a-z0-9]+', '_', model['brand'].lower() + '_' + model['model'].lower()).strip('_')}_ph_product"
            source_list.append(src(local_id, model["local_url"], "Official Philippine product page",
                                   "Official Xiaomi Philippines model page confirms a local product page, but not the date of first sale or an exact local price.", publisher="Xiaomi Philippines"))
        faq_id = None
        if model.get("faq_url"):
            faq_id = f"xiaomi_{re.sub(r'[^a-z0-9]+', '_', model['brand'].lower() + '_' + model['model'].lower()).strip('_')}_official_faq"
            source_list.append(src(faq_id, model["faq_url"], "Manufacturer support FAQ",
                                   "Model-specific Xiaomi support FAQ checked for technical information. A localized FAQ does not establish a first Philippine sale date.", publisher="Xiaomi support"))
        promo_id = None
        if model.get("promo"):
            promo_id = "xiaomi_ph_2026_11_11_sale_terms"
            source_list.append(src(promo_id, model["promo"]["url"], "Official Philippine campaign price table",
                                   "Campaign section lists SRP and sale price for the exact REDMI Note 14 6 GB + 128 GB black variant; PHP 7,999 is valid Nov 12–26 and Nov 28–30, 2026.", publisher="Xiaomi Philippines"))

        for variant in device.get("variants", []):
            cfg = configuration_from_label(variant.get("label", ""))
            fields = []
            if cfg and cfg in model.get("configs", []):
                fields.append(f("configuration", spec_id, f"{cfg[0]} GB RAM + {cfg[1]} GB storage", variant["label"],
                                note="The exact RAM/storage configuration is listed on the cited manufacturer specification page. This does not by itself establish local sale of that configuration in the Philippines."))
                fields.append(f("ram_capacity", spec_id, f"{cfg[0]} GB", cfg[0], key="ramGb", unit="GB"))
                fields.append(f("storage_capacity", spec_id, f"{cfg[1]} GB", cfg[1], key="storageGb", unit="GB"))
            for field_id, (raw, normalized, key, unit) in model["facts"].items():
                # An empty/unknown value is not recorded as a fabricated fact.
                if normalized is None:
                    fields.append(f(field_id, spec_id, raw, None, status="NOT_DISCLOSED", unit=unit,
                                    note="The cited manufacturer page did not publish a value for this field."))
                    continue
                # Some facts vary by finish; keep the sourced range in audit only.
                fields.append(f(field_id, spec_id, raw, normalized, key=key, unit=unit,
                                note="Exact model-level value from Xiaomi's official specification page; any regional variation noted in the source remains applicable."))
            if model.get("promo") and cfg == model["promo"]["config"]:
                promo = model["promo"]
                fields.append(f("current_price_php", promo_id,
                                f"SRP PHP {promo['srp']:,}; active campaign price PHP {promo['price']:,}", promo["price"], unit="PHP",
                                price_condition="new", price_type="Official Xiaomi Philippines campaign price; SRP shown alongside; valid Nov 12–26 and Nov 28–30, 2026",
                                price_observed=OBSERVED,
                                note="The terms list the exact REDMI Note 14 Black 6 GB + 128 GB row. Observation made Nov 25, 2026 during the active promotion."))
            item = {"deviceId": device["id"], "configurationId": variant["id"],
                    "brand": model["brand"], "model": model["model"],
                    "configuration": variant.get("label"), "sources": source_list, "fields": fields}
            if model.get("local_url"):
                item["availabilityEvidence"] = {
                    "verificationStatus": "VERIFIED_AUTHORIZED_AVAILABILITY",
                    "availabilityStatus": "Listed on official Xiaomi Philippines product page; observed 2026-11-25.",
                    "philippineAvailability": "Official Xiaomi Philippines product page for this model observed 2026-11-25. The page does not establish original Philippine launch/first-sale date or price.",
                    "observedAt": OBSERVED,
                    "qualityFlag": "Philippine launch or first-sale date not recorded",
                }
            records.append(item)

    target_keys = set()
    for item in records:
        add_review(manual, catalog, item)
        target_keys.add((item["deviceId"], item["configurationId"]))
    # This independently documented local 8 GB / 128 GB Redmi Note 14 Pro 5G
    # configuration is absent from the workbook's configurations sheet. Keep
    # it as a separate, explicitly secondary-sourced variant so a catalog
    # rebuild does not discard its dated Philippine price record.
    parent = next((r for r in manual["records"] if r["deviceId"] == "device_b4990c6cf5cce8"
                   and r["configurationId"] == "config_17fbad37e49629"), None)
    if parent is None:
        raise ValueError("Missing exact workbook variant for Redmi Note 14 Pro 5G")
    additional = parent.setdefault("additionalVariants", [])
    variant_id = "device_b4990c6cf5cce8-auto-8gb-128gb"
    if not any(v.get("id") == variant_id for v in additional):
        additional.append({"id": variant_id, "label": "8 GB RAM / 128 GB storage",
                           "sku": None, "modelCode": None,
                           "notes": "Distinct configuration and historical Philippine price documented by Pinoy Techno Guide (2025-01-15); not listed in the current Xiaomi global configuration table."})
    deduplicate_target_reviews(manual, target_keys)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"modelsReviewed": len(MODELS), "configurationsReviewed": len(records),
                      "verifiedFieldRowsAdded": sum(len(r["fields"]) for r in records), "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
