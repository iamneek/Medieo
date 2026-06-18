from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("NEON_CONNECTION_STRING")

engine = create_engine(DB_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
