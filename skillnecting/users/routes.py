from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from skillnecting import db, bcrypt
from skillnecting.models import User, Post
from skillnecting.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from skillnecting.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """function to register new user
        Take data from registration form
        hash password using bcrypt and then store user details into db
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            github_username=form.github_username.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """Funtion to validate username and password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            """login_user takes two paramenters
                user: takes data from user and queries data base to find if it exits
                if exists, uses bcrypt.check_password_hash to 
                validate is password is correct
                remember: enables form to remember data is user checks true
            """
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """Function to logout users"""
    print(request.referrer)
    logout_user()
    return redirect(request.referrer)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Function to return/update user account"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


@users.route("/<string:username>/posts")
def user_posts(username):
    """Function to return posts per user"""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_post.html", posts=posts, user=user)


@users.route("/home/<string:username>")
@users.route("/<string:username>")
def user_profile(username):
    """Funtion to return User profile"""
    user = User.query.filter_by(username=username).first_or_404()
    print(user)
    return render_template("user_profile.html", user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """Function to get request to reset password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('main.login'))
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Function to reset token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your Password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", title="Reset Password", form=form)
