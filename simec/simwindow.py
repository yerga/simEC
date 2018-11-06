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
from __future__ import unicode_literals
__author__ = "Daniel Martin-Yerga"
__email__ = "dyerga@gmail.com"
__copyright__ = "Copyright 2018"
__license__ = "GPLv3"
__program__ = "simEC"
__version__ = "0.0.1"


from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import QTimer
from ui_simwindow import Ui_SimWindow
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import expdata

TIMERLIST = []
RUNBUTTON = []


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        fig.tight_layout()


    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, xdata, ydata, static=True, expfile=None, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.xdata = xdata
        self.ydata = ydata
        self.static = static
        self.expfile = expfile

        self.numelements = len(self.xdata)
        self.labelx = 'E / V'
        self.labely = 'i / $\mu$A'
        self.title = 'Voltammetry'
        self.i = 0

        if self.expfile:
            getdata = expdata.GetData(expfile)
            self.expxdata, self.expydata = getdata.get_data()

        if self.static:
            self.update_figure()
        else:
            self.timer = QTimer(self)
            TIMERLIST.append(self.timer)
            self.timer.timeout.connect(self.update_figure)
            self.timer.start(1)

    def update_figure(self):
        faster = True
        if faster:
            self.i +=5
        else:
            self.i += 1
        print(self.i, '/', self.numelements)
        self.axes.cla()

        if self.static:
            self.axes.plot(self.xdata, self.ydata, 'b', label="cox")
            if self.expfile:
                self.axes.plot(self.expxdata, self.expydata, 'r', label="exp")
        else:
            self.axes.plot(self.xdata[0:self.i], self.ydata[0:self.i], 'b', label="cox")
            if self.expfile:
                self.axes.plot(self.expxdata[0:self.i], self.expydata[0:self.i], 'r', label="cox")

        self.axes.set_title(self.title)

        self.axes.grid()
        self.axes.set_xlabel(self.labelx, fontsize=14)
        self.axes.set_ylabel(self.labely, fontsize=14)

        self.figure.tight_layout()
        self.draw()

        if self.static:
            RUNBUTTON[0].setEnabled(True)
        else:
            if self.i >= self.numelements:
                for timer in TIMERLIST:
                    timer.stop()
                RUNBUTTON[0].setEnabled(True)


class SimWindow (QMainWindow):
    def __init__(self, parent=None, simdata=None, static=True, firstplot="i vs E", expfile=None):
        QMainWindow.__init__(self, parent)

        potential, current, distance, time, cox, cred, cchem = simdata

        # FIXME: Small hack to enable/disable the mainwindow RunButton with a global variable
        RUNBUTTON.append(parent.runButton)
        RUNBUTTON[0].setEnabled(False)

        self.ui = Ui_SimWindow()
        self.ui.setupUi(self)
        self.centralLayout = self.ui.centrallyout

        current = np.array(current).astype(float) * 1000000

        if firstplot == "i vs E":
            xdata = potential
            ydata = current
        elif firstplot == "i vs t":
            xdata = time
            ydata = current
        elif firstplot == "E vs t":
            xdata = time
            ydata = potential
        elif firstplot == "E vs i":
            xdata = current
            ydata = potential

        dc = MyDynamicMplCanvas(width=4, height=4, dpi=100, xdata=xdata, ydata=ydata, static=static, expfile=expfile)

        self.setGeometry(400,400,400,400)
        toolbar = NavigationToolbar(dc, self)
        self.centralLayout.addWidget(toolbar)
        self.centralLayout.addWidget(dc)


        self.setFocus()

    def closeEvent(self, event):
        for timer in TIMERLIST:
            timer.stop()
        RUNBUTTON[0].setEnabled(True)
        QMainWindow.closeEvent(self, event)