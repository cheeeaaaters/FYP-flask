var tray_detection_socket = io('/tray_detection_step');

tray_detection_socket.on('display', function (tray) {
    //console.log(tray) 
    append_to_gallery(tray)
});

tray_detection_socket.on('init_sb', function () {
    var chart = radialProgress('.process_percentage')
    chart.update(0)
})

tray_detection_socket.on('finish', function () {
    $('#test').html("FINISH")
});
