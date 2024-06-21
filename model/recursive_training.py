import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the model and vectorizer
model_filename = 'initial_svc_model.pkl'
vectorizer_filename = 'tfidf_vectorizer.pkl'
initial_model = joblib.load(model_filename)
vectorizer = joblib.load(vectorizer_filename)

# Load the processed and labeled data
processed_df = pd.read_csv('../database/processed_Articles.csv')
labeled_df = pd.read_csv('../database/manual.csv')

# Prepare the data for training and vectorization
X_labeled = labeled_df['Article']
y_labeled = labeled_df['sentiment']
X_unlabeled = processed_df['Processed_Article']

# Vectorize the text data using TF-IDF
X_labeled_tfidf = vectorizer.fit_transform(X_labeled).toarray()
X_unlabeled_tfidf = vectorizer.transform(X_unlabeled).toarray()

# Split labeled data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_labeled_tfidf, y_labeled, test_size=0.2, random_state=42)

# Recursive training function
def recursive_training(model, X_train, y_train, X_unlabeled, confidence_threshold=0.5, max_iterations=10):
    for iteration in range(max_iterations):
        if X_unlabeled.shape[0] == 0:
            print("No more unlabeled data left.")
            break
        
        # Predict probabilities on the unlabeled data
        probas = model.predict_proba(X_unlabeled)
        max_probas = np.max(probas, axis=1)
        
        # Select the most confident predictions
        confident_indices = np.where(max_probas >= confidence_threshold)[0]
        if len(confident_indices) == 0:
            print("No confident predictions left.")
            break
        print(confident_indices)
        confident_labels = model.predict(X_unlabeled[confident_indices])
        
        # Add confident predictions to the training set
        X_new_train = X_unlabeled[confident_indices]
        y_new_train = confident_labels

        # Remove the confident predictions from the unlabeled set
        X_unlabeled = np.delete(X_unlabeled, confident_indices, axis=0)
        
        X_train = np.vstack((X_train, X_new_train))
        y_train = np.hstack((y_train, y_new_train))
        
        # Retrain the model
        model.fit(X_train, y_train)
        print(f"Iteration {iteration + 1}: Added {len(confident_indices)} new labeled examples.")
        confidence_threshold+=0.15
    
    return model

# Perform recursive training
final_model = recursive_training(initial_model, X_train, y_train, X_unlabeled_tfidf)

# Evaluate the final model
y_pred_final = final_model.predict(X_test)
print("Final Model Performance:")
print(classification_report(y_test, y_pred_final))
print(f"Accuracy: {accuracy_score(y_test, y_pred_final)}")

# Save the final model
final_model_filename = 'final_svc_model.pkl'
joblib.dump(final_model, final_model_filename)
print(f"Final model saved to {final_model_filename}")
