from flask import Blueprint , request, jsonify
from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
auth = Blueprint('auth', __name__)

class SignupForm(FlaskForm):
    card_id = IntegerField(validators=[InputRequired()])
    firstname =  StringField(validators=[InputRequired(), Length(min=2, max=20)])
    lastname =  StringField(validators=[InputRequired(), Length(min=2, max=20)])
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
        password =  signup_form.password.data
        user  = User(card_id, firstname, lastname, email, password)
        return user.to_json()
    return "Error"

@auth.route('/login')
def login():
    return "<p>login</p>"

@auth.route('/logout')
def logout():
    return "<p>logout</p>"