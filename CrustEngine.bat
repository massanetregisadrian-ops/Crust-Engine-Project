@echo off
cd /d "%~dp0"
pythonw crust_engine_launcher.py
if %errorlevel% neq 0 (
    python crust_engine_launcher.py
    pause
)
