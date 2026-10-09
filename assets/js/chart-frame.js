// This is a live chart, never a host-page SVG injection. Only the owning parent
// on this resource's origin can initialize it. The sandbox has no networking,
// images, popups, forms, same-origin access or eval capability.
(() => {
  const element = document.getElementById('chart');
  const hostOrigin = new URL(location.href).origin;
  let chart, option, palette, reduced;
  const reply = message => parent.postMessage(message, hostOrigin);
  // Hover does not reliably cross an opaque frame boundary. Only forward the
  // pointer presence, never author HTML, to the owning chart's toolbar.
  document.documentElement.addEventListener('pointermove', () => reply({type: 'chart-pointer', inside: true}));
  document.documentElement.addEventListener('pointerleave', () => reply({type: 'chart-pointer', inside: false}));
  // Force rich-text tooltips at every option level. Strings remain strings;
  // there is no function revival, formatter compilation or source evaluation.
  function secure(value, depth = 0) {
    if (depth > 24) throw new Error('Too deeply nested');
    if (!value || typeof value !== 'object') return;
    if (Array.isArray(value)) {
      if (value.length > 10000) throw new Error('Too many items');
      value.forEach(item => secure(item, depth + 1)); return;
    }
    for (const key of Object.keys(value)) {
      if (['__proto__', 'constructor', 'prototype'].includes(key)) throw new Error('Unsafe key');
      if (key === 'source') continue; // Plain dataset values, never option objects.
      if (['link', 'sublink', 'image', 'graphic', 'toolbox', 'extraCssText', 'appendTo', 'appendToBody', 'className'].includes(key)) throw new Error('Unsupported capability');
      if (typeof value[key] === 'string' && value[key].startsWith('image://')) throw new Error('Images disabled');
      secure(value[key], depth + 1);
    }
    if (Object.hasOwn(value, 'tooltip')) {
      if (!value.tooltip || typeof value.tooltip !== 'object' || Array.isArray(value.tooltip)) throw new Error('Invalid tooltip');
      value.tooltip.renderMode = 'richText'; value.tooltip.confine = true;
    }
  }
  function motion() {
    const enabled = option.animation !== false && !reduced;
    chart.setOption({animation: enabled, series: option.series.map(series => ({
      animation: enabled && series.animation !== false,
      ...(series.markPoint ? {markPoint: {animation: enabled && series.markPoint.animation !== false}} : {}),
      ...(series.markLine ? {markLine: {animation: enabled && series.markLine.animation !== false}} : {}),
      ...(series.markArea ? {markArea: {animation: enabled && series.markArea.animation !== false}} : {})
    }))});
  }
  addEventListener('message', event => {
    if (event.source !== parent || event.origin !== hostOrigin) return;
    const message = event.data;
    try {
      if (message?.type === 'chart-init' && !chart) {
        if (typeof message.source !== 'string' || message.source.length > 1000000) throw new Error('Invalid source');
        option = JSON.parse(message.source);
        if (!option || Array.isArray(option) || !Array.isArray(option.series) || !option.series.length || option.series.length > 50) throw new Error('Invalid option');
        if (option.series.some(series => !['line', 'bar', 'pie', 'scatter'].includes(series.type))) throw new Error('Unsupported series');
        secure(option);
        palette = message.palette === 'dark' ? 'dark' : 'light'; reduced = !!message.reduced;
        const language = /^zh\b/i.test(message.language) ? 'ZH' : 'EN';
        document.documentElement.lang = language === 'ZH' ? 'zh-CN' : 'en';
        document.title = String(message.label);
        document.documentElement.style.colorScheme = palette;
        chart = echarts.init(element, palette === 'dark' ? 'dark' : {}, {renderer: 'svg', locale: language});
        const initial = JSON.parse(JSON.stringify(option));
        initial.backgroundColor ??= 'transparent';
        // Disable the first animation too, before the initial setOption call.
        if (reduced) {
          initial.animation = false;
          for (const series of initial.series) {
            series.animation = false;
            for (const key of ['markPoint', 'markLine', 'markArea']) if (series[key]) series[key].animation = false;
          }
        }
        initial.aria = {enabled: true, label: {description: String(message.label)}};
        chart.setOption(initial);
        new ResizeObserver(() => { if (element.clientWidth && element.clientHeight) chart.resize({animation: {duration: 0}}); }).observe(element);
        reply({type: 'chart-ready'});
      } else if (chart && message?.type === 'chart-environment') {
        const next = message.palette === 'dark' ? 'dark' : 'light';
        if (palette !== next) {
          palette = next; document.documentElement.style.colorScheme = palette;
          // setTheme recreates component models from authored options. Retain
          // reader selections rather than resetting them with the new palette.
          const current = chart.getOption();
          chart.setTheme(palette === 'dark' ? 'dark' : {});
          chart.setOption({...(current.legend ? {legend: current.legend} : {}),
            ...(current.dataZoom ? {dataZoom: current.dataZoom} : {})});
        }
        reduced = !!message.reduced; motion();
      }
    } catch {
      chart?.dispose(); chart = null; reply({type: 'chart-error'});
    }
  });
  if (window.echarts) reply({type: 'chart-frame-ready'});
  else reply({type: 'chart-error'});
})();
