#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 14:58:00 2024

@author: reinierramos
"""

import HodgkinHuxley as HH

soln, t   = HH.solveHH(system='single', solver='lsoda', I0=2.5)
figVoltA1 = HH.plotVoltage(soln, t)
figVoltA1[1].set_title('Single HH with constant input')
figChanA1 = HH.plotChannels(soln, t)
figChanA1[1].set_title('Single HH with constant input')


soln, t   = HH.solveHH(system='single', solver='rl4', Is=10, fs=4.905)
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
figVoltC[1].set_title(' Coupled HH with constant input')


soln, t  = HH.solveHH(system='noisy coupled', solver='euler', I0=2.5, Is=10, fs=4.905, In=60, L=3, g=0.1)
figVoltD = HH.plotVoltage(soln, t)
figVoltD[1].set_title('Noisy Coupled HH with bias, sinusoid, noisy input')