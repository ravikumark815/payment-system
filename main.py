import fps
from forms import RegistrationForm, LoginForm
from flask import Flask, render_template, url_for, flash, redirect
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b6d0232afb913ea0'

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