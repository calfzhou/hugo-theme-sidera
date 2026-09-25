// Native auto-popovers provide Escape, light-dismiss, focus return and one open
// region at a time. Without support/script, the original in-flow details stay open.
if ('showPopover' in HTMLElement.prototype) {
  document.documentElement.classList.add('drawers-ready');
  for (const [name, query] of [['left', '(max-width: 667px)'], ['right', '(max-width: 1180px)']]) {
    const region = document.querySelector(`#${name}-region`);
    const button = document.querySelector(`[data-region="${name}"]`);
    if (!region || !button) continue;
    const narrow = matchMedia(query);
    const update = () => {
      if (region.matches(':popover-open')) region.hidePopover();
      if (narrow.matches) region.setAttribute('popover', 'auto');
      else region.removeAttribute('popover');
      button.setAttribute('aria-expanded', 'false');
    };
    region.addEventListener('toggle', event => {
      button.setAttribute('aria-expanded', String(event.newState === 'open'));
    });
    region.addEventListener('click', event => {
      // Follow real TOC/history links; dismiss only the overlay, not the anchor.
      if (event.target.closest('a[href^="#"]') && region.matches(':popover-open')) region.hidePopover();
    });
    update();
    narrow.addEventListener('change', update);
  }
}

// Native anchors remain native (URL, history, focus and no-script behavior).
// Track the last heading above the reading offset; never steal focus or scroll the document.
const tocLinks = [...document.querySelectorAll('[data-toc] a[href^="#"]')];
const headings = [...document.querySelectorAll('.prose :is(h1,h2,h3,h4,h5,h6)[id]')]
  .filter(heading => tocLinks.some(link => {
    try { return decodeURIComponent(link.hash.slice(1)) === heading.id; }
    catch { return false; }
  }));
if (headings.length) {
  const revealCurrent = link => {
    const toc = link.closest('[data-toc]');
    if (!toc.clientHeight || toc.scrollHeight <= toc.clientHeight || toc.contains(document.activeElement)) return;
    const row = link.getBoundingClientRect(), box = toc.getBoundingClientRect();
    const above = row.top - box.top - 64, below = row.bottom - box.bottom + 100;
    if (above < 0) toc.scrollTop += above;
    else if (below > 0) toc.scrollTop += below;
  };
  for (const disclosure of document.querySelectorAll('[data-responsive-toc]')) {
    disclosure.addEventListener('toggle', () => {
      const link = disclosure.querySelector('[data-toc] a[aria-current]');
      if (disclosure.open && link) revealCurrent(link);
    });
  }
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
      if (active) {
        const changed = !link.hasAttribute('aria-current');
        link.setAttribute('aria-current', 'location');
        if (changed) revealCurrent(link);
      }
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

// Stellar/React Bits card hover, adapted to static Hugo cards (see third-party notices).
// One queued frame per hovered card; touch, reduced motion and keyboard never tilt.
const cardMotion = matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)');
for (const card of document.querySelectorAll('.article-card:has(.card-content), .collection-card')) {
  let frame = 0, point;
  const reset = () => {
    cancelAnimationFrame(frame); frame = 0; point = null;
    card.classList.remove('pointer-active');
    for (const key of ['--pointer-x', '--pointer-y', '--tilt-x', '--tilt-y']) card.style.removeProperty(key);
  };
  card.addEventListener('pointermove', event => {
    if (!cardMotion.matches || event.pointerType === 'touch') return;
    point = { x: event.clientX, y: event.clientY };
    if (frame) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      const rect = card.getBoundingClientRect();
      const x = Math.max(0, Math.min(rect.width, point.x - rect.left));
      const y = Math.max(0, Math.min(rect.height, point.y - rect.top));
      card.style.setProperty('--pointer-x', `${x}px`);
      card.style.setProperty('--pointer-y', `${y}px`);
      card.style.setProperty('--tilt-x', `${-(y / rect.height * 2 - 1) * 3}deg`);
      card.style.setProperty('--tilt-y', `${(x / rect.width * 2 - 1) * 3}deg`);
      card.classList.add('pointer-active');
    });
  });
  card.addEventListener('pointerleave', reset);
  card.addEventListener('pointercancel', reset);
  card.addEventListener('focusin', reset);
  cardMotion.addEventListener('change', reset);
}

// Sticky collection browsing gets Stellar's translucent pinned surface. Links remain native.
const topRegion = document.querySelector('.top-region:has([data-collection-nav])');
if (topRegion) {
  let scheduled = false;
  const update = () => {
    scheduled = false;
    const inset = parseFloat(getComputedStyle(topRegion).top) || 0;
    topRegion.classList.toggle('is-stuck', scrollY > 0 && topRegion.getBoundingClientRect().top <= inset + 1);
  };
  addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }, {passive: true});
  addEventListener('resize', update);
  update();
}
