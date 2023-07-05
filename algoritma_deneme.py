import pandas as pd
from scipy.stats import pearsonr
import random
from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient('mongodb+srv://cengizhankoserr:DreY7Fk744oSbMZX@movielens.oaqf0tu.mongodb.net/')

# Veritabanı seçimi
db = client['movielens']

# Collection seçimi
collection = db['similarity_between_movies']

# Veri setini yükleme
movies_df = pd.read_csv('movies.dat', sep='::', engine='python', header=None, names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')
ratings_df = pd.read_csv('ratings.dat', sep='::', engine='python', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])

# İlk 20 filmleri seçme
movies_subset = movies_df.head(20)
ratings_subset = ratings_df[ratings_df['MovieID'].isin(movies_subset['MovieID'])]

# Film-film benzerlik matrisini oluşturma
ratings_pivot = ratings_subset.pivot(index='MovieID', columns='UserID', values='Rating').fillna(0)

def calculate_similarity(movie_id_1, movie_id_2):
    ratings_1 = ratings_pivot.loc[movie_id_1]
    ratings_2 = ratings_pivot.loc[movie_id_2]
    correlation, _ = pearsonr(ratings_1, ratings_2)
    return correlation

def create_similarity_matrix(movie_ids):
    similarity_matrix = pd.DataFrame(index=movie_ids, columns=movie_ids)
    for movie_id_1 in movie_ids:
        for movie_id_2 in movie_ids:
            similarity = calculate_similarity(movie_id_1, movie_id_2)
            similarity_matrix.loc[movie_id_1, movie_id_2] = similarity
    return similarity_matrix

# İlk 20 filmler için benzerlik matrisini oluşturma
subset_movie_ids = movies_subset['MovieID'].tolist()
similarity_matrix = create_similarity_matrix(subset_movie_ids)

# MongoDB'ye benzerlik matrisini yükleme
for i, movie_id_1 in enumerate(subset_movie_ids):
    similarity_scores = []
    for movie_id_2 in subset_movie_ids:
        similarity = similarity_matrix.loc[movie_id_1, movie_id_2]
        similarity_scores.append(similarity)
    
    # MongoDB belgesi oluşturma
    document = {
        '_id': movie_id_1,
        'similarity_scores': similarity_scores
    }
    
    # Belgeyi MongoDB'ye ekleme
    collection.insert_one(document)


'''
# Rastgele bir film seçme
random_movie_id = random.choice(subset_movie_ids)
random_movie_title = movies_df[movies_df['MovieID'] == random_movie_id]['Title'].values[0]

# Rastgele filmin en benzer olduğu 5 filmi bulma
similar_movies = similarity_matrix[random_movie_id].sort_values(ascending=False)[1:6]
recommended_movies = [movies_df[movies_df['MovieID'] == movie_id]['Title'].values[0] for movie_id in similar_movies.index]

# Sonuçları görüntüleme
print(f"Rastgele Seçilen Film: {random_movie_title}")
print("En Benzer Filmler:")
for movie in recommended_movies:
    print(movie)
'''