from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug.security import check_password_hash
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

@views.route('/profile/edit/<username>', methods = ['GET', 'POST'])
@login_required
def profile_update(username):

    if username == current_user.username:

        if request.method == "POST":
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            user_db = User.query.filter_by(username=username).first()
            email_db = User.query.filter_by(email=email).first()
            print(user_db)
            if not user_db or user_db.username == current_user.username:
                if not email_db or email_db.email == current_user.email:
                    if check_password_hash(current_user.password, password):
                        current_user.username = username
                        current_user.email = email
                        db.session.commit()
                        return render_template("profile.html", user=current_user)   
                    else:
                        flash("The changes could not be applied because the password is invalid.", category="error")
                        return render_template("profile.html", user=current_user)
                else:
                    flash("The changes could not be applied because the email already exists.", category="error")
                    return render_template("profile.html", user=current_user)   
            else:
                flash("The changes could not be applied because the user already exists.", category="error")
                return render_template("profile.html", user=current_user)             

        return render_template('update.html', user=current_user)
    else:
        return "<h2>User Not Found</h2>"


