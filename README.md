# Masters Research Project
Level Control Research Project Repo


## Contents:
* Modbus Data Logging Tool
* PID Controller
* Enhanced PID Controller
* System Parameter Identification Tools Including:  
 Batch Least Squares  
 Recursive Least Squares  
 Pseudo Random Binary Sequence
* Minimum Variance Controller  
* Logged Lab Data
* Testing Platform


## Installation:
### Linux:
#### ArchLinux:
An installation script is provided for users of pacman and can be used by
running the following:
```
chmod +x installDistArch.sh
```
```
sudo ./installDistArch.sh
```
This script collects all dependencies required to run the programs within this 
repository and installs them automatically. The installation then runs a test 
suite to verfify the installation

#### Ubuntu:
An installation script is provided for users of apt-get and can be used by
running the following:
```
chmod +x installDistUbuntu.sh
```
```
sudo ./installDistUbuntu.sh
```
This script collects all dependencies required to run the programs within this 
repository and installs them automatically. The installation then runs a test 
suite to verfify the installation

### Windows:
The python distribution anaconda is the recommeded base for this project and
can be installed in the following way:

1. Download and install Anaconda with python 2.7 from [here](https://www.continuum.io/downloads) following the instructions givien by the vendor
2. Open the installed anaconda terminal and run:
```
conda install pip, numpy, pyyaml, matplotlib, pyserial
```
3. Followed by:
```
pip install -i http://pypi.anaconda.org/pypi/simple pymodbus
```
4. Verify all packages are installed correctly by running:
```
cd /location/of/researchProject
python2 ./tests/TESTINSTALL.py
```

## Running:
Scripts are provided to run each program within the .../scripts/OS_TYPE/ directory.
Both simulation mode and live system running versions are avaliable so the user 
does not require to be connected to a live system.

##Documentation
Individual detailed documentation is not yet avaliable however an insight to each 
controller is avaliable within the main research project report.