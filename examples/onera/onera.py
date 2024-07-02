#!/usr/bin/env python3
# -*- coding: utf8 -*-
# test encoding: à-é-è-ô-ï-€

# pyCFDutils
# Copyright 2020 Adrien Crovato
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Onera M6 wing

def get_config():
    """Inputs definition
    """
    return {
        'File': 'surface_flow.dat', # file containing the flow solution
        'Cuts': [0.01, 0.24, 0.53, 0.78, 0.96, 1.08, 1.14, 1.18], # y-coordinates of the slices
        'Tag': [None, None], # tag number and name if the solution is provided not only on the wing surface
        'Variable': 'Pressure_Coefficient', # name of variable to extract
        'AoA': 3.06 # angle of attack (degrees)
    }

def compute_loads(cfg):
    """Extract several slices along the wing span and compute the sectional aerodynamic load coefficients
    """
    from pycfdutils.vtk_utils import Reader, Cutter
    from pycfdutils.cross_sections import CrossSections
    # Define reader
    reader = Reader()
    reader.open(cfg['File'])
    # Create slices
    cutter = Cutter(reader.grid)
    loads = CrossSections()
    for i in range(len(cfg['Cuts'])):
        cutter.cut([0., cfg['Cuts'][i], 0.], [0., 1., 0.], cfg['Tag'][0], cfg['Tag'][1])
        pts, elems, vals = cutter.extract([cfg['Variable']], 2)
        loads.add_section(cfg['Cuts'][i], pts[:, [0, 2]], vals[cfg['Variable']])
    # Compute loads
    loads.compute_loads(cfg['AoA'])
    loads.display()
    loads.plot()
    loads.write()

def mkchdir_exec(dirname, fname, cfg):
    """Create a directory if it does not exist, change to it and execute
    """
    import os
    dir = os.path.join(os.getcwd(), dirname)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    os.chdir(dir)
    cfg['File'] = os.path.join(os.path.split(__file__)[0], fname) # to get relative path to this file
    compute_loads(cfg)
    os.chdir('..')

def main():
    # Get inputs
    cfg = get_config()
    # Compute loads for several file formats...
    # Tecplot ASCII, computed using SU2 (https://github.com/su2code/SU2/releases/tag/v7.0.6)
    print('--- SU2 - surface - Tecplot ASCII ---')
    mkchdir_exec('Tecplot_ASCII', 'surface_flow.dat', cfg)
    # VTK ASCII, computed using SU2
    print('--- SU2 - surface - VTK ASCII ---')
    mkchdir_exec('VTK_ASCII', 'surface_flow.vtk', cfg)
    # VTK binary, computed using SU2
    print('--- SU2 - surface - VTK binary ---')
    mkchdir_exec('VTK_bin', 'surface_flow.vtu', cfg)
    # VTK binary, computed using DART v1.2.0 (https://gitlab.uliege.be/am-dept/dartflo/-/releases)
    print('--- DART - field - VTK binary ---')
    cfg['Tag'] = ['tag', 5]
    cfg['Variable'] = 'Cp'
    mkchdir_exec('VTK_bin2', 'flow.vtu', cfg)

if __name__ == "__main__":
    main()
