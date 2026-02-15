import os
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("")

analyzer = SentimentIntensityAnalyzer("7a96a14ea46d46e481849d3024d03d7f")

def get_news_articles(query="technology", page_size=100):
    """
    Fetch news articles from NewsAPI and return structured list
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found in environment variables")

    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    try:
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page_size=page_size
        )
    except Exception as e:
        print("NewsAPI Error:", e)
        return []

    articles = response.get("articles", [])

    processed_articles = []

    for article in articles:
        title = article.get("title") or ""
        description = article.get("description") or ""
        source = article.get("source", {}).get("name", "Unknown")
        published_at = article.get("publishedAt")

        text = f"{title} {description}"

        # Sentiment analysis
        sentiment_score = analyzer.polarity_scores(text)["compound"]

        if sentiment_score >= 0.05:
            sentiment = "Positive"
        elif sentiment_score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        processed_articles.append({
            "title": title,
            "description": description,
            "source": source,
            "published_at": published_at,
            "sentiment": sentiment,
            "topic": query
        })

    return processed_articles