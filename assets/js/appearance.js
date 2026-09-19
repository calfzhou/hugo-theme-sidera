// Run in the head before styles/body paint. Dark is the default, not system.
(() => {
  const key = 'sidera-appearance';
  const modes = ['dark', 'light', 'system'];
  const system = window.matchMedia('(prefers-color-scheme: light)');
  let choice = 'dark';
  try {
    const stored = localStorage.getItem(key);
    if (modes.includes(stored)) choice = stored;
  } catch { /* Storage may be denied; the choice still works for this page. */ }
  function apply() {
    document.documentElement.dataset.appearance = choice === 'system'
      ? (system.matches ? 'light' : 'dark') : choice;
  }
  apply();
  system.addEventListener('change', () => { if (choice === 'system') apply(); });
  document.addEventListener('DOMContentLoaded', () => {
    const select = document.querySelector('#appearance');
    select.value = choice;
    select.addEventListener('change', () => {
      choice = select.value;
      apply();
      try { localStorage.setItem(key, choice); } catch { /* Session-only choice. */ }
    });
    select.closest('[hidden]').hidden = false;
  });
})();
