"""Flask app for Feedback"""

from flask import Flask, render_template, redirect, session
from models import db, connect_db, User
from forms import AddRegistrationForm, AddLoginForm
# from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = "thisisthekey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:drowssap@localhost:5432/feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()


@app.route('/')
def root():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_view():
    form = AddRegistrationForm()

    if form.validate_on_submit():


        u = User.register(username = form.username.data, password = form.password.data, email = form.email.data, first_name = form.first_name.data, last_name = form.last_name.data)
        session["username"] = u.username

        return redirect("/secret")

    else:
        return render_template('register.html', form=form)
    
@app.route('/login', methods=["GET", "POST"])
def login_view():
    form = AddLoginForm()

    if form.validate_on_submit():

        u = User.query.one_or_none(form.username.data)
        if u:
            if User.login(form.username.data, form.password.data):
                session["username"] = u.username
    else:
        return render_template('login.html', form=form)

@app.route('/secret')
def secret_view():
    if session["username"]:
        return "You are logged in'!"
    else:
        return redirect('/login')
