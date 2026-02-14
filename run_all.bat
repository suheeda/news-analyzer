@echo off
echo Starting News Analyzer...

:: 1. Update DB + ETL
python update_db.py

:: 2. Launch Streamlit dashboard
streamlit run dashboard.py
pause
