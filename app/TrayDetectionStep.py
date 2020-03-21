from app.Step import Step
from flask import render_template
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
import object_tracker_4 as Yolo

class TrayDetectionStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 0
        self.context["step_name"] = "tray_detection_step"
        self.coroutine = self.step_process()
        print("Tray Detection Step Created!")
        '''
        for v in glob.glob("/home/ubuntu/CanteenPreProcessing/data/videos/**/*.mov", recursive=True):
            video = Video(path=v)
            db.session.add(video)
            db.session.commit()
        '''

    def step_process(self):
        print("Start Process...")

        #get the inputs
        #TODO: Optionally can make video also an input stream
        videos = Video.query.all()
        
        for video in videos:        
            #TODO: pass the input to yolov3
            #preresquisite: usage of yield
            #outputStream is a generator        
            outputStream = Yolo.process([video])    
            (area, date_start, date_end) = self.convert_video(video)        
            delta = date_end - date_start

            #yolov3 returns:
            #can be any form you feel convenient 
            for tray in outputStream:

                if tray["path"] != None:
                    #TODO: update the html, call js 
                    emit('display', self.convert_to_json(tray), namespace='/tray_detection_step')
                    #Optional: attach a callback when client receives my signal
                    #emit('display', self.convert_to_json(tray), namespace='/tray_detection_step', callback=something)
                    #Example use case: when client internet dies, we may want to stop the process.

                    #Optional: this code could be inside the callback
                    #TODO: insert to database
                    new_tray = Tray(path=tray["path"],
                                    object_id=tray["obj_id"],
                                    video=video,
                                    area=area,
                                    date_time=date_start+delta*tray["percentage"])
                    db.session.add(new_tray)
                    db.session.commit()

                    print("One Loop Pass")

                #It will wait on this yield statement
                yield
        
        '''
        outputStream = FakeTrayDetection.process(videos)
        for tray in outputStream:
            emit('display', tray.path, namespace='/tray_detection_step')
            print("One Loop Pass")
            yield
        '''
        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/tray_detection_step')
        

    #If you wish to add something to start...
    def start(self): 
        #Add something before calling super().start()
        super().start()      

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()       
        
    def render(self):
        return render_template('test_step.html', list=range(10))

    #TODO: convert tray to json to pass to js
    def convert_to_json(self, tray):        
        return {
            'path': tray["path"],
            'percentage': tray["percentage"]
        }

    def convert_video(self, video):        
        path_parts = os.path.normpath(video.path).split(os.path.sep)
        name = path_parts[-1].split('.')[0]
        area = path_parts[-2]
        dates = path_parts[-3]

        date_parts = dates.split('_')
        year = int(date_parts[1])
        month = int(date_parts[2])
        day = int(date_parts[3])

        parts = name.split('-')
        start = parts[-2]
        end = parts[-1]
        def get_hour_min(i):
            minutes = int(i)/60
            hours = int(minutes)//60
            rmd = int(minutes%60)
            if rmd < 30:
                hour = 7 + hours
                minute = 30 + rmd
            else:
                hour = 8 + hours
                minute = (30 + rmd)%60
            return (hour, minute)

        hour_start, min_start = get_hour_min(start) 
        date_start = datetime(year, month, day, hour_start, min_start)
        hour_end, min_end = get_hour_min(end) 
        date_end = datetime(year, month, day, hour_end, min_end)
        
        return (area, date_start, date_end)

    #bind_socketio is used to deal with messages sent from js
    #Example use case: configuration buttons specifc to the step
    @bind_socketio('/tray_detection_step')
    def test(self, input):
        pass