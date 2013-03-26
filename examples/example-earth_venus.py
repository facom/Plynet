# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import scipy as sp
import pylab as plt
import scipy.integrate as integ
import os

import plynet as ply

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#			EARTH_VENUS COMPARISON
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


#Creating the earth planet
earth = ply.data.planet()
earth.comp = [{'comp':'Fe', 'MF':0.33, 'RL':0.5, 'EOS':'BM3'},{'comp':'pv_fmw', 'MF':0.67, 'RL':1.0, 'EOS':'BM3'}]
#Integration of earth
earth.structure()


#Creating the venus planet
venus = ply.data.planet()   
#Load properties
venus.load(filename='venus',fmt=['ur','-','mr','rho','P','g','T','c'])

#=======================================================================
#Results
#=======================================================================

plt.title('Venus Earth density profiles')
plt.xlabel('r/Rp')
plt.ylabel('Density (units in surface density Earth)')
plt.plot(venus.urvec,venus.rhovec/earth.rho(1.0),label='Venus: Density profile')
plt.plot(earth.urvec,earth.rhovec/earth.rho(1.0),label='Earth: Density profile')
plt.savefig("Density.png")
plt.close('all')