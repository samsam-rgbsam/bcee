@echo off
setlocal EnableExtensions
cd /d "%~dp0"
where py >nul 2>nul || (
  echo ERROR: Windows Python launcher not found.
  exit /b 1
)
for /f "tokens=*" %%V in ('py -3.14 -c "import platform; print(platform.python_version())" 2^>nul') do set PYVER=%%V
if not defined PYVER (
  echo ERROR: CPython 3.14 is not available through the Windows Python launcher.
  exit /b 1
)
if not "%PYVER%"=="3.14.6" (
  echo ERROR: Expected Python 3.14.6 but found %PYVER%.
  exit /b 1
)
py -3.14 tools\validate_gate0.py
exit /b %ERRORLEVEL%
