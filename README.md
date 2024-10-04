This is an ongoing project highlighting:
1) Hodgkin-Huxley
2) Logistic Map
3) Game of Life
4) Brian's Brain
5) Neuronal Cellular Automata


Hodgkin-Huxley (HH) Systems:
	The current version implements three ODE solvers:
		1) lsoda: LSODA, via odeint function
		2) euler: Forward Euler
		3) rk4: Runge-Kutta 4th Order
	Use solveHH(solver='euler') method from hhSolve.py
	
	For the duration, time list is generated from tIni to tFin with timestep dt:
		solveHH(..., tIni=float, tFin=float, dt=float)
	
	For the input current, there are four sets* of parameters:
		Set 1 (Constant Input Current): solveHH(..., Iconst=float)
				I_ext = Iconst
		Set 2 (Sinusoidal Input Current): solveHH(..., Iconst=float, pulseAmp=float, pulseFreq=float)
				I_ext = Iconst + pulseAmp*np.sin(2*np.pi*pulseFreq*t)
		Set 3 (Noisy Input Current): solveHH(..., Iconst=float, noiseAmp=float)
				I_ext = Iconst + noiseAmp*noise(t)
		Set 4 (Coupling Input Current): solveHH(..., Iconst=float, latticeSize=int, couplStr=float)
				I_ext = Iconst + np.sum(-couplStr*A_ij*(V_i-V_j))
		*Any of these sets of parameters can be combined for maximum insanity 
		[except when using LSODA, which does not allow noise and coupling].
		
	A) Single HH Systems
		To solve for the voltage V(t), use solveHH(..., system='single'). 
		Any solver can be used for single HH.
	B) Noisy single HH Systems
		Assumes a uniform noise with a zero time-average.
		To solve for the voltage V(t), use solveHH(..., system='noisy'). 
		Only euler and rk4 can be used.
		Must provide noiseAmp
	C) Coupled HH Systems
		Assumes a square lattice of size latticeSize with coupling strength couplStr.
		To solve for the voltage V(t), use solveHH(..., system='coupled'). 
		Only euler and rk4 can be used.
		Must provide latticesize and couplStr.
	D) Coupled Noisy HH Systems
		To solve for the voltage V(t), use solveHH(..., system='coupled noisy').
		Only euler and rk4 can be used.
		Must provide noiseAmp, latticesize, and couplStr.