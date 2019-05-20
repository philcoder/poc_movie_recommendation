from flask import render_template, flash, redirect
from app import app

from app.forms import LoginForm, RegisterLoginForm

'''
route exemple: http://localhost:16000/webui
'''
@app.route('/webui')
def main():
    form = LoginForm()
    registerForm = RegisterLoginForm()
    return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabLoginActive=True)

@app.route('/webui/login/signin', methods=['POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.userLogin.data))
        import datetime
        userdata = {
            'username' : form.userLogin.data,
            'date' : datetime.datetime.utcnow()
        }
        return render_template('home.html', data=userdata)

    registerForm = RegisterLoginForm()
    return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabLoginActive=True)

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
def home():
    import datetime
    userdata = {
        'username' : 'Philipp',
        'date' : datetime.datetime.utcnow()
    }
    return render_template('home.html', data=userdata)