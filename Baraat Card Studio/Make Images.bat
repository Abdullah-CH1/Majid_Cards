@echo off
cd /d "%~dp0"
echo Rebuilding the studio page...
python build.py
echo Making all card images (takes a few minutes)...
python render.py
echo.
echo Done. Images are in the Print and WhatsApp folders.
pause
