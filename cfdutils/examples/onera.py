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
    p['File'] = 'surface_flow' # file containing the flow solution on the surface
    p['Format'] = 'dat' # file format (dat = Tecplot ASCII, vtk = VTK)
    p['Cuts'] = [0.01, 0.24, 0.53, 0.78, 0.96, 1.08, 1.14, 1.18] # y-coordinates of the slices
    import os
    p['File'] = os.path.join(os.path.split(__file__)[0], p['File']) # to get relative path to this file
    return p

def main():
    '''Extract several slices along the wing span and compute the sectional aerodynamic load coefficients
    '''
    import cfdutils.tools.vtku as vu
    import cfdutils.tools.loads as lu
    # Get inputs
    p = inputs()
    # Define reader
    reader = vu.Reader()
    reader.open(p['File'], p['Format'])
    # Create slices
    #cutter = vu.Cutter(reader.reader.GetOutputPort())
    cutter = vu.Cutter(reader.grid)
    loads = lu.Loads()
    for i in range(0, len(p['Cuts'])):
        cutter.cut([0., p['Cuts'][i], 0.], [0., 1., 0.])
        pts, elems, vals = cutter.extract(2, ['Pressure_Coefficient']) # C<sub>p<_sub>
        loads.add(p['Cuts'][i], pts, vals['Pressure_Coefficient'])
    # Compute loads
    loads.compute()
    loads.display()
    loads.write()

if __name__ == "__main__":
    main()