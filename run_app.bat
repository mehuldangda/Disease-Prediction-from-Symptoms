@echo off
TITLE DiagnoWise AI - Disease Prediction System Launcher
echo ===================================================================
echo               DiagnoWise AI - Disease Prediction System
echo               B.Tech Final Year Project Execution Launcher
echo ===================================================================
echo.

echo [1/3] Installing/verifying Python dependencies...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Python requirements. Ensure Python is installed and added to PATH.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Checking Trained Model Binaries...
python -c "import os; exit(0 if os.path.exists('./saved_model/random_forest.joblib') else 1)"
if %ERRORLEVEL% NEQ 0 (
    echo Model binaries missing. Training ML classifiers...
    python -m ml.train
)

echo.
echo [3/3] Launching FastAPI Backend & Interactive Web Application...
echo.
echo ===================================================================
echo  Server running at:  http://localhost:8000
echo  Swagger API Docs:  http://localhost:8000/docs
echo ===================================================================
echo.
python main.py

pause
