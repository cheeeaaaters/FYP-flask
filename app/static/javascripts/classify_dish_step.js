
(function () {

    var classify_dish_socket = io('/classify_dish_step');

    var classify_dish_progess_bar;
    var classify_dish_infer_time_chart;
    var classify_dish_gallery;
    var color = d3.scaleOrdinal()
        .domain(["bbq", "two_choices", "delicacies", "japanese", "teppanyaki", "veggies"])
        .range(["rgb(252,186,3)", "rgb(122,149,255)", "rgb(235,157,252)"
                ,"rgb(255,127,122)","rgb(248,252,157)", "rgb(131,255,122)"])
        .unknown("rgb(219,219,219)")

    var i = 1;

    classify_dish_socket.on('display', function (tray) {
        classify_dish_progess_bar.update(tray.percentage * 100)
        classify_dish_gallery.append(tray)
        classify_dish_infer_time_chart.add({ x: i, y: tray.infer_time })
        i += 1;
    });

    classify_dish_socket.on('init_sb', function () {
        classify_dish_progess_bar = radialProgress('.process_percentage')
        classify_dish_progess_bar.update(0)
    })

    classify_dish_socket.on('init_mc', function () {
        var classify_dish_tabs = {
            introduction: $("#classify_dish_introduction_content"),
            gallery: $("#classify_dish_classifier_content"),
            infer_time: $("#classify_dish_infer_time_content")
        }

        $("#classify_dish_introduction").on('click', function () {
            for (const key in classify_dish_tabs) {
                classify_dish_tabs[key].addClass('hidden')
            }
            classify_dish_tabs.introduction.removeClass('hidden')
        })

        $("#classify_dish_classifier").on('click', () => {
            for (const key in classify_dish_tabs) {
                classify_dish_tabs[key].addClass('hidden')
            }
            classify_dish_tabs.gallery.removeClass('hidden')
        })

        $("#classify_dish_infer_time").on('click', () => {
            for (const key in classify_dish_tabs) {
                classify_dish_tabs[key].addClass('hidden')
            }
            classify_dish_tabs.infer_time.removeClass('hidden')
        })

        classify_dish_gallery = gallery("#classify_dish_classifier_content", [])
        classify_dish_gallery.set_description(wrappers => {
            wrappers.selectAll(".dish_tag")
                .data(d => [d.dish])
                .join("div")
                .attr("class", "dish_tag")
                .style('background', d => color(d))
                .text(d => d)
                .style("text-align", "center")
        })

        classify_dish_infer_time_chart = lineChart('#classify_dish_infer_time_graph', [], { width: 1000, height: 300 })

        for (const key in classify_dish_tabs) {
            classify_dish_tabs[key].addClass('hidden')
        }
        classify_dish_tabs.introduction.removeClass('hidden')

    })

    classify_dish_socket.on('finish', function () {
        $('#test').html("FINISH")
    });

})()
