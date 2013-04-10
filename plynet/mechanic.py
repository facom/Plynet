#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################
#	MECHANICS MODULE
#########################################################################################

#========================================================================================
#		IMPORTS
#========================================================================================
from __future__ import division
from plynet import *
from scipy.integrate import quad
import matplotlib.pylab as plt
import os

#========================================================================================
#		MODULE CONFIGURATION
#========================================================================================
confmech=loadconf("mechanicrc")


#========================================================================================
#		MODULE COMPATIBILITY
#========================================================================================
from plynet.numeric import *
from plynet.data import *

#========================================================================================
#		ROUTINES
#========================================================================================

#****************************************************************************************
#Bulk Modulus
#****************************************************************************************
def Ks( rho, T, comp, typeEOS ):
    exec("prop = confmech.prop_"+typeEOS+"_"+comp)
    ks = 0.0
    if typeEOS=='Vinet':
	x = rho/prop['rho0']
	#Gruneinsen parameter
	gamma = prop['gamma0']*x**(-prop['q'])
	#Debye temperature
	debye = prop['theta0']*np.exp( (prop['gamma0'] - gamma)/prop['q'] )
	#Thermal expansion coefficient
	alpha = gamma*prop['Cp']*prop['rho0']/prop['K0']*1/(1+np.log(x))
	#alpha = prop['alpha']
	#Isothermal bluk modulus
	kt = prop['K0']*(1 + (1.5*(prop['K0p'] - 1)*x**(-1/3.) + 1)*(1 - x**(-1/3.)))*\
	x**(2/3.)*np.exp(1.5*(prop['K0p'] - 1)*(1 - x**(-1/3.)))
	#BM3
	#kt = 0.5*prop['K0']*(  ( 7* x**(7./3 )-5*x**(5./3 ) )*\
   	   #( 1+0.75*( prop['K0p']-4 )*( x**(2./3 )-1 ) ) +\
   	   #1.5*( x*x*x-x**(7./3 ) )*( prop['K0p']-4 ) )  
	#Auxiliar function
	fT = \
	(1-prop['q']-3*gamma)*T**4/debye**3*Integral(debye/T) \
	+3*debye*gamma*1/(np.exp(debye/T)-1)
	f0 = \
	(1-prop['q']-3*gamma)*300.**4/debye**3*Integral(debye/300.) \
	+3*debye*gamma*1/(np.exp(debye/300.)-1)
	#Themal correction
	Delta_Kt = 3*prop['n']*confmech.RG*gamma*rho*( fT-f0 )
	#Isobar Bulk modulus
	ks = kt*( 1+alpha*gamma*T )
	#print kt, alpha*gamma*T
    return ks

#Auxiliar function 1
def Integral( x ):
    return integ.quad( lambda z:z**3/(np.exp(z)-1), 0, x, full_output = 1 )[0]
    

#****************************************************************************************
#EOS Pressure
#****************************************************************************************
def rho_EOS( P, comp, typeEOS ):
    exec("prop = confmech.prop_"+typeEOS+"_"+comp)
    if typeEOS=='Vinet':
	#Isothermal Presssure
	rho = opt.zeros.bisect( P_Vinet, 0.001 , 10000000.0, args=(prop, P,) )*prop['rho0']
    return rho

#Auxiliar function 2
def P_Vinet( x, prop, P ):
    return 3*prop['K0']*x**(2/3.)*(1-x**(-1/3.))*np.exp(1.5*(prop['K0p'] - 1)*\
    (1 - x**(-1/3.))) - P
    
    
#****************************************************************************************
#Thermal expansion coefficient
#****************************************************************************************
def Alpha( rho, comp, typeEOS ):
    exec("prop = confmech.prop_"+typeEOS+"_"+comp)
    alpha = 0
    if typeEOS=='Vinet':
	gamma = Gamma( rho, comp, typeEOS )
	alpha = gamma*prop['Cp']*prop['rho0']/prop['K0']*1/(1+np.log(rho/prop['rho0']))
    return alpha


#****************************************************************************************
#Gruneinsen parameter
#****************************************************************************************
def Gamma( rho, comp, typeEOS ):
    exec("prop = confmech.prop_"+typeEOS+"_"+comp)
    gamma = 0
    if typeEOS=='Vinet':
	x = rho/prop['rho0']
	gamma = prop['gamma0']*x**(-prop['q'])
    return gamma


#****************************************************************************************
#Debye parameter
#****************************************************************************************
def Debye( rho, comp, typeEOS ):
    exec("prop = confmech.prop_"+typeEOS+"_"+comp)
    debye = 0
    if typeEOS=='Vinet':
	gamma = Gamma( rho, comp, typeEOS )
	debye = prop['theta0']*np.exp( (prop['gamma0'] - gamma)/prop['q'] )
    return debye


