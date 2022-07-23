from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug.security import check_password_hash
import json
import os
import secrets

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
            profile_photo = request.files.get('profile_photo')
            remove_profile_photo = request.form.get('removeprofilephoto')
            profile_banner = request.files.get('profile_banner')
            remove_profile_banner = request.form.get('removeprofilebanner')
            password = request.form.get('password')

            user_db = User.query.filter_by(username=username).first()
            email_db = User.query.filter_by(email=email).first()

            if user_db.username == username and user_db.email == email and not profile_photo and not remove_profile_photo == "on" and not profile_banner and not remove_profile_banner == "on":
                flash("You cant edit with the same information.", category="error")
                return render_template("profile.html", user=current_user)
            else:
                if not user_db or user_db.username == current_user.username:
                    if not email_db or email_db.email == current_user.email:
                        if check_password_hash(current_user.password, password):
                            current_user.username = username
                            current_user.email = email
                            if current_user.profile_photo and not remove_profile_photo == "on":
                                os.remove(os.path.join(current_app.root_path, 'static/profilephotos', current_user.profile_photo))
                                current_user.profile_photo = save_images(profile_photo, "profilephotos")
                            elif not current_user.profile_photo and not remove_profile_photo == "on":
                                current_user.profile_photo = save_images(profile_photo, "profilephotos")
                            else:
                                os.remove(os.path.join(current_app.root_path, 'static/profilephotos', current_user.profile_photo))
                                current_user.profile_photo = None

                            if current_user.profile_banner and not remove_profile_banner == "on":
                                os.remove(os.path.join(current_app.root_path, 'static/profilebanners', current_user.profile_banner))
                                current_user.profile_banner = save_images(profile_banner, "profilebanners")
                            elif not current_user.profile_banner and not remove_profile_photo == "on":
                                current_user.profile_banner = save_images(profile_banner, "profilebanners")
                            else:
                                os.remove(os.path.join(current_app.root_path, 'static/profilebanners', current_user.profile_banner))
                                current_user.profile_banner = None

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



def save_images (photo, route):
    if photo:
        hash_photo = secrets.token_urlsafe(10)
        _, file_extension = os.path.splitext(photo.filename)
        photo_name = hash_photo + file_extension
        file_path = os.path.join(current_app.root_path, f'static/{route}', photo_name)
        photo.save(file_path)
        return photo_name

