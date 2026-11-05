@echo off
chcp 65001 >nul
cd /d "%~dp0"
where ollama >nul 2>nul
if %errorlevel%==0 (
  ollama list | findstr /b "qwen3" >nul || ollama pull qwen3:8b
) else (
  echo Ollama nerasta - pratimai veiks, bet be paaiskinimu ir pokalbio. Zr. README.
)
where py >nul 2>nul
if %errorlevel%==0 (py server.py) else (python server.py)
pause
