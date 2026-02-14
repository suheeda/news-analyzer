import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sqlalchemy.orm import sessionmaker
from etl_store import engine, Article, init_db

# Make sure NLTK VADER is available
nltk.download("vader_lexicon")

Session = sessionmaker(bind=engine, future=True)

def compute_sentiment():
    """Compute sentiment for all articles and store results in DB."""
    init_db()
    session = Session()

    sia = SentimentIntensityAnalyzer()
    articles = session.query(Article).all()

    updated = 0
    for art in articles:
        text = " ".join(
            [str(x) for x in [art.title, art.description, art.content] if x]
        )
        if not text.strip():
            continue

        # Compute sentiment
        scores = sia.polarity_scores(text)
        art.sentiment_compound = scores["compound"]
        updated += 1

    session.commit()
    session.close()
    print(f"✅ Sentiment updated for {updated} articles.")

if __name__ == "__main__":
    compute_sentiment()
