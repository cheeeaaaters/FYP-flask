from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from flask import render_template, url_for

class DataVisualizationStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 8
        self.context["step_name"] = "data_visualization_step"

    #If you wish to add something to start...
    def start(self): 
        #Add something before calling super().start()
        #super().start()   
        pass

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()     

    def render(self):
        return render_template('data_visualization_step.html')

    def render_sidebar(self):
        return render_template('data_visualization_step_sb.html')

    def requested(self):        
        emit('init_mc', namespace='/data_visualization_step')        

    def requested_sidebar(self):        
        emit('init_sb', namespace='/data_visualization_step')


    @bind_socketio('/data_visualization_step')
    def test(self, input):
        pass