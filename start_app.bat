@echo off
echo Starting News Analyzer App...

REM Activate virtual environment
call .venv\Scripts\activate

REM Start FastAPI backend on port 8000
start cmd /k "uvicorn main:app --reload --port 8000"

REM Wait 5 seconds to ensure backend starts
timeout /t 5 >nul

REM Start Streamlit frontend on port 8501
start cmd /k "python -m streamlit run streamlit_app.py"

echo App is running!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:8501
pause
