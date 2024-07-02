# pyCFDutils
# Copyright (C) 2023 Adrien Crovato
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import re

__version__ = re.findall(
    r"""__version__ = ["']+([0-9\.]*)["']+""",
    open('pycfdutils/__init__.py').read(),
)[0]

setup(
    name='pycfdutils',
    version=__version__,
    description='pyCFDutils is a colelction of post-processing utilities for CFD.',
    keywords='CFD aerodynamic post-processing utilities Python',
    author='Adrien Crovato',
    author_email='',
    url='https://github.com/acrovato/pycfdutils',
    license='Apache License, Version 2.0',
    packages=find_packages(include=['pycfdutils*']),
    install_requires=['numpy>=1.22', 'vtk>=9.2.2'],
    classifiers=['Operating System :: OS Independent', 'Programming Language :: Python'],
)
