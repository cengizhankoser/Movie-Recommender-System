from flask import Flask, request, jsonify
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
import joblib
from flask_cors import CORS
import re
app = Flask(__name__)
CORS(app)

# Modeli yükleme
model = joblib.load('model5.pkl')
movies_df = pd.read_csv('movies.dat', sep='::', engine='python', header=None, names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')
movies_df['Title'] = movies_df['Title'].apply(lambda x: x.split('(')[0].strip())
ratings_df = pd.read_csv('ratings.dat', sep='::', engine='python', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])

# API endpoint'i
@app.route('/api/recommend', methods=['POST'])
def recommend_movies():
    movie_title = request.json['movie_title']
    recommended_movies = get_similar_movies(movie_title)
    if recommended_movies:
        return jsonify({'recommended_movies': recommended_movies})
    else:
        return jsonify({'error': 'oops'})

# Bir filmi izleyenlere benzer filmleri önerme
def get_similar_movies(movie_title, top_n=8):
    movie_ids = movies_df[movies_df['Title'] == movie_title]['MovieID']
    if len(movie_ids) == 0:
        return None
    movie_id = movie_ids.values[0]
    similar_movies = model.get_neighbors(movie_id, k=top_n)
    recommended_movies = [movies_df[movies_df['MovieID'] == movie]['Title'].values[0] for movie in similar_movies]
    return recommended_movies



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
