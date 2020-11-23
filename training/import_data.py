import pandas as pd
from os import listdir
from os.path import isfile, join
import boto3
import json

FILES_DATA_DIRECTORY = './data'

def export_csv(df):
    data = {'Comment': df['Comment'], 
            'Sentiment': df['Sentiment'],
            'Sentiment_Mixed': df['Sentiment_Mixed'],
            'Sentiment_Negative': df['Sentiment_Negative'],
            'Sentiment_Neutral': df['Sentiment_Neutral'],
            'Sentiment_Positive': df['Sentiment_Positive']
            }
    df = pd.DataFrame(data) 
    df.to_csv('./output/result.csv')
    print('-------')
    print('Completed')


def merge_data(files):
    #return pd.read_excel(FILES_DATA_DIRECTORY + '/' + files[1], header=5)
    df_global = []
    for file in files:
        df = pd.read_excel(FILES_DATA_DIRECTORY + '/' + file, header=5)
        df_global.append(df)
    return pd.concat(df_global)

def set_sentiment(df):
    sentiment = []
    sentiment_mixed = []
    sentiment_negative = []
    sentiment_neutral = []
    sentiment_positive = []

    comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')
    i = 1
    length = len(df['Comment'])
    for comment in df['Comment']:
        print(str(i) + ' de ' + str(length))
        i += 1
        text = str(comment)
        response =  comprehend.detect_sentiment(Text=text, LanguageCode='es') #json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='es'), sort_keys=True, indent=4)
        sentiment.append(response['Sentiment'])

        sentiment_mixed.append(response['SentimentScore']['Mixed'])
        sentiment_negative.append(response['SentimentScore']['Negative'])
        sentiment_neutral.append(response['SentimentScore']['Neutral'])
        sentiment_positive.append(response['SentimentScore']['Positive'])

    df['Sentiment'] = pd.Series(sentiment, index=df.index)
    df['Sentiment_Mixed'] = pd.Series(sentiment_mixed, index=df.index)
    df['Sentiment_Negative'] = pd.Series(sentiment_negative, index=df.index)
    df['Sentiment_Neutral'] = pd.Series(sentiment_neutral, index=df.index)
    df['Sentiment_Positive'] = pd.Series(sentiment_positive, index=df.index)

    return df

if __name__ == '__main__':
    onlyfiles = [f for f in listdir(FILES_DATA_DIRECTORY) if isfile(join(FILES_DATA_DIRECTORY, f))]
    
    data = merge_data(onlyfiles)
    data = set_sentiment(data)
    export_csv(data)
