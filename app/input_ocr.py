from app import socketio
from flask_socketio import emit
from app import db
from app.DBModels import *

@socketio.on('connect', namespace='/ocr')
def connect():
    pass

@socketio.on('change_area', namespace='/ocr')
def change_area(area):    
    video_list = []
    for v in Video.query.filter(Video.path.like('%'+area+'%')).all():
        print(v)
        video_list.append(v.path)
    return video_list

@socketio.on('change_video', namespace='/ocr')
def change_video(vids):
    l = []
    '''
    for t in Tray.query.filter(Tray.video.has(Video.path.in_(vids))).all():
        info = {}
        info['path'] = t.path        
        info['ocr'] = t.ocr
        l.append(info)
    '''
    for t in range(100):
        info = {}
        info['path'] = "C:\\Users\\cheee\\Desktop\\UST\\fyp\\git_flask_app\\food_.jpg"      
        info['ocr'] = "1234"
        l.append(info)
    return l
        
@socketio.on('submit', namespace='/ocr')
def submit(ocr_map): 
    try:   
        for key, value in ocr_map.items():
            t = Tray.query.filter_by(path = key).first()
            if t != None:
                t.ocr = value if value != "" else None
                db.session.commit()
        return 1
    except:
        return 0
