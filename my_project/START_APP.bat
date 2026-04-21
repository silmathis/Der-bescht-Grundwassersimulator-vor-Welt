@echo off
REM Start the Groundwater Simulator
setlocal
cd /d "%~dp0"

set "VENV_PY=%~dp0.venv\Scripts\python.exe"

if exist "%VENV_PY%" (
	"%VENV_PY%" -m streamlit run app.py
) else (
	echo [WARN] Local virtual environment not found at .venv\Scripts\python.exe
	echo [WARN] Falling back to system Python from PATH.
	python -m streamlit run app.py
)

if errorlevel 1 (
	echo.
	echo [ERROR] Failed to start Streamlit app.
	echo [HINT] Recreate venv and install dependencies:
	echo        py -3.11 -m venv .venv
	echo        .venv\Scripts\python.exe -m pip install -U pip
	echo        .venv\Scripts\python.exe -m pip install -e .
)

pause
endlocal
