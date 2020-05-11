/*
    name,
    type, //dir, mov, jpg...    
*/
var fs_socket = io('/fs')

var video_root = '/home/ubuntu/data/fyp/videos'

var fs_tree;
var cur_point;

function update_tree(files, prev) {
    files.forEach(f => {
        updated = {
            _path: cur_point._path + '/' + f.name,
            _prev: prev,
            _type: f.type
        }
        cur_point[f.name] = { ...cur_point[f.name], ...updated }
    })
    //console.log(fs_tree)
}

function update_tree_2(files, prev, cp) {
    files.forEach(f => {
        updated = {
            _path: cp._path + '/' + f.name,
            _prev: prev,
            _type: f.type,
            _loaded: false
        }
        cp[f.name] = { ...cp[f.name], ...updated }
    })
}

function collect_files(cp) {
    files = []
    for (var key in cp) {
        if (!key.startsWith('_')) {
            files.push({
                name: key,
                type: cp[key]._type,
                selected: cp[key]._selected
            })
        }
    }
    return files
}

function fs_init() {
    fs_tree = {
        _path: video_root,
        _prev: null,
        _type: 'dir',
        _selected: false,
        _loaded: false
    }
    cur_point = fs_tree
    fs_socket.emit('get_fs', video_root, (files) => {
        update_tree(files, cur_point)
        load_directory(files)
    })
}

function isAllTrue(flags) {
    for (let key in flags) {
        if (!flags[key])
            return false
    }
    return true
}

function load_selected_directories(root, cb, selectAll) {
    let flags = {}
    for (let key in root) {
        if (!key.startsWith('_') && (root[key]._type == 'dir') && (selectAll || root[key]._selected) && !(root[key]._loaded)) {
            flags[key] = false
        }
    }
    if (Object.keys(flags).length === 0) {
        cb()
        return
    }
    //let is important
    for (let key in root) {
        if (!key.startsWith('_')) {
            if ((root[key]._type == 'dir') && (selectAll || root[key]._selected) && !(root[key]._loaded)) {
                fs_socket.emit('get_fs', root[key]._path, (files) => {
                    update_tree_2(files, root, root[key])
                    load_selected_directories(root[key], () => {
                        flags[key] = true
                        root[key]._loaded = true
                        if (isAllTrue(flags)) {
                            cb()
                        }
                    }, true)
                })
            }
        }
    }
}

function collect_selected_files(root, selectAll) {
    let l = []
    for (var key in root) {
        if (!key.startsWith('_')) {
            if (root[key]._type == 'dir') {
                if (!selectAll) {
                    if (root[key]._selected) {
                        l = l.concat(collect_selected_files(root[key], true))
                    } else {
                        l = l.concat(collect_selected_files(root[key], false))
                    }
                } else {
                    l = l.concat(collect_selected_files(root[key], true))
                }
            }
            else if (selectAll || root[key]._selected) {
                l.push(root[key]._path)
            }
        }
    }
    return l
}

function submit_tree(root) {
    let count = 0
    for (var key of root) {
        if (!key.startsWith('_')) {
            if (root[key]._selected) {
                fs_socket.emit('submit', root[key]._path, (code) => {
                    count += code
                })
            }
            else {
                if (root[key]._loaded){
                    count += submit_tree(root[key])
                }               
            }
        }
    }
    return count 
}

function fs_submit() {
    submit_tree(fs_tree)
}

function fs_cancel() {
    modal_mng.hide()
}

function go_back() {
    if (cur_point._prev != null) {
        cur_point = cur_point._prev
        console.log(cur_point._path)
        loaded_files = collect_files(cur_point)
        //console.log(loaded_files)
        load_directory(loaded_files)
    } else {
        modal_mng.hide()
    }
}

function load_directory(files) {

    file_container = d3.select('.files_container')
        .selectAll('.file_container')
        .data(files)
        .join('div')
        .attr('class', 'file_container')
        .on("mouseover", (d, i, n) => { n[i].classList.add('fs_grey') })
        .on("mouseout", (d, i, n) => { n[i].classList.remove('fs_grey') })
        .on("dblclick", d => {
            if (d.type == 'dir') {
                cur_point = cur_point[d.name]
                cur_point._loaded = true
                console.log(cur_point._path)
                loaded_files = collect_files(cur_point)
                load_directory(files)
                fs_socket.emit('get_fs', cur_point._path, (files) => {
                    update_tree(files, cur_point)
                    files.forEach(f => {
                        f.selected = cur_point[f.name]._selected
                    })
                    load_directory(files)
                })
            }
        })

    file_container.selectAll('input')
        .data(d => [d])
        .join('input')
        .attr('type', 'checkbox')
        .attr('class', 'fs_checkbox')
        .property('checked', d => (d.selected === undefined ? false : d.selected))
        .on("change", (d, i, n) => {
            cur_point[d.name]._selected = n[i].checked
        })

    file_container.selectAll('img')
        .data(d => [d])
        .join('img')
        .attr('src', d => d.type == 'dir' ? 'static/icons/folder-fill.svg' : 'static/icons/file.svg')

    file_container.selectAll('span')
        .data(d => [d])
        .join('span')
        .text(d => d.name)

}

