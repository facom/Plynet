#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################
#	NUMERIC MODULE
#########################################################################################


#========================================================================================
#		IMPORTS
#========================================================================================
from plynet import *

#========================================================================================
#		MODULE CONFIGURATION
#========================================================================================
##Configuration parameters of numeric module
confnum=loadconf("numericrc")

#========================================================================================
#		ROUTINES
#========================================================================================
def odestep(odesys,Yini,t,h,**kwargs):
    """Compute one step of integration for odesys system, in time t

    Parameters:\n
    -------------------------------------------------------------------------------------\n
    odesys : function\n
	Differential equations of dynamics system\n
    Yini : array\n
	System state in time t\n
    t : float\n
	Current time of integration\n
    h : float\n
	Predeterminate time step\n
    kwargs : --\n
	Extra arguments\n
	    
    Returns:\n
    -------------------------------------------------------------------------------------\n
    Y : array\n
	System state in time t + h
       
    Examples:\n
    -------------------------------------------------------------------------------------\n
    >> import plynet.numeric as num\n
    >> def df(x,t): return 2*x\n
    >> f=num.odestep(df,1,1,0.1)\n
    
    """
    #Odeint scheme
    Tint=[t,t+h]
    if confnum.scheme=='odeint':
	Y = integ.odeint(odesys,Yini,Tint,args=(kwargs,),full_output = 1)[1]

    #Euler Scheme
    if confnum.scheme=='euler':
	Y = Yini + h*odesys( Yini,t,**kwargs )

    #RK4 Scheme:
    if confnum.scheme=='rk4':
	k1 = odesys( Yini	  , t	   , **kwargs )
	k2 = odesys( Yini+0.5*h*k1, t+0.5*h, **kwargs )
	k3 = odesys( Yini+0.5*h*k2, t+0.5*h, **kwargs )
	k4 = odesys( Yini+h*k3    , t+h    , **kwargs )
	
	Y = Yini + h*(k1+2*k2+2*k3+k4)/6

    return Y


#========================================================================================
#		TEST MODULE
#========================================================================================
def test_config_numeric():
    print confnum.signature