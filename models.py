from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Float

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    source = Column(String(255))
    url = Column(String(500), unique=True)
    published_at = Column(DateTime)
    content = Column(Text)
    sentiment = Column(String(50))
    sentiment_compound = Column(Float)
    topic = Column(String(255))  # <-- new column for topic
