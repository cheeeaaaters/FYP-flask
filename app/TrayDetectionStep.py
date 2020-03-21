from app.Step import Step
from flask import render_template
from flask_socketio import emit
from .socketio_helper import bind_socketio
from fake.fake_tray_detection import FakeTrayDetection
from app import db
from app.DBModels import Video, Tray

class TrayDetectionStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 0
        self.context["step_name"] = "tray_detection_step"
        self.coroutine = self.step_process()
        print("Tray Detection Step Created!")

    def step_process(self):
        print("Start Process...")

        #TODO: init yolov3
        #TODO: Optionally call js to display loading bar  

        #get the inputs
        #TODO: Optionally can make video also an input stream
        videos = Video.query.all()

        #TODO: pass the input to yolov3
        #preresquisite: usage of yield
        #outputStream is a generator        
        outputStream = FakeTrayDetection.process(videos)

        #yolov3 returns:
        #tray with reference to video, area, time, image path, object_id(optional)
        #can be any form you feel convenient 
        for tray in outputStream:
            #TODO: update the html, call js 
            emit('display', self.convert_to_json(tray), namespace='/tray_detection_step')
            #Optional: attach a callback when client receives my signal
            #emit('display', self.convert_to_json(tray), namespace='/tray_detection_step', callback=something)
            #Example use case: when client internet dies, we may want to stop the process.

            #Optional: this code could be inside the callback
            #TODO: insert to database
            db.session.add(tray)
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

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
        return tray.id
    
    #bind_socketio is used to deal with messages sent from js
    #Example use case: configuration buttons specifc to the step
    @bind_socketio('/tray_detection_step')
    def test(self, input):
        pass