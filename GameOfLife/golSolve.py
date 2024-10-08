#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:02:03 2024

@author: reinierramos
"""

import numpy as np
import itertools as itools
from .golutils import updateGrid
from PIL import Image, ImageOps

from numpy import random as nrand

rng = nrand.default_rng(17)

def solveGOL(system=0, L=50, p=0.5, duration=30):
    """
    Solves the spatiotemporal snapshot of a Game of Life (GOL) CA.
    If system is 0, then the CA is initalized in a lattice of size L 
    with uniform random distribution of states with densities
    "alive":p and "dead":1-p.
    
    If system is not 0, then the CA is initialized with predefined life-forms
    (see README.md for more information).
    
    Parameters
    ----------
    system : int, default is 0
        Determines initial state of the CA.
        If 0, then a random state is initialized.
        Accepted values are 0 to 17.
    L : int, default is 50
        Lattice size for the GOL CA.
        This will be ignored if system is not 0.
    p : float, default is 0.5
        Initial density of "alive" cells in the CA.
        Must be between [0,1].
        This will be ignored if system is not 0.
    duration : int, default is 30
        Number of timesteps to solve GOL CA.

    Returns
    -------
    soln : ndarray of shape (duration, L, L)
        Snapshots of the spatiotemporal dynamics of GOL CA.

    """
    if not system:
        grid = rng.choice([0,1], size=(L,L), replace=True, p=(1-p,p))
    else:
        _ini = GOLSystems.get(system)
        L = int(np.sqrt(len(_ini)))
        grid = _ini.reshape((L,L))
    
    grid_coords = list(itools.product(range(L), repeat=2))
    soln = np.zeros((duration+1, L,L))
    soln[0,:,:] = grid
    
    for t in range(duration):
        grid = updateGrid(L, grid, grid_coords)
        soln[t+1,:,:] = grid
    return soln

def animateGOL(soln, out='animGOL.gif'):
    """
    Saves the spatiotemporal dynamics of GOL CA.

    Parameters
    ----------
    soln : ndarray of shape (duration, L, L)
        Snapshots of the spatiotemporal dynamics of GOL CA.
    out : str, default is 'animGOL.gif'
        Output file name of the GIF.
        Must end with '.gif'
        
    """
    duration, L, _ = soln.shape
    resize = 200
    ims = [Image.fromarray(np.uint8(soln[i,:,:]*255)) for i in range(duration)]
    ims = [im.convert('P', palette=Image.ADAPTIVE, colors=2) for im in ims]
    ims = [ImageOps.contain(im, (resize,resize)) for im in ims]
    ims[0].save(fp=out, format='gif', append_images=ims, save_all=True, 
                duration=duration, loop=0
                )


#### Predefined GOL Patterns
GOLSystems = {
    1:  np.array([0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0], dtype=int),                                             #block
    2:  np.array([0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=int),     #beehive
    3:  np.array([0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0], dtype=int),     #loaf
    4:  np.array([0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0], dtype=int),                           #boat
    5:  np.array([0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0], dtype=int),                           #tub
    6:  np.array([0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0], dtype=int),                           #blinker-2
    7:  np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=int),     #toad=2
    8:  np.array([0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0], dtype=int),     #beacon-2
    9:  np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,
                  0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,
                  0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,
                  0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], dtype=int),                                          #pulsar-3
    10: np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,
                  0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=int),     #pentadecathlon-15
    11: np.array([0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0], dtype=int),                           #glider
    12: np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,
                  0,0,1,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], dtype=int),            #lightweight spaceship
    13: np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,
                  0,1,0,0,0,0,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], dtype=int),            #middleweight spaceship
    14: np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,
                  0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], dtype=int),                                #heavyweight spaceship
    15: np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=int),                       #R-pentomino
    16: np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
                  0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], dtype=int),                            #Die hard
    17: np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,
                  0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,], dtype=int),                                                      #Acorn
    }