from .Step import Step
from flask_socketio import emit
from flask import render_template, url_for
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray
import sys
import os
from app import globs
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
        self.mode = 1
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
            info['mode'] = self.mode
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            yield

        self.stop()
        yield

        self.mode = 2

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
            info['mode'] = self.mode
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)
            yield

        self.stop()
        yield

        self.mode = 3

        # count.py
        '''
        output = {
            'regex': None,
            'ocr': None,
            'object_id': None,
            'percentage': 0
        }
        '''
        outputStream = Polling.process()
        for info in outputStream:
            info['mode'] = self.mode
            pattern = info['regex']
            info['paths'] = []
            for target in Tray.query.filter(Tray.path.like('%'+pattern+'%')).filter_by(object_id=info['object_id']).all():
                target.ocr = info['ocr']
                info['paths'].append(target.path)
            emit('display', info, namespace='/ocr_step')
            eventlet.sleep(0)        
            yield

        # TODO: update the html to indicate the process has finished
        from app.UIManager import main_content_manager
        main_content_manager.switch_to_step(globs.step_objects['ClassifyEatenStep'])
        self.mode = 1

    def start(self):        
        if self.started:            
            super.start()
        else:
            from app.UIManager import modal_manager            
            modal_manager.show(render_template('step_modal.html', num=Tray.query.filter_by(ocr=None).count()))   

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

    @bind_socketio('/ocr_step')
    def modal_status(self, status):  
        if status['code'] != 0:
            self.started = True
            super.start()
            
