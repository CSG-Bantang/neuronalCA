#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 00:01:02 2024

@author: reinierramos
"""

import numpy as np
import hhODEs as HH
from scipy.integrate import odeint


def lsoda(tList, Iparams):
    Vrest = 0
    guess = [Vrest,HH.m_inf(Vrest), HH.h_inf(Vrest), HH.n_inf(Vrest)]
    # guess   = np.array([-0.283, 0.051, 0.584, 0.321])
    soln   = odeint(HH.odes, guess, tList, args=(Iparams,))
    return soln

def euler(tList, Iparams):
    dt = Iparams.get('dt')
    # Vrest = 0
    # guess = [Vrest,HH.m_inf(Vrest), HH.h_inf(Vrest), HH.n_inf(Vrest)]
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
        next_ = HH.odes(guess, tList[_i+1], Iparams).T
        guess += next_*dt
        if 'coupled' in Iparams.get('system'): soln[:,_i+1, :] = guess
        else: soln[_i+1] = guess
    return soln

    
def rk4(tList, Iparams):
    dt = Iparams.get('dt')
    # Vrest = 0
    # guess = [Vrest,HH.m_inf(Vrest), HH.h_inf(Vrest), HH.n_inf(Vrest)]
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
        k1 = dt * HH.odes(guess,        tList[_i+1],        Iparams).T
        k2 = dt * HH.odes(guess+0.5*k1, tList[_i+1]+0.5*dt, Iparams).T
        k3 = dt * HH.odes(guess+0.5*k2, tList[_i+1]+0.5*dt, Iparams).T
        k4 = dt * HH.odes(guess+k3,     tList[_i+1]+dt,     Iparams).T
        guess += (k1 + 2*(k2+k3) + k4)/6
        if 'coupled' in Iparams.get('system'): soln[:,_i+1, :] = guess
        else: soln[_i+1] = guess
    return soln
