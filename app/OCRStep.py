from .Step import Step
from flask_socketio import emit
from flask import render_template
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray
import sys, os
import eventlet

path_to_yolo = '/home/ubuntu/CanteenPreProcessing'
sys.path.insert(1, path_to_yolo)
path_to_ocr = '/home/ubuntu/CanteenPreProcessing/OCR/main'
sys.path.insert(1, path_to_ocr)
import preprocessing as PreProcessing
import demo as OCR
import count as Polling

class OCRStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 1
        self.context["step_name"] = "ocr_step"
        self.coroutine = self.step_process()
        print("OCR Step Created")

    def step_process(self):
        print("Start Process...")

        #get the inputs        
        query = db.session.query(Tray)
        #TODO: Optional, may let user configure filter or not
        #input_trays = query.all()
        input_trays = query.filter_by(ocr=None).all()       
        '''
        #TODO: pass the input to OCR        
        outputStream = PreProcessing.process(input_trays)
        for info in outputStream:
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            yield

        self.stop()
        yield
        
        outputStream = OCR.process()
        for info in outputStream:
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            yield
        
        self.stop()
        yield
        '''
        outputStream = Polling.process()
        for info in outputStream:
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            pattern = info['regex']
            for target in Tray.query.filter(Tray.path.like('%'+pattern+'%')).filter_by(object_id=info['object_id']).all():
                target.ocr = info['ocr']
            yield
        
        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/ocr_step')

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

    #TODO: convert input to json to pass to js
    def convert_to_json(self, input):        
        return {}

    @bind_socketio('/ocr_step')
    def test(self, input):
        pass