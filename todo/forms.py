from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(2, 30)])
    password = PasswordField("Password",
                           validators=[DataRequired(), Length(8, 50)])
    password_confirm = PasswordField("Confirm Password",
                                   validators=[DataRequired(), EqualTo("password", "Passwords do not match")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(2, 30)])
    password = PasswordField("Password",
                           validators=[DataRequired(), Length(8, 50)])
    submit = SubmitField("Login")