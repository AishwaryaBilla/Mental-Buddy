import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sounddevice as sd
import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    return compound_score

@app.route('/', methods=['GET'])
def index():
    return render_template('templates/index.html')

@app.route('/suggestions', methods=['POST'])
def get_suggestions():
    data = request.form

    if 'input_method' not in data or 'input_text' not in data:
        return jsonify({'error': 'Invalid request data'})

    input_method = data['input_method']
    input_text = data['input_text']

    if input_method == 'text':
        user_input = input_text
    elif input_method == 'audio':
        user_input = analyze_audio_input(input_text)
        if user_input is None:
            return jsonify({'error': 'Could not understand audio.'})
    else:
        return jsonify({'error': 'Invalid input method.'})

    movies_df = pd.read_csv('C:/Users/aishw/OneDrive/Desktop/prog/movies.csv')
    songs_df = pd.read_csv('C:/Users/aishw/OneDrive/Desktop/prog/songs.csv')
    books_df = pd.read_csv('C:/Users/aishw/OneDrive/Desktop/prog/books.csv')

    compound_score = analyze_sentiment(user_input)

    if compound_score > 0:
        movies_suggestion = movies_df.iloc[0].to_dict()
        songs_suggestion = songs_df.iloc[0].to_dict()
        books_suggestion = books_df.iloc[0].to_dict()
    elif -0.25 <= compound_score < 0:
        movies_suggestion = movies_df.iloc[3].to_dict()
        songs_suggestion = songs_df.iloc[3].to_dict()
        books_suggestion = books_df.iloc[3].to_dict()
    elif -0.75 <= compound_score < -0.25:
        movies_suggestion = movies_df.iloc[2].to_dict()
        songs_suggestion = songs_df.iloc[2].to_dict()
        books_suggestion = books_df.iloc[2].to_dict()
    elif -1 <= compound_score < -0.75:
        movies_suggestion = movies_df.iloc[1].to_dict()
        songs_suggestion = songs_df.iloc[1].to_dict()
        books_suggestion = books_df.iloc[1].to_dict()
    else:
        return jsonify({'error': 'Invalid sentiment score'})

    result = {
        'movies': movies_suggestion,
        'songs': songs_suggestion,
        'books': books_suggestion
    }

    return jsonify(result)

def analyze_audio_input(audio):
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None

if __name__ == '__main__':
    app.run(debug=True)
