from .Step import Step
from flask_socketio import emit
from .socketio_helper import bind_socketio
from flask import render_template
from datetime import timedelta
from collections import Counter
from app import db
from app.DBModels import *
from app import globs

one_minute = timedelta(seconds=60)

class PairStep(Step):

    def __init__(self):
        super().__init__()
        self.context["step_id"] = 3
        self.context["step_name"] = "pair_step"
        self.state = [True, False, False]
        self.eat_min = timedelta(minutes=10)
        self.eat_max = timedelta(minutes=60)

    def dp(self, intervals, labels):

        def is_return_area(area):
            return (area == 'main_return_area') or (area == 'side_return_area') or (area == 'side_return_area_2')

        def dish(interval):
            counter = Counter([i.dish for i in interval])
            if len(counter.most_common(1)) > 0:
            	return counter.most_common(1)[0][0]
            return None

        def area(interval):
            num_return_area = sum(is_return_area(i.area) for i in interval)
            num_non_return_area = len(interval) - num_return_area            
            return 'return_area' if num_return_area > num_non_return_area else 'non_return_area'

        def avg_time(interval):
            min_time = min([i.date_time for i in interval])            
            sum_timedelta = sum([(i.date_time-min_time)
                                for i in interval], timedelta())
            avg_timedelta = sum_timedelta/len(interval)
            return min_time + avg_timedelta

        def make_sense(k1, k2):
            check1 = (not self.state[0]) or (labels[k2] == 'E' and labels[k1] == 'U')
            diff_time = avg_time(intervals[k2])-avg_time(intervals[k1])
            #print(check1)
            check2 = check1 #and (self.eat_min <= diff_time) and (diff_time <= self.eat_max)
            #print(check2)
            check3 = check2 and ((not self.state[1]) or ((area(intervals[k2]) == 'return_area') and (
                area(intervals[k1]) == 'non_return_area')))
            #print(check3)
            check4 = check3 and ((not self.state[2]) or (
                dish(intervals[k2]) == dish(intervals[k1])))
            if not check4:
                print(dish(intervals[k2]), dish(intervals[k1]))
            #print(check4)
            return check4

        n = len(intervals)
        num_pairs = [0] * (n+1)
        pointers = [-1] * (n+1)

        for i in range(n-2, -1, -1):            
            max = num_pairs[i+1]
            index = -1
            for j in range(i+1, n, 1):
                #print(i, j, make_sense(i, j))
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

        #print(pairs)
        return pairs

    def step_process(self):
        self.clean_up()
        print("Start Process...")

        # get the inputs
        # area != None, object_id != None are assumed
        # Filter
        q = Tray.query.filter(
            Tray.ocr != None,
            Tray.eaten != None,
            Tray.segmentation_info != None
        )
        # For each ocr, sort by time
        query = q.order_by(Tray.ocr, Tray.date_time)

        ocr = None
        list_of_trays = []
        for tray in query.all():
            if tray.ocr != ocr:
                ocr = tray.ocr
                list_of_trays.append([tray])
            else:
                list_of_trays[-1].append(tray)

        for same_ocr in list_of_trays:
            intervals = []
            for tray in same_ocr:
                if len(intervals) == 0:
                    intervals.append([tray])
                else:
                    last_interval = intervals[-1]
                    last_tray = last_interval[-1]
                    if (tray.date_time-last_tray.date_time) <= one_minute:
                        last_interval.append(tray)
                    else:
                        intervals.append([tray])
            #if(same_ocr[0].ocr == '0006'):
                #print(intervals)

            labels = []
            for interval in intervals:
                num_eaten = sum(tray.eaten for tray in interval)
                num_uneaten = len(interval) - num_eaten
                labels.append('E' if num_eaten > num_uneaten else 'U')

            #print(intervals)
            #print(labels)

            interval_pairs = self.dp(intervals, labels)

            def max_pixel(interval):
                i, max = (0, 0)
                for j, img in enumerate(interval):
                    info = img.segmentation_info
                    total = info.rice + info.meat + info.vegetable
                    if total > max:
                        i, max = (j, total)
                return i

            for (U, E) in interval_pairs:
                i = max_pixel(intervals[U])
                j = max_pixel(intervals[E])
                pair = Pair(ocr=intervals[U][i].ocr, before_tray=intervals[U][i], after_tray=intervals[E][j])
                #print(intervals[U][i].segmentation_info.total, intervals[E][j].segmentation_info.total)
                db.session.add(pair)
                db.session.commit()
                #print(pair.before_tray.segmentation_info.total, pair.after_tray.segmentation_info.total)
                #print(pair.before_tray)
                #print(pair.after_tray)

        self.started = False

        from app.UIManager import main_content_manager
        main_content_manager.switch_to_step(globs.step_objects['MultiLabelStep'])

    # If you wish to add something to start...
    def start(self):
        # Add something before calling super().start()
        if self.started:            
            self.step_process()
            self.stop()
        else:
            from app.UIManager import modal_manager
            modal_manager.show(render_template('step_modal.html', 
                num=Tray.query.filter(Tray.ocr != None,Tray.eaten != None,Tray.segmentation_info != None).count()))
        
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
        self.eat_min = timedelta(minutes=10)
        self.eat_max = timedelta(minutes=60)

    def clean_up(self):
        Pair.query.delete()
        db.session.commit()

    @bind_socketio('/pair_step')
    def change_state(self, state):
        self.state = state

    @bind_socketio('/pair_step')
    def change_eating_interval(self, min, max):
        self.eat_min = timedelta(minutes=int(min))
        self.eat_max = timedelta(minutes=int(max))
        #print(min, max)

    @bind_socketio('/pair_step')
    def modal_status(self, status):        
        if status['code'] != 0:
            self.started = True
            self.start()
