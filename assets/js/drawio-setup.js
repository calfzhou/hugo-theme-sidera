// Disable all upstream hosted services/dynamic resource paths before the bundle.
// CSP independently denies networking, eval, frames, form submission and external images.
window.urlParams = Object.create(null);
for (const key of ['PROXY_URL','STYLE_PATH','SHAPES_PATH','STENCIL_PATH','DRAW_MATH_URL','GRAPH_IMAGE_PATH','mxImageBasePath','mxBasePath','DRAWIO_BASE_URL']) window[key] = 'about:blank';
window.mxLoadResources = false;
window.mxLoadStylesheets = false;
// The upstream viewer bootstraps MathJax even on math=0 documents. This explicit
// disabled sentinel prevents that unused service; math=1 inputs are rejected.
window.MathJax = Object.freeze({});
