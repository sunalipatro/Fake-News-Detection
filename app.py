from flask import Flask, request, render_template, redirect, url_for, session
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
from text_cleaning import clean_text
from link_scrapper import scrapenews

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'



model = load_model('lstm_model.h5')
tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
sentiment = pickle.load(open('senti.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_text', methods=['POST'])
def predict_text():

    form_id = request.form.get('formid')
    if form_id == '1':
        title = request.form.get('title', '')
        article = request.form.get('article', '')
    elif form_id == '2':
        url = request.form.get('link')
        tempnews = scrapenews(url)
        title = tempnews[0]
        article = tempnews[1]
    
    text = title + ' ' + article
    # print(title)
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
    # session['title'] = title
    # session['article'] = article
    return redirect(url_for('predict_next'))



@app.route('/predict_next', methods=["GET", "POST"])
def predict_next():
    prediction_text = session.get('prediction_text', "No prediction made yet.")
    sentiment_text = session.get('sentiment_text', "Cannot perform sentiment analysis.")
    title = session.get("title","No title added")
    article = session.get("article","No article added")
    return render_template("predict.html", prediction_text="Given article is {}".format(prediction_text),sentiment_text="After performing the sentiment analysis, we found the article to be {}".format(sentiment_text))

# if __name__ == "__main__":
#     app.run(debug=False,host="0.0.0.0")
