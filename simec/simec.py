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
__copyright__ = "Copyright 2018"
__license__ = "GPLv3"
__program__ = "simEC"
__version__ = "0.0.1"

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui_mainwindow import Ui_MainWindow
from simwindow import SimWindow
from simulation import Simulation


class MainWindow (QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupMainWindow()

    def setupMainWindow(self):
        self.tabWidget = self.ui.tabWidget
        self.tabMechanism = self.ui.tabMechanism
        self.tabReaction = self.ui.tabReaction
        self.tabOptions = self.ui.tabOptions
        self.backButton = self.ui.backButton
        self.nextButton = self.ui.nextButton
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        self.settingsButton = self.ui.settingsButton

        self.comboMechanism = self.ui.comboMechanism
        self.comboMechanism.activated[str].connect(self.mechanismSelected)
        self.mechanismImg = self.ui.mechanismImg

        self.techniqueCB = self.ui.techniqueCB
        self.invertReactCB = self.ui.invertCheckbox

        self.Estartline = self.ui.Estartline
        self.Estartline.setText("0.5")
        self.Eswitchline = self.ui.Eswitchline
        self.Eswitchline.setText("-0.7")
        self.scanrateline = self.ui.scanrateline
        self.scanrateline.setText("0.1")
        self.EstartAmpline = self.ui.EstartAmpline
        self.EstartAmpline.setText("0.8")
        self.tstartline = self.ui.tstartline
        self.tstartline.setText("3")
        self.Epulseline = self.ui.Epulseline
        self.Epulseline.setText("-0.5")
        self.tpulseline = self.ui.tpulseline
        self.tpulseline.setText("30")
        self.Eformline = self.ui.Eformline
        self.Eformline.setText("0")
        self.k0line = self.ui.k0line
        self.k0line.setText("0.01")
        self.numelline = self.ui.numelline
        self.numelline.setText("1")
        self.alphaline = self.ui.alphaline
        self.alphaline.setText("0.5")
        self.kcfline = self.ui.kcfline
        self.kcfline.setText("0")
        self.kcrline = self.ui.kcrline
        self.kcrline.setText("0")
        self.concline = self.ui.concline
        self.concline.setText("5e-8")
        self.diffcoefline = self.ui.diffcoefline
        self.diffcoefline.setText("1e-5")
        self.arealine = self.ui.arealine
        self.arealine.setText("0.1")
        self.templine = self.ui.templine
        self.templine.setText("298")
        self.Cdlline = self.ui.Cdlline
        self.Cdlline.setText("0")

        self.staticCB = self.ui.staticBt
        self.firstplotCB = self.ui.firstplotCB
        self.secondplotCB = self.ui.secondplotCB
        self.expfileline = self.ui.expFileline

        self.browseBtn = self.ui.browseBtn
        self.browseBtn.clicked.connect(self.selectExpFile)

        self.runButton = self.ui.runButton
        self.runButton.clicked.connect(self.runSimulation)

        self.actionQuit = self.ui.actionQuit
        self.actionQuit.triggered.connect(self.quitApp)

    def quitApp(self):
        app.quit()

    def mechanismSelected(self, mechanism):
        if mechanism == "E":
            #print("E")
            self.mechanismImg.setText("<html><head/><body><p><img src=\":/figs/E.png\"/></p></body></html>")
        elif mechanism == "EC":
            #print("EC")
            self.mechanismImg.setText("<html><head/><body><p><img src=\":/figs/EC.png\"/></p></body></html>")
        elif mechanism == "ECE":
            #print("ECE")
            self.mechanismImg.setText("<html><head/><body><p><img src=\":/figs/ECE.png\"/></p></body></html>")

    def onNextButtonClicked(self):
        index = self.tabWidget.currentIndex()
        numtabs = self.tabWidget.count()
        print(index, numtabs)
        if index < numtabs-1:
            self.tabWidget.setCurrentIndex(index+1)

    def runSimulation(self):
        print("run simulation")
        simconfig = self.getSimConfig()

        # Perform simulation
        simulation = Simulation(simconfig)
        simdata = simulation.get_data()

        # Show plots in new widget
        static = self.staticCB.isChecked()
        firstplot = self.firstplotCB.currentText()
        expfile = (self.expfileline.text())

        simwindow = SimWindow(self, simdata, static, firstplot, expfile)
        simwindow.show()


    def getSimConfig(self):
        mechanism = self.comboMechanism.currentText()
        technique = self.techniqueCB.currentText()
        Estart = float(self.Estartline.text())
        Eswitch = float(self.Eswitchline.text())
        Eform = float(self.Eformline.text())
        n = float(self.numelline.text())
        k0 = float(self.k0line.text())
        alpha = float(self.alphaline.text())
        diffcoef = float(self.diffcoefline.text())
        area = float(self.arealine.text())
        temp = float(self.templine.text())
        scanrate = float(self.scanrateline.text())
        conc_bulk = float(self.concline.text())
        kcf = float(self.kcfline.text())
        kcr = float(self.kcrline.text())
        EstartAmp = float(self.EstartAmpline.text())
        tstart = float(self.tstartline.text())
        Epulse = float(self.Epulseline.text())
        tpulse = float(self.tpulseline.text())
        Cdl = float(self.Cdlline.text())

        simconfig = [technique, mechanism, Estart, Eswitch, scanrate, Eform, n, k0, alpha, diffcoef, area, temp,
                     conc_bulk, kcf, kcr, EstartAmp, tstart, Epulse, tpulse, Cdl]

        return simconfig

    def selectExpFile(self):
        filename, ffilter = QFileDialog.getOpenFileName(self, 'Select file')
        if filename:
            self.expfileline.setText(filename)


if __name__ == "__main__":

    #QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv)
    app.setApplicationName("simEC")
    app.setApplicationVersion("0.1.0")

    appname = "org.dyerga.simec"

    window = MainWindow()
    window.setWindowTitle("simEC")
    window.show()

    sys.exit(app.exec_())