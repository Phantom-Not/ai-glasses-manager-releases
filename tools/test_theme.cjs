/* Behavior fixtures for appearance when storage or system settings change. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../docs/assets/theme.js'), 'utf8');

function fixture({ saved = null, dark = false, blocked = false, loading = false } = {}) {
  const stored = new Map(saved === null ? [] : [['ai-glasses-manager:appearance', saved]]);
  const docEvents = {}, winEvents = {}, menuEvents = {};
  const root = { dataset: {} }, meta = {};
  let focused = false;
  const summary = { focus() { focused = true; } };
  const buttons = ['system', 'light', 'dark'].map(choice => ({
    dataset: { themeChoice: choice }, attrs: {},
    setAttribute(name, value) { this.attrs[name] = value; },
    closest() { return this; }
  }));
  const menu = {
    hidden: true, open: false,
    contains(target) { return buttons.includes(target) || target === summary; },
    querySelector() { return summary; },
    addEventListener(name, fn) { menuEvents[name] = fn; }
  };
  const media = { matches: dark, addEventListener(name, fn) { this.changed = fn; } };
  const document = {
    documentElement: root, readyState: loading ? 'loading' : 'complete',
    querySelector(selector) { return selector.includes('meta') ? meta : menu; },
    querySelectorAll(selector) { return selector === '[data-theme-choice]' ? buttons : selector.includes('meta') ? [meta] : []; },
    addEventListener(name, fn) { docEvents[name] = fn; }
  };
  const localStorage = {
    getItem(key) { if (blocked) throw Error('denied'); return stored.get(key) ?? null; },
    setItem(key, value) { if (blocked) throw Error('denied'); stored.set(key, value); },
    removeItem(key) { if (blocked) throw Error('denied'); stored.delete(key); }
  };
  vm.runInNewContext(source, { document, localStorage, window: {
    matchMedia() { return media; }, addEventListener(name, fn) { winEvents[name] = fn; }
  } });
  return { root, stored, media, meta, buttons, menu, docEvents, winEvents,
    choose(choice) { menuEvents.click({ target: buttons.find(b => b.dataset.themeChoice === choice) }); },
    changed(dark) { media.matches = dark; media.changed(); },
    focused: () => focused, menuEvents
  };
}
let f = fixture({ loading: true, dark: true });
assert.equal(f.root.dataset.theme, 'dark', 'system applied before DOM ready');
assert.equal(f.menu.hidden, true);
f.docEvents.DOMContentLoaded();
assert.equal(f.menu.hidden, false);
assert.equal(f.buttons[0].attrs['aria-pressed'], 'true');
f.changed(false); assert.equal(f.root.dataset.theme, 'light');
f.choose('dark'); assert.equal(f.root.dataset.theme, 'dark');
assert.equal(f.stored.get('ai-glasses-manager:appearance'), 'dark');
assert.equal(f.focused(), true);
f.changed(false); assert.equal(f.root.dataset.theme, 'dark', 'explicit choice overrides OS');
f.choose('system'); assert.equal(f.root.dataset.theme, 'light');
assert.equal(f.stored.size, 0);
f.changed(true); assert.equal(f.root.dataset.theme, 'dark');
f.winEvents.storage({ key: 'unrelated', newValue: 'light' });
assert.equal(f.root.dataset.theme, 'dark');
f.winEvents.storage({ key: 'ai-glasses-manager:appearance', newValue: 'light' });
assert.equal(f.root.dataset.theme, 'light');
f.winEvents.storage({ key: null, newValue: null });
assert.equal(f.root.dataset.theme, 'dark', 'cleared storage returns to system');
f = fixture({ saved: 'invalid' }); assert.equal(f.root.dataset.colorPreference, 'system');
f = fixture({ saved: 'light', dark: true }); assert.equal(f.root.dataset.theme, 'light');
f = fixture({ blocked: true, dark: true });
assert.equal(f.root.dataset.theme, 'dark');
f.choose('light'); assert.equal(f.root.dataset.theme, 'light', 'storage denied still allows page choice');
f.menu.open = true; f.docEvents.click({ target: {} }); assert.equal(f.menu.open, false);
f.menu.open = true; f.menuEvents.keydown({ key: 'Escape' }); assert.equal(f.menu.open, false);
assert.equal(f.meta.content, '#f7f8f5');
console.log('PASS theme: pre-paint, system changes, manual preference, invalid/blocked storage, cross-tab changes, menu closing and focus.');
