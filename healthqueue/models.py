#!/usr/bin/python
"""
This module defines the database models for the HealthQueue application.

Imports:
    - datetime: Provides classes for manipulating dates and times.
    - URLSafeTimedSerializer: Provides a timed URL-safe serializer for generating tokens.
    - current_app: Proxy to the application handling the current request.
    - db: Database instance from the HealthQueue application.
    - login_manager: Login manager instance from the HealthQueue application.
    - UserMixin: Provides default implementations for the methods that Flask-Login expects user objects to have.
"""

from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from healthqueue import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by their user ID.

    This function is used by Flask-Login to manage user sessions.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user object corresponding to the given user ID.
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    User model for storing user-related information.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        image_file (str): The profile image filename of the user.
        password (str): The hashed password of the user.
        queues (list): List of queues associated with the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    queues = db.relationship('Queue', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        Generates a password reset token for the user.

        Args:
            expires_sec (int): The expiration time for the token in seconds. Defaults to 1800 seconds (30 minutes).

        Returns:
            str: The generated token.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Verifies a password reset token.

        Args:
            token (str): The token to verify.

        Returns:
            User: The user object if the token is valid, None otherwise.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Queue(db.Model):
    """
    Queue model for storing queue-related information.

    Attributes:
        id (int): Unique identifier for the queue.
        title (str): The title of the queue.
        date_queued (datetime): The date and time when the queue was created.
        content (str): The content of the queue.
        user_id (int): The ID of the user who created the queue.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_queued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Queue('{self.title}', '{self.date_queued}')"
