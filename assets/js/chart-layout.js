// Bounded native-layout adapter for the pinned ECharts runtime. Measure its own
// component views rather than guessing legend rows from strings or font sizes.
function sideraChartLayout(chart, option) {
  const list = value => value == null ? [] : Array.isArray(value) ? value : [value];
  const grids = list(option.grid), xs = list(option.xAxis), ys = list(option.yAxis);
  const titles = list(option.title), legends = list(option.legend);
  const grid = grids[0] || {};
  if (grids.length > 1 || xs.length !== 1 || ys.length !== 1 || titles.length > 1 || legends.length > 1 ||
      list(option.dataZoom).length || option.series.some(series => !['line', 'bar', 'scatter'].includes(series.type)) ||
      ['top', 'bottom', 'height', 'y', 'y2', 'containLabel', 'outerBounds', 'outerBoundsMode'].some(key => Object.hasOwn(grid, key)) ||
      legends.some(legend => legend.orient === 'vertical')) return () => {};

  const model = chart.getModel();
  const initialGrid = model.getComponent('grid');
  if (!initialGrid) return () => {};
  const original = {top: initialGrid.get('top'), bottom: initialGrid.get('bottom')};
  // Only ordinary edge-anchored components; centered/custom coordinate placement
  // and explicit grid geometry remain ECharts/author-controlled.
  const edge = component => {
    const top = component.get('top'), bottom = component.get('bottom');
    const offset = value => typeof value === 'number' || (typeof value === 'string' && /^\d+(?:\.\d+)?%?$/.test(value));
    if (top === 'top' || offset(top)) return 'top';
    if (bottom === 'bottom' || offset(bottom)) return 'bottom';
    return null;
  };
  const components = [];
  for (const type of ['title', 'legend']) {
    const component = model.getComponent(type);
    if (!component || component.get('show') === false) continue;
    if (type === 'title' && !component.get('text') && !component.get('subtext')) continue;
    const side = edge(component);
    if (!side) return () => {};
    components.push({type, side});
  }
  const bounds = component => {
    const group = chart.getViewOfComponentModel(component).group;
    const rect = group.getBoundingRect().clone();
    rect.applyTransform(group.getLocalTransform());
    return rect;
  };
  const resize = () => chart.resize({
    // The DOM renderer must keep auto-sizing; explicit pixels would pin its next
    // resize to the old width. SSR geometry checks have no container to measure.
    ...(chart.isSSR() ? {width: chart.getWidth(), height: chart.getHeight()} : {}),
    animation: {duration: 0, delay: 0}, silent: true});
  const apply = margins => {
    // Queue the option change without an animated setOption render. ECharts'
    // resize consumes that pending update with a zero-duration animation payload.
    // Never measure a view partway between its old and new grid positions.
    chart.setOption({grid: margins}, {silent: true, lazyUpdate: true});
    resize();
  };
  return (afterResize = false) => {
    if (!afterResize) resize();
    // Two bounded passes accommodate axis-label geometry after the first reflow.
    // Never run from 'rendered'/'finished': setOption would feed back into itself.
    for (let pass = 0; pass < 2; pass++) {
      const current = chart.getModel(), plot = current.getComponent('grid').coordinateSystem.getRect();
      let top = 16, bottom = chart.getHeight() - 16;
      for (const {type, side} of components) {
        const rect = bounds(current.getComponent(type));
        if (side === 'top') top = Math.max(top, rect.y + rect.height + 12);
        else bottom = Math.min(bottom, rect.y - 12);
      }
      let above = 0, below = 0;
      for (const type of ['xAxis', 'yAxis']) {
        const axis = current.getComponent(type);
        if (axis.get('show') === false) continue;
        const rect = bounds(axis);
        above = Math.max(above, plot.y - rect.y);
        below = Math.max(below, rect.y + rect.height - plot.y - plot.height);
      }
      const margins = {top: Math.ceil(top + above), bottom: Math.ceil(chart.getHeight() - bottom + below)};
      // Don't collapse a tiny chart to nothing if its labels consume the canvas.
      // Keep the authored/default layout; users can increase the chart height.
      if (!Number.isFinite(margins.top + margins.bottom) || margins.top + margins.bottom > chart.getHeight() - 80) {
        apply(original);
        return;
      }
      const actual = current.getComponent('grid');
      if (actual.get('top') === margins.top && actual.get('bottom') === margins.bottom) return;
      apply(margins);
    }
  };
}
