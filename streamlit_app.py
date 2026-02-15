import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from etl_store import get_articles

st.set_page_config(page_title="News Analyzer", layout="wide")
st.title("📰 News Analyzer Dashboard")

articles = get_articles(limit=500)

data = []
for a in articles:
    data.append({
        "Title": a.title,
        "Description": a.description,
        "Source": a.source,
        "Published At": a.published_at,
        "Sentiment": a.sentiment,
        "Topic": a.topic
    })

df = pd.DataFrame(data)

# ✅ SAFETY CHECK
if df.empty:
    st.warning("No articles found in database.")
    st.stop()

if "Published At" in df.columns:
    df["Published At"] = pd.to_datetime(df["Published At"], errors="coerce")

# Sidebar filter
topics = ["All"] + sorted(df["Topic"].dropna().unique().tolist())
selected_topic = st.sidebar.selectbox("Select Topic", topics)

if selected_topic != "All":
    df = df[df["Topic"] == selected_topic]

# Search
search_query = st.text_input("Search Articles by Title")
if search_query:
    df = df[df["Title"].str.contains(search_query, case=False, na=False)]

st.write(f"Showing {len(df)} articles")
st.dataframe(df)

# Pie chart
sentiment_counts = df["Sentiment"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%")
ax1.axis("equal")
st.pyplot(fig1)

# Bar chart
topic_sentiment = df.groupby(["Topic", "Sentiment"]).size().unstack(fill_value=0)
st.bar_chart(topic_sentiment)