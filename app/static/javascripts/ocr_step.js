(function() {

var ocr_socket = io('/ocr_step');

var chart;
var ocr_infer_time_chart;
var ocr_locate_time_chart;
var ocr_ocr_time_chart;
var gallery_0;
var gallery_90;
var gallery_180;
var gallery_270;
var ocr_gallery;
var i = 1;

ocr_socket.on('display', function (tray) {  
    chart.update(tray.percentage* 100)   
    
    if (tray.mode == 1){
        gallery_0.append(tray)
        gallery_90.append(tray)
        gallery_180.append(tray)
        gallery_270.append(tray)
    }else if (tray.mode == 2){
        var ocr_content = d3.select("#ocr_ocr_content")
        ocr_content.select('.img_wrapper')
                    .style('margin-left', "50px")
                    .selectAll('img')
                    .data(['/my_images/' + tray.path])
                    .join('img')
                    .attr('src', p => p)
                    .attr('width', 500)
        ocr_content.select('#image_path').text(tray.path)
        ocr_content.select('#locate_time').text(tray.locate_time)
        ocr_content.select('#ocr_time').text(tray.ocr_time)
        text_count = tray.ocr_text.length
        ocr_content.select('#text_count').text(text_count)
        ocr_content.select('#text_found')
                    .selectAll('li')
                    .data(tray.ocr_text)
                    .join('li')
                    .text(d => d)
    }else if (tray.mode == 3){
        ocr_gallery.append(tray)
    }
   
});

ocr_socket.on('init_sb', function () {
    chart = radialProgress('.process_percentage')
    chart.update(0)
})

ocr_socket.on('init_mc', function () {
    var ocr_tabs = {
        introduction: $("#ocr_introduction_content"),
        preprocessing: $("#ocr_preprocessing_content"),
        ocr: $("#ocr_ocr_content"),
        polling: $("#ocr_polling_content"),
        infer_time: $("#ocr_infer_time_content")
    }

    $("#ocr_introduction").on('click', function () {                   
        for (const key in ocr_tabs) {
            ocr_tabs[key].addClass('hidden')
        }
        ocr_tabs.introduction.removeClass('hidden')       
    })

    $("#ocr_preprocessing").on('click', () => {
        for (const key in ocr_tabs) {
            ocr_tabs[key].addClass('hidden')
        }
        ocr_tabs.preprocessing.removeClass('hidden')          
    })
    
    $("#ocr_ocr").on('click', () => {
        for (const key in ocr_tabs) {
            ocr_tabs[key].addClass('hidden')
        }
        ocr_tabs.ocr.removeClass('hidden')
    })

    $("#ocr_polling").on('click', () => {
        for (const key in ocr_tabs) {
            ocr_tabs[key].addClass('hidden')
        }
        ocr_tabs.polling.removeClass('hidden')
    })
    
    $("#ocr_infer_time").on('click', () => {
        for (const key in ocr_tabs) {
            ocr_tabs[key].addClass('hidden')
        }
        ocr_tabs.infer_time.removeClass('hidden')
    })   

    var gallery_config = {
        row_size: 1,
        max_size: 5,
        absolute_path: false
    }

    gallery_0 = gallery("#gallery_0", [], gallery_config)
    gallery_90 = gallery("#gallery_90", [], gallery_config)
    gallery_180 = gallery("#gallery_180", [], gallery_config)
    gallery_270 = gallery("#gallery_270", [], gallery_config)

    ocr_gallery = gallery("#ocr_polling_content", [], {absolute_path: false})
    ocr_gallery.set_description(wrappers => {
        wrappers.selectAll("text")
            .data(d => [d.ocr])
            .join("text")
            .text(d => d)
            .style("text-align", "center")
    })

    ocr_infer_time_chart = lineChart('#preprocessing_infer_time_graph', [], {width: 1000, height: 300})
    ocr_locate_time_chart = lineChart('#ocr_locate_time_graph', [], {width: 1000, height: 300})
    ocr_ocr_time_chart = lineChart('#ocr_ocr_time_graph', [], {width: 1000, height: 300})
    
    for (const key in ocr_tabs) {
        ocr_tabs[key].addClass('hidden')
    }
    ocr_tabs.introduction.removeClass('hidden')     

})

ocr_socket.on('finish', function () {
    $('#test').html("FINISH")
});

})()
