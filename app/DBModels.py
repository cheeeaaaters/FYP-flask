from app import db

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
    total =  db.Column(db.Integer, nullable=False)
    rice = db.Column(db.Integer, nullable=False)
    meat = db.Column(db.Integer, nullable=False)
    vegetable = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<segmentation> %r' % self.segmentation_path

if __name__ == '__main__':
    db.metadata.clear()
    db.create_all()