from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///messages.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    email = Column(String(100))
    message = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)

def create_db():
    Base.metadata.create_all(bind=engine)
