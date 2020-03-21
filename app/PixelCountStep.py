from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio

class PixelCountStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 6
        self.context["step_name"] = "pixel_count_step"

    def start(self):
        pass

    def stop(self):
        pass

    def render(self):
        return 'Work In Progress.'

    @bind_socketio('/pixel_count_step')
    def step_process(self, input):
        pass