from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class PinCreation(FlaskForm):
    """Form for creating and updating Pin"""
    picture = FileField('Please upload image of your new pin',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg', 'mp4', 'movie', 'gif'])])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    pin_content = StringField('Content', validators=[DataRequired(), Length(max=150)])
    is_private = BooleanField('Private Pin?')
    is_notification_active = BooleanField('Notification Active?')
    submit = SubmitField('Post')
