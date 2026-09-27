// The user approved automatic native image loading. No API, polling, retries or
// stored counts. An image load proves delivery, not the provider's data accuracy.
(() => {
  for (const group of document.querySelectorAll('[data-sidera-badges]')) {
    const images=[...group.querySelectorAll('img')],status=group.querySelector('.badge-status');
    const done=new Set(),failed=new Set(),finishers=new Map();
    let timer;
    const update=()=>{
      const state=failed.size?'error':done.size===images.length?'ready':'loading';
      group.dataset.state=state;status.textContent=status.dataset[state];
      status.classList.toggle('visually-hidden',state!=='error');
      if(done.size===images.length)clearTimeout(timer);
    };
    for(const image of images){
      const finish=ok=>{done.add(image);if(ok)failed.delete(image);else failed.add(image);image.hidden=!ok;image.nextElementSibling.hidden=ok;update();};
      finishers.set(image,finish);
      image.addEventListener('load',()=>finish(true),{once:true});
      image.addEventListener('error',()=>finish(false),{once:true});
      if(image.complete)finish(image.naturalWidth>0);
    }
    update();
    const observer=new IntersectionObserver(entries=>{
      if(entries[0].isIntersecting){
        observer.disconnect();
        if(done.size!==images.length)timer=setTimeout(()=>{for(const [image,finish] of finishers)if(!done.has(image))finish(false);},15000);
      }
    });
    observer.observe(group);
  }
})();
