@echo off
echo Starting FastAPI Backend...
start cmd /k "cd /d "%~dp0" && call venv\Scripts\activate && uvicorn main:app --reload"

echo Starting Streamlit Frontend...
ping 127.0.0.1 -n 4 > nul
start cmd /k "cd /d "%~dp0nucleai" && call ..\venv\Scripts\activate && streamlit run app.py --server.headless true"

echo Launching browser to presentation page...
ping 127.0.0.1 -n 3 > nul
start chrome http://localhost:8501 || start http://localhost:8501

echo Both services started and browser launched!
