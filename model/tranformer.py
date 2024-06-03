from transformers import pipeline
import pandas as pd

sentiment_pipeline = pipeline('sentiment-analysis')

def get_transformer_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return result['label'].lower()

# Example usage with a dataframe
df = pd.read_csv('database/processed_headline.csv')
df['Transformer_Sentiment'] = df['Processed_Headline'].apply(get_transformer_sentiment)
df.to_csv('model/transformer.csv', index=False)
