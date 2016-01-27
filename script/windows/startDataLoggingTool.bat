@ECHO OFF
REM Author: Alexander David Leech
REM Date:   19/1/2016
REM Desc:   Script to start the data logging tool

cd ../../src/dataLoggingTool
echo Simulation Mode? (Y/N)
SET /P SIM=""

IF %SIM%==Y (
    python dataLoggingTool.py 1
    GOTO safeExit
)

IF %SIM%==N (
    python dataLoggingTool.py 0
    GOTO safeExit
)

echo Invalid Input

:safeExit
    cd ../../script/windows
    exit 1