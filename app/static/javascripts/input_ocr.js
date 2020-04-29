var ocr = {

}

var data = []

function gallery(selection, tray_detection_data, config) {

    var config = config || {}
    var row_size = config.row_size || 6
    var image_width = config.image_width || 150
    var mh = config.mh || 30
    var mv = config.mv || 30
    var max_size = config.max_size || 20
    var load_more = (config.load_more === undefined) ? false : config.load_more
    var load_more_size = config.load_more_size || max_size
    var absolute_path = (config.absolute_path === undefined) ? true : config.absolute_path
    var no_cache = (config.no_cache === undefined) ? false : config.no_cache
    //var absolute_path = false
    var path_prefix = absolute_path ? '/my_images/' : ''
    var path_suffix = no_cache ? () => ('?time=' + get_time()) : () => ''

    var description = wrappers => {
        wrappers.selectAll("text")
            .data(d => [d.ocr])            
            .join("text")
            .text(d => d)
            .style("text-align", "center")
    }
    
    var onClick = (d, i) => {
        move_cur(i)
    }    

    var array_limit = config.array_limit || 100000

    var cur = 0

    var vwrapper = d3.select(selection)
        .append("div")
        .attr('class', 'vertical_wrapper center_wrapper')
        .attr('width', '100%')        

    vwrapper.append("div")
        .attr("class", "gallery")
        .style("width", (image_width + mh * 2) * row_size + "px")

    function update_gallery(data) {

        var gallery = d3.select(selection)
            .selectAll(".gallery")

        var wrappers = gallery.selectAll(".img_wrapper")
            .data(data, d => d.path)
            .join("div")
            .style("margin", mv + "px " + mh + "px")
            .attr("class", (d,i) => "img_wrapper " + i)
            .style("display", "flex")
            .style("flex-direction", "column")

        wrappers.selectAll("img")
            .data(d => [path_prefix + d.path + path_suffix()])
            .join("img")
            .attr("src", p => p)
            .attr("width", image_width)

        if (description)
            wrappers.call(description)

        if (onClick)
            wrappers.on('click', onClick)

        $("." + cur).removeClass('active')
        $("." + cur).addClass('active')

    }

    function move_cur(index, scroll) {
        $("." + cur).removeClass('active')
        index = Math.max(Math.min(index, tray_detection_data.length - 1), 0)
        $("." + index).addClass('active')
        if(scroll)
            $("." + index)[0].scrollIntoView()
        cur = index
    }

    update_gallery(tray_detection_data)

    if(load_more){
        var container = vwrapper
        .append("div")
        .attr("class", "load_more_button_container")

        container.append("a")        
        .on('click', () => {
            max_size += load_more_size
            data = tray_detection_data.slice(0, max_size)
            update_gallery(data)
        })
        .append("img")
        .attr("src", 'static/icons/three-dots.svg')
        .attr("width", "40px")
        .style("cursor", "pointer")
    }

    document.addEventListener('keydown', function(event) {
        if(event.keyCode == 37) {
            //alert('Left was pressed');
            event.preventDefault()
            move_cur(cur - 1, true)
        }
        else if(event.keyCode == 39) {
            //alert('Right was pressed');
            event.preventDefault()
            move_cur(cur + 1, true)
        }
        else if(event.keyCode == 38) {
            //alert('Up was pressed');   
            event.preventDefault()         
            move_cur(cur - row_size, true)
        }
        else if(event.keyCode == 40) {
            //alert('Down was pressed');
            event.preventDefault()
            move_cur(cur + row_size, true)
        }
    });

    document.addEventListener('keydown', function(event) {
        if(isFinite(event.key)) {
            digit = event.key
            if (ocr[cur] === undefined){
                ocr[cur] = ''
            }
            if (ocr[cur].length < 4)            
                ocr[cur] += digit
            $("." + cur + " text")[0].textContent = ocr[cur]
        }
        else if(event.key == "Backspace"){
            text = $("." + cur + " text")[0].textContent
            ocr[cur] = text.slice(0, text.length-1) 
            $("." + cur + " text")[0].textContent = ocr[cur]
        }
        else if(event.key == "Delete"){
            ocr[cur] = ''
            $("." + cur + " text")[0].textContent = ocr[cur]
        }        
    });

    return {
        append: function (path) {
            tray_detection_data.unshift(path)
            if (tray_detection_data.length > array_limit) {
                tray_detection_data.pop()
            }
            //data = tray_detection_data.slice(0, max_size)
            update_gallery(tray_detection_data)
        },
        set_description: function (f) {
            description = f
            update_gallery(tray_detection_data)
        },
        set_on_click: function (f) {
            onClick = f
            update_gallery(tray_detection_data)
        },
        extend: function (m) {
            max_size = m
            data = tray_detection_data.slice(0, max_size)
            update_gallery(data)
        }
    }

}

var my_socket = io('/ocr');

my_socket.on('connect', () => {
    my_socket.emit('change_area', 'bbq', (d) => {
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
  
    for (var i=0, iLen=options.length; i<iLen; i++) {
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

function change_video() {
    var sel = document.getElementById("sel_video");
    selections = getSelectValues(sel)    
}

function filter() {
    my_socket.emit('change_video', selections, (trays) => {
        gallery('#gallery_container', trays)
        data = trays
    })
    ocr = {}
}

function submit() {    
    new_ocr = {}
    for(const key in ocr){
        new_ocr[data[key].path] = ocr[key]
    }
    console.log(new_ocr)
    my_socket.emit('submit', new_ocr, (code) => {
        if(code != 0){
            alert("Success!")
        }else{
            alert("Some error occured at server...")
        }
    })
}

