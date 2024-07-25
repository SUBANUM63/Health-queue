from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class QueueForm(FlaskForm):
    title = StringField('Name of Patient', validators=[DataRequired()])
    content = TextAreaField('Types of Exmination you want', validators=[DataRequired()])
    submit = SubmitField('Queue')
