// Progressive page-entry motion. Source/CSS is visible even if this script fails.
(() => {
  const shell = document.querySelector('.site-shell');
  if (!shell || shell.dataset.revealInitialized) return;
  shell.dataset.revealInitialized = 'true';
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const navigation = performance.getEntriesByType('navigation')[0];
  // Do not disturb heading destinations, restored positions or history traversal.
  if (motion.matches || location.hash || scrollY > 0 || navigation?.type === 'back_forward' ||
      typeof Element.prototype.animate !== 'function') return;

  const visible = element => {
    if (element.closest('[hidden], [inert]') || element.contains(document.activeElement)) return false;
    const rect = element.getBoundingClientRect();
    if (!rect.width || !rect.height) return false;
    let top = Math.max(0, rect.top), bottom = Math.min(innerHeight, rect.bottom);
    let left = Math.max(0, rect.left), right = Math.min(innerWidth, rect.right);
    for (let node = element; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.visibility !== 'visible' || style.display === 'none') return false;
      if (node !== element) {
        const box = node.getBoundingClientRect();
        if (/(auto|scroll|hidden|clip)/.test(style.overflowY)) {
          top = Math.max(top, box.top); bottom = Math.min(bottom, box.bottom);
        }
        if (/(auto|scroll|hidden|clip)/.test(style.overflowX)) {
          left = Math.max(left, box.left); right = Math.min(right, box.right);
        }
      }
    }
    return bottom > top && right > left;
  };
  // Independent columns start together; never animate both a region and its child.
  const groups = [
    ['.left-region', '.region-component, .sidebar-footer'],
    ['.right-region', '.region-component'],
    ['.reading-column', '.top-region, .view-header, .article-card, .archive-year, .article-header, [data-renderer="shared-article"] > .prose, .article-footer, .page-navigation, .pagination, .site-footer, .not-found'],
  ];
  const animations = new Map();
  const stop = () => {
    for (const animation of animations.values()) animation.cancel();
    animations.clear();
    motion.removeEventListener('change', stop);
    document.removeEventListener('focusin', stop);
    removeEventListener('pagehide', stop);
  };
  motion.addEventListener('change', stop);
  document.addEventListener('focusin', stop);
  addEventListener('pagehide', stop);
  try {
    for (const [rootSelector, selector] of groups) {
      const root = shell.querySelector(rootSelector);
      if (!root) continue;
      const candidates = [...root.querySelectorAll(selector)];
      const targets = candidates.filter(el => !candidates.some(parent => parent !== el && parent.contains(el)) && visible(el))
        .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
      targets.forEach((el, index) => {
        const animation = el.animate([
          {opacity: 0, translate: '0 8px'},
          {opacity: 1, translate: '0 0'},
        ], {duration: 1000, delay: Math.min(index, 3) * 100, easing: 'ease-out', fill: 'backwards'});
        animations.set(el, animation);
        animation.onfinish = () => {
          animations.delete(el);
          if (!animations.size) stop();
        };
      });
    }
  } catch {
    stop(); // An unsupported/failed animation cannot strand hidden content.
  }
  if (!animations.size) stop();
})();
