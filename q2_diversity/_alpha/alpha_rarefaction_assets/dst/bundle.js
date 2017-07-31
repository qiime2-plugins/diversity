webpackJsonp([0],[function(t,e,a){"use strict";function r(t){return t&&t.__esModule?t:{default:t}}var n=a(1),i=r(n);(0,i.default)()},function(t,e,a){"use strict";function r(){var t=metrics[0],e=categories[0],a=(0,n.select)("#main"),r=a.insert("div",":first-child").attr("class","viz row"),c=r.append("div").attr("class","col-lg-12"),o=c.append("div").attr("class","controls row"),l=c.append("div").attr("class","plot row"),u=l.append("div").attr("class","col-lg-12"),d=u.append("svg"),f=d.append("g");a.insert("h1",":first-child").text("Alpha Rarefaction"),f.append("g").attr("class","x axis"),f.append("g").attr("class","y axis"),f.append("text").attr("class","x label"),f.append("text").attr("class","y label"),i.state.initialize(t,e,o,d),(0,s.addMetricPicker)(o,metrics,t),categories.length>0&&(0,s.addCategoryPicker)(o,categories,e)}Object.defineProperty(e,"__esModule",{value:!0}),e.default=r;var n=a(2),i=a(3),s=a(6)},,function(t,e,a){"use strict";function r(t){return t&&t.__esModule?t:{default:t}}function n(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function i(t,e){var a="Sequencing Depth",r=e,n=1/0,i=0,s=1/0,c=0,o=t.columns.indexOf("depth"),l=t.columns.indexOf("min"),u=t.columns.indexOf("max");return t.data.forEach(function(t){var e=t[o];e<n&&(n=e),e>i&&(i=e),t[l]<s&&(s=t[l]),t[u]>c&&(c=t[u])}),{data:t,xAxisLabel:a,yAxisLabel:r,minX:n,maxX:i,minY:s,maxY:c}}function s(t,e,a,r){r.attr("href",t+".csv");var n=d[t];e&&(n=d[t][e]);var s=i(n,t);(0,l.default)(a,s)}Object.defineProperty(e,"__esModule",{value:!0}),e.state=void 0;var c=function(){function t(t,e){for(var a=0;a<e.length;a++){var r=e[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}return function(e,a,r){return a&&t(e.prototype,a),r&&t(e,r),e}}();e.default=i;var o=a(4),l=r(o),u=null,f=function(){function t(){return n(this,t),u||(u=this),this.category="",this.metric="",this.svg=null,this.href=null,u}return c(t,[{key:"initialize",value:function(t,e,a,r){var n=a.append("div").attr("class","col-lg-2 form-group downloadCSV");this.href=n.append("a").attr("href","").text("Download CSV"),this.svg=r,this.metric=t,this.category=e,s(t,e,this.svg,this.href)}},{key:"setCategory",value:function(t){this.category=t,s(this.metric,this.category,this.svg,this.href)}},{key:"setMetric",value:function(t){this.metric=t,s(this.metric,this.category,this.svg,this.href)}},{key:"getCategory",value:function(){return this.category}},{key:"getMetric",value:function(){return this.metric}}]),t}();e.state=new f},function(t,e,a){"use strict";function r(t,e,a,r){var n=t.select("g"),s=e.data.columns.indexOf("depth"),c=e.data.columns.indexOf("median"),o=e.data.columns.indexOf("sample-id");console.log(e);var l=[e.data.data.sort(function(t,e){return t[0]-e[0]})][0],u=Array.from(l,function(t){return t[0]}),d=new Set(u),f=(0,i.scaleOrdinal)(i.schemeCategory10).domain(d);n.selectAll("circle").remove(),n.selectAll("dot").data(l).enter().append("circle").attr("cx",function(t){return a(t[s])}).attr("cy",function(t){return r(t[c])}).attr("r",4).style("stroke",function(t){return f(t[o])})}function n(t,e){var a=400,n=1e3,c={top:20,left:70,right:50,bottom:50},o=t.select("g"),l=e.xAxisLabel,u=e.yAxisLabel,d=e.minX,f=e.maxX,p=e.minY,h=e.maxY,m=(0,i.axisBottom)(),v=(0,i.axisLeft)(),g=.03*(f-d);if(Number.isInteger(d)&&Number.isInteger(f)){g=Math.max(Math.round(g),1);var x=Math.max(3,f-d+2*g);m.ticks(Math.min(x,12),"d")}var y=(0,i.scaleLinear)().domain([d-g,f+g]).range([0,n]).nice(),b=(0,i.scaleLinear)().domain([p,h]).range([a,0]).nice();m.scale(y),v.scale(b),o.attr("transform","translate("+c.left+","+c.top+")"),(0,s.setupXLabel)(t,n,a,l,m),(0,s.setupYLabel)(t,a,u,v),r(t,e,y,b),t.attr("width",n+c.left+c.right).attr("height",a+c.bottom+c.top)}Object.defineProperty(e,"__esModule",{value:!0}),e.default=n;var i=a(2),s=a(5)},function(t,e){"use strict";function a(t,e,a,r,n){t.select(".x.axis").attr("transform","translate(0,"+a+")").call(n),t.select(".x.label").attr("text-anchor","middle").style("font","12px sans-serif").attr("transform","translate("+e/2+","+(a+40)+")").text(r)}function r(t,e,a,r){t.select(".y.axis").call(r),t.select(".y.label").attr("text-anchor","middle").style("font","12px sans-serif").attr("transform","translate(-50,"+e/2+")rotate(-90)").text(a)}Object.defineProperty(e,"__esModule",{value:!0}),e.setupXLabel=a,e.setupYLabel=r},function(t,e,a){"use strict";function r(t,e,a){var r=t.append("div").attr("class","col-lg-2 form-group metricPicker");return r.append("label").text("Metric"),r.append("select").attr("class","form-control").on("change",function(){var t=e[this.selectedIndex];i.state.setMetric(t)}).selectAll("option").data(e).enter().append("option").attr("value",function(t){return t}).text(function(t){return t}).property("selected",function(t){return t===a}),r}function n(t,e,a){var r=t.append("div").attr("class","col-lg-2 form-group categoryPicker");return r.append("label").text("Category"),r.append("select").attr("class","form-control").on("change",function(){var t=e[this.selectedIndex];i.state.setCategory(t)}).selectAll("option").data(e).enter().append("option").attr("value",function(t){return t}).text(function(t){return t}).property("selected",function(t){return t===a}),r}Object.defineProperty(e,"__esModule",{value:!0}),e.addMetricPicker=r,e.addCategoryPicker=n;var i=a(3)}]);