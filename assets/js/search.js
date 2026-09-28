(() => {
  'use strict';
  const script = document.querySelector('script[data-sidera-search]');
  if (!script) return;
  const rules = JSON.parse(script.dataset.rules);
  const wrapper = document.querySelector('[data-search-wrapper]');
  const root = document.querySelector('[data-search-body]');
  const markText = (parent, text, words, className = 'search-keyword') => {
    let previous = 0;
    for (const [start,end] of SideraSearch.matches(text, words)) {
      parent.append(document.createTextNode(text.slice(previous,start)));
      const mark = document.createElement('mark'); mark.className=className; mark.textContent=text.slice(start,end); parent.append(mark); previous=end;
    }
    parent.append(document.createTextNode(text.slice(previous)));
  };
  function clearMarks() {
    if (!root) return;
    for (const mark of root.querySelectorAll('mark[data-search-mark]')) mark.replaceWith(document.createTextNode(mark.textContent));
    root.normalize();
  }
  let clearButton;
  function highlight(scroll = true) {
    if (!root) return;
    clearMarks();
    const query = new URL(location.href).searchParams.get('kw') || '';
    const words = SideraSearch.tokens(query);
    if (clearButton) clearButton.hidden = !words.length;
    if (!words.length) return;
    if (!clearButton) {
      clearButton = document.createElement('button'); clearButton.type='button'; clearButton.className='search-highlight-clear';
      clearButton.textContent=root.dataset.clearHighlights; root.before(clearButton);
      clearButton.addEventListener('click', () => {
        const url = new URL(location.href); url.searchParams.delete('kw'); history.replaceState(history.state, '', url);
        clearMarks(); clearButton.hidden=true;
      });
    }
    const sections = SideraSearch.bodySections(root,rules);
    let anchor = null;
    try { anchor = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { /* malformed fragment: no forced scroll */ }
    // Prioritize the selected section so the bounded mark budget cannot be consumed
    // by unrelated intro matches. Keep the native heading target authoritative.
    const selected = anchor && sections.find(s => s.id === anchor.id);
    const ordered = selected ? [selected, ...sections.filter(s => s !== selected)] : sections;
    const byNode = new Map(); let budget = 100, usefulNode = null, usefulMark = null;
    for (const section of ordered) {
      for (const [start,end] of SideraSearch.matches(section.text, words, budget)) {
        if (budget-- <= 0) break;
        if (!usefulNode && (!selected || section === selected)) usefulNode = section.map.slice(start,end).find(Boolean)?.node;
        for (let i=start; i<end; i++) {
          const p = section.map[i]; if (!p) continue;
          let ranges = byNode.get(p.node); if (!ranges) byNode.set(p.node, ranges=[]);
          const last = ranges.at(-1);
          if (last && last[1] === p.offset) last[1]++; else ranges.push([p.offset,p.offset+1]);
        }
      }
      if (budget <= 0) break;
    }
    for (const [node,ranges] of byNode) {
      const text = node.nodeValue, fragment = document.createDocumentFragment(); let at=0;
      for (const [start,end] of ranges) {
        fragment.append(document.createTextNode(text.slice(at,start)));
        const mark=document.createElement('mark'); mark.dataset.searchMark=''; mark.className='search-body-mark'; mark.textContent=text.slice(start,end); fragment.append(mark); at=end;
        if (!usefulMark && node === usefulNode) usefulMark = mark;
      }
      fragment.append(document.createTextNode(text.slice(at))); node.replaceWith(fragment);
    }
    const target = anchor && root.contains(anchor) ? anchor : !location.hash ? root.querySelector('[data-search-mark]') : null;
    // Reveal the first match in the selected section too: its heading can be
    // outside a closed fold. Do not open every matching disclosure on the page.
    for (const item of [target, (!location.hash || selected) && usefulMark].filter(Boolean)) {
      for (let el=item.parentElement; el && el!==root; el=el.parentElement) if (el.localName==='details') el.open=true;
    }
    if (target) {
      if (scroll) requestAnimationFrame(() => target.scrollIntoView({block:'start',behavior:'instant'}));
    }
  }
  highlight();
  addEventListener('pageshow', e => { if (e.persisted) highlight(false); });
  addEventListener('popstate', () => highlight(false));
  if (!wrapper) return;
  const input = wrapper.querySelector('input'), scope = wrapper.querySelector('select');
  const result = wrapper.querySelector('.search-results'), status = wrapper.querySelector('.search-status'), clear = wrapper.querySelector('.search-clear');
  let documents = null, pending = null, failed = false;
  input.disabled=false; wrapper.querySelector('.search-fallback').hidden=true;
  const state = text => { status.textContent=text; status.hidden=!text; };
  function render() {
    const focused = result.contains(document.activeElement) ? document.activeElement.getAttribute('href') : null;
    result.replaceChildren(); const query=input.value.trim(), words=SideraSearch.tokens(query);
    wrapper.classList.toggle('searching', !!query); clear.hidden=!query;
    if (!query) { state(''); return; }
    if (!documents) { state(failed ? wrapper.dataset.failed : wrapper.dataset.loading); return; }
    const hits=SideraSearch.search(documents,query,scope?.value || '');
    state(hits.length ? '' : wrapper.dataset.empty);
    const list=document.createElement('ul'); list.className='search-result-list';
    for (const [index,hit] of hits.entries()) {
      const url=new URL(hit.doc.url,location.href);
      if (url.origin!==location.origin || !['http:','https:'].includes(url.protocol)) continue;
      url.searchParams.set('kw', query.slice(0,160)); if(hit.section?.id) url.hash=hit.section.id;
      const item=document.createElement('li'), title=document.createElement('span'); title.className='search-result-title'; title.id=`search-title-${index}`;
      markText(title,hit.doc.title,words); item.append(title);
      const link=document.createElement('a'); link.href=url.pathname+url.search+url.hash; link.referrerPolicy='no-referrer';
      link.className='search-result-link'; link.setAttribute('aria-labelledby',`search-title-${index} search-heading-${index}`);
      const context=document.createElement('span'); context.className='search-result-context'; context.textContent=hit.doc.context; link.append(context);
      const heading=document.createElement('span'); heading.className='search-result-section'; heading.id=`search-heading-${index}`;
      const marker=document.createElement('span'); marker.className='search-section-marker'; marker.setAttribute('aria-hidden','true'); marker.textContent='>'; heading.append(marker);
      markText(heading,hit.section?.title || (hit.section ? hit.doc.title : wrapper.dataset.titleOnly),words); link.append(heading);
      if(hit.section) {
        const first=hit.ranges[0]?.[0] || 0, start=Math.max(0,first-24), end=Math.min(hit.section.text.length,start+140);
        const snippet=document.createElement('p'); snippet.className='search-result-content';
        markText(snippet,(start ? '…' : '')+hit.section.text.slice(start,end)+(end<hit.section.text.length ? '…' : ''),words); link.append(snippet);
      }
      item.append(link); list.append(item);
    }
    if (list.children.length) result.append(list);
    if (focused) [...result.querySelectorAll('a')].find(a => a.getAttribute('href') === focused)?.focus();
  }
  async function load() {
    if (pending) return pending;
    failed=false;
    wrapper.classList.add('is-loading'); wrapper.classList.remove('search-error'); result.setAttribute('aria-busy','true');
    pending=(async () => {
      const controller=new AbortController(), timer=setTimeout(()=>controller.abort(),10000);
      try {
        const url=new URL(script.dataset.index,location.href); if(url.origin!==location.origin) throw Error('Nonlocal index');
        const response=await fetch(url,{cache:'no-store',referrerPolicy:'no-referrer',signal:controller.signal});
        if(!response.ok) throw Error('Index unavailable');
        const data=await response.json();
        if(data.version!==1 || !Array.isArray(data.documents) || !data.documents.every(d => ['url','title','scope','context'].every(k => typeof d[k] === 'string') && Array.isArray(d.sections) && d.sections.every(s => ['id','title','text'].every(k => typeof s[k] === 'string')))) throw Error('Invalid index');
        documents=data.documents; failed=false;
      } catch { documents=null; failed=true; }
      finally { clearTimeout(timer); pending=null; wrapper.classList.remove('is-loading'); wrapper.classList.toggle('search-error',failed); result.setAttribute('aria-busy','false'); render(); }
    })();
    render(); return pending;
  }
  input.addEventListener('input', event => { if(!event.isComposing) render(); });
  input.addEventListener('compositionend', render);
  input.addEventListener('focus', load);
  scope?.addEventListener('change', () => { input.placeholder=scope.value ? input.dataset.localLabel : input.dataset.globalLabel; input.setAttribute('aria-label',input.placeholder); render(); });
  const reset = () => { input.value=''; render(); input.focus(); };
  clear.addEventListener('click', reset);
  wrapper.addEventListener('keydown', e => {
    if(e.isComposing) return;
    const links=[...result.querySelectorAll('a')], at=links.indexOf(document.activeElement);
    if(e.key==='Escape' && input.value) { e.preventDefault(); e.stopPropagation(); reset(); }
    else if(e.key==='ArrowDown' && links.length && (e.target===input || at>=0)) { e.preventDefault(); links[Math.min(at+1,links.length-1)].focus(); }
    else if(e.key==='ArrowUp' && at>=0) { e.preventDefault(); (links[at-1] || input).focus(); }
    else if(e.key==='Enter' && e.target===input) { e.preventDefault(); links[0]?.click(); }
  });
  document.addEventListener('keydown', e => {
    if(e.defaultPrevented || e.isComposing || e.altKey || e.shiftKey || !(e.metaKey || e.ctrlKey) || e.key.toLowerCase()!=='k' || matchMedia('(max-width:667px)').matches) return;
    if(e.target!==input && e.target.closest('input,textarea,select,[contenteditable]:not([contenteditable="false"])')) return;
    e.preventDefault(); input.focus();
  });
  // Delegated spotlight only (no tilt/translation), including newly generated rows.
  const motion=matchMedia('(hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference)');
  result.addEventListener('pointermove', e => {
    const link=e.target.closest('.search-result-link'); if(!link || !motion.matches) return;
    const r=link.getBoundingClientRect(); link.style.setProperty('--pointer-x',`${e.clientX-r.left}px`); link.style.setProperty('--pointer-y',`${e.clientY-r.top}px`);
  });
  addEventListener('pageshow', e => { if(e.persisted) { render(); load(); } });
  load(); // source site's eager/no persistent cache policy
})();
