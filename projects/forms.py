from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, PasswordField, SubmitField # type: ignore
from wtforms.validators import Length,EqualTo, Email, DataRequired, ValidationError # type: ignore
from projects.models import User

class RegisterForm(FlaskForm):

    username = StringField(label="User Name:", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="Email Address:", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label='UserName', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')