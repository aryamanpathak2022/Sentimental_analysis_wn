from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flair.data import Sentence
from flair.models import TextClassifier
import pandas as pd

# Load Flair sentiment model (adjust model name as needed)
sentiment_model = TextClassifier.load('sentiment-fast')

data = pd.read_csv("../database/processed_Articles.csv")
text_column = "Processed_Article"  # Adjust based on your column name
texts = data[text_column]

# Create empty lists to store sentiment scores
textblob_scores = []
vader_scores = []
flair_scores = []

for text in texts:
    # TextBlob
    blob = TextBlob(text)
    textblob_scores.append(blob.sentiment.polarity)

    # VADER
    analyzer = SentimentIntensityAnalyzer()
    vader_scores.append(analyzer.polarity_scores(text)['compound'])

    # Flair
    sentence = Sentence(text)
    sentiment_model.predict(sentence)
    flair_scores.append(sentence.labels[0].score)  # Get score from first label

# ensemble

max_scores = []
for i in range(len(texts)):
    max_scores.append(max(textblob_scores[i], vader_scores[i], flair_scores[i]))

data['max_sentiment_score'] = max_scores


positive_threshold = 0.5
negative_threshold = -0.5

data['max_sentiment_category'] = data['max_sentiment_score'].apply(
    lambda score: 'positive' if score > positive_threshold else (
        'negative' if score < negative_threshold else 'neutral'
    )
)