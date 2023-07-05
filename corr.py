import pandas as pd
import numpy as np
import pickle

# Veri setini yükleme
movies_df = pd.read_csv('movies.dat', sep='::', engine='python', header=None, names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')
ratings_df = pd.read_csv('ratings.dat', sep='::', engine='python', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])

# Benzerlik matrisini yükleme veya hesaplama
try:
    with open('similarities.pickle', 'rb') as f:
        similarities = pickle.load(f)
except FileNotFoundError:
    # Filmlerin benzerlik matrisini hesaplamak için pivot tablosu oluşturma
    ratings_pivot = ratings_df.pivot(index='UserID', columns='MovieID', values='Rating').fillna(0)

    # Pearson korelasyon katsayısı hesaplama
    similarities = ratings_pivot.corr(method='pearson')

    # Benzerlik matrisini kaydetme
    with open('similarities.pickle', 'wb') as f:
        pickle.dump(similarities, f)

# Örnek olarak, belirli bir film için benzer filmleri gösterme
movie_id = 28  # İlgilenilen film ID'si
similar_movies = similarities[movie_id].sort_values(ascending=False)[:10]  # En benzer 10 film
similar_movie_titles = movies_df[movies_df['MovieID'].isin(similar_movies.index)]['Title']

# Benzer filmlerin sonuçlarını yazdırma
print(f"Benzer filmler {movies_df[movies_df['MovieID'] == movie_id]['Title'].iloc[0]} için:")
print(similar_movie_titles)
