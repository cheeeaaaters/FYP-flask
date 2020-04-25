var pair_socket = io('/pair_step');

(function () {

    var pair_list_group;
    var lg_data = [
        'Uneaten -> Eaten Constraint',
        'Area Constraint',
        'Dish Type Constraint'
    ]

    pair_socket.on('init_sb', function () {
        pair_list_group = list_group('#pair_list_group', lg_data, (state) => {
            pair_socket.emit('change_state', state)
        })
        pair_list_group.initState([true, false, false])

        var min = 10
        var max = 60

        var slider_min = $("#time_slider_min")[0]          
        slider_min.addEventListener('input', function() { 
            if(this.value != min){
                pair_socket.emit('change_eating_interval', this.value, max)
            }           
            min = this.value
        })

        var slider_max = $("#time_slider_max")[0]          
        slider_max.addEventListener('input', function() { 
            if(this.value != max){
                pair_socket.emit('change_eating_interval', min, this.value)
            }                
            max = this.value
        })
    })

    pair_socket.on('init_mc', function () {

    })

})()
