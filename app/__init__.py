from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:////home/tanigai/activitylistV1.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://arassane:19lewisham98@b756f29d-9162-4fc3-ae29-07122a2b2b08.td-app-6136.postgresql.dbs.scalingo.com:31084/td_app_6136?sslmode=prefer'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler) 

from app import routes

