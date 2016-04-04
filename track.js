var margin = {top: 20, right: 20, bottom: 30, left: 100},
  width = 1300,
  height = 500 - margin.top - margin.bottom;

var formatDate = d3.time.format("%Y");

var x = d3.scale.linear()
    .range([0, width-margin.left-margin.right]);

var y = d3.scale.linear()
    .range([0, height-margin.top-margin.bottom]);

x.domain([1775, 2016]);
y.domain([0,10]);

var xAxis = d3.svg.axis()
    .scale(x)
    .tickFormat(function(t) { return t; })
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .tickValues([0,1,2,3,4,5,6,7,8,9,10])
    .tickFormat(function(t) {
      if(t === 0) return "President";
      if(t === 1) return "VP";
      if(t === 2) return "Party Leader";
      if(t === 3) return "Cabinet Member";
      if(t === 4) return "Governor";
      if(t === 5) return "Senator";
      if(t === 6) return "Congressman";
      if(t === 7) return "St. Cabinet";
      if(t === 8) return "St. Senate";
      if(t === 9) return "St. Representative";
      if(t === 10) return "Mayor";
    })
    .orient("left");

var line = d3.svg.line()
    .x(function(d) {
      return x(parseInt(d))+margin.left;
     })
    .y(function(d) { return y((offices[d]["level"]-10)*-1)+margin.top; })
    .interpolate("step-after");

var svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate("+margin.left+"," + (height-margin.bottom) + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate("+margin.left+","+margin.top+")")
    .call(yAxis)

var offices;

$.getJSON("presidents.json", function(data) {
  console.log(data);

  var c = d3.scale.category20();

  for(var i=0;i<data.length;i++) {
    var pres = data[i]["name"];
    offices = data[i]["track"];

    var presfound = -1;
    var d = Object.keys(offices).filter(function(t) {
      if(offices[t]["level"] === null) return false;
      var ret = presfound === -1;
      if(offices[t]["level"] === 10) presfound = t;
      return ret;
    });
    
    svg.append("path")
        .datum(d)
        .attr("class", "line")
        .attr("d", line)
        .attr("stroke", c(i%20))
        .attr("pres", pres)
        .on("mouseover", function() {
        });
    for(var j=0;j<d.length;j++) {
      svg.append("svg:circle")
        .attr("r", 3)
        .attr("fill", c(i%20)) 
        .attr("cx", x(parseInt(d[j]))+margin.left)
        .attr("cy", y((offices[d[j]]["level"]-10)*-1)+margin.top)
        .attr("pres", pres)
        .attr("office", offices[d[j]]["office"])
        .on("mouseover", function() {
          console.log(d3.select(this).attr("pres") + ": " + d3.select(this).attr("office"));
        });
    }


    svg.append("svg:text")
      .attr("x", x(presfound)+margin.left-10)
      .attr("y", margin.top + (i%2 === 1 ? 10 : -5))
      .text(pres.split(" ")[pres.split(" ").length-1]);
  

  }
});

