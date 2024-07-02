# pyCFDutils
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
- Python 3 interpreter and libraries
- numpy and vtk packages
- matplotlib package (optional)

## Install and run
If you only want to use pyCFDutils, you can install it using
```python
python3 -m pip install . [--user]
```
and then run a case using
```python
python3 path/to/case.py
```

If you need to develop in pyCFDutils before using it, and you can directly run your case from the repo folder using
```python
python3 run.py path/to/case.py
```

## Documentation
The documentation is written in the classes/methods signature. The main features are listed here for convenience.

### vtk_utils.Reader
- `open(fname)`: read the file `fname`

### vtk_utils.Cutter
- `cut(cut_orig, cut_norm, tag_name=None, tag_id=None)`: create a cutplane defined by the point `cut_orig` and the normal `cut_norm`. If a tag name `tag_name` and number `tag_id` are provided, the slice is performed on the group defined by those parameters, otherwise the slice is performed on the grid directly.
- `pts, elems, vals = extract(var_names, tag_dim, at_point=True, sort=True)`: returns the coordinates of the points (`pts`), the list of connectivity (`elems`) and the data (`vals`) named `var_names` contained in the current cutplane of dimension `tag_dim`. `atPoint` inidcates that the data are defined at the points (as opposed to: defined at the cells center). In the former case, `sort` can be used to sort the data against the list of connectivity.

### cross_sections.CrossSections 
- `add_section(y, xz, cp)`: add data from a cutplane defined at y-coordinate `y` consisting of x and z-coordinates (`xz`) and pressure coefficient (`cp`).
- `compute_loads(aoa=0)`: compute sectional aerodynamic load coefficients at angle of attack `aoa` degrees.
- `display()`: print the loads on console.
- `plot()`: plot the loads.
- `write()`: save the loads to disk.
