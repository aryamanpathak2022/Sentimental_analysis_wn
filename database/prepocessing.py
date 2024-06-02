import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure you have the necessary NLTK data files
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove all characters other than alphabets
    text = re.sub('[^a-z\s]', '', text)
    
    # Tokenization
    words = nltk.word_tokenize(text)
    
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Rejoin words to form the processed sentence
    return ' '.join(words)

def preprocess_headlines(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file)
    
    # Remove rows with null values
    df.dropna(inplace=True)
    
    # Preprocess each headline
    df['Processed_Headline'] = df['Headline'].apply(preprocess_text)
    
    # Save the processed headlines to a new CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = 'headlines.csv'  # Input CSV file
    output_file = 'processed_headlines.csv'  # Output CSV file
    preprocess_headlines(input_file, output_file)
    print(f"Preprocessed data saved to {output_file}")
