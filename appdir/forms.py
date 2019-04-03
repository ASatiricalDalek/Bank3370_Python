from flask_wtf import FlaskForm
# No custom variations in Flask_WTF
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, FloatField,\
    DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from appdir.models import Patron, BankAccountType
from datetime import date
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # This method must be made in this format so WTForms knows to run it in addition to stock validators
    def validate_email(self, email):
        # find any patrons that have the same email. This is a no-no
        patrons = Patron.query.filter_by(patronEmail=email.data).first()
        if patrons is not None:
            raise ValidationError('Patron with this email already exists!')


class CreateCheckingAccountForm(FlaskForm):
    accountName = StringField('Account Name', validators=[DataRequired()])
    insurance = BooleanField('Insurance')
    submit = SubmitField('Submit', validators=[DataRequired()])


class NewAccountType(FlaskForm):
    # This *should* be pulled from the database, but it's not
    # Choices are in the format (value, display)
    choices = [('Checking', 'Checking'), ('Savings', 'Savings'), ('Retirement', 'Retirement')]
    accountChoice = RadioField(label="Select an account type", choices=choices, validators=[DataRequired()])
    submit = SubmitField(label="Open my Account")


class NewLoansType(FlaskForm):
    choices = [('Auto Loans', 'Auto Loans'), ('Student Loans', 'Student Loans'), ('Home Loans', 'Home Loans')]
    loansChoice = RadioField (label="Select a Loans type", choices=choices, validators=[DataRequired()])
    submit = SubmitField(label="Open Loans Type")


class CreateAutoLoanForm(FlaskForm):
        accountName = StringField('Account Name', validators=[DataRequired()])
        loanPayment = FloatField('Auto loan Payment')
        loanBalance = FloatField('Auto loan Balance')
        loanPaymentDate = DateField('Auto Loan Payment Date')
        submit = SubmitField('Submit', validators=[DataRequired()])


class CreateStudentLoanForm(FlaskForm):
            accountName = StringField('Account Name', validators=[DataRequired()])
            loanPayment = FloatField('Student loan Payment')
            loanBalance = FloatField('Student loan Balance')
            submit = SubmitField('Submit', validators=[DataRequired()])


class CreateHomeLoanForm(FlaskForm):
            accountName = StringField('Account Name', validators=[DataRequired()])
            loanPayment = FloatField('Student Loan Payment')
            loanBalance = FloatField('Student Loan Balance')
            submit = SubmitField('Submit', validators=[DataRequired()])
