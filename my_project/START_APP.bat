@echo off
REM Open deployed Groundwater Simulator by default.
REM Use START_APP.bat local to run the app locally.
setlocal
cd /d "%~dp0"

set "PUBLIC_URL=https://der-bescht-grundwassersimulator-vor-welt-cbpva7egfv7ffvhmjiujw.streamlit.app"

if /I "%~1"=="local" goto RUN_LOCAL

echo Opening public Streamlit app:
echo   %PUBLIC_URL%
start "" "%PUBLIC_URL%"
goto END

:RUN_LOCAL
echo Starting local Streamlit app...
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

:END
endlocal
