import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Dynamically find the absolute path of the 'dao' folder where this database.py file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Force the SQLite database file to always be created/read inside that exact 'dao' folder
DB_PATH = os.path.join(BASE_DIR, "tasks.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# For troubleshooting: This will print exactly where your database is being read from
print(f"📁 Connecting to SQLite database at: {DB_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()