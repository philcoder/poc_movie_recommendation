from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_required, logout_user, current_user, login_user

import random

from app import app
from app.forms import LoginForm, RegisterLoginForm
from app.dao import UserDao, MovieDao
from app.services import Publisher

userDao = UserDao()
movieDao = MovieDao()

'''
route exemple: http://localhost:16000/webui
'''
@app.route('/')
@app.route('/webui')
def index():
    #TODO: try to hide this if, maybe using decorator for this
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
        #ignore login from type userrole 'legacy'
        user = userDao.getUserByUsername(form.userName.data)
        if user is None or not user.check_password(form.userPassword.data) or user.userrole == 'old':
            flash(u'Invalid username or password', 'loginError')
            return redirect(url_for('index'))

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)

    registerForm = RegisterLoginForm()
    return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabLoginActive=True)

@app.route('/webui/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/webui/login/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    registerForm = RegisterLoginForm()
    if registerForm.validate_on_submit():
        userDao.add(registerForm.registerName.data, registerForm.registerUserName.data, registerForm.registerUserPassword.data)
        form = LoginForm()
        return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabLoginActive=True)

    form = LoginForm()
    return render_template('login.html', disablemenu=True, form=form, registerForm=registerForm, tabRegisterActive=True)


@app.route('/webui/home')
@login_required
def home():
    user = userDao.getUserById(current_user.get_id())
    import datetime
    userdata = {
        'username' : user.username,
        'date' : datetime.datetime.utcnow()
    }
    return render_template('home.html', data=userdata)

@app.route('/webui/searchMovie', methods=['POST'])
def search_movie_button():
    content = request.get_json()
    movies = movieDao.getMovieByName(content["movie_name"])
    if len(movies) != 0:
        moviePayload = []
        for movie in movies:
            moviePayload.append(
                {
                    'title' : movie.title,
                    'release_date' : movie.release_date,
                    'genres' : movie.genres,
                }
            )

        response = {}
        response['status'] = 'ok'
        response['movies'] = moviePayload[0]

        return jsonify(response)
    else:
        return jsonify({
            'status' : 'not_found'
        })

@app.route('/webui/randomMovie', methods=['GET'])
def random_movie_button():
    movieId = random.randint(1,1600)
    movie = movieDao.getMovieById(movieId)

    response = {}
    response['status'] = 'ok'
    response['movies'] = {
        'title' : movie.title,
        'release_date' : movie.release_date,
        'genres' : movie.genres,
    }

    return jsonify(response)


@app.route('/webui/recommendation', methods=['POST'])
def sent_recommendation_button():
    import datetime
    userdata = {
        'userid' : current_user.get_id(),
        'date' : datetime.datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S")
    }

    content = request.get_json()
    userdata.update(content)

    client = Publisher()
    client.publish(userdata)

    return jsonify(userdata)

@app.route('/webui/unprotected')
def unprotected():
    return render_template('unprotected.html', disablemenu=True)