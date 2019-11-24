from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from main import Login

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', 
                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_uname(self, uname):
        user = Login.query.filter_by(uname=uname.data).first()
        if user:
            raise ValidationError('Username is already registered. Please login with the same.')

class LoginForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    