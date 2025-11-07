# EudiaHackathon - Windows Startup Scripts

## Quick Start
Double-click `start-all-services.bat` to launch all three services simultaneously in separate terminal windows.

## Individual Scripts
- `start-frontend.bat` - Runs React frontend with `npx pnpm dev` (usually port 5173)
- `start-fastapi.bat` - Runs FastAPI server with `uvicorn server:app --reload` (port 8000)
- `start-backend.bat` - Runs Node.js backend with `npx nodemon index.js` (usually port 3000)

## Master Script
- `start-all-services.bat` - Launches all three services in separate command windows

## Usage
1. Ensure you have the required dependencies installed:
   - Node.js and npm/pnpm for frontend and backend
   - Python and required packages for FastAPI
2. Run `start-all-services.bat` from the project root
3. Each service will open in its own terminal window
4. Access your services:
   - Frontend: http://localhost:5173
   - FastAPI: http://localhost:8000
   - Backend: http://localhost:3000

## Notes
- Each terminal stays open so you can see logs and errors
- Press Ctrl+C in any terminal to stop that specific service
- Close terminal windows to stop services
- The launcher window can be closed after starting - services continue running