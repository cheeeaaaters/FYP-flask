from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio

class PairStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 3
        self.context["step_name"] = "pair_step"

    def step_process(self):
        print("Start Process...")

        #get the inputs        
        query = db.session.query(Tray)        
        input_trays = query.filter_by(
            ocr != None,
            eaten != None,
            segmentation_info != None
        )        

        #TODO: pass the input to model        
        outputStream = []
        
        #returns information about the input image, segmentation image, pixel count...
        #can be any form you feel convenient 
        for (input, info) in outputStream:
            #TODO: update the html, call js 
            emit('display', self.convert_to_json(input), namespace='/pair_step')
            #Optional: attach a callback when client receives my signal
            #emit('display', self.convert_to_json(input), namespace='/pair_step', callback=something)
            
            #TODO: add pair to database
            #TODO: algorithm!
            db.session.commit()

            print("One Loop Pass")
            #It will wait on this yield statement
            yield

        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/pair_step')

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

    @bind_socketio('/pair_step')
    def test(self, input):
        pass