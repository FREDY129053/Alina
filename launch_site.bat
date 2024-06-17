@echo off

cd /d C:\Users\User\Desktop\Alina\web_app\backend
call venv\Scripts\activate
start /b "" uvicorn main:app --reload

cd /d C:\Users\User\Desktop\Alina\web_app\frontend
start /b "" npm run dev

timeout /t 5 > null
start http://localhost:5173/game_info