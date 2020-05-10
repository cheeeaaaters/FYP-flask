import os
from flask_socketio import emit
from app import socketio
from app.DBModels import *
import glob

@socketio.on('get_fs', namespace='/fs')
def get_fs(path):
    print(path)
    l = []
    for file in sorted(glob.glob(path + '/*')):
        #print(file)
        if os.path.isdir(file):
            ext = 'dir'
        else:
            _, ext = os.path.splitext(file)
        l.append({
            'name': os.path.basename(file),
            'type': ext
        })
    return l


@socketio.on('submit', namespace='/fs')
def fs_submit(paths):
    try:
        count = 0
        for p in paths:
            if(Video.query.filter_by(path = p).first() == None):
                count += 1
                v = Video(path = p)
                db.session.add(v)
                db.session.commit()
        return count
    except:
        return -1