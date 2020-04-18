var trash_model_socket = io('/nav_button')

function trash_modal_yes(){
    trash_model_socket.emit('trash_modal_status', {code: 1, step: cur_step})
    modal_mng.hide()
}

function trash_modal_no(){  
    trash_model_socket.emit('trash_modal_status', {code: 0, step: cur_step})
    modal_mng.hide()
}