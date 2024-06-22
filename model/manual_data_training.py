import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Ensure you have the necessary NLTK data files
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

def preprocess_text(text):
    text = text.lower()
    text = re.sub('[^a-z\s]', '', text)
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

def preprocess_articles(input_file, output_file):
    df = pd.read_csv(input_file)
    df = df[df['Article'].notna() & df['Article'].str.strip().astype(bool)]
    df = df.drop_duplicates(subset='Article')
    df['Processed_Article'] = df['Article'].apply(preprocess_text)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = '../database/manual.csv'
    output_file = '../database/manual_processed_Articles.csv'
    preprocess_articles(input_file, output_file)
    print(f"Preprocessed data saved to {output_file}")

    processed_df = pd.read_csv('../database/processed_Articles.csv')
    labeled_df = pd.read_csv('../database/manual_processed_Articles.csv')

    # Mapping sentiment labels to numerical values
    sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    labeled_df['sentiment_numeric'] = labeled_df['sentiment'].map(sentiment_map)

    print(labeled_df['sentiment_numeric'].value_counts())

    X_labeled = labeled_df['Processed_Article']
    y_labeled = labeled_df['sentiment_numeric']  # Use numeric labels
    X_unlabeled = processed_df['Processed_Article']

    vectorizer = TfidfVectorizer(max_features=5000)
    X_labeled_tfidf = vectorizer.fit_transform(X_labeled)
    X_unlabeled_tfidf = vectorizer.transform(X_unlabeled)

    print(X_labeled_tfidf.shape)
    print(X_unlabeled_tfidf.shape)

    stratified_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in stratified_split.split(X_labeled_tfidf, y_labeled):
        X_train, X_test = X_labeled_tfidf[train_index], X_labeled_tfidf[test_index]
        y_train, y_test = y_labeled.iloc[train_index], y_labeled.iloc[test_index]

    param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001], 'kernel': ['rbf', 'linear', 'sigmoid']}
    grid = GridSearchCV(SVC(probability=True), param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)
    print(grid.best_params_)

    best_model = grid.best_estimator_

    y_pred = best_model.predict(X_test)
    print("Prediction Distribution:", pd.Series(y_pred).value_counts())
    print("Model Performance:")
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Define thresholds for classification
    threshold_positive = 0.75
    threshold_negative = -0.75

    # Classify predictions based on thresholds
    y_pred_classified = []
    print(y_pred)
    for pred in y_pred:
        if pred >= threshold_positive:
            y_pred_classified.append('positive')
        elif pred <= threshold_negative:
            y_pred_classified.append('negative')
        else:
            y_pred_classified.append('neutral')

    # Convert to numpy array for consistency
    y_pred_classified = np.array(y_pred_classified)

    # Print and save classification results
    print("Test Set Prediction Distribution:", pd.Series(y_pred_classified).value_counts())

    # Save the best model
    model_filename = 'best_svc_model.pkl'
    joblib.dump(best_model, model_filename)
    print(f"Model saved to {model_filename}")

    # Save the vectorizer
    vectorizer_filename = 'tfidf_vectorizer.pkl'
    joblib.dump(vectorizer, vectorizer_filename)
    print(f"Vectorizer saved to {vectorizer_filename}")
