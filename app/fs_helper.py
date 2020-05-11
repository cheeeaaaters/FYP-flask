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
def fs_submit(p):
    try:
        count = 0
        if os.path.isdir(p):
            for r, _, files in os.walk(p):
                for f in files:
                    if f.endswith(".mov") and Video.query.filter_by(path = os.path.join(r, f)).first() == None:                        
                        #print("Loaded video: " + os.path.join(r, f))
                        v = Video(path = os.path.join(r, f))                            
                        print("Loaded video: " + os.path.join(r, f))                          
                        db.session.add(v)
                        db.session.commit()
                        count += 1 
        elif p.endswith(".mov") and (Video.query.filter_by(path = p).first() == None):
            count += 1
            v = Video(path = p)
            db.session.add(v)
            db.session.commit()
        return count
    except:
        return -1