import { mount } from 'js/jsx/mount.jsx';
const hostOrigin = new URL(location.href).origin;
const tokens = ['--text', '--muted', '--quiet', '--secondary-text', '--control-border', '--accent', '--link', '--pin', '--danger', '--line', '--panel', '--surface', '--accent-soft', '--accent-fill', '--accent-on-fill', '--accent-fill-hover', '--ui', '--code'];
addEventListener('message', event => {
  if (event.source !== parent || event.origin !== hostOrigin || event.data?.type !== 'sidera-jsx-environment') return;
  const { scheme, tokens: values } = event.data;
  if (scheme === 'light' || scheme === 'dark') document.documentElement.dataset.colorScheme = scheme;
  for (const name of tokens) {
    if (typeof values?.[name] === 'string' && values[name].length <= 512) document.documentElement.style.setProperty(name, values[name]);
  }
});
try {
  mount(document.getElementById('root'), Component, {
    ready: () => parent.postMessage({ type: 'sidera-jsx-ready' }, hostOrigin),
    fail: () => parent.postMessage({ type: 'sidera-jsx-error' }, hostOrigin),
    prefix: 'jsx-frame-'
  });
} catch { parent.postMessage({ type: 'sidera-jsx-error' }, hostOrigin); }
