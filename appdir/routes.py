from flask import render_template, flash, redirect, url_for
from appdir import app
from appdir.forms import LoginForm

# routes contains the logic for all of our pages

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Only runs if the method is POST, and the form validates
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}' .format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    # Returned if the above is false, IE the method is GET, therefore the form hasn't been submitted
    # Or the form is invalid
    return render_template('login.html', title="Sign In", form=form)