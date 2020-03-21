from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray

class ClassifyDishStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 4
        self.context["step_name"] = "classify_dish_step"

    def step_process(self):
        print("Start Process...")

        #TODO: init classfier
        #TODO: Optionally call js to display loading bar  

        #get the inputs        
        query = db.session.query(Tray)
        #TODO: Optional, may let user configure filter or not
        input_trays = query.all()
        #input_trays = query.filter_by(ocr == None)        

        #TODO: pass the input to classifier        
        outputStream = None
        
        #classifier returns information about the input image, and dish
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            emit('display', self.convert_to_json(input), namespace='/classify_dish_step')
            #Optional: attach a callback when client receives my signal
            #emit('display', self.convert_to_json(input), namespace='/classify_dish_step', callback=something)

            #TODO: update input using info
            #input.dish = ??
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/classify_dish_step')

    #If you wish to add something to start...
    def start(self): 
        #Add something before calling super().start()
        super().start()      

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()     

    def render(self):
        return 'Work In Progress.'

    #TODO: convert tray to json to pass to js
    def convert_to_json(self, input):        
        return {}

    @bind_socketio('/classify_dish_step')
    def test(self, input):
        pass