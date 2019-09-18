var graph = {

pd2datajs: function(dt){
	var PlotData = [];
	for (var [f,gr] of Object.entries(dt)) {
		  var record = {};

		  record["key"] = f;
		  record["value"] = gr;
	      // console.log("color scale : "+colorScale(f))
		  PlotData.push(record);
		}
	return PlotData;
	},

traceHistogramme1: function(data,label_y,g,x,y,height,tooltip) {
	var colours = d3.scaleOrdinal()
    	.range(["#6F257F", "#CA0D59"]);
    x.domain(data.map(function(d) { return d.key; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    g.append("g")
      	.attr("class", "axis axis--y")
      	.call(d3.axisLeft(y).ticks(5).tickFormat(function(d) { return parseInt(d / 1000) + "K"; }).tickSizeInner([-width]))
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .attr("fill", "#5D6971")
        .text(label_y);

    g.selectAll(".bar")
      	.data(data)
      .enter().append("rect")
        .attr("x", function(d) { return x(d.key); })
        .attr("y", function(d) { return y(d.value); })
        .attr("width", x.bandwidth())
        .attr("height", function(d) { return height - y(d.value); })
        .attr("fill", function(d) { return colours(d.key); })
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html(d.value);
        })
    		.on("mouseout", function(d){ tooltip.style("display", "none");});
	},

traceHistogramme2: function(data,label_y,g,x,y,height,tooltip) {
  
  	// data.sort(function(a, b) { return a.value - b.value; });
  	var colours = d3.scaleOrdinal()
    	.range(["#6F257F", "#CA0D59"]);
  	x.domain([0, d3.max(data, function(d) { return d.value; })]);
    y.domain(data.map(function(d) { return d.key; })).padding(0.1);

    g.append("g")
        .attr("class", "x axis")
       	.attr("transform", "translate(0," + height + ")")
       	.call(d3.axisBottom(x).ticks(5).tickFormat(function(d) { return parseInt(d / 1000); }).tickSizeInner([-height]));

    g.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(y))
        .attr("fill", "#5D6971");

    g.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("height", y.bandwidth())
        .attr("y", function(d) { return y(d.key); })
        .attr("width", function(d) { return x(d.value); })
        .attr("fill", function(d) { return colours(d.key); })
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html((d.value));


        })
    		.on("mouseout", function(d){ tooltip.style("display", "none");});
},

scatterPlotZoom: function(data,elem_id,width,height,margin) {

  var svg = d3.select('#'+elem_id).append('svg')
    .attr('width', width + margin.right + margin.left)
    .attr('height', height + margin.top + margin.bottom)
    .attr('class', 'scatterchart'),

  width = 0.8*width;
  height = 0.8*height;
  var margin = {top: (0.1*width), right: (0.1*width), bottom: (0.1*width), left: (0.1*width)};

  // create a clipping region 
  svg.append("defs").append("clipPath")
      .attr("id", "clip")
    .append("rect")
      .attr("width", width)
      .attr("height", height);
  
  // create scale objects
  var xScale = d3.scaleTime()
    .domain(d3.extent(data,d=>d[1]))
    .range([0, width]);

  var yScale = d3.scaleLinear()
    .domain([0, d3.max(data,d=>d[0])])
    .range([height, 0]);
  // create axis objects
  var xAxis = d3.axisBottom(xScale)
    .tickFormat(d3.timeFormat("%Y-%m-%d"));

  var yAxis = d3.axisLeft(yScale);

  // Draw Axis
  var gX = svg.append('g')
    .attr('transform', 'translate(' + margin.left + ',' + (margin.top + height) + ')')
    .call(xAxis);

  var gY = svg.append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
    .call(yAxis);

  // Draw Datapoints
  var points_g = svg.append("g")
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
    .attr("clip-path", "url(#clip)")
    .classed("points_g", true);


  var points = points_g.selectAll("circle").data(data);
  points = points.enter().append("circle")
        .attr('cx', function(d) {return xScale(d[1])})
        .attr('cy', function(d) {return yScale(d[0])})
        .attr('fill-opacity', 0.6)
        .attr('r', 5);
        
  // Pan and zoom
  var zoom = d3.zoom()
      .scaleExtent([.5, 20])
      .extent([[0, 0], [width, height]])
      .on("zoom", zoomed);

  svg.append("rect")
      .attr("width", width)
      .attr("height", height)
      .style("fill", "none")
      .style("pointer-events", "all")
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
      .call(zoom);


  function zoomed() {
  // create new scale ojects based on event
      var new_xScale = d3.event.transform.rescaleX(xScale);
      var new_yScale = d3.event.transform.rescaleY(yScale);
  // update axes
      gX.call(xAxis.scale(new_xScale));
      gY.call(yAxis.scale(new_yScale));
      points.data(data)
       .attr('cx', function(d) {return new_xScale(d[1])})
       .attr('cy', function(d) {return new_yScale(d[0])})
       .attr('fill-opacity', 0.6);
  };
  
},

}