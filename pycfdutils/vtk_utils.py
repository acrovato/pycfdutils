# -*- coding: utf-8 -*-

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

try:
    import vtk
except:
    raise RuntimeError('VTK not found!\n')
import numpy as np
import os.path

class Reader:
    """VTK grid reader

    Attributes:
    grid: vtkDataObject
        object containing grid and data
    """
    def __init__(self):
        self.grid = None

    def open(self, fname):
        """Open solution file

        Parameters:
        fname: str
            name of grid file
        """
        # Get format
        fmt = os.path.splitext(fname)[1]
        # Create reader
        if fmt == '.dat':
            reader = vtk.vtkTecplotReader()
        elif fmt == '.vtk':
            reader = vtk.vtkUnstructuredGridReader()
            reader.ReadAllScalarsOn()
            reader.ReadAllVectorsOn()
            reader.ReadAllTensorsOn()
            reader.ReadAllFieldsOn()
        elif fmt == '.vtu':
            reader = vtk.vtkXMLUnstructuredGridReader()
        else:
            raise RuntimeError(f'Reader for format {fmt} not implemented!\n')
        # Open file
        if not os.path.isfile(fname):
            raise RuntimeError(f'File {fname} not found!\n')
        reader.SetFileName(fname)
        reader.Update()
        # Get grid data
        if fmt == '.dat':
            self.grid = reader.GetOutput().GetBlock(0)
        elif fmt == '.vtk' or fmt == '.vtu':
            self.grid = reader.GetOutput()

class Cutter:
    """Manage data extraction from a cutplane

    Parameters:
    grid: vtkDataObject
        object containing grid and data

    Attributes:
    grid: vtkDataObject
        object containing grid and data
    slice: vtkPolyData
        objects containing grid and data in cutplane
    """
    def __init__(self, grid):
        self.grid = grid
        self.slice = None

    def cut(self, cut_orig, cut_norm, tag_name=None, tag_id=None, to_points=True):
        """Create a cutplane on the grid or on a subset of it

        Parameters:
        cut_orig: array
            coordinates of origin of cutplane
        cut_norm: array
            components of vector normal to cutplane
        tag_name: str
            name of variable to create threshold on (default: None)
        tag_id: int
            ID number to threshold (default: None)
        to_points: bool
            whether cell data must be interpolated at points or not (default: True)
        """
        # Create a threshold containing the physical group to cut
        if tag_name:
            thresh = vtk.vtkThreshold()
            thresh.SetLowerThreshold(tag_id)
            thresh.SetUpperThreshold(tag_id)
            thresh.SetInputDataObject(self.grid)
            thresh.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS, tag_name)
            thresh.Update()
        # Create cut plane
        plane = vtk.vtkPlane()
        plane.SetOrigin(cut_orig[0], cut_orig[1], cut_orig[2])
        plane.SetNormal(cut_norm[0], cut_norm[1], cut_norm[2])
        # Cut the threshold or the grid and get data
        cutter = vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        if tag_id:
            cutter.SetInputDataObject(thresh.GetOutput())
        else:
            cutter.SetInputDataObject(self.grid)
        cutter.Update()
        self.slice = cutter.GetOutput()
        # Interpolate data at points
        if to_points and self.slice.GetCellData().GetNumberOfArrays() > 0:
            xfer = vtk.vtkCellDataToPointData()
            xfer.SetInputData(self.slice)
            xfer.Update()
            self.slice = xfer.GetOutput()

    def extract(self, var_names, tag_dim, sort=True):
        """Extract points, connectivity list and data from cutting plane

        Parameters:
        var_names: array
            array of names of data to extract
        tag_dim: int
            dimension of cutted entity
        sort: bool
            whether data must be sorted or not (default: True)
        """
        # Transfer point coordinates
        _pts = self.slice.GetPoints()
        pts = np.zeros((_pts.GetNumberOfPoints(), 3))
        for i in range(0, pts.shape[0]):
            for j in range(0, 3):
                pts[i][j] = _pts.GetPoint(i)[j]
        # Transfer connectivity
        if tag_dim == 3:
            _elems = self.slice.GetPolys().GetData()
            nV = 3 # assumes that all Poly(gon)s are triangles
        elif tag_dim == 2:
            _elems = self.slice.GetLines().GetData()
            nV = 2
        else:
            raise RuntimeError(f'tag_dim can only be 2 or 3 but {tag_dim} was given!\n')
        elems = np.zeros((_elems.GetNumberOfTuples() // (nV + 1), nV), dtype=int)
        for i in range(0, elems.shape[0]):
                for j in range(0, nV):
                    elems[i][j] = _elems.GetTuple((nV + 1) * i + j + 1)[0]
        # Transfer variables
        vals = {}
        for name in var_names:
            _vals = self.slice.GetPointData().GetArray(name)
            vals[name] = np.zeros((_vals.GetNumberOfTuples(), _vals.GetNumberOfComponents()))
            for i in range(0, vals[name].shape[0]):
                for j in range(0, vals[name].shape[1]):
                    vals[name][i,j] = _vals.GetTuple(i)[j]
        # Sort the data
        if sort:
            pts, elems, vals = self.__sort(pts, elems, vals)
        return pts, elems, vals

    def __sort(self, pts, elems, vals):
        """Sort data points and values against line connectivity list

        Parameters:
        pts: ndarray
            points coordinates
        elems: ndarray
            connectivity list
        vals: dict
            name-ndarray dictionnary of values
        """
        # store pts and vals in matrix
        data = pts
        for val in vals.values():
            data = np.hstack((data, val))
        # sort id vector
        elems = elems[elems[:, 0].argsort(), :]
        # sort data against elems
        nextId = 0
        for i in range(0, elems.shape[0]):
            pts[i,:] = data[elems[nextId,1], :3]
            col = 3
            for val in vals.values():
                val[i,:] = data[elems[nextId,1], col:col+val.shape[1]]
                col = col + val.shape[1]
            nextId = elems[nextId, 1]
        return pts, elems, vals
