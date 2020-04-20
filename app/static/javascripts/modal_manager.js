function get_socket() {
    if (cur_step == "TrayDetectionStep"){
        return tray_detection_socket
    }else if (cur_step == "OCRStep"){
        return ocr_socket
    }else if (cur_step == "ClassifyEatenStep"){
        return classify_eaten_socket
    }else if (cur_step == "ClassifyDishStep"){
        return classify_dish_socket
    }else if (cur_step == "SegmentationStep"){
        return segmentation_socket
    }else if (cur_step == "MultiLabelStep"){
        return multilabel_socket
    }else if (cur_step == "PairStep"){
        return pair_socket
    }else if (cur_step == "DataVisualizationStep"){
        return data_visualization_socket
    }
}

var modal_socket = io('/modal');

modal_socket.on('show', function(html_text){
    modal_mng.replaceContent(html_text)
})

modal_socket.on('hide', function(){
    modal_mng.hide()
})

modal_mng = {

    replaceContent: function (html_text) {        
        $('.modal').css("display", "block")
        $('.modal').html(html_text)
    },

    hide: function() {
        $('.modal').css("display", "none")
    }

};