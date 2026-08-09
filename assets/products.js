window.HELIONYX_PRODUCTS = [{"slug": "dyson-v7", "title": "Аккумулятор для Dyson V7 / SV11", "short": "Dyson V7 / SV11", "price": 3190, "image": "assets/products/dyson-v7/01.webp"}, {"slug": "dyson-v6", "title": "Аккумулятор для Dyson V6", "short": "Dyson V6", "price": 3090, "image": "assets/products/dyson-v6/01.webp"}, {"slug": "dyson-v11", "title": "Аккумулятор для Dyson V11", "short": "Dyson V11", "price": 4990, "image": "assets/products/dyson-v11/01.webp"}, {"slug": "dreame-5200", "title": "Аккумулятор для Dreame D9 / F9, 5200 мАч", "short": "Dreame D9 / F9 — 5200", "price": 2590, "image": "assets/products/dreame-5200/01.webp"}, {"slug": "samsung-jet90", "title": "Аккумулятор VCA-SBT90 для Samsung Jet 75 / 90", "short": "Samsung Jet 75 / 90", "price": 4790, "image": "assets/products/samsung-jet90/01.webp"}, {"slug": "exvac-3200", "title": "Аккумулятор INR18650 M26-4S1P, 3200 мАч", "short": "Mamibot / Polaris / Ecovacs", "price": 2090, "image": "assets/products/exvac-3200/01.webp"}, {"slug": "mop2-lite", "title": "Аккумулятор для Xiaomi Vacuum-Mop 2 Lite", "short": "Xiaomi Mop 2 Lite", "price": 2090, "image": "assets/products/mop2-lite/01.webp"}, {"slug": "mop2-3200", "title": "Аккумулятор для Xiaomi Vacuum-Mop 2", "short": "Xiaomi Vacuum-Mop 2", "price": 1990, "image": "assets/products/mop2-3200/01.webp"}, {"slug": "xiaomi-g1", "title": "Аккумулятор для Xiaomi Vacuum-Mop Essential G1", "short": "Xiaomi Essential G1", "price": 2090, "image": "assets/products/xiaomi-g1/01.webp"}, {"slug": "samsung-jet60", "title": "Аккумулятор для Samsung Jet 60", "short": "Samsung Jet 60", "price": 4490, "image": "assets/products/samsung-jet60/01.webp"}, {"slug": "lg-a9", "title": "Аккумулятор для LG CordZero A9", "short": "LG CordZero A9", "price": 3390, "image": "assets/products/lg-a9/01.webp"}, {"slug": "samsung-jet70", "title": "Аккумулятор VCA-SBT90E для Samsung Jet 70 / 90E", "short": "Samsung Jet 70 / 90E", "price": 4490, "image": "assets/products/samsung-jet70/01.webp"}, {"slug": "dreame-6400", "title": "Аккумулятор для Dreame D9 / F9, 6400 мАч", "short": "Dreame D9 / F9 — 6400", "price": 2890, "image": "assets/products/dreame-6400/01.webp"}, {"slug": "xiaomi-1c-5200", "title": "Аккумулятор для Xiaomi Vacuum-Mop 1C, 5200 мАч", "short": "Xiaomi Vacuum-Mop 1C — 5200", "price": 2790, "image": "assets/products/xiaomi-1c-5200/01.webp"}, {"slug": "roborock-6400", "title": "Аккумулятор для Roborock S5 / S6 / S7, 6400 мАч", "short": "Roborock S5 / S6 / S7", "price": 2990, "image": "assets/products/roborock-6400/01.webp"}, {"slug": "xiaomi-mopp-3200", "title": "Аккумулятор для Xiaomi Vacuum-Mop P / 2S / S10 / S12", "short": "Xiaomi Mop P / 2S / S10", "price": 2290, "image": "assets/products/xiaomi-mopp-3200/01.webp"}, {"slug": "xiaomi-1c-6400", "title": "Аккумулятор для Xiaomi Vacuum-Mop 1C, 6400 мАч", "short": "Xiaomi Vacuum-Mop 1C — 6400", "price": 2990, "image": "assets/products/xiaomi-1c-6400/01.webp"}];

