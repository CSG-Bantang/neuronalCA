#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 14:37:22 2024

@author: reinierramos
"""

import numpy as np
import hhSolvers as solve
from matplotlib import pyplot as plt
import networkx as nx

def singleHH(solver='euler', tIni=0, tFin=100, dt=0.025
           , Iconst = 10, pulseAmp = 0, pulseFreq = 0):
    tList = makeTimeList(tIni, tFin, dt)
    Iparams = np.array([Iconst, pulseAmp, pulseFreq, 'single'])
    solver_ = solvers.get(solver)
    soln = solver_(tList, Iparams).T
    return soln, tList

def noisyHH(solver='euler', tIni=0, tFin=100, dt=0.025
          , Iconst = 10, pulseAmp = 0, pulseFreq = 0
          , noiseAmp=10):
    tList = makeTimeList(tIni, tFin, dt)
    Iparams = np.array([Iconst, pulseAmp, pulseFreq, noiseAmp, 0, 'noisy'])
    solver_ = solversNoisy.get(solver)
    soln = solver_(tList, Iparams).T
    return soln, tList

def coupledHH(solver='euler', tIni=0, tFin=100, dt=0.025
            , Iconst = 20, pulseAmp = 0, pulseFreq = 0
            , noiseAmp=0
            , numberNeurons=(2,2), couplStr = 1):
    tList = makeTimeList(tIni, tFin, dt)
    r, c = numberNeurons        ###     population = r*c
    G = nx.grid_2d_graph(r,c)  
    adjMat = nx.to_numpy_array(G)
    adjMat = np.triu(adjMat, k=0)
    # pos = {_i:list(G.nodes)[_i] for _i in range(len(list(G.nodes)))}
    # H = nx.from_numpy_array(adjMat, create_using=nx.DiGraph)
    # nx.draw(H, pos=pos)
    # plt.show()
    
    Iparams = {'Iconst': Iconst, 'pulseAmp':pulseAmp, 'pulseFreq':pulseFreq
             # , 'noiseAmp':noiseAmp
             , 'r':r, 'c':c, 'couplStr':couplStr, 'adjMat':adjMat
             , 'type':'coupled'}
    solver_ = solversCoupled.get(solver)
    soln = solver_(tList, Iparams)
    return soln, tList
    

def makeTimeList(tIni=0, tFin=1000, dt=0.025):
    return np.arange(tIni, tFin, dt)

solvers = {'lsoda': solve.lsoda, 'euler': solve.euler, 'rk4':solve.rk4}
solversNoisy = {'euler': solve.eulerNoisy, 'rk4':solve.rk4Noisy}
solversCoupled = {'euler': solve.eulerCoupled, 'rk4':solve.rk4Coupled}


# ### Example single
# soln, tList = singleHH(solver='lsoda', Iconst=0, pulseAmp=10, pulseFreq=4.905, tFin=500)
# plt.plot(tList, soln[0])


# ### Example noisy
# soln, tList = noisyHH(solver='euler', Iconst=20, pulseAmp=0, pulseFreq=0, tFin=500, noiseAmp=20)
# plt.plot(tList, soln[0])

### Example coupled
L = 3
soln, tList = coupledHH(solver='euler', Iconst=20, tFin=200, noiseAmp=0, numberNeurons=(L,L), couplStr=0.1)
for i in range(L*L):
    plt.plot(tList, soln[i,:,0])

