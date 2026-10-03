// Opt-in original image viewer. URLs were validated server-side; originals stay img
// resources (never inserted SVG/HTML). No fetch/proxy, automatic download or gallery.
(() => {
  const template = document.querySelector('template[data-image-viewer-template]');
  if (!template || typeof HTMLDialogElement === 'undefined' || !HTMLDialogElement.prototype.showModal) return;
  let dialog, view, status, caption, active, zoom = 1, drag;
  function appearance() {
    if (!active) return;
    const {thumb, image} = active;
    const filters = [getComputedStyle(thumb).filter];
    for (let node = thumb.parentElement; node; node = node.parentElement) {
      if (node.matches('.invert-when-dark,.invert-when-light')) filters.push(getComputedStyle(node).filter);
    }
    image.style.filter = filters.filter(value => value !== 'none').join(' ') || 'none';
    image.style.backgroundColor = getComputedStyle(thumb).backgroundColor;
  }
  function size() {
    if (!active?.ready || !dialog.open) return;
    const image = active.image;
    const fit = Math.min(1, view.clientWidth / image.naturalWidth, view.clientHeight / image.naturalHeight);
    image.style.width = Math.max(1, image.naturalWidth * fit * zoom) + 'px';
  }
  function changeZoom(value) {
    if (!active?.ready) return;
    const rect = active.image.getBoundingClientRect(), viewport = view.getBoundingClientRect();
    const x = (viewport.left + view.clientWidth / 2 - rect.left) / rect.width;
    const y = (viewport.top + view.clientHeight / 2 - rect.top) / rect.height;
    zoom = value; size();
    view.scrollLeft = x * active.image.width - view.clientWidth / 2;
    view.scrollTop = y * active.image.height - view.clientHeight / 2;
  }
  function cleanup(restoreFocus) {
    const previous = active;active = null;drag = null;
    document.documentElement.classList.remove('image-modal-open');
    if (previous) {
      previous.image.removeAttribute('src');previous.link.setAttribute('aria-expanded', 'false');
      if (restoreFocus) previous.link.focus({preventScroll:true});
    }
    view.replaceChildren();view.removeAttribute('aria-busy');
  }
  function createDialog() {
    if (dialog) return;
    dialog = template.content.querySelector('dialog').cloneNode(true);
    document.body.append(dialog);
    view = dialog.querySelector('.image-view');status = dialog.querySelector('.image-viewer-status');caption = dialog.querySelector('.image-dialog-caption');
    dialog.addEventListener('close', () => { if (!dialog.open) cleanup(true); });
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
    dialog.addEventListener('keydown', event => {
      if (event.key !== 'Tab') return;
      const controls = [...dialog.querySelectorAll('button,a[href],[tabindex]')].filter(el => !el.disabled && el.tabIndex >= 0 && el.getClientRects().length);
      const first = controls[0], last = controls.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault();last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault();first.focus(); }
    });
    for (const button of dialog.querySelectorAll('button[data-image-action]')) button.addEventListener('click', () => {
      switch (button.dataset.imageAction) {
        case 'close': dialog.close();break;
        case 'in': changeZoom(Math.min(8, zoom * 1.25));break;
        case 'out': changeZoom(Math.max(.25, zoom / 1.25));break;
        case 'fit': zoom = 1;size();view.scrollTo(0, 0);break;
      }
    });
    view.addEventListener('keydown', event => {
      if (event.target !== view || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      const delta = {ArrowLeft:[-40,0],ArrowRight:[40,0],ArrowUp:[0,-40],ArrowDown:[0,40]}[event.key];
      if (delta) { event.preventDefault();view.scrollLeft += delta[0];view.scrollTop += delta[1]; }
    });
    view.addEventListener('pointerdown', event => {
      if (active?.ready && event.pointerType === 'mouse' && event.button === 0) {
        drag = {x:event.clientX,y:event.clientY,left:view.scrollLeft,top:view.scrollTop};view.setPointerCapture(event.pointerId);
      }
    });
    view.addEventListener('pointermove', event => { if (drag) { view.scrollLeft = drag.left + drag.x - event.clientX;view.scrollTop = drag.top + drag.y - event.clientY; } });
    view.addEventListener('pointerup', () => { drag = null; });view.addEventListener('lostpointercapture', () => { drag = null; });
    new ResizeObserver(size).observe(view);
  }
  for (const link of document.querySelectorAll('.content-image a[data-image-open]')) {
    link.setAttribute('aria-haspopup', 'dialog');link.setAttribute('aria-expanded', 'false');
    link.addEventListener('click', async event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) return;
      event.preventDefault();createDialog();if (dialog.open) return;
      if (active) cleanup(false); // A prior close event may still be queued.
      const thumb = link.querySelector('img'), image = new Image();image.className = 'image-viewer-image';image.alt = thumb.alt;image.draggable = false;
      const request = {link,thumb,image,ready:false};active = request;zoom = 1;
      const text = link.closest('figure').querySelector('figcaption')?.textContent || '';
      caption.textContent = text;caption.hidden = !text;
      dialog.setAttribute('aria-label', text || thumb.alt || dialog.dataset.defaultLabel);
      const download = dialog.querySelector('[data-image-action="download"]');
      download.href = link.href;download.target = link.target;download.rel = link.rel;
      for (const button of dialog.querySelectorAll('button:not([data-image-action="close"])')) button.disabled = true;
      status.textContent = dialog.dataset.loading;status.hidden = false;view.setAttribute('aria-busy', 'true');view.replaceChildren();
      link.setAttribute('aria-expanded', 'true');dialog.showModal();document.documentElement.classList.add('image-modal-open');
      appearance();image.src = link.href;
      try {
        await image.decode();
        if (active !== request || !dialog.open) return;
        request.ready = true;status.hidden = true;view.removeAttribute('aria-busy');
        view.replaceChildren(image);size();view.scrollTo(0, 0);
        for (const button of dialog.querySelectorAll('button')) button.disabled = false;
      } catch {
        if (active !== request || !dialog.open) return;
        status.textContent = dialog.dataset.error;status.hidden = false;view.removeAttribute('aria-busy');
      }
    });
  }
  new MutationObserver(appearance).observe(document.documentElement, {attributes:true,attributeFilter:['data-color-scheme']});
})();
