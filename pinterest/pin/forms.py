from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class PinCreation(FlaskForm):
    """Form for creating and updating Pin"""
    picture = FileField('Please upload image of your new pin',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg', 'mp4', 'movie', 'gif'])])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    pin_content = StringField('Content', validators=[DataRequired(), Length(max=150)])
    is_private = BooleanField('Private Pin?')
    submit = SubmitField('Post')


class PinboardCreation(FlaskForm):
    """Form for creating a pin board"""
    pin_board_name = StringField('PinBoard Name', validators=[DataRequired(), Length(min=2, max=80)])
    board_is_private = BooleanField('Keep this board a secret')
    submit = SubmitField('Create')


class AddPinToPinboard(FlaskForm):
    submit = SubmitField('Add to pinboard?')


class FilteredPins(FlaskForm):
    submit = SubmitField('Go')


class Like(FlaskForm):
    submit = SubmitField('LIKE')


class CommentForm(FlaskForm):
    comment = StringField('Add comment', validators=[DataRequired()])
    submit = SubmitField('Post')



