var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var format = d3.format(",d");

var color = function(type) {
  switch (type) {
    case 'Federal':
      out = '#618e36';
      break;
    case 'State':
      out = '#a7b638';
      break;
    case 'Regional':
      out = '#365872';
      break;
    case 'City':
      out = '#f09006';
      break;
    case 'County':
      out = '#da453f';
      break;
    default:
      out = '#5b5e5e';
      break;
  }
    return out
}


var pack = d3.pack()
    .size([width, height])
    .padding(1.5);


var root = d3.hierarchy({children: rows})
    .sum(function(d) { return d.value; })
    .each(function(d) {
      if (id = d.data.id) {
        d.id = id;
        d.title = d.data.title;
        d.class = d.data.title;
        d.package = d.data.package;
        d.url = d.data.url;
      }
    });

var tooltip = d3.select("body")
  .append("div")
  .attr('id', 'bubble-tooltip')
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("color", "white")
  .style("padding", "8px")
  .style("background-color", "#626D71")
  .style("border-radius", "6px")
  .style("text-align", "center")
  .style("width", "200px")
  .text("");

var node = svg.selectAll(".node")
  .data(pack(root).leaves())
  .enter().append("g")
    .attr("class", "node")
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    .on("mouseover", function(d){
      tooltip.html(d.title + ' ('+d.value+')');
      return tooltip.style("visibility", "visible");})
    .on("mousemove", function(){
      return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
    .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

node.append("circle")
    .attr("id", function(d) { return d.id; })
    .attr("r", function(d) { return d.r; })
    .style("fill", function(d) { return color(d.package); });

node.append("clipPath")
    .attr("id", function(d) { return "clip-" + d.id; })
  .append("use")
    .attr("xlink:href", function(d) { return "#" + d.id; });

//TODO make anchor tag to d.url ('#' is fine otherwise)
node.append("a").attr("href", function(d) { return d.url || '#' })
  .append("text")
    .attr('dominant-baseline', 'central')
    .attr("clip-path", function(d) { return "url(#clip-" + d.id + ")"; })
  .selectAll("tspan")
  .data(function(d) { return d.title.split(/(?=[A-Z][^A-Z])/g); })
  .enter().append("tspan")
    .attr('alignment-baseline', 'central')
    .attr("x", 0)
    .attr("y", function(d, i, nodes) {
        var fontSize = 16;
        var padding = 2;
        var fontFullSize = fontSize + padding;
        var maxHeight = (nodes.length * fontFullSize) - fontFullSize;
        var topLine = (maxHeight / 2) * -1;
        var thisLine = topLine + (i * fontFullSize);
        return thisLine;
      }
    )
    .text(function(d) { return d; });

node.append("title")
      .text(function(d) { return d.title + "\n" + format(d.value); });

node.selectAll("g > a > text")
  .style("opacity", function(d) {
    var box = this.getBoundingClientRect();
    var width = d.r * 2;
    var height = d.r * 2;
    if(box.width <= width && box.height <= height) {
      return 1; // fits, show the text
    } else {
      return 0; // does not fit, make transparent
    }
  });


//Build up Legend Data
var legendData = {};
for (i = 0; i < rows.length; i++) {
    var rowPackage = rows[i].package;
    if (rowPackage == "") {
        rowPackage = "Uncategorized";
    }

    if (rowPackage in legendData) {
      legendData[rowPackage]['count']++;
    } else {
      var rowColor = color(rowPackage);
      legendData[rowPackage] = {
        "color": rowColor,
        "text": rowPackage,
        "count": 1
      };
    }
}

var legendRectSize = 18;
var legendSpacing = 4;
//Add Legend, convert data to array
legendDataArray = Object.keys(legendData).map(function (key) { return legendData[key]; });

var legendWrapper = svg
  .append('g')
  .attr('class', 'legend-wrapper')
  .attr('transform', function() {
    var svgBox = svg.node().getBBox();
    var publisherTab = jQuery('.container');
    // console.log(publisherTab.width());
    return 'translate(' + (publisherTab.width() - 250) + ', 150)';
  });

var legendBackground = legendWrapper
  .append('rect')
  .attr('class', 'legend-background');

var legend = legendWrapper.selectAll('.legend')
  .data(legendDataArray)
  .enter()
  .append('g')
  .attr('class', 'legend')
  .attr('transform', function(d, i) {
    var height = legendRectSize + legendSpacing;
    var offset =  height * legendDataArray.length / 2;
    var horz = -2 * legendRectSize;
    var vert = i * height - offset;
    return 'translate(' + horz + ',' + vert + ')';
  });

legend.append('rect')
  .attr('width', legendRectSize)
  .attr('height', legendRectSize)
  .style('fill', function(d) { return d.color; });

legend.append('text')
  .attr('x', legendRectSize + legendSpacing)
  .attr('y', legendRectSize - legendSpacing)
  .attr('text-anchor', 'start')
  .text(function(d) { return d.text; });

legendBackground
  .attr('width', function() {
    var legendBox = d3.select('.legend-wrapper').node().getBBox();
    return legendBox.width + 20;
  })
  .attr('height', function() {
    var legendBox = d3.select('.legend-wrapper').node().getBBox();
    return legendBox.height + 20;
  })
  .attr('transform', function(d, i) {
    var legendBox = d3.select('.legend-wrapper').node().getBBox();
    var horz = legendBox.x;
    var vert = legendBox.y;
    return 'translate(' + (horz - 10) + ',' + (vert - 10) + ')';
  })
  .style('fill', '#FFFFFF')
  .style("stroke", '#b2d4dc')
  .style("stroke-width", 1);

//// Draw rects, and color them by original_index
//legend.append("rect")
//    .attr("width", 8)
//    .attr("height", 8)
//    .style("fill", function(d){return color(d.original_index)});
//
//legend.append("text")
//    .attr("x", function(d,i){ return d.depth*10 +10;})
//    .attr("dy", "0.50em")
//    .text(function(d){return d.title;})

