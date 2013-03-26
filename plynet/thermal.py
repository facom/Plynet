#!/usr/bin/env python
# -*- coding: utf-8 -*-
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#	THERMAL MODULE
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#========================================================================================
#		IMPORTS
#========================================================================================
from plynet import *

#========================================================================================
#		MODULE CONFIGURATION
#========================================================================================
confth=loadconf("thermalrc")

#========================================================================================
#		MODULE COMPATIBILITY
#========================================================================================
from plynet.numeric import *
from plynet.data import *

#========================================================================================
#		ROUTINES
#========================================================================================




#========================================================================================
#		TEST MODULE
#========================================================================================

def test_config_thermal():
    print confth.signature

def test_temprofile(p):
    print eot_conv(800, 0.8,p)
    print eot_cond(1000,0.5,p)
    print confth.alpha
    print physics.confphys.R_SI
