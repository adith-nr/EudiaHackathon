@echo off
echo Starting FastAPI Server...
cd /d "%~dp0\fastapi"
python -m uvicorn server:app --reload
pause