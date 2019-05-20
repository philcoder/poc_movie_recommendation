from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_required, logout_user, current_user, login_user

from app import app
from app.forms import LoginForm, RegisterLoginForm
from app.models import User, Post

'''
route exemple: http://localhost:16000/webui
'''
@app.route('/')
@app.route('/webui')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    registerForm = RegisterLoginForm()
    return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabLoginActive=True)

@app.route('/webui/login/signin', methods=['POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.userLogin.data).first()
        if user is None or not user.check_password(form.userPassword.data):
            flash(u'Invalid username or password', 'loginError')
            return redirect(url_for('index'))

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
        #return redirect(url_for('home'))

    registerForm = RegisterLoginForm()
    return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabLoginActive=True)

@app.route('/webui/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/webui/login/register', methods=['POST'])
def register():
    registerForm = RegisterLoginForm()
    if registerForm.validate_on_submit():
        registerForm.registerNameUser.data = ""
        registerForm.registerUserLogin.data = ""
        registerForm.registerUserPassword.data = ""
        form = LoginForm()
        return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabLoginActive=True)

    form = LoginForm()
    return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabRegisterActive=True)


@app.route('/webui/home')
@login_required
def home():
    import datetime
    userdata = {
        'username' : 'Philipp Xubad0',
        'date' : datetime.datetime.utcnow()
    }
    return render_template('home.html', data=userdata)

@app.route('/webui/unprotected')
def unprotected():
    return render_template('unprotected.html', disablemenu=True)