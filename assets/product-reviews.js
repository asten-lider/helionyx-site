(function () {
  "use strict";

  var PRODUCT_PATH = "/products/xiaomi-1c-6400/";
  if (window.location.pathname !== PRODUCT_PATH) return;

  var OZON_URL = "https://www.ozon.ru/product/akkumulyator-dlya-robota-pylesosa-xiaomi-mi-robot-vacuum-mop-1c-stytj01zhm-p1904-4s1p-mm-6500-mach-1310508272/";
  var reviews = [
    {
      author: "Мария Ф.",
      date: "2026-06-05",
      dateLabel: "5 июня 2026",
      text: "Отличный аккумулятор🔥🔥🔥, пылесос работает лучше, чем с заводским аккумулятором, аккумулятор был заряжен на 81%!!! пылесос на 81% заряда убрал 70м2, нашёл и встал на базу для зарядки !!! Очень довольна покупкой!!!"
    },
    {
      author: "Андрей Л.",
      date: "2025-10-14",
      dateLabel: "14 октября 2025",
      text: "Пришёл в срок обозначенным в заказе по весу раза в 3 тяжелее родного, проверил по напряжению 15,6в. Поставил в пылесос приложение показывает 83%. Всё работает будем тестить. Продавца рекомендую."
    },
    {
      author: "Юрий Н.",
      date: "2025-11-01",
      dateLabel: "1 ноября 2025",
      text: "Родная батарея 2600mAh, на этой указано 6500mAh, не знаю на сколько это правда, замеров я не делал, но провода на новом АКБ чуть толще и вес тоже потяжелее. заряда было 75% , отправил на уборку, в режиме \"стандарт\" уходит 1% заряда в минуты полторы - две, получается приблизительно 100% хватит где-то на 2,5 -3 часа, может и больше. В общем батарея хорошая..."
    },
    {
      author: "Андрей К.",
      date: "2025-09-21",
      dateLabel: "21 сентября 2025",
      text: "Пока впечатления только положительные. Фото старой и новой аккумуляторных батарей. Старая батарея за 4 года уже не обеспечивала уборку 63 м кв. за 1 уборку. Батарея была заряжена на 70%. Пока робот-пылесос стоит на зарядке. По скорости зарядки видно, что объём гораздо больше, чем у старой батареи. Проверим в эксплуатации."
    },
    {
      author: "Анна К.",
      date: "2026-05-12",
      dateLabel: "12 мая 2026",
      text: "Это даже лучше,чем заказывать на китайском маркетплейсе.Пришел товар быстро.Да,дороже,но зато можно нормально отзывы почитать и быть уверенным.подошел на пылесос отлично,работает уже два месяца,сразу чувствуется разница,когда поменяли батарею.заряда хватает на опробованные 2 уборки,больше за раз не запускали.По мощностям я не шарю,работает и хорошо"
    }
  ];

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function loadStyles() {
    if (document.querySelector('link[data-helionyx-product-reviews]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/assets/product-reviews.css";
    link.setAttribute("data-helionyx-product-reviews", "");
    document.head.appendChild(link);
  }

  function addProductRatingLink() {
    var info = document.querySelector(".product-info");
    var lead = info && info.querySelector(".product-lead");
    if (!info || !lead || info.querySelector("[data-product-review-summary]")) return;

    var summary = document.createElement("a");
    summary.className = "product-review-summary";
    summary.href = "#reviews";
    summary.setAttribute("data-product-review-summary", "");
    summary.setAttribute("aria-label", "Перейти к отзывам покупателей");
    summary.innerHTML = '<span class="product-review-summary__stars" aria-hidden="true">★★★★★</span><span><strong>5 выбранных отзывов с Ozon</strong><small>Карточка товара на Ozon: 2342 отзыва</small></span>';
    lead.insertAdjacentElement("afterend", summary);
  }

  function renderReviews() {
    if (document.querySelector("[data-product-reviews]")) return;
    var main = document.querySelector("main");
    if (!main) return;

    var cards = reviews.map(function (review) {
      return '<article class="product-review-card" itemprop="review" itemscope itemtype="https://schema.org/Review">' +
        '<div class="product-review-card__top">' +
          '<div><strong itemprop="author">' + escapeHtml(review.author) + '</strong><span>Покупатель на Ozon · 6500 мА·ч</span></div>' +
          '<div class="product-review-card__rating" aria-label="Оценка 5 из 5" itemprop="reviewRating" itemscope itemtype="https://schema.org/Rating"><span aria-hidden="true">★★★★★</span><meta itemprop="ratingValue" content="5"><meta itemprop="bestRating" content="5"></div>' +
        '</div>' +
        '<p itemprop="reviewBody">' + escapeHtml(review.text) + '</p>' +
        '<time datetime="' + escapeHtml(review.date) + '" itemprop="datePublished">' + escapeHtml(review.dateLabel) + '</time>' +
      '</article>';
    }).join("");

    var section = document.createElement("section");
    section.className = "section product-reviews-section";
    section.id = "reviews";
    section.setAttribute("data-product-reviews", "");
    section.innerHTML = '<div class="container">' +
      '<div class="product-reviews-heading">' +
        '<div><span class="eyebrow">Проверено покупателями</span><h2>Отзывы об аккумуляторе Xiaomi Vacuum-Mop 1C</h2><p>Ниже опубликованы точные цитаты из отзывов покупателей версии 6500 мА·ч на Ozon. Орфография и пунктуация авторов сохранены. Эти отзывы оставлены на Ozon, а не на helionyx.pro.</p></div>' +
        '<div class="product-reviews-score"><span aria-hidden="true">★★★★★</span><strong>5 выбранных отзывов</strong><small>Карточка товара на Ozon: 2342 отзыва<br>Проверено 5 августа 2026 года</small></div>' +
      '</div>' +
      '<div class="product-reviews-grid">' + cards + '</div>' +
      '<div class="product-reviews-footer"><p>Источник: отзывы покупателей в карточке товара R&amp;K Store на Ozon.</p><a class="button button--outline" href="' + OZON_URL + '" target="_blank" rel="noopener noreferrer nofollow">Посмотреть все отзывы на Ozon</a></div>' +
    '</div>';

    var sections = Array.prototype.slice.call(main.querySelectorAll(":scope > section"));
    var similar = sections.find(function (candidate) {
      var heading = candidate.querySelector("h2");
      return heading && heading.textContent.trim() === "Похожие аккумуляторы";
    });

    if (similar) main.insertBefore(section, similar);
    else main.appendChild(section);
  }

  function addStructuredReviews() {
    var scripts = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < scripts.length; i += 1) {
      try {
        var data = JSON.parse(scripts[i].textContent);
        if (data && data["@type"] === "Product" && data.sku === "BAT1C6500") {
          data.review = reviews.map(function (review) {
            return {
              "@type": "Review",
              author: {"@type": "Person", name: review.author},
              datePublished: review.date,
              reviewBody: review.text,
              reviewRating: {"@type": "Rating", ratingValue: 5, bestRating: 5, worstRating: 1}
            };
          });
          scripts[i].textContent = JSON.stringify(data);
          break;
        }
      } catch (error) {
        // Ignore unrelated or invalid JSON-LD blocks.
      }
    }
  }

  function init() {
    loadStyles();
    addProductRatingLink();
    renderReviews();
    addStructuredReviews();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, {once: true});
  } else {
    init();
  }
})();
