/**
 * PPK Instagram home adapter — mount only on the existing Instagram grid.
 *
 * Include AFTER the public, weekly-generated ppk-instagram-weekly.js:
 *   <script defer src="https://newcfo.github.io/ppk-instagram-feed/ppk-instagram-weekly.js"></script>
 *   <script defer src="https://newcfo.github.io/ppk-instagram-feed/ppk-instagram-home-adapter.js"></script>
 *
 * Add data-ppk-instagram-grid to the existing card GRID element, not the
 * whole section. This script updates existing anchors/images only.
 *
 * On validation error, all six existing static cards stay untouched.
 */
(function () {
  "use strict";
  function validInstagram(value) {
    try {
      var url = new URL(value);
      return (
        url.protocol === "https:" &&
        (url.hostname === "www.instagram.com" || url.hostname === "instagram.com") &&
        /^\/(p|reel|tv)\/[^/]+\/?/.test(url.pathname)
      );
    } catch (e) {
      return false;
    }
  }
  function validBeholdImage(value) {
    try {
      var url = new URL(value);
      return (
        url.protocol === "https:" &&
        ["behold.pictures", "cdn.behold.pictures", "cdn2.behold.pictures", "cdn2-dev.behold.pictures"].indexOf(url.hostname) !== -1
      );
    } catch (e) {
      return false;
    }
  }
  function applySnapshot() {
    var grid = document.querySelector("[data-ppk-instagram-grid]");
    var feed = window.PPK_INSTAGRAM_WEEKLY;
    if (!grid || !feed || !Array.isArray(feed.posts) || feed.posts.length !== 6) return;
    var cards = Array.prototype.slice.call(grid.querySelectorAll("a")).filter(function (a) {
      return a.querySelector("img") && validInstagram(a.href);
    });
    if (cards.length !== 6) return;
    var posts = feed.posts.map(function (p) {
      return {
        link: p && p.url,
        image: p && p.image,
        alt: String((p && p.alt) || "퍼펙트포션 인스타그램 게시물").slice(0, 160)
      };
    });
    // Validate all six before mutating any element.
    if (!posts.every(function (p) {
      return validInstagram(p.link) && validBeholdImage(p.image);
    })) return;
    posts.forEach(function (p, i) {
      var card = cards[i];
      var img = card.querySelector("img");
      card.href = p.link;
      card.target = "_blank";
      card.rel = "noopener noreferrer";
      card.setAttribute("aria-label", p.alt + " (새 탭에서 열기)");
      img.src = p.image;
      img.alt = p.alt;
      img.decoding = "async";
      img.loading = "lazy";
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applySnapshot, { once: true });
  } else {
    applySnapshot();
  }
})();
