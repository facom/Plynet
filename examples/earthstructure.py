# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################################################
#	EXAMPLE: EARTH INTERIOR STRUCTURE
#########################################################################################

#========================================================================================
#		IMPORTS
#========================================================================================
import numpy as np
import scipy as sp
import pylab as plt
import scipy.integrate as integ
import os
#Plynet!
import plynet as ply


#========================================================================================
#		CONFIGURATION OF INTEGRATION SCHEME
#========================================================================================
#Integration Scheme
ply.numeric.confnum.scheme = 'rk4'
#Integratio step
ply.numeric.confnum.h_step = 1./1000

#Error in residual mass condition
ply.numeric.confnum.accuracy_mr = 1e-10
#Number maxim of iterations in residual mass condition
ply.numeric.confnum.n_max_mr = 60
#Number of bisections in planet radius optimization
ply.numeric.confnum.n_section = 3
#Adimensional minim radius of integration. where criterion mass convergence will be performance
ply.numeric.confnum.r_min_int = 0.0


#========================================================================================
#		MAKING THE EARTH
#========================================================================================
#Creating the planet earth
earth = ply.data.planet( M=1.0, R=1.0, name='earth', urvec=np.linspace( 0.0,1.0,200 )  )
#earth.resetinterp()
#Earth with two layers
CMF = 0.33		#Core Mass Fraction
Rc = 0.55		#Guess of inner core radius
earth.comp = [\
{'comp':'Fe08FeS02',	'MF':CMF,	'Rini':0.0, 	'Rend':Rc,	'EOS':'Vinet',	'criterion':'Radius'},
{'comp':'pv_fmw',	'MF':1-CMF,	'Rini':Rc,	'Rend':1.0, 	'EOS':'Vinet',	'criterion':'Mass'}]

#Creating the real planet earth based upon PREM data
earth_prem = ply.data.planet( )
#Load prem data
earth_prem.load( filename = 'prem', fmt=['ur','-','rho','P','g','mr'] )


#========================================================================================
#		INTEGRATION OF THE EARTH INTERIOR
#========================================================================================
#If you want to update the planet radius after the integration
earth.structure( update = 'radius' )
#If you want to update the planet mass after the integration
#earth.structure( update = 'mass' )

   
#========================================================================================
#		RESULTS
#========================================================================================
#Saving results
earth.save()

plt.figure( figsize = (10,10) )
#Mass
plt.subplot(221)
plt.plot(earth_prem.R*earth_prem.urvec, earth_prem.mrvec,'o-',label='PREM')
plt.plot(earth.R*earth.urvec, earth.mrvec,label='Plynet',linewidth = 2,color = 'red')
plt.xlabel( 'r [$R_{\oplus}$]' )
plt.ylabel( 'M [Kg]' )
plt.legend(loc = "upper left")
plt.grid()
#Density
plt.subplot(222)
plt.plot(earth_prem.R*earth_prem.urvec,earth_prem.rhovec/1000.,'o-')
plt.plot(earth.R*earth.urvec,earth.rhovec/1000.,linewidth = 2,color = 'red')
plt.xlabel( 'r [$R_{\oplus}$]' )
plt.ylabel( 'Density $\\rho$ [$\\times 10^3$ kg/m$^3$]' )
plt.grid()
#Pressure
plt.subplot(223)
plt.plot(earth_prem.R*earth_prem.urvec,earth_prem.Pvec*1e9,'o-')
plt.plot(earth.R*earth.urvec,earth.Pvec,linewidth = 2,color = 'red')
plt.xlabel( 'r [$R_{\oplus}$]' )
plt.ylabel( 'Pressure P [Pa]' )
plt.grid()
#Gravity
plt.subplot(224)
plt.plot(earth_prem.R*earth_prem.urvec,earth_prem.gvec,'o-')
plt.plot(earth.R*earth.urvec,earth.gvec,linewidth = 2,color = 'red')
plt.xlabel( 'r [$R_{\oplus}$]' )
plt.ylabel( 'Gravity g [m/s$^2$]' )
plt.grid()

plt.savefig("EarthProfiles.png")
plt.close('all')