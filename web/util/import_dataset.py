#!/usr/bin/python3

import os
import sys

# setup dynamic project path for custom imports work
# this 'split' on '/util/' refer to folder where that script is located...
projectPath = os.path.realpath(__file__).split("/util/")[0]
sys.path.append(projectPath)

import pandas as pd
from app.models import Movie, User
from app.dao import MovieDao, UserDao

def main():
    insertMovieData()
    insertUserData()

def insertMovieData():
    movieDao = MovieDao()
    if movieDao.count() == 0:
        movie_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure','Animation', 
        'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy','Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 
        'Thriller', 'War', 'Western']
        moviesDataFrame = pd.read_csv('util/dataset/u.item', sep='|', names=movie_cols,encoding='latin-1')

        movies = []
        for line in moviesDataFrame.itertuples():
            genres = getGenreFromArray(line[6:25], movie_cols)
            movies.append(Movie(id=line[1], title=line[2], release_date=line[3], genres=genres))

        movieDao.addAll(movies)

    else:
        print("Movies already loaded!")
    
def getGenreFromArray(genre_array, movie_cols):
    index = 5
    genres = ""
    for genre_select in genre_array:
        if genre_select == 1:
            genres += movie_cols[index] + ", "
        
        index+=1
        
    return genres[:-2]

def insertUserData():
    userDao = UserDao()
    if userDao.count() == 1:
        u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
        usersDataFrame = pd.read_csv('util/dataset/u.user', sep='|', names=u_cols,encoding='latin-1')

        n_users = usersDataFrame.user_id.unique().shape[0] #943 users

        #create a fix pw
        user = User()
        user.set_password('123')
        generate_user_password = user.password_hash

        count = 1
        users = []
        while count <= n_users:
            username = "user_{}".format(count)
            user = User(name='legacy user',username=username, userrole='old', password_hash=generate_user_password)
            users.append(user)

            count += 1

        userDao.addAll(users)

    else:
        print("Users already loaded!")


main()