from flask import Blueprint , request, jsonify, session, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps
from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField
from wtforms.validators import InputRequired, Length
from dotenv import load_dotenv
import os 
import pymongo
import bcrypt

load_dotenv()
auth = Blueprint('auth', __name__)
secret_key = os.environ.get('APP_SECRET')
client = pymongo.MongoClient('localhost', 27017)
db = client.messaging_app


def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, secret_key)
        except Exception as e:
            print(e)
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


class SignupForm(FlaskForm):
    class Meta:
        csrf = False
    card_id = IntegerField(validators=[InputRequired()])
    firstname =  StringField(validators=[InputRequired(), Length(min=2, max=20)])
    lastname =  StringField(validators=[InputRequired(), Length(min=2, max=20)])
    email = EmailField(validators=[InputRequired()])
    password =  PasswordField(validators=[InputRequired()])
class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    email = EmailField(validators=[InputRequired()])
    password =  PasswordField(validators=[InputRequired()])


@auth.route('/signup', methods=["Post"])
def signup():
    signup_form = SignupForm()

    if signup_form.validate():
        card_id =  signup_form.card_id.data
        firstname =  signup_form.firstname.data
        lastname =  signup_form.lastname.data
        email = signup_form.email.data
        password =  bcrypt.hashpw(signup_form.password.data.encode(),bcrypt.gensalt()).hex()
        user  = User(card_id, firstname, lastname, email, password)
        user_dict = user.__dict__
        db['user'].insert_one(user_dict)
        return user_dict
    return signup_form.errors

@auth.route('/login', methods=['POST'])
def login():
    login_form = LoginForm()
    if login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        user = db['user'].find_one({'email': email})
        
        if not user:
            return make_response('Wrong email or password', 403)

        if bcrypt.checkpw(password.encode(), user['password']):
            token = jwt.encode({
                'user': email,
                'expiration': str(datetime.utcnow()+ timedelta(seconds=120))
            }, secret_key, algorithm='HS256')
        
            return jsonify({'token' : token.decode('utf-8')})
        else:
            return make_response('Wrong email or password', 403)
