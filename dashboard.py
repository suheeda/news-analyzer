import streamlit as st
import pandas as pd
import plotly.express as px
from etl_store import get_articles

st.set_page_config(page_title="News Analyzer", layout="wide")
st.title("📰 News Analyzer Dashboard")

# --- Fetch all articles ---
articles = get_articles(limit=500)
if not articles:
    st.warning("No articles found in the database.")
    st.stop()

# --- Convert to DataFrame ---
data = [{
    "title": a.title,
    "description": a.description,
    "source": a.source,
    "published_at": a.published_at,
    "sentiment": a.sentiment if a.sentiment else "unknown",
    "topic": a.topic if a.topic else "general",
    "url": getattr(a, 'url', '#')
} for a in articles]

df = pd.DataFrame(data)
df['published_date'] = pd.to_datetime(df['published_at'], errors='coerce').dt.date

# --- Sidebar filters ---
topics = ["All"] + sorted(df['topic'].dropna().unique().tolist())
selected_topic = st.sidebar.selectbox("Select Topic", topics)

sentiments = ["All"] + sorted(df['sentiment'].dropna().unique().tolist())
selected_sentiment = st.sidebar.selectbox("Filter by Sentiment", sentiments)

search_text = st.sidebar.text_input("Search News")

# --- Date filter with range selection ---
min_date = df['published_date'].min()
max_date = df['published_date'].max()
selected_date = st.sidebar.date_input(
    "Filter by Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# --- Filter dataframe ---
filtered_df = df.copy()
if selected_topic != "All":
    filtered_df = filtered_df[filtered_df['topic'] == selected_topic]
if selected_sentiment != "All":
    filtered_df = filtered_df[filtered_df['sentiment'] == selected_sentiment]
if search_text:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_text, case=False, na=False) |
        filtered_df['description'].str.contains(search_text, case=False, na=False)
    ]
# Filter by date range
if isinstance(selected_date, tuple) and len(selected_date) == 2:
    start_date, end_date = selected_date
    filtered_df = filtered_df[
        (filtered_df['published_date'] >= start_date) &
        (filtered_df['published_date'] <= end_date)
    ]

st.sidebar.markdown(f"**Articles Found:** {len(filtered_df)}")

# --- Sentiment colors ---
sentiment_colors = {
    "positive": "green",
    "neutral": "gray",
    "negative": "red",
    "unknown": "black"
}

# --- Summary Table with scroll-to-topic links ---
st.subheader("📊 Summary: Articles per Topic")
summary_list = []
for topic in filtered_df['topic'].dropna().unique():
    topic_articles = filtered_df[filtered_df['topic'] == topic]
    counts = topic_articles['sentiment'].value_counts()
    dominant_sentiment = counts.idxmax() if not counts.empty else "unknown"
    color = sentiment_colors.get(dominant_sentiment, "black")
    summary_list.append(
        f"- <span style='color:{color}; font-weight:bold'>"
        f"<a href='#{topic.replace(' ', '_')}'>{topic.capitalize()}</a></span> "
        f"({len(topic_articles)} articles, {dominant_sentiment})"
    )
for item in summary_list:
    st.markdown(item, unsafe_allow_html=True)

st.markdown("---")

# --- Charts ---
col1, col2, col3 = st.columns(3)

# Pie Chart
sentiment_counts = filtered_df['sentiment'].value_counts()
fig_pie = px.pie(
    names=sentiment_counts.index,
    values=sentiment_counts.values,
    title="Sentiment Distribution",
    color=sentiment_counts.index,
    color_discrete_map=sentiment_colors
)
col1.plotly_chart(fig_pie, use_container_width=True)

# Bar Chart (fixed)
fig_bar = px.bar(
    x=sentiment_counts.index,
    y=sentiment_counts.values,
    color=sentiment_counts.index,
    color_discrete_map=sentiment_colors,
    title="Sentiment Counts"
)
col2.plotly_chart(fig_bar, use_container_width=True)

# Line Chart
articles_over_time = df.groupby('published_date').size().reset_index(name='count')
fig_line = px.line(
    articles_over_time,
    x='published_date',
    y='count',
    title="Articles Over Time"
)
col3.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.subheader("📝 Articles by Topic")

# --- Articles grouped by topic ---
topics_to_show = filtered_df['topic'].dropna().unique() if selected_topic == "All" else [selected_topic]

for topic in topics_to_show:
    topic_articles = filtered_df[filtered_df['topic'] == topic]
    st.markdown(f"<a name='{topic.replace(' ', '_')}'></a>", unsafe_allow_html=True)

    with st.expander(f"📂 {topic.capitalize()} ({len(topic_articles)} articles)", expanded=True):
        max_articles = min(10, len(topic_articles))
        if len(topic_articles) > 1:
            max_articles = st.slider(
                f"Select number of articles to open for {topic.capitalize()}",
                min_value=1,
                max_value=min(50, len(topic_articles)),
                value=min(10, len(topic_articles))
            )

        # --- Reliable Open Articles Links ---
        st.markdown(f"### Open Top {max_articles} Articles in {topic.capitalize()}")
        for _, row in topic_articles.head(max_articles).iterrows():
            st.markdown(f"- [{row['title']}]({row['url']})", unsafe_allow_html=True)

        # Display articles
        for _, row in topic_articles.iterrows():
            color = sentiment_colors.get(row['sentiment'], "black")
            st.markdown(f"### [{row['title']}]({row['url']})", unsafe_allow_html=True)
            st.markdown(
                f"*Source:* {row['source']}  |  *Sentiment:* "
                f"<span style='color:{color}; font-weight:bold'>{row['sentiment'].capitalize()}</span>",
                unsafe_allow_html=True
            )
            st.markdown(f"{row['description']}")
            st.markdown("---")
