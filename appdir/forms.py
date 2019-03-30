from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField # No custom variations in Flask_WTF
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from appdir.models import Patron

# Define the login class using the WTForms library in Python
# This library also contains code to generate the HTML elements so we don't need to define those
# On the page
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # This method must be made in this format so WTForms knows to run it in addition to stock validators
    def validate_email(self, email):
        # find any patrons that have the same email. This is a no-no
        patrons = Patron.query.filter_by(patronEmail=email.data).first()
        if patrons is not None:
            raise ValidationError('Patron with this email already exists!')