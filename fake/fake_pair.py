import glob
from app.DBModels import *
from app import db
from datetime import datetime

class FakePair():

    @staticmethod
    def init_db():
        Video.query.delete()
        Tray.query.delete()
        Pair.query.delete()
        SegmentationInfo.query.delete()
        db.session.commit()

        video_fake = Video(path="fake")        
        db.session.add(video_fake)
        seg_info = SegmentationInfo(segmentation_path="fake1", total=100, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p1",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=False, ocr="0001", date_time=datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake2", total=120, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p2",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=False, ocr="0001", date_time=datetime(year=2000, month=1, day=1, hour=0, minute=0, second=2), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake3", total=110, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p3",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=False, ocr="0001", date_time=datetime(year=2000, month=1, day=1, hour=0, minute=0, second=4), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake4", total=40, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p4",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=True, ocr="0001", date_time=datetime(year=2000, month=1, day=1, hour=0, minute=30, second=0), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake5", total=30, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p5",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=True, ocr="0001", date_time=datetime(year=2000, month=1, day=1, hour=0, minute=30, second=2), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake6", total=50, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p6",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=True, ocr="0001", date_time=datetime(year=2000, month=1, day=1, hour=0, minute=30, second=4), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()

        seg_info = SegmentationInfo(segmentation_path="fake7", total=100, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p7",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=True, ocr="0001", date_time=datetime(year=2000, month=1, day=2, hour=0, minute=0, second=0), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake8", total=120, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p8",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=False, ocr="0001", date_time=datetime(year=2000, month=1, day=2, hour=0, minute=0, second=2), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake9", total=110, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p9",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=False, ocr="0001", date_time=datetime(year=2000, month=1, day=2, hour=0, minute=0, second=4), dish='bbq')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake10", total=40, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p10",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=True, ocr="0001", date_time=datetime(year=2000, month=1, day=2, hour=0, minute=30, second=0), dish='japanese')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake11", total=30, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p11",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=True, ocr="0001", date_time=datetime(year=2000, month=1, day=2, hour=0, minute=30, second=2), dish='japanese')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        seg_info = SegmentationInfo(segmentation_path="fake12", total=50, rice=40, meat=40, vegetable=20)
        tray = Tray(path="p12",video=video_fake,area='bbq',object_id=1, segmentation_info=seg_info, 
                    eaten=True, ocr="0001", date_time=datetime(year=2000, month=1, day=2, hour=0, minute=30, second=4), dish='japanese')
        db.session.add(seg_info)
        db.session.add(tray)
        db.session.commit()
        
if __name__ == '__main__':
    FakePair.init_db()