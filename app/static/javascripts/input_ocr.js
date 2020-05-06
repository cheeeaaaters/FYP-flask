var ocr = {

}

var data = []

var e1;
var e2;

$("#cross_button").click(() => {
    $('.modal').css("display", "none")
})

function details_modal(obj) {
    $('.modal').css("display", "block")
    $('#video').text(obj.video)
    $('#path').text(obj.path)
    $('#object_id').text(obj.object_id)
    $('#ocr').text(obj.ocr)
    $('#eaten').text(obj.eaten)
    $('#dish').text(obj.dish)
    $('#area').text(obj.area)
    $('#date_time').text(obj.date_time)
    $('#seg_path').text(obj.seg_path)
    $('#seg_total').text(obj.seg_total)
    $('#seg_rice').text(obj.seg_rice)
    $('#seg_vegetable').text(obj.seg_vegetable)
    $('#seg_meat').text(obj.seg_meat)
    $('#seg_other').text(obj.seg_other)
    $('#ml_rice').text(obj.ml_rice)
    $('#ml_vegetable').text(obj.ml_vegetable)
    $('#ml_meat').text(obj.ml_meat)    
}

function gallery(selection, tray_detection_data, config) {

    var ret = {}

    var config = config || {}
    var row_size = config.row_size || 5
    var image_width = config.image_width || 150
    var mh = config.mh || 30
    var mv = config.mv || 30
    var absolute_path = (config.absolute_path === undefined) ? true : config.absolute_path
    var no_cache = (config.no_cache === undefined) ? false : config.no_cache
    //var absolute_path = false
    var path_prefix = absolute_path ? '/my_images/' : ''
    var path_suffix = no_cache ? () => ('?time=' + get_time()) : () => ''

    var onClick = (d, i) => {
        move_cur(i)
    }

    ret.cur = 0

    $(selection).html("")
    document.removeEventListener('keydown', e1)
    document.removeEventListener('keydown', e2)

    var vwrapper = d3.select(selection)
        .append("div")
        .attr('class', 'vertical_wrapper center_wrapper')
        .attr('width', '100%')

    vwrapper.append("div")
        .attr("class", "gallery")
        .style("width", (image_width + mh * 2) * row_size + "px")

    var gallery = d3.select(selection)
        .selectAll(".gallery")

    var wrappers = gallery.selectAll(".img_wrapper")
        .data(tray_detection_data, d => d.path)
        .join("div")
        .style("margin", mv + "px " + mh + "px")
        .attr("class", (d, i) => "img_wrapper item" + i)
        .style("display", "flex")
        .style("flex-direction", "column")

    wrappers.selectAll("img")
        .data(d => [d])
        .join("img")
        .attr("src", d => path_prefix + d.path + path_suffix())
        .attr("width", image_width)
        .on('dblclick', d => {
            $.getJSON($SCRIPT_ROOT + '/details/' + d.path, {              
              }, function(data) {
                details_modal(data)
              });
        })

    if (onClick)
        wrappers.on('click', onClick)

    $("." + ret.cur).removeClass('active')
    $("." + ret.cur).addClass('active')

    function move_cur(index, scroll) {
        $(".item" + ret.cur).removeClass('active')
        index = Math.max(Math.min(index, tray_detection_data.length - 1), 0)
        $(".item" + index).addClass('active')
        if (scroll)
            $(".item" + index)[0].scrollIntoView()
        ret.cur = index
    }

    e1 = function (event) {
        if (event.keyCode == 37) {
            //alert('Left was pressed');
            event.preventDefault()
            move_cur(ret.cur - 1, true)
        }
        else if (event.keyCode == 39) {
            //alert('Right was pressed');
            event.preventDefault()
            move_cur(ret.cur + 1, true)
        }
        else if (event.keyCode == 38) {
            //alert('Up was pressed');   
            event.preventDefault()
            move_cur(ret.cur - row_size, true)
        }
        else if (event.keyCode == 40) {
            //alert('Down was pressed');
            event.preventDefault()
            move_cur(ret.cur + row_size, true)
        }
    }

    document.addEventListener('keydown', e1);

    ret.set_description = function (f) {
        description = f
        if (description)
            wrappers.call(description)
    }

    ret.set_on_click = function (f) {
        onClick = f
        if (onClick)
            wrappers.on('click', onClick)
    }

    ret.set_e2 = function (f) {
        e2 = f
        document.addEventListener('keydown', e2);
    }

    return ret
}

