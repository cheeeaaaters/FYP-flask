

function cross_point(selection, data, config) {

    function bound(value, min, max) {
        if (value < min) {
            return min;
        }
        if (value > max) {
            return max;
        }
        return value;
    }

    var config = config || {}
    var mh = config.mh || 10
    var mv = config.mv || 30

    var svg_width = 800
    var img_width = 300
    var ratio = 1;    
    var svg_height = img_width * ratio + mv;

    d3.select(selection)
        .append("svg")        
        .attr('class', "images_holder")
        .attr("width", svg_width)
        .attr("height", svg_height)

    var svg = d3.select(selection)
        .selectAll('.images_holder')

    var cx = (svg_width - img_width - mh - (mh + img_width))/2    

    var dot_orig = svg.select('.dot_orig')
    var dot_mask = svg.select('.dot_mask')

    var info = svg.append('g')
        .attr("transform", "translate(" + (mh + img_width) + "," + mv + ")")

    info.append("text")
        .attr("x", cx)
        .attr("y", 20)
        .attr("text-anchor", "middle")
        .attr('class', 'coords')
        .text("(0 , 0)")

    var orig = svg.append("svg:image")
        .attr("x", mh)
        .attr("y", mv)
        .attr("width", img_width)        
        .style("background-size", img_width + "px")
        .attr("xlink:href", "static/images/food.jpg")
        .on("mousemove", () => {
            var mouse = d3.mouse(d3.event.target);
            if (dot_orig.empty()) {
                dot_orig = svg.append('circle')
                    .attr('class', 'dot_orig')
                    .attr('r', 5)
                    .style('fill', 'red')
                    .style('pointer-events', 'none')
            }
            dot_orig.attr('cx', mouse[0])
                .attr('cy', mouse[1])

            if (dot_mask.empty()) {
                dot_mask = svg.append('circle')
                    .attr('class', 'dot_mask')
                    .attr('r', 5)
                    .style('fill', 'red')
            }
            dot_mask.attr('cx', svg_width - mh - img_width + (mouse[0] - mh))
                .attr('cy', mouse[1])

            info.select('.coords')
                .text("(" + Math.round(mouse[0]-mh) + " , " + Math.round(mouse[1]-mv) + ")")
        })
        .on("mouseleave", () => {
            dot_orig.remove()
            dot_orig = svg.select('.dot_orig')
            dot_mask.remove()      
            dot_mask = svg.select('.dot_mask')      
        })

    var mask = svg.append("svg:image")
        .attr("x", svg_width - mh - img_width)
        .attr("y", mv)
        .attr("width", img_width)        
        .style("background-size", img_width + "px")
        .attr("xlink:href", "static/images/food.jpg")
    

}