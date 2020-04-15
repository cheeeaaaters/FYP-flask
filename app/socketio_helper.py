from app import socketio
from functools import partial
from app import globs
import sys

def get_class_str(method):
    return method.__qualname__.split('.')[0]

def bind_socketio(namespace='/'):
    def decorator(func):
        if (func, namespace) not in globs.step_socketio_methods[get_class_str(func)]:
            globs.step_socketio_methods[get_class_str(func)].append((func, namespace))
    return decorator

def add_socketio():
    for class_name in globs.step_socketio_methods.keys():    
        if globs.step_objects[class_name] == None:
            cls = getattr(sys.modules["app."+class_name], class_name)
            step = cls()
            step.cls_name = class_name
            globs.step_objects[class_name] = step
            for func, namespace in globs.step_socketio_methods[class_name]:                
                socketio.on_event(func.__name__, partial(func, step), namespace=namespace)
