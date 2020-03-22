import glob
from app.DBModels import *
from app import db
import shutil

class FakeOCR():

    @staticmethod
    def init_db():
        video_fake = Video(path="fake")
        for i,path in enumerate(glob.glob("/home/ubuntu/407images_classed/eaten/bbq/*.jpg")):
            p = "/home/ubuntu/CanteenPreProcessing/result/recording_2019_11_06/return_area/cam_one-24600-24720/1-"+str(i)+".jpg"
            shutil.copy2(path, p)
            tray = Tray(path=p,video=video_fake,area='return_area',object_id=1)
            db.session.add(tray)
            db.session.commit()

    @staticmethod
    def process():
        trays = iter(Tray.query.all())
        for t in trays:
            yield t