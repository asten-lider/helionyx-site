#!/usr/bin/env python3
"""Internal, read-only battery selector. No public compatibility guarantees."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "compatibility-matrix-review.json"

def normalize(value):
    return re.sub(r"[^a-z0-9а-яё]+", "", str(value).casefold())

def search(products, query):
    q = normalize(query)
    if len(q) < 4:
        raise ValueError("Запрос слишком короткий: введите не меньше четырёх букв или цифр")
    found = []
    for p in products:
        groups = [
            ("Код устройства", p["compatible_device_codes"], 3),
            ("Парт-номер батареи", p["compatible_battery_part_numbers"], 3),
            ("Модель устройства", p["compatible_device_claims"], 2),
            ("Артикул HELIONYX", [p["current_sku"], p["source_sku"]], 3),
        ]
        matches = []
        for label, items, priority in groups:
            for item in items:
                n = normalize(item)
                if n == q or (len(q) >= 6 and q in n):
                    matches.append({"field": label, "source_value": item, "exact": n == q, "priority": priority})
        if matches:
            matches.sort(key=lambda m: (not m["exact"], -m["priority"], len(m["source_value"])))
            found.append({"slug": p["slug"], "sku": p["current_sku"], "url": "https://helionyx.pro/products/" + p["slug"] + "/", "matches": matches[:5], "verified_physical_fit": False, "warning": p["verification_note"]})
    found.sort(key=lambda p: (not p["matches"][0]["exact"], -p["matches"][0]["priority"], p["slug"]))
    return found

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Модель устройства, код, парт-номер АКБ или артикул")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not MATRIX.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "build-compatibility-matrix.py")], check=True, stdout=subprocess.DEVNULL)
    records = json.loads(MATRIX.read_text(encoding="utf-8"))["products"]
    found = search(records, args.query)
    if args.json:
        print(json.dumps({"query":args.query,"results":found}, ensure_ascii=False, indent=2))
    elif not found:
        print("Совпадений в исходной базе не найдено. Не подтверждайте совместимость без проверки.")
    else:
        for p in found:
            hit = p["matches"][0]
            print(f'{p["sku"]} | {hit["field"]}: {hit["source_value"]} | {p["url"]}')
            print("  Требуется проверка: корпус, разъём, полярность, напряжение, BMS и ревизия.")
if __name__ == "__main__":
    main()
