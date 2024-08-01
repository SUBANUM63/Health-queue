#!/usr/bin/python
"""
This module defines the forms used for user-related actions in the HealthQueue application.

Imports:
    - FlaskForm: Base class for creating forms with Flask-WTF.
    - FileField: Field for uploading files.
    - FileAllowed: Validator for allowed file extensions.
    - StringField: Field for entering string data.
    - PasswordField: Field for entering password data.
    - SubmitField: Field for form submission.
    - BooleanField: Field for boolean (True/False) values.
    - DataRequired: Validator to ensure field data is provided.
    - Length: Validator to ensure field data length constraints.
    - Email: Validator to ensure a valid email address.
    - EqualTo: Validator to ensure field data matches another field's data.
    - ValidationError: Exception raised during validation errors.
    - current_user: Represents the currently logged-in user.
    - User: User model for querying user data.

Classes:
    - RegistrationForm: Form for user registration.
    - LoginForm: Form for user login.
    - UpdateAccountForm: Form for updating user account information.
    - RequestResetForm: Form for requesting a password reset.
    - ResetPasswordForm: Form for resetting a password.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from healthqueue.models import User


class RegistrationForm(FlaskForm):
    """
    Form for users to create a new account.

    Fields:
        - username: Username with length constraints.
        - email: Email address with validation.
        - password: Password for the account.
        - confirm_password: Confirmation of the password, must match the password.
        - submit: Submit button to register the account.

    Methods:
        - validate_username: Custom validator to check if the username is already taken.
        - validate_email: Custom validator to check if the email is already taken.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    Form for users to log in.

    Fields:
        - email: Email address with validation.
        - password: Password for the account.
        - remember: Checkbox to remember the user.
        - submit: Submit button to log in.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    Form for users to update their account information.

    Fields:
        - username: Username with length constraints.
        - email: Email address with validation.
        - picture: Profile picture file upload.
        - submit: Submit button to update the account.

    Methods:
        - validate_username: Custom validator to check if the username is already taken.
        - validate_email: Custom validator to check if the email is already taken.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    """
    Form for users to request a password reset.

    Fields:
        - email: Email address with validation.
        - submit: Submit button to request the password reset.

    Methods:
        - validate_email: Custom validator to check if the email is associated with an account.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """
    Form for users to reset their password.

    Fields:
        - password: New password for the account.
        - confirm_password: Confirmation of the new password, must match the password.
        - submit: Submit button to reset the password.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
