// Single opaque sandbox per page, reused serially. No author config/JS or unused
// diagram grammars. Result is displayed as an inert SVG image, never host innerHTML.
(() => {
  const graph = document.getElementById('graph');
  addEventListener('message', async event => {
    if (event.source !== parent || event.data?.type !== 'render') return;
    const {request, source, palette} = event.data;
    try {
      if (typeof source !== 'string' || source.length > 50000 || /%%\s*\{|^\s*---/.test(source) || !/^\s*(?:(?:%%[^\n]*\n)\s*)*(?:flowchart\b|graph\b|gitGraph\s*:)/.test(source)) throw new Error('Unsupported source');
      const api = window.mermaid.default || window.mermaid;
      api.initialize({startOnLoad:false, securityLevel:'strict', suppressErrorRendering:true,
        maxTextSize:50000, maxEdges:500, theme:palette === 'dark' ? 'dark' : 'neutral',
        // Mermaid 11.17 uses root htmlLabels; the deprecated flowchart setting alone
        // leaves HTML labels enabled in some renderers. Native SVG text keeps the
        // result XML-valid (including multiline labels) for inert img decoding.
        htmlLabels:false, fontFamily:'Arial, sans-serif', flowchart:{useMaxWidth:false, curve:'linear'},
        secure:['securityLevel','startOnLoad','maxTextSize','maxEdges','themeCSS','htmlLabels','fontFamily','altFontFamily','themeVariables','flowchart']});
      graph.replaceChildren();
      const {svg} = await api.render('diagram', source, graph);
      parent.postMessage({type:'rendered',request,svg}, '*');
    } catch {
      parent.postMessage({type:'rendered',request,error:true}, '*');
    } finally { graph.replaceChildren(); }
  });
  parent.postMessage({type:'frame-ready'}, '*');
})();
