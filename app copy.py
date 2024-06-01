from flask import Flask, request, render_template, redirect, url_for, session
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
from link_scrapper import scrapenews
from text_cleaning import clean_text

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session

model = load_model('lstm_model.h5')
tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
sentiment = pickle.load(open('senti.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = ''
    title = ''
    article = ''
    toggle_state = request.form.get('toggle_state')
    if toggle_state == "toggled":
        url = request.form.get('title')
        tempnews = scrapenews(url)
        title = tempnews[0]
        article = tempnews[1]
    elif toggle_state == "not_toggled":
        title = request.form.get('title', '')
        article = request.form.get('article', '')
        print(title+"oyeee hete")
    
    # Store the title and article in session
    session['title'] = title
    session['article'] = article
    session.modified = True
    
    
    text = title + ' ' + article
    
    text = clean_text(text)
    sentiscore = sentiment.polarity_scores(text)
    tokenized_text = tokenizer.texts_to_sequences([text])
    tokenized_text = pad_sequences(tokenized_text, maxlen=250)
    prediction = model.predict(tokenized_text, batch_size=1, verbose=2)[0]

    if sentiscore['compound'] > 0:
        analysis = 'Positive'
    elif sentiscore['compound'] < 0:
        analysis = 'Negative'
    else:
        analysis = 'Neutral'
    if prediction >= 0.5:
        result = "True"
    else:
        result = "False"

    session['prediction_text'] = result
    session['sentiment_text'] = analysis
    
    # Redirect to predict_next route
    return redirect(url_for('predict_next'))

@app.route('/predict_next', methods=["GET", "POST"])
def predict_next():
    prediction_text = session.get('prediction_text', "No prediction made yet.")
    sentiment_text = session.get('sentiment_text', "Cannot perform sentiment analysis.")
    title = session.get('title', "Title not available")
    article = session.get('article', "Article not available")
    
    # Pass correct parameter names to render_template
    return render_template("predict.html", prediction_text="Given article is {}".format(prediction_text), sentiment_text="After performing the sentiment analysis, we found the article to be {}".format(sentiment_text),
                           title="Given title is {}".format(title),
                           article="Given article is {}".format(article))

if __name__ == "__main__":
    app.run(debug=True)
