from app.util import Singleton
import pandas as pd

""" 
DatasetMovieLens is a singleton class. 
See more: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
"""
class DatasetMovieLens(metaclass=Singleton):
    __instance = None
    __cols = None
    __ratings = None

    def __init__(self):
        self._loadDataset()
        if DatasetMovieLens.__instance != None:
            raise Exception("This class is a DatasetMovieLens!")
        else:
            DatasetMovieLens.__instance = self

    def _loadDataset(self):
        self.__cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
        #create a immutable dataframe obj
        self.__ratings = pd.read_csv('app/dataset/u.data', sep='\t', names=self.__cols,encoding='latin-1')

    def getDataset(self):
        return self.__ratings

    def getDatasetColumns(self):
        return self.__cols
