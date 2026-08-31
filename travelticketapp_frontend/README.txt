# TravelTicket Frontend

## Files
- index.html
- style.css
- script.js

## Backend
The JavaScript expects FastAPI at:
http://127.0.0.1:8000

## Run
1. Start your FastAPI backend:
   `.\venv\Scripts\python.exe -m uvicorn main:app --reload`
2. Open the frontend using VS Code Live Server, or run:
   `python -m http.server 5500`
   from this frontend folder.
3. Open:
   http://127.0.0.1:5500

## CORS
If the browser console shows a CORS error, add CORSMiddleware to FastAPI:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Restart FastAPI after changing main.py.
