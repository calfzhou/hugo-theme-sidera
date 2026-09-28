/* Local text model shared by result matching and destination highlighting.
 * Stellar 1.44 search journey informed the UI; see THIRD-PARTY-NOTICES.md.
 * No query regex, HTML interpretation, stemming, network or persistent storage. */
const SideraSearch = (() => {
  const whitespace = /[\t\n\f\r \u00a0]/u;
  const normalize = text => text.replace(/[\t\n\f\r \u00a0]+/g, ' ').trim();
  const folded = text => text.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
  function fold(text) {
    let value = ''; const starts = [], ends = [];
    let offset = 0;
    for (const char of text) {
      const part = folded(char);
      if (!part && ends.length) ends[ends.length - 1] = offset + char.length;
      for (let i = 0; i < part.length; i++) { starts.push(offset); ends.push(offset + char.length); }
      value += part; offset += char.length;
    }
    return {value, starts, ends};
  }
  const tokens = query => [...new Set(normalize(query.slice(0, 160)).split(' ').map(folded).filter(Boolean))].slice(0, 8);
  function matches(text, words, limit = 100) {
    const f = fold(text), found = [];
    for (const word of words) {
      let at = 0, n = 0;
      while (word && n++ < limit && (at = f.value.indexOf(word, at)) !== -1) {
        found.push([f.starts[at], f.ends[at + word.length - 1]]); at += word.length;
      }
    }
    found.sort((a,b) => a[0]-b[0] || b[1]-a[1]);
    const ranges = [];
    for (const r of found) {
      const last = ranges.at(-1);
      if (last && r[0] <= last[1]) last[1] = Math.max(last[1], r[1]); else ranges.push(r);
    }
    return ranges.slice(0, limit);
  }
  function search(documents, query, scope) {
    const words = tokens(query); if (!words.length) return [];
    const hits = [];
    for (const doc of documents) {
      if (scope && doc.scope !== scope) continue;
      const title = folded(doc.title); let hasBody = false, offset = 0;
      for (const section of doc.sections) {
        const text = folded(section.text), heading = folded(section.title);
        // All tokens must occur in this section or its page title; at least one in body.
        if (words.every(w => text.includes(w) || title.includes(w)) && words.some(w => text.includes(w))) {
          const ranges = matches(section.text, words);
          const rank = words.reduce((n,w) => n + (title.includes(w) ? 8 : 0) + (heading.includes(w) ? 5 : 0) + (text.includes(w) ? 1 : 0), 0);
          hits.push({doc, section, rank, offset, ranges}); hasBody = true;
        }
        offset += section.text.length + 1;
      }
      if (!hasBody && words.every(w => title.includes(w))) hits.push({doc, section: null, rank: 8 * words.length, offset: 0, ranges: []});
    }
    return hits.sort((a,b) => b.rank-a.rank || (a.doc.url < b.doc.url ? -1 : a.doc.url > b.doc.url ? 1 : a.offset-b.offset)).slice(0,40);
  }
  // DOM traversal follows discovery/text.html's block and subtree rules. Positions
  // map normalized UTF-16 offsets back to actual Text nodes, including inline spans.
  function bodySections(root, rules) {
    const sections = []; let id = '', title = '', raw = '', positions = [], heading = false;
    const add = (text, node = null) => {
      for (let i=0; i<text.length; i++) { positions.push(node ? {node, offset:i} : null); }
      raw += text; if (heading) title += text;
    };
    const finish = () => {
      let text = '', map = [], pending = null;
      for (let i=0; i<raw.length; i++) {
        if (whitespace.test(raw[i])) { if (text && pending === null) pending = i; }
        else {
          if (pending !== null) { text += ' '; map.push(positions[pending]); pending = null; }
          text += raw[i]; map.push(positions[i]);
        }
      }
      sections.push({id, title:normalize(title), text, map}); raw=''; positions=[]; title='';
    };
    function walk(node) {
      if (node.nodeType === 3) { add(node.nodeValue, node); return; }
      if (node.nodeType !== 1) return;
      const tag = node.localName;
      if ((tag === 'figcaption' && node.closest('.no-caption')) || rules.skipTags.includes(tag) || rules.skipClasses.some(c => node.classList.contains(c)) || node.hidden || node.getAttribute('aria-hidden') === 'true' || node.hasAttribute('data-search-exclude')) return;
      const isHeading = /^h[1-6]$/.test(tag);
      if (isHeading) { finish(); id = node.id; heading = true; }
      if (rules.blocks.includes(tag)) add('\n');
      for (const child of node.childNodes) walk(child);
      if (isHeading) heading = false;
      if (rules.blocks.includes(tag)) add('\n');
    }
    for (const child of root.childNodes) walk(child);
    finish(); return sections;
  }
  return {normalize, tokens, matches, search, bodySections};
})();
