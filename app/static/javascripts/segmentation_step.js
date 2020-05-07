var segmentation_socket = io('/segmentation_step');

(function () {

    var segmentation_progess_bar;
    var segmentation_infer_time_chart;
    var segmentation_gallery;
    var two_images;

    var i = 1;

    segmentation_socket.on('display', function (tray) {
        segmentation_progess_bar.update(tray.percentage * 100)
        segmentation_gallery.append({
            mask: tray.mask,
            orig: tray.orig,
            path: tray.blend
        })
        segmentation_infer_time_chart.add({ x: i, y: tray.infer_time })
        i += 1;
    });

    segmentation_socket.on('init_sb', function () {
        segmentation_progess_bar = radialProgress('.process_percentage')
        segmentation_progess_bar.update(0)

        options = {
            hrnet: $("#hrnet"),
            bisenet: $("#bisenet"),
            tensorrt: $("#tensorrt")
        }

        for (const model in options) {
            options[model].on('click', () => {
                for (const key in options) {
                    options[key].removeClass('active')
                }
                options[model].addClass('active')
                segmentation_socket.emit('select_model', model)
            })
        }

    })

    segmentation_socket.on('init_mc', function () {
        var segmentation_tabs = {
            introduction: $("#segmentation_introduction_content"),
            gallery: $("#segmentation_seg_content"),
            pixel_info: $("#segmentation_pixel_info_content"),
            infer_time: $("#segmentation_infer_time_content")
        }

        $("#segmentation_introduction").on('click', function () {
            for (const key in segmentation_tabs) {
                segmentation_tabs[key].addClass('hidden')
            }
            segmentation_tabs.introduction.removeClass('hidden')
        })

        $("#segmentation_seg").on('click', () => {
            for (const key in segmentation_tabs) {
                segmentation_tabs[key].addClass('hidden')
            }
            segmentation_tabs.gallery.removeClass('hidden')
        })

        $("#segmentation_pixel_info").on('click', () => {
            for (const key in segmentation_tabs) {
                segmentation_tabs[key].addClass('hidden')
            }
            segmentation_tabs.pixel_info.removeClass('hidden')
        })

        $("#segmentation_infer_time").on('click', () => {
            for (const key in segmentation_tabs) {
                segmentation_tabs[key].addClass('hidden')
            }
            segmentation_tabs.infer_time.removeClass('hidden')
        })

        var gallery_config = {
            row_size: 1,
            max_size: 20,
            image_width: 900,
            mv: 30,
            absolute_path: true,
            load_more: true,
            no_cache: true
        }

        segmentation_gallery = gallery("#segmentation_gallery", [], gallery_config)
        segmentation_gallery.set_on_click(d => {
            two_images.update([d.orig, d.mask])
            for (const key in segmentation_tabs) {
                segmentation_tabs[key].addClass('hidden')
            }
            segmentation_tabs.pixel_info.removeClass('hidden')
        })

        two_images = cross_point("#cross_point_container")
        segmentation_infer_time_chart = lineChart('#segmentation_infer_time_graph', [], { width: 1000, height: 300 })

        for (const key in segmentation_tabs) {
            segmentation_tabs[key].addClass('hidden')
        }
        segmentation_tabs.introduction.removeClass('hidden')

    })

})()
