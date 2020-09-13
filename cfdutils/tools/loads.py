#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Aerodynamic loads
# Adrien Crovato
# TODO check Cd sign, might be inverted

class Loads:
    def __init__(self):
        self.ys = [] # spanwise stations
        self.chds = [] # chord
        self.data = {} # coordinates and pressure coefficient
        self.cls = [] # lift
        self.cms = [] # moment positive nose-up (clockwise)
        self.cds = [] # pressure drag
    
    def add(self, y, pts, cp):
        '''Add data for a section along the span
        '''
        import numpy as np
        self.ys.append(y)
        c = max(pts[:,0]) - min(pts[:,0])
        self.chds.append(c)
        x_c = np.zeros(((pts.shape[0], 1)))
        x_c[:,0] = (pts[:,0] - min(pts[:,0])) / c
        self.data[len(self.ys)-1] = np.hstack((pts, x_c, cp))

    def compute(self, alpha = 0):
        '''Compute the sectional aerodynamic load coefficients
        '''
        import numpy as np
        for j in range(0, len(self.ys)):
            x = self.data[j][:,0]
            z = self.data[j][:,2]
            cp = self.data[j][:,4]
            c = self.chds[j] # chord
            c_4 = np.min(x) + 0.25*c # quarter-chord position
            # integrate pressure coefficient
            i = 0
            cz = 0
            cx = 0
            cm = 0 
            while i < (x.shape[0]-1):
                dx = (x[i+1] - x[i]) / c
                dz = -(z[i+1] - z[i]) / c
                cz += 0.5 * dx * (cp[i+1] + cp[i])
                cx += 0.5 * dz * (cp[i+1] + cp[i])
                cm -= -0.5*(cp[i+1]*(x[i+1]-c_4) + cp[i]*(x[i]-c_4)) * dx/c + 0.5*(cp[i+1]*z[i+1] + cp[i]*z[i]) * dz/c # positive nose-up (clockwise)
                i = i+1
            # rotate to flow direction
            cl = cz*np.cos(alpha) - cx*np.sin(alpha)
            cd = cz*np.sin(alpha) + cx*np.cos(alpha)
            self.cls.append(cl)
            self.cms.append(cm)
            self.cds.append(cd)
        
    def display(self):
        '''Display the results
        '''
        print('y = ', self.ys)
        print('Cl = ', self.cls)
        print('Cm = ', self.cms)
        print('Cd = ', self.cds)
    
    def write(self):
        '''Write to disk
        '''
        import numpy as np
        # pressure
        for j in range(0, len(self.ys)):
            print('writing pressure data file in workspace directory: slice_' + str(j) + '.dat...')
            np.savetxt('slice_'+str(j)+'.dat', self.data[j], fmt='%1.5e', delimiter=',', header='x, y, z, x/c, Cp @ y='+str(self.ys[j]), comments='')
        # loads
        loads = np.transpose(np.vstack((self.ys, self.cls, self.cms, self.cds)))
        print('writing loads data file in workspace directory: loads.dat...')
        np.savetxt('loads.dat', loads, fmt='%1.5e', delimiter=',', header='y, Cl, Cm, Cd', comments='')
