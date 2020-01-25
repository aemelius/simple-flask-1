from flask import Flask
import os
# from flask_bootstrap import Bootstrap
# from flask_mail import Mail
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from flask_pagedown import PageDown
# from config import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+os.environ.get('DB_USER')+":"+os.environ.get('DB_PASSWORD')+"@"+os.environ.get('DB_HOST')+"/"+os.environ.get('DB_NAME')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
