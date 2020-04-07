let cur_step = 'TrayDetectionStep'

$("#tray_detection_step").on('click', function() {
    let step = 'TrayDetectionStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }        
});

$("#ocr_step").on('click', function() {
    let step = 'OCRStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }      
});

$("#classify_eaten_step").on('click', function() {
    let step = 'ClassifyEatenStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }      
});

$("#pair_step").on('click', function() {
    let step = 'PairStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }      
});

$("#classify_dish_step").on('click', function() {
    let step = 'ClassifyDishStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }      
});

$("#segmentation_step").on('click', function() {
    let step = 'SegmentationStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }      
});

$("#multi_label_step").on('click', function() {
    let step = 'MultiLabelStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }      
});

$("#data_visualization_step").on('click', function() {
    let step = 'DataVisualizationStep'
    if(cur_step != step){
        mc_mng.switchToStep(step)
        sb_mng.switchToStep(step)
        cur_step = step
    }      
});