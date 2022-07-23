from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    profile_photo = db.Column(db.String(120), nullable=True)
    profile_banner = db.Column(db.String(120), nullable=True)
    last_connection = db.Column(db.String(120), nullable = False)