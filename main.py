from flask import Flask
from views import views
from auth import auth
from dotenv import load_dotenv
import os 
from flask_cors import CORS
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET")
socketio = SocketIO(app,cors_allowed_origins="*")

CORS(app,resources={r"/*":{"origins":"*"}})
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
    app.run(debug=True)
