#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 22:41:46 2024

@author: reinierramos
"""

import numpy as np
import networkx as nx
import hhSolvers as solve
from numpy import random as nrand
from matplotlib import pyplot as plt


rng = nrand.default_rng()

def solveHH(solver='euler', system='single', Iconst=0,
            tIni=0, tFin=100, dt=0.025, **kwargs):
    if 'noisy' in system and solver=='lsoda':
        raise SolverError(solver, system)
    tList = makeTimeList(tIni, tFin, dt)
    if 'coupled' in system:
        L = kwargs.get('latticeSize')
        pop = L*L
        G = nx.grid_2d_graph(L,L)  
        adjMat = nx.to_numpy_array(G)
        adjMat = np.triu(adjMat, k=0)
        kwargs.update({'aij':adjMat, 'pop':pop})
    if 'noisy' in system:
        noise = rng.random(len(tList))
        kwargs.update({'noise':noise})
    kwargs.update({'Iconst':Iconst, 'dt':dt, 'system':system})
    solver_ = solvers.get(solver)
    soln = solver_(tList, kwargs).T
    return soln, tList

def makeTimeList(tIni=0, tFin=100, dt=0.025):
    return np.arange(tIni, tFin, dt)

class SolverError(Exception):
    def __init__(self, solver, system
                , msg='LSODA is not applicable to noisy or stochastic systems.'):
        self.solver=solver
        self.system=system
        super().__init__(msg)

solvers = {'lsoda': solve.lsoda, 'euler': solve.euler, 'rk4':solve.rk4}

soln, tList = solveHH(solver='lsoda', system='single'
                      , Iconst=20, pulseAmp=0, pulseFreq=0
                      , noiseAmp=60
                      , latticeSize=3, couplStr = 0.1
                      )
plt.plot(tList, soln[0])


"""
Test Cases:
    Single neuron: Iconst=2.5, pulseAmp=0, pulseFreq=0
    Single neuron: Iconst=10, pulseAmp=0, pulseFreq=0
    Sine Input:    Iconst=0, pulseAmp=10, pulseFreq=4.905
    Coupled:       Iconst=20, pulseAmp=0, pulseFreq=0
                   latticeSize=3, couplStr = 0.1
    Noisy:         noiseAmp=60
"""