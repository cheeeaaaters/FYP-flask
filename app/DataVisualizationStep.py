from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio

class DataVisualizationStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 8
        self.context["step_name"] = "data_visualization_step"

    def start(self):
        pass

    def stop(self):
        pass

    def render(self):
        return 'Work In Progress.'

    @bind_socketio('/data_visualization_step')
    def step_process(self, input):
        pass