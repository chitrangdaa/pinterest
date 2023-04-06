from functools import wraps
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from pinterest import db, bcrypt
from pinterest.models import User
from pinterest.users.forms import (RegistrationForm, LoginForm,
                                   RequestResetForm, ResetPasswordForm, UpdateForm, ChangePasswordForm)
from pinterest.users.utils import send_reset_email, save_picture
#import cloudinary.uploader

users = Blueprint('users', __name__)


def authenticated(f):
    """ A decorator for checking if the user is authenticated or not"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.home'))

    return decorated_function


@users.route("/register", methods=['GET', 'POST'])
@authenticated
def register():
    """User Registration Route"""

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please log-in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='register', form=form)


@users.route("/login", methods=['GET', 'POST'])
@authenticated
def login():
    """User Login Route"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        admin = User.query.filter_by(is_admin=True, email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data) and not admin:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash('You have been logged in !', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif admin and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Welcome Admin !', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin.home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='loginn', form=form)


@users.route("/logout")
@login_required
def logout():
    """logout Route"""
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """ Update profile """
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            #upload_result = cloudinary.uploader.upload(form.picture.data, folder="Profile_Pics")
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # for showing current data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
@authenticated
def reset_request():
    """For requesting to change password and calling send email function"""
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
@authenticated
def reset_token(token):
    """for checking if the token still exists and changing password"""
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('You password has been changed successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/changepassword", methods=['GET', 'POST'])
@login_required
def change_password():
    """ For changing password """
    if current_user.is_authenticated:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if bcrypt.check_password_hash(current_user.password, form.old_password.data):
                hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                current_user.password = hashed_password
                db.session.commit()
                flash("Password changed successfully", category='success')
                return redirect(url_for('users.account'))
            else:
                flash("Incorrect Password,please try again", category='danger')
                return redirect(url_for('users.change_password'))
    return render_template('change_password.html', form=form, title='change password')
