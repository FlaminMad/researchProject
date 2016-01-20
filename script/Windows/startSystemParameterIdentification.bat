@ECHO OFF
REM Author: Alexander David Leech
REM Date:   19/1/2016
REM Desc:   Script to start the PID Controller program

cd ../../src/systemParameterIdentification
echo Enter selection number:
echo (1) Pre Sourced Data Tool
echo (2) Live Identification Tool
SET /P SELECTION=""

IF %SELECTION%==1 (
    echo Running identification on presourced data
    python preSourcedDataID.py
    GOTO safeExit
)

IF %SELECTION%==2 (
    echo Running identification on live system
    echo Simulation Mode? [Y/N]
    SET /P SIM=""
)
    
    IF %SIM%==Y (
        python liveSystemParamID.py 1
        GOTO safeExit
    )

    IF %SIM%==N (
        python liveSystemParamID.py 0
        GOTO safeExit
    )
    
    echo Invalid Input
    GOTO safeExit


echo Invalid Input

:safeExit
    cd ../../script/windows
    SET /P quit="Press any key to exit..."
    exit 1