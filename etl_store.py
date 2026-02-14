import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- Database setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///news.db")
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# --- Sentiment analyzer ---
analyzer = SentimentIntensityAnalyzer()

# --- Article model ---
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
    sentiment = Column(String, default="unknown")
    sentiment_compound = Column(Float, default=0.0)
    topic = Column(String, default="general")  # Ensure default topic

# --- Create tables if they don't exist ---
Base.metadata.create_all(engine)

# --- Helper function: compute sentiment ---
def compute_sentiment(text):
    if not text:
        return "unknown", 0.0
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return "positive", compound
    elif compound <= -0.05:
        return "negative", compound
    else:
        return "neutral", compound

# --- Save articles ---
def save_articles(articles_list):
    for art in articles_list:
        # Check if article already exists
        existing = session.query(Article).filter_by(url=art.get("url")).first()
        if existing:
            continue

        # Compute sentiment
        sentiment, compound = compute_sentiment(art.get("content") or art.get("description"))

        # Ensure topic exists
        topic = art.get("topic") or "general"

        published_at = art.get("publishedAt")
        if published_at:
            try:
                published_at = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            except Exception:
                published_at = None

        article_obj = Article(
            source=art.get("source"),
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

# --- Fetch articles ---
def get_articles(limit=None):
    query = session.query(Article).order_by(Article.published_at.desc())
    if limit:
        query = query.limit(limit)
    return query.all()
