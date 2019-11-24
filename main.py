# Libraries
import fps
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, UserMixin, login_user, logout_user, login_required

# Extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b6d0232afb913ea0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/fps'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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

class PaymentForm(FlaskForm):
    amount_paid = IntegerField('Amount')
    card_name = StringField('Card Name')
    card_number = IntegerField('Card Number')
    cvv = IntegerField('CVV', validators=[DataRequired(), Length(min=3, max=3)])
    expiry_month = IntegerField('CVV', validators=[DataRequired(), Length(min=1, max=2)])
    expiry_year = IntegerField('CVV', validators=[DataRequired(), Length(min=4, max=4)])
    fee_type = StringField('Fees', validators=[DataRequired()])

class Login(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    privilege = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Login('{self.uname}', '{self.password}', '{self.privilege}')"

class Fees(db.Model):
    uname = db.Column(db.String(10), primary_key=True, nullable=False)
    exam_fee = db.Column(db.Integer())
    lab_fee = db.Column(db.Integer())
    club_fee = db.Column(db.Integer())
    placement_fee = db.Column(db.Integer())
    stationary_fee = db.Column(db.Integer())
    library_fee = db.Column(db.Integer())

    def __repr__(self):
        return f"Login('{self.uname}', '{self.exam_fee}', '{self.lab_fee}', '{self.club_fee}', '{self.placement_fee}', '{self.stationary_fee}', '{self.library_fee}')"

class Payment(db.Model):
    trans_id = db.Column(db.String(10), primary_key=True, nullable=False)
    payment_type = db.Column(db.String(30), nullable=False)
    uname = db.Column(db.String(10), unique=True, nullable=False)
    amount_to_be_paid = db.Column(db.Integer())
    amount_paid = db.Column(db.Integer())
    amount_left = db.Column(db.Integer())
    card_number = db.Column(db.Integer())
    cvv = db.Column(db.Integer())
    expiry_month = db.Column(db.Integer())
    expiry_year = db.Column(db.Integer())
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Login('{self.trans_id}', '{self.uname}', '{self.amount_to_be_paid}', '{self.amount_paid}', '{self.amount_left}', '{self.card_number}', '{self.cvv}', '{self.expiry_date}', '{self.time_stamp}')"

@app.route("/")
def default():
    return render_template('default.html')

@app.route("/home")
@login_required
def home():
    fee = Fees.query.filter_by(uname=current_user.uname)
    return render_template('home.html', fees=fee)

@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(user_id)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Login.query.filter_by(uname=form.username.data).first()
        if user:
            flash('Username is already registered', 'danger')
        else:
            user = Login(uname=form.username.data, password=hashed_password, privilege="student")
            db.session.add(user)
            db.session.commit()
            user = Fees(exam_fee=0, lab_fee=0, stationary_fee=0, library_fee=0, placement_fee=0, club_fee=0)
            flash(f'Your account has been created', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(uname=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please verify username and password','danger')
    return render_template('login.html', title='login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('default'))

@app.route("/payment", methods=['GET', 'POST'])
@login_required
def payment():
    form = PaymentForm()
    if form.validate_on_submit():
        uname = current_user.uname
        trans_id = bcrypt.generate_password_hash(str(datetime.utcnow)).decode('utf-8')
        fee = Fees.query.filter_by(uname=uname)
        feeType = form.fee_type.data
        amount_to_be_paid = int(fee.feeType)
        amount_left = amount_to_be_paid - int(form.amount_paid.data)
        timestamp = datetime.utcnow
        fee_entry = Payment(trans_id=trans_id, payment_type=feeType, uname=uname, amount_to_be_paid=amount_to_be_paid, amount_left=amount_left, card_number=form.card_number.data, 
                                    cvv=form.cvv.data, expiry_month=form.expiry_month.data, expiry_year=form.expiry_year.data, timestamp=timestamp)
        db.session.add(fee_entry)
        db.session.commit()
        time.sleep(3)
        flash(f'Payment Successful. Redirecting to Home Page.', 'success')
    else:
        flash(f'Payment Failed. Please Try Again.', 'danger')
    return redirect(url_for('home'))

if __name__ == "__main__": 
    app.run(port=5000, debug=True)