from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from .models import User, Comment, Comment_Like
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
import json
import os
import secrets

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    users_array = []

    if request.method == 'GET':
        users_db = User.query.limit(10).all()

        for user in users_db:
            user_json = {"img": user.profile_photo,
            "nick": user.username,
            "id": user.id,}
            users_array.append(user_json)

        return render_template("index.html", user=current_user, users = users_db, usersjson = users_array)


@views.route('/profile/<user>', methods= ['GET', 'POST'])
@login_required
def profile(user):
    user_db = User.query.filter_by(username=user).first()
    print(user_db)
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

                            # IF: Si el usuario tiene una foto de perfil y no se toca el boton para remover la foto y se paso una foto en el input profile photo
                            if current_user.profile_photo and not remove_profile_photo == "on" and profile_photo:
                                os.remove(os.path.join(current_app.root_path, 'static/profilephotos', current_user.profile_photo))
                                current_user.profile_photo = save_images(profile_photo, "profilephotos")
                            # ELIF1: Si el usuario no tiene foto, no quiere borrar su foto y tiene pasada una foto, es decir, un valor en el input file
                            elif not current_user.profile_photo and not remove_profile_photo == "on" and profile_photo:
                                current_user.profile_photo = save_images(profile_photo, "profilephotos")
                            # ELIF2: Si el usuario tiene una foto de perfil y el checkbox esta activado y no tiene pasada ninguna foto. Elmina la foto y deja el dato null
                            elif current_user.profile_photo and remove_profile_photo == "on" and not profile_photo:
                                os.remove(os.path.join(current_app.root_path, 'static/profilephotos', current_user.profile_photo))
                                current_user.profile_photo = None

                            # IF: Si el usuario tiene una foto de banner y no se toca el boton para remover la foto de banner y se paso una foto en el input profile banner
                            if current_user.profile_banner and not remove_profile_banner == "on" and profile_banner:
                                os.remove(os.path.join(current_app.root_path, 'static/profilebanners', current_user.profile_banner))
                                current_user.profile_banner = save_images(profile_banner, "profilebanners" )
                            elif not current_user.profile_banner and not remove_profile_banner == "on" and profile_banner:
                                # ELIF1: Si el usuario no tiene foto de banner, no quiere borrar su foto de banner y tiene pasada una foto de banner, es decir, un valor en el input file
                                current_user.profile_banner = save_images(profile_banner, "profilebanners")
                            elif current_user.profile_banner and remove_profile_banner == "on" and not profile_banner:
                                # ELIF2: Si el usuario tiene una foto de banner y el checkbox esta activado y no tiene pasada ninguna foto banner. Elmina la foto y deja el dato null
                                os.remove(os.path.join(current_app.root_path, 'static/profilebanners', current_user.profile_banner))
                                current_user.profile_banner = None

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



def save_images (photo, route):
    if photo:
        hash_photo = secrets.token_urlsafe(10)
        _, file_extension = os.path.splitext(photo.filename)
        photo_name = hash_photo + file_extension
        file_path = os.path.join(current_app.root_path, f'static/{route}', photo_name)
        photo.save(file_path)
        return photo_name

@views.route("/<user>/<comment_id>", methods=['GET'])
@login_required
def like(user, comment_id):
    user_db = User.query.filter_by(username=user).first()
    comment = Comment.query.filter_by(id = comment_id)
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

    print(user_db, user, current_user.username)
    if user_db and user == current_user.username:
        return redirect(url_for('views.profile', user = current_user.username))
    else:
        return redirect(url_for('views.profile', user = user_db.username))
