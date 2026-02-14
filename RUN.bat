@echo off
REM Quick Start Script for Windows
REM การใช้: วาง YouTube URL เส้นตรง

title Viral Video Generator - Quick Start
color 0A

echo.
echo ============================================================
echo   VIRAL VIDEO GENERATOR - QUICK START
echo ============================================================
echo.

REM ตรวจสอบ Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ไม่พบ - ติดตั้ง Python ก่อน
    pause
    exit /b 1
)

REM รัน quick_start.py
python quick_start.py

pause
