# Welcome to CSG-Bantang/neuronalCA

This an ongoing project highlighting systems involving:
1) Hodgkin-Huxley
2) Logistic Map
3) Game of Life
4) Brian's Brain
5) Neuronal Cellular Automata

### I. Hodgkin-Huxley (HH) Systems
These systems involve solving coupled ordinary differential equations (ODEs) to describe the action potential across the neuronal membrane [[1]](#1).
### Usage:
Import the package by running  `import HodgkinHuxley as HH`. 
Use `HH.solveHH(system, solver, I0, ti,tf,dt, **kwargs)` to obtain $V, m, h,$ and $n$.

This package supports three ODE solvers:
1) `solver='lsoda'`: LSODA, via odeint function
2) `solver='euler'`: Forward Euler
3) `solver='rk4'`: Runge-Kutta 4th Order

For the external stimulus, there are four sets of parameters which can be implemented in any combination, except when using LSODA. *LSODA is incompatible with noisy and coupled systems.* For the stimulus duration, provide initial time `ti`, final time `tf` and timestep `dt`.
1) Constant Input: &emsp;&emsp; $I_{1} = I_0$
2) Sinusoidal Input [[2]](#2): $I_{2} = I_s~\sin(2\pi~f_s t)$
3) Noisy Input [[3]](#3): &emsp;&emsp; $I_{3} = I_n~\eta(t)$, where $\eta(t)\in[-1,1]$, $\langle \eta \rangle_t = 0$
4) Coupling Input [[3]](#3): &ensp; $I_{4} = \sum_{j} I_{ij}$, where $I_{ij} = -g a_{ij} (V_i-V_j)$

**A) Single HH Systems** <br>
These systems involve single independent HH neuron [[1][2][3]](#1,#2,#3). Any solver can be used, and any combination of $I_{1}$ and $I_{2}$. If both $I_{1}$ and $I_{2}$ are present, $I_1$ works as the bias current. Use `HH.solveHH(system='single', solver=, I0=, ti=,tf=,dt=, Is=,fs=)`.

**B) Noisy Single HH Systems** <br>
These systems assume a uniform noise with a zero time-average [[3]](#3). Use either `solver='euler'` or `solver='rk4'`. For the external stimulus, use any combination of $I_1$, $I_2$, and $I_3$. Use `HH.solveHH(system='noisy', solver=, I0=, ti=,tf=,dt=, Is=,fs=, In=)`.

**C) Coupled HH Systems** <br>
These systems assume a square lattice of size `L` and a population $L\times L$ [[3]](#3). Use either `solver='euler'` or `solver='rk4'`. For the external stimulus, use any combination of $I_1$, $I_2$, and $I_4$. Use `HH.solveHH(system='coupled', solver=, I0=, ti=,tf=,dt=, Is=,fs=, L=,g=)`.

**D) Noisy Coupled HH Systems** <br>
These systems assume a uniform noise with a zero time-average, and a square lattice of size `L` and a population $L\times L$. Use either `solver='euler'` or `solver='rk4'`. For the external stimulus, use any combination of $I_1$, $I_2$, $I_3$, and $I_4$. For maximum insanity, provide all `kwargs`: `HH.solveHH(system='noisy coupled', solver=, I0=, ti=,tf=,dt=, Is=,fs=, In=, L=,g=)`.

### Test Cases:
Run `main.py` to test the following systems: <br>
A.1) Single HH with constant input: `HH.solveHH(system='single', solver='lsoda', I0=2.5)` <br>
A.2) Single HH with  sinusoid input: `HH.solveHH(system='single', solver='rk4', Is=10, fs=4.905)` <br>
B) Noisy HH with constant input: `HH.solveHH(system='noisy', solver='euler', In=60)` <br>
C) Coupled HH with constant input: `HH.solveHH(system='coupled', solver='euler', I0=10, L=3, g=0.1)` <br>
D) Noisy Coupled HH with bias, sinusoid, noisy input: `HH.solveHH(system='noisy coupled', solver='euler', I0=2.5, Is=10, fs=4.905, In=60, L=3, g=0.1)`


### II. Logistic Map (LM) Systems
These systems involve solving logistic equation given by $x_{t+1} = r x_{t} (1-x{t})$, where
$r$ is the growth rate and $x_{t}$ is the state of the LM system at time $t$  [[4]](#4).

### Usage:
Import the package by running  `import LogisticMap as LM`. 

**A) Steady-state x(t)** <br>
Use `LM.solveLM(r=,x0=, ti=, tf=, dt=)` to obtain steady-state values over time. Provide the growth rate `r`, where $r \in [0,4]$. Provide initial state `x0` of the system where $x_{0} \in [0,1]$. LM systems are highly stable within these range of values. For the duration, provide initial time `ti`, final time `tf` and timestep `dt`.

**B) Return Map (or Input-Output Map)** <br>
Use `LM.logisticReturnMap(r)` to obtain the return map ($x_{t+1}$ vs $x_{t}$) of the logistic equation. Provide the growth rate `r`, where $r \in [0,4]$. LM systems are highly stable within these range of values.

### Test Cases:
Run `main.py` to test the following: <br>
A) Steady-state: `x, t = LM.solveLM(r, x0, ti=0, tf=50, dt=1)`, compare with varying `r` and `x0`, $r=[0,1,2,3,4]$ and $x_0=[0.25, 0.5, 0.9]$. <br>
B) Return map: `x, y = LM.logisticReturnMap(r)`, compare with varying `r`, $r=[0,1,2,3,4]$.


### III. Game of Life (GOL) Cellular Automata (CA)
These systems involve solving for the snapshots of the spatiotemporal dynamics of a Game of Life CA  [[5]](#5).

### Usage:
Import the package by running  `import GameOfLife as GOL`. The `duration` specifies the number of snapshots to be recorded.

**A) Random Initial State** <br>
Use `GOL.solveGOL(system=0, L=, p=, duration=)` to obtain the `duration` number of snapshots. The CA is set in a lattice size `L` and initialized with states from a uniform random distribution with state density "Alive":`p` and "Dead":`1-p`.

**B) Still-Lifes** <br>
dss

## References:
<a id="1">[1]</a> Hodgkin, Alan L., and Andrew F. Huxley. "A quantitative description of membrane current and its application to conduction and excitation in nerve." The Journal of physiology 117.4 (1952): 500. <br>
<a id="2">[2]</a> Escosio, Rey Audie S., and Johnrob Y. Bantang. "Frequency response analysis of a Hodgkin-Huxley neuron in a generalized current density stimulus." Proceedings of the Samahang Pisika ng Pilipinas (2016). <br>
<a id="3">[3]</a> Pang, James Christopher S., Christopher P. Monterola, and Johnrob Y. Bantang. "Noise-induced synchronization in a lattice Hodgkin–Huxley neural network." Physica A: Statistical Mechanics and its Applications 393 (2014): 638-645. <br>
<a id="4">[4]</a> Tsuchiya, Takashi and Yamagishi, Daisuke. "The Complete Bifurcation Diagram for the Logistic Map" Zeitschrift für Naturforschung A, vol. 52, no. 6-7, 1997, pp. 513-516. https://doi.org/10.1515/zna-1997-6-708 <br>
<a id="5">[5]</a> Gardner, Martin. "Mathematical games-The fantastic combinations of John Conway’s new solitaire game, Life, 1970." _Scientific American, October_: 120-123.
