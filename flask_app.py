from app import socketio
from app import app

if __name__ == "__main__":
    #app.run(debug=True, host='localhost', port=80)
    #socketio.run(app)
    socketio.run(app, debug=True, host="0.0.0.0", port=80)
    pass