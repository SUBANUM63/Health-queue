#!/usr/bin/python
"""
This module initializes and configures the Flask application for the HealthQueue project.

Modules:
    Flask: The Flask web framework.
    SQLAlchemy: Flask extension for SQLAlchemy integration.
    Bcrypt: Flask extension for Bcrypt hashing.
    LoginManager: Flask extension for user session management.
    Mail: Flask extension for sending emails.
    Config: Configuration class for the application settings.

Attributes:
    db (SQLAlchemy): Instance of SQLAlchemy for database operations.
    bcrypt (Bcrypt): Instance of Bcrypt for password hashing.
    login_manager (LoginManager): Instance of LoginManager for managing user sessions.
    mail (Mail): Instance of Mail for sending emails.

Functions:
    create_app(config_class=Config): Creates and configures the Flask application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from healthqueue.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    """
    Creates and configures the Flask application.

    Args:
        config_class (class): The configuration class to use for the application settings.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from healthqueue.users.routes import users
    from healthqueue.queues.routes import queues
    from healthqueue.main.routes import main
    from healthqueue.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(queues)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
