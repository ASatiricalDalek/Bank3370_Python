# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
from flask import Flask
# we created this class file (config) and class (Config)
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Define how a user logs in so Flask knows how to restrict access to unauthenticated users
login = LoginManager(app)
login.login_view = 'login' # Function that handles login

# This has to be at the bottom
from appdir import routes
