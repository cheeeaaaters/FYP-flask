
(function() {

var classify_eaten_socket = io('/classify_eaten_step');

var classify_eaten_progess_bar;
var classify_eaten_infer_time_chart;
var classify_eaten_gallery;
var classify_uneaten_gallery;
var i = 1;

classify_eaten_socket.on('display', function (tray) {  
    classify_eaten_progess_bar.update(tray.percentage * 100)  
    classify_eaten_gallery.append(tray)
    classify_uneaten_gallery.append(tray)
    classify_eaten_infer_time_chart.add({x: i, y: tray.ocr_time})
    i += 1;
});

classify_eaten_socket.on('init_sb', function () {
    classify_eaten_progess_bar = radialProgress('.process_percentage')
    classify_eaten_progess_bar.update(0)
})

classify_eaten_socket.on('init_mc', function () {
    var classify_eaten_tabs = {
        introduction: $("#classify_eaten_introduction_content"),
        gallery: $("#classify_eaten_classifier_content"),        
        infer_time: $("#classify_eaten_infer_time_content")
    }

    $("#classify_eaten_introduction").on('click', function () {                   
        for (const key in classify_eaten_tabs) {
            classify_eaten_tabs[key].addClass('hidden')
        }
        classify_eaten_tabs.introduction.removeClass('hidden')       
    })

    $("#classify_eaten_classifier").on('click', () => {
        for (const key in classify_eaten_tabs) {
            classify_eaten_tabs[key].addClass('hidden')
        }
        classify_eaten_tabs.gallery.removeClass('hidden')          
    })
    
    $("#classify_eaten_infer_time").on('click', () => {
        for (const key in classify_eaten_tabs) {
            classify_eaten_tabs[key].addClass('hidden')
        }
        classify_eaten_tabs.infer_time.removeClass('hidden')        
    })

    classify_eaten_gallery = gallery("#classify_eaten_gallery_content", [])
    classify_eaten_gallery.set_description(wrappers => {
        wrappers.selectAll("text")
            .data(d => [d.name])
            .join("text")
            .text(d => d)
            .style("text-align", "center")
    })

    var gallery_config = {
        row_size: 3,
        max_size: 9,
        mh: 20,
        absolute_path: false
    }
    classify_eaten_gallery = gallery("#gallery_eaten", [], gallery_config)
    classify_uneaten_gallery = gallery("#gallery_uneaten", [], gallery_config)
    classify_eaten_infer_time_chart = lineChart('#classify_eaten_infer_time_graph', [], {width: 1000, height: 300})
    
    for (const key in classify_eaten_tabs) {
        classify_eaten_tabs[key].addClass('hidden')
    }
    classify_eaten_tabs.introduction.removeClass('hidden')     

})

classify_eaten_socket.on('finish', function () {
    $('#test').html("FINISH")
});

})()
