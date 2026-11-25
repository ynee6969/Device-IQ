#!/usr/bin/env python3
"""Add source-backed laptop reviews discovered during the 2026-11-25 pass.

This is an idempotent source-data update. It adds only fields explicitly shown
on the cited manufacturer pages, and keeps announcement pricing dated.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
OBSERVED = "2026-11-25"


def source(sid, publisher, url, purpose, note, published=None):
    return {
        "id": sid, "publisher": publisher, "url": url,
        "publicationDate": published, "accessDate": OBSERVED,
        "purpose": purpose, "note": note,
    }


def field(fid, sid, source_value, normalized, *, key=None, unit=None, note=None,
          price_condition=None, price_type=None, price_observed=None):
    row = {
        "fieldId": fid, "status": "VERIFIED", "sourceId": sid,
        "sourceValue": source_value, "normalizedValue": normalized,
        "note": note or "Exact model or Philippine SKU checked against the cited manufacturer source.",
    }
    if unit is not None:
        row["unit"] = unit
    if key:
        row["catalogKey"] = key
        row["catalogValue"] = normalized
    if price_condition:
        row["priceCondition"] = price_condition
    if price_type:
        row["priceType"] = price_type
    if price_observed:
        row["priceObservedAt"] = price_observed
    return row


def add_manual_field(manual, existing_catalog, device_id, configuration_id, record):
    key = (device_id, configuration_id)
    device = next((d for d in existing_catalog if d["id"] == device_id), {})
    variant = next((v for v in device.get("variants", []) if v["id"] == configuration_id), None)
    review = next((r for r in manual["records"] if (r["deviceId"], r["configurationId"]) == key), None)
    if review is None:
        review = {
            "deviceId": device_id, "configurationId": configuration_id,
            "brand": record.get("brand") or device.get("brand"),
            "model": record.get("model") or device.get("model"),
            "configuration": record.get("configuration"),
            "configurationLabel": record.get("configurationLabel") or (variant or {}).get("label"),
            "sources": [], "fields": [],
        }
        manual["records"].append(review)
    for s in record.get("sources", []):
        if not any(x.get("id") == s["id"] for x in review["sources"]):
            review["sources"].append(s)
    existing_fields = {r.get("fieldId"): index for index, r in enumerate(review.get("fields", []))}
    for f in record.get("fields", []):
        if f["fieldId"] in existing_fields:
            previous = review["fields"][existing_fields[f["fieldId"]]]
            # A later exact-SKU review may add a public catalog mapping to a
            # previously audit-only field. Keep the source-backed refinement.
            if f.get("catalogKey") and not previous.get("catalogKey"):
                review["fields"][existing_fields[f["fieldId"]]] = f
            continue
        if f.get("catalogKey") and variant:
            old = (variant.get("specs") or {}).get(f["catalogKey"])
            if old is not None and str(old) != str(f.get("catalogValue")):
                # This replacement is backed by the exact SKU's official page.
                f["replaceExisting"] = True
        review["fields"].append(f)
        existing_fields[f["fieldId"]] = len(review["fields"]) - 1
    if record.get("replacementVariants"):
        review["replacementVariants"] = record["replacementVariants"]


def acer_records():
    data = [
        ("device_036b026407d2a9", "config_503035c068c969", "Aspire Go 15 AI AG15-43P-R19X", "NX.JPKSP.001", "https://store.acer.com/en-ph/aspire-go-15-ai-ag15-43p-r19x-opi-pure-silver", 55999, 53199, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "AMD Ryzen 5 7640HS", "AMD Ryzen 5 7640HS", "cpu", None),
            ("gpu", "AMD Radeon 680M Graphics", "AMD Radeon 680M Graphics", "gpu", None),
            ("ram_capacity", "16GB DDR5 SDRAM", 16, "ramGb", "GB"),
            ("ram_type", "DDR5 SDRAM", "DDR5", "ramType", None),
            ("storage_capacity", "512GB NVMe SSD", 512, "storageGb", "GB"),
            ("storage_type", "NVMe SSD", "NVMe SSD", "storageType", None),
            ("storage_slots", "Upgradeable to maximum 1TB", "Maximum supported capacity 1TB; slot count not stated", None, None),
            ("display_size", "15.6-inch", 15.6, "displayInches", "in"),
            ("display_technology", "IPS (In-Plane Switching)", "IPS", "displayType", None),
            ("ports", "Two USB Type-C ports", "2 x USB Type-C", "ports", None),
        ]),
        ("device_442be1206901c1", "config_26dcd487702194", "Aspire Lite AL14-42P-R1LF", "NX.DJ3SP.001", "https://store.acer.com/en-ph/aspire-lite-al14-42p-r1lf-opi-light-silver", 34999, 33249, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "AMD Ryzen 3 5300U quad-core", "AMD Ryzen 3 5300U", "cpu", None),
            ("ram_capacity", "8GB DDR4 RAM", 8, "ramGb", "GB"),
            ("ram_type", "DDR4", "DDR4", "ramType", None),
            ("storage_capacity", "512GB NVMe SSD", 512, "storageGb", "GB"),
            ("storage_type", "NVMe SSD", "NVMe SSD", "storageType", None),
            ("gpu", "AMD Radeon Graphics", "AMD Radeon Graphics", "gpu", None),
            ("display_size", "14.0-inch", 14, "displayInches", "in"),
            ("display_technology", "IPS (In-Plane Switching)", "IPS", "displayType", None),
            ("ports", "USB Type-C port", "USB Type-C", "ports", None),
        ]),
        ("device_f4bfe7f208cae3", "config_2d6dbc293f1116", "Aspire Lite AL15-33P-332M", "NX.DY0SP.001", "https://store.acer.com/en-ph/aspire-lite-al15-33p-332m-natural-titanium", 35999, 34199, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Intel Core 3 processor N355", "Intel Core 3 N355", "cpu", None),
            ("ram_capacity", "8GB LPDDR5 RAM", 8, "ramGb", "GB"),
            ("ram_type", "LPDDR5", "LPDDR5", "ramType", None),
            ("storage_capacity", "512GB NVMe SSD", 512, "storageGb", "GB"),
            ("storage_type", "NVMe SSD", "NVMe SSD", "storageType", None),
            ("storage_slots", "Upgradeable to maximum 1TB", "Maximum supported capacity 1TB; slot count not stated", None, None),
            ("gpu", "Intel UHD Graphics", "Intel UHD Graphics", "gpu", None),
            ("display_size", "15.6-inch", 15.6, "displayInches", "in"),
            ("display_technology", "IPS (In-Plane Switching)", "IPS", "displayType", None),
            ("ports", "USB Type-C port", "USB Type-C", "ports", None),
        ]),
        ("device_498860a23a9561", "config_7e6c1ccdc91313", "Predator Helios Neo 16 PHN16-72-99K9", "NH.QNNSP.003", "https://store.acer.com/en-ph/intel-corei9-predator-helios-neo-16-phn16-72-99k9-opi-black", 114999, 109249, "out of stock when checked", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Intel Core i9-14900HX", "Intel Core i9-14900HX", "cpu", None),
            ("ram_capacity", "16GB DDR5", 16, "ramGb", "GB"),
            ("ram_type", "DDR5", "DDR5", "ramType", None),
            ("ram_upgradeability", "Upgradable to 32GB; two memory slots", 32, "ramMaxGb", "GB"),
            ("storage_capacity", "512GB SSD", 512, "storageGb", "GB"),
            ("storage_type", "NVMe SSD, upgradeable to maximum 1TB", "NVMe SSD", "storageType", None),
            ("storage_slots", "Upgradeable to maximum 1TB; slot count not stated", "Maximum supported capacity 1TB; slot count not stated", None, None),
            ("display_size", "16.0-inch", 16, "displayInches", "in"),
            ("display_resolution", "2560 x 1600", "2560 x 1600", "resolution", None),
            ("display_technology", "IPS (In-Plane Switching)", "IPS", "displayType", None),
            ("display_refresh_rate", "165Hz", 165, "refreshHz", "Hz"),
            ("gpu", "NVIDIA GeForce RTX 4060", "NVIDIA GeForce RTX 4060", "gpu", None),
            ("gpu_vram", "8GB GDDR6 dedicated VRAM", 8, None, "GB"),
            ("wifi", "Wi-Fi 6E / 802.11ax", "Wi-Fi 6E", "wifi", None),
            ("bluetooth", "Bluetooth 5.3 or above", "Bluetooth 5.3 or above", None, None),
            ("webcam", "1280 x 720 front webcam", "720p webcam", None, None),
            ("battery_capacity", "90Wh", 90, "batteryWh", "Wh"),
        ]),
        ("device_24ba072c50e98d", "config_3ee1892f38ed88", "Predator Helios Neo 16 PHN16-73-93Y5", "NH.QX2SP.001", "https://store.acer.com/en-ph/predator-helios-neo-16-phn16-73-93y5-opi-abyssal-black", 214999, 204249, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Intel Core Ultra 9 275HX", "Intel Core Ultra 9 275HX", "cpu", None),
            ("ram_capacity", "32GB RAM", 32, "ramGb", "GB"),
            ("ram_upgradeability", "Upgradable to 192GB", 192, "ramMaxGb", "GB"),
            ("storage_capacity", "1TB NVMe SSD", 1024, "storageGb", "GB"),
            ("storage_type", "NVMe SSD", "NVMe SSD", "storageType", None),
            ("gpu", "NVIDIA GeForce RTX 5070 Ti", "NVIDIA GeForce RTX 5070 Ti", "gpu", None),
            ("gpu_vram", "12GB dedicated GDDR7 VRAM", 12, None, "GB"),
            ("keyboard", "FineTip RGB-backlight keyboard with numeric keypad", "RGB-backlit FineTip keyboard; numeric keypad", "keyboard", None),
            ("warranty", "2 Years Warranty", "2-year warranty", None, None),
        ]),
        ("device_e241e41dcc1848", "config_33fd77e02f526e", "Predator Helios Neo Slim 16 PHN16S-71-9269", "NH.QXASP.003", "https://store.acer.com/en-ph/predator-helios-neo-slim-16-phn16s-71-9269-opi-abyssal-black", 204999, 194749, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Intel Core Ultra 9 275HX", "Intel Core Ultra 9 275HX", "cpu", None),
            ("ram_capacity", "32GB RAM", 32, "ramGb", "GB"),
            ("storage_capacity", "1TB SSD", 1024, "storageGb", "GB"),
            ("gpu", "NVIDIA GeForce RTX 5070", "NVIDIA GeForce RTX 5070", "gpu", None),
            ("display_size", "16.0-inch", 16, "displayInches", "in"),
            ("display_technology", "OLED", "OLED", "displayType", None),
            ("keyboard", "FineTip RGB-backlight slim keyboard; multi-gesture touchpad", "RGB-backlit slim keyboard; multi-gesture touchpad", "keyboard", None),
        ]),
        ("device_668b383e956903", "config_b35b4fb479b661", "Swift Air 14 AI SFA14-I31-56FJ", "NX.SHYSP.002", "https://store.acer.com/en-ph/swift-air-14-ai-i-sfa14-i31-56fj-opi-sage-green", 67999, 67999, "out of stock when checked", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Intel Core 5 processor 320", "Intel Core 5 320", "cpu", None),
            ("ram_capacity", "8GB LPDDR5 RAM", 8, "ramGb", "GB"),
            ("ram_type", "LPDDR5", "LPDDR5", "ramType", None),
            ("storage_capacity", "512GB NVMe SSD", 512, "storageGb", "GB"),
            ("storage_type", "NVMe SSD", "NVMe SSD", "storageType", None),
            ("gpu", "Intel Graphics", "Intel Graphics", "gpu", None),
            ("display_size", "14.0-inch", 14, "displayInches", "in"),
            ("display_resolution", "WUXGA 1920 x 1200", "1920 x 1200", "resolution", None),
            ("display_technology", "IPS", "IPS", "displayType", None),
            ("battery_capacity", "70Wh 3-cell Li-ion battery", 70, "batteryWh", "Wh"),
        ]),
        ("device_c27970d6fe7316", "config_99091889235c83", "Swift Go SFG14-01-X2PX", "NX.KYXSP.003", "https://store.acer.com/en-ph/swift-go-sfg14-01-x2px-opi-steel-gray", 56999, 54149, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Qualcomm Snapdragon X Plus X1P-42-100", "Qualcomm Snapdragon X Plus X1P-42-100", "cpu", None),
            ("ram_capacity", "16GB RAM", 16, "ramGb", "GB"),
            ("storage_capacity", "1TB SSD", 1024, "storageGb", "GB"),
            ("display_size", "14.5-inch", 14.5, "displayInches", "in"),
            ("display_resolution", "WUXGA 1920 x 1200", "1920 x 1200", "resolution", None),
            ("display_technology", "IPS", "IPS", "displayType", None),
            ("gpu", "Qualcomm Adreno GPU", "Qualcomm Adreno GPU", "gpu", None),
            ("wifi", "Wi-Fi 7 / 802.11be", "Wi-Fi 7", "wifi", None),
            ("bluetooth", "Bluetooth 5.4 or above; LE Audio (LC3)", "Bluetooth 5.4 or above; LE Audio", None, None),
            ("webcam", "2560 x 1440 front webcam", "1440p webcam", None, None),
            ("battery_capacity", "65Wh 3-cell Li-ion battery", 65, "batteryWh", "Wh"),
            ("charging", "USB Type-C 65W PD AC adapter", 65, "chargingW", "W"),
            ("audio", "HD audio; two speakers; microphone", "HD audio; 2 speakers; microphone", "sound", None),
            ("ports", "2 USB 3.2 Gen 1; 2 USB Type-C; headphone", "2 x USB 3.2 Gen 1; 2 x USB Type-C; headphone jack", "ports", None),
        ]),
        ("device_7a93cefe5a4126", "config_045742254d2835", "Swift Go SFG14-75-55MB", "NX.JNBSP.001", "https://store.acer.com/en-ph/swift-go-sfg14-75-55mb-opi-steam-blue", 64999, 61749, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Intel Core Ultra 5 processor; exact submodel not stated on this listing", "Intel Core Ultra 5 (submodel not stated)", "cpu", None),
            ("ram_capacity", "16GB onboard LPDDR5X", 16, "ramGb", "GB"),
            ("ram_type", "LPDDR5X onboard", "LPDDR5X, onboard", "ramType", None),
            ("storage_capacity", "512GB NVMe SSD", 512, "storageGb", "GB"),
            ("storage_type", "NVMe SSD", "NVMe SSD", "storageType", None),
            ("display_size", "14.0-inch", 14, "displayInches", "in"),
            ("display_resolution", "WUXGA 1920 x 1200", "1920 x 1200", "resolution", None),
            ("display_technology", "OLED", "OLED", "displayType", None),
            ("display_brightness", "400 nits typical value", "400 nits typical", None, "nits"),
            ("gpu", "Intel Arc Graphics 130V", "Intel Arc Graphics 130V", "gpu", None),
            ("warranty", "2 Years Warranty", "2-year warranty", None, None),
        ]),
        ("device_fb7b36df78b458", "config_c310afe3f6e51c", "Swift SF14-51-553D", "NX.J2KSP.002", "https://store.acer.com/en-ph/swift-sf14-51-553d-opi-frost-blue", 74999, 71249, "in stock", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "Intel Core Ultra 5 228V", "Intel Core Ultra 5 228V", "cpu", None),
            ("ram_capacity", "32GB RAM", 32, "ramGb", "GB"),
            ("storage_capacity", "1TB NVMe SSD", 1024, "storageGb", "GB"),
            ("storage_type", "NVMe SSD", "NVMe SSD", "storageType", None),
            ("display_size", "14.5-inch", 14.5, "displayInches", "in"),
            ("display_resolution", "WQXGA+ 2880 x 1800", "2880 x 1800", "resolution", None),
            ("display_technology", "OLED", "OLED", "displayType", None),
            ("display_brightness", "400 nits", "400 nits", None, "nits"),
            ("gpu", "Intel Arc Graphics", "Intel Arc Graphics", "gpu", None),
            ("wifi", "Wi-Fi 7 / 802.11be", "Wi-Fi 7", "wifi", None),
            ("bluetooth", "Bluetooth 5.4 or above; LE Audio (LC3)", "Bluetooth 5.4 or above; LE Audio", None, None),
            ("ports", "2 USB 3.2 Gen 1; 2 USB Type-C; HDMI; audio line-in", "2 x USB 3.2 Gen 1; 2 x USB Type-C; HDMI; audio line-in", "ports", None),
        ]),
    ]
    out = []
    for did, vid, model, sku, url, regular, special, stock, specs in data:
        sid = "acer_" + sku.lower().replace(".", "_")
        publisher = "Acer Philippines Official Store"
        source_obj = source(sid, publisher, url, "Exact Philippine SKU specifications and dated local listing price",
                            f"Official Philippine product listing; status shown as {stock}. Regular price PHP {regular:,}; special/listed price PHP {special:,}. Price may change.")
        fields = [field("model_number", sid, sku, sku, note="Exact Acer Philippines reference/part number.")]
        fields.append(field("configuration", sid, "; ".join(f"{fid}: {src}" for fid, src, *_ in specs),
                            "; ".join(f"{fid}: {norm}" for fid, _, norm, *_ in specs), note="Exact configuration fields explicitly stated for this Philippine SKU."))
        for fid, source_value, normalized, key, unit in specs:
            fields.append(field(fid, sid, source_value, normalized, key=key, unit=unit))
        fields.append(field("current_price_php", sid, f"Regular PHP {regular:,}; special/listed PHP {special:,}; {stock}", special,
                            unit="PHP", note=f"Dated Acer Philippines Official Store price observation on 2026-11-25. {stock.capitalize()}; do not interpret as a guaranteed offer.",
                            price_condition="new", price_type=(f"Acer Philippines Official Store single listed price; {stock}" if regular == special else f"Acer Philippines Official Store listed special price; regular price PHP {regular:,}; {stock}"), price_observed=OBSERVED))
        out.append({"deviceId": did, "configurationId": vid, "sources": [source_obj], "fields": fields})
    return out


def asus_records():
    news_proart = "https://www.asus.com/ph/news/6b8nlidlxkjioucl/"
    news_zen = "https://www.asus.com/ph/news/6v9jkea7qhr8ro33/"
    proart_px13 = "https://www.asus.com/ph/laptops/for-creators/proart/proart-px13-hn7306/"
    proart_gopro = "https://www.asus.com/ph/laptops/for-creators/proart/proart-gopro-edition-px13-hn7306/"
    proart_p16_spec = "https://www.asus.com/ph/laptops/for-creators/proart/proart-p16-h7606/techspec/"
    duo_product = "https://www.asus.com/ph/laptops/for-home/zenbook/asus-zenbook-duo-ux8407/"
    sources = {
        "asus_proart_launch_20260420": source("asus_proart_launch_20260420", "ASUS Philippines", news_proart, "Philippine product launch, exact SKU and introductory price", "ASUS Philippines newsroom announcement dated 2026-04-20. The source says authorized-store availability would follow in the coming weeks; the first retail date is not inferred.", "2026-04-20"),
        "asus_proart_px13_product": source("asus_proart_px13_product", "ASUS Philippines", proart_px13, "Exact PX13 SKU specification and introductory price", "ASUS Philippines product page with exact HN7306EA-LX054WSM configuration and published introductory price."),
        "asus_proart_gopro_product": source("asus_proart_gopro_product", "ASUS Philippines", proart_gopro, "Exact GoPro Edition SKU specification and introductory price", "ASUS Philippines product page with exact HN7306EAC-LX075WSM configuration and published introductory price."),
        "asus_proart_p16_specs": source("asus_proart_p16_specs", "ASUS Philippines", proart_p16_spec, "Exact H7606WW technical specifications", "Manufacturer tech-spec page distinguishes H7606WW from the separate H7606WI configuration."),
        "asus_zenbook_2026_launch": source("asus_zenbook_2026_launch", "ASUS Philippines", news_zen, "Philippine launch SKU, specification and introductory price", "ASUS Philippines announcement dated 2026-03-25; exact 2026 SKUs and introductory prices are recorded from the named configuration table.", "2026-03-25"),
        "asus_zenbook_duo_product": source("asus_zenbook_duo_product", "ASUS Philippines", duo_product, "Current Philippine product page specification and starting price", "Current ASUS Philippines product page lists UX8407AA configuration and a separate starting price; retained as a dated observation distinct from the March introductory price."),
        "asus_ux3480_launch_20261007": source("asus_ux3480_launch_20261007", "ASUS Philippines", "https://www.asus.com/ph/news/asus-zenbook-14-ux3480-launches-in-the-philippines/", "Exact local Zenbook 14 SKUs and introductory prices", "ASUS Philippines launch announcement dated 2026-10-07. Only the five SKUs already represented in the workbook are reviewed; the separate coming-soon beige SKU is not added.", "2026-10-07"),
        "asus_ux3480_intel_specs": source("asus_ux3480_intel_specs", "ASUS Philippines", "https://www.asus.com/ph/laptops/for-home/zenbook/asus-zenbook-14-ux3480-intel/techspec/", "UX3480AA technical specifications", "Manufacturer technical table distinguishes the Intel Core Ultra 9 and Core Ultra 7 specifications."),
        "asus_ux3480_amd_specs": source("asus_ux3480_amd_specs", "ASUS", "https://www.asus.com/laptops/for-home/zenbook/asus-zenbook-14-ux3480-amd/techspec/", "UX3480KA technical specifications", "Manufacturer technical table distinguishes Ryzen AI 7 and Ryzen AI 5 configurations. The PH launch source is used for local SKU and pricing."),
        "asus_ux3480_qualcomm_specs": source("asus_ux3480_qualcomm_specs", "ASUS Philippines", "https://www.asus.com/ph/laptops/for-home/zenbook/asus-zenbook-14-ux3480-qualcomm/techspec/", "UX3480QA technical specifications", "Manufacturer technical table for the Snapdragon configuration."),
    }

    def make_fields(sid, sku, values, price, price_date, price_note, *, launch_price=None):
        rows = [field("model_number", sid, sku, sku, note="Exact Philippine SKU named by the ASUS Philippines source.")]
        rows.append(field("configuration", sid, "; ".join(f"{fid}: {sv}" for fid, sv, *_ in values),
                          "; ".join(f"{fid}: {nv}" for fid, _, nv, *_ in values), note="Exact configuration explicitly listed for this Philippine SKU."))
        for fid, source_value, normalized, key, unit in values:
            rows.append(field(fid, sid, source_value, normalized, key=key, unit=unit))
        if launch_price:
            amount, source_text = launch_price
            rows.append(field("official_launch_price_php", sid, source_text, amount, unit="PHP", note="Official Philippine introductory price published on the announcement date; historical, not a live quotation."))
        if price:
            amount, source_text, source_id = price
            rows.append(field("current_price_php", source_id, source_text, amount, unit="PHP", note=price_note,
                              price_condition="new", price_type="Official ASUS Philippines price observation; see note for date and terms.", price_observed=price_date))
        return rows

    def new_variant(did, model, category_sku, vid, sku, model_code, sourceids, values, price, price_note, *, launch=None, extra_sources=None):
        sourceid = sourceids[0]
        pubdate = sources[sourceid]["publicationDate"]
        p_amount, p_text, p_source_id, p_date = price if price else (None, None, None, None)
        all_sources = [sources[x] for x in sourceids]
        if extra_sources:
            all_sources.extend(extra_sources)
        fields = [field("model_number", sourceid, sku, sku, note="Exact Philippine SKU named by the ASUS Philippines source."),
                  field("configuration", sourceid, "; ".join(f"{fid}: {sv}" for fid, sv, *_ in values),
                        "; ".join(f"{fid}: {nv}" for fid, _, nv, *_ in values), note="Exact configuration explicitly listed for this Philippine SKU.")]
        for fid, source_value, normalized, key, unit, sid_override in [(*v, None) if len(v) == 5 else v for v in values]:
            fields.append(field(fid, sid_override or sourceid, source_value, normalized, key=key, unit=unit))
        if launch:
            amount, text = launch
            fields.append(field("official_launch_price_php", sourceid, text, amount, unit="PHP", note="Official Philippine introductory price on the launch announcement date; historical, not a live quotation."))
        if price:
            fields.append(field("current_price_php", p_source_id, p_text, p_amount, unit="PHP", note=price_note,
                                price_condition="new", price_type="Official ASUS Philippines price observation; see note for date and terms.", price_observed=p_date))
        return {
            "deviceId": did, "configurationId": vid, "brand": "ASUS", "model": model,
            "configuration": sku, "configurationLabel": sku,
            "replacementVariants": [{"id": vid, "label": sku, "sku": sku, "modelCode": model_code}],
            "sources": all_sources, "fields": fields,
        }

    p16_values = [
        ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
        ("cpu", "AMD Ryzen AI 9 HX 370", "AMD Ryzen AI 9 HX 370", "cpu", None),
        ("cpu_cores_threads", "12 cores / 24 threads", "12 cores / 24 threads", None, None),
        ("gpu", "NVIDIA GeForce RTX 5080 Laptop GPU; AMD Radeon 890M Graphics", "NVIDIA GeForce RTX 5080 Laptop GPU; AMD Radeon 890M Graphics", "gpu", None),
        ("gpu_vram", "16GB GDDR7", 16, None, "GB"),
        ("display_size", "16.0-inch", 16, "displayInches", "in"),
        ("display_resolution", "4K 3840 x 2400", "3840 x 2400", "resolution", None),
        ("display_technology", "OLED", "OLED", "displayType", None),
        ("display_refresh_rate", "120Hz", 120, "refreshHz", "Hz"),
        ("display_brightness", "1600 nits HDR peak", "1600 nits HDR peak", None, "nits"),
        ("display_color", "100% DCI-P3", "100% DCI-P3", None, None),
        ("touchscreen", "Touch screen", True, "touchscreen", None),
        ("ram_capacity", "64GB LPDDR5X on board", 64, "ramGb", "GB"),
        ("ram_type", "LPDDR5X on board", "LPDDR5X, onboard", "ramType", None),
        ("storage_capacity", "2TB M.2 NVMe PCIe 4.0 SSD", 2048, "storageGb", "GB"),
        ("storage_type", "M.2 NVMe PCIe 4.0 SSD", "M.2 NVMe PCIe 4.0 SSD", "storageType", None),
    ]
    records = [new_variant("device_8cef5fb897991d", "ProArt P16 (H7606)", None,
                           "device_8cef5fb897991d-h7606ww-se021wsm", "H7606WW-SE021WSM", "H7606WW",
                           ["asus_proart_launch_20260420", "asus_proart_p16_specs"], p16_values,
                           (289995, "Introductory price PHP 289,995", "asus_proart_launch_20260420", "2026-04-20"),
                           "ASUS Philippines published PHP 289,995 as the introductory price on 2026-04-20; retail availability was announced for later weeks, so this is not a current-offer guarantee.",
                           launch=(289995, "Introductory Price PHP 289,995; published 2026-04-20")),
              ]
    # The technical table is the only source for these detailed P16 fields.
    for row in records:
        for f in row["fields"]:
            if f["fieldId"] not in {"model_number", "configuration", "official_launch_price_php", "current_price_php"}:
                f["sourceId"] = "asus_proart_p16_specs"

    gopro_values = [
        ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
        ("cpu", "AMD Ryzen AI MAX+ 395", "AMD Ryzen AI MAX+ 395", "cpu", None),
        ("ram_capacity", "128GB LPDDR5X on board", 128, "ramGb", "GB"),
        ("ram_type", "LPDDR5X on board", "LPDDR5X, onboard", "ramType", None),
        ("storage_capacity", "1TB M.2 NVMe PCIe 4.0 SSD", 1024, "storageGb", "GB"),
        ("storage_type", "M.2 NVMe PCIe 4.0 SSD", "M.2 NVMe PCIe 4.0 SSD", "storageType", None),
        ("display_size", "13.3-inch", 13.3, "displayInches", "in"),
        ("display_resolution", "3K 2880 x 1800", "2880 x 1800", "resolution", None),
        ("display_technology", "OLED", "OLED", "displayType", None),
        ("touchscreen", "Touchscreen", True, "touchscreen", None),
        ("gpu", "AMD Radeon Graphics", "AMD Radeon Graphics", "gpu", None),
        ("warranty", "3Y Warranty", "3-year warranty", None, None),
        ("ports", "2 USB4 Type-C; 1 USB 3.2 Type-A; 1 3.5mm combo audio; 1 HDMI 2.1; 1 MicroSD 3.0 reader", "2 x USB4 Type-C; USB 3.2 Type-A; 3.5 mm combo; HDMI 2.1; MicroSD 3.0", "ports", None),
    ]
    records.append(new_variant("device_ea2924f7ecf7ce", "ProArt GoPro Edition (PX13)", None,
                               "device_ea2924f7ecf7ce-hn7306eac-lx075wsm", "HN7306EAC-LX075WSM", "HN7306EAC",
                               ["asus_proart_gopro_product", "asus_proart_launch_20260420"], gopro_values,
                               (209995, "Introductory price PHP 209,995", "asus_proart_gopro_product", "2026-11-25"),
                               "ASUS Philippines product page showed the published introductory price of PHP 209,995 when accessed 2026-11-25; actual retail pricing and availability may vary.",
                               launch=(209995, "Introductory price PHP 209,995")))

    # Existing exact PX13 variant from the 2026 announcement.
    records.append({
        "deviceId": "device_00536c6bd5502e", "configurationId": "config_15a5da2d8b61bc",
        "brand": "ASUS", "model": "ProArt PX13 (HN7306)", "configuration": "HN7306EA-LX054WSM",
        "sources": [sources["asus_proart_px13_product"], sources["asus_proart_launch_20260420"]],
        "fields": make_fields("asus_proart_px13_product", "HN7306EA-LX054WSM", [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
            ("cpu", "AMD Ryzen AI MAX+ 395", "AMD Ryzen AI MAX+ 395", "cpu", None),
            ("gpu", "AMD Radeon Graphics", "AMD Radeon Graphics", "gpu", None),
            ("ram_capacity", "32GB LPDDR5X on board", 32, "ramGb", "GB"),
            ("ram_type", "LPDDR5X on board", "LPDDR5X, onboard", "ramType", None),
            ("storage_capacity", "1TB M.2 NVMe PCIe 4.0 SSD", 1024, "storageGb", "GB"),
            ("storage_type", "M.2 NVMe PCIe 4.0 SSD", "M.2 NVMe PCIe 4.0 SSD", "storageType", None),
            ("display_size", "13.3-inch", 13.3, "displayInches", "in"),
            ("display_resolution", "3K 2880 x 1800", "2880 x 1800", "resolution", None),
            ("display_technology", "OLED", "OLED", "displayType", None),
            ("touchscreen", "OLED touchscreen", True, "touchscreen", None),
            ("ports", "2 USB4 Type-C; 1 USB 3.2 Gen 2 Type-A; HDMI 2.1 FRL; UHS-II MicroSD reader; 3.5mm headphone jack", "2 x USB4 Type-C; USB 3.2 Gen 2 Type-A; HDMI 2.1; UHS-II MicroSD; 3.5 mm audio", "ports", None),
            ("warranty", "3Y Warranty; 1 Year Local Accidental Damage Protection + Local On-site Support", "3-year warranty; 1-year local accidental damage protection and local on-site support", None, None),
        ], (164995, "Introductory Price PHP 164,995", "asus_proart_px13_product"), "2026-04-20", "Official Philippine introductory price published 2026-04-20; this historical price is not a live quotation.", launch_price=(164995, "Introductory Price PHP 164,995")),
    })

    duo_variant = "device_fc5e931cb8adc4-ux8407aa-sn152wsm"
    duo_values = [
        ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
        ("cpu", "Intel Core Ultra 9 386H", "Intel Core Ultra 9 386H", "cpu", None),
        ("display_size", "Dual 14-inch displays", 14, "displayInches", "in"),
        ("display_resolution", "Dual 3K (2880 x 1800) OLED displays", "Dual 2880 x 1800", "resolution", None),
        ("display_technology", "Dual ASUS Lumina Pro OLED", "Dual OLED", "displayType", None),
        ("display_refresh_rate", "144Hz", 144, "refreshHz", "Hz"),
        ("display_brightness", "1000 nits", "1000 nits", None, "nits"),
        ("touchscreen", "Dual touchscreen displays", True, "touchscreen", None),
        ("ram_capacity", "32GB LPDDR5X", 32, "ramGb", "GB"),
        ("ram_type", "LPDDR5X onboard", "LPDDR5X, onboard", "ramType", None),
        ("storage_capacity", "1TB M.2 SSD", 1024, "storageGb", "GB"),
        ("storage_type", "M.2 PCIe 4 SSD", "M.2 PCIe 4 SSD", "storageType", None),
        ("battery_life", "Up to 32 hours single-screen; up to 18 hours dual-screen", "Manufacturer claims up to 32 h single-screen / 18 h dual-screen; test conditions not stated in the source passage", None, None),
        ("ports", "2 Thunderbolt 4 USB-C; 1 USB 3.2 Gen 2 Type-A; HDMI 2.1 FRL; 3.5mm combo audio", "2 x Thunderbolt 4 USB-C; USB 3.2 Gen 2 Type-A; HDMI 2.1 FRL; 3.5 mm combo audio", "ports", None),
        ("warranty", "ASUS Quality and Service Package", "ASUS Quality and Service Package; specific duration not stated in the launch SKU table", None, None),
    ]
    records.append(new_variant("device_fc5e931cb8adc4", "Zenbook DUO (UX8407)", None, duo_variant,
                               "UX8407AA-SN152WSM", "UX8407AA", ["asus_zenbook_2026_launch", "asus_zenbook_duo_product"], duo_values,
                               (219995, "Current product page price starts at PHP 219,995", "asus_zenbook_duo_product", OBSERVED),
                               "The current ASUS Philippines product page lists a starting price of PHP 219,995, observed 2026-11-25. This is distinct from the exact SKU's PHP 179,995 launch introductory price on 2026-03-25.",
                               launch=(179995, "UX8407AA-SN152WSM introductory price PHP 179,995; announced 2026-03-25")))
    s14_values = [
        ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None),
        ("cpu", "Intel Core Ultra 9 386H", "Intel Core Ultra 9 386H", "cpu", None),
        ("display_size", "14-inch", 14, "displayInches", "in"),
        ("display_resolution", "3K 2880 x 1800", "2880 x 1800", "resolution", None),
        ("display_technology", "ASUS Lumina OLED touchscreen", "OLED", "displayType", None),
        ("display_refresh_rate", "120Hz", 120, "refreshHz", "Hz"),
        ("display_brightness", "1100 nits", "1100 nits", None, "nits"),
        ("touchscreen", "OLED touchscreen", True, "touchscreen", None),
        ("ram_capacity", "32GB LPDDR5X onboard", 32, "ramGb", "GB"),
        ("ram_type", "LPDDR5X onboard", "LPDDR5X, onboard", "ramType", None),
        ("storage_capacity", "1TB M.2 PCIe 4 SSD", 1024, "storageGb", "GB"),
        ("storage_type", "M.2 PCIe 4 SSD", "M.2 PCIe 4 SSD", "storageType", None),
        ("battery_capacity", "77Wh", 77, "batteryWh", "Wh"),
        ("battery_life", "Up to 27 hours", "Manufacturer claim up to 27 h; test conditions not stated in the source passage", None, None),
        ("ports", "2 Thunderbolt 4; USB 3.2 Gen 2 Type-A; 3.5mm combo audio; HDMI 2.1 TMDS", "2 x Thunderbolt 4; USB 3.2 Gen 2 Type-A; 3.5 mm combo audio; HDMI 2.1 TMDS", "ports", None),
        ("weight", "1.2kg", 1200, "weightG", "g"),
    ]
    records.append(new_variant("device_686411caae8d78", "Zenbook S14 (UX5406)", None,
                               "device_686411caae8d78-ux5406aa-su165wsm", "UX5406AA-SU165WSM", "UX5406AA",
                               ["asus_zenbook_2026_launch"], s14_values,
                               (129995, "UX5406AA-SU165WSM introductory price PHP 129,995", "asus_zenbook_2026_launch", "2026-03-25"),
                               "Exact-SKU introductory price announced by ASUS Philippines on 2026-03-25; historical price, not a current quotation.",
                               launch=(129995, "UX5406AA-SU165WSM introductory price PHP 129,995; announced 2026-03-25")))

    ux_launch = "asus_ux3480_launch_20261007"
    ux_catalog = {"device_a07417c32a861d": "Zenbook 14 (UX3480)"}
    ux_variants = [
        ("config_2104cbd53025ef", "UX3480AA-U2489WSM", "UX3480AA", "Intel Core Ultra 9 386H", 24, 129995, "intel", True, "16 cores / 16 threads"),
        ("config_18ad6d3f8d0f8e", "UX3480AA-U2477WSM", "UX3480AA", "Intel Core Ultra 7 355", 16, 106995, "intel", True, "8 cores / 8 threads"),
        ("config_f66f082a33d7c7", "UX3480KA-U1137WSM", "UX3480KA", "AMD Ryzen AI 7 345", 16, 94995, "amd", True, "6 cores / 12 threads"),
        ("config_4cc45014b7ad2d", "UX3480KA-U1135WSM", "UX3480KA", "AMD Ryzen AI 5 330", 16, 86995, "amd", False, "4 cores / 8 threads"),
        ("config_5104406ef8b646", "UX3480QA-U1004WSM", "UX3480QA", "Snapdragon X X1 26 100", 16, 76995, "qualcomm", False, "8 cores / 8 threads"),
    ]
    for vid, sku, model_code, cpu, ram, price, platform, touch, core_thread in ux_variants:
        tech_sid = {"intel": "asus_ux3480_intel_specs", "amd": "asus_ux3480_amd_specs", "qualcomm": "asus_ux3480_qualcomm_specs"}[platform]
        gpu = {"intel": "Intel Graphics", "amd": "AMD Radeon Graphics", "qualcomm": "Qualcomm Adreno GPU"}[platform]
        touch_label = "Touch screen" if touch else "Non-touch screen"
        values = [
            ("operating_system", "Windows 11 Home", "Windows 11 Home", "os", None, tech_sid),
            ("cpu", cpu, cpu, "cpu", None, ux_launch),
            ("cpu_cores_threads", core_thread, core_thread, None, None, tech_sid),
            ("gpu", gpu, gpu, "gpu", None, tech_sid),
            ("display_size", "14.0-inch", 14, "displayInches", "in", tech_sid),
            ("display_resolution", "WUXGA/FHD 1920 x 1200", "1920 x 1200", "resolution", None, tech_sid),
            ("display_technology", "OLED 16:10", "OLED", "displayType", None, tech_sid),
            ("display_refresh_rate", "60Hz", 60, "refreshHz", "Hz", tech_sid),
            ("display_brightness", "300 nits", "300 nits", None, "nits", tech_sid),
            ("display_color", "100% DCI-P3", "100% DCI-P3", None, None, tech_sid),
            ("touchscreen", touch_label, touch, "touchscreen", None, tech_sid),
            ("ram_capacity", f"{ram}GB LPDDR5X on board", ram, "ramGb", "GB", ux_launch),
            ("ram_type", "LPDDR5X on board", "LPDDR5X, onboard", "ramType", None, tech_sid),
            ("storage_capacity", "512GB SSD", 512, "storageGb", "GB", ux_launch),
            ("storage_type", "M.2 NVMe PCIe 4.0 SSD", "M.2 NVMe PCIe 4.0 SSD", "storageType", None, tech_sid),
        ]
        sources_used = [sources[ux_launch], sources[tech_sid]]
        fields = [field("model_number", ux_launch, sku, sku, note="Exact Philippine SKU from ASUS Philippines launch table."),
                  field("configuration", ux_launch, f"{sku}: {cpu}; {ram}GB LPDDR5X; 512GB SSD; 14-inch WUXGA OLED", f"{cpu}; {ram}GB RAM; 512GB storage; 14-inch 1920 x 1200 OLED", note="Exact SKU configuration from the Philippine launch table; technical page supplies panel and platform details.")]
        for fid, source_value, normalized, key, unit, sid in values:
            fields.append(field(fid, sid, source_value, normalized, key=key, unit=unit))
        fields.append(field("official_launch_price_php", ux_launch, f"Introductory price PHP {price:,}", price, unit="PHP", note="Official ASUS Philippines introductory price published 2026-10-07; historical, not a live quotation."))
        fields.append(field("current_price_php", ux_launch, f"Introductory price PHP {price:,}", price, unit="PHP", note="Dated ASUS Philippines launch price observation from 2026-10-07; historical, not a current retailer offer.", price_condition="new", price_type="Official Philippine introductory price", price_observed="2026-10-07"))
        records.append({"deviceId": "device_a07417c32a861d", "configurationId": vid,
                        "brand": "ASUS", "model": ux_catalog["device_a07417c32a861d"],
                        "configuration": sku, "configurationLabel": sku,
                        "sources": sources_used, "fields": fields})

    # User asked for record-level exact model verification; do not add global models as local variants.
    return records


def supplemental_laptop_records():
    """Add exact-SKU details found in the official technical tables.

    These fields were still pending after the first review because they are
    outside the abbreviated product summaries. Values remain tied to the exact
    Acer part number or ASUS model-code column.
    """
    acer_store = "https://store.acer.com/en-ph/intel-corei9-predator-helios-neo-16-phn16-72-99k9-opi-black"
    acer_specs = "https://www.acer.com/ph-en/predator/laptops/helios/helios-neo-16/pdp/NH.QNNSP.003"
    intel_specs = "https://www.intel.com/content/www/us/en/products/sku/235995/intel-core-i9-processor-14900hx-36m-cache-up-to-5-80-ghz/specifications.html"
    asus_specs = "https://www.asus.com/ph/laptops/for-creators/proart/proart-p16-h7606/techspec/"
    asus_product = "https://www.asus.com/ph/laptops/for-creators/proart/proart-p16-h7606/"
    asus_launch = "https://www.asus.com/ph/news/6b8nlidlxkjioucl/"

    acer_review = {
        "deviceId": "device_498860a23a9561",
        "configurationId": "config_7e6c1ccdc91313",
        "brand": "Acer",
        "model": "Predator Helios Neo 16 PHN16-72-99K9",
        "configuration": "NH.QNNSP.003",
        "sources": [
            source("acer_phn16_72_99k9_specs", "Acer Philippines", acer_specs,
                   "Exact NH.QNNSP.003 technical specifications",
                   "Acer Philippines product specification page is titled PHN16-72-99K9 and identifies part NH.QNNSP.003."),
            source("acer_phn16_72_99k9_store_details", "Acer Philippines Official Store", acer_store,
                   "Exact Philippine SKU detailed specifications",
                   "Official store page identifies product PHN16-72-99K9 and reference NH.QNNSP.003."),
            source("intel_i9_14900hx_specs", "Intel", intel_specs,
                   "Processor core and thread count",
                   "Intel ARK specification page for the exact Intel Core i9-14900HX CPU installed in this Acer SKU."),
        ],
        "fields": [
            field("cpu_cores_threads", "intel_i9_14900hx_specs",
                  "24 total cores (8 performance + 16 efficient); 32 threads",
                  "24 cores / 32 threads",
                  note="Intel ARK data for the i9-14900HX named on the exact Acer listing."),
            field("display_color", "acer_phn16_72_99k9_specs",
                  "100% sRGB color gamut", "100% sRGB",
                  note="Exact PHN16-72-99K9 manufacturer specification page."),
            field("touchscreen", "acer_phn16_72_99k9_specs",
                  "Touchscreen: No", False, key="touchscreen",
                  note="Explicitly listed as non-touch on the exact part-number specification page."),
            field("gpu_tgp", "acer_phn16_72_99k9_specs",
                  "Maximum Graphics Power: up to 140 W", 140, unit="W",
                  note="Acer's technical specification for NH.QNNSP.003; this is the listed maximum graphics power."),
            field("battery_life", "acer_phn16_72_99k9_specs",
                  "Maximum Battery Run Time: 6 Hours",
                  "Up to 6 hours; test conditions not stated",
                  note="Acer's published maximum-runtime figure; actual runtime varies by configuration and use."),
            field("audio", "acer_phn16_72_99k9_store_details",
                  "HD Audio: Yes; Speakers: Yes; Microphone: Yes",
                  "HD audio; speakers and microphone included",
                  key="sound"),
            field("keyboard", "acer_phn16_72_99k9_store_details",
                  "FineTip RGB-backlight keyboard with independent standard numeric keypad",
                  "RGB-backlit FineTip keyboard with numeric keypad",
                  key="keyboard"),
            field("touchpad", "acer_phn16_72_99k9_store_details",
                  "Multi-gesture touchpad, supporting two-finger scroll",
                  "Multi-gesture touchpad with two-finger scrolling"),
            field("ports", "acer_phn16_72_99k9_store_details",
                  "HDMI x1; USB 3.2 Gen 1 Type-A x1; USB 3.2 Gen 2 Type-A x2; USB 3.2 Type-C x2; RJ-45; audio line-in; headphone",
                  "HDMI; 1 x USB-A Gen 1; 2 x USB-A Gen 2; 2 x USB-C; RJ-45; audio line-in; headphone",
                  key="ports"),
            field("ethernet", "acer_phn16_72_99k9_store_details",
                  "Killer Ethernet E3100G; 2.5 Gigabit Ethernet",
                  "Killer E3100G 2.5 Gigabit Ethernet"),
            field("charging", "acer_phn16_72_99k9_store_details",
                  "3-pin 330 W AC adapter", "330 W AC adapter"),
            field("weight", "acer_phn16_72_99k9_store_details",
                  "Weight (approximate): 2.80 kg", 2800, key="weightG", unit="g"),
            field("security", "acer_phn16_72_99k9_specs",
                  "Kensington lock slot; Firmware Trusted Platform Module (TPM) solution",
                  "Kensington lock slot; firmware TPM"),
            field("warranty", "acer_phn16_72_99k9_store_details",
                  "2 Years Warranty", "2-year warranty"),
        ],
    }

    asus_review = {
        "deviceId": "device_8cef5fb897991d",
        "configurationId": "device_8cef5fb897991d-h7606ww-se021wsm",
        "brand": "ASUS",
        "model": "ProArt P16 (H7606)",
        "configuration": "H7606WW-SE021WSM",
        "sources": [
            source("asus_proart_p16_specs", "ASUS Philippines", asus_specs,
                   "Exact H7606WW technical specifications",
                   "ASUS technical table distinguishes H7606WW from H7606WI; values below use the H7606WW column."),
            source("asus_proart_p16_product", "ASUS Philippines", asus_product,
                   "Exact H7606WW Philippine product and warranty details",
                   "Philippine product page identifies H7606WW-SE021WSM, its PHP starting price and local warranty terms."),
            source("asus_proart_launch_20260420", "ASUS Philippines", asus_launch,
                   "Philippine launch announcement",
                   "ASUS announced the local launch on 2026-04-20 and said authorized-store availability would follow in the coming weeks; first retail date is not inferred.",
                   "2026-04-20"),
        ],
        "fields": [
            field("philippine_release_date", "asus_proart_launch_20260420",
                  "ASUS announced the Philippine launch of ProArt P16 on 2026-04-20; authorized-store availability was to follow later",
                  "2026-04-20",
                  note="This is the official Philippine launch announcement date, not an inferred first retail-sale date."),
            field("ram_upgradeability", "asus_proart_p16_specs",
                  "64GB LPDDR5X on board; maximum total system memory up to 64GB",
                  64, key="ramMaxGb", unit="GB",
                  note="All 64GB is onboard; ASUS lists 64GB as the maximum total system memory."),
            field("storage_slots", "asus_proart_p16_specs",
                  "1 x M.2 2280 PCIe 4.0 x4 + 1 x M.2 2280 PCIe 4.0 x2",
                  "2 x M.2 2280 slots (PCIe 4.0 x4 and PCIe 4.0 x2)"),
            field("battery_capacity", "asus_proart_p16_specs",
                  "90WHrs, 4S1P, 4-cell Li-ion", 90, key="batteryWh", unit="Wh"),
            field("charging", "asus_proart_p16_specs",
                  "240W AC adapter; charger inclusion varies by country, region, and model",
                  "240 W AC adapter specification; in-box inclusion varies by region"),
            field("webcam", "asus_proart_p16_specs",
                  "FHD camera with IR function to support Windows Hello",
                  "FHD infrared camera; Windows Hello support"),
            field("audio", "asus_proart_p16_specs",
                  "Built-in array microphone; built-in speaker; Smart Amp Technology",
                  "Built-in speaker and array microphone; Smart Amp",
                  key="sound"),
            field("keyboard", "asus_proart_p16_specs",
                  "Backlit Chiclet Keyboard; 1.7 mm key travel; Copilot key",
                  "Backlit chiclet keyboard; 1.7 mm travel; Copilot key",
                  key="keyboard"),
            field("touchpad", "asus_proart_p16_specs",
                  "Precision touchpad, support DialPad",
                  "Precision touchpad with DialPad support"),
            field("ports", "asus_proart_p16_specs",
                  "2 x USB 3.2 Gen 2 Type-A; 1 x USB4 Gen 3 Type-C (up to 40Gbps, display/power delivery); 1 x USB 3.2 Gen 2 Type-C (up to 10Gbps, display/power delivery); DC-in; 3.5mm combo audio; HDMI 2.1 FRL; SD Express 7.0 card reader",
                  "2 x USB-A 10Gbps; USB4 Type-C 40Gbps; USB-C 10Gbps; DC-in; 3.5 mm combo; HDMI 2.1 FRL; SD Express 7.0",
                  key="ports"),
            field("wifi", "asus_proart_p16_specs",
                  "Wi-Fi 7 (802.11be), triple-band, 2x2",
                  "Wi-Fi 7, triple-band 2x2", key="wifi"),
            field("bluetooth", "asus_proart_p16_specs",
                  "Bluetooth 5.4 wireless card; version may vary with OS and driver support",
                  "Bluetooth 5.4 (version may vary with OS and driver availability)"),
            field("dimensions", "asus_proart_p16_specs",
                  "35.49 x 24.69 x 1.49–1.83 cm", "35.49 x 24.69 x 1.49–1.83 cm",
                  key="dimensions"),
            field("weight", "asus_proart_p16_specs", "1.95 kg", 1950, key="weightG", unit="g"),
            field("security", "asus_proart_p16_specs",
                  "Firmware TPM; Microsoft Pluton security processor; IR webcam with Windows Hello support",
                  "Firmware TPM; Microsoft Pluton; IR Windows Hello camera"),
            field("warranty", "asus_proart_p16_product",
                  "3Y Warranty; 1 Year Local Accidental Damage Protection + Local On-site Support",
                  "3-year warranty; 1-year local accidental damage protection and local on-site support"),
            {
                "fieldId": "battery_life", "status": "NOT_DISCLOSED",
                "sourceId": "asus_proart_p16_specs",
                "sourceValue": "ASUS Philippines technical specification table lists battery capacity but no runtime estimate for H7606WW.",
                "normalizedValue": None, "unit": "hours",
                "note": "Runtime is not stated on the cited H7606WW technical table; no endurance figure was inferred.",
            },
            {
                "fieldId": "gpu_tgp", "status": "NOT_DISCLOSED",
                "sourceId": "asus_proart_p16_specs",
                "sourceValue": "ASUS Philippines technical specification table identifies the GPU and VRAM but does not state a total graphics power value for H7606WW.",
                "normalizedValue": None, "unit": "W",
                "note": "No TGP value is published in the cited H7606WW technical table; none was inferred from the GPU model.",
            },
        ],
    }
    return [acer_review, asus_review]


def main():
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    reviews = acer_records() + asus_records() + supplemental_laptop_records()
    for record in reviews:
        add_manual_field(manual, catalog, record["deviceId"], record["configurationId"], record)
    manual["reviewedAt"] = OBSERVED
    MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"laptopConfigsReviewed": len(reviews), "manualReviewRecords": len(manual["records"]), "reviewedAt": OBSERVED}, indent=2))


if __name__ == "__main__":
    main()
