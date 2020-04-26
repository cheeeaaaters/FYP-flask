from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from flask import render_template, url_for
from app.DBModels import *

class DataVisualizationStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 8
        self.context["step_name"] = "data_visualization_step"

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

    @bind_socketio('/data_visualization_step')
    def q1(self):
        data = Tray.query.filter(Tray.eaten == False & Tray.segmentation_info != None).all()
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
    def q1_2(self):
        data = Tray.query.filter(Tray.eaten == False & Tray.segmentation_info != None).all()
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
        data = Tray.query.filter(Tray.eaten == False & Tray.dish != None
        & Tray.segmentation_info != None).all()
        counts = [
            { 'name': 'bbq', 'count': [0 0 0] },
            { 'name': 'two choices', 'count': [0 0 0] },
            { 'name': 'delicacies', 'count': [0 0 0] },
            { 'name': 'japanese', 'count': [0 0 0] },
            { 'name': 'teppanyaki', 'count': [0 0 0] }
        ]
        index_map = {
            'bbq': 0, 'two_choices': 1, 'delicacies': 2, 'japanese': 3, 'teppanyaki': 4
        }
        for dd in data:
            (a, b, c, _) = self.get_prop(dd)
            counts[index_map[dd.dish]]['count'][0] += a       
            counts[index_map[dd.dish]]['count'][1] += b
            counts[index_map[dd.dish]]['count'][2] += c     
        for c in counts:
            s = sum(c['count'])
            if s != 0:   
                for cc in c['count']:
                    cc = cc/s
        return counts

    @bind_socketio('/data_visualization_step')
    def q2_2(self):
        data = Tray.query.filter(Tray.eaten == False & Tray.dish != None
        & Tray.segmentation_info != None).all()
        counts = [
            { 'name': 'bbq', 'count': [0 0 0 0] },
            { 'name': 'two choices', 'count': [0 0 0 0] },
            { 'name': 'delicacies', 'count': [0 0 0 0] },
            { 'name': 'japanese', 'count': [0 0 0 0] },
            { 'name': 'teppanyaki', 'count': [0 0 0 0] }
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
                for cc in c['count']:
                    cc = cc/s
        return counts

    @bind_socketio('/data_visualization_step')
    def q3(self):
        data = Tray.query.filter(Tray.eaten == True & Tray.segmentation_info != None).all()
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
    def q3_2(self):
        data = Tray.query.filter(Tray.eaten == True & Tray.segmentation_info != None).all()
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
    def q4(self):
        data = Tray.query.filter(Tray.eaten == True & Tray.dish != None
        & Tray.segmentation_info != None).all()
        counts = [
            { 'name': 'bbq', 'count': [0 0 0] },
            { 'name': 'two choices', 'count': [0 0 0] },
            { 'name': 'delicacies', 'count': [0 0 0] },
            { 'name': 'japanese', 'count': [0 0 0] },
            { 'name': 'teppanyaki', 'count': [0 0 0] }
        ]
        index_map = {
            'bbq': 0, 'two_choices': 1, 'delicacies': 2, 'japanese': 3, 'teppanyaki': 4
        }
        for dd in data:
            (a, b, c, _) = self.get_prop(dd)
            counts[index_map[dd.dish]]['count'][0] += a       
            counts[index_map[dd.dish]]['count'][1] += b
            counts[index_map[dd.dish]]['count'][2] += c     
        for c in counts:
            s = sum(c['count'])
            if s != 0:   
                for cc in c['count']:
                    cc = cc/s

        return counts

    @bind_socketio('/data_visualization_step')
    def q4_2(self):
        data = Tray.query.filter(Tray.eaten == True & Tray.dish != None
        & Tray.segmentation_info != None).all()
        counts = [
            { 'name': 'bbq', 'count': [0 0 0 0] },
            { 'name': 'two choices', 'count': [0 0 0 0] },
            { 'name': 'delicacies', 'count': [0 0 0 0] },
            { 'name': 'japanese', 'count': [0 0 0 0] },
            { 'name': 'teppanyaki', 'count': [0 0 0 0] }
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
                for cc in c['count']:
                    cc = cc/s
                    
        return counts

    @bind_socketio('/data_visualization_step')
    def q5(self):
        return [
            { 'name': 'bbq', 'before': 16, 'after': 4 },
            { 'name': 'bbq', 'before': 14, 'after': 5 },
            { 'name': 'bbq', 'before': 12, 'after': 6 },
            { 'name': 'japanese', 'before': 7, 'after': 4 },
            { 'name': 'japanese', 'before': 1, 'after': 8 }
        ]    