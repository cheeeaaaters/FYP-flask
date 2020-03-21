from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from app import db
from app.DBModels import Tray

class SegmentationStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 5
        self.context["step_name"] = "segmentation_step"
        print("Segmentation Step Created")

    def step_process(self):
        print("Start Process...")

        #TODO: init chosen segmentation model
        #TODO: Optionally call js to display loading bar  

        #get the inputs        
        query = db.session.query(Tray)        
        input_trays = query.filter_by(ocr != None)        

        #TODO: pass the input to model        
        outputStream = []
        
        #The model returns information about the input image, segmentation image, pixel count...
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            emit('display', self.convert_to_json(input), namespace='/segmentation_step')
            #Optional: attach a callback when client receives my signal
            #emit('display', self.convert_to_json(input), namespace='/segmentation_step', callback=something)
            
            #TODO: update input using info
            #segmentation_info = ??
            #input.segmentation_info = segmentation_info
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
        return self.context["step_name"]

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