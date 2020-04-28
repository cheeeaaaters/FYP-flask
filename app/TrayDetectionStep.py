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
from app import globs
from collections import defaultdict

path_to_yolo = '/home/ubuntu/CanteenPreProcessing'
sys.path.insert(1, path_to_yolo)
#import object_tracker_4 as Yolo

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
        self.limit = 3
        print("Tray Detection Step Created!")

    def step_process(self):
        print("Start Process...")

        def limit_buffer(buf):
            for obj_id in buf:
                if len(buf[obj_id]) > self.limit:                    
                    step = (len(buf[obj_id]) - 1) / (self.limit - 1)
                    b = []
                    for i in range(self.limit):
                        b.append(buf[obj_id][int(i*step)])
                    buf[obj_id] = b
                    
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

            buffer = defaultdict(lambda: [])

            # yolov3 returns:
            # can be any form you feel convenient
            for tray in outputStream:                

                if tray["path"] != None:

                    tray['name'] = os.path.basename(tray["path"])
                    tray['video_path'] = video.path
                    tray['area'] = area
                    tray['date_time'] = (
                        date_start+delta*tray["percentage"]).strftime("%d-%b-%Y (%H:%M:%S.%f)")

                    info_dict = {
                        'path': tray["path"],
                        'object_id': tray["obj_id"],
                        'video': video,
                        'area': area,
                        'date_time': date_start+delta*tray["percentage"]
                    }
                    buffer[tray["obj_id"]].append(info_dict)
                    #print(tray["obj_id"], buffer[tray["obj_id"]])
                    
                    # TODO: update the html, call js
                    emit('display', tray, namespace='/tray_detection_step')
                    # Optional: attach a callback when client receives my signal
                    # emit('display', self.convert_to_json(tray), namespace='/tray_detection_step', callback=something)
                    # Example use case: when client internet dies, we may want to stop the process.

                    #print("One Loop Pass")

                else:
                    emit('display', tray, namespace='/tray_detection_step')

                # It will wait on this yield statement
                yield
            
            
            limit_buffer(buffer)
            for t in buffer:
                for info_dict in buffer[t]:
                    # TODO: insert to database
                    same_tray = Tray.query.filter_by(path=info_dict['path'])
                    if not same_tray.first():
                        new_tray = Tray(**info_dict)
                        db.session.add(new_tray)
                    else:
                        del info_dict['video']
                        same_tray.update(info_dict)
                        same_tray.video = video

            db.session.commit()
                    
        #from app.UIManager import main_content_manager
        # main_content_manager.switch_to_step(globs.step_objects['OCRStep'])

    # If you wish to add something to start...
    def start(self):        
        if self.started:            
            super().start()
        else:
            count = 0
            for r, _, files in os.walk(os.path.join(path_to_yolo, 'data/videos')):
                for f in files:
                    count += 1
            from app.UIManager import modal_manager
            modal_manager.show(render_template('step_modal.html', num=count))   
     
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

    @bind_socketio('/tray_detection_step')
    def modal_status(self, status):
        start = datetime(2019, 9, 10, 12)
        end = datetime(2019, 9, 10, 3)
        if status['code'] != 0:
            for r, _, files in os.walk(os.path.join(path_to_yolo, 'data/videos')):
                for f in files:
                    if Video.query.filter_by(path = os.path.join(r, f)).first() == None:                        
                        print("Loaded video: " + os.path.join(r, f))
                        v = Video(path = os.path.join(r, f))
                        (area, date_start, date_end) = self.convert_video(v)
                        if start <= date_start <= end:  
                            print("Loaded video: " + os.path.join(r, f))                          
                            db.session.add(v)
                            db.session.commit() 
            self.started = True
            self.start()
            
    @bind_socketio('/tray_detection_step')
    def change_limit(self, val):        
        self.limit = val