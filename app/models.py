from .db import db
from . import bcrypt
from . import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):    

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    hashed_master_key = db.Column(db.String(length=80), nullable=False)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    passwords = db.relationship("Password", backref="owner", lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_master_key):
        self.hashed_master_key = bcrypt.generate_password_hash(plain_master_key)

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_master_key, attempted_password)

    def __repr__(self):
        return f"User: <{self.name}>"
    

class Password(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    service = db.Column(db.String(length=30), nullable=False)
    link = db.Column(db.String(length=200), nullable=False)
    cipher_pass = db.Column(db.String(length=100), nullable=False)
    iv = db.Column(db.String(length=70), nullable=False)
    salt = db.Column(db.String(length=70), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)