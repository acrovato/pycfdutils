# pycfdutils
Python CFD post-processing utilities  
Adrien Crovato, 2020

MATLAB utilities available [here](https://github.com/acrovato/mcfdutils).

## Features
pycfdutils can be used to:
- create sectional pressure data from field or surface solution files in Tecplot ASCII, VTK ASCII or VTK binary format
- compute the sectional aerodynamic loads
- save the pressure data and the loads to disk

## Requirements
pycfdutils needs
- python 3 interpreter and libraries
- numpy and vtk packages

## Usage
Create a Python script calling the different utilities that you need in your working directory. Examples are given under the directory [examples](examples/). Run the computation by calling `run.py path/to/your_script.py`. Output files will be saved in your current working directory under a `workspace` directory.

**Known bugs**  
- The sign of the sectional aerodynamic drag coefficient might be inverted
