#!/usr/bin/env python
# -*- coding: utf-8 -*-
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#	PACKAGE INITIALIZATION
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#========================================================================================
#		IMPORTS
#========================================================================================
import os,sys
import numpy as np
import scipy as sp
import scipy.interpolate as interpolate
import scipy.integrate as integ
import scipy.optimize as opt

#========================================================================================
#		ALIASES
#========================================================================================
"""Example: stop(), stop(1)"""
stop=sys.exit
"""Example: pause(), pause("Press enter to continue...")"""
pause=raw_input
"""Interpolant function generator"""
interp=interpolate.interp1d

#========================================================================================
#		ROUTINES
#========================================================================================
class dictobj(object):
    def __init__(self,dic={}):self.__dict__.update(dic)
    def __add__(self,other):
        self.__dict__.update(other.__dict__)
        return self

#Load configuration
def loadconf(filename):
    """Load configuration file

    Parameters:
    ----------
    filename: string
       Filename with configuration values.  Routine look for file in
       package directory with name filename.py and in the local
       directory with name .filename

    Returns:
    -------
    conf: dictobj
       Object with attributes as variables in configuration file

    Examples:
    --------
    >> loadconf('plynetrc')

    """
    d=dict()
    conf=dictobj()
    qfile=False
    filepath=os.path.dirname(os.path.abspath(__file__))
    #Read global file:
    globconf=filepath+"/conf/"+filename+".py"
    if os.path.lexists(globconf):
        execfile(globconf,{},d)
        conf+=dictobj(d)
        qfile=True
    #Read local file:
    localconf="."+filename
    if os.path.lexists(localconf):
        execfile(localconf,{},d)
        conf+=dictobj(d)
        qfile=True
    if qfile is False:
        print "No configuration file has been found (%s)."%globconf
    return conf

#Error routine
def error(msg='An error has occurred',code=1):
    """Display an error message and exit with an error code
    
    Parameters:
    ----------
    msg='An error has occurred':
        
    code=1:
        Exit code

    Examples:
    --------
    
    >> error(code=1)

    >> error("Failed test",code=123)

    """
    print >>sys.stderr,"Plynet Error (code %d): %s"%(code,msg)
    sys.exit(code)

#Debug routine
def debug(msg,out=sys.stderr,level=1):
    """Display a debug message
    
    Parameters:
    ----------
    msg:
       Custom message to display
     
    out=sys.stderr:
       Where the ouput will be redirected

    level=1:
       Debugging level.  Controlled by config.debuglevel
       configuration variable

    Examples:
    --------

    >>> debug("Debug message")

    """
    try:
        debuglevel=int(os.getenv('debuglevel'))

    except:
        try:debuglevel=config.debuglevel
        except:debuglevel=0

    if debuglevel>=level:
        print >>out,"**debug**:"+msg


#Obtain type of a var
def gettype(var):
    """Return the type of var

    Parameters:
    ----------
    var: any type
       Type to be tested

    Returns:
    -------
    type: type
       Type of var

    Examples:
    --------
    >>> gettype(3)
    <type 'int'>

    >>> gettype(None)
    <type 'int'>

    >>> gettype([1,2,3])
    <type 'list'>

    >>> gettype('Hello World')
    <type 'str'>

    """
    if var is None:return int
    else:return type(var)

#Update dictionary
def updatedic(dic,default,**kwargs):
    """Update dictionary using kwargs and default values in default dictionary
    
    Parameters:
    ----------
    dic: dictionart
       Dictionary to update

    default: dictionary
       Dictionary with default values to dic.  All the dict. entries
       must be strings with the form type(value)


    kwargs: dictionary
       New values

    Returns:
    -------
    Nothing

    Examples:
    --------
    See data.py for examples

    """

    for attr in default:
        if (isinstance(attr,str)) and ('__' not in attr) and ('function' not in `type(default[attr])`):
            if attr in kwargs:
                dic[attr]=kwargs[attr]
            else:
                exec("dic['%s']=%s"%(attr,default[attr]))

#========================================================================================
#LOAD CONFIGURATION
#========================================================================================
config=loadconf('plynetrc')

#========================================================================================
#TEST MODULE
#========================================================================================
def test_config():
    print config.signature

#========================================================================================
#OTHER MODULES
#========================================================================================
def verbose(msg,out=sys.stderr,level=1):
    """Verbose message
    """
    if config.verbose>=level:
        print >>out,msg

import data, mechanic, thermal, magnetic, numeric
