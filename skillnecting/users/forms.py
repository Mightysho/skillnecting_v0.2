from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from skillnecting.models import User


class RegistrationForm(FlaskForm):
    """ Class for registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    github_username = StringField('Github Username', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Function to validate if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        """Function to validate if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

    def validate_github_username(self, github_username):
        """Function to validate if email already exists"""
        user = User.query.filter_by(github_username=github_username.data).first()
        if user:
            raise ValidationError('That Github Username is taken. Please use a different one')


class LoginForm(FlaskForm):
    """ Class for registration form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """ Class for Updating User details"""
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Function to update username of account user"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one')

    def validate_email(self, email):
        """Function to update email of account user"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one')


class RequestResetForm(FlaskForm):
    """Class for Requesting a reset form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """Function to validate if email  exists"""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """Class for creating for to Reset password"""
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
