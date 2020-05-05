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

$("#hammer_button").on('click', function() {
    nav_button_socket.emit('hammer_button')
});

db_options = {
    app: $("#app"),
    demo: $("#demo"),    
}

var db_socket = io('/db')

for(const model in db_options){
    db_options[model].on('click', () => {
        for(const key in db_options){
            db_options[key].removeClass('active')
        }
        db_options[model].addClass('active')
        db_socket.emit('switch', model, (code) => {
            if (code != 0){
                alert('db switch success!')
            }
            else{
                alert('db switch fail...')
            }            
        })
    })
}