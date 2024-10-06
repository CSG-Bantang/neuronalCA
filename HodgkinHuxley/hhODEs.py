#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 00:07:10 2024

@author: reinierramos
"""

import numpy as np

C   =    1
GNa =  120
GK  =   36
Glk =    0.3
ENa =  115
EK  = - 12
Elk =   10.6

def odes(vars_, t, params_):
    """
    Set of coupled ODEs modeling Hodgkin-Huxley system.
    The external stimulus is described by `params_`.
    
    Parameters
    ----------
    vars_ : 2D or 3D ndarray
        Values of V, m, h, n at time `t-1`.
    t : float or ndarray
        Time for which `vars_` is calculated.
    params_ : dict
        Container for parameters valid for each type of stimulus input.

    Returns
    -------
    [...] : 2D or 3D ndarray
        Values of V, m, h, n at time `t`.

    """
    V, m, h, n = vars_.T
    channelNa = GNa * (ENa-V) * np.power(m,3) * h 
    channelK  = GK  * (EK -V) * np.power(n,4)
    channellk = Glk * (Elk-V)
    
    I = Iext(params_, t)

    dVdt = (channelNa + channelK + channellk + I)/C
    dmdt = alpham(V)*(1-m) - betam(V)*m
    dhdt = alphah(V)*(1-h) - betah(V)*h
    dndt = alphan(V)*(1-n) - betan(V)*n
    return np.array([dVdt, dmdt, dhdt, dndt])

### Boltzmann Transport Equations
def alphan(V_): return 0.01*(10-V_) / (np.exp((10-V_)/10)-1)
def alpham(V_): return 0.1*(25-V_) / (np.exp((25-V_)/10)-1) 
def alphah(V_): return 0.07*np.exp(-V_/20)
def betah(V_):  return 1 / (np.exp((30-V_)/10)+1)
def betam(V_):  return 4*np.exp(-V_/18)
def betan(V_):  return 0.125*np.exp(-V_/80)

### Steady-State Values of Channels
def n_inf(V_=0.0):  return alphan(V_) / (alphan(V_) + betan(V_))
def m_inf(V_=0.0):  return alpham(V_) / (alpham(V_) + betam(V_))
def h_inf(V_=0.0):  return alphah(V_) / (alphah(V_) + betah(V_))

def Iext(params_, t):
    """
    External stimulus current injected to a single HH neuron.

    Parameters
    ----------
    params_ : dict
        Container for parameters valid for each type of stimulus input.
    t : float or ndarray
        Time for which `I` is calculated.

    Returns
    -------
    I : float or ndarray
        Total external stimulus.

    Valid keywords in `params_`:
        system : str
            Type of HH system ('single', 'noisy', 'coupled', 'noisy coupled').
        dt : float
            Timestep size, in ms.
        I0 : float
            Amplitude, in uA/cm^2, of the constant or bias current.
        Is : float
            Amplitude, in uA/cm^2, of the sine input.
        fs : float
            Frequency, in Hz, of the sine input.
        In : float
            Amplitude, in uA/cm^2, of the noisy input.
        noise : 1D ndarray
            List of generated random numbers from a uniform distribution [0, 1].
        noise_t : float
            Value of the noise at time t, extracted from `noise(t)`.
        L : int
            Lattice size.
        pop : int
            Total number of neurons in the square lattice of size `L`.
        aij : 2D ndarray
            Adjacency matrix of the square lattice.
        g : float
            Uniform coupling strength of each neuron to its neighbors in the lattice.
        Vij : ndarray
            Voltage difference Vi - Vj from neighboring neurons.
        
    """
    I0 = params_.get('I0')
    Is, fs = params_.get('Is'), params_.get('fs')/1000
    Isine = Is * np.sin(2*np.pi*fs*t)
    if 'noisy' in params_.get('system'):
        sigma, eta_t = params_.get('In'), params_.get('noise_t')
        Inoise = sigma*(eta_t - 0.5)
        I0 += Inoise
    if 'coupled' in params_.get('system'):
        g, aij, Vij = params_.get('g'), params_.get('aij'), params_.get('Vij')
        Iij = np.sum(-g*aij*Vij, axis=0)
        Iij[0] += I0 + Isine
        return Iij
    return I0 + Isine