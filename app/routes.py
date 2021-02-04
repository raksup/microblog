from flask import render_template, flash, url_for, redirect
from flask_login.utils import login_required
from datetime import datetime
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_manager, login_user, current_user, logout_user

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    posts = [
        {'author': {'username':'John'}, 'body':'Have a good day.'},
        {'author': {'username':'Susan'}, 'body':'Nice movie in theatres.'}
    ]
    return render_template('index.html', title='Index', posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#For user profile page
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    posts = [
        {'author':user, 'body':'Test Post #1'},
        {'author':user, 'body':'Test Post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
