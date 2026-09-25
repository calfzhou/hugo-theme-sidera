// Apply before styles/body paint. Owner default -> valid saved visitor preference.
(() => {
  const key = 'sidera-appearance';
  const modes = ['dark', 'light', 'auto'];
  const root = document.documentElement;
  const system = matchMedia('(prefers-color-scheme: light)');
  const fallback = modes.includes(root.dataset.appearanceDefault) ? root.dataset.appearanceDefault : 'auto';
  let choice = fallback;
  try {
    const stored = localStorage.getItem(key);
    if (stored === 'system') {
      // Migrate the former stored spelling once; public config/API accepts only auto.
      choice = 'auto';
      localStorage.setItem(key, choice);
    } else if (modes.includes(stored)) choice = stored;
  } catch { /* Denied storage still permits a choice for this page. */ }
  function apply() {
    root.dataset.appearanceMode = choice;
    root.dataset.appearance = choice === 'auto' ? (system.matches ? 'light' : 'dark') : choice;
    for (const button of document.querySelectorAll('[data-appearance-cycle]')) {
      const label = button.dataset[`label${choice[0].toUpperCase()}${choice.slice(1)}`];
      button.setAttribute('aria-label', label);
      button.title = label;
    }
  }
  function setAppearance(mode) {
    if (!modes.includes(mode)) throw new TypeError('Sidera appearance must be dark, light or auto');
    choice = mode;
    apply();
    try { localStorage.setItem(key, choice); } catch { /* Page-local preference. */ }
    return choice;
  }
  window.Sidera = Object.assign(window.Sidera || {}, {
    setAppearance,
    cycleAppearance: () => {
      const mode = setAppearance(modes[(modes.indexOf(choice) + 1) % modes.length]);
      const notice = document.getElementById('sidera-toast');
      const message = notice?.dataset[`mode${mode[0].toUpperCase()}${mode.slice(1)}`];
      if (message && window.Sidera.toast) window.Sidera.toast(message);
      return mode;
    }
  });
  apply();
  system.addEventListener('change', () => { if (choice === 'auto') apply(); });
  addEventListener('storage', event => {
    if (event.key === key || event.key === null) {
      choice = modes.includes(event.newValue) ? event.newValue : fallback;
      apply();
    }
  });
  document.addEventListener('DOMContentLoaded', () => {
    for (const button of document.querySelectorAll('[data-appearance-cycle]')) {
      button.addEventListener('click', window.Sidera.cycleAppearance);
      button.hidden = false;
    }
    apply();
  });
})();
