from flask import render_template, flash, redirect, url_for, request
from appdir import app, db
from appdir.forms import LoginForm, RegistrationForm, CreateCheckingAccountForm, NewAccountType, CreditScoreForm,\
    EstimateInterestForm
from flask_login import current_user, login_user, logout_user, login_required
from appdir.models import Patron, BankAccount, PatronBankAccounts, BankAccountType
from werkzeug.urls import url_parse # used to redirect users to the page they were at before they logged in
from math import pow
# routes contains the logic for all of our pages


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title = 'Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the current user is logged in, they don't need to see this form; send them home
    # current_user is a var from flask_login that contains the current user
    # check if that user is authenticated (function defined in models.py; comes from Flask_login)
    # Not logged in users will return false to is_authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Only runs if the method is POST, and the form validates
    if form.validate_on_submit():
        # Retrieve the first record from the db w/ email matching the form entry (should be only 1)
        patron = Patron.query.filter_by(patronEmail = form.email.data).first()
        # if the patron doesn't exist, or the password is wrong
        if patron is None or not patron.checkPassword(form.password.data):
            # display message (see base.html)
            flash('Invalid email address of password')
            return redirect(url_for('index'))
        # Flask-login provides this function; keeps the current_user variable set to this user
        login_user(patron, remember=form.remember_me.data)
        # Next page is set when a user tries to enter a authBlocked page, and is redirected to login instead
        nextPage = request.args.get('next')
        if not nextPage or url_parse(nextPage).netloc != '': # This ensures the URL actually exists in the application
            # if there is no next page set (IE the user went right to login) set nextPage to home
            nextPage = url_for('index')
        return redirect(nextPage)
    # Returned if the above is false, IE the method is GET, therefore the form hasn't been submitted
    # Or the form is invalid
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/accounts/<id>', methods=['GET', 'POST'])
@login_required
def accounts(id):
    form = NewAccountType()
    if form.validate_on_submit():
        accountType = form.accountChoice.data
        if accountType == "Checking":
            flash("Checking Account Selected")
            return redirect(url_for('newCheckingAccount', id=current_user.get_id()))
        elif accountType == "Savings":
            flash("Savings Account Selected")
        elif accountType == "Retirement":
            flash("Retirement Account Selected")
        else:
            flash(accountType + " Selected")
        return redirect(url_for('accounts', id=current_user.get_id()))
    else:
        thisPatronsAccounts = PatronBankAccounts()

        listOfAccounts = thisPatronsAccounts.query.filter_by(id_patron=current_user.get_id()).all()
        # Using this list of all the account IDs, query the bankAccount table to find all this patron's accounts
    return render_template('accounts.html', form=form)


@app.route('/accounts/<id>/new_account', methods=['GET', 'POST'])
@login_required
def newCheckingAccount(id):
    form = CreateCheckingAccountForm()
    if form.validate_on_submit():
        newAccount = BankAccount()
        newAccountRelation = PatronBankAccounts()

        newAccount.accountType = "Checking"
        newAccount.accountBalance = 0
        newAccount.accountName = form.accountName.data
        if (form.insurance.data):
            newAccount.insurance = 1
        else:
            newAccount.insurance = 0

        # Provisionally adds this account to the DB so it gets a unique ID
        db.session.add(newAccount)
        db.session.flush()

        # Use that unique ID, and the current user's sessions ID to create the relationship
        newAccountRelation.id_bankAccount = newAccount.id
        newAccountRelation.id_patron = current_user.get_id()

        db.session.add(newAccountRelation)
        db.session.commit()

        flash("Checking account successfully created!")
        return redirect(url_for('accounts', id=current_user.get_id()) )

    return render_template('newCheckingAccount.html', title='Open a Checking Account' ,form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        patron = Patron()
        patron.patronFirstName = form.firstName.data
        patron.patronLastName = form.lastName.data
        patron.patronEmail = form.email.data
        patron.setPassword(form.password.data)
        db.session.add(patron)
        db.session.commit()
        flash("Congratulations " + form.firstName.data + " you are now a registered user")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/creditScore', methods=['GET', 'POST'])
def creditScore():
    form = CreditScoreForm()
    if form.validate_on_submit():
        averageAge = form.averageAge.data
        hardInquiries = form.hardInquiries.data
        creditUtilization = form.creditUtilization.data
        latePay = form.latePay.data
        totalAccounts = form.totalAccounts.data
        derogatoryMarks = form.derogatoryMarks.data
        if (derogatoryMarks<1 and totalAccounts>8 and hardInquiries<3 and latePay<1 and creditUtilization<10 and
                    averageAge>24):
            creditScore=800
        else:
            creditScore=600
        flash("Congratulations your Credit Score is " + str(creditScore))
        return render_template('creditScore.html', title='Credit Score', form=form, creditScore=creditScore)
    return render_template('creditScore.html', title='Credit Score', form=form)


@app.route('/estimateInterest/<id>', methods=['GET', 'POST'])
@login_required
def estimateInterest(id):
    form = EstimateInterestForm()
    if form.validate_on_submit():
        account = form.accountType.data
        startingfunds = form.startingFunds.data
        months = form.monthsOfInterest.data
        accountinfo = BankAccountType.query.filter_by(accountType=account).first()
        interestrate = accountinfo.accountInterestRate
        powermath = pow((1+interestrate), months)
        estimateinterest = startingfunds*powermath

        flash("Congratulations your Estimated Interest return is $" + str(round(estimateinterest,2)))
        return render_template('estimateInterest.html', title='Estimate Interest', form=form,
                               estimateinterest=estimateinterest)
    return render_template('estimateInterest.html', title='Estimate Interest', form=form)
