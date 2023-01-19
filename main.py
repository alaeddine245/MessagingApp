from flask import Flask, request
from functools import wraps
from views import views
from auth import auth
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit
import jwt
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET")
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
clients = {}


def check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            disconnected(request.sid)
        try:
            data = jwt.decode(token, os.environ.get('APP_SECRET'))
        except Exception as e:
            disconnected(request.sid)
        return f(*args, **kwargs)
    return decorated_function

# @check_login


@socketio.on("connect")
def connected(auth):
    print(auth)
    print("client has connected")
    user = jwt.decode(auth['token'], os.environ.get(
        'APP_SECRET'), algorithms=['HS256'])['user']
    clients[user] = request.sid
    emit("connect", {"data": f"id: {user} is connected"})

# @check_login


@socketio.on('data')
def handle_message(data):
    print("data from the front end: ", str(data))

    # user = jwt.decode(request.args.get("token"), os.environ.get('APP_SECRET'))['user']
    # , 'from': list(clients.keys())[
    #  list(clients.values()).index(request.sid)]
    data = json.loads(str(data))
    emit("data", {'data': data['data'],
         'id': request.sid}, to=clients[data['user']])


# @check_login
@ socketio.on("disconnect")
def disconnected():
    print("user disconnected")
    user = jwt.decode(request.args.get("token"),
                      os.environ.get('APP_SECRET'))['user']
    clients.pop(user)
    emit("disconnect", f"user {user} disconnected", broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
    app.run(debug=True)
