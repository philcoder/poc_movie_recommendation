import time

from app.dao import TestDao


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics.pairwise import pairwise_distances

class Engine:

    def test(self, data):
        print(" [x] Received %r" % data)

        time.sleep(10)

        text = "You watch the {} at {}".format(data["type"], data["date"])
        dao = TestDao()
        dao.insertDataOnForm(text, int(data["userid"]))
        dao.close()
        print(" [x] Done")

    def loadMovieLensDataset(self):
        r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
        self.ratings = pd.read_csv('app/dataset/u.data', sep='\t', names=r_cols,encoding='latin-1')

    def collaborativeFilteringModel(self):
        print(type(self.ratings))
        print(self.ratings.head())

        #default dataset
        n_users = self.ratings.user_id.unique().shape[0] #943 users
        n_items = self.ratings.movie_id.unique().shape[0] #1682 movies
        
        #init matrix with zeros and populate with ratings
        data_matrix = np.zeros((n_users, n_items))
        for line in self.ratings.itertuples():
            data_matrix[line[1]-1, line[2]-1] = line[3]

        #user_similarity = pairwise_distances(data_matrix, metric='cosine')
        item_similarity = pairwise_distances(data_matrix.T, metric='cosine') #use matrix transpose

        #user_prediction = self.predict(data_matrix, user_similarity, type='user') #between user-user
        item_prediction = self.predict(data_matrix, item_similarity, type='item')

        userid = 5
        print(self.extractTopMovies(item_prediction[userid]))
        
    

    def predict(self, ratings, similarity, type='user'):
        if type == 'user':
            mean_user_rating = ratings.mean(axis=1)
            #We use np.newaxis so that mean_user_rating has same format as ratings
            ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
            return mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
        elif type == 'item':
            return ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
        
    
    def extractTopMovies(self, item_prediction, size = 5):
        count = 1
        movies_tuples = []
        for item in np.nditer(item_prediction):
            movies_tuples.append((count, item))
            count += 1

        def takeSecond(elem):
            return elem[1]
        
        movies_tuples = sorted(movies_tuples, key=takeSecond, reverse=True)
        movies_tuples = movies_tuples[0:size]
        movies_ids = [id[0] for id in movies_tuples]
        
        movies_ids.sort()
        return movies_tuples

