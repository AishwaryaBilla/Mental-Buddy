import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sounddevice as sd
import speech_recognition as sr
from textblob import TextBlob
import pandas as pd

def get_text_input():
    text = input("Enter your text: ")
    return text

def get_audio_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Error occurred: {0}".format(e))

# Ask the user for input method
input_method = input("Enter 'text' for text input or 'audio' for audio input: ")

if input_method == 'text':
    user_input = get_text_input()
elif input_method == 'audio':
    user_input = get_audio_input()
else:
    print("Invalid input method.")

analyzer = SentimentIntensityAnalyzer()
scores = analyzer.polarity_scores(user_input)

movies_df = pd.read_csv('C:/Users/aishw/OneDrive/Desktop/prog/movies.csv')
songs_df = pd.read_csv('C:/Users/aishw/OneDrive/Desktop/prog/songs.csv')
books_df = pd.read_csv('C:/Users/aishw/OneDrive/Desktop/prog/books.csv')

compound_score = scores['compound']

if compound_score > 0:
    print("The movies suggested are:\n")
    print(movies_df.iloc[0])
    print("\n\nThe songs suggested are:\n")
    print(songs_df.iloc[0])
    print("\n\nThe books suggested are:\n")
    print(books_df.iloc[0])
elif -0.25 <= compound_score < 0:
    print("The movies suggested are:\n")
    print(movies_df.iloc[3])
    print("\n\nThe songs suggested are:\n")
    print(songs_df.iloc[3])
    print("\n\nThe books suggested are:\n")
    print(books_df.iloc[3])
elif -0.75 <= compound_score < -0.25:
    print("The movies suggested are:\n")
    print(movies_df.iloc[2])
    print("\n\nThe songs suggested are:\n")
    print(songs_df.iloc[2])
    print("\n\nThe books suggested are:\n")
    print(books_df.iloc[2])
elif -1 <= compound_score < -0.75:
    print("The movies suggested are:\n")
    print(movies_df.iloc[1])
    print("\n\nThe songs suggested are:\n")
    print(songs_df.iloc[1])
    print("\n\nThe books suggested are:\n")
    print(books_df.iloc[1])
