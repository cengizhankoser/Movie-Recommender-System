import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Veri setini yükleme
movies_df = pd.read_csv('movies.dat', sep='::', engine='python', header=None, names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')
ratings_df = pd.read_csv('ratings.dat', sep='::', engine='python', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])

# Film-film benzerlik matrisini oluşturma
ratings_pivot = ratings_df.pivot(index='UserID', columns='MovieID', values='Rating').fillna(0)
ratings_array = ratings_pivot.to_numpy()

def get_similar_movies(movie_title, top_n=5):
    movie_id = movies_df[movies_df['Title'] == movie_title]['MovieID'].values[0]
    target_movie_ratings = ratings_array[:, movie_id]

    # Benzerlik matrisini hesaplama
    similarity_matrix = 1 - pdist(ratings_array.T, metric='correlation')
    similarity_matrix = squareform(similarity_matrix)

    # MovieID'ye göre sıralama
    similar_movies_indices = np.argsort(similarity_matrix[movie_id])[::-1][1:]
    similar_movies = [(index, similarity_matrix[movie_id][index]) for index in similar_movies_indices]

    recommended_movies = [movies_df[movies_df['MovieID'] == movie[0]]['Title'].values[0] for movie in similar_movies[:top_n]]
    return recommended_movies

# Örnek kullanım
movie_title = 'Toy Story (1995)'
recommended_movies = get_similar_movies(movie_title)

# Önerilen filmleri yazdırma
print(f"Filme Benzer Önerilen Filmler:")
for movie in recommended_movies:
    print(movie)
