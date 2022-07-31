from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from .models import User, Comment, Comment_Like
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
import json
import os
from datetime import datetime
from .functions import save_images, check_files_on_update

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    users_array = []
    users_on = []

    if request.method == "POST":
        pass

    if request.method == 'GET':
        users_db = User.query.limit(10).all()
        users_db_ons = User.query.all()
        
        time_now = datetime.utcnow()

        for user in users_db_ons:
            time_afk = time_now - user.is_active
            time_afk = str(time_afk)
            values_time = time_afk.split(":")
            minutes = int(values_time[1])
            if minutes < 5:
                users_on.append(user)
        
        for user in users_db:
            user_json = {"img": user.profile_photo,
            "nick": user.username,
            "id": user.id,}
            users_array.append(user_json)

        return render_template("index.html", user=current_user, users = users_db, usersjson = users_array, users_on = users_on)


@views.route('/profile/<user>', methods= ['GET', 'POST'])
@login_required
def profile(user):
    user_db = User.query.filter_by(username=user).first()
    profile_comments_db = db.session.query(User,Comment).join(Comment).filter_by(profile_id = user_db.id)

    if request.method == 'POST':

        content = request.form.get('comment')

        new_comment = Comment(content = content,user_id = current_user.id, profile_id = user_db.id)
        db.session.add(new_comment)
        db.session.commit()

        if user_db and user == current_user.username:
            return redirect(url_for('views.profile', user = current_user.username))
        else:
            return redirect(url_for('views.profile', user = user_db.username))

    if request.method == 'GET':

        if user_db and user == current_user.username:
            return render_template('profile.html', user=current_user, comments = profile_comments_db)
        elif user_db and user == user_db.username:
            return render_template('profile.html', user=user_db, comments = profile_comments_db)
        else:
            return render_template("<h2>User Not Found</h2>")

@views.route('/profile/edit/<username>', methods = ['GET', 'POST'])
@login_required
def profile_update(username):
    
    user_db = User.query.filter_by(username=username).first()
    profile_comments_db = db.session.query(User,Comment).join(Comment).filter_by(profile_id = user_db.id)

    # El update se va a cargar solo si el usuario que se pasa por url es igual al usuario logeado.
    if username == current_user.username:

        if request.method == "POST":
            # Obtenemos todos los datos del form.
            username = request.form.get('username')
            email = request.form.get('email')
            profile_photo = request.files.get('profile_photo')
            remove_profile_photo = request.form.get('removeprofilephoto')
            profile_banner = request.files.get('profile_banner')
            remove_profile_banner = request.form.get('removeprofilebanner')
            password = request.form.get('password')

            # Obtenemos si el username existe en la base de datos al igual que el mail.
            user_db = User.query.filter_by(username=username).first()
            email_db = User.query.filter_by(email=email).first()


            # Chequea si todos los datos del update al dar update son iguales, es decir, si no fueron editados.
            if (user_db and user_db.username == username) and user_db.email == email and not profile_photo and not remove_profile_photo == "on" and not profile_banner and not remove_profile_banner == "on":
                flash("You cant edit with the same information.", category="error")
                return redirect(url_for('views.profile', user = current_user.username))
            else:
                # Si no existe dicho usuario.
                if not user_db or user_db.username == current_user.username:
                    # Si no existe dicho email.
                    if not email_db or email_db.email == current_user.email:
                        # Si la contraseña pasada es igual a la contraseña encriptada en la base de datos
                        if check_password_hash(current_user.password, password):

                            current_user.username = username
                            current_user.email = email
                            current_profile_photo_user = current_user.profile_photo 
                            current_profile_banner_user = current_user.profile_banner 

                            current_user.profile_photo = check_files_on_update(current_profile_photo_user, profile_photo, current_app, remove_profile_photo, "profilephotos", "default.webp")
                            current_user.profile_banner = check_files_on_update(current_profile_banner_user, profile_banner, current_app, remove_profile_banner, "profilebanners", "default.jpg") 

                            db.session.commit()
                            return redirect(url_for('views.profile', user = current_user.username))   
                        else:
                            flash("The changes could not be applied because the password is invalid.", category="error")
                            return redirect(url_for('views.profile', user = current_user.username))
                    else:
                        flash("The changes could not be applied because the email already exists.", category="error")
                        return redirect(url_for('views.profile', user = current_user.username))
                else:
                    flash("The changes could not be applied because the user already exists.", category="error")
                    return redirect(url_for('views.profile', user = current_user.username))

                         

        return render_template('update.html', user=current_user, comments = profile_comments_db)
    else:
        return "<h2>User Not Found</h2>"


@views.route("/<user>/<comment_id>/like", methods=['GET'])
@login_required
def like(user, comment_id):
    comment = Comment.query.filter_by(id = comment_id).first()
    user_db = User.query.filter_by(id=comment.profile_id).first()
    like = Comment_Like.query.filter_by(user_id = current_user.id, comment_id = comment_id).first()

    if not comment:
        flash('Comment does not exist.', category="error")
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Comment_Like(user_id = current_user.id, comment_id = comment_id)
        db.session.add(like)
        db.session.commit()

    if user_db:
        return redirect(url_for('views.profile', user = user_db.username))

@views.route("<user>/<comment_id>/delete")
@login_required
def delete_comment(user ,comment_id):
    comment = Comment.query.filter_by(id = comment_id).first()


    if not comment:
        flash('Comment does not exist.', category="error")
    else:
        user_db = User.query.filter_by(id=comment.profile_id).first()

        db.session.delete(comment)
        db.session.commit()

        if user_db:
            return redirect(url_for('views.profile', user = user_db.username))

    return redirect(url_for('views.profile', user = user))


@views.before_request
@login_required
def update_user_is_active():
    current_user.is_active = datetime.utcnow()
    db.session.commit()