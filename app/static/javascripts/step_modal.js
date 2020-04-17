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

function step_modal_yes(){
    get_socket().emit('modal_status', {code: 1, step: cur_step})
    modal_mng.hide()
}

function step_modal_no(){  
    get_socket().emit('modal_status', {code: 0, step: cur_step})
    modal_mng.hide()
}