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
  // A single native modal moves the active canvas; it does not duplicate renderers,
  // source data or listeners. Native modal focus containment/Escape remain intact.
  let dialog, modal;
  const makeDialog=()=>{
    if(dialog)return;
    dialog=document.createElement('dialog');dialog.className='diagram-dialog prose';
    const title=document.createElement('div');title.className='diagram-dialog-title';
    const close=document.createElement('button');close.type='button';close.className='diagram-action diagram-close';
    close.title=script.dataset.close;close.setAttribute('aria-label',script.dataset.close);
    const icon=document.createElement('span');icon.textContent='×';icon.setAttribute('aria-hidden','true');close.append(icon);
    close.addEventListener('click',()=>dialog.close());dialog.append(title,close);document.body.append(dialog);
    dialog.addEventListener('keydown',event=>{
      if(event.key!=='Tab')return;
      const items=[...dialog.querySelectorAll('button,a[href],[tabindex],summary')].filter(el=>!el.disabled&&el.tabIndex>=0&&el.getClientRects().length);
      const first=items[0],last=items.at(-1);
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
    });
    dialog.addEventListener('click',event=>{
      const r=dialog.getBoundingClientRect();
      if(event.target===dialog&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))dialog.close();
    });
    dialog.addEventListener('close',()=>{
      const current=modal;if(!current)return;modal=null;
      current.home.replaceChild(current.canvas,current.placeholder);
      document.documentElement.classList.remove('diagram-modal-open');
      current.canvas.style.filter='';dialog.removeAttribute('data-fixed-light');
      current.restore();current.opener.focus({preventScroll:true});
    });
  };
  const records=[];
  for (const figure of document.querySelectorAll('[data-sidera-diagram]')) {
    const view=figure.querySelector('.diagram-view'), status=figure.querySelector('.diagram-status');
    const canvas=figure.querySelector('.diagram-canvas'), details=figure.querySelector('.diagram-source');
    const source=details?details.querySelector('code').textContent:JSON.parse(figure.dataset.diagramSource);
    const tools=figure.querySelector('.diagram-tools');
    const image=new Image();image.alt=figure.dataset.diagramLabel;image.draggable=false;
    view.tabIndex=0;view.setAttribute('role','group');view.setAttribute('aria-label',image.alt);
    if(details){details.open=false;details.querySelector('summary').hidden=true;details.id='diagram-source-'+(++serial);tools.querySelector('[data-diagram-action="source"]').setAttribute('aria-controls',details.id);}
    let palette, blob, scale=1, revision=0, visible=false, hasRendered=false;
    const inModal=()=>modal?.figure===figure;
    const update = state => {
      figure.dataset.state=state;status.textContent=status.dataset[state];
      status.classList.toggle('visually-hidden',state!=='error');
    };
    const size = () => {
      if(!image.naturalWidth)return;
      const fit=inModal()?Math.min(view.clientWidth/image.naturalWidth,view.clientHeight/image.naturalHeight):Math.min(1,view.clientWidth/image.naturalWidth);
      image.style.width=Math.max(1,image.naturalWidth*fit*scale)+'px';
    };
    const modalPalette=()=>{
      if(!inModal())return;
      const filters=[];
      for(let el=figure;el;el=el.parentElement){
        if(el.matches('.invert-when-dark,.invert-when-light')){
          const filter=getComputedStyle(el).filter;if(filter!=='none')filters.push(filter);
        }
      }
      // Top-layer content no longer receives ancestor filters. Reapply only the
      // explicit author filters to this canvas, not to the whole modal or page.
      canvas.style.filter=filters.join(' ');
      dialog.toggleAttribute('data-fixed-light',!!figure.closest('.invert-when-dark,.invert-when-light'));
    };
    const refresh = async () => {
      if (!(visible||inModal()) || !view.parentElement.getBoundingClientRect().width) return;
      modalPalette();
      const explicit=figure.closest('.invert-when-dark,.invert-when-light');
      const next=explicit?'light':document.documentElement.dataset.colorScheme === 'dark'?'dark':'light';
      if (next===palette) {size();return;}
      palette=next;const current=++revision;update('loading');
      try {
        const svg=await service(figure.dataset.sideraDiagram).render(source,next);
        if(current!==revision)return;
        const url=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'}));image.src=url;
        try {await image.decode();} catch(error) {URL.revokeObjectURL(url);throw error;}
        if(current!==revision){URL.revokeObjectURL(url);return;}
        if(blob)URL.revokeObjectURL(blob);blob=url;
        view.replaceChildren(image);view.hidden=false;tools.hidden=false;
        for(const button of tools.querySelectorAll('button'))button.hidden=false;
        if(details){if(!hasRendered)details.open=false;details.querySelector('summary').hidden=true;tools.querySelector('[data-diagram-action="source"]').setAttribute('aria-expanded',String(details.open));}
        hasRendered=true;
        size();update('ready');
      } catch {
        if(current!==revision)return;
        view.hidden=true;
        for(const button of tools.querySelectorAll('button'))button.hidden=true;
        tools.hidden=!!details;
        if(details){details.open=true;details.querySelector('summary').hidden=false;}
        update('error');
      }
    };
    for(const button of tools.querySelectorAll('button')) button.addEventListener('click',()=>{
      switch(button.dataset.diagramAction){
        case 'in':scale=Math.min(8,scale*1.25);break;
        case 'out':scale=Math.max(.25,scale/1.25);break;
        case 'fit':scale=1;view.scrollTo(0,0);break;
        case 'source':details.open=!details.open;button.setAttribute('aria-expanded',String(details.open));break;
        case 'expand':{
          makeDialog();if(dialog.open)break;
          const previousScale=scale,left=view.scrollLeft,top=view.scrollTop,home=canvas.parentNode;
          const placeholder=document.createElement('div');placeholder.style.height=canvas.getBoundingClientRect().height+'px';placeholder.setAttribute('aria-hidden','true');
          modal={figure,canvas,opener:button,home,placeholder,restore:()=>{scale=previousScale;size();view.scrollTo(left,top);}};
          home.replaceChild(placeholder,canvas);
          dialog.setAttribute('aria-label',image.alt);dialog.querySelector('.diagram-dialog-title').textContent=image.alt;
          dialog.append(canvas);scale=1;modalPalette();dialog.showModal();document.documentElement.classList.add('diagram-modal-open');size();view.focus();break;
        }
      }
      size();
    });
    const resize=new ResizeObserver(()=>{if(visible||inModal())refresh();});resize.observe(figure);resize.observe(view);
    view.addEventListener('keydown',event=>{
      if(event.target!==view||event.altKey||event.ctrlKey||event.metaKey||event.shiftKey)return;
      const delta={ArrowLeft:[-40,0],ArrowRight:[40,0],ArrowUp:[0,-40],ArrowDown:[0,40]}[event.key];
      if(delta){event.preventDefault();view.scrollLeft+=delta[0];view.scrollTop+=delta[1];}
    });
    let drag;
    view.addEventListener('pointerdown',event=>{if(event.pointerType==='mouse'&&event.button===0){drag={x:event.clientX,y:event.clientY,left:view.scrollLeft,top:view.scrollTop};view.setPointerCapture(event.pointerId);}});
    view.addEventListener('pointermove',event=>{if(drag){view.scrollLeft=drag.left+drag.x-event.clientX;view.scrollTop=drag.top+drag.y-event.clientY;}});
    view.addEventListener('pointerup',()=>{drag=null;});view.addEventListener('lostpointercapture',()=>{drag=null;});
    const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)refresh();},{rootMargin:'200px'});
    observer.observe(figure);records.push(refresh);
  }
  new MutationObserver(()=>records.forEach(refresh=>refresh())).observe(document.documentElement,{attributes:true,attributeFilter:['data-color-scheme']});
})();
