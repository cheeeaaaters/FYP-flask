var hammer_model_socket = io('/nav_button')

function hammer_modal_yes(){
    hammer_model_socket.emit('hammer_modal_status', {code: 1, step: cur_step})
    modal_mng.hide()
}

function hammer_modal_no(){  
    hammer_model_socket.emit('hammer_modal_status', {code: 0, step: cur_step})
    modal_mng.hide()
}