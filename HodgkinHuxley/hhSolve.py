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

def solveHH(system='single', solver='euler', 
            I0=0, Is=0, fs=0, ti=0, tf=100, dt=0.025, **kwargs):
    if solver=='lsoda' and system!='single':  raise SolverError(system, solver)
    
    tList = makeTimeList(ti, tf, dt)
    
    if 'coupled' in system:
        L = kwargs.get('L')
        population = L*L
        G = nx.grid_2d_graph(L,L)  
        adjMat = nx.to_numpy_array(G)
        adjMat = np.triu(adjMat, k=0)
        kwargs.update({'aij':adjMat, 'pop':population})
        
    if 'noisy' in system:
        noise = rng.random(len(tList))
        kwargs.update({'noise':noise})
    kwargs.update({'I0':I0, 'Is':Is, 'fs':fs, 'dt':dt, 'system':system})
    solver_ = solvers.get(solver)
    soln = solver_(tList, kwargs).T
    return soln, tList

def makeTimeList(ti=0, tf=100, dt=0.025):   return np.arange(ti, tf, dt)

class SolverError(Exception):
    def __init__(self, system, solver
                , msg='LSODA is incompatible to noisy and coupled systems.'):
        self.system=system
        self.solver=solver
        super().__init__(msg)

solvers = {'lsoda': solve.lsoda, 'euler': solve.euler, 'rk4':solve.rk4}

# soln, tList = solveHH(solver='lsoda', system='single'
#                       # , I0=20, Is=0, fs=0
#                       # , In=60
#                       # , L=3, g = 0.1
#                        )
# plt.plot(tList, soln[0])


"""
Test Cases:
    Single neuron: Iconst=2.5, pulseAmp=0, pulseFreq=0
    Single neuron: Iconst=10, pulseAmp=0, pulseFreq=0
    Sine Input:    Iconst=0, pulseAmp=10, pulseFreq=4.905
    Coupled:       Iconst=20, pulseAmp=0, pulseFreq=0
                   latticeSize=3, couplStr = 0.1
    Noisy:         noiseAmp=60
"""