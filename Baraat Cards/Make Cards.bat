@echo off
cd /d "%~dp0"
echo Making the Baraat card images...
python make_cards.py
echo.
echo Done. Look in the Print and WhatsApp folders.
pause
