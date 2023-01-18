from flask import Blueprint , request, jsonify, session, make_response
import jwt
from functools import wraps
from dotenv import load_dotenv
import os 
load_dotenv()
secret_key = os.environ.get('APP_SECRET')


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            print(secret_key)
            data = jwt.decode(token, secret_key,algorithms=['HS256'])
        except Exception as e:
            print(e)
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


views = Blueprint('views', __name__)

@views.route('/home', )
# @token_required
def home():
    return "<h1>Test</h1>"