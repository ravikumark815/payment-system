from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', 
                validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')