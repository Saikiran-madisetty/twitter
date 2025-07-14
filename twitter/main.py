import configparser
from sqlalchemy import create_engine, text
import tweepy
 
# Load config
config = configparser.ConfigParser(interpolation=None)
config.read(r"C:\Users\Saikiran\OneDrive - Kasmo Digital Private Limited\Desktop\twitter\config.ini")
 
# Twitter API setup
bearer_token = config['twitter']['bearer_token']
client = tweepy.Client(bearer_token=bearer_token)
# Access the value
connection_string = config['sql']['engine1']
print(connection_string) 
# SQLAlchemy DB connection
engine = create_engine(config['sql']['engine1'])
 
# Query for tweets
query = "Machine learning -is:retweet lang:en"
tweets = client.search_recent_tweets(
    query=query,
    max_results=10,
    tweet_fields=["id","text" ]
)
print(tweets)
# Insert into DB
insert_sql = text("""
    IF NOT EXISTS (SELECT 1 FROM Tweets WHERE id = :id)
    INSERT INTO Tweets (id, tweet_text)
    VALUES (:id, :tweet_text)
""")
 
with engine.connect() as conn:
    for tweet in tweets.data:
        conn.execute(insert_sql, {
                 "id": tweet.id,
                "tweet_text": tweet.text
        })
    conn.commit()
 
print("Tweets inserted successfully.")