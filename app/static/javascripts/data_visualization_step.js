function pieChart(data, id, width, height, color) {

    var total = d3.sum(data, d => d.count)

    var svg = d3.select("#" + id)
        .attr("width", width)
        .attr("height", height),
        radius = Math.min(width, height) / 2.5;

    var g = svg.append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var pie = d3.pie().value(d => d.count)

    var path = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var label = d3.arc()
        .outerRadius(radius)
        .innerRadius(radius - 120);

    var percent = d3.arc()
        .outerRadius(radius + 40)
        .innerRadius(radius);

    var arc = g.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");

    arc.append("path")
        .attr("d", path)
        .attr("fill", function (d, i) { return color[i]; });

    arc.append("text")
        .attr("transform", function (d) {
            return "translate(" + label.centroid(d) + ")";
        })
        .text(function (d) { return d.data.type; });

    arc.append("text")
        .attr("transform", function (d) {
            return "translate(" + percent.centroid(d) + ")";
        })
        .text(function (d) { return Math.round((d.data.count / total) * 100) + "%"; });
}

function stackBarChart(series, id, margin, width, color) {

    var height = series.length * 40 + margin.top + margin.bottom

    var x = d3.scaleLinear()
        .domain([0, d3.max(series, d => d3.sum(d.count))])
        .range([margin.left, width - margin.right])

    var y = d3.scaleBand()
        .domain(series.map(d => d.name))
        .range([margin.top, height - margin.bottom])
        .padding(0.16)

    var xAxis = g => g
        .attr("transform", `translate(0,${margin.top})`)
        .call(d3.axisTop(x).ticks(width / 100))

    var yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).tickSizeOuter(0))

    const svg = d3.select("#" + id)
        .attr("width", width)
        .attr("height", height);

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
                    color: color[i]
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

function scatterPlot(data, id, width, height) {

    data.forEach(d => { d.percent = 100 * d.after / (d.before + 0.00001) })

    var svg = d3.select("#" + id)
        .attr("width", width * 2)
        .attr("height", height);
    margin = 40

    // Add X axis
    var x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.after)])
        .range([margin, width - margin]);

    svg.append("g")
        .attr("transform", "translate(0," + (height - margin) + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.before)])
        .range([height - margin, margin]);

    svg.append("g")
        .attr("transform", "translate(" + margin + ",0)")
        .call(d3.axisLeft(y));

    // Color scale: give me a specie name, I return a color
    var color = d3.scaleOrdinal()
        .domain(d3.map(data, d => d.name).keys())
        .range(d3.schemeCategory10)


    // Highlight the specie that is hovered
    var highlight = function (d) {
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

        d3.selectAll(".panel_line")
            .style("stroke", "rgb(0,0,0,0.15)")

        d3.selectAll('.line_' + selected)
            .style("stroke", color(selected))
    }

    // Highlight the specie that is hovered
    var doNotHighlight = function () {
        d3.selectAll(".dot")
            .transition()
            .duration(200)
            .style("fill", "lightgrey")
            .attr("r", 5)

        d3.selectAll(".panel_line")
            .style("stroke", "rgb(0,0,0,0.15)")
    }

    // Add dots
    svg.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", function (d) { return "dot " + d.name })
        .attr("cx", function (d) { return x(d.after); })
        .attr("cy", function (d) { return y(d.before); })
        .attr("r", 5)
        .style("fill", "lightgrey")
        .on("mouseover", highlight)
        .on("mouseleave", doNotHighlight)

    var panel = svg.append("g")
        .attr("transform", "translate(" + (margin + width) + "," + margin + ")")
        .attr("class", "panel")

    var labels = panel.selectAll("g")
        .data(d3.map(data, d => d.name).keys())
        .enter()
        .append("g")
        .attr("transform", (d, i) => "translate(0," + 50 * i + ")")
        .on("mouseover", d => highlight({ name: d }))
        .on("mouseleave", doNotHighlight)

    //console.log(a)

    labels.append("circle")
        .attr("r", 5)
        .attr("fill", name => color(name))

    labels.append("text")
        .attr("transform", "translate(20, 5)")
        .text(name => name)

    labels.append("line")
        .attr("class", name => "line_" + name + " panel_line")
        .attr("transform", "translate(0, 15)")
        .style("stroke", "rgb(0,0,0,0.15)")
        .style("stroke-width", 2)
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", 100)
        .attr("y2", 0)

    var highlight_percent = function (val) {
        svg.selectAll('circle')
            .filter(d => d.percent <= val)
            .style("fill", d => color(d.name))
            .attr("r", 7)

        svg.selectAll('circle')
            .filter(d => d.percent > val)
            .style("fill", "lightgrey")
            .attr("r", 5)
    }

    var sliderVertical = d3
        .sliderLeft()
        .min(0)
        .max(100)
        .height(300)
        .ticks(5)
        .default(1)
        .fill('#87a9ff')
        .on('onchange', highlight_percent)


    var gVertical = panel
        .append('svg')
        .attr("x", 100)
        .attr("y", -20)
        .attr('width', 150)
        .attr('height', 500)
        .append('g')
        .attr('transform', 'translate(140,20)');

    gVertical.call(sliderVertical);

}

