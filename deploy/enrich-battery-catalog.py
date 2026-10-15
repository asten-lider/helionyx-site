#!/usr/bin/env python3
"""Enrich all HELIONYX product pages from the authoritative battery catalog."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).with_name("helionyx-batteries.json")
CSS_HREF = "../../assets/battery-data.css"

PRODUCT_PAGE_PATTERN = re.compile(
    r'<section class="section section--soft">\s*'
    r'<div class="container product-details(?: [^"]*)?">\s*'
    r'<div><span class="eyebrow">[^<]*совместимост(?:ь|и)[^<]*</span>.*?</section>',
    re.DOTALL | re.IGNORECASE,
)
GENERATED_PATTERN = re.compile(
    r'<!-- HELIONYX_BATTERY_DATA_START -->.*?'
    r'<!-- HELIONYX_BATTERY_DATA_END -->',
    re.DOTALL,
)
ARTICLE_PATTERN = re.compile(
    r'<article class="product-card"(?P<attrs>[^>]*)>.*?'
    r'<button[^>]*data-product="(?P<slug>[^"]+)"[^>]*>.*?</article>',
    re.DOTALL,
)
PRODUCT_JSON_LD_PATTERN = re.compile(
    r'(<script type="application/ld\+json">)(.*?)(</script>)',
    re.DOTALL,
)


def values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(part).strip() for part in value if str(part).strip()]
    return [part.strip() for part in str(value).split(";") if part.strip()]


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def num(value: Any) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value).replace(".", ",")


def list_html(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def first(items: list[str], count: int = 1) -> str:
    return ", ".join(items[:count])


def truncate(text: str, limit: int = 158) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    shortened = text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,.;:")
    return shortened + "…"


def yes_no(value: Any) -> str:
    return "есть" if str(value).strip().casefold() == "да" else "нет"


def build_meta(record: dict[str, Any]) -> str:
    devices = values(record.get("compatible_devices"))
    codes = values(record.get("compatible_codes"))
    parts = values(record.get("compatible_part_no"))
    text = (
        f"Аккумулятор {record['site_sku']} для {first(devices, 2)}. "
        f"{num(record.get('typical_capacity'))} мАч, "
        f"{num(record.get('nominal_voltage'))} В. "
    )
    if codes:
        text += f"Коды: {first(codes, 2)}. "
    if parts:
        text += f"Part No.: {first(parts, 1)}. "
    text += f"Гарантия {num(record.get('warranty_months'))} месяцев."
    return truncate(text)


def build_description(record: dict[str, Any]) -> str:
    devices = values(record.get("compatible_devices"))
    codes = values(record.get("compatible_codes"))
    parts = values(record.get("compatible_part_no"))
    chunks = [
        f"Литий-ионный аккумулятор HELIONYX {record['site_sku']}",
        f"{num(record.get('typical_capacity'))} мАч",
        f"{num(record.get('nominal_voltage'))} В",
    ]
    if devices:
        chunks.append("для " + ", ".join(devices))
    if codes:
        chunks.append("совместимые коды: " + ", ".join(codes))
    if parts:
        chunks.append("заменяет аккумуляторы: " + ", ".join(parts))
    return ". ".join(chunks) + "."


def compatibility_block(record: dict[str, Any]) -> str:
    devices = values(record.get("compatible_devices"))
    codes = values(record.get("compatible_codes"))
    parts = values(record.get("compatible_part_no"))
    model_note = ""
    if record["source_model"] != record["site_sku"]:
        model_note = (
            f"<p class=\"battery-catalog__model-note\">"
            f"Артикул на сайте: <strong>{esc(record['site_sku'])}</strong>. "
            f"Обозначение модели в технической документации: "
            f"<strong>{esc(record['source_model'])}</strong>.</p>"
        )
    return f'''<!-- HELIONYX_BATTERY_DATA_START -->
<section class="section section--soft battery-catalog-section" data-authoritative-battery-data>
  <div class="container battery-catalog">
    <div class="battery-catalog__heading">
      <span class="eyebrow">Совместимость</span>
      <h2>Совместимые модели, коды устройств и номера аккумуляторов</h2>
      <p>Полный перечень совместимости для аккумулятора HELIONYX {esc(record["site_sku"])}.</p>
      {model_note}
    </div>
    <div class="battery-catalog__columns">
      <article>
        <h3>Модели пылесосов</h3>
        {list_html(devices)}
      </article>
      <article>
        <h3>Коды и обозначения устройств</h3>
        {list_html(codes)}
      </article>
      <article>
        <h3>Совместимые Part No. аккумуляторов</h3>
        {list_html(parts)}
      </article>
    </div>
  </div>
</section>

<section class="section battery-tech-section">
  <div class="container battery-tech">
    <div class="battery-tech__heading">
      <span class="eyebrow">Технические данные</span>
      <h2>Характеристики аккумулятора {esc(record["site_sku"])}</h2>
    </div>
    <dl class="battery-tech__grid">
      <div><dt>Химическая система</dt><dd>{esc(record.get("chemistry") or "—")}</dd></div>
      <div><dt>Конфигурация</dt><dd>{esc(record.get("config") or "—")}</dd></div>
      <div><dt>Номинальное напряжение</dt><dd>{num(record.get("nominal_voltage"))} В</dd></div>
      <div><dt>Максимальное напряжение заряда</dt><dd>{num(record.get("max_charge_voltage"))} В</dd></div>
      <div><dt>Типовая ёмкость</dt><dd>{num(record.get("typical_capacity"))} мАч</dd></div>
      <div><dt>Нормированная ёмкость</dt><dd>{num(record.get("rated_capacity"))} мАч</dd></div>
      <div><dt>Типовая энергия</dt><dd>{num(record.get("typical_energy"))} Вт·ч</dd></div>
      <div><dt>Нормированная энергия</dt><dd>{num(record.get("rated_energy"))} Вт·ч</dd></div>
      <div><dt>Элементы</dt><dd>{num(record.get("cell_count"))} × {esc(record.get("cell_format") or "—")}, {esc(record.get("cell_model") or "—")}</dd></div>
      <div><dt>Максимальный длительный ток</dt><dd>{num(record.get("max_continuous_discharge_current"))} А</dd></div>
      <div><dt>Метод заряда</dt><dd>{esc(record.get("charge_method") or "—")}</dd></div>
      <div><dt>Гарантия</dt><dd>{num(record.get("warranty_months"))} месяцев</dd></div>
    </dl>

    <details class="battery-tech__details">
      <summary>Температуры, BMS и защитные функции</summary>
      <div class="battery-tech__details-grid">
        <div>
          <h3>Температурные условия</h3>
          <ul>
            <li>Заряд: от {num(record.get("charge_temp_min"))} до {num(record.get("charge_temp_max"))} °C</li>
            <li>Разряд: от {num(record.get("discharge_temp_min"))} до {num(record.get("discharge_temp_max"))} °C</li>
            <li>Хранение: от {num(record.get("storage_temp_min"))} до {num(record.get("storage_temp_max"))} °C</li>
            <li>Рекомендуемый заряд при хранении: {esc(record.get("storage_soc") or "—")}</li>
          </ul>
        </div>
        <div>
          <h3>Система защиты</h3>
          <ul>
            <li>BMS: {yes_no(record.get("bms_installed"))}</li>
            <li>Защита от перезаряда: {yes_no(record.get("protection_overcharge"))}</li>
            <li>Защита от переразряда: {yes_no(record.get("protection_overdischarge"))}</li>
            <li>Защита от перегрузки по току: {yes_no(record.get("protection_overcurrent"))}</li>
            <li>Защита от короткого замыкания: {yes_no(record.get("protection_short_circuit"))}</li>
          </ul>
        </div>
        <div>
          <h3>Подключение и контроль</h3>
          <ul>
            <li>Количество контактов: {num(record.get("connector_count"))}</li>
            <li>Распиновка: {esc(record.get("connector_pinout") or "не указана")}</li>
            <li>Термоконтроль: {esc(record.get("ntc") or "не указан")}</li>
            <li>{esc(record.get("temperature_control") or "Сигнал контроля температуры обрабатывается совместимым устройством.")}</li>
          </ul>
        </div>
      </div>
    </details>

    <details class="battery-tech__details">
      <summary>Производитель и техническая документация</summary>
      <div class="battery-tech__document">
        <p><strong>Производитель:</strong> {esc(record.get("manufacturer") or "—")}</p>
        <p><strong>Страна производства:</strong> {esc(record.get("country") or "—")}</p>
        <p><strong>Обозначение руководства:</strong> {esc(record.get("document_designation") or "—")}, редакция {esc(record.get("document_revision") or "—")}</p>
        <p><strong>Дата производства:</strong> {esc(record.get("production_date") or "—")}</p>
        <p><strong>Стандарты:</strong> {esc(record.get("standards") or "—")}</p>
      </div>
    </details>
  </div>
</section>
<!-- HELIONYX_BATTERY_DATA_END -->'''


def update_json_ld(text: str, record: dict[str, Any], description: str) -> str:
    def replace(match: re.Match[str]) -> str:
        raw = match.group(2)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        if payload.get("@type") != "Product":
            return match.group(0)

        payload["description"] = description
        payload["model"] = record["source_model"]
        payload["additionalProperty"] = [
            {"@type": "PropertyValue", "name": "Артикул HELIONYX", "value": record["site_sku"]},
            {"@type": "PropertyValue", "name": "Конфигурация", "value": record.get("config")},
            {"@type": "PropertyValue", "name": "Номинальное напряжение", "value": f"{num(record.get('nominal_voltage'))} В"},
            {"@type": "PropertyValue", "name": "Типовая ёмкость", "value": f"{num(record.get('typical_capacity'))} мАч"},
            {"@type": "PropertyValue", "name": "Нормированная ёмкость", "value": f"{num(record.get('rated_capacity'))} мАч"},
            {"@type": "PropertyValue", "name": "Совместимые устройства", "value": "; ".join(values(record.get("compatible_devices")))},
            {"@type": "PropertyValue", "name": "Коды устройств", "value": "; ".join(values(record.get("compatible_codes")))},
            {"@type": "PropertyValue", "name": "Совместимые Part No.", "value": "; ".join(values(record.get("compatible_part_no")))},
        ]
        return match.group(1) + json.dumps(
            payload, ensure_ascii=False, separators=(",", ":")
        ) + match.group(3)

    return PRODUCT_JSON_LD_PATTERN.sub(replace, text)


def enrich_product_page(record: dict[str, Any]) -> None:
    path = ROOT / "products" / record["slug"] / "index.html"
    if not path.exists():
        raise SystemExit(f"Не найдена карточка товара: {path}")

    text = path.read_text(encoding="utf-8")
    meta = build_meta(record)
    description = build_description(record)

    text, meta_count = re.subn(
        r'(<meta name="description" content=")[^"]*(">)',
        lambda m: m.group(1) + esc(meta) + m.group(2),
        text,
        count=1,
    )
    if meta_count != 1:
        raise SystemExit(f"Не найден meta description: {path}")

    text = re.sub(
        r'(<meta property="og:description" content=")[^"]*(">)',
        lambda m: m.group(1) + esc(meta) + m.group(2),
        text,
        count=1,
    )
    text = update_json_ld(text, record, description)

    css_tag = f'<link rel="stylesheet" href="{CSS_HREF}">'
    if css_tag not in text:
        site_css = '<link rel="stylesheet" href="../../assets/site.css">'
        if site_css not in text:
            raise SystemExit(f"Не найдена основная таблица стилей: {path}")
        text = text.replace(site_css, site_css + "\n  " + css_tag, 1)

    generated = compatibility_block(record)
    if GENERATED_PATTERN.search(text):
        text = GENERATED_PATTERN.sub(generated, text, count=1)
    else:
        text, count = PRODUCT_PAGE_PATTERN.subn(generated, text, count=1)
        if count != 1:
            raise SystemExit(f"Не найден исходный блок совместимости: {path}")

    path.write_text(text, encoding="utf-8")
    print(f"Карточка обновлена: {record['slug']}")


def search_text(record: dict[str, Any]) -> str:
    parts = [
        record["site_sku"],
        record["source_model"],
        record.get("compatible_devices"),
        record.get("compatible_codes"),
        record.get("compatible_part_no"),
        record.get("typical_capacity"),
        record.get("rated_capacity"),
        record.get("nominal_voltage"),
        record.get("cell_model"),
    ]
    return re.sub(r"\s+", " ", " ".join(str(part) for part in parts if part)).strip().casefold()


def enrich_search_indexes(by_slug: dict[str, dict[str, Any]]) -> None:
    for path in ROOT.rglob("*.html"):
        if "admin" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")

        def replace_article(match: re.Match[str]) -> str:
            slug = match.group("slug")
            record = by_slug.get(slug)
            if not record:
                return match.group(0)
            block = match.group(0)
            opening_end = block.find(">")
            opening = block[: opening_end + 1]
            rest = block[opening_end + 1 :]
            value = esc(search_text(record))
            if re.search(r'\sdata-search="[^"]*"', opening):
                opening = re.sub(
                    r'\sdata-search="[^"]*"',
                    f' data-search="{value}"',
                    opening,
                    count=1,
                )
            else:
                opening = opening[:-1] + f' data-search="{value}">'
            return opening + rest

        new_text = ARTICLE_PATTERN.sub(replace_article, text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"Поисковый индекс обновлён: {path.relative_to(ROOT)}")


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    common = payload.get("common") or {}
    records = [{**common, **record} for record in (payload.get("records") or [])]
    if len(records) != 17:
        raise SystemExit(f"Ожидалось 17 аккумуляторов, получено: {len(records)}")

    by_slug = {record["slug"]: record for record in records}
    if len(by_slug) != 17:
        raise SystemExit("В каталоге найдены повторяющиеся slug")

    for record in records:
        enrich_product_page(record)
    enrich_search_indexes(by_slug)
    print("Готово: 17 карточек и поисковые индексы обновлены из единой базы HELIONYX.")


if __name__ == "__main__":
    main()
