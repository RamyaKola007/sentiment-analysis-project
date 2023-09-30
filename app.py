# app.py

from flask import Flask, render_template, request
import spacy
from textblob import TextBlob

app = Flask(__name__)

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define a list of predefined features
predefined_features = ["product", "service", "company", "movie", "comedy","action","drama","quality","sentiment","thing"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']

    # Perform sentiment analysis using TextBlob for the entire text
    overall_sentiment = perform_sentiment_analysis(text)

    # Extract predefined features and adjectives from the text
    extracted_features = extract_predefined_features(text)
    extracted_adjectives = extract_adjectives(text)

    return render_template('result.html', text=text, overall_sentiment=overall_sentiment,
                           extracted_features=extracted_features, extracted_adjectives=extracted_adjectives)

def perform_sentiment_analysis(text):
    # Perform sentiment analysis using TextBlob
    analysis = TextBlob(text)
    sentiment_polarity = analysis.sentiment.polarity

    if sentiment_polarity > 0:
        return "Positive"
    elif sentiment_polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def extract_predefined_features(text):
    # Initialize an empty list to store extracted predefined features
    extracted_features = []

    # Convert the text to lowercase for case-insensitive matching
    text_lower = text.lower()

    # Check if each predefined feature exists in the text
    for feature in predefined_features:
        feature_lower = feature.lower()
        if feature_lower in text_lower:
            extracted_features.append(feature)

    return extracted_features

def extract_adjectives(text):
    # Initialize an empty list to store extracted adjectives
    extracted_adjectives = []

    # Process the text using spaCy
    doc = nlp(text)

    # Iterate through the tokens in the processed text
    for token in doc:
        # Check if the token is an adjective
        if token.pos_ == "ADJ":
            extracted_adjectives.append(token.text)

    return extracted_adjectives

if __name__ == '__main__':
    app.run(debug=True)
