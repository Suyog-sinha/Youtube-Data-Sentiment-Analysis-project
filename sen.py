import pandas as pd
from google.cloud import language_v1
from google.cloud.language_v1 import enums

client = language_v1.LanguageServiceClient()

def analyze_sentiment(text_content):
    
    type_ = enums.Document.Type.PLAIN_TEXT

    
    document = {"content": text_content, "type": type_}

   
    response = client.analyze_sentiment(document=document)

    
    sentiment = response.document_sentiment
    score = sentiment.score
    magnitude = sentiment.magnitude

    
    if score >= 0.1:
        sentiment_label = "Positive"
    elif score <= -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return sentiment_label, score, magnitude

dataset_path = 'Sentiment_result.csv'
df = pd.read_csv(Sentiment_result.csv)


df['Sentiment'], df['Sentiment Score'], df['Sentiment Magnitude'] = zip(*df['comments'].apply(analyze_sentiment).tolist())


print(df[['comments', 'Sentiment', 'Sentiment Score', 'Sentiment Magnitude']])
