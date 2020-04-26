from .Step import Step
from flask_socketio import emit
from flask import render_template, url_for
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray, SegmentationInfo
import sys, os
import eventlet
import shutil

path_to_seg = "/home/ubuntu/FYPSeg"
sys.path.insert(1, path_to_seg)
sys.path.insert(1, "/home/ubuntu")
#import detect as Seg
#import FYPSeg

class SegmentationStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 5
        self.context["step_name"] = "segmentation_step"
        self.coroutine = self.step_process()
        self.model = 'HRNet'
        print("Segmentation Step Created")

    def step_process(self):
        print("Start Process...")        

        #get the inputs      
        input_trays = Tray.query.filter_by(segmentation_info=None)      

        #TODO: pass the input to model        
        outputStream = Seg.process(input_trays, model=self.model, backref=True)
        
        #The model returns information about the input image, segmentation image, pixel count...
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            info['orig'] = input.path
            emit('display', info, namespace='/segmentation_step')
            eventlet.sleep(0)
            
            #TODO: update input using info
            segmentation_info = SegmentationInfo(segmentation_path=info["mask"]
                                                ,total=info["pc_total"]
                                                ,rice=info["pc_1"]
                                                ,vegetable=info["pc_2"]
                                                ,meat=info["pc_3"]
                                                ,other=info["pc_4"])
            input.segmentation_info = segmentation_info
            db.session.add(segmentation_info)
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

    # If you wish to add something to start...
    def start(self):
        if self.started:            
            super().start()
        else:
            from app.UIManager import modal_manager
            modal_manager.show(render_template('step_modal.html', num=Tray.query.filter_by(segmentation_info=None).count()))

    # If you wish to add something to stop...
    def stop(self):
        # Add something before calling super().stop()
        super().stop()

    def render(self):
        return render_template('segmentation_step.html')

    def render_sidebar(self):
        return render_template('segmentation_step_sb.html')

    def requested(self):        
        emit('init_mc', namespace='/segmentation_step')        

    def requested_sidebar(self):        
        emit('init_sb', namespace='/segmentation_step')

    def clean_up(self):
        for t in Tray.query.all():
            t.segmentation_info = None
        SegmentationInfo.query.delete()
        db.session.commit()
        try:
            shutil.rmtree(os.path.join(path_to_seg, "outputs"))            
        except OSError as e:
            print("Error removing directory")

    #TODO select model to use
    @bind_socketio('/segmentation_step')
    def select_model(self, model):
        if model == 'hrnet':
            self.model = 'HRNet'
        elif model == 'bisenet':
            self.model = 'BiSeNet'

    @bind_socketio('/segmentation_step')
    def modal_status(self, status):        
        if status['code'] != 0:
            self.started = True
            self.start()