var data_visualization_socket = io('/data_visualization_step');

(function () {

    var color = ['#ff5959', '#8fff87', '#87a9ff', '#444444']
    var color_2 = ['#ff5959', '#8fff87', '#87a9ff', '#f5d742', '#444444']
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

    var groups = [
        [
            { name: 'rice: none', count: 10 },
            { name: 'rice: little', count: 5 },
            { name: 'rice: many', count: 2 },
        ],
        [
            { name: 'vegetable: none', count: 10 },
            { name: 'vegetable: little', count: 5 },
            { name: 'vegetable: many', count: 2 },
        ],
        [
            { name: 'meat: none', count: 10 },
            { name: 'meat: little', count: 5 },
            { name: 'meat: many', count: 2 },
        ]
    ]

    var margin = { top: 30, right: 40, bottom: 0, left: 60 } 
    var margin2 =  { top: 30, right: 40, bottom: 0, left: 120 }   

    var data_2 = [
        { name: 'bbq', before: 16, after: 4 },
        { name: 'bbq', before: 14, after: 5 },
        { name: 'bbq', before: 12, after: 6 },
        { name: 'japanese', before: 7, after: 4 },
        { name: 'japanese', before: 1, after: 8 }
    ]    

    
    var data_3 = [
        { name: 'bbq', count: 1 },
        { name: 'japanese', count: 1 },
        { name: 'delicacies', count: 1 },
        { name: 'two_choices', count: 1 },
        { name: 'teppanyaki', count: 1 },
        { name: 'null', count: 1 },
    ]
    
    var vs, sp, dc;    
    var dv_list_group;
    var lg_data = [
        'All',
        'Rice',
        'Vegetable',
        'Meat'
    ]
  
    data_visualization_socket.on('init_sb', function () {

        vs = vslider("#sp_slider")
        dv_list_group = list_group('#dv_list_group', lg_data, (state) => {
            data_visualization_socket.emit('q5_change_state', state, () => {
                data_visualization_socket.emit('q5', (data) => {
                    $("#p_1").empty()
                    $("#donut_1").empty()
                    console.log(data)                    
                    sp = scatterPlot(data, "p_1", 600, 600)                   
                    dc = donut_chart("#donut_1", data_3)
                    sp.set_filtered_list_change((fl) => {
                        data_3.forEach(d => d.count = 0)
                        fl.forEach(d => {
                            data_3.forEach(dd => {
                                if(d.name == dd.name){
                                    dd.count += 1
                                }
                            })
                        })                    
                        dc.update(data_3)
                    })         
                    vs.set_handler(sp.highlight_percent)                      
                })    
            })
        })
        dv_list_group.initState([true, false, false, false])

    })

    data_visualization_socket.on('init_mc', function () {

        flag = true;

        var data_visualization_tabs = {
            introduction: $("#data_visualization_introduction_content"),
            q1: $("#data_visualization_q1_content"),
            q2: $("#data_visualization_q2_content"),
            q3: $("#data_visualization_q3_content"),
            q4: $("#data_visualization_q4_content"),
            q5: $("#data_visualization_q5_content"),
            q6: $("#data_visualization_q6_content"),
        }

        var data_visualization_sb = {
            q5: $('#q5_sb')
        }

        $("#data_visualization_introduction").on('click', function () {
            for (const key in data_visualization_tabs) {
                data_visualization_tabs[key].addClass('hidden')
            }
            data_visualization_tabs.introduction.removeClass('hidden')
            for (const key in data_visualization_sb) {
                data_visualization_sb[key].addClass('hidden')
            }
        })

        var q1_drawn, q1_2_drawn = false;

        $("#data_visualization_q1").on('click', () => {
            for (const key in data_visualization_tabs) {
                data_visualization_tabs[key].addClass('hidden')
            }
            data_visualization_tabs.q1.removeClass('hidden')
            for (const key in data_visualization_sb) {
                data_visualization_sb[key].addClass('hidden')
            }
            data_visualization_socket.emit('q1', 'all', (data) => {
                if(!q1_drawn)
                    pieChart(data, "np_1", 400, 400, color)
                q1_drawn = true
            })  
            data_visualization_socket.emit('q1_2', 'all', (data) => {
                if(!q1_2_drawn)
                    pieChart(data, "np_1_2", 400, 400, color)
                q1_2_drawn = true
            })
            legion(["rice", "vegetable", "meat", "background"], "#q1_legion", color)
            options = {
                all: $("#data_visualization_q1_content #all"),
                bbq: $("#data_visualization_q1_content #bbq"),
                japanese: $("#data_visualization_q1_content #japanese"),
                two_choices: $("#data_visualization_q1_content #two_choices"),
                teppanyaki: $("#data_visualization_q1_content #teppanyaki"),
                delicacies: $("#data_visualization_q1_content #delicacies")
            }
            for(const dish in options){
                options[dish].on('click', () => {
                    for(const key in options){
                        options[key].removeClass('active')
                    }
                    options[dish].addClass('active')
                    data_visualization_socket.emit('q1', dish, (data) => {
                        $("#np_1").empty()
                        pieChart(data, "np_1", 400, 400, color)
                    }) 
                    data_visualization_socket.emit('q1_2', dish, (data) => {
                        $("#np_1_2").empty()
                        pieChart(data, "np_1_2", 400, 400, color)
                    }) 
                })
            }          
        })

        $("#data_visualization_q2").on('click', () => {
            for (const key in data_visualization_tabs) {
                data_visualization_tabs[key].addClass('hidden')
            }
            data_visualization_tabs.q2.removeClass('hidden')
            for (const key in data_visualization_sb) {
                data_visualization_sb[key].addClass('hidden')
            }
            data_visualization_socket.emit('q2', (data) => {
                stackBarChart(data, "np_2", margin, 800, color)
            })  
            data_visualization_socket.emit('q2_2', (data) => {
                stackBarChart(data, "np_2_2", margin, 800, color)
            })                            
        })

        var q3_drawn, q3_2_drawn = false;

        $("#data_visualization_q3").on('click', () => {
            for (const key in data_visualization_tabs) {
                data_visualization_tabs[key].addClass('hidden')
            }
            data_visualization_tabs.q3.removeClass('hidden')
            for (const key in data_visualization_sb) {
                data_visualization_sb[key].addClass('hidden')
            }
            data_visualization_socket.emit('q3', 'all', (data) => {
                if (!q3_drawn)
                    pieChart(data, "np_3", 400, 400, color_2)
                q3_drawn = true
            })  
            data_visualization_socket.emit('q3_2', 'all', (data) => {
                if (!q3_2_drawn)
                    pieChart(data, "np_3_2", 400, 400, color_2)
                q3_2_drawn = true
            })
            legion(["rice", "vegetable", "meat", "other", "background"], "#q3_legion", color_2)
            options = {
                all: $("#data_visualization_q3_content #all"),
                bbq: $("#data_visualization_q3_content #bbq"),
                japanese: $("#data_visualization_q3_content #japanese"),
                two_choices: $("#data_visualization_q3_content #two_choices"),
                teppanyaki: $("#data_visualization_q3_content #teppanyaki"),
                delicacies: $("#data_visualization_q3_content #delicacies")
            }
            for(const dish in options){
                options[dish].on('click', () => {
                    for(const key in options){
                        options[key].removeClass('active')
                    }
                    options[dish].addClass('active')
                    data_visualization_socket.emit('q3', dish, (data) => {
                        $("#np_3").empty()
                        pieChart(data, "np_3", 400, 400, color_2)
                    }) 
                    data_visualization_socket.emit('q3_2', dish, (data) => {
                        $("#np_3_2").empty()
                        pieChart(data, "np_3_2", 400, 400, color_2)
                    }) 
                })
            }               
        })

        $("#data_visualization_q4").on('click', () => {
            for (const key in data_visualization_tabs) {
                data_visualization_tabs[key].addClass('hidden')
            }
            data_visualization_tabs.q4.removeClass('hidden')
            for (const key in data_visualization_sb) {
                data_visualization_sb[key].addClass('hidden')
            }
            data_visualization_socket.emit('q4', (data) => {
                stackBarChart(data, "np_4", margin, 800, color_2)
            })  
            data_visualization_socket.emit('q4_2', (data) => {
                stackBarChart(data, "np_4_2", margin, 800, color_2)
            })               
        })

        $("#data_visualization_q5").on('click', () => {
            for (const key in data_visualization_tabs) {
                data_visualization_tabs[key].addClass('hidden')
            }
            data_visualization_tabs.q5.removeClass('hidden')
            for (const key in data_visualization_sb) {
                data_visualization_sb[key].addClass('hidden')
            }
            data_visualization_sb.q5.removeClass('hidden')
            data_visualization_socket.emit('q5', (data) => {
                $("#p_1").empty()
                $("#donut_1").empty()
                sp = scatterPlot(data, "p_1", 600, 600)                   
                dc = donut_chart("#donut_1", data_3)
                sp.set_filtered_list_change((fl) => {
                    data_3.forEach(d => d.count = 0)
                    fl.forEach(d => {
                        data_3.forEach(dd => {
                            if(d.name == dd.name){
                                dd.count += 1
                            }
                        })
                    })                    
                    dc.update(data_3)
                })         
                vs.set_handler(sp.highlight_percent)      
            })               
        })

        var q6_drawn = false

        $("#data_visualization_q6").on('click', () => {
            for (const key in data_visualization_tabs) {
                data_visualization_tabs[key].addClass('hidden')
            }
            data_visualization_tabs.q6.removeClass('hidden')
            for (const key in data_visualization_sb) {
                data_visualization_sb[key].addClass('hidden')
            }            
            data_visualization_socket.emit('q6', 'all', (data) => {
                if(!q6_drawn)
                    groupBarChart(data, "p_2", margin2, 900, color)
                q6_drawn = true
            })
            options = {
                all: $("#data_visualization_q6_content #all"),
                bbq: $("#data_visualization_q6_content #bbq"),
                japanese: $("#data_visualization_q6_content #japanese"),
                two_choices: $("#data_visualization_q6_content #two_choices"),
                teppanyaki: $("#data_visualization_q6_content #teppanyaki"),
                delicacies: $("#data_visualization_q6_content #delicacies")
            }
            for(const dish in options){
                options[dish].on('click', () => {
                    for(const key in options){
                        options[key].removeClass('active')
                    }
                    options[dish].addClass('active')
                    data_visualization_socket.emit('q6', dish, (data) => {
                        $("#np_3").empty()
                        groupBarChart(data, "p_2", margin2, 900, color)
                    })                     
                })
            }                             
        })

        for (const key in data_visualization_tabs) {
            data_visualization_tabs[key].addClass('hidden')
        }
        data_visualization_tabs.introduction.removeClass('hidden')
      
    })

})()
