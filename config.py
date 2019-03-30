import os

baseDir = os.path.abspath(os.path.dirname(__file__))

# Use either the environment variable, SECRET_KEY or a hard coded string
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'top-secret-bro'
    # Check DB_URL env variable to see if DB path is defined. If not, set it manually
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(baseDir, 'Bank3370.db')
    SQLACHEMY_TRACK_MODIFICATIONS = False

