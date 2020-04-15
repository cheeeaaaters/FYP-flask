from .Step import Step
from flask_socketio import emit
from flask import render_template, url_for
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray
import sys, os
import eventlet

path_to_eaten_classifier = '/home/ubuntu/eaten'
sys.path.insert(1, path_to_eaten_classifier)

'''
output = {
        "preds": None,
        "infer_time": 0,
        "percentage": 0
    }
'''

class ClassifyEatenStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 2
        self.context["step_name"] = "classify_eaten_step"
        self.coroutine = self.step_process()
        print("Classify Eaten Step Created")

    def step_process(self):
        print("Start Process...")
        import eaten_main as Classifier 

        #get the inputs        
        query = db.session.query(Tray)
        #TODO: Optional, may let user configure filter or not
        input_trays = query.filter_by(eaten=None)
        #input_trays = query.filter_by(ocr=None)        

        #TODO: pass the input to classifier        
        outputStream = Classifier.process(input_trays, backref=True)
        
        #classifier returns information about the input image, and eaten
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            info["eaten"] = (info["preds"][0].item() == 1)
            emit('display', info, namespace='/classify_eaten_step')
            eventlet.sleep(0)
          
            #TODO: update input using info
            input.eaten = (info["preds"][0].item() == 1)
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

    #If you wish to add something to start...
    def start(self): 
        if self.started:            
            super.start()
        else:
            from app.UIManager import modal_manager
            modal_manager.show(render_template('step_modal.html', num=Tray.query.filter_by(eaten=None).count()))   

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()     

    def render(self):
        return render_template('classify_eaten_step.html')

    def render_sidebar(self):
        return render_template('classify_eaten_step_sb.html')

    def requested(self):        
        emit('init_mc', namespace='/classify_eaten_step')        

    def requested_sidebar(self):        
        emit('init_sb', namespace='/classify_eaten_step')

    @bind_socketio('/modal')
    def modal_status(self, status):        
        if status['step'] == "ClassifyEatenStep" and status['code'] != 0:
            self.started = True
            super.start()