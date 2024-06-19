import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the processed and labeled data
processed_df = pd.read_csv('../database/processed_Articles.csv')
labeled_df = pd.read_csv('../database/manual.csv')

# Prepare the data for training and vectorization
X_labeled = labeled_df['Article']
y_labeled = labeled_df['sentiment']
X_unlabeled = processed_df['Processed_Article']

# Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_labeled_tfidf = vectorizer.fit_transform(X_labeled)
X_unlabeled_tfidf = vectorizer.transform(X_unlabeled)

# Split labeled data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_labeled_tfidf, y_labeled, test_size=0.2, random_state=42)

# Train the initial SVC model
initial_model = SVC(probability=True)
initial_model.fit(X_train, y_train)

# Evaluate the initial model
y_pred = initial_model.predict(X_test)
print("Initial Model Performance:")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Save the trained model
model_filename = 'initial_svc_model.pkl'
joblib.dump(initial_model, model_filename)
print(f"Model saved to {model_filename}")

# Save the vectorizer
vectorizer_filename = 'tfidf_vectorizer.pkl'
joblib.dump(vectorizer, vectorizer_filename)
print(f"Vectorizer saved to {vectorizer_filename}")
