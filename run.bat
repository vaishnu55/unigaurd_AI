@echo off
title UniGuard AI Prototype
echo ===================================================
echo UniGuard AI - Hackathon Prototype Setup
echo ===================================================

echo.
echo Checking for Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ===================================================
    echo [!] Python is not installed on this device!
    echo [!] Downloading and installing Python automatically...
    echo ===================================================
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
    echo Installing Python in the background. This may take 1-2 minutes...
    start /wait python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del python_installer.exe
    echo.
    echo ===================================================
    echo [SUCCESS] Python has been installed successfully!
    echo IMPORTANT: You must close this window and double-click 'run.bat' again to continue.
    echo ===================================================
    pause
    exit
)

echo.
echo [1/5] Installing Dependencies...
python -m pip install -r requirements.txt

echo.
echo [2/5] Training Custom AI Model (No pre-existing models!)...
python 1_train_model.py

echo.
echo [3/5] Starting Protected Target Server (Port 5000)...
start "Target Server (Protected Zone)" cmd /k "title Protected Server && python 2_target_server.py"
timeout /t 2 /nobreak >nul

echo.
echo [4/5] Starting AI Monitoring Dashboard (Port 5001)...
start "AI Dashboard (Monitoring Zone)" cmd /k "title AI Monitor && python 3_ai_monitor.py"
timeout /t 2 /nobreak >nul

echo.
echo [5/5] Opening Dashboard in Browser...
start http://localhost:5001

echo.
echo ===================================================
echo SETUP COMPLETE!
echo - The Target Server is running.
echo - The AI Dashboard is open in your browser.
echo - A "one_way_telemetry.csv" file was created to act as the Data Diode.
echo ===================================================
echo.
echo Are you ready to simulate a hacker attack?
pause

echo.
python 4_attacker.py

echo.
echo Done! Check your browser. You should see the Custom AI caught the attack!
pause
