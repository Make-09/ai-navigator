// nav helpers: add i18n strings and small behavior
document.addEventListener("DOMContentLoaded", function () {
  // init lang selector (from lang.js)
  if (typeof initLocales === "function") {
    try { initLocales(); } catch (e) { console.error(e); }
  }

  // refresh UI strings from currentLocale if already present
  if (typeof currentLocale !== "undefined") {
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (currentLocale.strings && currentLocale.strings[key]) el.textContent = currentLocale.strings[key];
    });
  }

  // smooth scroll to anchors in same page (about/faq/policy)
  document.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', (e) => {
      // normal navigation works — but if it's a hash for same page, smooth scroll
      const href = a.getAttribute('href');
      if (href && href.indexOf('#') !== -1) {
        e.preventDefault();
        const id = href.split('#')[1];
        const el = document.getElementById(id);
        if (el) el.scrollIntoView({behavior: 'smooth', block: 'center'});
        else window.location.href = href; // fallback
      }
    });
  });
});
