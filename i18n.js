/**
 * ADEstock i18n Engine
 * Supports: es (default), en, pt
 * Detection: localStorage → navigator.language → 'es'
 */

(function () {
  'use strict';

  var SUPPORTED = ['es', 'en', 'pt'];
  var DEFAULT_LANG = 'es';
  var STORAGE_KEY = 'adestock_lang';

  /* ─── 1. Detect language ────────────────────────────── */
  function detectLang() {
    // 1a. User preference saved in localStorage
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;

    // 1b. Browser language
    var nav = (navigator.language || navigator.userLanguage || '').toLowerCase();
    if (nav.startsWith('pt')) return 'pt';
    if (nav.startsWith('en')) return 'en';
    if (nav.startsWith('es')) return 'es';

    return DEFAULT_LANG;
  }

  /* ─── 2. Get translation dict ───────────────────────── */
  function getDict(lang) {
    if (lang === 'en' && window.i18n_en) return window.i18n_en;
    if (lang === 'pt' && window.i18n_pt) return window.i18n_pt;
    return window.i18n_es || {};
  }

  /* ─── 3. Apply translations to DOM ─────────────────── */
  function applyTranslations(lang) {
    var dict = getDict(lang);

    // Text content
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (dict[key] !== undefined) el.textContent = dict[key];
    });

    // HTML content (elements with links / bold tags inside)
    document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-html');
      if (dict[key] !== undefined) el.innerHTML = dict[key];
    });

    // title attribute
    document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-title');
      if (dict[key] !== undefined) el.setAttribute('title', dict[key]);
    });

    // aria-label attribute
    document.querySelectorAll('[data-i18n-aria]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-aria');
      if (dict[key] !== undefined) el.setAttribute('aria-label', dict[key]);
    });

    // placeholder attribute
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-placeholder');
      if (dict[key] !== undefined) el.setAttribute('placeholder', dict[key]);
    });

    // <html lang="">
    document.documentElement.setAttribute('lang', lang);

    // <title>
    var titleKey = document.body.getAttribute('data-page-title');
    if (titleKey && dict[titleKey]) document.title = dict[titleKey];

    // <meta name="description">
    var metaDescKey = document.body.getAttribute('data-page-desc');
    if (metaDescKey && dict[metaDescKey]) {
      var metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) metaDesc.setAttribute('content', dict[metaDescKey]);
    }

    // Update active state on switcher buttons
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.classList.toggle('lang-btn--active', btn.getAttribute('data-lang') === lang);
    });

    // Notify dynamic sections that language changed
    document.dispatchEvent(new CustomEvent('adestock:langchange', { detail: { lang: lang } }));
  }

  /* ─── 4. Set language (public API) ─────────────────── */
  function setLang(lang) {
    if (SUPPORTED.indexOf(lang) === -1) lang = DEFAULT_LANG;
    localStorage.setItem(STORAGE_KEY, lang);
    applyTranslations(lang);
  }

  /* ─── 5. Inject language switcher into every navbar ── */
  function injectSwitcher() {
    var navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;

    // Avoid double injection
    if (document.querySelector('.lang-switcher')) return;

    var current = detectLang();
    var switcher = document.createElement('li');
    switcher.className = 'lang-switcher';
    switcher.innerHTML =
      '<button class="lang-btn' + (current === 'es' ? ' lang-btn--active' : '') + '" data-lang="es" aria-label="Español">ES</button>' +
      '<button class="lang-btn' + (current === 'en' ? ' lang-btn--active' : '') + '" data-lang="en" aria-label="English">EN</button>' +
      '<button class="lang-btn' + (current === 'pt' ? ' lang-btn--active' : '') + '" data-lang="pt" aria-label="Português">PT</button>';

    navLinks.appendChild(switcher);

    switcher.addEventListener('click', function (e) {
      var btn = e.target.closest('.lang-btn');
      if (btn) setLang(btn.getAttribute('data-lang'));
    });
  }

  /* ─── 6. Boot ───────────────────────────────────────── */
  function boot() {
    injectSwitcher();
    applyTranslations(detectLang());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  // Expose public API
  window.ADEi18n = { setLang: setLang, detectLang: detectLang };
})();
