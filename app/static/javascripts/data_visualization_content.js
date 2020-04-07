(function () {

    var color = ['#ff5959', '#8fff87', '#87a9ff']
    var data_1 = [
        { type: "rice", count: 6 },
        { type: "vegetable", count: 2 },
        { type: "meat", count: 4 }
    ]

    var series = [
        { name: 'a1', count: [10, 20, 40] },
        { name: 'a2', count: [20, 30, 50] },
        { name: 'a3', count: [5, 6, 20] }
    ]

    var margin = { top: 30, right: 40, bottom: 0, left: 60 }    

    var data_2 = [
        { name: 'bbq', before: 16, after: 4 },
        { name: 'bbq', before: 14, after: 5 },
        { name: 'bbq', before: 12, after: 6 },
        { name: 'japanese', before: 7, after: 4 },
        { name: 'japanese', before: 1, after: 8 }
    ]    

    var data_visualization_socket = io('/data_visualization_step');

    data_visualization_socket.on('init_sb', function () {

    })

    data_visualization_socket.on('init_mc', function () {

        pieChart(data_1, "np_1", 400, 400, color)
        pieChart(data_1, "np_3", 400, 400, color)

        stackBarChart(series, "np_2", margin, 800, color)
        stackBarChart(series, "np_4", margin, 800, color)

        scatterPlot(data_2, "p_1", 600, 600)

    })

})()
