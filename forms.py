from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class TodoForm(FlaskForm):
    todo = StringField("Todo")
    submit = SubmitField("Add Todo")


class NewUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()]),
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    photo = StringField("Photo File")
    admin = BooleanField("Admin")
    submit = SubmitField("Add User")


