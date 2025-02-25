from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv(override=True)

DATABASE = os.getenv("DB_DATABASE")
PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
USERNAME = os.getenv("DB_USERNAME")

url = URL.create(
    drivername="postgresql",
    username=USERNAME,
    host=DB_HOST,
    database=DATABASE,
    password=PASSWORD
)
engine = create_engine(url)

# Create engine
engine = create_engine(url)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
