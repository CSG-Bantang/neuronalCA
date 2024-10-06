#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 14:58:00 2024

@author: reinierramos
"""

import HodgkinHuxley as HH
import LogisticMap as LM
import GameOfLife as GOL
from matplotlib import pyplot as plt


# ### Hodgkin-Huxley Systems
soln, t   = HH.solveHH(system='single', solver='lsoda', I0=2.5)
figVoltA1 = HH.plotVoltage(soln, t)
figVoltA1[1].set_title('Single HH with constant input')
figChanA1 = HH.plotChannels(soln, t)
figChanA1[1].set_title('Single HH with constant input')

soln, t   = HH.solveHH(system='single', solver='rk4', Is=10, fs=4.905)
figVoltA2 = HH.plotVoltage(soln, t)
figVoltA2[1].set_title('Single HH with sinusoid input')
figChanA2 = HH.plotChannels(soln, t)
figChanA2[1].set_title('Single HH with sinusoid input')

soln, t  = HH.solveHH(system='noisy', solver='euler', In=60)
figVoltB = HH.plotVoltage(soln, t)
figVoltB[1].set_title('Noisy HH with constant input')
figVoltB = HH.plotChannels(soln, t)
figVoltB[1].set_title('Noisy HH with constant input')

soln, t  = HH.solveHH(system='coupled', solver='euler', I0=10, L=3, g=0.1)
figVoltC = HH.plotVoltage(soln, t)
figVoltC[1].set_title('Coupled HH with constant input')

soln, t  = HH.solveHH(system='noisy coupled', solver='euler', I0=2.5, Is=10, fs=4.905, In=60, L=3, g=0.1)
figVoltD = HH.plotVoltage(soln, t)
figVoltD[1].set_title('Noisy Coupled HH with bias, sinusoid, noisy input')

plt.close()


### Logistic Map Systems
for r in [0,1,2,3,4]:
    for x0 in [0.25, 0.5, 0.9]:
        x, t = LM.solveLM(r, x0, ti=0, tf=25, dt=1)
        figSteadyState = LM.plotXvsT(x, t)
        figSteadyState[1].set_title(f'Steady-state of LM system, $r={r}$, $x_0={x0}$')
        plt.show()
        plt.close()

for r in [0,1,2,3,4]:
    x, y = LM.logisticReturnMap(r)
    figLMap = LM.plotReturnMap(x, y)
    figLMap[1].set_title(f'Return map of LM system, $r={r}$')
    plt.show()
    plt.close()


### Game of Life Systems
soln=GOL.solveGOL(system=0, L=50, p=0.5, duration=30)
GOL.animateGOL(soln)

soln=GOL.solveGOL(system=11, duration=30)
GOL.animateGOL(soln)


