from flask import render_template, flash, redirect, url_for, request
from appdir import app
from appdir.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from appdir.models import Patron
from werkzeug.urls import url_parse # used to redirect users to the page they were at before they logged in

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


@app.route('/accounts')
@login_required
def accounts():
    return render_template('accounts.html')