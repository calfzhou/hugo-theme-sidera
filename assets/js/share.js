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


// Native fenced-code copy reuses the same Clipboard API, text-only toast and
// selected-field fallback pattern. Never include line numbers or toolbar text.
(() => {
  for (const block of document.querySelectorAll('article[data-renderer] .prose :is(.code-block,.content-copy)')) {
    const button = block.querySelector('.code-copy');
    const code = block.querySelector('.lntd:last-child code') || block.querySelector('pre code') || block.querySelector('.copy-value');
    if (!button || !code) continue;
    const fallback = block.querySelector('.code-copy-fallback');
    const idleLabel = button.getAttribute('aria-label');
    let resetTimer, pending = false;
    const reset = () => {
      block.classList.remove('is-copied');
      button.textContent = button.dataset.copy;
      button.setAttribute('aria-label', idleLabel);
    };
    button.hidden = false;
    block.classList.add('copy-ready');
    button.addEventListener('click', async () => {
      if (pending) return;
      pending = true;
      button.setAttribute('aria-busy', 'true');
      clearTimeout(resetTimer);
      reset();
      const plain = code.cloneNode(true);
      plain.querySelectorAll('.ln, .lnt').forEach(number => number.remove());
      // Chroma/HTML normalize CRLF. Inclusions retain their exact selected UTF-8
      // source separately; ordinary fences keep their existing rendered-text behavior.
      const text = block.hasAttribute('data-code-source')
        ? JSON.parse(block.dataset.codeSource) : plain.textContent;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(text);
        fallback.hidden = true;
        block.classList.add('is-copied');
        button.textContent = button.dataset.copied;
        button.setAttribute('aria-label', button.dataset.copied);
        window.Sidera?.toast(button.dataset.success, 2500);
        resetTimer = setTimeout(reset, 3000);
      } catch {
        fallback.value = text;
        fallback.hidden = false;
        fallback.focus();
        fallback.select();
        window.Sidera?.toast(button.dataset.failure);
      } finally {
        pending = false;
        button.removeAttribute('aria-busy');
      }
    });
  }
})();
