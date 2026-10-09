// One live opaque frame per visible chart. No author options enter the host DOM
// as HTML or executable JS; both authoring paths produce the same escaped JSON.
(() => {
  const script = document.querySelector('[data-sidera-charts-script]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const records = [];
  let serial = 0;
  for (const figure of document.querySelectorAll('[data-sidera-chart]')) {
    const view = figure.querySelector('.chart-view');
    const canvas = figure.querySelector('.chart-canvas');
    const status = figure.querySelector('.chart-status');
    const details = figure.querySelector('.chart-source');
    const source = figure.querySelector('.chart-source code').textContent;
    const sourceButton = figure.querySelector('[data-chart-action="source"]');
    const summary = details.querySelector('summary');
    let id;
    do { id = 'chart-source-' + (++serial); } while (document.getElementById(id));
    details.id = id;
    sourceButton.setAttribute('aria-controls', id);
    sourceButton.hidden = false; summary.hidden = true;
    details.dataset.enhanced = '';
    sourceButton.addEventListener('click', () => {
      details.open = !details.open;
      sourceButton.setAttribute('aria-expanded', String(details.open));
    });
    details.addEventListener('toggle', () => sourceButton.setAttribute('aria-expanded', String(details.open)));
    // Reserve the plot before lazy initialization and collapse the no-JS fallback
    // once. Later readiness must not undo a reader's source disclosure choice.
    view.hidden = false;
    if (!details.contains(document.activeElement)) details.open = false;
    let frame, timer, receive, visible = false, started = false, ready = false, palette;
    const update = state => {
      figure.dataset.state = state;
      status.textContent = status.dataset[state];
      status.classList.toggle('visually-hidden', state === 'ready');
    };
    const fail = () => {
      clearTimeout(timer); ready = false;
      if (receive) removeEventListener('message', receive);
      frame?.remove(); view.hidden = true; canvas.classList.remove('chart-hover');
      sourceButton.hidden = true; summary.hidden = false;
      details.open = true; update('error');
    };
    const send = message => frame?.contentWindow?.postMessage(message, '*');
    const environment = () => ({
      palette: figure.closest('.invert-when-dark,.invert-when-light') ? 'light' :
        document.documentElement.dataset.colorScheme === 'dark' ? 'dark' : 'light',
      reduced: reduced.matches
    });
    const refresh = () => {
      if (!ready) return;
      const next = environment();
      const key = JSON.stringify(next);
      if (palette !== key) { palette = key; send({type: 'chart-environment', ...next}); }
    };
    const start = () => {
      if (started || !figure.getBoundingClientRect().width || !figure.getClientRects().length) return;
      started = true; update('loading');
      frame = document.createElement('iframe');
      frame.className = 'chart-frame'; frame.sandbox = 'allow-scripts';
      frame.title = figure.dataset.chartLabel;
      frame.referrerPolicy = 'no-referrer';
      receive = event => {
        if (event.source !== frame.contentWindow || event.origin !== 'null') return;
        const message = event.data;
        if (message?.type === 'chart-frame-ready' && !ready) {
          send({type: 'chart-init', source, label: figure.dataset.chartLabel,
            language: document.documentElement.lang, ...environment()});
        } else if (message?.type === 'chart-ready') {
          clearTimeout(timer); ready = true;
          update('ready'); refresh();
        } else if (message?.type === 'chart-pointer' && typeof message.inside === 'boolean') {
          if (message.inside) {
            for (const other of document.querySelectorAll('.chart-hover')) if (other !== canvas) other.classList.remove('chart-hover');
          }
          canvas.classList.toggle('chart-hover', message.inside);
        } else if (message?.type === 'chart-error') fail();
      };
      addEventListener('message', receive);
      frame.addEventListener('error', fail, {once: true});
      timer = setTimeout(fail, 15000);
      frame.src = script.dataset.frame; view.append(frame);
    };
    const intersection = new IntersectionObserver(entries => {
      visible = entries.some(entry => entry.isIntersecting);
      if (visible) start();
      if (started) { intersection.disconnect(); resize.disconnect(); }
    }, {rootMargin: '200px'});
    // Closed details can intersect with a zero-sized box. Opening the fold may
    // change its size without crossing an intersection threshold.
    const resize = new ResizeObserver(() => {
      if (visible && !started) start();
      if (started) { intersection.disconnect(); resize.disconnect(); }
    });
    resize.observe(figure); intersection.observe(figure);
    records.push(refresh);
  }
  // A pointer leaving an out-of-process frame may resume only in the host.
  document.addEventListener('pointerover', event => {
    for (const canvas of document.querySelectorAll('.chart-hover')) {
      if (!canvas.contains(event.target)) canvas.classList.remove('chart-hover');
    }
  });
  new MutationObserver(() => records.forEach(refresh => refresh())).observe(document.documentElement,
    {attributes: true, attributeFilter: ['data-color-scheme']});
  reduced.addEventListener('change', () => records.forEach(refresh => refresh()));
})();
