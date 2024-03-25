@echo off

cd %~dp0

@REM 提权
@REM Net session >nul 2>&1 || powershell start-process 1.bat -verb runas

@REM 调用KeymouseGo
.\KeymouseGo .\scripts\press_win_test.txt --runtimes 1 --speed 200

exit 0