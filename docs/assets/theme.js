/* Apply the initial appearance before the stylesheet paints. No network requests. */
(() => {
  'use strict';
  const root = document.documentElement;
  const key = 'ai-glasses-manager:appearance';
  const valid = value => ['system', 'light', 'dark'].includes(value);
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'system';
  try {
    const saved = localStorage.getItem(key);
    if (valid(saved)) preference = saved;
  } catch (_) { /* The system setting still works when storage is unavailable. */ }

  function apply() {
    const theme = preference === 'system' ? (media.matches ? 'dark' : 'light') : preference;
    root.dataset.theme = theme;
    root.dataset.colorPreference = preference;
    document.querySelectorAll('meta[name="theme-color"]').forEach(color => {
      color.content = theme === 'dark' ? '#0c1820' : '#f7f8f5';
    });
    document.querySelectorAll('[data-theme-choice]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.themeChoice === preference));
    });
  }
  apply();
  const onSystemChange = () => { if (preference === 'system') apply(); };
  if (media.addEventListener) media.addEventListener('change', onSystemChange);
  else media.addListener(onSystemChange);
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    preference = valid(event.newValue) ? event.newValue : 'system';
    apply();
  });

  function ready() {
    const menu = document.querySelector('.theme-menu');
    if (!menu) return;
    menu.addEventListener('toggle', () => {
      if (menu.open) document.querySelectorAll('.language-menu[open],.mobile-menu[open]').forEach(other => { other.open = false; });
    });
    menu.hidden = false;
    apply();
    menu.addEventListener('click', event => {
      const button = event.target.closest('[data-theme-choice]');
      if (!button || !menu.contains(button)) return;
      preference = button.dataset.themeChoice;
      try {
        if (preference === 'system') localStorage.removeItem(key);
        else localStorage.setItem(key, preference);
      } catch (_) { /* Keep the selected appearance for this page. */ }
      apply();
      menu.open = false;
      menu.querySelector('summary').focus();
    });
    document.addEventListener('click', event => {
      if (!menu.contains(event.target)) menu.open = false;
    });
    menu.addEventListener('keydown', event => {
      if (event.key !== 'Escape') return;
      menu.open = false;
      menu.querySelector('summary').focus();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready, { once: true });
  else ready();
})();
