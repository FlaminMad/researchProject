@ECHO OFF
REM Author: Alexander David Leech
REM Date:   27/1/2016
REM Desc:   Script to start the Neural Network Controller

cd ../../src/neuralNetworkControl
echo Simulation Mode? (Y/N)
SET /P SIM=""

IF %SIM%==Y (
    python researchProjectAIControl.py 1
    GOTO safeExit
)

IF %SIM%==N (
    python researchProjectAIControl.py 0
    GOTO safeExit
)

echo Invalid Input

:safeExit
    cd ../../script/windows
    exit 1