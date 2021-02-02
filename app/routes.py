from flask import render_template, flash, url_for, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Raksup'}
    posts = [
        {'author': {'username':'John'}, 'body':'Have a good day.'},
        {'author': {'username':'Susan'}, 'body':'Nice movie in theatres.'}
    ]
    return render_template('index.html', user=user, title='Index', posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)