var sidebar_socket = io('/sidebar');

sidebar_socket.on('connect', function() {
    sidebar_socket.emit('request', (html_text) => {
        sb_mng.replaceContent(html_text)
        sidebar_socket.emit('request_success_sidebar')
    });
});

sidebar_socket.on('request', function(html_text) {
    sb_mng.replaceContent(html_text)
});

//namespace 
//js interface
sb_mng = {

    replaceContent: function (html_text) {
        $('#sidebar').html(html_text)
    },

    switchToStep: function (step) {        
        sidebar_socket.emit('request_step', step, (html_text) => {
            sb_mng.replaceContent(html_text)
            sidebar_socket.emit('request_success_sidebar')
        })
    }

};
