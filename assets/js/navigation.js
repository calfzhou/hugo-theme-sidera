// In-flow native disclosures. No script leaves every region reachable and open.
for (const [selector, query] of [
  ['.site-menu', '(min-width: 761px)'],
  ['.context-menu', '(min-width: 1231px)']
]) {
  const disclosure = document.querySelector(selector);
  if (!disclosure) continue;
  const wide = matchMedia(query);
  const update = () => { disclosure.open = wide.matches; };
  update();
  wide.addEventListener('change', update);
}

// Native anchors remain native (URL, history, focus and no-script behavior).
// Track the last heading above the reading offset; do not steal focus or scroll a rail.
const tocLinks = [...document.querySelectorAll('[data-toc] a[href^="#"]')];
const headings = [...document.querySelectorAll('.prose :is(h2,h3,h4,h5,h6)[id]')]
  .filter(heading => tocLinks.some(link => {
    try { return decodeURIComponent(link.hash.slice(1)) === heading.id; }
    catch { return false; }
  }));
if (headings.length) {
  let queued = false;
  const update = () => {
    queued = false;
    let current = headings[0];
    for (const heading of headings) {
      if (heading.getBoundingClientRect().top > 36) break;
      current = heading;
    }
    for (const link of tocLinks) {
      let active = false;
      try { active = decodeURIComponent(link.hash.slice(1)) === current.id; } catch { /* malformed custom anchor */ }
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  };
  const schedule = () => { if (!queued) { queued = true; requestAnimationFrame(update); } };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule);
  addEventListener('hashchange', schedule);
  addEventListener('load', schedule);
  update();
}
