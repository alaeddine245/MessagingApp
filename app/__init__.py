from flask import Flask
from .views import views
from .auth import auth
from dotenv import load_dotenv
import os 
from flask_cors import CORS

load_dotenv()
socketio=""
def create_app():
    global socketio
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("APP_SECRET")

    CORS(app,resources={r"/*":{"origins":"*"}})
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app