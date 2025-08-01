from flask import Flask
from .db import db
import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)
db.init_app(app)
login_manager = LoginManager(app)

from . import routes

with app.app_context():
    db.create_all()


