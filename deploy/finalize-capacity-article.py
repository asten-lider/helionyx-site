#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
article = root / "articles" / "pochemu-9800-mah-ne-byvaet-v-akkumulyatore-pylesosa" / "index.html"
sitemap = root / "sitemap.xml"

article_text = article.read_text(encoding="utf-8")
article_text = article_text.replace("xiaomi-1c-6500/01.webp", "xiaomi-1c-6400/01.webp")
article.write_text(article_text, encoding="utf-8")

url = "https://helionyx.pro/articles/pochemu-9800-mah-ne-byvaet-v-akkumulyatore-pylesosa/"
entry = (
    "  <url><loc>" + url + "</loc><lastmod>2026-07-31</lastmod>"
    "<changefreq>monthly</changefreq><priority>0.9</priority></url>\n"
)
text = sitemap.read_text(encoding="utf-8")
if url not in text:
    marker = "  <url><loc>https://helionyx.pro/articles/zamena-akkumulyatora-xiaomi-vacuum-mop-1c/"
    position = text.find(marker)
    if position < 0:
        raise SystemExit("Не найдено место для статьи в sitemap.xml")
    text = text[:position] + entry + text[position:]
    sitemap.write_text(text, encoding="utf-8")

print("Статья о завышенной ёмкости проверена и добавлена в sitemap.")
