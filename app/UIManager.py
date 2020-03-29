from app import globs
from app import socketio
from flask_socketio import emit

#Python interface of main content for js
class MainContentManager():

    first_step = globs.step_objects['TrayDetectionStep']    

    def __init__(self):
        self.change_cur_to(self.first_step)

    def change_cur_to(self, step_obj):
        globs.cur_step = step_obj

    #js requests html
    def request_first_step(self):
        return self.request_step(self.first_step)

    #js requests html
    def request_step(self, step_obj):
        if step_obj != None:
            return step_obj.render()
        else:
            return 'step object is not created.'
    
    #python function to communicate to the main content ui
    def switch_to_first_step(self):  
        def cb():
            self.change_cur_to(self.first_step)
            self.first_step.requested()
        emit('request', self.request_first_step(), 
        callback=cb,
        namespace='/main_content')

    #python function to communicate to the main content ui
    def switch_to_step(self, step_obj):
        def cb():
            self.change_cur_to(step_obj)
            step_obj.requested()
        if step_obj != None:
            emit('request', self.request_step(step_obj), 
            callback=cb,
            namespace='/main_content')

##########################################################
main_content_manager = MainContentManager()

@socketio.on('request', namespace='/main_content')
def request_main_step():
    main_content_manager.change_cur_to(main_content_manager.first_step)
    return main_content_manager.request_first_step()

@socketio.on('request_step', namespace='/main_content')
def request_step(step):
    step = globs.step_objects[step]
    main_content_manager.change_cur_to(step)
    return main_content_manager.request_step(step)

@socketio.on('request_success', namespace='/main_content')
def request_success():    
    globs.cur_step.requested()
##########################################################

#Python interface of main content for js
class SidebarManager():

    first_step = globs.step_objects['TrayDetectionStep']    

    def __init__(self):
        self.change_cur_to(self.first_step)

    def change_cur_to(self, step_obj):
        globs.cur_step = step_obj

    #js requests html
    def request_first_step(self):
        return self.request_step(self.first_step)

    #js requests html
    def request_step(self, step_obj):
        if step_obj != None:
            return step_obj.render_sidebar()
        else:
            return ''
    
    #python function to communicate to the main content ui
    def switch_to_first_step(self):        
        def cb():
            self.change_cur_to(self.first_step)
            self.first_step.requested_sidebar()
        emit('request', self.request_first_step(), 
        callback=cb,
        namespace='/sidebar')

    #python function to communicate to the main content ui
    def switch_to_step(self, step_obj):
        def cb():
            self.change_cur_to(step_obj)
            step_obj.requested_sidebar()
        if step_obj != None:
            emit('request', self.request_step(step_obj), 
            callback=cb,
            namespace='/sidebar')

##########################################################
sidebar_manager = SidebarManager()

@socketio.on('request', namespace='/sidebar')
def request_main_step_sb():
    sidebar_manager.change_cur_to(sidebar_manager.first_step)
    return sidebar_manager.request_first_step()

@socketio.on('request_step', namespace='/sidebar')
def request_step_sb(step):
    step = globs.step_objects[step]
    sidebar_manager.change_cur_to(step)
    return sidebar_manager.request_step(step)

@socketio.on('request_success_sidebar', namespace='/sidebar')
def request_success_sb():
    globs.cur_step.requested_sidebar()
##########################################################

#Python interface of nav nuttons for js
class NavButtonManager():

    def __init__(self):
        pass
    
    def start_button_handler(self):
        cur = globs.cur_step
        if cur != None and not cur.running:
            cur.running = True
            cur.start()            

    def pause_button_handler(self):
        cur = globs.cur_step
        if cur != None and cur.running:
            cur.running = False
            cur.stop()            

##########################################################
nav_button_manager = NavButtonManager()

@socketio.on('start_button', namespace='/nav_button')
def start_button_handler():
    nav_button_manager.start_button_handler()

@socketio.on('pause_button', namespace='/nav_button')
def pause_button_handler():
    nav_button_manager.pause_button_handler()
##########################################################