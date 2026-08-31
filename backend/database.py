from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
print("Database.py started")
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
with engine.connect() as connection:
    print("MySQL Database Connected Successfully!")