// Exercise the shipped controller without adding a test-only runtime API.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
const source = await readFile(new URL('../assets/js/random.js', import.meta.url), 'utf8');

async function boot(urls, current, {ok = true, reject = false, jsonError = false} = {}) {
  const buttons = Array.from({length: 3}, () => ({
    hidden: false, disabled: true, listeners: [], attributes: new Map([['aria-busy', 'true']]),
    removeAttribute(name) { this.attributes.delete(name); },
    addEventListener(type, listener) { assert.equal(type, 'click'); this.listeners.push(listener); },
  }));
  const jumps = [];
  let fetches = 0, random = 0;
  const context = {
    document: {
      currentScript: {dataset: {index: '/preview/random/en.hash.json', current}},
      querySelectorAll: () => buttons,
    },
    fetch: async url => {
      fetches++;
      assert.equal(url, '/preview/random/en.hash.json');
      if (reject) throw new Error('Network unavailable');
      return {ok, json: async () => { if (jsonError) throw new Error('Invalid JSON'); return urls; }};
    },
    location: {origin: 'https://example.invalid', href: 'https://example.invalid' + current, assign: url => jumps.push(url)},
    URL, Math: {floor: Math.floor, random: () => random},
  };
  vm.runInNewContext(source, context);
  assert(buttons.every(b => !b.hidden && b.disabled && b.attributes.get('aria-busy') === 'true' && !b.listeners.length),
    'Every instance keeps its server-rendered loading state before the fetch settles');
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(fetches, 1, 'Repeated instances share one fetch');
  assert(buttons.every(b => !b.attributes.has('aria-busy')), 'Settled controls are not busy');
  return {buttons, jumps, choose(value, button = 0) { random = value; buttons[button].listeners[0](); }};
}

for (let size = 0; size <= 8; size++) {
  const urls = Array.from({length: size}, (_, i) => `/preview/article-${i}/`);
  for (let current = -1; current < size; current++) {
    const currentURL = urls[current] || '/preview/';
    const eligible = urls.filter(url => url !== currentURL);
    const test = await boot(urls, currentURL);
    assert(test.buttons.every(b => b.hidden === !eligible.length && b.disabled === !eligible.length));
    if (!eligible.length) {
      assert(test.buttons.every(b => !b.listeners.length));
      continue;
    }
    for (let i = 0; i < eligible.length; i++) {
      // Each equal-sized random interval selects exactly one other article.
      test.choose((i + 0.5) / eligible.length, i % 3);
      assert.equal(test.jumps.at(-1), eligible[i]);
    }
    test.choose(0); assert.equal(test.jumps.at(-1), eligible[0]);
    test.choose(1 - Number.EPSILON); assert.equal(test.jumps.at(-1), eligible.at(-1));
    assert(!test.jumps.includes(currentURL));
    assert.deepEqual(urls, Array.from({length: size}, (_, i) => `/preview/article-${i}/`));
  }
}
for (const options of [{ok: false}, {reject: true}, {jsonError: true}]) {
  const test = await boot(['/preview/other/'], '/preview/', options);
  assert(test.buttons.every(b => b.hidden && b.disabled && !b.listeners.length));
}
for (const urls of [null, {}, [3], ['javascript:alert(1)'], ['//outside.invalid/'], ['https://outside.invalid/'], ['/\\outside.invalid/']]) {
  const test = await boot(urls, '/preview/');
  assert(test.buttons.every(b => b.hidden && b.disabled && !b.listeners.length));
}
console.log('PASS random selection: every position and interval, shared fetch, repeated instances, empty/singleton, immutable pool, failures and unsafe URLs');
