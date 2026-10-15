import { mount } from './mount.jsx';
const script = document.querySelector('[data-sidera-jsx-script]');
const styles = new Map();
let serial = 0;
function loadStyle(url) {
  if (!url) return Promise.resolve();
  if (!styles.has(url)) styles.set(url, new Promise((resolve, reject) => {
    const link = document.createElement('link');
    link.rel = 'stylesheet'; link.href = url;
    link.onload = resolve; link.onerror = reject;
    document.head.append(link);
  }));
  return styles.get(url);
}
const tokens = ['--text', '--muted', '--quiet', '--accent', '--link', '--pin', '--line', '--panel', '--surface', '--accent-soft', '--ui', '--code'];
const environments = [];
for (const figure of document.querySelectorAll('[data-sidera-jsx]')) {
  const container = figure.querySelector('.jsx-root');
  const status = figure.querySelector('.jsx-status');
  const fallback = figure.querySelector('.jsx-fallback');
  let started = false, failed = false, frame, timer, receive;
  const prefix = `sidera-jsx-${++serial}-`;
  const fail = error => {
    if (failed) return;
    failed = true; clearTimeout(timer);
    if (receive) removeEventListener('message', receive);
    frame?.remove(); container.hidden = true; fallback.hidden = false;
    figure.dataset.state = 'error'; status.textContent = script.dataset.error;
    status.classList.remove('visually-hidden');
    console.error('Sidera JSX:', error);
  };
  const ready = () => {
    if (failed) return;
    clearTimeout(timer); figure.dataset.state = 'ready';
    fallback.hidden = true; status.textContent = script.dataset.ready;
    status.classList.add('visually-hidden');
  };
  const environment = () => {
    if (!frame || failed) return;
    const css = getComputedStyle(figure);
    frame.contentWindow?.postMessage({ type: 'sidera-jsx-environment',
      scheme: document.documentElement.dataset.colorScheme,
      tokens: Object.fromEntries(tokens.map(key => [key, css.getPropertyValue(key)])) }, '*');
  };
  const start = async () => {
    if (started || !figure.getClientRects().length || !figure.getBoundingClientRect().width) return;
    started = true; observer.unobserve(figure); resize.disconnect();
    figure.dataset.state = 'loading'; status.textContent = script.dataset.loading;
    container.hidden = false;
    timer = setTimeout(() => fail('Component startup timed out'), 15000);
    try {
      if (figure.dataset.mode === 'sandbox') {
        frame = document.createElement('iframe'); frame.className = 'jsx-frame';
        frame.sandbox = 'allow-scripts'; frame.title = figure.dataset.label;
        frame.referrerPolicy = 'no-referrer'; frame.style.height = `${figure.dataset.height}px`;
        receive = event => {
          if (event.source !== frame.contentWindow || event.origin !== 'null') return;
          if (event.data?.type === 'sidera-jsx-ready') { environment(); ready(); }
          else if (event.data?.type === 'sidera-jsx-error') fail('Sandbox render failed');
        };
        addEventListener('message', receive); environments.push(environment);
        frame.addEventListener('error', fail, { once: true });
        frame.src = figure.dataset.module; container.append(frame);
      } else {
        const [module] = await Promise.all([import(figure.dataset.module), loadStyle(figure.dataset.css)]);
        if (failed) return;
        mount(container, module.default, { ready, fail, prefix });
      }
    } catch (error) { fail(error); }
  };
  let visible = false;
  const observer = new IntersectionObserver(entries => {
    visible = entries.some(entry => entry.isIntersecting);
    if (visible) start();
  }, { rootMargin: '200px' });
  const resize = new ResizeObserver(() => { if (visible) start(); });
  observer.observe(figure); resize.observe(figure);
}
new MutationObserver(() => environments.forEach(update => update())).observe(document.documentElement,
  { attributes: true, attributeFilter: ['data-color-scheme'] });
