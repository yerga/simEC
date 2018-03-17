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

import numpy as np
import math as mt

class Simulation():
    def __init__(self, simconfig):
        technique, mechanism, Estart, Eswitch, scanrate, Eform, n, ko, alpha, D, area, temp, conc_bulk, \
            kcf, kcr, EstartAmp, t1, Epulse, tend = simconfig

        tunits = 1000
        xunits = 100
        # physical constants
        F = 96485
        R = 8.31451

        # TODO; multipulse amperometry
        pulses = "single"
        numpulses = 1

        if mechanism == "CE":
            if kcr != 0:
                cchem_bulk = conc_bulk / (1 + kcf / kcr)
            else:
                cchem_bulk = 0
            cox_bulk = conc_bulk - cchem_bulk
            cred_bulk = 0
        else:
            cox_bulk = conc_bulk
            cred_bulk = 0
            cchem_bulk = 0


        # ttot: time to complete one full sweep from e.start to e.start
        # tunits: number of discrete times used to calculate results
        # deltat: increment in time
        # time: vector of discrete times for diffusion grid
        if technique == "Voltammetry":
            ttot = 2 * (Estart - Eswitch) / scanrate
            deltat = ttot / tunits
            self.time = np.arange(0, ttot + deltat, deltat)
        elif technique == "Chronoamperometry":
            ttot = tend
            deltat = ttot / tunits
            self.time = np.arange(0, ttot + deltat, deltat)

        # xtot: max distance from electrode chosen to exceed difusion limit
        # xunits: number of discrete distances used to calculate results
        # deltax: increment in distance
        # distance: vector of discrete distances for diffusion grid
        xtot = 6 * mt.sqrt(D * ttot)
        # xunits = 50
        deltax = xtot / xunits
        self.distance = np.arange(0, xtot, deltax)

        # potential: vector of discrete applied potentials; initial vector is
        # filled using Estart and then potentials are calculated at other
        # times using two loops (Estart -> Eswitch and Eswitch -> Estart)
        if technique == "Voltammetry":
            self.potential = [Estart] * (tunits + 1)
            for i in range(int(tunits / 2)):
                # print(i, potential[i], potential[i] - scanrate*deltat)
                self.potential[i + 1] = self.potential[i] - scanrate * deltat
            for i in range(int((1 + tunits) / 2), tunits):
                # print(i, potential[i], potential[i] + scanrate*deltat)
                self.potential[i + 1] = self.potential[i] + scanrate * deltat
        else:
            pot1 = [Estart] * round(tunits*t1/ttot)
            pot2 = [Epulse] * (tunits-len(pot1)+1)
            self.potential = pot1 + pot2

        # kf: rate constant for forward (ox -> red) reaction at each potential
        # kb: rate constant for backward (red -> ox) reaction at each potential
        # lambda: simulation parameter (just a gathering of constants)
        kf = ko * np.exp(-alpha * n * F * (np.array(self.potential) - Eform) / (R * temp))
        kb = ko * np.exp((1 - alpha) * n * F * (np.array(self.potential) - Eform) / (R * temp))
        alambda = D * deltat / (deltax) ** 2

        # initialize diffusion grid (rows = time; cols = distance)
        #  using bulk concentrations for ox and for red
        self.cox = [[cox_bulk for x in range(xunits + 1)] for x in range(tunits + 1)]
        self.cred = [[cred_bulk for x in range(xunits + 1)] for x in range(tunits + 1)]
        self.cchem = [[cchem_bulk for x in range(xunits + 1)] for x in range(tunits + 1)]

        # create vectors for fluxes and current, which are calculated
        # later in for loops; the initial values here not important as actual
        # values are calculated later
        jox = [0.0] * (tunits + 1)
        jred = [0.0] * (tunits + 1)
        self.current_total = [0.0] * (tunits + 1)

        # calculate diffusion grid over time and over distance; for each time
        # the diffusion grid first is calculated at all distances except for
        # that at the electrode surface and then calculated at the electrode
        # surface; finally, the current is calculate for each time

        for i in range(1, tunits + 1):
            for j in range(1, xunits):
                self.cox[i][j] = self.cox[i - 1][j] + alambda * (
                        self.cox[i - 1][j - 1] - 2 * self.cox[i - 1][j] + self.cox[i - 1][j + 1])

                if mechanism == "E":
                    self.cred[i][j] = self.cred[i - 1][j] + alambda * (
                            self.cred[i - 1][j - 1] - 2 * self.cred[i - 1][j] + self.cred[i - 1][j + 1])
                elif mechanism == "EC" or mechanism == "ECat":
                    self.cred[i][j] = self.cred[i - 1][j] + alambda * (
                            self.cred[i - 1][j - 1] - 2 * self.cred[i - 1][j] + self.cred[i - 1][j + 1]) - (
                                              kcf * deltat * self.cred[i - 1][j]) + (kcr * deltat * self.cchem[i - 1][j])
                    self.cchem[i][j] = self.cchem[i - 1][j] + alambda * (
                            self.cchem[i - 1][j - 1] - 2 * self.cchem[i - 1][j] + self.cchem[i - 1][j + 1]) + (
                                               kcf * deltat * self.cred[i - 1][j]) - (kcr * deltat * self.cchem[i - 1][j])
                    if mechanism == "ECat":
                        self.cox[i][j] = self.cox[i - 1][j] + alambda * (
                                self.cox[i - 1][j - 1] - 2 * self.cox[i - 1][j] + self.cox[i - 1][j + 1]) + kcf * deltat * \
                                         self.cred[i - 1][j] - kcr * deltat * self.cox[i - 1][j]
                elif mechanism == "CE":
                    self.cox[i][j] = self.cox[i - 1][j] + alambda * (
                            self.cox[i - 1][j - 1] - 2 * self.cox[i - 1][j] + self.cox[i - 1][j + 1]) + kcf * deltat * \
                                     self.cchem[i - 1][j] - kcr * deltat * self.cox[i - 1][j]
                    self.cred[i][j] = self.cred[i - 1][j] + alambda * (
                            self.cred[i - 1][j - 1] - 2 * self.cred[i - 1][j] + self.cred[i - 1][j + 1])
                    self.cchem[i][j] = self.cchem[i - 1][j] + alambda * (
                            self.cchem[i - 1][j - 1] - 2 * self.cchem[i - 1][j] + self.cchem[i - 1][j + 1]) - (
                                               kcf * deltat * self.cchem[i - 1][j]) + (kcr * deltat * self.cox[i - 1][j])

                jox[i] = -(kf[i] * self.cox[i][1] - kb[i] * self.cred[i][1]) / (1 + (kf[i] * deltax) / D + (kb[i] * deltax) / D)

                jred[i] = -jox[i]
                self.cox[i][0] = self.cox[i][1] + jox[i] * deltax / D
                self.cred[i][0] = self.cred[i][1] + jred[i] * deltax / D
                self.cchem[i][0] = self.cchem[i][1]

            self.current_total[i] = n * F * area * jox[i]


        if technique == "Chronoamperometry":
            #FIXME: something with tend in CA
            lists = [self.potential, self.current_total, self.time, self.cox, self.cred, self.cchem]
            for lista in lists:
                if type(lista) == np.ndarray:
                    newlist = lista.tolist()
                    newlist.pop(0)
                    self.time = np.array(newlist)
                else:
                    lista.pop(0)


    def get_data(self):
        # return calculated results as a list to input into plotting functions
        # current_total: vector of current at each discrete time
        # potential: vector of discrete potentials
        # time: vector of discrete times
        # distance: vector of discrete distances
        # cox: matrix of ox concentrations in diffusion grid
        # cred: matrix of red concentrations in diffusion grid

        simdata = [self.potential, self.current_total, self.distance, self.time, self.cox, self.cred, self.cchem]
        return simdata