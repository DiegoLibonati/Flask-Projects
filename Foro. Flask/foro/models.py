from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    profile_photo = db.Column(db.String(120), nullable=True, default="default.webp")
    profile_banner = db.Column(db.String(120), nullable=True, default="default.jpg")
    last_connection = db.Column(db.String(120), nullable = False)
    comments = db.relationship('Comment', backref="user")
    likes = db.relationship('Comment_Like', backref="user")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=True)
    profile_id = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship('Comment_Like', backref="comment")

class Comment_Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
