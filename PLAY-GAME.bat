@echo off
title FightKro - Sansad Showdown
color 0E
cd /d "%~dp0"

echo ========================================================
echo               FIGHTKRO - SANSAD SHOWDOWN
echo             Creator ^& Developer: Dr-MrBot
echo ========================================================
echo.
echo Starting local game server (no XAMPP needed)...
echo.

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python server.py
    goto done
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py server.py
    goto done
)

where node >nul 2>nul
if %ERRORLEVEL% equ 0 (
    node server.js
    goto done
)

echo.
echo [ERROR] Neither Python nor Node.js was found in your PATH!
echo To run FightKro without XAMPP, please install Python from:
echo https://www.python.org/downloads/
echo.
pause

:done

