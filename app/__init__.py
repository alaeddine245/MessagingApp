from flask import Flask
from .views import views
from .auth import auth
from dotenv import load_dotenv
import os 

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("APP_SECRET")
    print(app.config['SECRET_KEY'])



    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app