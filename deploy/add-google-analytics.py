#!/usr/bin/env python3
"""Install GA4 on public HELIONYX HTML pages during VPS deployment."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_ID = "G-62246W7DKY"
MARKER = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID

SNIPPET = f'''<!-- Google Analytics 4 -->
<script async src="{MARKER}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{MEASUREMENT_ID}');
</script>
<!-- End Google Analytics 4 -->'''

changed = skipped = 0
for page in ROOT.rglob("*.html"):
    rel = page.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        continue
    if rel.parts[0] in ("admin", "payment-result", "checkout"):
        continue
    if len(rel.parts) == 1 and (rel.name.startswith("google") or rel.name.startswith("yandex")):
        continue
    html = page.read_text(encoding="utf-8")
    if MARKER in html:
        skipped += 1
        continue
    if "</head>" not in html:
        raise SystemExit(f"Missing </head>: {rel}")
    html = html.replace("</head>", f"  {SNIPPET}\n</head>", 1)
    page.write_text(html, encoding="utf-8")
    changed += 1

print(f"GA4 {MEASUREMENT_ID}: installed on {changed} pages, already present on {skipped}.")
