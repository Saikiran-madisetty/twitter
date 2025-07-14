import configparser
from sqlalchemy import create_engine

# Read config
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

# Get connection string
connection_string = config['sql']['engine1']
print("Connecting with:", connection_string)

# Connect using SQLAlchemy
engine = create_engine(connection_string)
connection = engine.connect()
print("✅ Connected to database!")
