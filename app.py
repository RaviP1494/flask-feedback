"""Flask app for Feedback"""

from flask import Flask, render_template, redirect, session
from models import db, connect_db, User, Feedback
from forms import AddRegistrationForm, AddLoginForm, AddFeedbackForm, UpdateFeedbackForm
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
    # if "username" in session:
    #     return redirect(f"/users/{session['username']}")
    
    form = AddRegistrationForm()

    if form.validate_on_submit():


        u = User.register(username = form.username.data, password = form.password.data, email = form.email.data, first_name = form.first_name.data, last_name = form.last_name.data)
        session["username"] = u.username

        return redirect(f"/users/{u.username}")

    else:
        return render_template('register.html', form=form)
    
@app.route('/login', methods=["GET", "POST"])
def login_view():
    form = AddLoginForm()

    if form.validate_on_submit():

        u = User.query.get(form.username.data)
        if u:
            if User.login(form.username.data, form.password.data):
                session["username"] = u.username
                return redirect(f"/users/{u.username}")
            else:
                return render_template('login.html', form=AddLoginForm())
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_view(username):
    if session["username"]:
        u = User.query.get(username)
        feedbacks = u.feedback
        return render_template('user.html', user=u, fbs = feedbacks)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/users/<username>/delete')
def delete_user(username):
    u = User.query.get(username)
    if session["username"] == u.username:
        db.session.delete(u)
        db.session.commit()
        session.clear()
        return redirect('/')
    else:
        session.clear()
        return redirect('/register')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    form = AddFeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('addfb.html', form=form)

@app.route('/feedback/<int:fb_id>/update', methods=["GET","POST"])
def update_feedback(fb_id):
    feedback = Feedback.query.get(fb_id)

    form = UpdateFeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f'/users/{username}')
    else:
        return render_template('editfb.html', form=form)

@app.route('/feedback/<int:fb_id>/delete', methods=["POST"])
def delete_feedback(fb_id):
    feedback = Feedback.query.get(fb_id)

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.username}')