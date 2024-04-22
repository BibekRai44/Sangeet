from flask import Flask, render_template, request, jsonify,url_for
import pickle
import pandas as pd
app = Flask(__name__)

model=pickle.load(open('predict_artist.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artist_name_predictor')
def artist_name_predictor():
    return render_template('artist_name_predictor.html')

@app.route('/suggest_artist')
def suggest_artist():
    return render_template('artist_suggestor.html')

@app.route('/predict', methods=['POST'])
def predict():
    
    followers_count = request.json['followersCount']
    popularity = request.json['popularity']

    prediction = model.predict([[followers_count, popularity]])
    predicted_artist_name = prediction[0]

    return jsonify({'artistName': predicted_artist_name})

df = pd.read_csv("new_data.csv")

def recommend_similar_artists(artist_name, df, top_n=3):
    artist_name = artist_name.lower()
    
    matching_artists = df[df['Artist Name'].str.lower().str.contains(artist_name)]
    
    if len(matching_artists) == 0:
        print("No artist found with a similar name.")
        return
    input_artist_info = matching_artists.iloc[0]
    
    input_genre = input_artist_info['genres_type']
    
    similar_genre_artists = df[df['genres_type'] == input_genre]
    
    similar_genre_artists = similar_genre_artists[similar_genre_artists['Artist Name'].str.lower() != artist_name]
    
    similar_artists = similar_genre_artists.head(top_n)
    
    return similar_artists

@app.route('/suggest', methods=['POST'])
def suggest():
    artist_name = request.json['artistName']
    similar_artists = recommend_similar_artists(artist_name, df)
    suggested_artist_names = similar_artists['Artist Name'].tolist()
    return jsonify({'artistNames': suggested_artist_names})

if __name__ == '__main__':
    app.run(debug=True)
