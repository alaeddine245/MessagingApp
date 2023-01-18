from flask import Blueprint, request
from .__init__ import socketio
from flask_socketio import emit

chat = Blueprint('chat', __name__)

