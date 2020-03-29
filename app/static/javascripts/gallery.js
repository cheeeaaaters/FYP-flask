
var tray_detection_data = []
var row_size = 8
var image_width = 100
var mh = 15
var mv = 10
var max_size = 20

function update_gallery(data) {

    var gallery = d3.selectAll(".gallery")
        .style("width", (image_width + mh * 2) * row_size + "px")

    gallery.selectAll(".img_wrapper")
        .data(data, d => d)
        .join("div")
        .style("margin", mv + "px " + mh + "px")
        .attr("class", "img_wrapper")
            .selectAll("img")
            .data(d => [d])
            .join("img")
            .attr("src", p => p)
            .attr("width", image_width)

}

function append_to_gallery(path){

    tray_detection_data.push(path)
    data = tray_detection_data.slice(0, max_size-1)
    update_gallery(data)

}