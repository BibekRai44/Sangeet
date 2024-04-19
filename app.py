from flask import Flask, render_template, request, jsonify
import pickle
app = Flask(__name__)

model=pickle.load(open('predict_artist.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    
    followers_count = request.json['followersCount']
    popularity = request.json['popularity']

    prediction = model.predict([[followers_count, popularity]])
    predicted_artist_name = prediction[0]

    return jsonify({'artistName': predicted_artist_name})

if __name__ == '__main__':
    app.run(debug=True)
