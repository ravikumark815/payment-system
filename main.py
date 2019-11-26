# Libraries
import fps
import time
from datetime import datetime, timedelta, date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, UserMixin, login_user, logout_user, login_required
from random import randint

# Extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b6d0232afb913ea0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/fps'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# HTML Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=10, max=13)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_uname(self, uname):
        user = Login.query.filter_by(uname=uname.data).first()
        if user:
            raise ValidationError('Username is already registered. Please login with the same.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=10, max=13)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PaymentForm(FlaskForm):
    amount_paid = IntegerField('Amount')
    card_name = StringField('Name of the Card Holder')
    card_number = IntegerField('Card Number')
    cvv = IntegerField('CVV', validators=[DataRequired()])
    expiry_month = IntegerField('Card Expiry Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    expiry_year = IntegerField('Card Expiry Year', validators=[DataRequired(), NumberRange(min=2019, max=2030)])
    fee_type = StringField('Fee Type')
    submit = SubmitField('Submit')
    # fee_type = SelectField('Fees', choices=['Exam Fees','Lab Fees','Library Fees','Placement Fees','Stationary Fees','Club Fees'], validators=[DataRequired()])

class StatisticsForm(FlaskForm):
    from_date = IntegerField('Start Date', validators=[DataRequired(), NumberRange(min=1, max=31)])
    from_month = IntegerField('Start Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    from_year = IntegerField('Start Year', validators=[DataRequired(), NumberRange(min=2000, max=2020)])
    to_date = IntegerField('End Date', validators=[DataRequired(), NumberRange(min=1, max=31)])
    to_month = IntegerField('End Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    to_year = IntegerField('End Year', validators=[DataRequired(), NumberRange(min=2000, max=2020)])
    submit = SubmitField('Submit')

class AccountResetForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=10, max=13)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

# My SQL Models
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
        return f"Fees('{self.uname}', '{self.exam_fee}', '{self.lab_fee}', '{self.club_fee}', '{self.placement_fee}', '{self.stationary_fee}', '{self.library_fee}')"

class Payment(db.Model):
    transaction_id = db.Column(db.String(10), primary_key=True, nullable=False)
    payment_type = db.Column(db.String(30), nullable=False)
    uname = db.Column(db.String(10), unique=True, nullable=False)
    amount_to_be_paid = db.Column(db.Integer())
    amount_paid = db.Column(db.Integer())
    amount_left = db.Column(db.Integer())
    card_number = db.Column(db.Integer())
    cvv = db.Column(db.Integer())
    expiry_month = db.Column(db.Integer())
    expiry_year = db.Column(db.Integer())
    date = db.Column(db.Integer())
    month = db.Column(db.Integer())
    year = db.Column(db.Integer())
    usn = db.Column(db.String(45))

    def __repr__(self):
        return f"Payment('{self.transaction_id}', '{self.payment_type}', '{self.uname}', '{self.amount_to_be_paid}', '{self.amount_paid}', '{self.amount_left}', '{self.card_number}', '{self.cvv}', '{self.expiry_month}', '{self.expiry_year}', '{self.date}', '{self.month}', '{self.year}')"

# Flask Routes
@app.route("/")
def default():
    return render_template('default.html')

@app.route("/home")
@login_required
def home():
    fee = Fees.query.filter_by(uname=current_user.uname)
    return render_template('home.html', fees=fee)

@app.route("/recent")
@login_required
def recent():
    pay = Payment.query.filter_by(usn=current_user.uname)
    return render_template('recent.html', pay=pay)

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
            id = 0
            privilege="student"
            if form.username.data.lower()=="administrator":
                id = 1
                privilege="administrator"
            user = Login(uname=form.username.data, password=hashed_password, privilege=privilege, id=id)
            db.session.add(user)
            db.session.commit()
            user = Fees(uname=form.username.data, exam_fee=0, lab_fee=0, stationary_fee=0, library_fee=0, placement_fee=0, club_fee=0)
            db.session.add(user)
            db.session.commit()
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

@app.route("/cred", methods=['GET', 'POST'])
@login_required
def cred():
    form = AccountResetForm()
    if current_user.is_authenticated:
        if current_user.uname.lower()=='administrator':
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = Login.query.filter_by(uname=form.username.data).first()
                if user:
                    user = Login(uname=form.username.data, password=hashed_password, privilege="student")
                    user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    user.password = "asknacksnlsdc"
                    db.session.commit()
                    flash('Password has been reset successfully', 'success')
                else:
                    flash('Invalid Username. Please Verify', 'danger')
        else:
            flash('Only Administrator has privileges for this operation.','danger')
            return redirect(url_for('home'))
    return render_template('cred.html', title='Account Reset', form = form)

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
        trans_id = randint(1000000000,9999999999)
        fee = Fees.query.filter_by(uname=uname).first()
        amount_to_be_paid = 0
        if form.fee_type.data.lower() == 'exam':
            amount_to_be_paid = int(fee.exam_fee)
        elif form.fee_type.data.lower() == 'library':
            amount_to_be_paid = int(fee.exam_fee)
        elif form.fee_type.data.lower() == 'stationary':
            amount_to_be_paid = int(fee.exam_fee)
        elif form.fee_type.data.lower() == 'placement':
            amount_to_be_paid = int(fee.exam_fee)
        elif form.fee_type.data.lower() == 'club':
            amount_to_be_paid = int(fee.exam_fee)
        elif form.fee_type.data.lower() == 'lab':
            amount_to_be_paid = int(fee.exam_fee)
        else:
            flash(f'Please enter valid Fees Type. (Exam/Library/Stationary/Lab/Club/Placement)', 'danger')
        amount_left = int(amount_to_be_paid) - int(form.amount_paid.data)
        today = date.today()
        fee_entry = Payment(transaction_id=trans_id, payment_type=form.fee_type.data, usn=uname, amount_to_be_paid=amount_to_be_paid, amount_left=amount_left, amount_paid=form.amount_paid.data, uname='administrator', card_number=form.card_number.data, 
                                    cvv=form.cvv.data, expiry_month=form.expiry_month.data, expiry_year=form.expiry_year.data, date=today.day, month=today.month,  year=today.year)
        db.session.add(fee_entry)
        db.session.commit()
        time.sleep(3)
        flash(f'Payment Successful.', 'success')
        return render_template('receipt.html', data=fee_entry, title='Receipt', form=form)
    return render_template('payment.html', title='Payment', form=form)

@app.route("/stats", methods=['GET', 'POST'])
@login_required
def stats():
    form = StatisticsForm()
    if current_user.is_authenticated:
        if current_user.uname.lower()=='administrator':
            if form.validate_on_submit():
                uname = current_user.uname
                pay_entry = Payment.query.filter_by(uname=uname)
                stats = []
                start,end = datetime(form.from_year.data, form.from_month.data, form.from_date.data), datetime(form.to_year.data, form.to_month.data, form.to_date.data)
                dates = [start + timedelta(days=i) for i in range((end-start).days+1)]
                for i in pay_entry:
                    if datetime(i.year, i.month, i.date) in dates:
                        stats.append(i)
                if len(stats):
                    total = 0
                    for i in stats:
                        total += int(i.amount_paid)
                    return render_template('stats.html', stats=stats, total=total, form=form)
                else:
                    flash(f'No Payments made in this date range', 'success')
        else:
            flash('Only Administrator has privileges for this operation.','danger')
            return redirect(url_for('home'))
    return render_template('stats.html', title='Statistics', form=form)

if __name__ == "__main__": 
    app.run(port=5000, debug=True)