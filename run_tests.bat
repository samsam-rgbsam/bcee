@echo off
setlocal EnableExtensions
cd /d "%~dp0"
py -3.14 tools\validate_gate0.py
exit /b %ERRORLEVEL%
