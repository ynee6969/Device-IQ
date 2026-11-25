#!/usr/bin/env python3
"""Merge collected candidate evidence without discarding the prior snapshot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows_by_key(rows: list[dict], key_fields: tuple[str, ...]) -> list[dict]:
    grouped: dict[tuple, dict] = {}
    for row in rows:
        key = tuple(row.get(field) for field in key_fields)
        current = grouped.get(key)
        if current is None or str(row.get("observed_at") or "") >= str(current.get("observed_at") or ""):
            grouped[key] = row
    return list(grouped.values())


def merge():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=ROOT / "research/enrichment/latest.json")
    parser.add_argument("--incoming", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "research/enrichment/latest.json")
    args = parser.parse_args()
    base = json.loads(args.base.read_text(encoding="utf-8"))
    incoming = json.loads(args.incoming.read_text(encoding="utf-8"))

    merged = dict(base)
    for collection, key_fields in {
        "observations": ("device_id", "key", "value", "unit", "source_url"),
        "prices": ("device_id", "amount_php", "variant_ram_gb", "variant_storage_gb", "source_url", "observed_at"),
        "fetches": ("device_id", "source_url", "status"),
        "discovery": ("device_id", "source_url", "source_kind", "status"),
    }.items():
        merged[collection] = rows_by_key([*base.get(collection, []), *incoming.get(collection, [])], key_fields)

    model_rows = {row["device_id"]: row for row in base.get("models", [])}
    model_rows.update({row["device_id"]: row for row in incoming.get("models", [])})
    merged["models"] = list(model_rows.values())
    merged["run_at"] = incoming.get("run_at") or base.get("run_at")
    merged["inventory_count"] = incoming.get("inventory_count", base.get("inventory_count"))
    merged["selected_count"] = incoming.get("selected_count", base.get("selected_count"))
    merged["merged_runs"] = [
        *base.get("merged_runs", []),
        {"run_at": base.get("run_at"), "observations": len(base.get("observations", [])),
         "prices": len(base.get("prices", [])), "fetches": len(base.get("fetches", []))},
        {"run_at": incoming.get("run_at"), "observations": len(incoming.get("observations", [])),
         "prices": len(incoming.get("prices", [])), "fetches": len(incoming.get("fetches", []))},
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"observations": len(merged["observations"]), "prices": len(merged["prices"]),
                      "fetches": len(merged["fetches"]), "discovery": len(merged["discovery"]),
                      "incomingRunAt": incoming.get("run_at"), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    merge()
