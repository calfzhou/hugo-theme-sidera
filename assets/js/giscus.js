// One explicit activation per document. The provider owns authentication and its DOM.
(() => {
  const host = document.querySelector('[data-sidera-giscus]');
  if (!host || host.dataset.initialized) return;
  host.dataset.initialized = 'true';
  const origin = 'https://giscus.app';
  const button = host.querySelector('button');
  const status = host.querySelector('[role="status"]');
  const container = host.querySelector('.giscus');
  let frame, timer, started = false, failed = false, lastTheme;
  const theme = () => document.documentElement.dataset.colorScheme === 'light' ? 'light' : 'dark';
  const state = (name, text) => { host.dataset.state = name; status.textContent = text; };
  const unavailable = () => { failed = true; clearTimeout(timer); state('unavailable', host.dataset.unavailable); };
  const updateTheme = () => {
    if (!frame || lastTheme === theme()) return;
    lastTheme = theme();
    frame.contentWindow.postMessage({giscus: {setConfig: {theme: lastTheme}}}, origin);
  };
  const palette = new MutationObserver(updateTheme);
  const inserted = new MutationObserver(() => {
    const candidate = container.querySelector('iframe.giscus-frame');
    if (!candidate || candidate === frame) return;
    // Never trust an unrelated frame supplied by an override/extension.
    if (new URL(candidate.src, location.href).origin !== origin) return;
    frame = candidate;
    frame.title = document.getElementById('comments-heading').textContent;
    frame.referrerPolicy = 'no-referrer';
    frame.addEventListener('load', () => { lastTheme = undefined; updateTheme(); });
    updateTheme();
  });
  const onMessage = event => {
    if (event.origin !== origin || !frame || event.source !== frame.contentWindow) return;
    const data = event.data?.giscus;
    if (!data || typeof data !== 'object') return;
    if (typeof data.error === 'string') {
      if (data.error.includes('Discussion not found')) {
        clearTimeout(timer); failed = false; state('empty', host.dataset.empty);
      } else unavailable();
    } else if (Number.isFinite(data.resizeHeight) && data.resizeHeight > 0) {
      // This proves widget communication, NOT a successful GitHub discussion fetch.
      clearTimeout(timer);
      if (!failed && host.dataset.state !== 'empty') state('opened', host.dataset.opened);
    }
  };
  button.hidden = false;
  state('idle', '');
  button.addEventListener('click', () => {
    if (started) return;
    started = true; button.hidden = true;
    state('loading', host.dataset.loading);
    inserted.observe(container, {childList: true});
    palette.observe(document.documentElement, {attributes: true, attributeFilter: ['data-color-scheme']});
    addEventListener('message', onMessage);
    timer = setTimeout(unavailable, 15000);
    const backlink = document.querySelector('meta[name="giscus:backlink"]') || document.createElement('meta');
    backlink.name = 'giscus:backlink'; backlink.content = host.dataset.backlink;
    if (!backlink.isConnected) document.head.append(backlink);
    const script = document.createElement('script');
    script.src = origin + '/client.js'; script.async = true;
    script.crossOrigin = 'anonymous'; script.referrerPolicy = 'no-referrer';
    for (const key of ['repo', 'repoId', 'category', 'categoryId', 'term', 'lang', 'strict', 'inputPosition']) script.dataset[key] = host.dataset[key];
    Object.assign(script.dataset, {mapping: 'specific', theme: theme(), reactionsEnabled: host.dataset.reactions, emitMetadata: '0'});
    script.addEventListener('error', unavailable, {once: true});
    host.append(script);
  });
  // BFCache retains this bounded instance; ordinary navigation discards the document.
  addEventListener('pagehide', event => {
    if (event.persisted) return;
    clearTimeout(timer); inserted.disconnect(); palette.disconnect(); removeEventListener('message', onMessage);
  });
})();
