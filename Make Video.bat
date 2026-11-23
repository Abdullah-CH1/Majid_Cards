@echo off
rem Double-click to open the HTML -> MP4 menu.
cd /d "%~dp0"
python html2mp4.py %*
echo.
pause
