import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
import joblib
from surprise import accuracy
# Veri setini yükleme
movies_df = pd.read_csv('movies.dat', sep='::', engine='python', header=None, names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')
ratings_df = pd.read_csv('ratings.dat', sep='::', engine='python', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
movies_df['Title'] = movies_df['Title'].apply(lambda x: x.split('(')[0].strip())



# Surprise veri setini oluşturma
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['UserID', 'MovieID', 'Rating']], reader)
# Veri setini eğitim ve test kümelerine ayırma
trainset, testset = train_test_split(data, test_size=0.10, random_state=40)

# Item-based Collaborative Filtering modelini eğitme
bsl_options = {
    "method": "als",
    "n_epochs": 100,
}

sim_options = {'name': 'pearson'}
model = KNNBasic(bsl_options=bsl_options,sim_options=sim_options)
model.fit(trainset)

# Modeli kaydetme
joblib.dump(model, 'model8.pkl')
print("Model başarıyla kaydedildi.")

model = joblib.load('model8.pkl')
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print("RMSE:", rmse)
mae = accuracy.mae(predictions)
print("MAE:", mae)
fcp = accuracy.fcp(predictions)
print("FCP:", fcp)

'''

# Bir filmi izleyenlere benzer filmleri önerme
def get_similar_movies(movie_title, top_n=8):
    movie_ids = movies_df[movies_df['Title'] == movie_title]['MovieID']
    if len(movie_ids) == 0:
        return None
    movie_id = movie_ids.values[0]
    similar_movies = model.get_neighbors(movie_id, k=top_n)
    recommended_movies = [movies_df[movies_df['MovieID'] == movie]['Title'].values[0] for movie in similar_movies]
    return recommended_movies

# Örnek kullanım
movie_title = 'Toy Story'
recommended_movies = get_similar_movies(movie_title)
print(f"Filme Benzer Önerilen Filmler: {recommended_movies}")

'''
