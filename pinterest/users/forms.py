from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from pinterest.models import User


from pinterest.users.utils import validate_password


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), validate_password])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """for validation of unique username"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken,please choose a different one!')

    def validate_email(self, email):
        """for validation of unique email"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken,please choose a different one!')


class LoginForm(FlaskForm):
    """User/Admin Login Form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateForm(FlaskForm):
    """User/Admin Update Profile Form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Checking if the username is already taken by other user or not"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken,please choose a different one!')

    def validate_email(self, email):
        """Checking if the email is already taken by other user or not"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken,please choose a different one!')


class RequestResetForm(FlaskForm):
    """Reset Request Form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """Checking if the email entered for forgot password corresponds some account or not"""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account of that email!')


class ResetPasswordForm(FlaskForm):
    """Reset Password Form"""
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Password Reset')
