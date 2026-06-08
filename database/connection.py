from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from sqlalchemy import create_engine
# we don't need the api key here because we only trying to communicate with the BD


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# if we were using mysql or oracle the difference would be in the postgresql it would be mysql, oracle 

engine = create_engine(DATABASE_URL)
# using the create_engine fuction from sqlalchemy we can easly create the engine 