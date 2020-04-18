var nav_button_socket = io('/nav_button');

$("#start_button").on('click', function() {
    nav_button_socket.emit('start_button')
});

$("#pause_button").on('click', function() {
    nav_button_socket.emit('pause_button')
});

$("#trash_button").on('click', function() {
    nav_button_socket.emit('trash_button')
});