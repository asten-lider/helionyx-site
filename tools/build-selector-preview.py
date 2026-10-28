#!/usr/bin/env python3
"""Build an offline, internal-only HTML selector preview from the review matrix."""
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
matrix = ROOT / "data" / "compatibility-matrix-review.json"
subprocess.run([sys.executable, str(ROOT / "tools" / "build-compatibility-matrix.py")], check=True)
data = json.loads(matrix.read_text(encoding="utf-8"))
assert len(data["products"]) == 17
# Avoid a script end tag escaping embedded JSON into HTML.
payload = json.dumps(data["products"], ensure_ascii=False).replace("<", "\\u003c")
page = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>HELIONYX — внутренний подбор аккумулятора</title>
<style>
:root{color-scheme:light;font-family:system-ui,-apple-system,sans-serif}body{background:#f6f8fc;color:#17243b;margin:0}
main{max-width:880px;margin:40px auto;padding:0 18px}h1{font-size:clamp(25px,4vw,38px)}p{line-height:1.5}
input{box-sizing:border-box;width:100%;padding:15px;border:1px solid #b9c8d8;border-radius:12px;font-size:18px}
.card{background:white;border:1px solid #e2e8f0;border-radius:14px;padding:20px;margin:14px 0}
small,.muted{color:#53657d}.warning{border-left:4px solid #b97508;padding:12px;background:#fff9eb}
a{color:#145bd7}.tag{display:inline-block;padding:5px 9px;border-radius:8px;background:#e9f1ff;margin:5px 5px 5px 0}
</style></head><body><main><p class="muted">HELIONYX / ВНУТРЕННЯЯ ТЕСТОВАЯ ВЕРСИЯ</p>
<h1>Подбор аккумулятора</h1><p>Поиск по модели, коду устройства, парт-номеру старой батареи или артикулу HELIONYX.</p>
<label for="query"><b>Введите модель или номер АКБ</b></label>
<input id="query" placeholder="Например: Dyson V7 Absolute или P1904-4S1P-MM" autocomplete="off">
<p class="warning">Результат означает совпадение с исходной базой HELIONYX, <b>не подтверждённую физическую совместимость</b>. Перед покупкой проверять корпус, напряжение, разъём, полярность и ревизию устройства.</p>
<div id="results" aria-live="polite"><p class="muted">Для начала введите не менее 4 букв или цифр.</p></div>
</main><script id="data" type="application/json">__PAYLOAD__</script><script>
"use strict";
const products=JSON.parse(document.getElementById("data").textContent);
const q=document.getElementById("query"),out=document.getElementById("results");
const norm=s=>String(s||"").toLocaleLowerCase("ru").replace(/[^a-z0-9а-яё]/g,"");
function el(tag,text,cls){const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node;}
function update(){
out.replaceChildren();const term=norm(q.value);
if(term.length<4){out.append(el("p","Введите не менее четырёх букв или цифр.","muted"));return;}
let results=[];
for(const p of products){
 let hits=[];
 const sets=[["Код устройства",p.compatible_device_codes],["Парт-номер батареи",p.compatible_battery_part_numbers],["Модель техники",p.compatible_device_claims],["Артикул", [p.current_sku,p.source_sku]]];
 for(const [label,values] of sets)for(const value of values){
  const n=norm(value);if(n===term||(term.length>=6&&n.includes(term)))hits.push({label,value,exact:n===term});
 }
 if(hits.length){hits.sort((a,b)=>Number(b.exact)-Number(a.exact));results.push({p,hits});}
}
results.sort((a,b)=>Number(b.hits[0].exact)-Number(a.hits[0].exact));
if(!results.length){out.append(el("p","Совпадений в исходной базе нет. Нельзя обещать совместимость без дополнительной проверки."));return;}
out.append(el("p", "Найдено позиций: "+results.length,"muted"));
for(const {p,hits} of results){
 const card=el("article",undefined,"card");
 card.append(el("h2",p.current_sku));
 for(const hit of hits.slice(0,3))card.append(el("span",hit.label+": "+hit.value+(hit.exact?" (точное совпадение)":""),"tag"));
 card.append(el("p","Напряжение по исходной базе: "+(p.nominal_voltage??"требует уточнения")+" В"));
 card.append(el("p","Совместимость по исходной базе. Физическая проверка не проведена.","muted"));
 const link=el("a","Открыть карточку товара");link.href="https://helionyx.pro/products/"+encodeURIComponent(p.slug)+"/";link.target="_blank";link.rel="noopener noreferrer";card.append(link);out.append(card);
}
}
q.addEventListener("input",update);update();
</script></body></html>""".replace("__PAYLOAD__", payload)
target = ROOT / "internal" / "selector-preview.html"
target.parent.mkdir(exist_ok=True)
target.write_text(page, encoding="utf-8")
print(f"INTERNAL PREVIEW GENERATED: {target}, products={len(data['products'])}")
