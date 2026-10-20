// One shared, cacheable URL pool per language. The current page is skipped by
// index, without an N-1 copy or random retries. Repeated components share a fetch.
(() => {
  const script = document.currentScript;
  const buttons = document.querySelectorAll('[data-sidera-random]');
  if (!script || !buttons.length) return;
  // The initial HTML already reserves this disabled control's place, even before
  // deferred scripts run. Readiness changes interactivity, not layout or reveal.
  fetch(script.dataset.index)
    .then(response => {
      if (!response.ok) throw new Error('Random article index unavailable');
      return response.json();
    })
    .then(urls => {
      if (!Array.isArray(urls) || !urls.every(url => typeof url === 'string' &&
          url.startsWith('/') && new URL(url, location.href).origin === location.origin)) {
        throw new Error('Invalid random article index');
      }
      const current = urls.indexOf(script.dataset.current);
      const count = urls.length - (current >= 0 ? 1 : 0);
      if (!count) throw new Error('No other articles');
      for (const button of buttons) {
        button.addEventListener('click', () => {
          let index = Math.floor(Math.random() * count);
          if (current >= 0 && index >= current) index++;
          location.assign(urls[index]);
        });
        button.removeAttribute('aria-busy');
        button.disabled = false;
      }
    })
    .catch(() => {
      for (const button of buttons) {
        button.hidden = true;
        button.disabled = true;
        button.removeAttribute('aria-busy');
      }
    });
})();
