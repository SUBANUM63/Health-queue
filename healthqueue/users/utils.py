#!/usr/bin/python
"""
This module provides utility functions for the HealthQueue application.

Functions:
    - save_picture: Saves and resizes a user's profile picture.
    - send_reset_email: Sends an email to reset a user's password.

Imports:
    - os: Provides a portable way of using operating system-dependent functionality.
    - secrets: Provides access to the most secure source of randomness.
    - Image: Class from the PIL (Pillow) library to handle image processing.
    - url_for: Generates URLs for the application.
    - current_app: Represents the current Flask application.
    - Message: Class from Flask-Mail to handle email messages.
    - mail: Instance of the Mail class from Flask-Mail, initialized in the main application.
"""

import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from healthqueue import mail


def save_picture(form_picture):
    """
    Save a profile picture uploaded by the user.

    Generates a random filename for the picture to avoid filename collisions,
    resizes the image to a standard size, and saves it in the 'static/profile_pics'
    directory.

    Args:
        - form_picture: The uploaded picture file.

    Returns:
        - picture_fn: The filename of the saved picture.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    """
    Send a password reset email to the user.

    Generates a password reset token and sends an email with a link to reset
    the password. If the user did not request a password reset, they can ignore
    the email.

    Args:
        - user: The user object representing the recipient of the email.

    Returns:
        - None
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
