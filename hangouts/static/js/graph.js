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
}
}