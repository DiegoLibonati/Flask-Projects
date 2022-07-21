from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("index.html", user=current_user)

@views.route('/profile/<username>')
@login_required
def profile(username):

    if username == current_user.username:
        return render_template('profile.html', user=current_user)
    else:
        return render_template("<h2>User Not Found</h2>")


