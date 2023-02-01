from flask import Blueprint, request, jsonify, session, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField
from wtforms.validators import InputRequired, Length
from dotenv import load_dotenv
import os
import ldap
from ldap import modlist

ldap_connection = ldap.initialize("ldap://localhost")
ldap_connection.bind_s("cn=admin,dc=messaging,dc=com", "12345")

load_dotenv()
auth = Blueprint('auth', __name__)
secret_key = os.environ.get('APP_SECRET')

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except Exception as e:
            print(e)
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


class SignupForm(FlaskForm):
    class Meta:
        csrf = False
    card_id = IntegerField(validators=[InputRequired()])
    firstname = StringField(
        validators=[InputRequired(), Length(min=2, max=20)])
    lastname = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    username = EmailField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username = EmailField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


@auth.route('/signup', methods=["Post"])
def signup():
    signup_form = SignupForm()

    if signup_form.validate():
        card_id = signup_form.card_id.data
        firstname = signup_form.firstname.data
        lastname = signup_form.lastname.data
        username = signup_form.username.data
        password = signup_form.password.data
        user = User(card_id, firstname, lastname, username, password)
        user_dict = user.__dict__
        dn = f"cn={username},dc=messaging,dc=com"
        attrs = {
            'objectclass': [b'person', b'top'],
            'cn': bytes(username, 'utf-8'),
            'sn': bytes(username, 'utf-8'),
            'userPassword': bytes(password, 'utf-8')
        }
        ldif = modlist.addModlist(attrs)
        try:
            ldap_connection.add_s(dn, ldif)
        except ldap.ALREADY_EXISTS:
            return make_response('Account already exists', 403)
        except ldap.LDAPError:
            return make_response('Sign up failed', 403)

        return user_dict
    return signup_form.errors


@auth.route('/login', methods=['POST'])
def login():
    login_form = LoginForm()
    if login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        #user = db['user'].find_one({'email': email})
        try:
            cn = f"cn={username}, dc=messaging,dc=com"
            ldap_connection.simple_bind_s(cn, password)
        except (ldap.INVALID_CREDENTIALS, ldap.UNWILLING_TO_PERFORM):
            print('INVALID CREDENTIALS USER')
            return make_response('Wrong email or password', 403)
        token = jwt.encode({
                'user': username,
                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        }, secret_key, algorithm='HS256')
        return jsonify({'token': token.decode(encoding='UTF-8')})
    return make_response('Form not valid', 403)
