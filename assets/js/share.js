// Progressive copy only: ordinary share links and QR details remain native without JavaScript.
(() => {
  for (const section of document.querySelectorAll('.article-share')) {
    const button = section.querySelector('[data-share-copy]');
    if (!button || !navigator.clipboard?.writeText) continue;
    button.hidden = false;
    section.querySelector('.share-link-fallback').hidden = true;
    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        await navigator.clipboard.writeText(section.dataset.shareUrl);
        window.Sidera?.toast(button.dataset.success);
      } catch {
        const fallback = section.querySelector('.share-copy-fallback');
        fallback.hidden = false;
        const input = fallback.querySelector('input');
        input.focus(); input.select();
        window.Sidera?.toast(button.dataset.failure);
      } finally { button.disabled = false; }
    });
  }
})();
