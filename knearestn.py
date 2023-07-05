import pandas as pd
from surprise import Dataset, Reader
from sklearn.neighbors import NearestNeighbors
import joblib
from surprise.model_selection import train_test_split
from surprise import accuracy

# Veri setini yükleme
movies_df = pd.read_csv('movies.dat', sep='::', engine='python', header=None, names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')
ratings_df = pd.read_csv('ratings.dat', sep='::', engine='python', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
movies_df['Title'] = movies_df['Title'].apply(lambda x: x.split('(')[0].strip())

# Surprise veri setini oluşturma
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['UserID', 'MovieID', 'Rating']], reader)
'''

# Kullanıcı-film matrisini oluşturma
trainset, testset = train_test_split(data, test_size=0.20, random_state=40)
user_movie_matrix = trainset.build_testset()

# Komşuluk modelini oluşturma
model = NearestNeighbors(metric='cosine')
model.fit(user_movie_matrix)
joblib.dump(model, 'model4.pkl')
print("Model başarıyla kaydedildi.")

predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print("RMSE:", rmse)
mae = accuracy.mae(predictions)
print("MAE:", mae)
fcp = accuracy.fcp(predictions)
print("FCP:", fcp)
'''
model = joblib.load('model4.pkl')

# Bir film için benzer filmleri bulma
def get_similar_movies(movie_title, top_n=8):
    movie_id = movies_df[movies_df['Title'] == movie_title]['MovieID'].values[0]
    query_movie = trainset.to_inner_iid(movie_id)
    distances, indices = model.kneighbors(trainset.ur[query_movie], n_neighbors=top_n+1)
    similar_movie_ids = [trainset.to_raw_iid(inner_id) for inner_id in indices.flatten()]
    similar_movies = movies_df[movies_df['MovieID'].isin(similar_movie_ids)]['Title'].values
    return similar_movies[1:]

# Örnek kullanım
movie_title = 'Toy Story'
recommended_movies = get_similar_movies(movie_title)
print(f"Filme Benzer Önerilen Filmler: {recommended_movies}")
