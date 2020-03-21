from app import app
from app import db
from app.DBModels import *

Tray.query.delete()
db.session.commit()