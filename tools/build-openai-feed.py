#!/usr/bin/env python3
"""Build an OpenAI discovery feed from existing public Product JSON-LD.

This is an export only: it does not submit a feed or modify inventory.
"""
import argparse
import json
import re
from pathlib import Path

BASE = "https://helionyx.pro"
REQUIRED = ("item_id", "title", "description", "url", "brand", "seller_name", "image_url", "availability", "price")
STATUS = {
    "https://schema.org/InStock": "in_stock",
    "https://schema.org/OutOfStock": "out_of_stock",
    "https://schema.org/PreOrder": "pre_order",
    "https://schema.org/BackOrder": "backorder",
    "https://schema.org/LimitedAvailability": "unknown",
}


def extract_jsonld(html):
    for raw in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.I | re.S):
        data = json.loads(raw)
        for item in data if isinstance(data, list) else [data]:
            if item.get("@type") == "Product":
                return item
    raise ValueError("Product JSON-LD not found")


def record(path):
    product = extract_jsonld(path.read_text(encoding="utf-8"))
    offer = product.get("offers") or {}
    # Products awaiting pricing are deliberately excluded; never invent prices.
    if not isinstance(offer, dict) or not offer.get("price"):
        return None
    slug = path.parent.name
    expected_url = f"{BASE}/products/{slug}/"
    if product.get("url") != expected_url or offer.get("url") != expected_url:
        raise ValueError(f"{slug}: product/offer URL mismatch")
    images = product.get("image") or []
    if isinstance(images, str):
        images = [images]
    if not images or any(not u.startswith(BASE + "/") for u in images):
        raise ValueError(f"{slug}: invalid image URLs")
    currency = offer.get("priceCurrency")
    if currency != "RUB":
        raise ValueError(f"{slug}: unexpected currency")
    amount = offer["price"]
    if not isinstance(amount, (float, int)) or isinstance(amount, bool) or amount <= 0:
        raise ValueError(f"{slug}: invalid price")
    availability = STATUS.get(offer.get("availability"))
    if availability is None:
        raise ValueError(f"{slug}: unsupported stock status")
    seller = offer.get("seller") or {}
    rec = {
        "item_id": product.get("sku") or slug,
        "title": product.get("name"),
        "description": product.get("description"),
        "url": expected_url,
        "brand": (product.get("brand") or {}).get("name"),
        "seller_name": seller.get("name"),
        "image_url": images[0],
        "availability": availability,
        "price": f"{amount:.2f} RUB",
        "is_eligible_checkout": False,
        "is_ads_eligible": False,
    }
    if len(images) > 1:
        rec["additional_image_urls"] = images[1:]
    if product.get("mpn"):
        rec["mpn"] = product["mpn"]
    for field in REQUIRED:
        if not rec.get(field):
            raise ValueError(f"{slug}: missing {field}")
    return rec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    products = sorted((args.root / "products").glob("*/index.html"))
    if not products:
        raise SystemExit("No product pages found")
    rows = [record(path) for path in products]
    rows = [row for row in rows if row is not None]
    ids = [row["item_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate item IDs")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    print(f"Exported {len(rows)} priced products; excluded {len(products)-len(rows)} without a confirmed price")


if __name__ == "__main__":
    main()
