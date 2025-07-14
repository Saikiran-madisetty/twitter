import configparser
from sqlalchemy import create_engine, text
import tweepy
 
# Load config with interpolation disabled
config = configparser.ConfigParser(interpolation=None)
config.read(r"C:\Users\Saikiran\OneDrive - Kasmo Digital Private Limited\Desktop\twitter\config.ini")
 
# Twitter API setup
bearer_token = config['twitter']['bearer_token']
client = tweepy.Client(bearer_token=bearer_token)
 
# SQLAlchemy engine setup for SQL Server
engine = create_engine(config['sql']['engine1'])
 
# Get user ID based on username
username = "Sundar pichai"
user = client.get_user(username=username)
user_id = user.data.id
 
# Fetch last tweet ID from your DB
with engine.connect() as conn:
    result = conn.execute(text("SELECT MAX(id) FROM Tweets"))
    last_id = result.scalar() or 0  
 
# Fetch recent tweets from Twitter
tweets = client.get_users_tweets(
    id=user_id,
    max_results=5,
    tweet_fields=["id","text"]
)
 
# SQL insert statement aligned with your schema
insert_sql = text("""
    IF NOT EXISTS (SELECT 1 FROM Tweets WHERE id = :id)
    INSERT INTO Tweets (id, tweet_text)
    VALUES (:id, :tweet_text)
""")
 
# Insert tweets into the DB
if tweets.data:
    with engine.connect() as conn:
        for tweet in tweets.data:
            conn.execute(insert_sql, {
                "id": tweet.id,
                "tweet_text": tweet.text
            })
        conn.commit()
    print("Tweets updated successfully.")
else:
    print("No new tweets found.")