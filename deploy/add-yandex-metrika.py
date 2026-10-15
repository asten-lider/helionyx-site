#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
COUNTER_ID = "111263691"

HEAD_SNIPPET = f'''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id={COUNTER_ID}', 'ym');

    ym({COUNTER_ID}, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
</script>'''

BODY_SNIPPET = f'''<noscript><div><img src="https://mc.yandex.ru/watch/{COUNTER_ID}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->'''

changed = 0
skipped = 0
errors = []

for page in sorted(ROOT.rglob("*.html")):
    rel = page.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        continue
    if len(rel.parts) == 1 and (rel.name.startswith("google") or rel.name.startswith("yandex")):
        skipped += 1
        continue

    text = page.read_text(encoding="utf-8")

    if f"mc.yandex.ru/metrika/tag.js?id={COUNTER_ID}" in text:
        skipped += 1
        continue

    if "</head>" not in text:
        errors.append(f"{page.relative_to(ROOT)}: нет </head>")
        continue

    body_match = re.search(r"<body(?:\s[^>]*)?>", text, flags=re.IGNORECASE)
    if not body_match:
        errors.append(f"{page.relative_to(ROOT)}: нет <body>")
        continue

    text = text.replace("</head>", f"  {HEAD_SNIPPET}\n</head>", 1)

    body_match = re.search(r"<body(?:\s[^>]*)?>", text, flags=re.IGNORECASE)
    insert_at = body_match.end()
    text = text[:insert_at] + "\n  " + BODY_SNIPPET + text[insert_at:]

    page.write_text(text, encoding="utf-8")
    changed += 1

if errors:
    raise SystemExit("Не удалось установить Метрику:\n" + "\n".join(errors))

print(f"Яндекс Метрика {COUNTER_ID}: обновлено {changed}, уже установлено {skipped} HTML-страниц.")
