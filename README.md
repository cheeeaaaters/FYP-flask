# FYP-flask

pip install flask

pip install flask-bootstrap

pip install eventlet

pip install flask-socketio

pip install flask-sqlalchemy


Debug Mode:

Linux:
  export FLASK_ENV=development
  
Window:
  set FLASK_ENV=development

[overview](https://docs.google.com/document/d/1oYXBfSsrXQM78Fvqqk-nFNm5oLyM0JAnFdLaIHQajck/edit?usp=sharing)

[pipeline](https://docs.google.com/document/d/1_EJtF2skQDNwex0ntVgstE3AF8VTqejnrtQCkS1VgrY/edit?usp=sharing)

# FAQ
## 1. Why socketio not emitting???
> It will emit, but not until the thread running now unblocks.
> Especially during some computational intensive work.
> In object_tracker_4.py, yolov3 is taking control of the thread.
> In order to let eventlet schedule another thread,
> use eventlet.sleep(0).
> Remember to import eventlet.

## 2. I changed DB / delete app.db. Now it gives exception. What to do???
>1. go to __init__.py
>2. comment everything below db = SQLAlchemy(app)
>3. open terminal
>4. python
>5. import app
>6. from app.DBModels import *
>7. from app import db
>8. db.metadata.clear()
>9. go to the file system, and delete app.db inside the app folder
>10. db.create_all()
>11. db.session.close()
>12. Video.query.all(), to check if there is exception
>13. exit()
>14. uncomment and run

## 3. I changed the html/js/css. It not updating. What to do???
>Press cltr+shift+R on chrome

## 4. Where to add the js/css?
> The styles block inside base_min.html

## 5. why need yield?
> To make the function a coroutine, so that it can be paused and send a signal to the cilent side.



