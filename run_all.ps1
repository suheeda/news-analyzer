Write-Host "Starting News Analyzer..." -ForegroundColor Cyan

# 1. Ensure 'topic' column exists
Write-Host "Checking database schema..." -ForegroundColor Yellow
python check_topic_column.py

# 2. Run ETL to fetch & store new articles
Write-Host "Running ETL to fetch new articles..." -ForegroundColor Yellow
python fetch_articles.py

# 3. Launch Streamlit dashboard
Write-Host "Launching Streamlit Dashboard..." -ForegroundColor Green
streamlit run dashboard.py
