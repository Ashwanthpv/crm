@echo off
cd /d D:\cuf
echo Running makemigrations...
.venv\Scripts\python.exe manage.py makemigrations
if errorlevel 1 (
    echo makemigrations failed
    exit /b 1
)
echo.
echo Running migrate...
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 (
    echo migrate failed
    exit /b 1
)
echo.
echo Migrations completed successfully!
