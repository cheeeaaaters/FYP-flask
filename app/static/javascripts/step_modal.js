function step_modal_yes(){
    get_socket().emit('modal_status', {code: 1, step: cur_step})
    modal_mng.hide()
}

function step_modal_no(){  
    get_socket().emit('modal_status', {code: 0, step: cur_step})
    modal_mng.hide()
}