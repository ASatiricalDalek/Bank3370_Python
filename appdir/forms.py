from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField # No custom variations in Flask_WTF
from wtforms.validators import DataRequired

# Define the login class using the WTForms library in Python
# This library also contains code to generate the HTML elements so we don't need to define those
# On the page
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')