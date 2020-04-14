from app.Step import Step
from flask import render_template, url_for
from flask_socketio import emit
from .socketio_helper import bind_socketio
from fake.fake_tray_detection import FakeTrayDetection
from app import db
from app.DBModels import Video, Tray
from datetime import datetime
import sys
import os
import glob

path_to_yolo = '/home/ubuntu/CanteenPreProcessing'
sys.path.insert(1, path_to_yolo)

'''
    output = {
        'path': None,
        'obj_id': 0,
        'count': count,
        'percentage': 0,
        'infer_time': 0,
        'name': ...,
        'video_path': ...,
        'area': ...,
        'date_time': ...,
    }
'''

class TrayDetectionStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 0
        self.context["step_name"] = "tray_detection_step"
        self.coroutine = self.step_process()
        print("Tray Detection Step Created!")

    def step_process(self):
        print("Start Process...")
        import object_tracker_4 as Yolo

        # get the inputs
        # TODO: Optionally can make video also an input stream
        videos = Video.query.all()

        for video in videos:
            # TODO: pass the input to yolov3
            # preresquisite: usage of yield
            # outputStream is a generator
            outputStream = Yolo.process([video])
            # outputStream = []
            (area, date_start, date_end) = self.convert_video(video)
            delta = date_end - date_start

            # yolov3 returns:
            # can be any form you feel convenient
            for tray in outputStream:

                if tray["path"] != None:

                    tray['name'] = os.path.basename(tray["path"])
                    tray['video_path'] = video.path
                    tray['area'] = area
                    tray['date_time'] = (
                        date_start+delta*tray["percentage"]).strftime("%d-%b-%Y (%H:%M:%S.%f)")

                    # TODO: update the html, call js
                    emit('display', tray, namespace='/tray_detection_step')
                    # Optional: attach a callback when client receives my signal
                    # emit('display', self.convert_to_json(tray), namespace='/tray_detection_step', callback=something)
                    # Example use case: when client internet dies, we may want to stop the process.

                    # Optional: this code could be inside the callback
                    # TODO: insert to database
                    info_dict = {
                        'path': tray["path"],
                        'object_id': tray["obj_id"],
                        'video': video,
                        'area': area,
                        'date_time': date_start+delta*tray["percentage"]
                    }
                    
                    same_tray = Tray.query.filter_by(path=new_tray.path).first()
                    if not same_tray:
                        new_tray = Tray(**info_dict)
                        db.session.add(new_tray)
                    else:
                        same_tray.update(info_dict)
                    
                    db.session.commit()
                    print("One Loop Pass")

                # It will wait on this yield statement
                yield
        from app.UIManager import main_content_manager
        main_content_manager.switch_to_step(globs.step_objects['OCRStep'])

    # If you wish to add something to start...
    def start(self):
        if self.started:            
            super.start()
        else:
            from app.UIManager import modal_manager
            modal_manager.show(render_template('step_modal.html', num=Video.query.count()))           
            

    # If you wish to add something to stop...
    def stop(self):
        # Add something before calling super().stop()
        super().stop()

    def render(self):
        return render_template('tray_detection_step.html')

    def render_sidebar(self):
        return render_template('tray_detection_step_sb.html')

    def requested(self):
        emit('init_mc', namespace='/tray_detection_step')

    def requested_sidebar(self):
        emit('init_sb', namespace='/tray_detection_step')

    # TODO: convert tray to json to pass to js
    def convert_to_json(self, tray):
        return {
            'name': os.path.basename(tray["path"]),
            'path': tray["path"],
            'percentage': tray["percentage"],
            'infer_time': tray["infer_time"],
        }

    def convert_video(self, video):
        path_parts=os.path.normpath(video.path).split(os.path.sep)
        name=path_parts[-1].split('.')[0]
        area=path_parts[-2]
        dates=path_parts[-3]

        date_parts=dates.split('_')
        year=int(date_parts[1])
        month=int(date_parts[2])
        day=int(date_parts[3])

        parts=name.split('-')
        start=parts[-2]
        end=parts[-1]
        def get_hour_min(i):
            minutes=int(i)/60
            hours=int(minutes)//60
            rmd=int(minutes % 60)
            if rmd < 30:
                hour=7 + hours
                minute=30 + rmd
            else:
                hour=8 + hours
                minute=(30 + rmd) % 60
            return (hour, minute)

        hour_start, min_start=get_hour_min(start)
        date_start=datetime(year, month, day, hour_start, min_start)
        hour_end, min_end=get_hour_min(end)
        date_end=datetime(year, month, day, hour_end, min_end)

        return (area, date_start, date_end)

    @bind_socketio('/modal')
    def modal_status(self, status):        
        if status['step'] == "TrayDetectionStep" and status['code'] != 0:
            super.start()
            self.started = True
