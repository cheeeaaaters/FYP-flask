from flask import render_template
from app import app, socketio

@app.route('/')
def index():
    return render_template('base.html')
    #print(type(a))
    #return "<h1>HELLO</h1>"

@app.route('/test')
def testing():
    return 'hello from asdasd another file'

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))