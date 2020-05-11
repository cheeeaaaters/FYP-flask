from .Step import Step
from flask import render_template, url_for
from flask_socketio import emit
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray
import sys, os
from app import globs
import eventlet

path_to_dish_classifier = '/home/ubuntu/dish'
sys.path.insert(1, path_to_dish_classifier)

'''
output = {
        "preds": None,
        "infer_time": 0,
        "percentage": 0
    }
'''

class ClassifyDishStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 4
        self.context["step_name"] = "classify_dish_step"        
        self.dish_map = ["bbq", "japanese", "teppanyaki", "two_choices", "delicacies"]
        self.coroutine = self.step_process()
        print("Classify Dish Step Created")

    def new_dish(self, eaten, area, dish):
        if (area != 'main_return_area') and (area != 'side_return_area') and (area != 'side_return_area_2') and (area != 'teppanyaki'):
            return area 
        elif area == 'teppanyaki':
            if eaten:
                return dish
            else:
                return 'teppanyaki'
        else:
            if eaten:
                return dish
            else:
                return None
        return None

    def step_process(self):
        print("Start Process...")
        import dish_main as Classifier 

        #get the inputs        
        query = db.session.query(Tray)
        #TODO: Optional, may let user configure filter or not
        #input_trays = query.filter_by(dish=None).all()   
        input_trays = query.all()
        #input_trays = query.filter_by(ocr=None)        

        #TODO: pass the input to classifier        
        outputStream = Classifier.process(input_trays, backref=True)
        
        #classifier returns information about the input image, and dish
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            info['name'] = os.path.basename(input.path)
            info['path'] = input.path
            info["dish"] = self.dish_map[info["preds"][0].item()]
            del info["preds"]
            emit('display', info, namespace='/classify_dish_step')
            #Optional: attach a callback when client receives my signal
            #emit('display', self.convert_to_json(input), namespace='/classify_dish_step', callback=something)

            #TODO: update input using info
            input['dish'] = self.new_dish(input.eaten, input.area, input['dish'])
            input.dish = info["dish"]
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield
        
        #from app.UIManager import main_content_manager
        #main_content_manager.switch_to_step(globs.step_objects['SegmentationStep'])

    #If you wish to add something to start...
    def start(self): 
        if self.started:            
            super().start()
        else:
            from app.UIManager import modal_manager
            modal_manager.show(render_template('step_modal.html', num=Tray.query.count()))

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()       
        
    def render(self):
        return render_template('classify_dish_step.html')

    def render_sidebar(self):        
        return render_template('classify_dish_step_sb.html')

    def requested(self):        
        emit('init_mc', namespace='/classify_dish_step')        

    def requested_sidebar(self):    
        emit('init_sb', namespace='/classify_dish_step')

    def clean_up(self):
        for t in Tray.query.all():
            t.dish = None
        db.session.commit()

    @bind_socketio('/classify_dish_step')
    def modal_status(self, status):        
        if status['code'] != 0:
            self.started = True
            self.start()
        else:
            self.stop()
