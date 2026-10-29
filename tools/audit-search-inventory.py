#!/usr/bin/env python3
"""Audit HELIONYX organic-search product availability against local-warehouse snapshot.
Read-only: prints inconsistencies; never changes pages or publishes feeds.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data/yandex-verified-2026-10-28.csv"
with CSV.open(encoding="utf-8", newline="") as src:
    confirmed = {r["sku"]: r for r in csv.DictReader(src)}
problems = []
fulfillable_without_count = []
priced = 0
for path in sorted((ROOT / "products").glob("*/index.html")):
    html = path.read_text(encoding="utf-8")
    blocks = re.findall(r'<script[^>]*type=["\\\']application/ld[+]json["\\\'][^>]*>(.*?)</script>', html, re.I | re.S)
    products = [json.loads(t) for t in blocks if json.loads(t).get("@type") == "Product"]
    if len(products) != 1:
        problems.append(f"{path.parent.name}: invalid Product JSON-LD count")
        continue
    p = products[0]
    offer = p.get("offers") or {}
    sku = p.get("sku", "")
    if not offer.get("price"):
        continue
    priced += 1
    if sku not in confirmed:
        if offer.get("availability") == "https://schema.org/InStock":
            fulfillable_without_count.append(sku)
    else:
        if int(offer["price"]) != int(confirmed[sku]["price_rub"]):
            problems.append(f"{sku}: website price differs from approved feed")
        if offer.get("availability") != "https://schema.org/InStock":
            problems.append(f"{sku}: warehouse has stock but page is not marked InStock")
print(f"Audited {priced} priced product pages; {len(confirmed)} approved local-stock offers")
for sku in fulfillable_without_count:
    print("INFO:", sku, "has no reported local count; owner says a unit can be sourced for an order")
for problem in problems:
    print("REVIEW:", problem)
if problems:
    print("WARNING: SEO inventory discrepancies require owner review before changes.")
else:
    print("PASS: prices of confirmed stock align; sourcing-only items are not treated as out of stock.")
