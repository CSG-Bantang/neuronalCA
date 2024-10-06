#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 00:01:02 2024

@author: reinierramos
"""

import numpy as np
from .hhODEs import odes, m_inf, h_inf, n_inf
from scipy.integrate import odeint


def lsoda(tList, Iparams):
    """
    Solve the ODEs using LSODA (Livermore Solver for Ordinary Differential
    Equations) via the implementation of `scipy.integrate.odeint`).

    Parameters
    ----------
    tList : 1D array
        List of time values to solve the ODE.
    Iparams : dict
        Container for parameters valid for each type of stimulus input.

    Returns
    -------
    soln : 2D ndarray
        Values of V, m, h, n for al `t` in `tList`.

    Valid keywords in `Iparams`:
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

    """
    Vrest = 0
    guess = [Vrest,m_inf(Vrest), h_inf(Vrest), n_inf(Vrest)]
    # guess   = np.array([-0.283, 0.051, 0.584, 0.321])
    soln   = odeint(odes, guess, tList, args=(Iparams,))
    return soln

def euler(tList, Iparams):
    """
    Solve the ODEs using the forward Euler method.

    Parameters
    ----------
    tList : 1D array
        List of time values to solve the ODE.
    Iparams : dict
        Container for parameters valid for each type of stimulus input.

    Returns
    -------
    soln : 2D ndarray
        Values of V, m, h, n for al `t` in `tList`.
        
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
            List of generated random numbers from a uniform distribution [-0.5, 0.5].
        L : int
            Lattice size.
        pop : int
            Total number of neurons in the square lattice of size `L`.
        aij : 2D ndarray
            Adjacency matrix of the square lattice.
        g : float
            Uniform coupling strength of each neuron to its neighbors in the lattice.

    """
    dt = Iparams.get('dt')
    # Vrest = 0
    # guess = [Vrest,m_inf(Vrest), h_inf(Vrest), n_inf(Vrest)]
    guess   = np.array([-0.283, 0.051, 0.584, 0.321])
    if 'coupled' in Iparams.get('system'):
        soln = np.zeros([Iparams.get('pop'), len(tList), 4])
        soln[:,0,:] = guess
        guess = soln[:,0,:]
    else:
        soln    = np.zeros([len(tList), 4])
        soln[0] = guess
    for _i in range(len(tList)-1):
        if 'noisy' in Iparams.get('system'):
            noise_ = Iparams.get('noise')[_i]
            Iparams.update({'noise_t': noise_})
        if 'coupled' in Iparams.get('system'):
            Vi = np.tile(soln[:,_i,0], (Iparams.get('pop'),1))
            Vj = Vi.T
            Vij = Vi-Vj
            Iparams.update({'Vij':Vij})
        next_ = odes(guess, tList[_i+1], Iparams).T
        guess += next_*dt
        if 'coupled' in Iparams.get('system'): soln[:,_i+1, :] = guess
        else: soln[_i+1] = guess
    return soln

def rk4(tList, Iparams):
    """
    Solve the ODEs using the 4th-order Runge-Kutta method.

    Parameters
    ----------
    tList : 1D array
        List of time values to solve the ODE.
    Iparams : dict
        Container for parameters valid for each type of stimulus input.

    Returns
    -------
    soln : 2D ndarray
        Values of V, m, h, n for al `t` in `tList`.
        
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
            List of generated random numbers from a uniform distribution [-0.5, 0.5].
        L : int
            Lattice size.
        pop : int
            Total number of neurons in the square lattice of size `L`.
        aij : 2D ndarray
            Adjacency matrix of the square lattice.
        g : float
            Uniform coupling strength of each neuron to its neighbors in the lattice.

    """
    dt = Iparams.get('dt')
    # Vrest = 0
    # guess = [Vrest,m_inf(Vrest), h_inf(Vrest), n_inf(Vrest)]
    guess   = np.array([-0.283, 0.051, 0.584, 0.321])
    if 'coupled' in Iparams.get('system'):
        soln = np.zeros([Iparams.get('pop'), len(tList), 4])
        soln[:,0,:] = guess
        guess = soln[:,0,:]
    else:
        soln    = np.zeros([len(tList), 4])
        soln[0] = guess
    for _i in range(len(tList)-1):
        if 'noisy' in Iparams.get('system'):
            noise_ = Iparams.get('noise')[_i]
            Iparams.update({'noise_t': noise_})
        if 'coupled' in Iparams.get('system'):
            Vi = np.tile(soln[:,_i,0], (Iparams.get('pop'),1))
            Vj = Vi.T
            Vij = Vi-Vj
            Iparams.update({'Vij':Vij})
        k1 = dt * odes(guess,        tList[_i+1],        Iparams).T
        k2 = dt * odes(guess+0.5*k1, tList[_i+1]+0.5*dt, Iparams).T
        k3 = dt * odes(guess+0.5*k2, tList[_i+1]+0.5*dt, Iparams).T
        k4 = dt * odes(guess+k3,     tList[_i+1]+dt,     Iparams).T
        guess += (k1 + 2*(k2+k3) + k4)/6
        if 'coupled' in Iparams.get('system'): soln[:,_i+1, :] = guess
        else: soln[_i+1] = guess
    return soln
