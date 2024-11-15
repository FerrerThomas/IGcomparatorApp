@echo off
where python >nul 2>nul
if errorlevel 1 (
    echo Python no está instalado. Descárgalo desde https://www.python.org/downloads/
    pause
    exit
)

@echo off
cd "%~dp0data"
start "" pythonw app_instagram.py
exit

