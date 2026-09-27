// Native viewer/exporter, isolated from the article DOM and network. One reusable
// graph avoids loading the 4 MB library or creating a viewer for every diagram.
(() => {
  const stage = document.getElementById('graph');
  let viewer, initialized=false;
  addEventListener('message', event => {
    if (event.source !== parent || event.data?.type !== 'render') return;
    const {request,source,palette} = event.data;
    try {
      if (!initialized) {
        if (!window.GraphViewer || !window.mxStencilRegistry) throw new Error('Viewer unavailable');
        mxStencil.allowEval=false;mxStencilRegistry.allowEval=false;mxStencilRegistry.dynamicLoading=false;
        mxStencilRegistry.parseStencilSets([document.getElementById('stencils').content.textContent]);
        initialized=true;
      }
      if (typeof source !== 'string' || source.length > 1000000 || /<!DOCTYPE|<!ENTITY/i.test(source)) throw new Error('Invalid source');
      const doc = new DOMParser().parseFromString(source,'application/xml');
      if (doc.querySelector('parsererror') || doc.documentElement.tagName !== 'mxfile' || doc.querySelectorAll('diagram').length !== 1 || doc.querySelectorAll('mxGraphModel').length !== 1) throw new Error('One uncompressed page required');
      const model = doc.querySelector('mxGraphModel');
      if (model.getAttribute('math') === '1' || model.hasAttribute('extFonts') || model.hasAttribute('backgroundImage') || model.querySelectorAll('mxCell').length > 2500) throw new Error('Unsupported model');
      // Guard pathological geometry before upstream layout; never evaluate custom
      // stencils or fetch images, fonts, links, math or external shape packages.
      for (const node of model.querySelectorAll('*')) {
        for (const key of ['x','y','width','height']) {
          if (node.hasAttribute(key) && (!Number.isFinite(Number(node.getAttribute(key))) || Math.abs(Number(node.getAttribute(key))) > 100000)) throw new Error('Invalid geometry');
        }
        const style = node.getAttribute('style') || '';
        if (/image\s*=|shape\s*=\s*stencil\(/i.test(style)) throw new Error('Unsupported image or stencil');
        const shape = /(?:^|;)shape=([^;]+)/.exec(style)?.[1];
        if (shape && !mxCellRenderer.defaultShapes[shape] && !mxStencilRegistry.stencils[shape]) throw new Error('Missing local shape');
      }
      if (!viewer) {
        viewer = new GraphViewer(stage,doc.documentElement,{toolbar:'',lightbox:false,nav:false,
          'browser-translate':false,'check-visible-state':false,'auto-fit':false,'resize':false,
          'dark-mode':palette,'show-note-icons':false,'show-link-icons':false,'show-tooltip-icons':false});
        viewer.graph.openLink = () => {};
      } else {
        viewer.darkMode = palette;
        viewer.darkModeChanged();
        viewer.setGraphXml(doc.documentElement);
      }
      const svg = viewer.graph.getSvg(palette === 'dark' ? '#1b1e22' : '#ffffff',1,8);
      // Links are not active in the published SVG image; strip them defensively.
      for (const link of svg.querySelectorAll('a')) link.replaceWith(...link.childNodes);
      parent.postMessage({type:'rendered',request,svg:new XMLSerializer().serializeToString(svg)}, '*');
    } catch {
      parent.postMessage({type:'rendered',request,error:true}, '*');
    }
  });
  parent.postMessage({type:'frame-ready'}, '*');
})();
