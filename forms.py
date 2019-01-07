from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import TextAreaField
from wtforms import BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import ValidationError
from models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),
		Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
		validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken')

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),
		Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	picture = FileField('Update Profile picture', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update')

	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken')

	def validate_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken')


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),Email()])
	submit = SubmitField('Request Password')

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
		validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Reset Password')