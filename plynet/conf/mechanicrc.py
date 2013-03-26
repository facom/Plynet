#!/usr/bin/env python
# -*- coding: utf-8 -*-
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#	CONFIGURATION FILE OF MECHANICS MODULE
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
signature='mechanic'


#========================================================================================
#EOS Parameters
#========================================================================================

#Vinet EOS ------------------------------------------------------------------------------

#CORE ...................................................................................
prop_Vinet_Fe={ 
		     'rho0'  : 8300.,
		     'K0'    : 164.8e9,
		     'K0p'   : 5.33,
		     'gamma0': 1.36,
		     'q'     : 0.91,
		     'theta0': 998,
		     'n'     : 17.90510295434198746643,
		     'Cp'    : 850.,
		     'alpha' : 1.16475E-5}
		     
prop_Vinet_FeS={ 
		     'rho0'  : 5330.,
		     'K0'    : 126e9,
		     'K0p'   : 4.8,
		     'gamma0': 1.36,
		     'q'     : 0.91,
		     'theta0': 998,
		     'n'     : 17.90510295434198746643,
		     'Cp'    : 850.,
		     'alpha' : 1.16475E-5}

prop_Vinet_Fe08FeS02={ 
		     'rho0'  : 7171.0,
		     'K0'    : 150.2E9,
		     'K0p'   : 5.675,
		     #'gamma0': 1.36,
		     'gamma0': 2.06,
		     'q'     : 0.91, 
		     'theta0': 998.0,
		     'n'     : 17.90510295434198746643,
		     'Cp'    : 850.,
		     'alpha' : 1.16475E-5}
		
#MANTLE .................................................................................
prop_Vinet_pv_fmw={  
		     'rho0'  : 4152.,
		     'K0'    : 223.6e9,
		     'K0p'   : 4.274,
		     'gamma0': 1.48,
		     'q'     : 1.4,
		     'theta0': 1070,
		     'n'     : 58.46107077297227776024,
		     'Cp'    : 1250.,
		     'alpha' : 1.7329E-5}
		     
prop_Vinet_ol={ 
		     'rho0'  : 3347.,
		     'K0'    : 126.8e9,
		     'K0p'   : 4.274,
		     'gamma0': 0.99,
		     'q'     : 2.1,
		     'theta0': 809,
		     'n'     : 58.46107077297227776024,
		     'Cp'    : 1250.,
		     'alpha' : 1.7329E-5}
		     
		     
prop_Vinet_Free={ 
		     'rho0'  : 0.,
		     'K0'    : 0.,
		     'K0p'   : 0.,
		     'gamma0': 0.,
		     'q'     : 0.,
		     'theta0': 998.0,
		     'n'     : 17.90510295434198746643,
		     'Cp'    : 850.,
		     'alpha' : 1.16475E-5}
		     
#========================================================================================
#General constants
#========================================================================================
# Constante de los gases y de Cavendish
G=6.67e-11
#Rg=8.314472
RG=8.31451

#Earth mass in SI units
M_SI = 5.98e24          
#standar pressure (convention)
P_SI = 1e12
#Earth radius in SI units
R_SI = 6.37e6
# Normalization Temperature
T_Norm = 1e3
