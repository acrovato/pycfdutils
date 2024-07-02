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

import numpy as np

class CrossSections:
    """Manage cross-sectional data along the wing span

    Attributes:
    y_sec: array
        y-coordinate of cross-sections
    chords: array
        chord length of cross-sections
    xz_le: array
        x and z-coordinates of cross-sections leading edge
    xz_c: array
        x and z-coordinates of cross-sections normalized by chord
    cp: array
        pressure coefficients along the chord of cross-sections
    cl: array
        spanwise lift distribution
    cm: array
        spanwise moment distribution
    cd: array
        spanwise drag distribution
    """
    def __init__(self):
        # Geometry
        self.y_sec = []
        self.chords = []
        self.xz_le = []
        self.xz_c = []
        # Loads
        self.cp = []
        self.cl = []
        self.cm = []
        self.cd = []

    def add_section(self, y, xz, cp):
        """Add cross-sectional data

        Parameters:
        y: float
            y-coordinate of cross-section
        xz: ndarray
            x and z-coordinates of cross-section
        cp: array
            pressure coefficients along the chord of cross-section
        """
        # Normalize coordinates
        ile = np.argmin(xz[:, 0]) # LE index
        c = max(xz[:, 0]) - min(xz[:, 0]) # chord length
        xzc = np.zeros((xz.shape[0], 2))
        xzc[:,0] = (xz[:,0] - xz[ile,0]) / c
        xzc[:,1] = (xz[:,1] - xz[ile,1]) / c
        # Add data
        self.y_sec.append(y)
        self.chords.append(c)
        self.xz_le.append(xz[ile, :])
        self.xz_c.append(xzc)
        self.cp.append(cp)

    def compute_loads(self, aoa=0):
        """Compute sectional aerodynamic load coefficients

        Parameters:
        aoa: float
            angle of attack in degrees (default: 0.)
        """
        aoa = np.deg2rad(aoa)
        for i in range(len(self.y_sec)):
            xc = self.xz_c[i][:, 0]
            zc = self.xz_c[i][:, 1]
            cp = self.cp[i][:, 0]
            # Integrate pressure coefficient
            cz = 0
            cx = 0
            cm = 0
            for j in range(len(xc) - 1):
                dx = xc[j + 1] - xc[j]
                dz = -(zc[j + 1] - zc[j])
                cz -= 0.5 * dx * (cp[j + 1] + cp[j])
                cx -= 0.5 * dz * (cp[j + 1] + cp[j])
                cm -= -0.5 * (cp[j + 1] * (xc[j + 1] - 0.25) + cp[j] * (xc[j] - 0.25)) * dx + 0.5 * (cp[j + 1] * zc[j + 1] + cp[j] * zc[j]) * dz
            # Rotate to flow direction
            cl = cz * np.cos(aoa) - cx * np.sin(aoa)
            cd = cz * np.sin(aoa) + cx * np.cos(aoa)
            self.cl.append(cl)
            self.cm.append(cm)
            self.cd.append(cd)

    def display(self):
        """Display the results
        """
        print('y = ', self.y_sec)
        print('cl = ', self.cl)
        print('cm = ', self.cm)
        print('cd = ', self.cd)

    def plot(self):
        """Plot the sectional pressure and load coefficients
        """
        import matplotlib.pyplot as plt
        # Pressure
        fig, ax = plt.subplots()
        ax.set_xlabel('$x/c$')
        ax.set_ylabel('$c_p$')
        ax.invert_yaxis()
        for i in range(len(self.y_sec)):
            ax.plot(self.xz_c[i][:, 0], self.cp[i], label = f'y = {self.y_sec[i]}')
        ax.legend()
        plt.draw()
        # Loads
        fig, ax1 = plt.subplots()
        # left axis
        color = 'tab:blue'
        ax1.set_xlabel('$y$')
        ax1.set_ylabel('$c_l$', color=color)
        ax1.plot(self.y_sec, self.cl, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        # right axis
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('$c_m$', color=color)
        ax2.plot(self.y_sec, self.cm, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

    def write(self):
        """Write to disk
        """
        # Pressure
        for i in range(len(self.y_sec)):
            print(f'Writing pressure data file in workspace directory: slice_{i}.dat')
            hdr = f'y = {self.y_sec[i]}, c = {self.chords[i]}, le = {self.xz_le[i]}\n'
            hdr += '{:>9s}, {:>10s}, {:>10s}'.format('x/c', 'z/c', 'cp')
            data = np.hstack((self.xz_c[i], self.cp[i]))
            np.savetxt(f'slice_{i}.dat', data, fmt='%+1.4e', delimiter=',', header=hdr)
        # Loads
        hdr = '{:>9s}, {:>10s}, {:>10s}, {:>10s}'.format('y', 'cl', 'cm', 'cd')
        data = np.transpose(np.vstack((self.y_sec, self.cl, self.cm, self.cd)))
        print('Writing loads data file in workspace directory: loads.dat...')
        np.savetxt('loads.dat', data, fmt='%+1.4e', delimiter=',', header=hdr)
