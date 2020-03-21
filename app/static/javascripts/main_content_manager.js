var main_content_socket = io('/main_content');

main_content_socket.on('connect', function() {
    main_content_socket.emit('request', (html_text) => mc_mng.replaceContent(html_text));
});

main_content_socket.on('request', function(html_text) {
    mc_mng.replaceContent(html_text)
});

//namespace 
//js interface
mc_mng = {

    replaceContent: function (html_text) {
        $('#main_content').html(html_text)
    },

    switchToStep: function (step) {        
        main_content_socket.emit('request_step', step, (html_text) => mc_mng.replaceContent(html_text))
    }

};


