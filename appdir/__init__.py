# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
from flask import Flask
# we created this class file (config) and class (Config) 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from appdir import routes

# @app.route('/', methods=['POST', 'GET'])
# def hello_world():
#     return(render_template('home.html'))
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
