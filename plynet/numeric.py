#!/usr/bin/env python
# -*- coding: utf-8 -*-
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#	NUMERIC MODULE
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#========================================================================================
#		IMPORTS
#========================================================================================
from plynet import *

#========================================================================================
#		MODULE CONFIGURATION
#========================================================================================
confnum=loadconf("numericrc")

#========================================================================================
#		MODULE COMPATIBILITY
#========================================================================================

#========================================================================================
#		ROUTINES
#========================================================================================
def odestep(odesys,Yini,t,h,**kwargs):
    """Compute one step of integration for odesys system, in time t

    Parameters:
    ----------
    odesys: differential equations of dynamics system
    Yini: system state in time t
    t: actual time of integration
    h: predeterminate time step
    kwargs: extra arguments
	    
    Returns:
    -------
    Y: system state in time t + h
       
    Examples:
    --------
    >> import plynet.numeric as num
    >> #Integration of f'(x)=2x
    >> def df(x,t): return 2*x
    >> #Return function f value in x=1.1
    >> f=num.odestep(df,1,1,0.1)

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