from flask import Blueprint, request
from flask_socketio import emit
import sys
from functools import wraps
import jwt
import os
from main import socketio

chat = Blueprint('chat', __name__)

clients ={}

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

@socketio.on("connect")
def connected():
    print(request)
    print("client has connected")
    user = jwt.decode(request.args.get("token"), os.environ.get('APP_SECRET'))['user']
    clients[user] = request.sid
    emit("connect",{"data":f"id: {user} is connected"})

@socketio.on('data')
def handle_message(data):
    print("data from the front end: ",str(data))
    user = jwt.decode(request.args.get("token"), os.environ.get('APP_SECRET'))['user']
    emit("data",{'data':data,'id':request.sid, 'from': user}, to=clients[request.args.get("to")])



@socketio.on("disconnect")
def disconnected():
    print("user disconnected")
    user = jwt.decode(request.args.get("token"), os.environ.get('APP_SECRET'))['user']
    clients.pop(user)
    emit("disconnect",f"user {user} disconnected",broadcast=True)



