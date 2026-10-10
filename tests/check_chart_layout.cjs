// Pinned renderer geometry tests, no DOM/network/install or output artifacts.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const echarts = require(path.join(root, 'assets/vendor/echarts-6.1.0/echarts.common.min.js'));
vm.runInThisContext(fs.readFileSync(path.join(root, 'assets/js/chart-layout.js'), 'utf8'));
const base = {animation: false, legend: {}, xAxis: {type: 'category', data: Array.from({length: 10}, (_, i) => `i=${i + 1}`)},
  yAxis: {}, series: Array.from({length: 10}, (_, i) => ({name: `m=${i + 1}`, type: 'line', data: Array.from({length: 10}, (_, j) => (i + j) / 20)}))};
function bounds(chart, type) {
  const group = chart.getViewOfComponentModel(chart.getModel().getComponent(type)).group;
  const rect = group.getBoundingRect().clone(); rect.applyTransform(group.getLocalTransform()); return rect;
}
for (const extra of [{}, {title: {text: 'Ten series'}}, {title: {show: false}}, {legend: {top: 0}},
  {legend: {type: 'scroll'}}, {xAxis: {...base.xAxis, axisLabel: {rotate: 30}}},
  {yAxis: {name: 'Probability'}}, {xAxis: {...base.xAxis, show: false}}]) {
  const option = {...base, ...extra};
  const chart = echarts.init(null, {}, {renderer: 'svg', ssr: true, width: 640, height: 360});
  chart.setOption(option);
  const fit = sideraChartLayout(chart, option);
  const results = [];
  for (const width of [640, 320, 390, 640]) {
    chart.resize({width, height: 360, animation: {duration: 0, delay: 0}}); fit(true);
    const grid = chart.getModel().getComponent('grid'), plot = grid.coordinateSystem.getRect();
    assert(Number.isFinite(plot.height) && plot.height >= 80);
    const legend = bounds(chart, 'legend');
    if (extra.legend?.top === 0) assert(plot.y >= legend.y + legend.height + 11);
    else if (option.xAxis.show !== false) {
      const axis = bounds(chart, 'xAxis');
      assert(axis.y + axis.height <= legend.y - 11, JSON.stringify({extra, width, axis, legend}));
    }
    if (extra.title?.text) {
      const title = bounds(chart, 'title');
      assert(plot.y >= title.y + title.height + 11);
    }
    const before = JSON.stringify(chart.getOption().grid); fit();
    assert.equal(JSON.stringify(chart.getOption().grid), before, 'Layout must settle');
    results.push({top: grid.get('top'), bottom: grid.get('bottom')});
  }
  assert.deepEqual(results[0], results[3], 'Wide-to-narrow-to-wide must not accumulate padding');
  chart.dispatchAction({type: 'legendUnSelect', name: 'm=1'}); fit();
  assert.equal(chart.getOption().legend[0].selected['m=1'], false);
  chart.dispose();
}
for (const extra of [{grid: {top: 0, bottom: 45}}, {grid: {height: '65%'}}, {grid: [{}, {}]},
  {legend: {orient: 'vertical'}}, {dataZoom: [{type: 'slider'}]}, {yAxis: [{}, {}]},
  {title: [{text: 'First'}, {text: 'Second'}]}, {grid: {containLabel: true}}]) {
  const option = {...base, ...extra};
  const chart = echarts.init(null, {}, {renderer: 'svg', ssr: true, width: 500, height: 360}); chart.setOption(option);
  const before = JSON.stringify(chart.getOption().grid); sideraChartLayout(chart, option)();
  assert.equal(JSON.stringify(chart.getOption().grid), before, 'Explicit/complex geometry must be preserved'); chart.dispose();
}
console.log('PASS adaptive chart layout: wrapping/top/scroll legends, title/no title, names/rotated/hidden axes, resize stability, selections and explicit/complex opt-out');
