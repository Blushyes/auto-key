@echo off

cd %~dp0

@REM 提权
@REM Net session >nul 2>&1 || powershell start-process 1.bat -verb runas

@REM 调用powershell脚本 2.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\2.ps1

exit /b %ERRORLEVEL%