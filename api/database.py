from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv(override=True)

DB_DATABASE = os.getenv("DB_DATABASE")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")

url = URL.create(
    drivername="postgresql",
    username=DB_USERNAME,
    host=DB_HOST,
    database=DB_DATABASE,
    password=DB_PASSWORD
)
engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
