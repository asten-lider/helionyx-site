(function () {
  if (window.location.pathname !== "/catalog/" || document.querySelector("[data-advanced-catalog-filters]")) return;

  const PRODUCTS_META = {
    "dyson-v7": { brand: "dyson", voltage: "21.6", capacity: 2500, batteryType: "standard" },
    "dyson-v6": { brand: "dyson", voltage: "21.6", capacity: 2500, batteryType: "standard" },
    "dyson-v11": { brand: "dyson", voltage: "25.2", capacity: 4000, batteryType: "extended" },
    "dreame-5200": { brand: "dreame", voltage: "14.4", capacity: 5200, batteryType: "standard" },
    "samsung-jet90": { brand: "samsung", voltage: "21.6", capacity: 4000, batteryType: "extended" },
    "exvac-3200": { brand: "other", voltage: "14.4", capacity: 3200, batteryType: "standard" },
    "mop2-lite": { brand: "xiaomi", voltage: "14.4", capacity: 3200, batteryType: "standard" },
    "mop2-3200": { brand: "xiaomi", voltage: "14.4", capacity: 3200, batteryType: "standard" },
    "xiaomi-g1": { brand: "xiaomi", voltage: "14.4", capacity: 3200, batteryType: "standard" },
    "samsung-jet60": { brand: "samsung", voltage: "21.6", capacity: 4000, batteryType: "extended" },
    "lg-a9": { brand: "lg", voltage: "25.2", capacity: 2500, batteryType: "standard" },
    "samsung-jet70": { brand: "samsung", voltage: "21.6", capacity: 4000, batteryType: "extended" },
    "dreame-6400": { brand: "dreame", voltage: "14.4", capacity: 6400, batteryType: "extended" },
    "xiaomi-1c-5200": { brand: "xiaomi", voltage: "14.4", capacity: 5200, batteryType: "standard" },
    "roborock-6400": { brand: "roborock", voltage: "14.4", capacity: 6400, batteryType: "extended" },
    "xiaomi-mopp-3200": { brand: "xiaomi", voltage: "14.4", capacity: 3200, batteryType: "standard" },
    "xiaomi-1c-6400": { brand: "xiaomi", voltage: "14.4", capacity: 6400, batteryType: "extended" },
    "batlfp12100": { brand: "helionyx", voltage: "12.8", capacity: 100000, batteryType: "lifepo4" },
    "batlfp12100h": { brand: "helionyx", voltage: "12.8", capacity: 100000, batteryType: "lifepo4-heated" }
  };

  const tools = document.querySelector(".catalog-tools");
  const grid = document.querySelector("[data-product-grid]");
  if (!tools || !grid) return;

  const cards = Array.from(grid.querySelectorAll(".product-card"));
  cards.forEach((card, index) => {
    const button = card.querySelector("[data-product]");
    const slug = card.dataset.slug || button?.dataset.product || "";
    const meta = PRODUCTS_META[slug] || {};
    const priceText = card.querySelector(".product-card__bottom strong")?.textContent || "";
    const title = card.querySelector(".product-card__title")?.textContent?.trim() || "";
    card.dataset.slug = slug;
    card.dataset.brand = meta.brand || "other";
    card.dataset.voltage = meta.voltage || "";
    card.dataset.capacity = String(meta.capacity || 0);
    card.dataset.batteryType = meta.batteryType || "standard";
    card.dataset.price = priceText.replace(/\D/g, "") || "0";
    card.dataset.title = title.toLocaleLowerCase("ru-RU");
    card.dataset.originalOrder = String(index);
  });

  const panel = document.createElement("div");
  panel.className = "catalog-advanced-filters";
  panel.dataset.advancedCatalogFilters = "";
  panel.innerHTML = `
    <div class="catalog-filter-field">
      <label for="catalog-brand">Бренд</label>
      <select id="catalog-brand" data-catalog-brand>
        <option value="all">Все бренды</option>
        <option value="xiaomi">Xiaomi</option>
        <option value="dreame">Dreame</option>
        <option value="dyson">Dyson</option>
        <option value="samsung">Samsung</option>
        <option value="lg">LG</option>
        <option value="roborock">Roborock</option>
        <option value="helionyx">HELIONYX LiFePO4</option>
        <option value="other">Другие</option>
      </select>
    </div>
    <div class="catalog-filter-field">
      <label for="catalog-voltage">Напряжение</label>
      <select id="catalog-voltage" data-catalog-voltage>
        <option value="all">Любое</option>
        <option value="12.8">12,8 В</option>
        <option value="14.4">14,4 В</option>
        <option value="21.6">21,6 В</option>
        <option value="25.2">25,2 В</option>
      </select>
    </div>
    <div class="catalog-filter-field">
      <label for="catalog-capacity">Ёмкость</label>
      <select id="catalog-capacity" data-catalog-capacity>
        <option value="all">Любая</option>
        <option value="under3200">До 3200 мАч</option>
        <option value="3200-4999">3200–4999 мАч</option>
        <option value="5000plus">От 5000 мАч</option>
      </select>
    </div>
    <div class="catalog-filter-field">
      <label for="catalog-battery-type">Вариант</label>
      <select id="catalog-battery-type" data-catalog-battery-type>
        <option value="all">Все варианты</option>
        <option value="standard">Штатная ёмкость</option>
        <option value="extended">Повышенная ёмкость</option>
        <option value="lifepo4">LiFePO4 100 А·ч</option>
        <option value="lifepo4-heated">LiFePO4 100 А·ч с подогревом</option>
      </select>
    </div>
    <div class="catalog-filter-field catalog-filter-field--sort">
      <label for="catalog-sort">Сортировка</label>
      <select id="catalog-sort" data-catalog-sort>
        <option value="default">По умолчанию</option>
        <option value="price-asc">Сначала дешевле</option>
        <option value="price-desc">Сначала дороже</option>
        <option value="capacity-desc">Ёмкость: по убыванию</option>
        <option value="capacity-asc">Ёмкость: по возрастанию</option>
        <option value="title-asc">По названию</option>
      </select>
    </div>
    <button class="catalog-filter-reset" type="button" data-catalog-reset>Сбросить</button>
    <p class="catalog-filter-count" data-catalog-count aria-live="polite"></p>`;
  tools.append(panel);

  const style = document.createElement("style");
  style.textContent = `
    .catalog-advanced-filters{display:grid;grid-template-columns:repeat(5,minmax(140px,1fr)) auto;gap:12px;align-items:end;width:100%;margin-top:16px;padding:18px;border:1px solid #dce5f2;border-radius:18px;background:#f7faff}
    .catalog-filter-field{display:grid;gap:6px}.catalog-filter-field label{font-size:13px;font-weight:700;color:#344054}
    .catalog-filter-field select{width:100%;min-height:44px;padding:0 36px 0 12px;border:1px solid #cfd9e8;border-radius:11px;background:#fff;color:#172033;font:inherit}
    .catalog-filter-field select:focus{outline:3px solid rgba(13,95,255,.14);border-color:#0d5fff}
    .catalog-filter-reset{min-height:44px;padding:0 16px;border:1px solid #cfd9e8;border-radius:11px;background:#fff;color:#0d5fff;font-weight:700;cursor:pointer}
    .catalog-filter-reset:hover{border-color:#0d5fff}.catalog-filter-count{grid-column:1/-1;margin:0;color:#667085;font-size:14px}
    @media(max-width:1050px){.catalog-advanced-filters{grid-template-columns:repeat(3,minmax(150px,1fr))}.catalog-filter-reset{align-self:end}}
    @media(max-width:680px){.catalog-advanced-filters{grid-template-columns:1fr 1fr;padding:14px}.catalog-filter-field--sort,.catalog-filter-reset{grid-column:1/-1}.catalog-filter-reset{width:100%}}
  `;
  document.head.append(style);

  function capacityMatches(value, range) {
    if (range === "all") return true;
    if (range === "under3200") return value < 3200;
    if (range === "3200-4999") return value >= 3200 && value < 5000;
    return value >= 5000;
  }

  function getActiveCategory() {
    return document.querySelector("[data-filter].is-active")?.dataset.filter || "all";
  }

  function applyAdvancedFilters() {
    const query = (document.querySelector("[data-product-search]")?.value || "").trim().toLocaleLowerCase("ru-RU");
    const category = getActiveCategory();
    const brand = panel.querySelector("[data-catalog-brand]").value;
    const voltage = panel.querySelector("[data-catalog-voltage]").value;
    const capacityRange = panel.querySelector("[data-catalog-capacity]").value;
    const batteryType = panel.querySelector("[data-catalog-battery-type]").value;
    const sort = panel.querySelector("[data-catalog-sort]").value;

    let visible = 0;
    cards.forEach((card) => {
      const capacity = Number(card.dataset.capacity || 0);
      const show =
        (!query || (card.dataset.search || "").includes(query)) &&
        (category === "all" || card.dataset.category === category) &&
        (brand === "all" || card.dataset.brand === brand) &&
        (voltage === "all" || card.dataset.voltage === voltage) &&
        capacityMatches(capacity, capacityRange) &&
        (batteryType === "all" || card.dataset.batteryType === batteryType);
      card.hidden = !show;
      if (show) visible += 1;
    });

    const compare = {
      "price-asc": (a, b) => Number(a.dataset.price) - Number(b.dataset.price),
      "price-desc": (a, b) => Number(b.dataset.price) - Number(a.dataset.price),
      "capacity-desc": (a, b) => Number(b.dataset.capacity) - Number(a.dataset.capacity),
      "capacity-asc": (a, b) => Number(a.dataset.capacity) - Number(b.dataset.capacity),
      "title-asc": (a, b) => a.dataset.title.localeCompare(b.dataset.title, "ru"),
      default: (a, b) => Number(a.dataset.originalOrder) - Number(b.dataset.originalOrder)
    }[sort];
    cards.slice().sort(compare).forEach((card) => grid.append(card));

    const count = panel.querySelector("[data-catalog-count]");
    if (count) count.textContent = `Найдено товаров: ${visible}`;
    const noResults = document.querySelector("[data-no-results]");
    if (noResults) noResults.classList.toggle("is-visible", visible === 0);
  }

  panel.addEventListener("change", applyAdvancedFilters);
  panel.querySelector("[data-catalog-reset]").addEventListener("click", () => {
    panel.querySelectorAll("select").forEach((select) => { select.selectedIndex = 0; });
    const search = document.querySelector("[data-product-search]");
    if (search) search.value = "";
    document.querySelectorAll("[data-filter]").forEach((button) => button.classList.toggle("is-active", button.dataset.filter === "all"));
    applyAdvancedFilters();
  });
  document.querySelector("[data-product-search]")?.addEventListener("input", applyAdvancedFilters);
  document.querySelectorAll("[data-filter]").forEach((button) => button.addEventListener("click", () => setTimeout(applyAdvancedFilters, 0)));

  applyAdvancedFilters();
})();
