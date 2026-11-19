# pyCFDutils
Python CFD post-processing utilities  
Adrien Crovato, 2020

MATLAB utilities available [here](https://github.com/acrovato/mcfdutils).

## Features
pycfdutils can be used to:
- create sectional pressure data from field or surface solution files in Tecplot ASCII, VTK ASCII or VTK binary format
- compute the sectional aerodynamic loads
- save the pressure, friction and the loads to disk

## Requirements
pycfdutils needs
- Python 3 interpreter and libraries
- numpy and vtk packages
- matplotlib package (optional)

## Install and run
You can install pyCFDutils using
```python
python3 -m pip install . [--user]
```
If you want pyCFDutils to create a workspace directory automatically, run a case using
```python
pycfdutils-run path/to/case.py
```
Otherwise, you can simply run
```python
python3 path/to/case.py
```

## Documentation
The documentation is written in the classes/methods signature. The main features are listed here for convenience.

### vtk_utils.Reader
- `open(fname)`: read the file `fname`.

### vtk_utils.Cutter
- `cut(cut_orig, cut_norm, tag_name=None, tag_lid=None, tag_uid=None, to_points=True)`: create a cutplane defined by the point `cut_orig` and the normal `cut_norm`. If `tag_name`, `tag_lid` and `tag_uid` are provided, the slice is performed on the group obtained by thresholding the grid using the variable `tag_name` between the values `tag_lid` and `tag_uid`. Otherwise the slice is performed on the grid directly. If `to_points=True`, the data will be interpolated from the cell centers to the grid vertices.
- `pts, elems, vals = extract(var_names, tag_dim, sort=True)`: returns the coordinates of the points (`pts`), the list of connectivity (`elems`) and the data (`vals`) named `var_names` contained in the current cutplane of dimension `tag_dim`. If `sort=True`, the data will be sorted against the list of connectivity.

### cross_sections.CrossSections 
- `__init__(name='', aoa=0.)`: create a cross section object named `name` at an angle of attack `aoa` degrees.
- `add_section(y, xz, cp, cf=None)`: add data from a cutplane defined at y-coordinate `y` consisting of x and z-coordinates `xz`, pressure coefficient `cp` and friction coefficient `cf`.
- `compute_loads()`: compute sectional aerodynamic load coefficients.
- `display()`: print the loads on console.
- `plot()`: plot the pressure, friction and loads.
- `write()`: save the sectional data and the loads to disk.
