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
h = 100. #Len of the arrays
ur = np.linspace(0,1,h)
def T0_prof( Tup, dT ):
    T0 = np.zeros(h)
    i = -1
    T_end = 0
    for r in np.linspace(1,0,h):
	if r>0.98:
	    T0[i] = Tup + 1200*(1.0-r)/0.02
	if r<0.98 and r>0.55:
	    T0[i] = 1500*np.exp( (0.98**2-r**2)/1 )
	    T_end = T0[i]
	if r<0.55:
	    T0[i] = (T_end+dT)*np.exp( (0.55**2-r**2)/1 )
	i-=1
    return T0
    
T0 = T0_prof(300,5000)
	    
#Three layers considered
#comp = [\
#{'comp':'Fe',	    'MF':0.1,'Rini':0.0, 'Rend':0.2, 'EOS':'Vinet','criterion':'-'},\
#{'comp':'Fe08FeS02','MF':0.3,'Rini':0.2, 'Rend':0.55,'EOS':'Vinet','criterion':'Radius'},
#{'comp':'ol',	    'MF':0.6,'Rini':0.55,'Rend':1.0, 'EOS':'Vinet','criterion':'Radius'}]

#Two layers considered
comp = [\
{'comp':'Fe08FeS02','MF':0.33,'Rini':0.0, 'Rend':0.55,'EOS':'Vinet','criterion':'Radius'},
{'comp':'pv_fmw','MF':0.67,'Rini':0.55,'Rend':1.0, 'EOS':'Vinet','criterion':'Mass'}]
#{'comp':'ol','MF':0.67,'Rini':0.55,'Rend':1.0, 'EOS':'Vinet','criterion':'Mass'}]

'''
CMM = 0.33
Rc = 0.55
ur = np.linspace(0,1,100)
comp = [\
{'comp':'Fe08FeS02','MF':CMM,   'Rini':0.0, 'Rend':Rc,  'EOS':'Vinet', 'criterion':'-'},
{'comp':'pv_fmw',   'MF':1-CMM, 'Rini':Rc,  'Rend':1.0, 'EOS':'Vinet', 'criterion':'Mass'}]
'''

#Creating the planet earth
earth = ply.data.planet( urvec=ur, Tvec=T0, M=1.0, R=1.1, comp=comp )

#Integration Scheme
ply.numeric.confnum.scheme = 'rk4'
#Integratio step
ply.numeric.confnum.h_step = 1./900

#Error in residual mass condition
ply.numeric.confnum.accuracy_mr = 1e-10
#Number maxim of iterations in residual mass condition
ply.numeric.confnum.n_max_mr = 50
#Number of bisections in planet radius optimization
ply.numeric.confnum.n_section = 2
#Adimensional minim radius of integration. where criterion mass convergence will be performance
ply.numeric.confnum.r_min_int = 0.0


#=======================================================================
#Integration
#=======================================================================

#Temperature iteration
earth.structure()

#Load previous datas
#earth.load( filename='planet-state000', fmt=['ur','r','mr','rho','P','g','phi','T'] )   

#=======================================================================
#Results
#=======================================================================
earth.save()
earth2 = ply.data.planet( urvec=ur, M=1.0, R=1.1, comp=comp )

earth2.load( filename = 'prem', fmt=['ur','-','rho','P','g','mr'] )

plt.plot(earth.urvec,earth.mrvec,label='mass')
plt.legend()
plt.savefig("Mass.png")
plt.xlabel( 'r [$R_{earth}$]' )
plt.ylabel( 'M [Kg]' )
plt.close('all')

#plt.subplot(121)
plt.plot(earth2.urvec,earth2.rhovec,'o-',label='density PREM')
plt.plot(earth.urvec,earth.rhovec,label='density')
plt.xlabel( 'r [$R_{earth}$]' )
plt.ylabel( '$\\rho$ [kg/m$^3$]' )
plt.legend()
plt.savefig("Density.png")
plt.close('all')


#plt.subplot(122)
plt.plot(earth2.urvec,earth2.Pvec*1e9,'o-',label='pressure PREM')
plt.plot(earth.urvec,earth.Pvec,label='pressure')
plt.xlabel( 'r [$R_{earth}$]' )
plt.ylabel( 'P [Pa]' )
plt.legend()
plt.savefig("Pressure.png")
plt.close('all')




plt.plot(earth.urvec,earth.gvec,label='gravity')
plt.plot(earth2.urvec,earth2.gvec,'o-',label='gravity PREM')
plt.legend()
plt.xlabel( 'r [$f_{earth}$]' )
plt.ylabel( 'g [m/s$^2$]' )
plt.savefig("Gravity.png")
plt.close('all')

plt.plot(earth.urvec,earth.Tvec,label='temperature')
plt.legend()
plt.xlabel( 'r [$f_{earth}$]' )
plt.ylabel( 'T [K]' )
plt.savefig("Temperature.png")
plt.close('all')

#plt.show()