#****************************************************************************************
#Differential Equations of planet structure
#****************************************************************************************
def EOE(Y,r,**kwargs):  
    norm = kwargs.get('norm')
    layer_prop = kwargs.get('layer_prop')
    T = kwargs.get('T')
    
    M   = Y[0]*norm['M']*confmech.M_SI	         #dimensional mass SI
    rho = Y[1]*norm['rho']                       #dimensional density SI    
    g   = Y[2]*norm['g']                         #dimensional gravity SI    
    P   = Y[3]*norm['P']                         #dimensional pressure SI    
    rd  = abs(r)*norm['R']*confmech.R_SI     	 #dimensional radius SI
    
    #1-Mass
    dMdr = (4*np.pi)*rho*(rd**2)
    
    #2-Density
    Tp = T(0)
    if r>=0: Tp = T(r)
    ks = Ks( rho, Tp, layer_prop['comp'], layer_prop['EOS'] )
    drhodr = -rho**2*g/ks
    
    #3-Gravity
    dgdr = (4*np.pi*confmech.G*rho)-(2*confmech.G*M)/(rd**3)
    
    #4-Pressure
    dPdr = -rho*g
    
    return np.array([dMdr/(norm['M']*confmech.M_SI), drhodr/norm['rho'],\
    dgdr/norm['g'], dPdr/norm['P'] ])*norm['R']*confmech.R_SI
    
    
#****************************************************************************************
#	Integator of structure for a given planet radius 
#****************************************************************************************
def strprofile(p, R = 1.0):
    signal = False
    
    #Constants of normalization
    g = confmech.G*p.M*confmech.M_SI/(R*confmech.R_SI)**2
    p.norm = {\
    'M':1.0*p.mr(1.0), 'rho':1.0*p.rho(1.0),\
    'P':confmech.P_SI, 'g':g, 'R':1.0*R }

    #Initial conditions (adimensional)
    Y = np.array([ p.mr(1.0)/p.norm['M'], p.rho(1.0)/p.norm['rho'],\
    g/p.norm['g'], p.P(1.0)/p.norm['P']])

    i = 1
    layer = -1                   #initial layer
    MT = p.comp[layer]['MF']     #total mass layer
    p.comp[-1]['RL'] = 1.0       #radius of last layer
    Nh = int(1./confnum.h_step)	 #number of steps
    
    #reset of properties
    urvec = np.linspace(0.0, 1.0, Nh)
    p.mrvec = p.mr(urvec)
    p.rhovec = p.rho(urvec)
    p.Pvec = p.P(urvec)
    p.gvec = p.g(urvec)
    Mprev = 0

    #Integration (adimensional)
    for r in urvec[::-1]:
        p.mrvec[-i]  = Y[0]*p.norm['M']
        p.rhovec[-i] = Y[1]*p.norm['rho']
        p.gvec[-i]   = Y[2]*p.norm['g']
	p.Pvec[-i]   = Y[3]*p.norm['P']

        #Errors in mass integration (signal)
        if p.mrvec[-i]<0 or p.mrvec[-i]>p.M or \
        np.isnan(abs(p.mrvec[-i])) or np.isinf(abs(p.mrvec[-i])):
	    signal = True
	    #Reset of properties
	    urvec = p.urvec
	    p.urvec = np.linspace(0.0, 1.0, Nh)
	    p.resetinterp(['mr','rho','P','g'])
	    p.urvec = urvec 
	    p.mrvec = p.mr(p.urvec)
	    p.rhovec = p.rho(p.urvec)
	    p.Pvec = p.P(p.urvec)
	    p.gvec = p.g(p.urvec)    
	    #Problems of convergence for gravity in r=0
	    p.gvec[0] = 0.
	    return p, signal

	#Integration step
        Y=odestep(EOE, Y, r, -confnum.h_step, norm=p.norm, layer_prop=p.comp[layer], T=p.T )
        #Detection of layer
        if p.comp[layer]['criterion'] == 'Radius' and r < p.comp[layer]['Rini']:
	    p.comp[layer]['MF'] = 1 - Y[0] - Mprev
	    Mprev += 1 - Y[0]
            layer -= 1
            #New density value
            Y[1] = rho_EOS( p.Pvec[-i], p.comp[layer]['comp'], p.comp[layer]['EOS'] )/p.norm['rho']
            
            if layer == -len(p.comp):
		p.comp[layer]['MF'] = Y[0]

        if p.comp[layer]['criterion'] == 'Mass' and Y[0] <= 1 - p.comp[layer]['MF']:
	    Mprev += p.comp[layer]['MF']
	    p.comp[layer]['Rini'] = r
	    layer -= 1
	    #New density value
            Y[1] = rho_EOS( p.Pvec[-i], p.comp[layer]['comp'], p.comp[layer]['EOS'] )/p.norm['rho']
	    
            p.comp[layer]['Rend'] = r
            if layer == -len(p.comp):
		p.comp[layer]['Rini'] = 0.0
	i += 1
	
    #Problems of convergence for gravity in r=0
    p.gvec[0] = 0.
    
    #Reset of properties
    urvec = p.urvec
    p.urvec = np.linspace(0.0, 1.0, Nh)
    p.resetinterp(['mr','rho','P','g'])

    p.urvec = urvec 
    p.mrvec = p.mr(p.urvec)
    p.rhovec = p.rho(p.urvec)
    p.Pvec = p.P(p.urvec)
    p.gvec = p.g(p.urvec)    
    
    return p, signal