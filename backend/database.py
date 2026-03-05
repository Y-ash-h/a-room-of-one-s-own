import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()

# Vercel Postgres uses POSTGRES_URL or POSTGRES_URL_NON_POOLING
DATABASE_URL = os.getenv("POSTGRES_URL_NON_POOLING", os.getenv("POSTGRES_URL", os.getenv("DATABASE_URL", "sqlite:///./cabinet.db")))

# Neon / Render / Vercel Postgres supply "postgres://" but SQLAlchemy needs "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs check_same_thread=False; PostgreSQL ignores this kwarg
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit from
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
