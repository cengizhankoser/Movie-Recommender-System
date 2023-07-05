import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
import joblib


movies_df = pd.read_csv('movies.dat', sep='::', engine='python', header=None, names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')
ratings_df = pd.read_csv('ratings.dat', sep='::', engine='python', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
ratings = pd.merge(movies_df,ratings_df).drop(['Genres', 'Timestamp'], axis=1)

user_ratings = ratings.pivot_table(index=['UserID'], columns=['Title'], values='Rating')
user_ratings = user_ratings.dropna(thresh=10,axis=1).fillna(0)

item_similarity_df = user_ratings.corr(method='pearson')
print(item_similarity_df)

