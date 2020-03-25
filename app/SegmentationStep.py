from .Step import Step
from flask_socketio import emit
from flask import render_template
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray, SegmentationInfo
import sys, os
import eventlet

path_to_seg = "/home/ubuntu/FYP-Seg"
sys.path.insert(1, path_to_seg)
import detect as Seg

class SegmentationStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 5
        self.context["step_name"] = "segmentation_step"
        self.coroutine = self.step_process()
        print("Segmentation Step Created")

    def step_process(self):
        print("Start Process...")

        #get the inputs      
        input_trays = Tray.query.all()      

        #TODO: pass the input to model        
        outputStream = Seg.process(input_trays, backref=True)
        
        #The model returns information about the input image, segmentation image, pixel count...
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            emit('display', info, namespace='/segmentation_step')
            eventlet.sleep(0)
            
            #TODO: update input using info
            segmentation_info = SegmentationInfo(segmentation_path=info["mask"]
                                                ,total=info["pc_total"]
                                                ,rice=info["pc_1"]
                                                ,vegetable=info["pc_2"]
                                                ,meat=info["pc_3"])
            input.segmentation_info = segmentation_info
            db.session.add(segmentation_info)
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/segmentation_step')

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
        return {}

    #TODO select model to use
    @bind_socketio('/segmentation_step')
    def select_model(self, model):
        pass

    #TODO select loss
    @bind_socketio('/segmentation_step')
    def select_loss(self, loss):
        pass