import fps
from datetime import datetime
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b6d0232afb913ea0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/fps'

db = SQLAlchemy(app)

class Login(db.Model):
    uname = db.Column(db.String(10), primary_key=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Login('{self.uname}', '{self.image_file}', '{self.password}')"

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
    uname = db.Column(db.String(10), unique=True, nullable=False)
    amount_to_be_paid = db.Column(db.Integer())
    amount_paid = db.Column(db.Integer())
    amount_left = db.Column(db.Integer())
    card_number = db.Column(db.Integer())
    cvv = db.Column(db.Integer())
    expiry_date = db.Column(db.String(5))
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Login('{self.trans_id}', '{self.uname}', '{self.amount_to_be_paid}', '{self.amount_paid}', '{self.amount_left}', '{self.card_number}', '{self.cvv}', '{self.expiry_date}', '{self.time_stamp}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == 'password':
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please verify username and password','danger')
    return render_template('login.html', title='login', form=form)

if __name__ == "__main__": 
    app.run(debug=True)