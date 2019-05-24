import time

from app.dao import RatingDao, SeggestMovieDao
from app.dataset import DatasetMovieLens

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import pairwise_distances

'''
PS: this engine executes inside python subprocess...

For more details of implementation see: https://www.analyticsvidhya.com/blog/2018/06/comprehensive-guide-recommendation-engine-python/ (item 4)
'''
class Engine:
    ratingId = None
    useridModelMap = None
    ratingDao = None
    seggestMovieDao = None

    def __init__(self):
        self.ratingDao = RatingDao()
        self.seggestMovieDao = SeggestMovieDao()

    def initCollaborativeFilteringModel(self, ratingId):
        try:
            self.ratingId = ratingId['rating_id']
            datasetMovieLens = DatasetMovieLens()
            dataset = datasetMovieLens.getDataset()
            cols = datasetMovieLens.getDatasetColumns()

            numUsersDatasetMovieLens = dataset.user_id.unique().shape[0]
            userMapIndex = self.userMapIndexModel(numUsersDatasetMovieLens)

            userid = self.ratingDao.getUserIdByRatingId(self.ratingId)
            self.useridModelMap = userMapIndex["{}".format(userid)]

            #get all ratings from database and transf in dataframe
            ratingDatabase = self.ratingDao.getAllRatings()
            ratingDataFrame = self.createRatingDataFrame(userMapIndex, ratingDatabase, cols)

            #create new database
            dataset = dataset.append(ratingDataFrame)

            self.processCollaborativeFilteringModel(dataset)
        except Exception as e: 
            print(e)

    def createRatingDataFrame(self, userMapIndex, ratingDatabase, cols):
        ratingDatabaseWithNewIds = []
        for row in ratingDatabase:
            indexMap = "{}".format(row[0])
            ratingDatabaseWithNewIds.append((userMapIndex[indexMap], row[1], row[2], row[3]))

        return pd.DataFrame(ratingDatabaseWithNewIds, columns=cols)


    def userMapIndexModel(self, numUsersDataset):
        user_ids = self.ratingDao.getDistinctUserId()

        # #correlation between database userid with model userid
        userMapIndex = {}
        count = 1
        for id in user_ids:
            userid_database = "{}".format(id[0])
            userMapIndex[userid_database] = numUsersDataset+count
            count += 1

        return userMapIndex


    def processCollaborativeFilteringModel(self, dataset):
        #count unique elements on dataset
        n_users = dataset.user_id.unique().shape[0] 
        n_items = dataset.movie_id.unique().shape[0]

        #init matrix with zeros and populate with ratings
        data_matrix = np.zeros((n_users, n_items))
        for line in dataset.itertuples():
            data_matrix[line[1]-1, line[2]-1] = line[3]

        #user_similarity = pairwise_distances(data_matrix, metric='cosine')
        item_similarity = pairwise_distances(data_matrix.T, metric='cosine') #use matrix transpose

        #user_prediction = self.predict(data_matrix, user_similarity, type='user') #between user-user
        item_prediction = self.predict(data_matrix, item_similarity, type='item')

        #print(self.extractTopMovies(item_prediction[self.useridModelMap-1]))
        #save results
        selectMovieIds = self.extractTopMovies(item_prediction[self.useridModelMap-1])
        self.seggestMovieDao.addOrUpdate(self.ratingId, selectMovieIds)

        self.ratingDao.close()
        self.seggestMovieDao.close()

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
        return movies_ids