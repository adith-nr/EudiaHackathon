@echo off
echo Starting Frontend (React with PNPM)...
cd /d "%~dp0\frontend"
npx pnpm dev
pause