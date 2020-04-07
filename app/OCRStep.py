from .Step import Step
from flask_socketio import emit
from flask import render_template, url_for
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray
import sys
import os
import eventlet

'''
import count as Polling
import demo as OCR
import preprocessing as PreProcessing
path_to_yolo = '/home/ubuntu/CanteenPreProcessing'
sys.path.insert(1, path_to_yolo)
path_to_ocr = '/home/ubuntu/CanteenPreProcessing/OCR/main'
sys.path.insert(1, path_to_ocr)
'''

class OCRStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 1
        self.context["step_name"] = "ocr_step"
        self.coroutine = self.step_process()
        print("OCR Step Created")

    def step_process(self):
        print("Start Process...")

        # get the inputs
        query = db.session.query(Tray)
        # TODO: Optional, may let user configure filter or not
        #input_trays = query.all()
        input_trays = query.filter_by(ocr=None).all()

        # TODO: pass the input to OCR
        # preprocessing.py
        '''
        output = {
            'paths': [],
            'percentage': 0,
            'time': 0
        }
        '''
        outputStream = PreProcessing.process(input_trays)
        for info in outputStream:
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            yield

        self.stop()
        yield

        # demo.py
        '''
        output = {
            'path': None,
            'percentage': 0,
            'locate_time': 0,
            'ocr_time': 0,
            'ocr_text': [],
            'err': False
        }
        '''
        outputStream = OCR.process()
        for info in outputStream:
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            yield

        self.stop()
        yield

        # count.py
        '''
        output = {
            'regex': None,
            'ocr': None,
            'object_id': None
        }
        '''
        outputStream = Polling.process()
        for info in outputStream:
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            pattern = info['regex']
            for target in Tray.query.filter(Tray.path.like('%'+pattern+'%')).filter_by(object_id=info['object_id']).all():
                target.ocr = info['ocr']
            yield

        # TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/ocr_step')

    # If you wish to add something to start...
    def start(self):
        # Add something before calling super().start()
        #super().start()
        obj = {
            'mode': 3,
            'percentage': 0.1,
            'path': url_for('static', filename='images/food.jpg'),
            'locate_time': 0.1,
            'ocr_time': 0.1,
            'ocr_text': ['a','b','c'],
            'ocr': "0001"
        }
        obj2 = {
            'mode': 1,
            'percentage': 0.1,
            'path': url_for('static', filename='images/food.jpg'),
            'locate_time': 0.1,
            'ocr_time': 0.1,
            'ocr_text': ['a','b','c'],
            'ocr': "0001"
        }
        emit('display', obj, namespace='/ocr_step')
        emit('display', obj2, namespace='/ocr_step')


    # If you wish to add something to stop...
    def stop(self):
        # Add something before calling super().stop()
        super().stop()

    def render(self):
        return render_template('ocr_step.html')

    def render_sidebar(self):
        return render_template('ocr_step_sb.html')

    def requested(self):        
        emit('init_mc', namespace='/ocr_step')        

    def requested_sidebar(self):        
        emit('init_sb', namespace='/ocr_step')

    # TODO: convert input to json to pass to js
    def convert_to_json(self, input):
        return {}

    @bind_socketio('/ocr_step')
    def test(self, input):
        pass
