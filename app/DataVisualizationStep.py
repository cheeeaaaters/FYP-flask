from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from flask import render_template, url_for
from app.DBModels import *
from datetime import timedelta

class DataVisualizationStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 8
        self.context["step_name"] = "data_visualization_step"
        self.q5_state = [True, False, False, False]

    def no_dup(self):
        f = SegmentationInfo.food(['rice', 'vegetable', 'meat'])
        food_trays = db.session.query(Tray, f.label('food')).join(SegmentationInfo).subquery()  
        a = db.session.query(food_trays.c.id, db.func.max(food_trays.c.food)).group_by(food_trays.c.video_id, food_trays.c.object_id).order_by(food_trays.c.id)
        aa = a.subquery()
        b = db.session.query(Tray).join(aa, Tray.id == aa.c.id)
        return b

    #If you wish to add something to start...
    def start(self): 
        #Add something before calling super().start()
        #super().start()   
        pass

    #If you wish to add something to stop...
    def stop(self):
        #Add something before calling super().stop()
        super().stop()     

    def render(self):
        return render_template('data_visualization_step.html')

    def render_sidebar(self):
        return render_template('data_visualization_step_sb.html')

    def requested(self):        
        emit('init_mc', namespace='/data_visualization_step')        

    def requested_sidebar(self):        
        emit('init_sb', namespace='/data_visualization_step')

    def get_prop(self, d):
        seg = d.segmentation_info
        a = seg.rice / seg.total            
        b = seg.vegetable / seg.total            
        c = seg.meat / seg.total 
        d = 1 - a - b - c
        return (a, b, c, d)

    def get_prop_other(self, d):
        seg = d.segmentation_info
        a = seg.rice / seg.total            
        b = seg.vegetable / seg.total            
        c = seg.meat / seg.total
        d = seg.other / seg.total 
        e = 1 - a - b - c - d
        return (a, b, c, d, e)

    @bind_socketio('/data_visualization_step')
    def q1(self, dish):
        data = self.no_dup().filter(Tray.eaten == False, Tray.segmentation_info != None)
        if dish != 'all':
            data = data.filter(Tray.dish == dish)
        data = data.all()
        counts = [
            { 'type': "rice", 'count': 0},
            { 'type': "vegetable", 'count': 0},
            { 'type': "meat", 'count': 0}
        ]
        for dd in data:
            (a, b, c, _) = self.get_prop(dd)            
            counts[0]['count'] += a          
            counts[1]['count'] += b           
            counts[2]['count'] += c        
        
        return counts        

    @bind_socketio('/data_visualization_step')
    def q1_2(self, dish):
        data = self.no_dup().filter((Tray.eaten == False) & (Tray.segmentation_info != None))
        if dish != 'all':
            data = data.filter(Tray.dish == dish)
        data = data.all()
        counts = [
            { 'type': "rice", 'count': 0},
            { 'type': "vegetable", 'count': 0},
            { 'type': "meat", 'count': 0},
            { 'type': "background", 'count': 0 } 
        ]
        for dd in data:
            (a, b, c, d) = self.get_prop(dd)
            counts[0]['count'] += a           
            counts[1]['count'] += b           
            counts[2]['count'] += c  
            counts[3]['count'] += d  
        
        return counts        

    @bind_socketio('/data_visualization_step')
    def q2(self):
        data = self.no_dup().filter((Tray.eaten == False) & (Tray.dish != None)
        & (Tray.segmentation_info != None)).all()
        counts = [
            { 'name': 'bbq', 'count': [0, 0, 0] },
            { 'name': 'two choices', 'count': [0, 0, 0] },
            { 'name': 'delicacies', 'count': [0, 0, 0] },
            { 'name': 'japanese', 'count': [0, 0, 0] },
            { 'name': 'teppanyaki', 'count': [0, 0, 0] }
        ]
        index_map = {
            'bbq': 0, 'two_choices': 1, 'delicacies': 2, 'japanese': 3, 'teppanyaki': 4
        }
        for dd in data:
            (a, b, c, _) = self.get_prop(dd)
            counts[index_map[dd.dish]]['count'][0] += a       
            counts[index_map[dd.dish]]['count'][1] += b
            counts[index_map[dd.dish]]['count'][2] += c 
        #print(counts)    
        for c in counts:
            s = sum(c['count'])
            if s != 0:   
                for i in range(len(c['count'])):
                    c['count'][i] = c['count'][i]/s
        #print(counts)
        return counts

    @bind_socketio('/data_visualization_step')
    def q2_2(self):
        data = self.no_dup().filter((Tray.eaten == False) & (Tray.dish != None)
        & (Tray.segmentation_info != None)).all()
        counts = [
            { 'name': 'bbq', 'count': [0, 0, 0, 0] },
            { 'name': 'two choices', 'count': [0, 0, 0, 0] },
            { 'name': 'delicacies', 'count': [0, 0, 0, 0] },
            { 'name': 'japanese', 'count': [0, 0, 0, 0] },
            { 'name': 'teppanyaki', 'count': [0, 0, 0, 0] }
        ]
        index_map = {
            'bbq': 0, 'two_choices': 1, 'delicacies': 2, 'japanese': 3, 'teppanyaki': 4
        }
        for dd in data:
            (a, b, c, d) = self.get_prop(dd)
            counts[index_map[dd.dish]]['count'][0] += a       
            counts[index_map[dd.dish]]['count'][1] += b
            counts[index_map[dd.dish]]['count'][2] += c     
            counts[index_map[dd.dish]]['count'][3] += d
        for c in counts:
            s = sum(c['count'])
            if s != 0:   
                for i in range(len(c['count'])):
                    c['count'][i] = c['count'][i]/s
        return counts

    @bind_socketio('/data_visualization_step')
    def q3(self, dish):   
        data = self.no_dup().filter(Tray.eaten == True, Tray.segmentation_info != None)
        if dish != 'all':
            data = data.filter(Tray.dish == dish)
        data = data.all()
        counts = [
            { 'type': "rice", 'count': 0},
            { 'type': "vegetable", 'count': 0},
            { 'type': "meat", 'count': 0},
            { 'type': "other", 'count': 0}
        ]
        print(counts)
        for dd in data:
            (a, b, c, d, _) = self.get_prop_other(dd)
            counts[0]['count'] += a          
            counts[1]['count'] += b           
            counts[2]['count'] += c 
            counts[3]['count'] += d             
        
        return counts 

    @bind_socketio('/data_visualization_step')
    def q3_2(self, dish):
        data = self.no_dup().filter(Tray.eaten == True, Tray.segmentation_info != None)
        if dish != 'all':
            data = data.filter(Tray.dish == dish)
        data = data.all()
        counts = [
            { 'type': "rice", 'count': 0},
            { 'type': "vegetable", 'count': 0},
            { 'type': "meat", 'count': 0},
            { 'type': "other", 'count': 0},
            { 'type': "background", 'count': 0 } 
        ]
        for dd in data:
            (a, b, c, d, e) = self.get_prop_other(dd)
            counts[0]['count'] += a           
            counts[1]['count'] += b           
            counts[2]['count'] += c  
            counts[3]['count'] += d  
            counts[4]['count'] += e
        
        return counts      

    @bind_socketio('/data_visualization_step')
    def q4(self):
        data = self.no_dup().filter((Tray.eaten == True) & (Tray.dish != None)
        & (Tray.segmentation_info != None)).all()
        counts = [
            { 'name': 'bbq', 'count': [0, 0, 0, 0] },
            { 'name': 'two choices', 'count': [0, 0, 0, 0] },
            { 'name': 'delicacies', 'count': [0, 0, 0, 0] },
            { 'name': 'japanese', 'count': [0, 0, 0, 0] },
            { 'name': 'teppanyaki', 'count': [0, 0, 0, 0] }
        ]
        index_map = {
            'bbq': 0, 'two_choices': 1, 'delicacies': 2, 'japanese': 3, 'teppanyaki': 4
        }
        for dd in data:
            (a, b, c, d, _) = self.get_prop_other(dd)
            counts[index_map[dd.dish]]['count'][0] += a       
            counts[index_map[dd.dish]]['count'][1] += b
            counts[index_map[dd.dish]]['count'][2] += c  
            counts[index_map[dd.dish]]['count'][3] += d   
        for c in counts:
            s = sum(c['count'])
            if s != 0:   
                for i in range(len(c['count'])):
                    c['count'][i] = c['count'][i]/s

        return counts

    @bind_socketio('/data_visualization_step')
    def q4_2(self):
        data = self.no_dup().filter((Tray.eaten == True) & (Tray.dish != None)
        & (Tray.segmentation_info != None)).all()
        counts = [
            { 'name': 'bbq', 'count': [0, 0, 0, 0, 0] },
            { 'name': 'two choices', 'count': [0, 0, 0, 0, 0] },
            { 'name': 'delicacies', 'count': [0, 0, 0, 0, 0] },
            { 'name': 'japanese', 'count': [0, 0, 0, 0, 0] },
            { 'name': 'teppanyaki', 'count': [0, 0, 0, 0, 0] }
        ]
        index_map = {
            'bbq': 0, 'two_choices': 1, 'delicacies': 2, 'japanese': 3, 'teppanyaki': 4
        }
        for dd in data:
            (a, b, c, d, e) = self.get_prop_other(dd)
            counts[index_map[dd.dish]]['count'][0] += a       
            counts[index_map[dd.dish]]['count'][1] += b
            counts[index_map[dd.dish]]['count'][2] += c     
            counts[index_map[dd.dish]]['count'][3] += d
            counts[index_map[dd.dish]]['count'][4] += e
        for c in counts:
            s = sum(c['count'])
            if s != 0:   
                for i in range(len(c['count'])):
                    c['count'][i] = c['count'][i]/s
                    
        return counts

    @bind_socketio('/data_visualization_step')
    def q5_change_state(self, state):
        self.q5_state = state
        return True

    @bind_socketio('/data_visualization_step')
    def q5(self):
        l = []
        for p in Pair.query.all():
            obj = {
                'name': p.before_tray.dish                
            }
            (a1, b1, c1, d1) = self.get_prop(p.before_tray)
            (a2, b2, c2, d2) = self.get_prop(p.after_tray)
            t1 = p.before_tray.segmentation_info.total
            t2 = p.after_tray.segmentation_info.total
            if self.q5_state[0]:
                obj['before'] = 1 - d1
                obj['after'] = 1 - d2
            else:
                obj['before'] = 0
                obj['after'] = 0
                if self.q5_state[1]:
                    obj['before'] += a1
                    obj['after'] += a2
                if self.q5_state[2]:
                    obj['before'] += b1
                    obj['after'] += b2
                if self.q5_state[3]:
                    obj['before'] += c1
                    obj['after'] += c2
            l.append(obj)

        return l  

    @bind_socketio('/data_visualization_step')
    def q6(self, dish):
        data = self.no_dup().filter(Tray.eaten == True, Tray.multilabel_info != None)
        if dish != 'all':
            data = data.filter(Tray.dish == dish)
        data = data.all()
        counts = [
            [
                { 'name': 'rice: none', 'count': 0 },
                { 'name': 'rice: little', 'count': 0 },
                { 'name': 'rice: many', 'count': 0 },
            ],
            [
                { 'name': 'vegetable: none', 'count': 0 },
                { 'name': 'vegetable: little', 'count': 0 },
                { 'name': 'vegetable: many', 'count': 0 },
            ],
            [
                { 'name': 'meat: none', 'count': 0 },
                { 'name': 'meat: little', 'count': 0 },
                { 'name': 'meat: many', 'count': 0 },
            ]
        ]
        for dd in data:
            ml = dd.multilabel_info
            counts[0][ml.rice]['count'] += 1
            counts[1][ml.vegetable]['count'] += 1
            counts[2][ml.meat]['count'] += 1
        return counts
    
    @bind_socketio('/data_visualization_step')
    def q7(self):
        l = []        
        for i in range(10, 120, 10):
            l.append({
                'start': i,
                'end': i + 10,
                'count': 0
            })        
        for p in Pair.query.all():
            delta = p.after_tray.date_time - p.before_tray.date_time
            minutes = delta.total_seconds() / 60
            index = int(minutes / 10) - 1
            index = max(min(index, len(l) - 1),0)
            l[index]['count'] += 1
        return l