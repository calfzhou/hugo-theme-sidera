// Progressive content controls: source HTML remains readable if this file fails.
(() => {
  let serial = 0;
  const uniqueID = () => {
    let id;
    do { id = `sidera-content-${++serial}`; } while (document.getElementById(id));
    return id;
  };
  const groups = [];
  for (const group of document.querySelectorAll('.content-tabs')) {
    const panels = [...group.children].filter(el => el.classList.contains('content-tab'));
    if (!panels.length) continue;
    const nav = document.createElement('div');
    nav.className = 'tabs-nav';
    nav.setAttribute('role', 'tablist');
    nav.setAttribute('aria-label', group.dataset.label);
    nav.dataset.searchExclude = '';
    const buttons = panels.map(panel => {
      const title = panel.querySelector(':scope > .tab-title');
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = title.textContent;
      button.id = uniqueID();
      panel.id ||= uniqueID();
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-controls', panel.id);
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', button.id);
      panel.tabIndex = 0;
      nav.append(button);
      return button;
    });
    const activate = (index, focus = false) => {
      buttons.forEach((button, i) => {
        button.setAttribute('aria-selected', String(i === index));
        button.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) {
        buttons[index].focus({preventScroll: true});
        // Scroll the tab strip only, never jump the document on arrow keys.
        const r = buttons[index].getBoundingClientRect(), box = nav.getBoundingClientRect();
        if (r.left < box.left) nav.scrollLeft -= box.left - r.left;
        if (r.right > box.right) nav.scrollLeft += r.right - box.right;
      }
    };
    nav.addEventListener('click', event => {
      const index = buttons.indexOf(event.target.closest('button'));
      if (index >= 0) activate(index);
    });
    nav.addEventListener('keydown', event => {
      const index = buttons.indexOf(event.target);
      if (index < 0) return;
      const rtl = getComputedStyle(nav).direction === 'rtl';
      const step = event.key === 'ArrowRight' ? (rtl ? -1 : 1) : (rtl ? 1 : -1);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 :
        ['ArrowLeft', 'ArrowRight'].includes(event.key) ? (index + step + buttons.length) % buttons.length : -1;
      if (next >= 0) { event.preventDefault(); activate(next, true); }
    });
    group.prepend(nav);
    activate(Math.min(panels.length - 1, Math.max(0, Number(group.dataset.active) - 1)));
    group.dataset.enhanced = '';
    groups.push({panels, activate});
  }
  // TOC/deep links open every enclosing panel (including nested tab groups).
  const reveal = target => {
    if (!target) return;
    for (let parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.localName === 'details') parent.open = true;
    }
    for (const {panels, activate} of groups) {
      const index = panels.findIndex(panel => panel.contains(target));
      if (index >= 0) activate(index);
    }
  };
  const fragmentTarget = () => {
    try { return document.getElementById(decodeURIComponent(location.hash.slice(1))); }
    catch { return null; }
  };
  const revealHash = () => {
    const target = fragmentTarget();
    reveal(target);
    if (target) requestAnimationFrame(() => target.scrollIntoView({block: 'start', behavior: 'instant'}));
  };
  if (groups.length) {
    revealHash();
    addEventListener('hashchange', revealHash);
    document.addEventListener('click', event => {
      const link = event.target.closest('a[href]');
      if (!link) return;
      const url = new URL(link.href, location.href);
      if (url.origin === location.origin && url.pathname === location.pathname && url.search === location.search && url.hash) {
        try { reveal(document.getElementById(decodeURIComponent(url.hash.slice(1)))); } catch { /* malformed fragment */ }
      }
    });
    document.addEventListener('sidera:reveal', event => reveal(event.target));
  }
  for (const button of document.querySelectorAll('.content-reveal')) {
    button.dataset.enhanced = '';
    button.setAttribute('aria-pressed', 'false');
    button.addEventListener('click', () => button.setAttribute('aria-pressed', String(button.getAttribute('aria-pressed') !== 'true')));
  }
  for (const tip of document.querySelectorAll('.content-tip')) {
    const trigger = tip.querySelector('.tip-trigger'), bubble = tip.querySelector('.tip-bubble');
    if (!trigger || !bubble || !('showPopover' in bubble)) continue;
    bubble.id = uniqueID();
    bubble.popover = 'manual';
    trigger.setAttribute('aria-describedby', bubble.id);
    tip.dataset.enhanced = '';
    let dismissed = false, hovered = false;
    const position = () => {
      const r = trigger.getBoundingClientRect(), b = bubble.getBoundingClientRect();
      bubble.style.left = `${Math.max(8, Math.min(innerWidth - b.width - 8, r.left + r.width / 2 - b.width / 2))}px`;
      bubble.style.top = `${Math.max(8, Math.min(innerHeight - b.height - 8, r.top >= b.height + 8 ? r.top - b.height : r.bottom))}px`;
    };
    const close = () => { if (bubble.matches(':popover-open')) bubble.hidePopover(); };
    const show = () => {
      if (dismissed) return;
      if (!bubble.matches(':popover-open')) bubble.showPopover();
      position();
    };
    tip.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') { hovered = true; dismissed = false; show(); } });
    tip.addEventListener('pointerleave', () => { hovered = false; if (!tip.contains(document.activeElement)) { close(); dismissed = false; } });
    trigger.addEventListener('focus', show);
    trigger.addEventListener('click', () => { dismissed = false; show(); });
    tip.addEventListener('focusout', event => { if (!tip.contains(event.relatedTarget)) { dismissed = false; if (!hovered) close(); } });
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && bubble.matches(':popover-open')) { close(); dismissed = true; } });
    document.addEventListener('pointerdown', event => { if (!tip.contains(event.target)) { close(); dismissed = true; } });
    addEventListener('resize', () => { if (bubble.matches(':popover-open')) position(); });
    document.addEventListener('scroll', () => { if (bubble.matches(':popover-open')) position(); }, {capture: true, passive: true});
  }
})();
