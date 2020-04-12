var modal_socket = io('/modal');

modal_socket.on('show', function(html_text){
    modal_mng.replaceContent(html_text)
})

modal_socket.on('hide', function(){
    modal_mng.hide()
})

modal_mng = {

    replaceContent: function (html_text) {        
        $('.modal').css("display", "block")
        $('.modal').html(html_text)
    },

    hide: function() {
        $('.modal').css("display", "none")
    }

};