// Register before the bundle's own load listener: only explicit frame requests render.
addEventListener('load', () => {
  const api=window.mermaid?.default || window.mermaid;
  if(api)api.startOnLoad=false;
}, {once:true});
