var multilabel_socket = io('/multilabel_step');

(function () {

    var multilabel_progess_bar;
    var multilabel_infer_time_chart;
    var pair_gallery;

    var i = 1;

    multilabel_socket.on('display', function (tray) {
        multilabel_progess_bar.update(tray.percentage * 100)
        pair_gallery.append(tray)
        multilabel_infer_time_chart.add({ x: i, y: tray.infer_time })
        i += 1;
    });

    multilabel_socket.on('init_sb', function () {        
        multilabel_progess_bar = radialProgress('.process_percentage')
        multilabel_progess_bar.update(0)
    })

    multilabel_socket.on('init_mc', function () {
        var multilabel_tabs = {
            introduction: $("#multilabel_introduction_content"),
            gallery: $("#multilabel_classifier_content"),
            infer_time: $("#multilabel_infer_time_content")
        }

        $("#multilabel_introduction").on('click', function () {
            for (const key in multilabel_tabs) {
                multilabel_tabs[key].addClass('hidden')
            }
            multilabel_tabs.introduction.removeClass('hidden')
        })

        $("#multilabel_classifier").on('click', () => {
            for (const key in multilabel_tabs) {
                multilabel_tabs[key].addClass('hidden')
            }
            multilabel_tabs.gallery.removeClass('hidden')
        })

        $("#multilabel_infer_time").on('click', () => {
            for (const key in multilabel_tabs) {
                multilabel_tabs[key].addClass('hidden')
            }
            multilabel_tabs.infer_time.removeClass('hidden')
        })

        pair_gallery = multilabel_gallery("#multilabel_classifier_content", [], {
            absolute_path: true,
            load_more: true
        })        

        multilabel_infer_time_chart = lineChart('#multilabel_infer_time_graph', [], { width: 1000, height: 300 })

        for (const key in multilabel_tabs) {
            multilabel_tabs[key].addClass('hidden')
        }
        multilabel_tabs.introduction.removeClass('hidden')

    })

})()
