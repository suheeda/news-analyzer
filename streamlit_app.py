import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from etl_store import get_articles

st.set_page_config(page_title="News Analyzer", layout="wide")
st.title("📰 News Analyzer Dashboard")

# Fetch articles
articles = get_articles(limit=500)
data = [{
    "Title": a.title,
    "Description": a.description,
    "Source": a.source,
    "Published At": a.published_at,
    "Sentiment": a.sentiment,
    "Topic": a.topic
} for a in articles]

df = pd.DataFrame(data)
df['Published At'] = pd.to_datetime(df['Published At'])

# --- Sidebar: Topic filter ---
topics = ["All"] + sorted(df['Topic'].dropna().unique().tolist())
selected_topic = st.sidebar.selectbox("Select Topic", topics)

if selected_topic != "All":
    df = df[df['Topic'] == selected_topic]

# --- Search box ---
search_query = st.text_input("Search Articles by Title")
if search_query:
    df = df[df['Title'].str.contains(search_query, case=False, na=False)]

st.write(f"Showing {len(df)} articles")
st.dataframe(df)

# --- Sentiment pie chart ---
sentiment_counts = df['Sentiment'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=['green','red','gray'])
ax1.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
st.pyplot(fig1)

# --- Sentiment bar chart by topic ---
if not df.empty:
    topic_sentiment = df.groupby(['Topic', 'Sentiment']).size().unstack(fill_value=0)
    st.bar_chart(topic_sentiment)
