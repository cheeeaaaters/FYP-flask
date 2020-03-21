from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio

class MultiLabelStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 7
        self.context["step_name"] = "multi_label_step"

    def start(self):
        pass

    def stop(self):
        pass

    def render(self):
        return 'Work In Progress.'

    @bind_socketio('/multi_label_step')
    def step_process(self, input):
        pass