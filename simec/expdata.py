#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Short description of this Python module.
Longer description of this module.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Daniel Martin-Yerga"
__email__ = "dyerga@gmail.com"
__license__ = "GPLv3"
__program__ = "simEC"
__version__ = "0.1"

import csv
import numpy as np

class GetData:
    def __init__(self, filename):
        self.datacsv = []

        # Open and read CSV file
        textfile = open(filename)
        reader = csv.reader(textfile, delimiter=';')
        for row in reader:
            self.datacsv.append(row)
        textfile.close()

        #print ("datacsv: ", self.datacsv)
        self.numrows = len(self.datacsv)
        self.numcolumns = len(self.datacsv[1])
        self.xdata = []
        self.ydata = []

    def get_data(self):
        self.xdata = self.get_column_data(0)
        self.ydata = self.get_column_data(2)

        #Convert to uA
        self.ydata = np.array(self.ydata)*1e6

        return self.xdata, self.ydata


    def get_column_data(self, numcol):
        datatotal = []
        #print("numrows: ", self.numrows)
        for i in range(1, self.numrows):
            #print("numrow: ", i)
            #print ("numcol: ", numcol)
            #print("sdatacsv: ", self.datacsv[i])
            data = self.datacsv[i][numcol]
            if data != '':
                data = float(data)
                datatotal.append(data)
        return datatotal
