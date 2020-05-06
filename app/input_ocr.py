from app import socketio
from flask_socketio import emit
from app import db
from app.DBModels import *
from  sqlalchemy.sql.expression import func, select

@socketio.on('connect', namespace='/ocr')
def connect():
    pass

@socketio.on('change_area', namespace='/ocr')
def change_area(area):    
    video_list = []
    for v in Video.query.filter(Video.path.like('%'+area+'%')).order_by(Video.path).all():
        #print(v)
        video_list.append(v.path)
    return video_list

@socketio.on('change_video', namespace='/ocr')
def change_video(obj):    
    l = []
    if obj['all_area']:
        q = db.session.query(Tray)
    else:    
        q = Tray.query.filter(Tray.video.has(Video.path.in_(obj['selections'])))
    if obj['mode'] == 'seg':
        q = q.filter(Tray.segmentation_info != None)
    if obj['dish'] != 'all':
        q = q.filter(Tray.dish == obj['dish'])
    if obj['eaten'] != 'all':
        obj['eaten'] = obj['eaten'] == 'eaten'
        q = q.filter(Tray.eaten == obj['eaten'])    
    if obj['rice'] != 'all':
        q = q.filter(Tray.multilabel_info != None).filter(Tray.multilabel_info.has(MultiLabelInfo.rice == int(obj['rice'])))
    if obj['vegetable'] != 'all':
        q = q.filter(Tray.multilabel_info != None).filter(Tray.multilabel_info.has(MultiLabelInfo.vegetable == int(obj['vegetable'])))
    if obj['meat'] != 'all':
        q = q.filter(Tray.multilabel_info != None).filter(Tray.multilabel_info.has(MultiLabelInfo.meat == int(obj['meat'])))
        
    if obj['random']:
        q = q.order_by(func.random())

    if obj['low'] != '' and obj['high'] != '':
        try:
            q = q.slice(int(obj['low']), int(obj['high'])) 
        except:
            pass   
    elif obj['low'] == '' and obj['high'] != '':
        try:
            q = q.limit(int(obj['high'])) 
        except:
            pass
    elif obj['low'] != '' and obj['high'] == '':
        try:
            q = q.offset(int(obj['low'])) 
        except:
            pass

    if obj['mode'] == 'ocr':
        for t in q.all():        
            info = {}
            info['path'] = t.path        
            info['ocr'] = t.ocr
            l.append(info)
    elif obj['mode'] == 'eaten':
        for t in q.all():        
            info = {}
            info['path'] = t.path        
            info['eaten'] = t.eaten
            l.append(info)
    elif obj['mode'] == 'dish':
        for t in q.all():        
            info = {}
            info['path'] = t.path        
            info['dish'] = t.dish
            l.append(info)
    elif obj['mode'] == 'seg':
        for t in q.all():        
            info = {}
            info['path'] = t.path 
            info['mask'] = t.segmentation_info.segmentation_path               
            l.append(info)
    elif obj['mode'] == 'pair':
        for p in Pair.query.all():        
            info = {}
            info['before'] = p.before_tray.path        
            info['after'] = p.after_tray.path
            info['ocr'] = p.ocr
            l.append(info)
    elif obj['mode'] == 'multilabel':
        for t in q.all():        
            info = {}
            info['path'] = t.path
            if t.multilabel_info == None:
                info['rice'] = None
                info['vegetable'] = None   
                info['meat'] = None
            else:
                info['rice'] = t.multilabel_info.rice 
                info['vegetable'] = t.multilabel_info.vegetable   
                info['meat'] = t.multilabel_info.meat                 
            l.append(info)
    return l

@socketio.on('count', namespace='/ocr')
def count(obj):        
    if obj['all_area']:
        q = db.session.query(Tray)
    else:    
        q = Tray.query.filter(Tray.video.has(Video.path.in_(obj['selections'])))
    if obj['mode'] == 'seg':
        q = q.filter(Tray.segmentation_info != None)    
    if obj['dish'] != 'all':
        q = q.filter(Tray.dish == obj['dish'])
    if obj['eaten'] != 'all':
        obj['eaten'] = obj['eaten'] == 'eaten'
        q = q.filter(Tray.eaten == obj['eaten'])    
    if obj['rice'] != 'all':
        q = q.filter(Tray.multilabel_info != None).filter(Tray.multilabel_info.has(MultiLabelInfo.rice == int(obj['rice'])))
    if obj['vegetable'] != 'all':
        q = q.filter(Tray.multilabel_info != None).filter(Tray.multilabel_info.has(MultiLabelInfo.vegetable == int(obj['vegetable'])))
    if obj['meat'] != 'all':
        q = q.filter(Tray.multilabel_info != None).filter(Tray.multilabel_info.has(MultiLabelInfo.meat == int(obj['meat'])))
        
    if obj['random']:
        q = q.order_by(func.random())

    if obj['low'] != '' and obj['high'] != '':
        try:
            q = q.slice(int(obj['low']), int(obj['high'])) 
        except:
            pass   
    elif obj['low'] == '' and obj['high'] != '':
        try:
            q = q.limit(int(obj['high'])) 
        except:
            pass
    elif obj['low'] != '' and obj['high'] == '':
        try:
            q = q.offset(int(obj['low'])) 
        except:
            pass    
    return q.count()
        
@socketio.on('submit', namespace='/ocr')
def submit(ocr_map, mode): 
    try:   
        if mode == 'ocr':
            for key, value in ocr_map.items():
                t = Tray.query.filter_by(path = key).first()
                if t != None:
                    t.ocr = value if value != "" else None
                    db.session.commit()
            return 1
        elif mode == 'eaten':
            for key, value in ocr_map.items():
                t = Tray.query.filter_by(path = key).first()
                if t != None:
                    if value == "":
                        t.eaten = None
                    elif value == "U":
                        t.eaten = False 
                    elif value == "E":
                        t.eaten = True                            
                    db.session.commit()
            return 1
        elif mode == 'dish':
            for key, value in ocr_map.items():
                t = Tray.query.filter_by(path = key).first()
                if t != None:
                    t.dish = value if value != "" else None
                    db.session.commit()
            return 1
        elif mode == 'multilabel':
            for key, value in ocr_map.items():
                t = Tray.query.filter_by(path = key).first()
                if t != None:
                    label = [0, 0, 0]                    
                    for i in range(len(value)):
                        label[i] = int(value[i])-1
                    if len(value) == 0 and t.multilabel_info != None:
                        db.session.delete(t.multilabel_info)
                        t.multilabel_info = None
                    elif t.multilabel_info != None:                   
                        t.multilabel_info.rice = label[0]
                        t.multilabel_info.vegetable = label[1]
                        t.multilabel_info.meat = label[2]
                    else:
                        ml = MultiLabelInfo(rice=label[0], vegetable=label[1], meat=label[2])
                        db.session.add(ml)
                        t.multilabel_info = ml
                    db.session.commit()
            return 1
        return 0
    except:
        return 0
