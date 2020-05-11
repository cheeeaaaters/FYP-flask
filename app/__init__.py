from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from app import globs
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
bootstrap = Bootstrap(app)

#This is needed for asynchronous emit
import eventlet
eventlet.monkey_patch()
socketio = SocketIO(app, async_mode="eventlet")

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_copy.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

#db.metadata.clear()
#db.create_all()

#from app import DBManager


from app import socketio_helper
from app import DBModels
from app import Step
from app import TrayDetectionStep
from app import OCRStep
from app import ClassifyEatenStep
from app import ClassifyDishStep
from app import SegmentationStep
from app import PairStep
from app import MultiLabelStep
from app import DataVisualizationStep

from app import fs_helper

socketio_helper.add_socketio()

from app import UIManager
from app import test

from app import input_ocr

print("hi")
#exit()
