#!/usr/bin/env python3
# -*- coding: utf8 -*-
# test encoding: à-é-è-ô-ï-€

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
# Adrien Crovato

def inputs():
    '''Inputs definition
    '''
    p = {}
    p['File'] = 'surface_flow' # file containing the flow solution
    p['Format'] = 'dat' # file format (dat = Tecplot ASCII, vtk = VTK ASCII, vtu = VTK)
    p['Cuts'] = [0.01, 0.24, 0.53, 0.78, 0.96, 1.08, 1.14, 1.18] # y-coordinates of the slices
    p['Tag'] = [None, None] # tag number and name if the solution is provided not only on the wing surface
    p['Variable'] = 'Pressure_Coefficient' # name of variable to extract
    p['AoA'] = 3.06 # angle of attack (degrees)
    return p
    
def cLoads(p):
    '''Extract several slices along the wing span and compute the sectional aerodynamic load coefficients
    '''
    import cfdutils.tools.vtku as vu
    import cfdutils.tools.loads as lu
    # Define reader
    reader = vu.Reader()
    reader.open(p['File'], p['Format'])
    # Create slices
    cutter = vu.Cutter(reader.grid)
    loads = lu.Loads()
    for i in range(0, len(p['Cuts'])):
        cutter.cut([0., p['Cuts'][i], 0.], [0., 1., 0.], p['Tag'][0], p['Tag'][1])
        pts, elems, vals = cutter.extract(2, [p['Variable']])
        loads.add(p['Cuts'][i], pts, vals[p['Variable']])
    # Compute loads
    loads.compute(p['AoA'])
    loads.display()
    loads.plot()
    loads.write()
    
def mkchdirexec(dirname, p):
    '''Create a directory if it does not exist, change to it and execute
    '''
    import os
    dir = os.path.join(os.getcwd(), dirname)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    os.chdir(dir)
    p['File'] = os.path.join(os.path.split(__file__)[0], p['File']) # to get relative path to this file
    cLoads(p)
    os.chdir('..')

def main():
    # Get inputs
    p = inputs()
    # Compute loads for several file formats...
    # Tecplot ASCII, computed using SU2 (https://github.com/su2code/SU2/releases/tag/v7.0.6)
    print('--- SU2 - surface -Tecplot ASCII ---')
    p['Format'] = 'dat'
    mkchdirexec('Tecplot_ASCII', p)
    # VTK ASCII, computed using SU2
    print('--- SU2 - surface - VTK ASCII ---')
    p['Format'] = 'vtk'
    mkchdirexec('VTK_ASCII', p)
    # VTK binary, computed using SU2
    print('--- SU2 - surface - VTK binary ---')
    p['Format'] = 'vtu'
    mkchdirexec('VTK_bin', p)
    # VTK binary, computed using Flow v1.9.2 (https://gitlab.uliege.be/am-dept/waves/-/releases)
    print('--- Flow - field - VTK binary ---')
    p['File'] = 'flow'
    p['Tag'] = [5, 'tag']
    p['Variable'] = 'Cp'
    mkchdirexec('VTK_bin2', p)

if __name__ == "__main__":
    main()