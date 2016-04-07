@ECHO OFF
REM Author: Alexander David Leech
REM Date:   06/04/2016
REM Desc:   Script to start the Enahnced PID Controller program

cd ../../src/EnhancedPIDControl
echo Simulation Mode? (Y/N)
SET /P SIM=""

IF %SIM%==Y (
    python PIDControlEnhanced.py 1
    GOTO safeExit
)

IF %SIM%==N (
    python PIDControlEnhanced.py 0
    GOTO safeExit
)

echo Invalid Input

:safeExit
    cd ../../script/windows
    exit 1