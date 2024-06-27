import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF
from sklearn.decomposition import SparsePCA 
from sklearn.decomposition import TruncatedSVD  
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from afinn import Afinn
import matplotlib.pyplot as plt

# Load Data:

data = pd.read_csv("../database/processed_Articles.csv")
text_column = "Processed_Article"  # Adjust based on your column name
texts = data[text_column]

# Create TF-IDF Vectorizer:

vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed
features = vectorizer.fit_transform(texts)


# LDA
# num_topics = 20  # Adjust num_topics based on domain and desired granularity
# lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
# # print words in lda
# lda.fit(features)
# for i, topic in enumerate(lda.components_):
#     print(f"Top words for topic #{i}:")
#     print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-5:]])
#     print("\n")
# topic_distributions = lda.fit_transform(features)
# Convert TF-IDF features to dense array
# features_dense = features.toarray()

# # Sparse PCA
# num_topics = 20  # Adjust num_topics based on domain and desired granularity
# sparse_pca = SparsePCA(n_components=num_topics, random_state=42)
# topic_distributions = sparse_pca.fit_transform(features_dense)

# TruncatedSVD
num_topics = 20  # Adjust num_topics based on domain and desired granularity
svd = TruncatedSVD(n_components=num_topics, random_state=42)
topic_distributions = svd.fit_transform(features)


# KMeans

# kmeans = KMeans(n_clusters=3, random_state=42)  # Adjust n_clusters as needed
# kmeans.fit(topic_distributions)
# clusters = kmeans.predict(topic_distributions)



# ... (Rest of your code)

# Hierarchical Clustering (example with Ward linkage)
ward_clusterer = AgglomerativeClustering(n_clusters=3, linkage='ward')
ward_clusterer.fit(topic_distributions)  # Use fit for training
clusters = ward_clusterer.labels_ # Use predict for assigning labels

plt.figure(figsize=(8, 6))
plt.scatter(topic_distributions[:, 0], topic_distributions[:, 1], c=clusters)  # Adjust indexing for your data dimensions
plt.title('Topic Distributions - KMeans Clusters')
plt.xlabel('Component 1')
plt.ylabel('Component 2')  # Adjust labels based on your data
plt.grid(True)
plt.show()

# Add cluster labels to data
data['cluster'] = clusters
print(data['cluster'])
# print count of values in cluster
print(data['cluster'].value_counts())
# Save Data:
data.to_csv("../database/processed_Articles.csv", index=False)



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

# plot the numnber of positive,bnegatives and neutral


# Assuming 'data' is your DataFrame with 'sentiment_category' column

# Count sentiment categories
sentiment_counts = data['sentiment_category'].value_counts()
cluster_count= data['cluster'].value_counts()

# Create the bar chart
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
sentiment_counts.plot(kind='bar', color=['red', 'green', 'blue'])
plt.title('Sentiment Distribution in News Articles')
plt.xlabel('Sentiment Category (P: Positive, N: Negative, neutral)')
plt.ylabel('Count')
plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add subtle gridlines
plt.tight_layout()  # Adjust spacing for better visualization

plt.figure(figsize=(8, 6))  # Adjust figure size as needed
cluster_count.plot(kind='bar', color=['red', 'green', 'blue'])
plt.title('Sentiment Distribution in News Articles')
plt.xlabel('Sentiment Category (P: Positive, N: Negative, neutral)')
plt.ylabel('Count')
plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add subtle gridlines
plt.tight_layout() 




# Assuming 'data' is your DataFrame with 'sentiment_category' and 'Company_name' columns

# Group data by company and sentiment category
sentiment_by_company = (
    data.groupby(['Company_name', 'sentiment_category'])
    .size()
    .to_frame(name='count')
    .unstack(fill_value=0)
)

# Create the stacked bar chart
sentiment_by_company.plot(kind='bar', stacked=True, colormap='Set3')
plt.title('Sentiment Distribution by Company')
plt.xlabel('Company Name')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.legend(title='Sentiment Category')
plt.tight_layout()

plt.show()
