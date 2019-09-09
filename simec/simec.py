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

import sys
import inspect
from distutils.dist import strtobool
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QLineEdit, QCheckBox, QRadioButton
from PyQt5.QtCore import QSize, QPoint, QSettings
from ui_mainwindow import Ui_MainWindow
from simwindow import SimWindow
from simulation import Simulation


class MainWindow (QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupMainWindow()

        self.settings = QSettings("simEC")

    def setupMainWindow(self):
        self.tabWidget = self.ui.tabWidget
        self.tabMechanism = self.ui.tabMechanism
        self.tabReaction = self.ui.tabReaction
        self.tabOptions = self.ui.tabOptions
        self.settingsButton = self.ui.settingsButton
        self.loadButton = self.ui.loadButton
        self.loadButton.clicked.connect(self.loadSettings)
        self.saveButton = self.ui.saveButton
        self.saveButton.clicked.connect(self.saveSettings)

        self.comboMechanism = self.ui.comboMechanism
        self.comboMechanism.activated[str].connect(self.mechanismSelected)
        self.mechanismImg = self.ui.mechanismImg

        self.techniqueCB = self.ui.techniqueCB
        self.techniqueCB.activated[str].connect(self.techniqueSelected)
        self.invertReactCB = self.ui.invertCheckbox

        self.cabox = self.ui.ampBox
        self.cabox.setDisabled(True)
        self.voltbox = self.ui.voltBox

        self.Estartline = self.ui.Estartline
        self.Estartline.setText("0.5")
        self.Eswitchline = self.ui.Eswitchline
        self.Eswitchline.setText("-0.7")
        self.scanrateline = self.ui.scanrateline
        self.scanrateline.setText("0.1")
        self.shiftline = self.ui.shiftEdit
        self.shiftline.setText("0")
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
        self.diffcoefline.setText("1e-6")
        self.diffcoef2line = self.ui.diffcoef2line
        self.diffcoef2line.setText("1e-6")
        self.dblabel = self.ui.dblabel
        self.dblabel.setHidden(True)
        self.diffcoef2line.setHidden(True)
        self.arealine = self.ui.arealine
        self.arealine.setText("0.1")
        self.templine = self.ui.templine
        self.templine.setText("298")
        self.Cdlline = self.ui.Cdlline
        self.Cdlline.setText("0")
        self.Ruline = self.ui.ruline
        self.Ruline.setText("0")

        self.staticCB = self.ui.staticBt
        self.firstplotCB = self.ui.firstplotCB
        self.secondplotCB = self.ui.secondplotCB
        self.expfileline = self.ui.expFileline

        self.browseBtn = self.ui.browseBtn
        self.browseBtn.clicked.connect(self.selectExpFile)

        self.blankcb = self.ui.blankcb

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


    def techniqueSelected(self, technique):
        #TODO: complete all the enabled/disabled parameters
        if technique == "Voltammetry":
            self.cabox.setDisabled(True)
            self.voltbox.setEnabled(True)
        elif technique == "Chronoamperometry":
            self.cabox.setEnabled(True)
            self.voltbox.setDisabled(True)


    def runSimulation(self):
        print("run simulation")
        simconfig = self.getSimConfig()

        # Perform simulation
        simulation = Simulation(simconfig)
        simdata = simulation.get_data()

        # Show plots in new widget
        static = self.staticCB.isChecked()
        firstplot = self.firstplotCB.currentText()
        #TODO: show second plot
        #TODO: plot concentration profile
        expfile = (self.expfileline.text())
        blank = self.blankcb.isChecked()

        simwindow = SimWindow(self, simdata, static, firstplot, expfile, blank)
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
        diffcoef2 = float(self.diffcoef2line.text())
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
        shift = float(self.shiftline.text())
        ru = float(self.Ruline.text())

        simconfig = [technique, mechanism, Estart, Eswitch, scanrate, Eform, n, k0, alpha, diffcoef, diffcoef2, area,
                     temp, conc_bulk, kcf, kcr, EstartAmp, tstart, Epulse, tpulse, Cdl, shift, ru]

        return simconfig

    def selectExpFile(self):
        filename, ffilter = QFileDialog.getOpenFileName(self, 'Select file')
        if filename:
            self.expfileline.setText(filename)

    def saveSettings(self):
        filename, ffilter = QFileDialog.getSaveFileName(self)
        if filename:
            self.settings = QSettings(filename, QSettings.IniFormat)
            self.guisave(self.ui)
            print("Settings saved!")


    def loadSettings(self):
        filename, ffilter = QFileDialog.getOpenFileName(self, 'Select file')
        if filename:
            self.settings = QSettings(filename, QSettings.IniFormat)
            self.guirestore(self.ui)

    def guisave(self, window):
      # Save geometry
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos', self.pos())

        for name, obj in inspect.getmembers(window):
          # if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
            if isinstance(obj, QComboBox):
              name = obj.objectName()  # get combobox name
              index = obj.currentIndex()  # get current index from combobox
              text = obj.itemText(index)  # get the text for current index
              self.settings.setValue(name, text)  # save combobox selection to registry

            if isinstance(obj, QLineEdit):
              name = obj.objectName()
              value = obj.text()
              self.settings.setValue(name, value)  # save ui values, so they can be restored next time

            if isinstance(obj, QCheckBox):
              name = obj.objectName()
              state = obj.isChecked()
              self.settings.setValue(name, state)

            if isinstance(obj, QRadioButton):
              name = obj.objectName()
              value = obj.isChecked()  # get stored value from registry
              self.settings.setValue(name, value)


    def guirestore(self, window):

        # Restore geometry
        self.resize(self.settings.value('size', QSize(500, 500)))
        self.move(self.settings.value('pos', QPoint(60, 60)))

        for name, obj in inspect.getmembers(window):
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current region from combobox
                # text   = obj.itemText(index)   # get the text for new selected index
                name = obj.objectName()

                value = (self.settings.value(name))

                if value == "":
                  continue

                index = obj.findText(value)  # get the corresponding index for specified string in combobox

                if index == -1:  # add to list if not found
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)  # preselect a combobox value by index

            if isinstance(obj, QLineEdit):
              name = obj.objectName()
              value = (self.settings.value(name))  # get stored value from registry
              obj.setText(value)  # restore lineEditFile

            if isinstance(obj, QCheckBox):
              name = obj.objectName()
              value = self.settings.value(name)  # get stored value from registry
              if value != None:
                  obj.setChecked(strtobool(value))  # restore checkbox

            if isinstance(obj, QRadioButton):
             name = obj.objectName()
             value = self.settings.value(name)  # get stored value from registry
             if value != None:
                 obj.setChecked(strtobool(value))


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