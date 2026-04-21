@echo off
REM Start the Groundwater Simulator
cd /d "%~dp0"
python -m streamlit run app.py
pause
