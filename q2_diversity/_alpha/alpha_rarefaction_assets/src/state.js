/* global d */
import { setupData } from './data';
import render from './render';

function updateData(metric, category, svg, href, legend, legendTitle) {
  href.attr('href', `${metric}.csv`);
  let data = d[metric];
  if (category) {
    data = d[metric][category];
  }
  const preppedData = setupData(data, metric);
  render(svg, preppedData, category, legend, legendTitle);
}

class State {
  constructor() {
    this.category = '';
    this.metric = '';
    this.svg = null;
    this.href = null;
    this.legend = null;
    this.legendTitle = null;
  }
  initialize(metric, category, row, svg, legend, legendTitle) {
    this.href = row.select('.downloadCSV a');
    this.svg = svg;
    this.metric = metric;
    this.category = category;
    this.legend = legend;
    this.legendTitle = legendTitle;
    updateData(metric, category, this.svg, this.href, this.legend, this.legendTitle);
  }
  setCategory(c) {
    this.category = c;
    updateData(this.metric, this.category, this.svg, this.href, this.legend, this.legendTitle);
  }
  setMetric(m) {
    this.metric = m;
    updateData(this.metric, this.category, this.svg, this.href, this.legend, this.legendTitle);
  }
  getCategory() {
    return this.category;
  }
  getMetric() {
    return this.metric;
  }
  getSvg() {
    return this.svg;
  }
}
const state = new State();
export { state as default };
