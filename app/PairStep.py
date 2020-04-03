from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from flask import render_template
from datetime import timedelta
from collections import Counter
from app import db
from app.DBModels import *

one_minute = timedelta(seconds=60)
eat_min = timedelta(minutes=10)
eat_max = timedelta(minutes=60)

class PairStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 3
        self.context["step_name"] = "pair_step"

    @staticmethod
    def dp(intervals, labels):

        def dish(interval):
            counter = Counter(interval)
            return counter.most_common(1)[0]

        def area(interval):
            num_return_area = sum(i.area == 'return_area' for i in interval)
            num_non_return_area = len(interval) - num_return_area
            return 'return_area' if num_return_area > num_non_return_area else 'non_return_area'

        def avg_time(interval):
            min_time = min(interval)
            sum_timedelta = sum((i-min_time) for i in interval)
            avg_timedelta = sum_timedelta/len(interval)
            return min_time + avg_timedelta

        def make_sense(k1, k2):
            check1 = labels[k2] == 'E' and labels[k1] == 'U'            
            diff_time = avg_time(intervals[k2])-avg_time(intervals[k1])
            check2 = check1 and (eat_min <= diff_time <= eat_max)
            check3 = check2 and (area(intervals[k2]) == 'return_area') and (area(intervals[k1]) == 'non_return_area')
            check4 = check3 and (dish(intervals[k2]) == dish(intervals[k1]))
            return check4

        n = len(intervals)
        num_pairs = [0] * n 
        pointers = [-1] * n

        for i in range(n-2, -1, -1):
            if labels[i] == 'E':
                num_pairs[i] = num_pairs[i+1]
            else:
                max = num_pairs[i+1]
                index = -1
                for j in range(i+1, n+1, 1):
                    if make_sense(i, j):
                        if (1+num_pairs[j+1]) > max:
                            max = (1+num_pairs[j+1])
                            index = j
                num_pairs[i] = max
                pointers[i] = index
        
        pairs = []
        cur = 0
        while cur < n:
            p = pointers[cur]
            if p == -1:
                cur += 1
            else:
                pairs.append((cur, p))
                cur = p+1

        return pairs


    def step_process(self):
        print("Start Process...")

        #get the inputs               
        #area != None, object_id != None are assumed     
        #Filter  
        q = Tray.query.filter(
            Tray.ocr != None,
            Tray.eaten != None,
            Tray.segmentation_info != None
        )
        #For each ocr, sort by time
        query = q.order_by(Tray.ocr, Tray.date_time)
        
        ocr = None
        intervals = []
        for tray in query.all():

            if (tray.ocr != ocr):
                ocr = tray.ocr
                intervals.clear()
            if len(intervals) == 0:
                intervals.append([tray])
            last_interval = intervals[-1]
            last_tray = last_interval[-1]
            if (tray.date_time-last_tray.date_time) <= one_minute:
                last_interval.append(tray)
            else:
                intervals.append([tray])
        
            labels = []
            for interval in intervals:
                num_eaten = sum(tray.eaten for tray in interval)
                num_uneaten = len(interval) - num_eaten
                labels.append('E' if num_eaten > num_uneaten else 'U')

            interval_pairs = dp(intervals, labels)

            def max_pixel(interval):
                i, max = (0, 0)
                for j, img in enumerate(interval):
                    if img.segmentation_info.total > max:
                        i, max = (j, img.segmentation_info.total)
                return i

            for (U, E) in interval_pairs:
                i = max_pixel(U)
                j = max_pixel(E) 
                pair = Pair(ocr=ocr, before_tray=U[i], after_tray=E[j])
                db.session.add(pair)
                db.session.commit()

        #TODO: update the html to indicate the process has finished
        emit('finish', {}, namespace='/pair_step')

    # If you wish to add something to start...
    def start(self):
        # Add something before calling super().start()
        #super().start()
        obj = {
            'mode': 3,
            'percentage': 0.1,
            'path': url_for('static', filename='images/food.jpg'),
            'locate_time': 0.1,
            'ocr_time': 0.1,
            'ocr_text': ['a','b','c'],
            'ocr': "0001"
        }
        emit('display', obj, namespace='/ocr_step')


    # If you wish to add something to stop...
    def stop(self):
        # Add something before calling super().stop()
        super().stop()

    def render(self):
        return render_template('pair_step.html')

    def render_sidebar(self):
        return render_template('pair_step_sb.html')

    def requested(self):        
        emit('init_mc', namespace='/pair_step')        

    def requested_sidebar(self):        
        emit('init_sb', namespace='/pair_step')

    #TODO: convert tray to json to pass to js
    def convert_to_json(self, input):        
        return {}

    @bind_socketio('/pair_step')
    def test(self, input):
        pass