function pair_gallery(selection, tray_detection_data, config) {

    var config = config || {}
    var row_size = config.row_size || 3
    var image_width = config.image_width || 100
    var pair_mh = config.pair_mh || 10
    var mh = config.mh || 50
    var mv = config.mv || 10
    var absolute_path = (config.absolute_path === undefined) ? true : config.absolute_path
    var path_prefix = absolute_path ? '/my_images/' : ''

    $(selection).html("")
    document.removeEventListener('keydown', e1)
    document.removeEventListener('keydown', e2)

    var vwrapper = d3.select(selection)
        .append("div")
        .attr('class', 'vertical_wrapper center_wrapper')
        .attr('width', '100%')

    vwrapper.append("div")
        .attr("class", "gallery")
        .style("width", (image_width * 2 + mh * 2 + pair_mh) * row_size + "px")    

    var gallery = d3.select(selection)
        .selectAll(".gallery")

    var wrappers = gallery.selectAll(".pair_wrapper")
        .data(tray_detection_data)
        .join("div")
        .style("margin", mv + "px " + mh + "px")
        .attr("class", "pair_wrapper")
        .style("display", "flex")
        .style("flex-direction", "column")
        .style("width", image_width * 2 + pair_mh + "px")

    var img_wrapper = wrappers.selectAll(".imgs_wrapper")
        .data(d => [d])
        .join("div")
        .attr('class', "imgs_wrapper")

    img_wrapper.selectAll("img")
        .data(d => [d.before_path, d.after_path])
        .join('img')
        .attr("src", p => path_prefix + p)
        .attr("width", image_width)
        .style("margin-right", (d, i) => (i == 0 ? pair_mh + "px" : "0px"))
        .on('dblclick', d => {
            $.getJSON($SCRIPT_ROOT + '/details/' + d, {              
              }, function(data) {
                details_modal(data)
              });
        })

    return {
        set_description: function (f) {
            description = f
            if (description)
                wrappers.call(description)
        }
    }

}

var my_socket = io('/ocr');

my_socket.on('connect', () => {
    my_socket.emit('change_area', 'bbq', (d) => {
        console.log(d)
        d3.select("#sel_video")
            .selectAll('option')
            .data(d)
            .join('option')
            .attr('value', dd => dd)
            .text(dd => dd.split('/').slice(-1)[0])
    })
})

function getSelectValues(select) {
    var result = [];
    var options = select && select.options;
    var opt;

    for (var i = 0, iLen = options.length; i < iLen; i++) {
        opt = options[i];

        if (opt.selected) {
            result.push(opt.value || opt.text);
        }
    }
    return result;
}

function change_area() {
    var x = document.getElementById("sel_area").value;
    my_socket.emit('change_area', x, (d) => {
        d3.select("#sel_video")
            .selectAll('option')
            .data(d)
            .join('option')
            .attr('value', dd => dd)
            .text(dd => dd.split('/').slice(-1)[0])
    })
}

var selections = []
var eaten = 'all'
var dish = 'all'
var mode = 'ocr'
var rice = 'all'
var vegetable = 'all'
var meat = 'all'

function change_video() {
    var sel = document.getElementById("sel_video");
    selections = getSelectValues(sel)
}

function change_eaten() {
    eaten = document.getElementById("sel_eaten").value;
}

function change_dish() {
    dish = document.getElementById("sel_dish").value;
}

function change_rice() {
    rice = document.getElementById("sel_rice").value;
}

function change_vegetable() {
    vegetable = document.getElementById("sel_vegetable").value;
}

function change_meat() {
    meat = document.getElementById("sel_meat").value;
}

function change_mode() {
    mode = document.getElementById("sel_mode").value;
}

