@echo off
REM 启动后端和前端服务

echo Starting backend on port 8007...
cd /d D:\CODE\aitext
start /B python -m uvicorn interfaces.main:app --host 127.0.0.1 --port 8007 --reload > backend.log 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8007 ^| findstr LISTENING') do (
    echo %%a > backend.pid
    echo Backend started with PID: %%a
    goto :frontend
)

:frontend
echo Starting frontend on port 3000...
cd /d D:\CODE\aitext\web-app
start /B npm run dev -- --port 3000 > ..\frontend.log 2>&1
timeout /t 2 /nobreak > nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo %%a > ..\frontend.pid
    echo Frontend started with PID: %%a
    goto :done
)

:done
echo.
echo Services started:
echo   Backend:  http://localhost:8007
echo   Frontend: http://localhost:3000
echo.
echo Use stop.bat to stop services
