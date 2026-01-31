@echo off
cls
:start
TerrariaServer.exe -config serverconfig.txt >> terraria.log 2>&1
@echo.
@echo Restarting server...
@echo.
goto start