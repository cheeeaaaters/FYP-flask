from collections import defaultdict

global step_objects
step_objects = defaultdict(lambda: None)

global cur_step
cur_step = None

global step_socketio_methods
step_socketio_methods = defaultdict(lambda: [])