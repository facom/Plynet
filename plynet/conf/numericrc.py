#!/usr/bin/env python
# -*- coding: utf-8 -*-
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#	CONFIGURATION FILE OF NUMERIC MODULE
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
signature='numeric'

#========================================================================================
#Integrator Configurations
#========================================================================================
scheme = 'rk4'			#Scheme of integration
h_step = 1./150			#Adimensional integration step

#========================================================================================
#Find Root Configurations
#========================================================================================
accuracy_mr = 1e-10		#Error in residual mass for total radius optimization
n_section = 2			#Number of bisection for total radius optimization
n_max_mr = 40			#Maxim Number of iteration for radius optimization code
r_min_int = 0.05		#Adimensional minim radius of integration. where 
				#criterion mass convergence will be performance

#========================================================================================
#Temperature Convergence Configurations
#========================================================================================
n_max_tmp = 20			#Maxim Number of iteration for temperature convergence
accuracy_temp = 0.1/100.        #Error max in the temperature for every r
