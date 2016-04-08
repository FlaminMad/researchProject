# Masters Research Project
Level Control Research Project Repo

## Contents:
* Modbus Data Logging Tool
* PID Controller
* Minimum Variance Controller
* System Parameter Identification Tool (RLS)
* Logged Lab Data

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
This script collects all dependancies required to run the programs within and
installs them automatically. The installation then runs a test suite to verfify
the installation

#### Ubuntu:
An installation script is provided for users of apt-get and can be used by
running the following:
```
chmod +x installDistUbuntu.sh
```
```
sudo ./installDistUbuntu.sh
```
This script collects all dependancies required to run the programs within and
installs them automatically. The installation then runs a test suite to verfify
the installation

### Windows:
The python distribution anaconda is the recommeded base for this project and
can be installed in the following way:
1. Download and install Anaconda with python 2.7 from [here](https://www.continuum.io/downloads)
   following the instructions givien by the vendor
2. Open the installed anaconda terminal and run:
```
conda install pip, numpy, pyyaml, matplotlib, pyserial
```
Followed by:
```
pip install -i http://pypi.anaconda.org/pypi/simple pymodbus
```
3. Verify all packages are installed correctly by running:
```
cd /location/of/researchProject
python2 ./tests/TESTINSTALL.py
```