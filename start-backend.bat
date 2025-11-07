@echo off
echo Starting Backend (Node.js with Nodemon)...
cd /d "%~dp0\backend"
npx nodemon index.js
pause