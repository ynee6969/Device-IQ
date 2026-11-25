#!/usr/bin/env python3
"""Keep only exact-match catalog images with a reusable license or permission.

Wikimedia Commons metadata is read through its public MediaWiki API. Images
without a recorded reuse license/permission are removed from the public image
manifest and their source/rights issue is kept in a separate audit file.
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "lib/catalog/image-manifest.json"
ALIASES = ROOT / "research/catalog-image-aliases.json"
CATALOG = ROOT / "lib/catalog/public-inventory.json"
UNAVAILABLE = ROOT / "research/catalog-image-unavailable.json"
OBSERVED = "2026-11-26"
XIAOMI_TERMS = "https://www.mi.com/ph/support/terms/terms-of-use/"
SAMSUNG_TERMS = "https://www.samsung.com/ph/business/info/legal/"
ASUS_TERMS = "https://www.asus.com/ph/terms_of_use_notice_privacy_policy/official-site/"


def clean_html(value):
    return re.sub(r"<[^>]+>", "", str(value or "")).replace("&amp;", "&").strip()


def commons_metadata(items):
    """Fetch metadata in small batches and return by normalized Commons title."""
    result = {}
    for start in range(0, len(items), 25):
        batch = items[start:start + 25]
        query = urllib.parse.urlencode({
            "action": "query", "prop": "imageinfo", "iiprop": "url|extmetadata",
            "titles": "|".join(item[1] for item in batch),
            "format": "json", "formatversion": "2",
        })
        request = urllib.request.Request(
            "https://commons.wikimedia.org/w/api.php?" + query,
            headers={"User-Agent": "DeviceIQ research audit/1.0 (https://github.com/ynee6969/Device-IQ)"},
        )
        payload = json.loads(urllib.request.urlopen(request, timeout=30).read())
        pages = {page["title"].casefold(): page for page in payload["query"]["pages"]}
        normalized = {row["from"].replace("_", " ").casefold(): row["to"].casefold()
                      for row in payload["query"].get("normalized", [])}
        for key, title, _ in batch:
            lookup = title.replace("_", " ").casefold()
            page = pages.get(lookup) or pages.get(normalized.get(lookup, ""))
            if not page or "imageinfo" not in page:
                raise ValueError(f"Commons page unavailable: {title}")
            metadata = page["imageinfo"][0].get("extmetadata", {})
            value = lambda name: clean_html(metadata.get(name, {}).get("value"))
            license_name = value("LicenseShortName")
            license_url = value("LicenseUrl")
            if license_url.startswith("http://creativecommons.org/"):
                license_url = "https://creativecommons.org/" + license_url.removeprefix("http://creativecommons.org/")
            artist = value("Artist")
            usage = value("UsageTerms") or license_name
            if not license_name or not license_url or not artist:
                raise ValueError(f"Commons image lacks usable license metadata: {title}")
            if license_name not in {"CC0", "CC BY 4.0", "CC BY-SA 3.0", "CC BY-SA 4.0"}:
                raise ValueError(f"Commons license needs manual review: {title} ({license_name})")
            result[key] = {
                "credit": f"{artist} (Wikimedia Commons)",
                "usageTerms": usage,
                "licenseUrl": license_url,
                "rightsCheckedAt": OBSERVED,
                "changes": "Converted to WebP for catalog delivery; no subject editing.",
            }
    return result


def identity_for_key(key, manifest, aliases, devices):
    by_image_id = next((device_id for device_id, device in devices.items()
                        if device.get("imageId") == key), None)
    if by_image_id:
        return by_image_id, devices[by_image_id]
    path = manifest[key].get("path")
    by_shared_asset = next((device_id for device_id, device in devices.items()
                            if device.get("imageId") in manifest
                            and manifest[device["imageId"]].get("path") == path), None)
    if by_shared_asset:
        return by_shared_asset, devices[by_shared_asset]
    device_id = next((device_id for device_id, alias in aliases.items() if alias == key), key)
    device = devices.get(device_id)
    if not device:
        # Old image entries can outlive a catalog record after workbook
        # reconciliation. They are not evidence for a current public record.
        return None, None
    return device_id, device


def terms_for(source_page):
    host = urllib.parse.urlparse(source_page).hostname or ""
    if host.endswith("mi.com") or host.endswith("appmifile.com"):
        return "REUSE_PERMISSION_REQUIRED", XIAOMI_TERMS, "Xiaomi site terms prohibit copying or republishing site content without express authorization."
    if host.endswith("samsung.com") or host.endswith("samsungebiz.com"):
        return "REUSE_PERMISSION_REQUIRED", SAMSUNG_TERMS, "Samsung states that its site content remains Samsung/licensor property and grants no reuse license for this use."
    if host.endswith("asus.com"):
        return "REUSE_PERMISSION_REQUIRED", ASUS_TERMS, "ASUS terms state that site photos/materials may not be reused without prior written permission."
    return "REUSE_RIGHTS_NOT_ESTABLISHED", None, "No reusable image license or written permission is recorded in the project."


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    aliases = json.loads(ALIASES.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    previous_unavailable = json.loads(UNAVAILABLE.read_text(encoding="utf-8")) if UNAVAILABLE.exists() else {}
    devices = {device["id"]: device for device in catalog}
    commons = []
    for key, image in manifest.items():
        if "commons.wikimedia.org/wiki/File:" in image.get("sourcePage", ""):
            title = urllib.parse.unquote(urllib.parse.urlparse(image["sourcePage"]).path.removeprefix("/wiki/"))
            commons.append((key, title, image))
    rights = commons_metadata(commons)

    kept = {}
    unavailable = {}
    assigned_devices = set()
    for key, image in manifest.items():
        device_id, device = identity_for_key(key, manifest, aliases, devices)
        if not device_id:
            continue
        if key in rights:
            kept[key] = {**image, **rights[key]}
            assigned_devices.add(device_id)
            continue
        status, rights_url, reason = terms_for(image.get("sourcePage", ""))
        unavailable[device_id] = {
            "status": status,
            "reason": reason,
            "sourcePage": image.get("sourcePage"),
            "assetUrl": image.get("assetUrl"),
            "scope": image.get("scope"),
            "rightsTermsUrl": rights_url,
            "observedAt": OBSERVED,
            "altText": f"Image unavailable for {device.get('brand', '')} {device.get('model', '')}",
        }

    for device_id, device in devices.items():
        if device_id in assigned_devices or device_id in unavailable:
            continue
        if device_id in previous_unavailable:
            unavailable[device_id] = previous_unavailable[device_id]
            continue
        unavailable[device_id] = {
            "status": "NO_RELIABLE_MATCH",
            "reason": "No reliable exact-model image with documented reuse rights is currently assigned.",
            "sourcePage": None,
            "assetUrl": None,
            "scope": None,
            "rightsTermsUrl": None,
            "observedAt": OBSERVED,
            "altText": f"Image unavailable for {device.get('brand', '')} {device.get('model', '')}",
        }

    kept_paths = {image["path"] for image in kept.values()}
    removed_paths = {image["path"] for key, image in manifest.items() if key not in kept}
    deleted_files = 0
    for public_path in sorted(removed_paths - kept_paths):
        asset = (ROOT / "public" / public_path.lstrip("/")).resolve()
        public_root = (ROOT / "public").resolve()
        if public_root not in asset.parents:
            raise ValueError(f"Refusing to remove image outside public directory: {asset}")
        if asset.exists():
            asset.unlink()
            deleted_files += 1

    MANIFEST.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    UNAVAILABLE.write_text(json.dumps(unavailable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    statuses = [row.get("status") for row in unavailable.values()]
    print(json.dumps({"priorAssignments": len(manifest), "licensedAssignmentsKept": len(kept),
                      "imageUnavailableRecords": len(unavailable),
                      "reusePermissionRequired": statuses.count("REUSE_PERMISSION_REQUIRED"),
                      "reuseRightsNotEstablished": statuses.count("REUSE_RIGHTS_NOT_ESTABLISHED"),
                      "noReliableMatch": statuses.count("NO_RELIABLE_MATCH"),
                      "removedLocalAssets": deleted_files,
                      "observedAt": OBSERVED}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
