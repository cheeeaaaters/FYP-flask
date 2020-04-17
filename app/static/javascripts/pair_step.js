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
    })

    pair_socket.on('init_mc', function () {

    })

})()
