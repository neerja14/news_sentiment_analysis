import string
import requests
import json
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from langdetect import detect
import mysql.connector
from sqlalchemy import create_engine
import pymysql

nltk.download('punkt')
nltk.download('stopwords')

def fetching():

    def clean_text(text):
        text = text.lower()
        text = ''.join([char for char in text if char not in string.punctuation])
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token not in stopwords.words('english')]
        return ' '.join(tokens)

    def analyze_sentiment(text):
        return TextBlob(text).sentiment

    def categorize_sentiment(polarity):
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'

    def fetch_news():
        base_url= ('https://newsapi.org/v2/everything?'
        'q=(Narendra+Modi)&'
        'language = en&'
        'from=2024-01-10&'
        'to=2024-01-30&'
        'apiKey=0b2702ac89d64fdaac467ab4fc047639'
        )
            # base_url = "https://newsapi.org/v2/everything"
        # params = {
        #     "q": query,
        #     "from": from_date,
        #     "to": to_date,
        #     "sortBy": "publishedAt",
        #     "apiKey": api_key
        # }
        # response = requests.get(base_url, params=params)
        response = requests.get(base_url)
        return response.json()

    def save_to_json(filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file)

    def json_to_df(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            print(data)
        return pd.json_normalize(data, 'articles')

    def is_english(text):
        try:
            return detect(text) == 'en'
        except:
            return False

    def insert_into_db(df,db_config):
        conn=mysql.connector.connect(**db_config)
        cursor=conn.cursor()
        engine=create_engine(f'mysql+pymysql://root:@mysql:3306/news_data_db', echo=False)
        # insert_query="""
        # INSERT INTO news_articles(tittle, content , sentiment , published_at)
        # VALUES(%s, %s, %s , %s)
        # """
        # for _, row in df.iterrows():
        #     values=(row['title'] , row['content'] , row['sentiment'] , row['publishedAt'])
        #     print(values)
        #     cursor.execute(insert_query, values)
        print("Printing DF")
        print(df.head(20))
        print(df.columns.tolist())
        df.to_sql(name='news_articles', con=engine, if_exists='replace')
            
        # conn.commit()
        # cursor.close()
        # conn.close()
        
    # api_key = "0b2702ac89d64fdaac467ab4fc047639"  
    # query = "India OR Maldives"
    # from_date = "2024-01-01"
    # to_date = "2024-01-21"

    news_data = fetch_news()
    save_to_json('news_data.json', news_data)

    df = json_to_df('news_data.json')
    df = df[df['content'].apply(lambda x: is_english(x) if x else False)]
    df['cleaned_content'] = df['content'].apply(lambda x: clean_text(x) if x else '')
    df['sentiment_analysis'] = df['cleaned_content'].apply(lambda x: analyze_sentiment(x))
    df['sentiment'] = df['sentiment_analysis'].apply(lambda x: categorize_sentiment(x.polarity))
    df['publishedAt']=df['publishedAt'].apply(lambda x: x[:10])
    df['publishedAt']=df['publishedAt'].astype('datetime64[ns]')

    print(df)
    db_config={
        'host': 'mysql',
        'user': 'root',
        'port':"3306",
        'database': 'news_data_db'
    }
    insert_into_db(df, db_config)