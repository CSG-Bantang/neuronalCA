#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 15:13:36 2024

@author: reinierramos
"""

from .hhSolve import (solveHH, makeTimeList, plotVoltage, plotChannels)
from .hhODEs import (odes, alpham, alphah, alphan, betam, betah, betan, 
                     m_inf, h_inf, n_inf, Iext)
from .hhSolvers import lsoda, euler, rk4

from .lmSolve import (solveLM, logisticEquation, logisticReturnMap, plotXvsT, plotReturnMap)