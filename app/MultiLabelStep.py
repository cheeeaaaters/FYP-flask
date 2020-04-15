from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from flask import render_template, url_for
import sys, os
from app import globs

path_to_multi_classifier = ''
sys.path.insert(1, path_to_multi_classifier)

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
            emit('display', self.convert_to_json(info), namespace='/multilabel_step')
            eventlet.sleep(0)
          
            #TODO: update input using info
            input.eaten = (info["preds"][0].item() == 1)
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/multilabel_step')

    #If you wish to add something to start...
    def start(self): 
        #Add something before calling super().start()
        #super().start()   
        obj = {            
            'percentage': 0.1,
            'before_path': url_for('static', filename='images/food.jpg'),
            'after_path': url_for('static', filename='images/food.jpg'),            
            'infer_time': 0.1,
            'pair_id': 0,
            'before_label': [1,2,2],
            'after_label': [0,1,0]
        }
        emit('display', obj, namespace='/multilabel_step')   

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

    @bind_socketio('/multilabel_step')
    def test(self, input):
        pass