#!/usr/bin/python
"""
This module handles the user-related routes and functionality for the HealthQueue application.

Routes:
    - /register: Handles user registration.
    - /login: Handles user login.
    - /logout: Logs out the current user.
    - /account: Displays and allows updating of the current user's account information.
    - /user/<string:username>: Displays the queues created by a specific user.
    - /reset_password: Handles password reset requests.
    - /reset_password/<token>: Handles the reset password functionality using a token.

Imports:
    - render_template: Renders templates for the web application.
    - url_for: Generates URLs for the web application.
    - flash: Displays flash messages to the user.
    - redirect: Redirects the user to a different route.
    - request: Handles HTTP requests.
    - Blueprint: Creates a blueprint for user-related routes.
    - login_user: Logs in a user.
    - current_user: Represents the currently logged-in user.
    - logout_user: Logs out the current user.
    - login_required: Ensures that a route can only be accessed by logged-in users.
    - db: Database instance for SQLAlchemy.
    - bcrypt: Bcrypt instance for password hashing.
    - User: User model.
    - Queue: Queue model.
    - RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm: Forms for user-related actions.
    - save_picture, send_reset_email: Utility functions for saving profile pictures and sending reset emails.

Functions:
    - register: Handles user registration.
    - login: Handles user login.
    - logout: Logs out the current user.
    - account: Displays and allows updating of the current user's account information.
    - user_queues: Displays the queues created by a specific user.
    - reset_request: Handles password reset requests.
    - reset_token: Handles the reset password functionality using a token.
"""

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from healthqueue import db, bcrypt
from healthqueue.models import User, Queue
from healthqueue.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from healthqueue.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Handle the registration of new users.

    If the user is already authenticated, redirect them to the home page.
    If the form is submitted and valid, hash the password, create a new user,
    and add the user to the database. Flash a success message and redirect
    to the login page. Render the registration template with the form.

    Returns:
        - Redirect to home page if already authenticated.
        - Redirect to login page after successful registration.
        - Render the registration page with the form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    If the user is already authenticated, redirect them to the home page.
    If the form is submitted and valid, check the user's email and password,
    log the user in, and redirect them to the next page or home page. Flash
    an error message if login is unsuccessful. Render the login template with
    the form.

    Returns:
        - Redirect to home page if already authenticated.
        - Redirect to the next page or home page after successful login.
        - Render the login page with the form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """
    Handle user logout.

    Log the user out and redirect them to the home page.

    Returns:
        - Redirect to home page after logout.
    """
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Handle account updates for logged-in users.

    If the form is submitted and valid, update the user's username and email,
    and save the profile picture if provided. Flash a success message and
    redirect to the account page. Prepopulate the form fields with the current
    user's information when the page is loaded. Render the account template with
    the form and user's profile picture.

    Returns:
        - Redirect to account page after successful update.
        - Render the account page with the form and profile picture.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_queues(username):
    """
    Display the queues of a specific user.

    Fetch the user by username and paginate their queues, ordered by
    the date they were queued. Render the user_queues template with the
    user's queues and user information.

    Args:
        - username: The username of the user whose queues are to be displayed.

    Returns:
        - Render the user_queues page with the user's queues and information.
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    queues = Queue.query.filter_by(author=user)\
        .order_by(Queue.date_queued.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_queues.html', queues=queues, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    Handle password reset requests.

    If the user is already authenticated, redirect them to the home page.
    If the form is submitted and valid, send a password reset email to the
    user's email address. Flash an informational message and redirect to the
    login page. Render the reset_request template with the form.

    Returns:
        - Redirect to home page if already authenticated.
        - Redirect to login page after requesting a password reset.
        - Render the reset_request page with the form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    Handle password resets using a token.

    If the user is already authenticated, redirect them to the home page.
    Verify the reset token and fetch the user. If the token is invalid or expired,
    flash a warning message and redirect to the reset_request page. If the form is
    submitted and valid, update the user's password and save it to the database.
    Flash a success message and redirect to the login page. Render the reset_token
    template with the form.

    Args:
        - token: The token used to verify the password reset request.

    Returns:
        - Redirect to home page if already authenticated.
        - Redirect to reset_request page if the token is invalid or expired.
        - Redirect to login page after successful password reset.
        - Render the reset_token page with the form.
    """
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
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
