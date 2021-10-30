from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# using the .env file to fake the environment variable, in production DB_URL will be a proper variable.

load_dotenv()

# connect to database using env variable

# engine managaes the overall connection to the db
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)

# session generates temporary connection for CRUD operations
Session = sessionmaker(bind=engine)

# base helps map the models to sql tables
Base = declarative_base()