(function () {
  function addXiaomi1cGuideLink() {
    var path = window.location.pathname;
    if (path !== "/products/xiaomi-1c-5200/" && path !== "/products/xiaomi-1c-6400/") return;
    if (document.querySelector("[data-xiaomi-1c-guide]")) return;
    var sections = document.querySelectorAll("main .section");
    var anchor = sections.length ? sections[sections.length - 1] : null;
    var section = document.createElement("section");
    section.className = "section";
    section.setAttribute("data-xiaomi-1c-guide", "");
    section.innerHTML = '<div class="container product-details"><div><span class="eyebrow">Полезная инструкция</span><h2>Как заменить аккумулятор Xiaomi Vacuum-Mop 1C</h2></div><div><p>Подробно разобрали симптомы износа, маркировки STYTJ01ZHM и P1904-4S1P-MM, порядок замены и выбор между 5200 и 6500 мАч.</p><a class="button button--outline" href="../../articles/zamena-akkumulyatora-xiaomi-vacuum-mop-1c/">Открыть инструкцию по замене</a></div></div>';
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(section, anchor);
    else document.querySelector("main")?.appendChild(section);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", addXiaomi1cGuideLink);
  else addXiaomi1cGuideLink();
})();

(function () {
  if (document.querySelector('script[data-helionyx-quick-search]')) return;
  var script = document.createElement("script");
  script.src = "/assets/quick-search.js";
  script.defer = true;
  script.setAttribute("data-helionyx-quick-search", "");
  document.head.appendChild(script);
})();

(function () {
  if (document.querySelector('script[data-helionyx-consent]')) return;
  var script = document.createElement("script");
  script.src = "/assets/consent.js";
  script.defer = true;
  script.setAttribute("data-helionyx-consent", "");
  document.head.appendChild(script);
})();

(function () {
  if (window.location.pathname !== "/catalog/" || document.querySelector('script[data-helionyx-catalog-filters]')) return;
  var script = document.createElement("script");
  script.src = "/assets/catalog-filters.js";
  script.defer = true;
  script.setAttribute("data-helionyx-catalog-filters", "");
  document.head.appendChild(script);
})();

(function () {
  if (document.querySelector('script[data-helionyx-card-enhancements]')) return;
  var script = document.createElement("script");
  script.src = "/assets/card-enhancements.js";
  script.defer = true;
  script.setAttribute("data-helionyx-card-enhancements", "");
  document.head.appendChild(script);
})();

(function () {
  if (document.querySelector('script[data-helionyx-checkout-routing]')) return;
  var script = document.createElement("script");
  script.src = "/assets/checkout-routing.js";
  script.defer = true;
  script.setAttribute("data-helionyx-checkout-routing", "");
  document.head.appendChild(script);
})();

(function () {
  var path = window.location.pathname;
  if (path !== "/products/xiaomi-1c-5200/" && path !== "/products/xiaomi-1c-6400/") return;
  if (document.querySelector('script[data-xiaomi-1c-compatibility]')) return;
  var script = document.createElement("script");
  script.src = "/assets/xiaomi-1c-compatibility.js";
  script.defer = true;
  script.setAttribute("data-xiaomi-1c-compatibility", "");
  document.head.appendChild(script);
})();

(function () {
  function addReturnsFooterLink() {
    if (document.querySelector('a[data-helionyx-returns-link]')) return;
    var headings = document.querySelectorAll('.site-footer h3');
    for (var i = 0; i < headings.length; i += 1) {
      if (headings[i].textContent.trim() !== 'Покупателям') continue;
      var column = headings[i].parentElement;
      if (!column) return;
      var link = document.createElement('a');
      link.href = '/returns/';
      link.textContent = 'Возврат и обмен';
      link.setAttribute('data-helionyx-returns-link', '');
      var privacy = Array.from(column.querySelectorAll('a')).find(function (item) {
        return item.getAttribute('href') && item.getAttribute('href').indexOf('privacy') !== -1;
      });
      if (privacy) column.insertBefore(link, privacy);
      else column.appendChild(link);
      return;
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addReturnsFooterLink);
  else addReturnsFooterLink();
})();
