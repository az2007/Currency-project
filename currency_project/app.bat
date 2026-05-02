@echo off
REM
cd /d "%~dp0"

REM
start "" cmd /c "streamlit run streamlit_app.py ^& pause"