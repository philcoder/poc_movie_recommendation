from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_required, logout_user, current_user, login_user

import random

from app import app
from app.forms import LoginForm, RegisterLoginForm
from app.dao import UserDao, MovieDao, UserRatingDao, SuggestMoviesDao
from app.services import Publisher

userDao = UserDao()
movieDao = MovieDao()
userRatingDao = UserRatingDao()
suggestMoviesDao = SuggestMoviesDao()


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
        registerForm.registerName.data = ""
        registerForm.registerUserName.data = ""
        registerForm.registerUserPassword.data = ""
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
        'menu_button_text' : 'History'
    }
    return render_template('home.html', data=userdata)

@app.route('/webui/searchMovie', methods=['POST'])
def search_movie_button():
    content = request.get_json()
    movies = movieDao.getMovieByName(content["movie_name"])
    if len(movies) != 0:
        return create_movie_response(movies[0])
    else:
        return jsonify({
            'status' : 'not_found'
        })

@app.route('/webui/randomMovie', methods=['GET'])
def random_movie_button():
    movieId = random.randint(1,1600)
    movie = movieDao.getMovieById(movieId)
    return create_movie_response(movie)

def create_movie_response(movie):
    response = {}
    response['status'] = 'ok'
    response['movie'] = {
        'id' : movie.id,
        'title' : movie.title,
        'release_date' : movie.release_date,
        'genres' : movie.genres,
    }

    return jsonify(response)


@app.route('/webui/recommendation', methods=['POST'])
def sent_recommendation_button():
    content = request.get_json()

    userId = int(current_user.get_id())
    movieId = int(content["movie_id"])
    rating = int(content["rating"])

    ratingId = -1
    userRating = userRatingDao.getIdUserRating(userId, movieId)
    if userRating is None:
        userRatingDao.add(userId, movieId, rating)
        userRating = userRatingDao.getIdUserRating(userId, movieId)
        ratingId = userRating.id
    else:
        ratingId = userRating.id
        userRatingDao.updateRating(ratingId, rating)

    response = {}
    response['rating_id'] = ratingId

    client = Publisher()
    client.publish(response)

    response['status'] = 'ok'
    return jsonify(response)

@app.route('/webui/watchRecommendation', methods=['POST'])
def watch_movie_recommendation():
    content = request.get_json()
    suggestMovies = suggestMoviesDao.getSuggestMovieByRating(content['rating_id'])

    response = {}
    if not suggestMovies:
        response['status'] = 'empty_table'
    else:
        response['status'] = 'ok'
        movies = []
        for suggest in suggestMovies:
            movies.append({
                'title' : suggest.movie.title,
                'genres' : suggest.movie.genres,
            })
        response['movies'] = movies

    return jsonify(response)

@app.route('/webui/history')
@login_required
def history():
    user = userDao.getUserById(current_user.get_id())
    userdata = {
        'username' : user.username,
        'menu_button_text' : 'Home'
    }
    return render_template('history.html', data=userdata)

@app.route('/webui/userRatings', methods=['GET'])
def getUserRatings():
    userRatings = userRatingDao.getUserRatingByUserId(current_user.get_id())
    response = {}
    if not userRatings:
        response['status'] = 'empty_table'
    else:
        response['status'] = 'ok'

        ratings = []
        for user in userRatings:
            ratings.append({
                'title' : user.movie.title,
                'rating' : user.rating,
                'suggests' : getMoviesFromArray(user.suggest_movies),
            })
        response['history_ratings'] = ratings
    
    return jsonify(response)

def getMoviesFromArray(suggest_movies):
    movies = ""
    for suggest in suggest_movies:
        movies += suggest.movie.title + "; "
        
    return movies[:-2]