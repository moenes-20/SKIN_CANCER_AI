@echo off
title Skin Cancer AI - Launcher
color 0B
cls

echo.
echo  ============================================
echo       SKIN CANCER AI - Launching...
echo  ============================================
echo.

set BASE=%~dp0
set PYTHON="%BASE%.venv\Scripts\python.exe"

:: Start Flask app (port 5000)
echo  [1/2] Starting Flask App on http://127.0.0.1:5000 ...
start "Skin Cancer AI - Flask" cmd /k "cd /d "%BASE%" && %PYTHON% app.py"

:: Wait 3 seconds for Flask to boot
timeout /t 3 /nobreak >nul

:: Start Presentation site (port 8080)
echo  [2/2] Starting Presentation Site on http://localhost:8080 ...
start "Skin Cancer AI - Presentation" cmd /k "cd /d "%BASE%presentation" && %PYTHON% -m http.server 8080"

:: Wait 2 more seconds then open browser
timeout /t 2 /nobreak >nul

echo.
echo  ============================================
echo   Ouverture du site de presentation...
echo  ============================================
echo.

:: Open the presentation site in the default browser
start "" "http://localhost:8080"

echo  Les deux serveurs sont demarres !
echo.
echo  - Site de presentation : http://localhost:8080
*   - Application Flask    : http://127.0.0.1:5000
echo.
echo  Appuyez sur une touche pour fermer cette fenetre.
echo  (Les serveurs continuent de tourner dans leurs fenetres)
pause >nul
