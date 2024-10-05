#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 22:42:32 2024

@author: reinierramos
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

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

def logisticEquation(r=1.0, xt=0.5):    return r*xt*(1-xt)

def solveLM(r=1.0, x0=0.5, ti=0, tf=50, dt=1):
    """
    Solves logistic map (LM) equation given a duration.

    Parameters
    ----------
    r : float, default is 1.0
        Logistic growth rate.
        Must be between 0 and 4.
    x0 : float, default is 0.5
        Normalized initial state of the LM system.
        Must be between 0 and 1.
    ti : float, default is 0
        Initial time, in arb. time unit.
    tf : float, default is 50
        Final time, in arb. time unit.
    dt : float, default is 1
        Time step, in arb. time unit.

    Returns
    -------
    xList : 1D ndarray
        Values of x(t).
    tList : 1D ndarray
        Time points for which LM is evaluated.

    """
    tList = np.arange(ti,tf,dt)
    xList = np.zeros(len(tList))
    xList[0] = x0
    for _i in range(len(tList)-1):
        xList[_i+1] = logisticEquation(r, xList[_i])
    return xList, tList

def logisticReturnMap(r=1.0):
    """
    Return map for the logistic equation x[t+1] = r * (1-x[t]) * x[t].

    Parameters
    ----------
    r : float, default is 1.0
        Logistic growth rate.
        Must be between 0 and 4.

    Returns
    -------
    x : 1D ndarray
        Input states x[t].
    y : 1D ndarray
        Output states x[t+1].

    """
    x = np.linspace(0, 1, 300)
    y = logisticEquation(r, x)
    return x, y

def plotXvsT(x, t):
    """
    Plotter function for normalized steady-state x(t).

    Parameters
    ----------
    x : 1D ndarray
        Values of x(t).
    t : 1D ndarray
        Time points for which LM is evaluated.

    Returns
    -------
    fig : matplotlib.figure.Figure object
        Figure instance for which x(t) is plotted.
        Has all the attributes of matplotlib.figure.Figure
    ax : matplotlib.axes._axes.Axes object
        Axes instance for which x(t) is plotted.
        Has all the attributes of matplotlib.axes._axes.Axes
    
    `fig` and `ax` are the same as if `fig, ax = plt.subplots()` is called.

    """
    ti, tf = t[0], t[-1]
    fig, ax = plt.subplots(figsize=(6,5),
                           subplot_kw=dict(xlim=(ti-0.5, tf+0.5)
                                         , ylim=(-0.05,1.05)
                                         , xlabel='Timestep, t'
                                         , ylabel='Steady-state, x(t)'))
    ax.plot(t, x, color='k', lw=1, marker='d', markersize=8, markerfacecolor='white')
    ax.locator_params(axis='both', tight=True, nbins=5)
    return fig, ax

def plotReturnMap(x, y, show_diagonal=True):
    """
    Plotter function for normalized return map of logistic equation.
    A dashed diagonal, y = x, line is shown in the background for future analysis.

    Parameters
    ----------
    x : 1D ndarray
        Input states x[t].
    y : 1D ndarray
        Output states x[t+1].
    show_diagonal : bool, default is True
        If True, plots a dashed diagonal, y = x, in the background.

    Returns
    -------
    fig : matplotlib.figure.Figure object
        Figure instance for which return map is plotted.
        Has all the attributes of matplotlib.figure.Figure
    ax : matplotlib.axes._axes.Axes object
        Axes instance for which return map is plotted.
        Has all the attributes of matplotlib.axes._axes.Axes
    
    `fig` and `ax` are the same as if `fig, ax = plt.subplots()` is called.

    """
    fig, ax = plt.subplots(figsize=(6,6),
                           subplot_kw=dict(xlim=(-0.05,1.05)
                                         , ylim=(-0.05,1.05)
                                         , xlabel='Previous Steady-State, $x_{t}$'
                                         , ylabel='Next Steady-State, $x_{t+1}$'))
    if show_diagonal:      ax.plot(x, x, color='gray', ls='--', lw=2)
    ax.plot(x, y, color='k', lw=4)
    ax.locator_params(axis='both', tight=True, nbins=5)
    return fig, ax
