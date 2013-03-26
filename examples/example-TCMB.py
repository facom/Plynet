# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import scipy as sp
import pylab as plt
import scipy.integrate as integ
import os

import plynet as ply

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#			MASS-RADIUS RELATION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#=======================================================================
#Parameters Configuration
#=======================================================================
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
#Planets declaration
#=======================================================================
#Composition
comp = [{'comp':'Fe', 'MF':0.33, 'RL':0.5, 'EOS':'BM3'},{'comp':'pv_fmw', 'MF':0.67, 'RL':1.0, 'EOS':'BM3'}]

planet = []			#Arrays of planets
N = 40				#Number of planets
Mvec = np.linspace(1.0,5.,N)	#Vector of mass
Rvec = []			#Vector of radius
TCMB = []			#Vector of temperature in core-mantle boundary

i = 0
for M in Mvec:
    print '\n\nIntegration of Planet %d'%(i+1)
    planet.append( ply.data.planet(M=M, comp=comp) )
    planet[i].structure()
    Rvec.append(planet[i].R*ply.physics.confphys.R_SI)
    TCMB.append(planet[i].T(planet[i].comp[0]['RL']))
    planet[i].save(suffix='N%d'%i)		#Save each planet as .dat file
    i += 1


#=======================================================================
#Results
#=======================================================================

#Mass-Radius
plt.title('Mass-Radius relation')
plt.xlabel('Mass (Earth Units)')
plt.ylabel('Radius')  
plt.plot(Mvec,Rvec,label='Mass-Radius')
plt.legend()
plt.savefig("Mass-Radius.png")
plt.close('all')

#Temperature CMB
plt.title('Mass-TCMB relation')
plt.xlabel('Mass (Earth Units)')
plt.ylabel('TCMB (k)')  
plt.plot(Mvec,TCMB,label='Mass-TCMB')
plt.legend()
plt.savefig("Mass-TCMB.png")
plt.close('all')


np.savetxt('Mass-data.dat', np.transpose([Rvec,Mvec,TCMB]),fmt='%.18e', delimiter=' ')


#Temperature Profiles
for i in xrange(0,N):
    plt.title('Temperature profiles')
    plt.xlabel('Radius (SI)')
    plt.ylabel('Temperature (K)')
    plt.plot(planet[i].urvec*planet[i].R*ply.physics.confphys.R_SI,planet[i].Tvec,label='%.2f EM'%Mvec[i])
plt.legend()
plt.savefig("Temp-Profiles.png")
plt.close('all')


#Density Profiles
for i in xrange(0,N):
    plt.title('Density profiles')
    plt.xlabel('Radius (SI)')
    plt.ylabel('Density (SI)')
    plt.plot(planet[i].urvec*planet[i].R*ply.physics.confphys.R_SI,planet[i].rhovec,label='%.2f EM'%Mvec[i])
plt.legend()
plt.savefig("Dens-Profiles.png")
plt.close('all')