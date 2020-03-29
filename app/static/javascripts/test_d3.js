function test1() {
    data = [
        { type: "rice", count: 1 },
        { type: "vegetable", count: 1 },
        { type: "meat", count: 2 }
    ]

    var svg = d3.select("svg"),
        width = svg.attr("width"),
        height = svg.attr("height"),
        radius = Math.min(width, height) / 2;

    var g = svg.append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var color = ['#ff0000', '#00ff00', '#0000ff']

    var pie = d3.pie().value(d => d.count)

    var path = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var label = d3.arc()
        .outerRadius(radius)
        .innerRadius(radius - 80);

    var arc = g.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");

    arc.append("path")
        .attr("d", path)
        .attr("fill", function (d, i) { return color[i]; });

    console.log(arc)

    arc.append("text")
        .attr("transform", function (d) {
            return "translate(" + label.centroid(d) + ")";
        })
        .text(function (d) { return d.data.type; });


    svg.append("g")
        .attr("transform", "translate(" + (width / 2 - 120) + "," + 20 + ")")
        .append("text")
        .text("Browser use statistics - Jan 2017")
        .attr("class", "title")
}

function test2(){
    series = [
        { name: 'a1', count: [100, 200, 400] },
        { name: 'a2', count: [200, 300, 500] },
        { name: 'a3', count: [50, 60, 200] }
    ]

    margin = { top: 30, right: 10, bottom: 0, left: 30 }
    height = series.length * 25 + margin.top + margin.bottom
    width = 500

    x = d3.scaleLinear()
        .domain([0, d3.max(series, d => d3.sum(d.count))])
        .range([margin.left, width - margin.right])

    y = d3.scaleBand()
        .domain(series.map(d => d.name))
        .range([margin.top, height - margin.bottom])
        .padding(0.08)

    xAxis = g => g
        .attr("transform", `translate(0,${margin.top})`)
        .call(d3.axisTop(x).ticks(width / 100))

    yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).tickSizeOuter(0))

    color = d3.scaleOrdinal()
        .domain([0,1,2])
        .range(d3.schemeSpectral[series.length])
        .unknown("#ccc")

    const svg = d3.select("svg")
        .attr("viewBox", [0, 0, width, height]);

    svg
        .selectAll("g")
        .data(series)
        .join("g")
        .selectAll("g")
        .data(d => {
            dd = [];
            for (i = 0, s = 0; i < d.count.length; i++) {
                dd.push({
                    x: x(s),
                    y: y(d.name),
                    width: x(d.count[i]) - x(0),
                    color: color(i)
                });
                s += d.count[i]
            }
            return dd;
        }) 
    .join("rect")
    .attr("x", d => d.x)
    .attr("y", d => d.y)
    .attr("width", d => d.width)
    .attr("height", y.bandwidth())
    .attr("fill", d => d.color)
    
    svg.append("g")
    .call(xAxis);

    svg.append("g")
    .call(yAxis);
}


data = [
    {name: 'bbq', before: 16, after: 4},
    {name: 'bbq', before: 14, after: 5},
    {name: 'bbq', before: 12, after: 6},
    {name: 'return_area', before: 7, after: 4},
    {name: 'return_area', before: 1, after: 8}
]

var width = 600,
    height = 600,
    svg = d3.select("svg").attr("width", width).attr("height", height);

margin = 40

// Add X axis
var x = d3.scaleLinear()
.domain([0, d3.max(data, d => d.after)])
.range([margin, width-margin]);

svg.append("g")
.attr("transform", "translate(0," + (height-margin) + ")")
.call(d3.axisBottom(x));

// Add Y axis
var y = d3.scaleLinear()
.domain([0, d3.max(data, d => d.before)])
.range([height-margin, margin]);

svg.append("g")
.attr("transform", "translate(" + margin + ",0)")
.call(d3.axisLeft(y));

// Color scale: give me a specie name, I return a color
var color = d3.scaleOrdinal()
.domain(["bbq", "return_area" ])
.range([ "#440154ff", "#21908dff"])


// Highlight the specie that is hovered
var highlight = function(d){
    selected = d.name

    d3.selectAll(".dot")
    .transition()
    .duration(200)
    .style("fill", "lightgrey")
    .attr("r", 3)

    d3.selectAll("." + selected)
    .transition()
    .duration(200)
    .style("fill", color(selected))
    .attr("r", 7)
}

// Highlight the specie that is hovered
var doNotHighlight = function(){
    d3.selectAll(".dot")
    .transition()
    .duration(200)
    .style("fill", "lightgrey")
    .attr("r", 5 )
}

// Add dots
svg.append('g')
.selectAll("dot")
.data(data)
.enter()
.append("circle")
  .attr("class", function (d) { return "dot " + d.name } )
  .attr("cx", function (d) { return x(d.after); } )
  .attr("cy", function (d) { return y(d.before); } )
  .attr("r", 5)
  .style("fill", function (d) { return color(d.name) } )
.on("mouseover", highlight)
.on("mouseleave", doNotHighlight )
