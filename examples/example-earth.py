# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import scipy as sp
import pylab as plt
import scipy.integrate as integ
import os

import plynet as ply

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#			EARTH INTEGRATION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#=======================================================================
#Configuration of the integration 
#=======================================================================

#Linear temperature profile
h = 100 #Len of the arrays
ur = np.linspace(0,1,h)
T0 = np.linspace(5000,300,h)

#Two layers considered
comp = [{'comp':'Fe', 'MF':0.33, 'RL':0.5, 'EOS':'BM3'},{'comp':'pv_fmw', 'MF':0.67, 'RL':1.0, 'EOS':'Vinet'}]

#Creating the planet earth
earth = ply.data.planet( urvec=ur, Tvec=T0, M=1.0, R=1.0, comp=comp )

#Integration Scheme
ply.numeric.confnum.scheme = 'rk4'
#Integratio step
ply.numeric.confnum.h_step = 1./150

#Error in residual mass condition
ply.numeric.confnum.accuracy_mr = 1e-10
#Number maxim of iterations in residual mass condition
ply.numeric.confnum.n_max_mr = 40
#Number of bisections in planet radius optimization
ply.numeric.confnum.n_section = 2
#Adimensional minim radius of integration. where criterion mass convergence will be performance
ply.numeric.confnum.r_min_int = 0.0

#Error in temperature convergence criterion
ply.numeric.confnum.accuracy_tmp = 0.05/100.
#Maxim Number of iteration for temperature convergence
ply.numeric.confnum.n_max_tmp = 20

#=======================================================================
#Integration
#=======================================================================

#Temperature iteration
earth.structure()
   
#=======================================================================
#Results
#=======================================================================
earth.save()

plt.plot(earth.urvec,earth.mrvec,label='mass')
plt.legend()
plt.savefig("Mass.png")
plt.close('all')

plt.plot(earth.urvec,earth.rhovec,label='density')
plt.legend()
plt.savefig("Density.png")
plt.close('all')

plt.plot(earth.urvec,earth.Pvec,label='pressure')
plt.legend()
plt.savefig("Pressure.png")
plt.close('all')

plt.plot(earth.urvec,earth.gvec,label='gravity')
plt.legend()
plt.savefig("Gravity.png")
plt.close('all')

plt.plot(earth.urvec,earth.Tvec,label='temperature')
plt.legend()
plt.savefig("Temperature.png")
plt.close('all')
