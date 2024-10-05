#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 22:41:46 2024

@author: reinierramos
"""

import numpy as np
import networkx as nx
from .hhSolvers import lsoda, euler, rk4
from matplotlib import pyplot as plt
from numpy import random as nrand

import matplotlib as mpl

rng = nrand.default_rng()

axislabelsFontsize     = 17
titleFontsize          = 15
ticklabelsFontsize     = 15
dpiSize                = 300
figureParameters = {  'axes.labelsize' : axislabelsFontsize
                    , 'axes.titlesize' : titleFontsize
                    , 'xtick.labelsize': ticklabelsFontsize
                    , 'ytick.labelsize': ticklabelsFontsize
                    , 'savefig.dpi'    : dpiSize
                    , 'image.origin'   : 'lower'
                    }
mpl.rcParams.update(figureParameters)

solvers = {'lsoda': lsoda, 'euler': euler, 'rk4':rk4}

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

def plotVoltage(soln, tList):
    ti, tf = tList[0], tList[-1]
    fig, ax = plt.subplots(figsize=(6,5),
                            subplot_kw=dict(xlim=(ti-0.5, tf+0.5)
                                          , ylim=(-20,120)
                                          , xlabel='Time, in ms'
                                          , ylabel='Voltage, in mV'))
    V, _, _, _ = soln
    if len(V.shape) == 2:
        for _i in range(V.shape[1]):
            if _i == 0:  ax.plot(tList, V[:,_i], color='k', lw=2)
            else:        ax.plot(tList, V[:,_i])
    elif len(V.shape) == 1:
        ax.plot(tList, V, color='k', lw=2)
    ax.locator_params(axis='both', tight=True, nbins=5)
    return fig, ax

def plotChannels(soln, tList):
    ti, tf = tList[0], tList[-1]
    fig, ax = plt.subplots(figsize=(6,4),
                           subplot_kw=dict(xlim=(ti-0.5, tf+0.5)
                                         , ylim=(-0.05,1.05)
                                         , xlabel='Time, in ms'
                                         , ylabel='Gating variable'))
    _, m, h, n = soln    
    ax.plot(tList, m, color='darkgreen', lw=2, label='Na activation')
    ax.plot(tList, h, color='turquoise', lw=2, label='Na inactivation')
    ax.plot(tList, n, color='goldenrod', lw=2, label='K activation')
    plt.legend(fontsize=12, loc=1)
    ax.locator_params(axis='both', tight=True, nbins=5)
    return fig, ax
