@echo off
title EudiaHackathon - All Services Launcher
echo =============================================
echo   EudiaHackathon Development Environment
echo =============================================
echo.
echo Starting all services in separate windows...
echo.

REM Start Frontend (React with PNPM)
echo [1/3] Starting Frontend...
start "Frontend - React (PNPM)" cmd /k "cd /d "%~dp0\frontend" && echo Starting Frontend on http://localhost:5173... && npx pnpm dev"

REM Wait a moment between starts
timeout /t 2 /nobreak >nul

REM Start FastAPI Server
echo [2/3] Starting FastAPI Server...
start "FastAPI Server" cmd /k "cd /d "%~dp0\fastapi" && echo Starting FastAPI on http://localhost:8000... && python -m uvicorn server:app --reload"

REM Wait a moment between starts
timeout /t 2 /nobreak >nul

REM Start Backend (Node.js)
echo [3/3] Starting Backend...
start "Backend - Node.js" cmd /k "cd /d "%~dp0\backend" && echo Starting Node.js Backend... && npx nodemon index.js"

echo.
echo =============================================
echo All services are starting in separate windows:
echo  - Frontend:  http://localhost:5173
echo  - FastAPI:   http://localhost:8000
echo  - Backend:   http://localhost:3000
echo.
echo Press any key to close this launcher window...
echo (Services will continue running in their own windows)
echo =============================================
pause >nul