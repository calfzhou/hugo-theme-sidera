// Two lazy local sandbox services at most, one per renderer. Render sequentially;
// display inert SVG images, not vendor HTML or interactive code in the article DOM.
(() => {
  const script = document.querySelector('[data-sidera-diagrams-script]');
  const services = new Map();
  let serial = 0;
  function service(kind) {
    if (services.has(kind)) return services.get(kind);
    const frame = document.createElement('iframe');
    frame.sandbox = 'allow-scripts';
    frame.setAttribute('aria-hidden','true');frame.tabIndex = -1;
    frame.className = 'diagram-renderer';
    let pending;
    const ready = new Promise((resolve,reject) => {
      const timer = setTimeout(()=>reject(new Error('Renderer unavailable')),15000);
      addEventListener('message', event => {
        if (event.source !== frame.contentWindow || event.origin !== 'null') return;
        if (event.data?.type === 'frame-ready') {clearTimeout(timer);resolve();}
        if (pending && event.data?.type === 'rendered' && event.data.request === pending.request) {
          clearTimeout(pending.timer);
          const {resolve,reject} = pending;pending = null;
          if (event.data.error || typeof event.data.svg !== 'string' || event.data.svg.length > 10000000) reject(new Error('Rendering failed'));
          else resolve(event.data.svg);
        }
      });
    });
    let chain = ready;
    const render = (source,palette) => {
      const task = chain.then(()=>new Promise((resolve,reject)=>{
        const request = ++serial;
        const timer = setTimeout(()=>{pending=null;reject(new Error('Rendering timed out'));},15000);
        pending = {request,timer,resolve,reject};
        frame.contentWindow.postMessage({type:'render',request,source,palette},'*');
      }));
      // A parse failure must not poison later diagrams. No retry of the failed input.
      chain = task.catch(()=>{});
      return task;
    };
    frame.src = script.dataset[kind];document.body.append(frame);
    const api = {render};services.set(kind,api);return api;
  }
  const records=[];
  for (const figure of document.querySelectorAll('[data-sidera-diagram]')) {
    const view=figure.querySelector('.diagram-view'), status=figure.querySelector('.diagram-status');
    const source=figure.querySelector('.diagram-source code').textContent;
    const details=figure.querySelector('.diagram-source'), tools=figure.querySelector('.diagram-tools');
    const image=new Image();image.alt=figure.querySelector('figcaption').textContent;image.draggable=false;
    view.tabIndex=0;view.setAttribute('role','group');view.setAttribute('aria-label',image.alt);
    let palette, blob, scale=1, revision=0, visible=false;
    const update = state => {figure.dataset.state=state;status.textContent=status.dataset[state];};
    const size = () => {image.style.width=Math.max(1,Math.min(view.clientWidth,image.naturalWidth)*scale)+'px';};
    const refresh = async () => {
      if (!visible || !figure.getBoundingClientRect().width) return;
      const explicit=figure.closest('.invert-when-dark,.invert-when-light');
      const next=explicit?'light':document.documentElement.dataset.colorScheme === 'dark'?'dark':'light';
      if (next===palette) {size();return;}
      palette=next;view.style.backgroundColor=next==='dark'?'#1b1e22':'#ffffff';const current=++revision;update('loading');
      try {
        const svg=await service(figure.dataset.sideraDiagram).render(source,next);
        if(current!==revision)return;
        const url=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'}));
        image.src=url;
        try {await image.decode();} catch(error) {URL.revokeObjectURL(url);throw error;}
        if(current!==revision){URL.revokeObjectURL(url);return;}
        if(blob)URL.revokeObjectURL(blob);blob=url;
        view.replaceChildren(image);view.hidden=false;tools.hidden=false;details.open=false;
        size();update('ready');
      } catch {
        if(current!==revision)return;
        view.hidden=true;tools.hidden=true;details.open=true;update('error');
      }
    };
    for(const button of tools.querySelectorAll('button')) button.addEventListener('click',()=>{
      switch(button.dataset.diagramAction){
        case 'in':scale=Math.min(8,scale*1.25);break;
        case 'out':scale=Math.max(.25,scale/1.25);break;
        case 'fit':scale=1;view.scrollTo(0,0);break;
        case 'expand':button.setAttribute('aria-pressed',String(figure.classList.toggle('is-expanded')));break;
      }
      size();
    });
    new ResizeObserver(()=>{if(visible)refresh();}).observe(figure);
    // Native scrolling supports touch/keyboard; pointer drag is a convenience.
    let drag;
    view.addEventListener('pointerdown',event=>{if(event.pointerType==='mouse'&&event.button===0){drag={x:event.clientX,y:event.clientY,left:view.scrollLeft,top:view.scrollTop};view.setPointerCapture(event.pointerId);}});
    view.addEventListener('pointermove',event=>{if(drag){view.scrollLeft=drag.left+drag.x-event.clientX;view.scrollTop=drag.top+drag.y-event.clientY;}});
    view.addEventListener('pointerup',()=>{drag=null;});view.addEventListener('lostpointercapture',()=>{drag=null;});
    const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)refresh();},{rootMargin:'200px'});
    observer.observe(figure);records.push(refresh);
  }
  new MutationObserver(()=>records.forEach(refresh=>refresh())).observe(document.documentElement,{attributes:true,attributeFilter:['data-color-scheme']});
})();
