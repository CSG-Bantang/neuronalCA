#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:03:12 2024

@author: reinierramos
"""

import numba as nb

STATES=2
Dead, Alive = range(STATES)

def updateGrid(L, grid, grid_coords):
    """
    Updates the GOL grid applying golRules.

    """
    prev = grid.copy()
    for j,i in grid_coords:
        cell = prev[j,i]
        aliveNeighbors = countAliveNeighbors(L, prev, j, i)
        grid[j,i] = golRules(cell, aliveNeighbors)
    return grid

@nb.njit(nb.int32(nb.int32, nb.int32[:,:], nb.int32, nb.int32))
def countAliveNeighbors(L, prev, j, i):
    """
    Counts the number of alive neighbors of the cell in prev[j,i].

    """
    return sum([prev[j-1  ,i-1], prev[j-1  ,i], prev[j-1  ,i-L+1]
               ,prev[j    ,i-1],                prev[j    ,i-L+1]
               ,prev[j-L+1,i-1], prev[j-L+1,i], prev[j-L+1,i-L+1]
               ])

@nb.njit(nb.int32(nb.int32, nb.int32))
def golRules(cell, aliveNeighbors):
    """
    GOL Transition Rules:
        if cell=Alive and aliveNeighbors < 2, cell->Dead
        if cell=Alive and aliveNeighbors > 3, cell->Dead
        if cell=Alive and aliveNeighbors = 2, cell->Alive
        if cell=Alive and aliveNeighbors = 3, cell->Alive
        if cell=Dead  and aliveNeighbors = 3, cell->Alive

    """
    return Alive*(cell==Alive)*(aliveNeighbors==2 or aliveNeighbors==3) + \
           Alive*(cell==Dead)*(aliveNeighbors==3)