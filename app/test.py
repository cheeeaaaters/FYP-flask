from flask import render_template, send_file
from app import app, socketio

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/test')
def testing():
    return render_template('data_visualization_step.html')

@app.route('/my_images/<path:filename>')
def get_images(filename):
    return send_file(filename)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))