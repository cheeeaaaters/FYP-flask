
function gallery(selection, tray_detection_data, config) {

    var config = config || {}
    var row_size = config.row_size || 8
    var image_width = config.image_width || 100
    var mh = config.mh || 15
    var mv = config.mv || 10
    var max_size = config.max_size || 20
    var absolute_path = (config.absolute_path === undefined) ? true : config.absolute_path
    //var absolute_path = false
    var path_prefix = absolute_path ? '/my_images/' : ''
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
            .data(d => [path_prefix + d.path])
            .join("img")
            .attr("src", p => p)
            .attr("width", image_width)

        if (description)
            wrappers.call(description)

        if (onClick)
            wrappers.on('click', onClick)

    }

    update_gallery(tray_detection_data)

    return {
        append: function (path) {
            tray_detection_data.unshift(path)
            data = tray_detection_data.slice(0, max_size)
            update_gallery(data)
        },
        set_description: function (f) {
            description = f
            update_gallery(tray_detection_data)
        },
        set_on_click: function (f) {
            onClick = f
            update_gallery(tray_detection_data)
        }
    }

}

function multilabel_gallery(selection, tray_detection_data, config) {

    var config = config || {}
    var row_size = config.row_size || 3
    var image_width = config.image_width || 100
    var pair_mh = config.pair_mh || 10
    var mh = config.mh || 50
    var mv = config.mv || 10
    var max_size = config.max_size || 9
    var absolute_path = (config.absolute_path === undefined) ? true : config.absolute_path
    var path_prefix = absolute_path ? '/my_images/' : ''
    var rect_width = image_width * 0.2
    var rect_height = rect_width * 0.4
    var cls = ["tag_rice", "tag_vegetable", "tag_meat"]

    d3.select(selection)
        .append("div")
        .attr("class", "gallery")
        .style("width", (image_width * 2 + mh * 2 + pair_mh) * row_size + "px")

    function draw_tag(svg, label) {
        var tag_y = 10
        var before_tag_x = (image_width - rect_width * 3) / 2
        var after_tag_x = image_width + pair_mh + before_tag_x

        var before_tag = svg.selectAll(".before_tag")
            .data(d => [d])
            .join("g")
            .attr("transform", "translate(" + before_tag_x + "," + tag_y + ")")
            .attr("class", "before_tag")

        before_tag.selectAll("rect")
            .data(d => d.before_label)
            .join("rect")
            .attr("x", (d, i) => rect_width * i)
            .attr("y", d => rect_height * (2 - d))
            .attr("width", rect_width)
            .attr("height", d => rect_height * (d + 1))
            .attr("class", (d, i) => cls[i])

        var after_tag = svg.selectAll(".after_tag")
            .data(d => [d])
            .join("g")
            .attr("transform", "translate(" + after_tag_x + "," + tag_y + ")")
            .attr("class", "after_tag")

        after_tag.selectAll("rect")
            .data(d => d.after_label)
            .join("rect")
            .attr("x", (d, i) => rect_width * i)
            .attr("y", d => rect_height * (2 - d))
            .attr("width", rect_width)
            .attr("height", d => rect_height * (d + 1))
            .attr("class", (d, i) => cls[i])
    }

    function tag(wrappers) {
        var svg = wrappers.selectAll("svg")
            .data(d => [d])
            .join("svg")
            .attr("width", image_width * 2 + pair_mh)

        draw_tag(svg)
    }

    function update_gallery(data) {

        var gallery = d3.select(selection)
            .selectAll(".gallery")

        var wrappers = gallery.selectAll(".pair_wrapper")
            .data(data, d => d.pair_id)
            .join("div")
            .style("margin", mv + "px " + mh + "px")
            .attr("class", "pair_wrapper")
            .style("display", "flex")
            .style("flex-direction", "column")
            .style("width", image_width * 2 + pair_mh + "px")

        var img_wrapper = wrappers.selectAll(".imgs_wrapper")
            .data(d => [d])
            .join("div")
            .attr('class', "imgs_wrapper")

        img_wrapper.selectAll("img")
            .data(d => [path_prefix + d.before_path, path_prefix + d.after_path])
            .join('img')
            .attr("src", p => p)
            .attr("width", image_width)
            .style("margin-right", (d, i) => (i == 0 ? pair_mh + "px" : "0px"))

        wrappers.call(tag)    

    }

    update_gallery(tray_detection_data)

    return {
        append: function (path) {
            tray_detection_data.unshift(path)
            data = tray_detection_data.slice(0, max_size)
            update_gallery(data)
        }
    }

}
