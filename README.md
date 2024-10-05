# Welcome to CSG-Bantang/neuronalCA

This an ongoing project highlighting systems involving:
1) Hodgkin-Huxley
2) Logistic Map
3) Game of Life
4) Brian's Brain
5) Neuronal Cellular Automata


## I. Hodgkin-Huxley (HH) Systems
These systems involve solving coupled ordinary differential equations (ODEs) to describe the action potential in the neuronal membrane [[1]](#1). <br>
Use `solveHH(system, solver, I0, ti,tf,dt, **kwargs)` to obtain $V, m, h,$ and $n$. <br>
This package supports three ODE solvers:
1) `solver="lsoda"`: LSODA, via odeint function
2) `solver="euler"`: Forward Euler
3) `solver="rk4"`: Runge-Kutta 4th Order

For the external stimulus, there are four sets of parameters which can be implemented in any combination, except when using LSODA<sup>a </sup>.
1) Constant Input: &emsp;&emsp; $I_{1} = I_0$
2) Sinusoidal Input [[2]](#2): $I_{2} = I_s~\sin(2\pi~f_s t)$
3) Noisy Input [[3]](#3): &emsp;&emsp; $I_{3} = I_n~\eta(t)$, where $\eta(t)\in[-1,1]$, $\langle \eta \rangle_t = 0$
4) Coupling Input [[3]](#3): &ensp; $I_{4} = \sum_{j} I_{ij}$, where $I_{ij} = -g a_{ij} (V_i-V_j)$

*<sup>a </sup> LSODA is incompatible with noisy and coupled systems.*

For the stimulus duration, provide initial time `ti`, final time `tf` and timestep `dt`.

### A) Single HH Systems
These systems involve single independent HH neuron [[1][2][3]](#1,#2,#3). Any solver can be used, and any combination of $I_{1}$ and $I_{2}$. <br>
If both $I_{1}$ and $I_{2}$ are present, $I_1$ works as the bias current. <br>
Use `solveHH(system="single", solver=, I0=, ti=,tf=,dt=, Is=,fs=)`

### B) Noisy Single HH Systems
These systems assume a uniform noise with a zero time-average [[3]](#3). Use either `euler` or `rk4`. For the external stimulus, use any combination of $I_1$, $I_2$, and $I_3$. <br>
Use `solveHH(system="noisy", solver=, I0=, ti=,tf=,dt=, Is=,fs=, In=)`

### C) Coupled HH Systems
These systems assume a square lattice of size `L` and a population $L\times L$ [[3]](#3). <br>
Use either `euler` or `rk4`. For the external stimulus, use any combination of $I_1$, $I_2$, and $I_4$. <br>
Use `solveHH(system="coupled", solver=, I0=, ti=,tf=,dt=, Is=,fs=, L=,g=)`

### D) Noisy Coupled HH Systems
These systems assume a uniform noise with a zero time-average, and a square lattice of size `L` and a population $L\times L$. <br>
Use either `euler` or `rk4`. For the external stimulus, use any combination of $I_1$, $I_2$, $I_3$, and $I_4$. <br>
For maximum insanity, provide all `kwargs`: `solveHH(system="noisy coupled", solver=, I0=, ti=,tf=,dt=, Is=,fs=, In=, L=,g=)`.

### Test Cases:
A.1) Single HH with constant input: `solveHH(system='single', solver='lsoda', I0=2.5)` <br>
A.2) Single HH with  sinusoid input: `solveHH(system='single', solver='rl4', Is=10, fs=4.905)` <br>
B) Noisy HH with constant input: `solveHH(system='noisy', solver='euler', In=60)` <br>
C) Coupled HH with constant input: `solveHH(system='coupled', solver='euler', I0=10, L=3, g=0.1)` <br>
D) Noisy Coupled HH with bias, sinusoid, noisy input: `solveHH(system='noisy coupled', solver='euler', I0=2.5, Is=10, fs=4.905, In=60, L=3, g=0.1)` <br>

## References:
<a id="1">[1]</a> Hodgkin, Alan L., and Andrew F. Huxley. "A quantitative description of membrane current and its application to conduction and excitation in nerve." The Journal of physiology 117.4 (1952): 500. <br>
<a id="2">[2]</a> Escosio, Rey Audie S., and Johnrob Y. Bantang. "Frequency response analysis of a Hodgkin-Huxley neuron in a generalized current density stimulus." Proceedings of the Samahang Pisika ng Pilipinas (2016). <br>
<a id="3">[3]</a> Pang, James Christopher S., Christopher P. Monterola, and Johnrob Y. Bantang. "Noise-induced synchronization in a lattice Hodgkin–Huxley neural network." Physica A: Statistical Mechanics and its Applications 393 (2014): 638-645. <br>
