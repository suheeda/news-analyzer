import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from etl_store import get_articles, save_articles
import fetch_articles

st.set_page_config(page_title="News Analyzer", layout="wide")
st.title("📰 News Analyzer Dashboard")

# -----------------------------------
# Fetch articles from DB
# -----------------------------------
articles = get_articles(limit=500)

# -----------------------------------
# If DB empty → auto fetch
# -----------------------------------
if not articles:
    st.warning("No articles found. Fetching latest news...")
    try:
        new_articles = fetch_articles.fetch_live_articles()
        if new_articles:
            save_articles(new_articles)
            articles = get_articles(limit=500)
        else:
            st.error("No articles fetched from NewsAPI.")
            st.stop()
    except Exception as e:
        st.error(f"Error while fetching articles: {e}")
        st.stop()

# If still empty
if not articles:
    st.error("No articles available.")
    st.stop()

# -----------------------------------
# Convert to DataFrame
# -----------------------------------
data = [{
    "Title": a.title,
    "Description": a.description,
    "Source": a.source,
    "Published At": a.published_at,
    "Sentiment": a.sentiment,
    "Topic": a.topic
} for a in articles]

df = pd.DataFrame(data)

if df.empty:
    st.error("Database returned empty dataset.")
    st.stop()

# Safe datetime conversion
if "Published At" in df.columns:
    df["Published At"] = pd.to_datetime(df["Published At"], errors="coerce")

# -----------------------------------
# Sidebar Filter
# -----------------------------------
if "Topic" in df.columns:
    topics = ["All"] + sorted(df["Topic"].dropna().unique().tolist())
else:
    topics = ["All"]

selected_topic = st.sidebar.selectbox("Select Topic", topics)

if selected_topic != "All" and "Topic" in df.columns:
    df = df[df["Topic"] == selected_topic]

# -----------------------------------
# Search
# -----------------------------------
search_query = st.text_input("Search Articles by Title")

if search_query and "Title" in df.columns:
    df = df[df["Title"].str.contains(search_query, case=False, na=False)]

st.write(f"Showing {len(df)} articles")
st.dataframe(df)

# -----------------------------------
# Sentiment Pie Chart
# -----------------------------------
if not df.empty and "Sentiment" in df.columns:
    sentiment_counts = df["Sentiment"].value_counts()

    if not sentiment_counts.empty:
        fig1, ax1 = plt.subplots()
        ax1.pie(
            sentiment_counts,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            startangle=90
        )
        ax1.axis("equal")
        st.pyplot(fig1)

# -----------------------------------
# Topic Sentiment Bar Chart
# -----------------------------------
if not df.empty and "Topic" in df.columns and "Sentiment" in df.columns:
    topic_sentiment = df.groupby(["Topic", "Sentiment"]).size().unstack(fill_value=0)
    st.bar_chart(topic_sentiment)