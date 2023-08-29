@echo off
python --version 3>NUL
if errorlevel 1 goto errorNoPython
python main.py

goto :EOF

:errorNoPython
echo.
echo Error^: Python is not installed, make sure to install python 3.>
