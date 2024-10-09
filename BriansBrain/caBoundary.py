#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:05:28 2024

@author: reinierramos
"""

import numpy as np
import numba as nb

def getNeighbors(propsCA, grid, j, i):
    """
    Returns neighbors of cell[j,i] from grid 
    given the following keys from propsCA:
        'L': int, lattice size
            L > 0.
        'lat': str, lattice
            Accepted values: 'toroidal', 'spherical'
        'nei': str, neighborhood
            Accepted values: 'Moore', 'vonNeumann'
        'tot': str, totalisticity
            Accepted values: 'inner', 'outer'
        'L': int, radius of neighborhood
            Currently not implemented, will be ignored.
    """
    L = propsCA.get('L')
    
    match propsCA:
        case {'lat':'toroidal', 'nei':'Moore', 'tot':'inner'}:
            final = toroidal_Moore_inner(L, grid, j, i)
        case {'lat':'toroidal', 'nei':'Moore', 'tot':'outer'}:
            final = toroidal_Moore_outer(L, grid, j, i)
        case {'lat':'toroidal', 'nei':'vonNeumann', 'tot':'inner'}:
            final = toroidal_vonNeumann_inner(L, grid, j, i)
        case {'lat':'toroidal', 'nei':'vonNeumann', 'tot':'outer'}:
            final = toroidal_vonNeumann_outer(L, grid, j, i)
        case {'lat':'spherical', 'nei':'Moore', 'tot':'inner'}:
            final = spherical_Moore_inner(L, grid, j, i)
        case {'lat':'spherical', 'nei':'Moore', 'tot':'outer'}:
            final = spherical_Moore_outer(L, grid, j, i)
        case {'lat':'spherical', 'nei':'vonNeumann', 'tot':'inner'}:
            final = spherical_vonNeumann_inner(L, grid, j, i)
        case {'lat':'spherical', 'nei':'vonNeumann', 'tot':'outer'}:
            final = spherical_vonNeumann_outer(L, grid, j, i)
    return final  

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def toroidal_Moore_inner(L, grid, j, i):
    return np.array([grid[j-1, i-1],   grid[j, i-1],   grid[j-L+1, i-1],
                     grid[j-1, i],     grid[j, i],     grid[j-L+1, i],
                     grid[j-1, i-L+1], grid[j, i-L+1], grid[j-L+1, i-L+1]])

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def toroidal_Moore_outer(L, grid, j, i):
    return np.array([grid[j-1, i-1],   grid[j, i-1],   grid[j-L+1, i-1],
                     grid[j-1, i],                     grid[j-L+1, i],
                     grid[j-1, i-L+1], grid[j, i-L+1], grid[j-L+1, i-L+1]])

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def toroidal_vonNeumann_outer(L, grid, j, i):
    return np.array([grid[j, i-1],   grid[j-1, i], 
                     grid[j-L+1, i], grid[j, i-L+1]])

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def toroidal_vonNeumann_inner(L, grid, j, i):
    return np.array([grid[j, i-1],   grid[j-1, i], grid[j,i],
                     grid[j-L+1, i], grid[j, i-L+1]])

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def spherical_Moore_outer(L, grid, j, i):
    if j == 0:
        neighbors = np.empty(L-1+3).astype(np.int32)
        neighbors[:i] = grid[j,:i]
        neighbors[i:L-1] = grid[j,i+1:L]
        neighbors[L-1:] = [grid[j+1,i-1], grid[j+1,i], grid[j+1,i-L+1]]
    elif j == L-1:
        neighbors = np.empty(L-1+3).astype(np.int32)
        neighbors[:i] = grid[j,:i]
        neighbors[i:L-1] = grid[j,i+1:L]
        neighbors[L-1:] = [grid[j-1,i-1], grid[j-1,i], grid[j-1,i-L+1]]
    else:
        neighbors = np.array([grid[j-1, i-1  ], grid[j, i-1  ], grid[j-L+1, i-1  ],
                              grid[j-1, i    ],                 grid[j-L+1, i    ],
                              grid[j-1, i-L+1], grid[j, i-L+1], grid[j-L+1, i-L+1]])
    return neighbors

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def spherical_Moore_inner(L, grid, j, i):
    if j == 0:
        neighbors = np.empty(L+3).astype(np.int32)
        neighbors[:L] = grid[j,:]
        neighbors[L:] = [grid[j+1,i-1], grid[j+1,i], grid[j+1,i-L+1]]
    elif j == L-1:
        neighbors = np.empty(L+3).astype(np.int32)
        neighbors[:L] = grid[j,:]
        neighbors[L:] = [grid[j-1,i-1], grid[j-1,i], grid[j-1,i-L+1]]
    else:
        neighbors = np.array([grid[j-1, i-1  ], grid[j, i-1  ], grid[j-L+1, i-1  ],
                              grid[j-1, i    ], grid[j, i    ], grid[j-L+1, i    ],
                              grid[j-1, i-L+1], grid[j, i-L+1], grid[j-L+1, i-L+1]])
    return neighbors

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def spherical_vonNeumann_outer(L, grid, j, i):
    if j == 0:
        neighbors = np.empty(L-1+1).astype(np.int32)
        neighbors[:i] = grid[j,:i]
        neighbors[i:L-1] = grid[j,i+1:L]
        neighbors[L-1:] = grid[j+1,i]
    elif j == L-1:
        neighbors = np.empty(L-1+1).astype(np.int32)
        neighbors[:i] = grid[j,:i]
        neighbors[i:L-1] = grid[j,i+1:L]
        neighbors[L-1:] = grid[j-1,i]
    else:
        neighbors = np.array([grid[j, i-1],   grid[j-1, i], 
                         grid[j-L+1, i], grid[j, i-L+1]])
    return neighbors

@nb.njit(nb.int32[:](nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def spherical_vonNeumann_inner(L, grid, j, i):
    if j == 0:
        neighbors = np.empty(L+1).astype(np.int32)
        neighbors[:L] = grid[j,:]
        neighbors[L:] = grid[j+1,i]
    elif j == L-1:
        neighbors = np.empty(L+1).astype(np.int32)
        neighbors[:L] = grid[j,:]
        neighbors[L:] = grid[j-1,i]
    else:
        neighbors = np.array([grid[j, i-1],   grid[j-1, i], grid[j,i],
                         grid[j-L+1, i], grid[j, i-L+1]])
    return neighbors


