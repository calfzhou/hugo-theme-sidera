// Source-led Stellar toast presentation, with plain-text messages and one latest notification.
(() => {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let hideTimer, cleanupTimer, frame;
  function toast(message, duration = 2000) {
    if (typeof message !== 'string' || !Number.isFinite(duration) || duration < 0) {
      throw new TypeError('Sidera.toast requires a text message and a nonnegative duration');
    }
    if (!message.trim()) return;
    const notice = document.getElementById('sidera-toast');
    const status = document.getElementById('sidera-toast-status');
    if (!notice || !status) return; // UI is available after the document is ready.
    clearTimeout(hideTimer); clearTimeout(cleanupTimer); cancelAnimationFrame(frame);
    notice.classList.remove('is-visible');
    // A manual popover keeps site feedback above an open native sidebar drawer, without dismissing it.
    if (typeof notice.showPopover === 'function') {
      if (notice.matches(':popover-open')) notice.hidePopover();
      notice.setAttribute('popover', 'manual');
    }
    notice.textContent = message;
    status.textContent = '';
    notice.hidden = false;
    if (typeof notice.showPopover === 'function') notice.showPopover();
    notice.getBoundingClientRect(); // Establish the offscreen state before the entrance transition.
    frame = requestAnimationFrame(() => {
      notice.classList.add('is-visible');
      status.textContent = message;
      hideTimer = setTimeout(() => {
        notice.classList.remove('is-visible');
        cleanupTimer = setTimeout(() => {
          if (typeof notice.hidePopover === 'function' && notice.matches(':popover-open')) notice.hidePopover();
          notice.hidden = true;
          notice.textContent = '';
          status.textContent = '';
        }, reducedMotion.matches ? 0 : 500);
      }, duration + (reducedMotion.matches ? 0 : 500));
    });
  }
  window.Sidera = Object.assign(window.Sidera || {}, {toast});
})();
