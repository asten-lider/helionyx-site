#!/usr/bin/env python3
"""Read-only audit of original HELIONYX compatibility records vs published Product JSON-LD."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
records = []
for file in sorted((ROOT / "deploy").glob("helionyx-batteries-[1-4].json")):
    records.extend(json.loads(file.read_text(encoding="utf-8")).get("records", []))
if len(records) != 17:
    raise SystemExit(f"Expected 17 records, got {len(records)}")

lines = ["# Аудит совместимости HELIONYX", "", "Источник: 4 JSON-выгрузки исходной Excel-базы. Это утверждения из каталога, не независимая физическая проверка.", "",
         "| Карточка | Артикул из базы | Артикул сайта | Моделей в записи | Кодов устройств | Парт-номеров | Проверка |",
         "|---|---|---|---:|---:|---:|---|"]
issues = []
for row in records:
    slug = row["slug"]
    page = ROOT / "products" / slug / "index.html"
    html = page.read_text(encoding="utf-8")
    blocks = [json.loads(text) for text in re.findall(r'<script[^>]*type="application/ld[+]json"[^>]*>(.*?)</script>', html, re.S)]
    products = [p for p in blocks if p.get("@type") == "Product"]
    if len(products) != 1:
        raise SystemExit(f"{slug}: expected exactly one Product JSON-LD")
    product = products[0]
    source_sku = str(row.get("site_sku", ""))
    live_sku = str(product.get("sku", ""))
    match = source_sku == live_sku
    status = "OK" if match else "РАСХОЖДЕНИЕ SKU"
    if not match:
        issues.append((slug, source_sku, live_sku))
    count = lambda k: len([x for x in str(row.get(k) or "").split(",") if x.strip()])
    lines.append(f"| {slug} | {source_sku} | {live_sku} | {count('compatible_devices')} | {count('compatible_codes')} | {count('compatible_part_no')} | {status} |")
lines.extend(["", "## Требует ручного подтверждения", "",
              "Совпадение модели или парт-номера само по себе не доказывает электрическую и механическую совместимость. Перед расширением заявлений на сайте сверять напряжение, разъём, полярность, форму корпуса, BMS/сигнальные контакты и ревизию устройства.",
              "", "## Несовпадения артикулов", ""])
for slug,source,site in issues:
    lines.append(f"- `{slug}`: база `{source}`, карточка `{site}`. Не менять до сверки с фактическим SKU магазина.")
if not issues:
    lines.append("- Не обнаружены.")
out = ROOT / "docs" / "compatibility-audit.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Audited {len(records)} records; {len(issues)} SKU mismatches. Report: {out}")
