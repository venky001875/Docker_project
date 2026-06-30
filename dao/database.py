import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Dynamically find the absolute path of the 'dao' folder where this database.py file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "tasks.db")

# 2. Check if a DATABASE_URL is provided by the environment (.env file / Docker)
# If it's not provided, fall back to the absolute local path to prevent file separation issues
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DEFAULT_DB_PATH}"
)

# For troubleshooting: This prints exactly where your engine is pointing
print(f"📁 Connecting to SQLite database at: {DATABASE_URL}")

# 3. Initialize the SQLAlchemy database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()