#!/usr/bin/env python3
"""Build a review-only compatibility matrix from Excel-derived source records.

Device and part-number entries are source claims, not independently verified fits.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
aliases = json.loads((DATA / "confirmed-sku-aliases.json").read_text(encoding="utf-8"))
alias_map = {x["slug"]: x for x in aliases["items"]}
records = []
for path in sorted((ROOT / "deploy").glob("helionyx-batteries-[1-4].json")):
    records.extend(json.loads(path.read_text(encoding="utf-8"))["records"])
assert len(records) == 17
assert len({x["slug"] for x in records}) == len(records)

def tokens(value):
    # Source JSON stores arrays; preserve each array entry (including commas inside model names).
    if value is None:
        return []
    if isinstance(value, list):
        entries = value
    elif isinstance(value, str):
        entries = value.split(",")
    else:
        raise TypeError(f"Unexpected compatibility field type: {type(value).__name__}")
    return list(dict.fromkeys(v.strip() for v in entries if isinstance(v, str) and v.strip()))

def get_product(slug):
    html = (ROOT / "products" / slug / "index.html").read_text(encoding="utf-8")
    found = []
    for text in re.findall(r'<script[^>]+type=["\']application/ld[+]json["\'][^>]*>(.*?)</script>', html, re.S):
        data = json.loads(text)
        if data.get("@type") == "Product":
            found.append(data)
    if len(found) != 1:
        raise ValueError(f"{slug}: expected one Product schema, got {len(found)}")
    return found[0]

matrix = []
warnings = []
for item in records:
    slug = item["slug"]
    schema = get_product(slug)
    current = schema["sku"]
    source = item["site_sku"]
    alias = alias_map.get(slug)
    if source != current and not (alias and alias["confirmed"] and alias["source_sku"] == source and alias["current_sku"] == current):
        warnings.append(f"UNCONFIRMED SKU: {slug}: {source} -> {current}")
    models = tokens(item.get("compatible_devices"))
    codes = tokens(item.get("compatible_codes"))
    parts = tokens(item.get("compatible_part_no"))
    if not models:
        warnings.append(f"NO DEVICE MODELS: {slug}")
    if not parts:
        warnings.append(f"NO BATTERY PART NUMBERS: {slug}")
    matrix.append({
        "slug": slug,
        "source_sku": source,
        "current_sku": current,
        "sku_alias_confirmed": bool(source == current or (alias and alias["confirmed"])),
        "nominal_voltage": item.get("nominal_voltage"),
        "connector_pinout": item.get("connector_pinout"),
        "compatible_device_claims": models,
        "compatible_device_codes": codes,
        "compatible_battery_part_numbers": parts,
        "compatibility_evidence": "owner_supplied_excel_derived",
        "physical_fit_verified": False,
        "verification_note": "Check body, connector, polarity, BMS, voltage and device revision before promising fit"
    })
    if len(models) > 20:
        warnings.append(f"BROAD MODEL CLAIMS ({len(models)}): {slug} — manual validation advised")

DATA.mkdir(exist_ok=True)
(DATA / "compatibility-matrix-review.json").write_text(json.dumps({
    "schema_version": 1,
    "purpose": "Internal review only; never use as confirmed public fitment",
    "products": matrix,
    "warnings": warnings
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Products: {len(matrix)}, owner-confirmed alias pairs: {len(alias_map)}, review warnings: {len(warnings)}")
for warning in warnings:
    print("REVIEW:", warning)
