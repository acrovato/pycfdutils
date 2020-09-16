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
- matplotlib package (optional)

## Usage
Create a Python script calling the different utilities that you need in your working directory. Examples are given under the directory [examples](cfdutils/examples/). Run the computation by calling `run.py path/to/your_script.py`. Output files will be saved in your current working directory under a `workspace` directory.

**Known bugs**  
- The sign of the sectional aerodynamic drag coefficient might be inverted

## Documentation
The different utilities are loacated under the directory [tools](cfdutils/tools/). Three classes are currently implemented.

**vtku.Reader**  
- `reader`: return the vtk reader used to open and read the data
- `grid`: return the (unstructured grid) data
- `open(fname, fmt)`: read the file `fname.fmt`

**vtku.Cutter**  
- `grid`: return the (unstructured grid) data
- `slice`: return the data contained in the slice
- `cut(self, cutO, cutN, tag=None, tag_name=None)`: perform a slice using the plane defined by the point `cutO` and the normal `cutN`. If a tag number `tag` and name `tag_name` are provided, the slice is performed on the group defined by those parameters, otherwise the slice is performed on the grid directly
- `pts, elems, vals = extract(self, tagDim, vname, atPoint = True, sorted = True)`: returns the coordinates of the points (`pts`), the list of connectivity (`elems`) and the data (`vals`) named `vname` contained in the current `slice` of dimension `tagDim`. `atPoint` inidcates that the data are defined at the points (as opposed to: defined at the cells center). In the former case, `sorted` can be used to sort the data against the list of connectivity.

**loads.Loads**  
- `ys`: return the y-coordinate of the stations
- `chds`: return the chord of the stations
- `data`: return the x, y and z-coordinates and the chordwise sectional pressure coefficient of the stations
- `cls`: return the sectional lift coefficient of the stations
- `cms`: return the sectional moment coefficient of the stations
- `cds`: return the sectional drag coefficient of the stations
- `add(y, pts, cp)`: add slice data consisting of chordwise x, y and z-coordinates (pts) and pressure coefficient (cp) defined at y-coordinate `y`
- `compute(alpha = 0)`: compute sectional aerodynamic load coefficients at angle of attack `alpha` degrees
- `display()`: print the loads on output
- `plot()`: plot the loads
- `write()`: save the loads to disk
