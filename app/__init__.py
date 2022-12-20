from flask import Flask
from .views import views
from .auth import auth
import pymongo

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'random string123'

    client = pymongo.MongoClient('localhost', 27017)
    db = client.user_login_system

    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app