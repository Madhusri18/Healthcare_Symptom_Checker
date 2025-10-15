# database.py
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file
DATABASE_URL = "sqlite:///./symptoms.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Database model (table)
class SymptomRecord(Base):
    __tablename__ = "symptom_records"

    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(Text, nullable=False)
    analysis = Column(Text, nullable=False)


# Function to create all tables
def init_db():
    Base.metadata.create_all(bind=engine)
