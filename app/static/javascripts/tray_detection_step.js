var tray_detection_socket = io('/tray_detection_step');

var tray_detection_progess_bar;
var infer_time_chart;
var tray_gallery;
var i = 1;

tray_detection_socket.on('display', function (tray) {  
    tray_detection_progess_bar.update(tray.percentage* 100)  
    tray_gallery.append(tray)
    infer_time_chart.add({x: i, y: tray.infer_time})
    i += 1;
});

tray_detection_socket.on('init_sb', function () {
    tray_detection_progess_bar = radialProgress('.process_percentage')
    tray_detection_progess_bar.update(0)
})

tray_detection_socket.on('init_mc', function () {
    var tray_detection_tabs = {
        introduction: $("#tray_detection_introduction_content"),
        gallery: $("#tray_detection_gallery_content"),
        details: $("#tray_detection_details_content"),
        infer_time: $("#tray_detection_infer_time_content")
    }

    $("#tray_detection_introduction").on('click', function () {                   
        for (const key in tray_detection_tabs) {
            tray_detection_tabs[key].addClass('hidden')
        }
        tray_detection_tabs.introduction.removeClass('hidden')       
    })

    $("#tray_detection_gallery").on('click', () => {
        for (const key in tray_detection_tabs) {
            tray_detection_tabs[key].addClass('hidden')
        }
        tray_detection_tabs.gallery.removeClass('hidden')          
    })
    
    $("#tray_detection_details").on('click', () => {
        for (const key in tray_detection_tabs) {
            tray_detection_tabs[key].addClass('hidden')
        }
        tray_detection_tabs.details.removeClass('hidden')
    })
    
    $("#tray_detection_infer_time").on('click', () => {
        for (const key in tray_detection_tabs) {
            tray_detection_tabs[key].addClass('hidden')
        }
        tray_detection_tabs.infer_time.removeClass('hidden')        
    })

    tray_gallery = gallery("#tray_detection_gallery_content", [])
    tray_gallery.set_description(wrappers => {
        wrappers.selectAll("text")
            .data(d => [d.name])
            .join("text")
            .text(d => d)
            .style("text-align", "center")
    })
    tray_gallery.set_on_click(d => {
        var details = d3.select('#tray_detection_details_content')
        details.select('.img_wrapper')
                .style('margin-left', "50px")
                .selectAll('img')
                .data([d.path])
                .join('img')
                .attr('src', p => p)
                .attr('width', 500)        
        details.select('#image_path').text(d.path)
        details.select('#video_path').text(d.video_path)
        details.select('#object_id').text(d.obj_id)
        details.select('#area').text(d.area)
        details.select('#date_time').text(d.date_time)
        details.select('#infer_time').text(d.infer_time)

        for (const key in tray_detection_tabs) {
            tray_detection_tabs[key].addClass('hidden')
        }
        tray_detection_tabs.details.removeClass('hidden')
    })

    infer_time_chart = lineChart('#tray_detection_infer_time_graph', [], {width: 1000, height: 300})
    
    for (const key in tray_detection_tabs) {
        tray_detection_tabs[key].addClass('hidden')
    }
    tray_detection_tabs.introduction.removeClass('hidden')     

})

tray_detection_socket.on('finish', function () {
    $('#test').html("FINISH")
});


