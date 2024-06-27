import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from afinn import Afinn

# Load Data:

data = pd.read_csv("../database/processed_Articles.csv")
text_column = "Processed_Article"  # Adjust based on your column name
texts = data[text_column]

# Create TF-IDF Vectorizer:

vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed
features = vectorizer.fit_transform(texts)
# LDA
num_topics = 20  # Adjust num_topics based on domain and desired granularity
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
# print words in lda
lda.fit(features)
for i, topic in enumerate(lda.components_):
    print(f"Top words for topic #{i}:")
    print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-5:]])
    print("\n")
topic_distributions = lda.fit_transform(features)


# KMeans

kmeans = KMeans(n_clusters=3, random_state=42)  # Adjust n_clusters as needed
kmeans.fit(topic_distributions)
clusters = kmeans.predict(topic_distributions)

# Sentiment Lexicon:

sentiment_lexicon = {
    'positive': ['love', 'happy', 'great', 'excellent', 'awesome'],
    'negative': ['hate', 'sad', 'bad', 'terrible', 'awful'],
}
# sentient score

# def sentiment_score(text, lexicon):
#     score = 0
#     for sentiment, words in lexicon.items():
#         for word in words:
#             if word in text:
#                 score += 1 if sentiment == 'positive' else -1
#     return score

# data['sentiment_score'] = texts.apply(lambda text: sentiment_score(text, sentiment_lexicon))
afinn = Afinn()

sentiment_scores = [afinn.score(text) for text in texts]
data['sentiment_score'] = sentiment_scores

# Save Data:
data.to_csv("../database/processed_Articles.csv", index=False)
print(data)


# Define thresholds (adjust based on your analysis)
positive_threshold = 5
negative_threshold = -5

# Categorize sentiment based on thresholds
data['sentiment_category'] = data['sentiment_score'].apply(
    lambda score: 'positive' if score > positive_threshold else (
        'negative' if score < negative_threshold else 'neutral'
    )
)

# Print a sample of the data with sentiment categories
print(data[['sentiment_score', 'sentiment_category']].head())
# save
data.to_csv("../database/processed_Articles.csv", index=False)
