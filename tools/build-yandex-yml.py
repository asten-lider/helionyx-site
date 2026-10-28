#!/usr/bin/env python3
"""Produce a Yandex YML product feed from HELIONYX's published Product/Offer JSON-LD.

This export is not a stock-management system. Validate current stock and prices
before submitting the resulting feed to Yandex.
"""
import argparse
import datetime as dt
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://helionyx.pro"
AVAILABILITY = {"https://schema.org/InStock": "true", "https://schema.org/OutOfStock": "false",
                "https://schema.org/PreOrder": "false", "https://schema.org/BackOrder": "false"}

def product_data(page):
    content = page.read_text(encoding="utf-8")
    products = []
    for text in re.findall(r'<script[^>]*type=["\']application/ld[+]json["\'][^>]*>(.*?)</script>', content, re.I | re.S):
        data = json.loads(text)
        if data.get("@type") == "Product":
            products.append(data)
    if len(products) != 1:
        raise ValueError(f"{page}: expected one Product JSON-LD, found {len(products)}")
    return products[0]

def add(parent, tag, value):
    return ET.SubElement(parent, tag).__setattr__("text", str(value))

def generate(root, output):
    products = sorted((root / "products").glob("*/index.html"))
    if len(products) != 19:
        raise ValueError(f"Expected 19 products, found {len(products)}")
    catalog = ET.Element("yml_catalog", {"date": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")})
    shop = ET.SubElement(catalog, "shop")
    add(shop, "name", "HELIONYX")
    add(shop, "company", "ИП Швырев Евгений Александрович")
    add(shop, "url", BASE + "/")
    currencies = ET.SubElement(shop, "currencies")
    ET.SubElement(currencies, "currency", {"id": "RUB", "rate": "1"})
    categories = ET.SubElement(shop, "categories")
    ET.SubElement(categories, "category", {"id": "1"}).text = "Аккумуляторы для пылесосов"
    offers = ET.SubElement(shop, "offers")
    excluded = []
    for page in products:
        p = product_data(page)
        offer = p.get("offers")
        if not isinstance(offer, dict) or not offer.get("price"):
            excluded.append(page.parent.name)
            continue
        slug = page.parent.name
        url = BASE + "/products/" + slug + "/"
        if p.get("url") != url or offer.get("url") != url:
            raise ValueError(f"{slug}: canonical/offer URL mismatch")
        if offer.get("priceCurrency") != "RUB":
            raise ValueError(f"{slug}: currency mismatch")
        price = offer["price"]
        if isinstance(price, bool) or not isinstance(price, (float,int)) or price <= 0:
            raise ValueError(f"{slug}: invalid price")
        status = AVAILABILITY.get(offer.get("availability"))
        if status is None:
            raise ValueError(f"{slug}: unrecognized availability")
        images = p.get("image", [])
        if isinstance(images, str):
            images = [images]
        if not images or not all(u.startswith(BASE + "/") for u in images):
            raise ValueError(f"{slug}: missing/invalid image")
        sku = p.get("sku")
        if not sku:
            raise ValueError(f"{slug}: missing SKU")
        entry = ET.SubElement(offers, "offer", {"id": str(sku), "available": status})
        add(entry, "url", url)
        add(entry, "price", f"{price:g}")
        add(entry, "currencyId", "RUB")
        add(entry, "categoryId", "1")
        for img in images[:5]:
            add(entry, "picture", img)
        add(entry, "name", p["name"])
        add(entry, "vendor", p.get("brand", {}).get("name", "HELIONYX"))
        add(entry, "vendorCode", sku)
        add(entry, "description", p.get("description", ""))
    if len(offers) != 17:
        raise ValueError(f"Expected 17 priced products, got {len(offers)}")
    if len({x.attrib["id"] for x in offers}) != len(offers):
        raise ValueError("Duplicate product SKU in feed")
    ET.indent(catalog, space="  ")
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(catalog).write(output, encoding="utf-8", xml_declaration=True)
    print(f"YML OK: {len(offers)} offers; excluded unpriced: {', '.join(excluded)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    generate(args.root, args.output)
