import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------------- DATABASE SETUP ---------------- #

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///news.db")

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# ---------------- SENTIMENT ANALYZER ---------------- #

analyzer = SentimentIntensityAnalyzer()

# ---------------- ARTICLE MODEL ---------------- #

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    source = Column(String)
    author = Column(String)
    title = Column(String)
    description = Column(Text)
    url = Column(String, unique=True)
    published_at = Column(DateTime)
    content = Column(Text)
    sentiment = Column(String, default="neutral")
    sentiment_compound = Column(Float, default=0.0)
    topic = Column(String, default="general")

# Create tables if not exist
Base.metadata.create_all(engine)

# ---------------- SENTIMENT FUNCTION ---------------- #

def compute_sentiment(text):
    if not text:
        return "neutral", 0.0

    scores = analyzer.polarity_scores(text)
    compound = scores.get("compound", 0.0)

    if compound >= 0.05:
        return "Positive", compound
    elif compound <= -0.05:
        return "Negative", compound
    else:
        return "Neutral", compound

# ---------------- SAVE ARTICLES ---------------- #

def save_articles(articles_list):
    for art in articles_list:

        # Skip if URL missing
        if not art.get("url"):
            continue

        # Check duplicate
        existing = session.query(Article).filter_by(url=art.get("url")).first()
        if existing:
            continue

        # Handle NewsAPI source (can be dict)
        source_data = art.get("source")
        if isinstance(source_data, dict):
            source_name = source_data.get("name")
        else:
            source_name = source_data

        # Compute sentiment
        text_for_sentiment = art.get("content") or art.get("description") or ""
        sentiment, compound = compute_sentiment(text_for_sentiment)

        # Handle topic safely
        topic = art.get("topic") or "general"

        # Handle published date safely
        published_at = None
        published_raw = art.get("publishedAt")

        if published_raw:
            try:
                published_at = datetime.fromisoformat(
                    published_raw.replace("Z", "+00:00")
                )
            except Exception:
                published_at = None

        article_obj = Article(
            source=source_name,
            author=art.get("author"),
            title=art.get("title"),
            description=art.get("description"),
            url=art.get("url"),
            published_at=published_at,
            content=art.get("content"),
            sentiment=sentiment,
            sentiment_compound=compound,
            topic=topic
        )

        session.add(article_obj)

    session.commit()

# ---------------- FETCH ARTICLES ---------------- #

def get_articles(limit=None):
    query = session.query(Article).order_by(
        Article.published_at.desc().nullslast()
    )

    if limit:
        query = query.limit(limit)

    return query.all()