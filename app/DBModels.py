from app import db
from sqlalchemy.ext.hybrid import hybrid_method

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), unique=True, nullable=False)
    trays = db.relationship('Tray', backref='video', lazy=True)

    def __repr__(self):
        return '<videe> %s' % self.path

class Tray(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), unique=True, nullable=False)
    #segmentation_path = db.Column(db.String(120), unique=True)   
    segmentation_info =  db.relationship('SegmentationInfo', backref='tray', lazy=True)
    segmentation_info_id = db.Column(db.Integer, db.ForeignKey('segmentation_info.id'))
    multilabel_info =  db.relationship('MultiLabelInfo', backref='tray', lazy=True)
    multilabel_info_id = db.Column(db.Integer, db.ForeignKey('multi_label_info.id'))
    object_id = db.Column(db.Integer, nullable=False)
    ocr = db.Column(db.String(4))
    eaten = db.Column(db.Boolean)
    dish = db.Column(db.String(20), index=True)
    area = db.Column(db.String(20), nullable=False)
    date_time = db.Column(db.DateTime, index=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)

    def __repr__(self):
        return '<tray> %s' % self.path

class Pair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ocr = db.Column(db.String(4), index=True, nullable=False)
    before_tray_id = db.Column(db.Integer, db.ForeignKey('tray.id'), nullable=False)
    before_tray = db.relationship('Tray', foreign_keys=[before_tray_id], backref='pair_before', uselist=False)
    after_tray_id = db.Column(db.Integer, db.ForeignKey('tray.id'), nullable=False)
    after_tray = db.relationship('Tray', foreign_keys=[after_tray_id], backref='pair_after', uselist=False)

    def __repr__(self):
        return '<pair> %r' % self.ocr

class SegmentationInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segmentation_path = db.Column(db.String(120), unique=True, nullable=False)
    total =  db.Column(db.Integer, default=0)
    rice = db.Column(db.Integer, default=0)
    meat = db.Column(db.Integer, default=0)
    vegetable = db.Column(db.Integer, default=0)
    other = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<segmentation> %r' % self.segmentation_path

    @hybrid_method
    def food(self, fields):
        return sum(getattr(self, field) for field in fields)

    @food.expression
    def food(cls, fields):
        return sum(getattr(cls, field) for field in fields)

class MultiLabelInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rice = db.Column(db.Integer)
    meat = db.Column(db.Integer)
    vegetable = db.Column(db.Integer)
    rice_conf = db.Column(db.Float)
    meat_conf = db.Column(db.Float)
    vegetable_conf = db.Column(db.Float)

    def __repr__(self):
        return '<multilabel> (%d %d %d)' % (self.rice, self.vegetable, self.meat)

if __name__ == '__main__':
    db.metadata.clear()
    db.create_all()