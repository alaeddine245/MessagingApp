from app import create_app
from app.chat import check_login
from flask_socketio import SocketIO,emit
from flask import request
import os
app = create_app()
socketio = SocketIO(app,cors_allowed_origins="*")

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
    app.run(debug=True)
