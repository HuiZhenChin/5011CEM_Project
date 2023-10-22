import pandas as pd
import nltk
from googletrans import Translator
from textblob import TextBlob

nltk.download("punkt")

review = pd.read_csv("olist_order_reviews_dataset.csv")
review.dropna(subset=["review_comment_message"], inplace=True)

# 1000 samples
sampled_review = review.sample(n=1000, random_state=42)

def translate_to_english(comment):
    translator = Translator()
    translated = translator.translate(comment, src='pt', dest='en')
    return translated.text

def assign_sentiment_label(comment):
    analysis = TextBlob(comment)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        return 'positive'
    elif sentiment == 0:
        return 'neutral'
    else:
        return 'negative'

# translate Portuguese comments to English
sampled_review['translated_comment'] = sampled_review['review_comment_message'].apply(translate_to_english)

# assign sentiment labels
sampled_review['sentiment_label'] = sampled_review['translated_comment'].apply(assign_sentiment_label)

# save results to a new CSV file
sampled_review.to_csv('translated_reviews.csv', index=False)