function filter() {
    my_socket.emit('change_video', {
        selections,
        eaten,
        dish,
        rice,
        vegetable,
        meat,
        low: document.getElementById("low").value,
        high: document.getElementById("high").value,
        random: document.getElementById("random").checked,
        all_area: document.getElementById("all_area").checked,
        mode
    }, (trays) => {
        console.log(trays)
        if (mode == 'ocr') {
            g = gallery('#gallery_container', trays)
            g.set_description(wrappers => {
                wrappers.selectAll("text")
                    .data(d => [d.ocr])
                    .join("text")
                    .text(d => d)
                    .style("text-align", "center")
            })
            g.set_e2(function (event) {
                if (isFinite(event.key)) {
                    digit = event.key
                    if (ocr[g.cur] === undefined) {
                        ocr[g.cur] = ''
                    }
                    if (ocr[g.cur].length < 4)
                        ocr[g.cur] += digit
                    $(".item" + g.cur + " text")[0].textContent = ocr[g.cur]
                }
                else if (event.key == "Backspace") {
                    text = $(".item" + g.cur + " text")[0].textContent
                    ocr[g.cur] = text.slice(0, text.length - 1)
                    $(".item" + g.cur + " text")[0].textContent = ocr[g.cur]
                }
                else if (event.key == "Delete") {
                    ocr[g.cur] = ''
                    $(".item" + g.cur + " text")[0].textContent = ocr[g.cur]
                }
            })
            data = trays
        }
        else if (mode == 'eaten') {
            g = gallery('#gallery_container', trays)
            g.set_description(wrappers => {
                wrappers.selectAll("text")
                    .data(d => {
                        if(d.eaten === true)
                            return ['E']
                        else if(d.eaten === false)
                            return ['U']
                        return []
                    })
                    .join("text")
                    .text(d => d)
                    .style("text-align", "center")
            })
            g.set_e2(function (event) {
                if (event.key == 'U' || event.key == 'E') {
                    digit = event.key
                    if (ocr[g.cur] === undefined) {
                        ocr[g.cur] = ''
                    }
                    if (ocr[g.cur].length < 1)
                        ocr[g.cur] += digit
                    $(".item" + g.cur + " text")[0].textContent = ocr[g.cur]
                }
                else if (event.key == "Backspace") {
                    text = $(".item" + g.cur + " text")[0].textContent
                    ocr[g.cur] = text.slice(0, text.length - 1)
                    $(".item" + g.cur + " text")[0].textContent = ocr[g.cur]
                }
                else if (event.key == "Delete") {
                    ocr[g.cur] = ''
                    $(".item" + g.cur + " text")[0].textContent = ocr[g.cur]
                }
            })
            data = trays
        }
        else if (mode == 'dish') {
            var color = d3.scaleOrdinal()
                .domain(["bbq", "two_choices", "delicacies", "japanese", "teppanyaki", "veggies"])
                .range(["rgb(252,186,3)", "rgb(122,149,255)", "rgb(235,157,252)"
                    , "rgb(255,127,122)", "rgb(248,252,157)", "rgb(131,255,122)"])
                .unknown("rgb(219,219,219)")
            var dish_map = ['bbq', 'japanese', 'teppanyaki', 'two_choices', 'delicacies']
            g = gallery('#gallery_container', trays)
            g.set_description(wrappers => {
                wrappers.selectAll(".dish_tag")
                    .data(d => [d.dish])
                    .join("div")
                    .attr("class", "dish_tag")
                    .style('background', d => color(d))
                    .text(d => d)
                    .style("text-align", "center")
            })
            g.set_e2(function (event) {
                if (['1', '2', '3', '4', '5'].includes(event.key)) {
                    digit = event.key
                    if (ocr[g.cur] === undefined) {
                        ocr[g.cur] = ''
                    }                    
                    ocr[g.cur] = dish_map[parseInt(digit) - 1]
                    d3.select('.item' + g.cur).select(".dish_tag")
                        .data(d => [ocr[g.cur]])
                        .join("div")
                        .attr("class", "dish_tag")
                        .style('background', d => color(d))
                        .text(d => d)
                        .style("text-align", "center")
                }
                else if (event.key == "Backspace" || event.key == "Delete") {
                    ocr[g.cur] = ''
                    $(".item" + g.cur + " .dish_tag").empty()
                }
            })
            data = trays
        }
        else if (mode == 'seg') {           
            g = pair_gallery('#gallery_container', trays.map(d => {return {
                before_path: d.path,
                after_path: d.mask
            }}))            
            data = []
        }
        else if (mode == 'pair') {           
            g = pair_gallery('#gallery_container', trays.map(d => {return {
                before_path: d.before,
                after_path: d.after,
                ocr: d.ocr
            }}))
            g.set_description(wrappers => {
                wrappers.selectAll("text")
                    .data(d => [d.ocr])
                    .join("text")
                    .text(d => d)
                    .style("text-align", "center")
            })            
            data = []
        }
        else if (mode == 'multilabel') {  
            
            var rect_width = 20
            var rect_height = 8
            var cls = ["tag_rice", "tag_vegetable", "tag_meat"]
            
            function draw_tag(svg) {
                var tag_y = 10                
        
                var before_tag = svg.selectAll(".tag")
                    .data(d => [d])
                    .join("g")
                    .attr("transform", "translate(" + 45 + "," + tag_y + ")")
                    .attr("class", "tag")
        
                before_tag.selectAll("rect")
                    .data(d => [d.rice, d.vegetable, d.meat].filter(e => e != null))
                    .join("rect")
                    .attr("x", (d, i) => rect_width * i)
                    .attr("y", d => rect_height * (2 - d))
                    .attr("width", rect_width)
                    .attr("height", d => rect_height * (d + 1))
                    .attr("class", (d, i) => cls[i])        
            }
        
            function tag(wrappers) {
                var svg = wrappers.selectAll("svg")
                    .data(d => [d])
                    .join("svg")
                    .attr("width", 150)
        
                draw_tag(svg)
            }

            g = gallery('#gallery_container', trays)
            g.set_description(tag)
            g.set_e2(function (event) {
                if (event.key == '1' || event.key == '2' || event.key == '3') {                              
                    digit = event.key
                    if (ocr[g.cur] === undefined) {
                        ocr[g.cur] = []
                    }     
                    if (ocr[g.cur].length < 3)
                        ocr[g.cur].push(digit)                   
                }
                else if (event.key == "Backspace") { 
                    if (ocr[g.cur] === undefined){
                        ocr[g.cur] = [(trays[g.cur].rice+1).toString()
                        , (trays[g.cur].vegetable+1).toString()
                        , (trays[g.cur].meat).toString()]  
                    }               
                    ocr[g.cur].pop()                  
                }
                else if (event.key == "Delete") {
                    ocr[g.cur] = []                    
                }
                d3.select(".item" + g.cur)
                    	.select('.tag')
                        .selectAll("rect")
                        .data(ocr[g.cur])
                    	.join("rect")
                    	.attr("x", (d, i) => rect_width * i)
                    	.attr("y", d => rect_height * (2 - (parseInt(d) - 1)))
                    	.attr("width", rect_width)
                    	.attr("height", d => rect_height * (parseInt(d)))
                    	.attr("class", (d, i) => cls[i]) 
            })
            data = trays
        }
    })
    ocr = {}
}

function count() {
    my_socket.emit('count', {
        selections,
        eaten,
        dish,
        rice,
        vegetable,
        meat,
        low: document.getElementById("low").value,
        high: document.getElementById("high").value,
        random: document.getElementById("random").checked,
        all_area: document.getElementById("all_area").checked,
        mode
    }, (num) => {
        alert(num)
    })
}

function submit() {
    new_ocr = {}
    for (const key in ocr) {
        new_ocr[data[key].path] = ocr[key]
    }
    console.log(new_ocr)
    my_socket.emit('submit', new_ocr, mode, (code) => {
        if (code != 0) {
            alert("Success!")
        } else {
            alert("Some error occured at server...")
        }
    })
}

