import time
from app import app
from app import db
import glob
from app.DBModels import Video, Tray
import os

class FakeTrayDetection():

    @staticmethod
    def init_db():        
        file_path = os.path.dirname(__file__)
        video_path = glob.glob(file_path+'/videos/*')
        print(video_path)
        video1 = Video(path=video_path[0])
        video2 = Video(path=video_path[1])        
        db.session.add(video1)
        db.session.add(video2)
        
        trays_path = glob.glob(file_path+'/trays/*.png')
        trays_path.extend(glob.glob(file_path+'/trays/*.jpg'))
        for i,tray_path in enumerate(trays_path):
            if(i<5):
                tray = Tray(path=tray_path, area="bbq", video=video1)
            else:
                tray = Tray(path=tray_path, area="return area", video=video2)
            db.session.add(tray)
        db.session.commit()
        #db.session.rollback()                

    @staticmethod
    def process(input):
        trays = iter(Tray.query.all())
        for t in trays:
            time.sleep(2)
            yield t
