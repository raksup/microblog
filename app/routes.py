from flask import render_template, flash, url_for, redirect
from flask_login.utils import login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_manager, login_user, current_user, logout_user

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

@login_required
@app.route('/logout')
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