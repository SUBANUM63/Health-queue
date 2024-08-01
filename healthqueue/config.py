#!/usr/bin/python
"""
 Module for Configuration of the Flask application.
"""

import os


class Config:
    """
    Configuration class for the Flask application.

    This class sets up configuration variables for the application, including
    secret keys, database URIs, and mail server settings. Configuration values
    are typically retrieved from environment variables to ensure security and
    flexibility.

    Attributes:
        - SECRET_KEY: Secret key for securing sessions and cookies.
        - SQLALCHEMY_DATABASE_URI: URI for the SQLAlchemy database connection.
        - MAIL_SERVER: Mail server address for sending emails.
        - MAIL_PORT: Port to use for the mail server.
        - MAIL_USE_TLS: Whether to use TLS for securing the mail server connection.
        - MAIL_USERNAME: Username for authenticating with the mail server.
        - MAIL_PASSWORD: Password for authenticating with the mail server.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
