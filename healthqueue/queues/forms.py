"""
QueueForm

This class represents a Flask-WTF form for queuing a patient.

Attributes:
    title (wtforms.StringField): A StringField representing the patient's name.
        Required by DataRequired validator.
    content (wtforms.TextAreaField): A TextAreaField representing the desired examination types.
        Required by DataRequired validator.
    submit (wtforms.SubmitField): A SubmitField for submitting the form.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class QueueForm(FlaskForm):
    """
    QueueForm

    This class represents a Flask-WTF form for queuing a patient.

    Attributes:
        title (wtforms.StringField): A StringField representing the patient's name.
            Required by DataRequired validator.
        content (wtforms.TextAreaField): A TextAreaField representing the desired examination types.
            Required by DataRequired validator.
        submit (wtforms.SubmitField): A SubmitField for submitting the form.
    """
    title = StringField('Name of Patient', validators=[DataRequired()])
    content = TextAreaField('Types of Examination you want', validators=[DataRequired()])
    submit = SubmitField('Queue')