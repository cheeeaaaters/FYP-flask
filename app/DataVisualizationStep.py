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
    def q1(self):
        return [
            { 'type': "rice", 'count': 6 },
            { 'type': "vegetable", 'count': 2 },
            { 'type': "meat", 'count': 4 }
        ]

    @bind_socketio('/data_visualization_step')
    def q1_2(self):
        return [
            { 'type': "rice", 'count': 6 },
            { 'type': "vegetable", 'count': 2 },
            { 'type': "meat", 'count': 4 },
            { 'type': "background", 'count': 16 }            
        ]

    @bind_socketio('/data_visualization_step')
    def q2(self):
        return [
            { 'name': 'bbq', 'count': [10, 20, 40] },
            { 'name': 'two choices', 'count': [20, 30, 50] },
            { 'name': 'delicacies', 'count': [5, 6, 20] },
            { 'name': 'japanese', 'count': [12, 24, 20] },
            { 'name': 'teppanyaki', 'count': [5, 10, 20] }
        ]   

    @bind_socketio('/data_visualization_step')
    def q2_2(self):
        return [
            { 'name': 'bbq', 'count': [10, 20, 40, 30] },
            { 'name': 'two choices', 'count': [20, 30, 50, 0] },
            { 'name': 'delicacies', 'count': [5, 6, 20, 69] },
            { 'name': 'japanese', 'count': [12, 24, 20, 44] },
            { 'name': 'teppanyaki', 'count': [5, 10, 20, 65] }
        ]  

    @bind_socketio('/data_visualization_step')
    def q3(self):
        return [
            { 'type': "rice", 'count': 6 },
            { 'type': "vegetable", 'count': 2 },
            { 'type': "meat", 'count': 4 }
        ]

    @bind_socketio('/data_visualization_step')
    def q3_2(self):
        return [
            { 'type': "rice", 'count': 6 },
            { 'type': "vegetable", 'count': 2 },
            { 'type': "meat", 'count': 4 },
            { 'type': "background", 'count': 16 }            
        ]

    @bind_socketio('/data_visualization_step')
    def q4(self):
        return [
            { 'name': 'bbq', 'count': [10, 20, 40] },
            { 'name': 'two choices', 'count': [20, 30, 50] },
            { 'name': 'delicacies', 'count': [5, 6, 20] },
            { 'name': 'japanese', 'count': [12, 24, 20] },
            { 'name': 'teppanyaki', 'count': [5, 10, 20] }
        ]   

    @bind_socketio('/data_visualization_step')
    def q4_2(self):
        return [
            { 'name': 'bbq', 'count': [10, 20, 40, 30] },
            { 'name': 'two choices', 'count': [20, 30, 50, 0] },
            { 'name': 'delicacies', 'count': [5, 6, 20, 69] },
            { 'name': 'japanese', 'count': [12, 24, 20, 44] },
            { 'name': 'teppanyaki', 'count': [5, 10, 20, 65] }
        ]  

    @bind_socketio('/data_visualization_step')
    def q5(self):
        return [
            { 'name': 'bbq', 'before': 16, 'after': 4 },
            { 'name': 'bbq', 'before': 14, 'after': 5 },
            { 'name': 'bbq', 'before': 12, 'after': 6 },
            { 'name': 'japanese', 'before': 7, 'after': 4 },
            { 'name': 'japanese', 'before': 1, 'after': 8 }
        ]    