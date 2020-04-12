function step_modal_yes(){
    modal_socket.emit('modal_status', {code: 1, step: cur_step})
    modal_mng.hide()
}

function step_modal_no(){
    modal_socket.emit('modal_status', {code: 0, step: cur_step})
    modal_mng.hide()
}