from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db
from app.DBModels import *
import os 
from flask_socketio import emit
from app import socketio

db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database')

Session = sessionmaker()

engine = create_engine('sqlite:///' + os.path.join(db_dir, 'app.db'), echo=False, pool_threadlocal=True)
connection = engine.connect()

engine2 = create_engine('sqlite:///' + os.path.join(db_dir, 'demo.db'), echo=False, pool_threadlocal=True)
connection2 = engine2.connect()

session = Session(bind=connection)
session2 = Session(bind=connection2)

def r():
    pass

def switch_db(db_name):
    if db_name == 'app':
        db.session = session
    elif db_name == 'demo':
        db.session = session2
    Video.query = db.session.query(Video)
    Tray.query = db.session.query(Tray)
    Pair.query = db.session.query(Pair)
    SegmentationInfo.query = db.session.query(SegmentationInfo)
    MultiLabelInfo.query = db.session.query(MultiLabelInfo)
    db.session.remove = r
    print(Video.query.count())

@socketio.on('switch', namespace='/db')
def switch(db_name):
    try:
        switch_db(db_name)
    except:
        return 0
    return 1