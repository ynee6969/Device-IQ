#!/usr/bin/env python3
"""Use the manufacturer's global launch date for the Black Shark 5 records."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "research/enrichment/manual-field-reviews.json"
DEVICE_ID = "device_a9d69522a3d0fe"
SOURCE = {
    "id": "black_shark_5_global_release",
    "publisher": "Black Shark (Global)",
    "url": "https://blackshark.gg/blogs/press-room/black-shark-launches-the-mobile-gaming-flagship-black-shark-5-series-globally",
    "publicationDate": "2022-06-09",
    "accessDate": "2026-11-26",
    "purpose": "Manufacturer-stated global availability of the Black Shark 5 series",
    "note": "Black Shark's global press release says the Black Shark 5 series was unveiled to the global market on June 9, 2022. This manufacturer date is recorded separately from the Philippine official sale start reported as July 2, 2022. GSMArena's April 4 release date refers to its technical model listing and is not used as the manufacturer-stated global availability date.",
}
FIELD_NOTE = "Manufacturer-stated global market unveiling date. The reported Philippine official sale began July 2, 2022. GSMArena lists April 4 for a technical model record; that date is not substituted for the manufacturer's stated global availability."


def main() -> None:
    data = json.loads(MANUAL.read_text(encoding="utf-8"))
    updated = 0
    for record in data["records"]:
        if record.get("deviceId") != DEVICE_ID:
            continue
        sources = record.setdefault("sources", [])
        if not any(item.get("id") == SOURCE["id"] for item in sources):
            sources.append(SOURCE.copy())
        release = next(item for item in record["fields"] if item.get("fieldId") == "global_release_date")
        release.update({
            "status": "VERIFIED",
            "sourceId": SOURCE["id"],
            "sourceValue": "Black Shark Global states the Black Shark 5 series was unveiled to the global market on June 9, 2022",
            "normalizedValue": "2022-06-09",
            "note": FIELD_NOTE,
        })
        evidence = record.get("availabilityEvidence")
        if evidence:
            notes = evidence.get("researchNotes", "")
            if "Black Shark's manufacturer press release states" not in notes:
                anchor = "YugaTech and REVU support two local RAM/storage variants:"
                if anchor not in notes:
                    raise ValueError("Expected Black Shark 5 research-notes anchor is missing")
                statement = "Black Shark's manufacturer press release states the series was unveiled to the global market on June 9, 2022; this is recorded separately from the Philippine official sale date of July 2, 2022 reported by YugaTech and REVU. "
                evidence["researchNotes"] = notes.replace(anchor, statement + anchor, 1)
        updated += 1
    if updated != 2:
        raise ValueError(f"Expected 2 Black Shark 5 configurations, updated {updated}")
    MANUAL.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {updated} Black Shark 5 configurations to 2022-06-09 using manufacturer source evidence.")


if __name__ == "__main__":
    main()