/*
color = ['#ff5959', '#8fff87', '#87a9ff']
data_1 = [
    { type: "rice", count: 6 },
    { type: "vegetable", count: 2 },
    { type: "meat", count: 4 }
]

pieChart(data_1, "np_1", 400, 400, color)
pieChart(data_1, "np_3", 400, 400, color)

series = [
    { name: 'a1', count: [10, 20, 40] },
    { name: 'a2', count: [20, 30, 50] },
    { name: 'a3', count: [5, 6, 20] }
]

margin = { top: 30, right: 40, bottom: 0, left: 60 }

stackBarChart(series, "np_2", margin, 800, color)
stackBarChart(series, "np_4", margin, 800, color)

data_2 = [
    { name: 'bbq', before: 16, after: 4 },
    { name: 'bbq', before: 14, after: 5 },
    { name: 'bbq', before: 12, after: 6 },
    { name: 'japanese', before: 7, after: 4 },
    { name: 'japanese', before: 1, after: 8 }
]

scatterPlot(data_2, "p_1", 600, 600)
*/

function radialProgress(selector) {

    const parent = d3.select(selector)
    const size = parent.node().getBoundingClientRect()
    const svg = parent.append('svg')
        .attr('width', size.width)
        .attr('height', size.height);
    const outerRadius = Math.min(size.width, size.height) * 0.45;
    const thickness = 10;
    let value = 0;

    const mainArc = d3.arc()
        .startAngle(0)
        .endAngle(Math.PI * 2)
        .innerRadius(outerRadius - thickness)
        .outerRadius(outerRadius)

    svg.append("path")
        .attr('class', 'progress-bar-bg')
        .attr('transform', `translate(${size.width / 2},${size.height / 2})`)
        .attr('d', mainArc())

    const mainArcPath = svg.append("path")
        .attr('class', 'progress-bar')
        .attr('transform', `translate(${size.width / 2},${size.height / 2})`)

    svg.append("circle")
        .attr('class', 'progress-bar')
        .attr('transform', `translate(${size.width / 2},${size.height / 2 - outerRadius + thickness / 2})`)
        .attr('width', thickness)
        .attr('height', thickness)
        .attr('r', thickness / 2)

    const end = svg.append("circle")
        .attr('class', 'progress-bar')
        .attr('transform', `translate(${size.width / 2},${size.height / 2 - outerRadius + thickness / 2})`)
        .attr('width', thickness)
        .attr('height', thickness)
        .attr('r', thickness / 2)

    let percentLabel = svg.append("text")
        .attr('class', 'progress-label')
        .attr('transform', `translate(${size.width / 2},${size.height / 2})`)
        .text('0')

    return {
        update: function (progressPercent) {
            const startValue = value
            const startAngle = Math.PI * startValue / 50
            const angleDiff = Math.PI * progressPercent / 50 - startAngle;
            const startAngleDeg = startAngle / Math.PI * 180
            const angleDiffDeg = angleDiff / Math.PI * 180
            const transitionDuration = 1500

            mainArcPath.transition().duration(transitionDuration).attrTween('d', function () {
                return function (t) {
                    mainArc.endAngle(startAngle + angleDiff * t)
                    return mainArc();
                }
            })
            end.transition().duration(transitionDuration).attrTween('transform', function () {
                return function (t) {
                    return `translate(${size.width / 2},${size.height / 2})` +
                        `rotate(${(startAngleDeg + angleDiffDeg * t)})` +
                        `translate(0,-${outerRadius - thickness / 2})`
                }
            })
            percentLabel.transition().duration(transitionDuration).tween('bla', function () {
                return function (t) {
                    percentLabel.text(Math.round(startValue + (progressPercent - startValue) * t));
                }
            })
            value = progressPercent
        }
    }

}

function lineChart(selector, data) {

    var margin = { top: 10, right: 30, bottom: 30, left: 60 }
    var ymax = 1
    if (data.length > 0) {
        ymax = Math.max(d3.max(data, d => d.y), ymax)
    }

    const parent = d3.select(selector)
    const size = parent.node().getBoundingClientRect()
    //console.log(size)
    const svg = parent.append('svg')
        .attr('width', size.width)
        .attr('height', size.height)

    const svgg = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var width = size.width - margin.left - margin.right,
        height = size.height - margin.top - margin.bottom;
    // append the svg object to the body of the page

    // Add X axis --> it is a date format
    var x = d3.scaleLinear()
        .domain([0, 200])
        .range([0, width]);
    var x2 = x.copy();
    var axis = d3.axisBottom(x).ticks(width / 50)
    var axisG = svgg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(axis);
    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, ymax])
        .range([height, 0]);
    svgg.append("g")
        .attr("class", "y-axis")
        .call(d3.axisLeft(y));
    // Add the line
    var line = d3.line()
        .x(function (d) { return x(d.x) })
        .y(function (d) { return y(d.y) })

    svgg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "#69b3a2")
        .attr("stroke-width", 1.5)
        .attr("d", line)
        .attr("class", "infer_time_line")

    var zoom = d3.zoom()
        .scaleExtent([1, 1])
        .on('zoom', function () {
            x = d3.event.transform.rescaleX(x2)
            axis.scale(x);
            axisG.call(axis);
            svg.select('.infer_time_line')
                .attr('d', line)
        });

    svg.call(zoom);

    return {
        add: function (pt) {
            data.push(pt)
            if (pt.y > ymax) {
                ymax = pt.y
                y = d3.scaleLinear()
                    .domain([0, ymax])
                    .range([height, 0]);                
                svgg.select(".y-axis").remove()
                svgg.append("g")
                .attr("class", "y-axis")
                .call(d3.axisLeft(y));
            }
            svg.select('.infer_time_line')
                .attr('d', line)
        }
    }

}
