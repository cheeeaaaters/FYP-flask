
function gallery(selection, tray_detection_data, config) {

    var config = config || {}
    var row_size = config.row_size || 8
    var image_width = config.image_width || 100
    var mh = config.mh || 15
    var mv = config.mv || 10
    var max_size = config.max_size || 20
    var description;
    var onClick;

    d3.select(selection)
        .append("div")
        .attr("class", "gallery")
        .style("width", (image_width + mh * 2) * row_size + "px")

    function update_gallery(data) {

        var gallery = d3.select(selection)
            .selectAll(".gallery")

        var wrappers = gallery.selectAll(".img_wrapper")
            .data(data, d => d.path)
            .join("div")
            .style("margin", mv + "px " + mh + "px")
            .attr("class", "img_wrapper")
            .style("display", "flex")
            .style("flex-direction", "column")

        wrappers.selectAll("img")
            .data(d => ['/my_images/' + d.path])
            .join("img")
            .attr("src", p => p)
            .attr("width", image_width)

        if(description)
            wrappers.call(description)

        if(onClick)
            wrappers.on('click', onClick)

    }

    return {
        append: function (path) {
            tray_detection_data.unshift(path)
            data = tray_detection_data.slice(0, max_size)
            update_gallery(data)
        },
        set_description: function (f) {
            description = f
        },
        set_on_click: function (f) {
            onClick = f
        }
    }

}