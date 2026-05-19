@echo off
cd /d %~dp0\..\..\runner_autocad
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
set EDA_AUTOCAD_REAL=1
uvicorn app:app --host 127.0.0.1 --port 8765
