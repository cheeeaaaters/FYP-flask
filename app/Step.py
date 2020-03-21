from flask_socketio import emit
from .socketio_helper import bind_socketio
#from app import globals

class Step():

    def __init__(self):
        print("Empty Step Created!")
        self.context = {
            "step_id": -1,
            "step_name": "no_step"
        }
        self.running = False
        self.coroutine = None

    #This function will be called when you press the start button
    def start(self): 
        print("step start!")
        #running will be inherited from Step, it is controlled by NavButtonManager
        while(self.running):
            try:
                next(self.coroutine)
            except StopIteration:
                #new coroutine
                self.coroutine = self.step_process()
                break
            except:
                print('BBBBBBUUUUUUUUUUGGGGGGGGGGG')
                break
        if self.running:
            self.stop()        

    #This function will be called when you press the stop button
    def stop(self):
        self.running = False
        print("step stop!") 

    #should return an HTML string
    #you could use the flask render template to convert Jinjia to Html
    #will be substituted to the main content
    def render(self):
        return 'Work In Progress.'
    
    #Examples for how to use bind_socketio
    #binds the decorated function to THE global object of this step
    #which is created automatically
    #Syntax:
    '''
    @bind_socketio(namespace='/something')
    def function_name(self, arg1, arg2, ...):
        processing....
        emit('event_name', reponse, namespace='/something') -> initiate events, used for replying
        return r1, r2, ... -> passed to callback function in js, used to indicate success/fail 
        #see socketio for more details
    '''
    #On the js side
    '''
    <script type="text/javascript" charset="utf-8">
        var socket = io(/something);
        socket.on('event_name1', function(response1, response2, ...) {
            socket.emit('event_name2', args, callback);
        });
    </script>
    '''
    #Note: Sometime when testing, you may need to press cltr_shift_R on browser for it to reload.
