#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VTK utilities for CFD post-processing
# Adrien Crovato
# TODO work with GetOutputPort/SetInputConnection instead of GetOutput/SetInputDataObject

try:
    import vtk
except:
    raise Exception('VTK not found. Aborting!\n')

class Reader:
    def __init__(self, ):
        self.reader = None
        self.grid = None

    def open(self, fname, fmt):
        '''Open solution file
        '''
        import os.path
        # Create reader
        if fmt == 'dat':
            self.reader = vtk.vtkTecplotReader()
        elif fmt == 'vtk':
            self.reader = vtk.vtkUnstructuredGridReader()
            self.reader.ReadAllScalarsOn()
            self.reader.ReadAllVectorsOn()
            self.reader.ReadAllTensorsOn()
            self.reader.ReadAllFieldsOn()
        elif fmt == 'vtu':
            self.reader = vtk.vtkXMLUnstructuredGridReader()
        else:
            raise Exception('Reader for format ' + fmt + ' not implemented!\n')
        # Open file
        if not os.path.isfile(fname+'.'+fmt):
            raise Exception('file ' + os.path.realpath(fname + '.' + fmt) + ' not found!\n')
        self.reader.SetFileName(fname+'.'+fmt)
        self.reader.Update()
        #Get grid data
        if fmt == 'dat':
            self.grid = self.reader.GetOutput().GetBlock(0)
        elif fmt == 'vtk' or fmt == 'vtu':
            self.grid = self.reader.GetOutput()

class Cutter:
    def __init__(self, _grid):
        self.grid = _grid
        self.slice = None

    def cut(self, cutO, cutN, tag=None, tag_name=None):
        '''Cut the physical group ided "tag" with a plane defined by point "cutO" and normal "cutN"
        '''
        # create a threshold containing the physical group (numbered "tag", called "tag_name") to cut
        if tag:
            thresh = vtk.vtkThreshold()
            thresh.ThresholdBetween(tag,tag)
            thresh.SetInputDataObject(self.grid) #thresh.SetInputConnection(self.grid)
            thresh.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS, tag_name)
            thresh.Update()
        # create cutting plane
        plane = vtk.vtkPlane()
        plane.SetOrigin(cutO[0], cutO[1], cutO[2])
        plane.SetNormal(cutN[0], cutN[1], cutN[2])
        # cut the threshold or the grid and get data
        cutter = vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        if tag:
            cutter.SetInputDataObject(thresh.GetOutput()) #cutter.SetInputConnection(thresh.GetOutputPort())
        else:
            cutter.SetInputDataObject(self.grid) #cutter.SetInputConnection(self.grid)
        cutter.Update()
        self.slice = cutter.GetOutput()

    def extract(self, tagDim, vname, atPoint = True, sorted = True):
        '''Extract points "pts", connectivity list "elems" and data "vals" named "vname" from cutting plane data self.slice
        The physical group dimension is given by "tagDim" and "atPoint" is True if vname is defined at points.
        '''
        import numpy as np
        # transfer point coordinates
        _pts = self.slice.GetPoints()
        pts = np.zeros((_pts.GetNumberOfPoints(), 3))
        for i in range(0, pts.shape[0]):
            for j in range(0, 3):
                pts[i][j] = _pts.GetPoint(i)[j]
        # transfer connectivity
        if tagDim == 3:
            _elems = self.slice.GetPolys().GetData()
            nV = 3 # assumes that all Poly(gon)s are triangles
        elif tagDim == 2:
            _elems = self.slice.GetLines().GetData()
            nV = 2
        else:
            raise Exception('tagDim can only be 2 or 3 but ' + tagDim + ' was given!\n')
        elems = np.zeros((_elems.GetNumberOfTuples() // (nV+1), nV), dtype=int)
        for i in range(0, elems.shape[0]):
                for j in range(0, nV):
                    elems[i][j] = _elems.GetTuple((nV+1)*i+j+1)[0]
        # transfer variables
        vals = {}
        for name in vname:
            if atPoint: # data at points
                _vals =  self.slice.GetPointData().GetArray(name)
            else: # data at elements
                _vals =  self.slice.GetCellData().GetArray(name)
            vals[name] = np.zeros((_vals.GetNumberOfTuples(), _vals.GetNumberOfComponents()))
            for i in range(0, vals[name].shape[0]):
                for j in range(0, vals[name].shape[1]):
                    vals[name][i][j] = _vals.GetTuple(i)[j]
        # sort the data
        if sorted:
            if not atPoint:
                print('Sorting method not implemented for data defined at cell. Skipping sort!\n')
            else:
               pts, elems, vals = self.__sort(pts, elems, vals)
        return pts, elems, vals
    
    def __sort(self, pts, elems, vals):
        '''Sort data (pts, vals) array against line connectivity list (elems)
        '''
        import numpy as np
        # store pts and vals in matrix
        data = pts
        for val in vals.values(): 
            data = np.hstack((data, val))
        # sort id vector
        elems = elems[elems[:,0].argsort(),:]
        # sort data against elems
        nextId = 0
        for i in range(0, elems.shape[0]):
            pts[i,:] = data[elems[nextId,1],:3]
            col = 3
            for val in vals.values():
                val[i,:] = data[elems[nextId,1],col:col+val.shape[1]]
                col = col + val.shape[1]
            nextId = elems[nextId,1]
        return pts, elems, vals
 