from .Step import Step
from flask_socketio import emit
from flask import render_template
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray
import sys, os
import eventlet

path_to_eaten_classifier = '/home/ubuntu/eaten'
sys.path.insert(1, path_to_eaten_classifier)
import eaten_main as Classifier 

class ClassifyEatenStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 2
        self.context["step_name"] = "classify_eaten_step"
        self.coroutine = self.step_process()
        print("Classify Eaten Step Created")

    def step_process(self):
        print("Start Process...")

        #get the inputs        
        query = db.session.query(Tray)
        #TODO: Optional, may let user configure filter or not
        input_trays = query.all()
        #input_trays = query.filter_by(ocr == None)        

        #TODO: pass the input to classifier        
        outputStream = Classifier.process(input_trays, backref=True)
        
        #classifier returns information about the input image, and eaten
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            emit('display', self.convert_to_json(info), namespace='/classify_eaten_step')
            eventlet.sleep(0)
          
            #TODO: update input using info
            input.eaten = (info["preds"][0].item() == 1)
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/classify_eaten_step')

    #If you wish to add something to start...
    def start(self): 
        #Add something before calling super().start()
        super().start()      

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()     

    def render(self):
        return render_template('test_step.html')

    #TODO: convert tray to json to pass to js
    def convert_to_json(self, input):            
        return {
            "eaten": (input["preds"][0].item() == 1),
            "infer_time": input["infer_time"],
            "percentage": input["percentage"]
        }

    @bind_socketio('/classify_eaten_step')
    def test(self, input):
        pass