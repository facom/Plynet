#!/usr/bin/env python
# -*- coding: utf-8 -*-
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#	PHYSICS MODULE
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

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
confphys=loadconf("magneticrc")


#========================================================================================
#		MODULE COMPATIBILITY
#========================================================================================
from plynet.numeric import *
from plynet.data import *

#========================================================================================
#		ROUTINES
#========================================================================================
