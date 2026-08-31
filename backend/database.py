from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
print("Database.py started")
DATABASE_URL = "mysql+pymysql://root:gayatri%402416@localhost/travel_ticket_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
with engine.connect() as connection:
    print("MySQL Database Connected Successfully!")