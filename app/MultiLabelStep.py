from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from flask import render_template, url_for
import sys, os
from app import globs
from app.DBModels import *

path_to_multi_classifier = ''
sys.path.insert(1, path_to_multi_classifier)

'''
output = {
            "before_rice_preds": None,
            "before_vegetable_preds": None,
            "before_meat_preds": None,
            "after_rice_preds": None,
            "after_vegetable_preds": None,
            "after_meat_preds": None,
            "before_rice_infer_time": 0,
            "before_vegetable_infer_time": 0,
            "before_meat_infer_time": 0,
            "after_rice_infer_time": 0,
            "after_vegetable_infer_time": 0,
            "after_meat_infer_time": 0,
            "percentage": 0
        }
'''

class MultiLabelStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 7
        self.context["step_name"] = "multilabel_step"
        self.coroutine = self.step_process()

    def step_process(self):
        print("Start Process...")
        import multilabel_main as Classifier 

        #get the inputs        
        query = db.session.query(Pair)
        #TODO: Optional, may let user configure filter or not
        input_pairs = query.filter(Pair.after_tray.multilabel_info == None
        & Pair.before_tray.dish != None & Pair.after_tray.dish != None).all()
        #input_trays = query.filter_by(ocr == None)        

        #TODO: pass the input to classifier        
        outputStream = Classifier.process(input_pairs, backref=True)
        
        for (input, info) in outputStream:

            json = {}
            
            json["percentage"] = info["percentage"]
            json["pair_id"] = input.id
            json["before_path"] = input.before_tray.path
            json["after_path"] = input.after_tray.path
            json["infer_time"] = 0
            json["before_label"] = []
            json["after_label"] = []
            for ba in ["before", "after"]:
                mlinfo = MultiLabelInfo()
                for food in ["rice", "vegetable", "meat"]:
                    json["infer_time"] += info[ba + "_" + food + "_" + "infer_time"]
                    pred = info[ba + "_" + food + "_" + "preds"]
                    l = 0 if pred == None else pred[0].item()
                    json[ba + "_label"].append(l)
                    setattr(mlinfo, food, l)
                getattr(input, ba + "_tray").multilabel_info = mlinfo
                db.session.commit()

            #TODO: update the html, call js 
            emit('display', json, namespace='/multilabel_step')
            eventlet.sleep(0)
          
            print("One Loop Pass")
            #It will wait on this yield statement
            yield

    #If you wish to add something to start...
    def start(self): 
        if self.started:            
            super().start()
        else:
            from app.UIManager import modal_manager
            modal_manager.show(render_template('step_modal.html', 
                num=Pair.query.filter(Pair.after_tray.multilabel_info == None
                & Pair.before_tray.dish != None & Pair.after_tray.dish != None).count()))         

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()     

    def render(self):
        return render_template('multilabel_step.html')

    def render_sidebar(self):
        return render_template('multilabel_step_sb.html')

    def requested(self):         
        emit('init_mc', namespace='/multilabel_step')        

    def requested_sidebar(self):        
        emit('init_sb', namespace='/multilabel_step')

    def clean_up(self):
        for p in Pair.query.all():
            p.multilabel_info = None
        MultiLabelInfo.query.delete()
        db.session.commit()        

    @bind_socketio('/multilabel_step')
    def modal_status(self, status):        
        if status['code'] != 0:
            self.started = True
            self.start()