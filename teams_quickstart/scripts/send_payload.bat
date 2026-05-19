@echo off
if "%~1"=="" (
  echo Usage: send_payload.bat path\to\payload.json
  exit /b 1
)
curl -X POST http://127.0.0.1:8765/apply-plan -H "Content-Type: application/json" -d @%1
