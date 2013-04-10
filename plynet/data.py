#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################
#	DATA MODULE
#########################################################################################

#========================================================================================
#		IMPORTS
#========================================================================================
from plynet import *


#========================================================================================
#		MODULE COMPATIBILITY
#========================================================================================
from plynet.mechanic  import *
from plynet.numeric   import *


#========================================================================================
#		PLANET CLASS
#========================================================================================
class planet(object):
    """Planet class
    
    Attributes
    ----------
    name: string
    Planet name. Default 'planet'
    
    R: double
    Planet Radius. Default 1.0, Units Earth Radius.

    M: double
    Planet Mass. Default 1.0, Units Earth Mass.

    comp: list
    Different planet shells from surface to nucleus with its composition, equation of state, and mass fraction
    Default [{'comp':'Fe','MF':0.4,'RL':0.0,'EOS':'BM3'},{'comp':'pv_fmw','MF':0.6,'RL':0.0,'EOS':'BM3'}]
    
    urvec: list
    List with radius where the propierties will be evaluated. Default np.linspace(0.,1.,100) adimensional
    
    Tvec: list
    List with initial temperature profile, according to urvec. Default np.linspace(6000,300,100) K
    
    """
    #************************************************************************************
    #	ATTRIBUTES
    #************************************************************************************
    #General properties
    name = "'planet'"
    state="int(0)"
    M = '1.0'
    R = '1.0'
    
    #Environmental properties
    a="float(1.0)"#AU
    environment="None"
    
    #Internal vectors (with boundary conditions)
    urvec="[0.,1.]"		#Adimensional points for values evaluate
    Tvec="[5000,300]"		#K
    mrvec="[0.0,1.0]"		#MT
    rhovec="[11000,4000]"	#kg/m3
    phivec="[0.0,-6.689629e+07]"#m^2/s^2
    Pvec="[1E11,0.0]"		#Pa
    gvec="[0,9.8]"		#m/s2
    cvec="[0,1]"		#Integer
   
    #Composition
    comp = "[\
    {'comp':'Fe',    'MF':0.4,'Rini':0.0, 'Rend':0.33,'EOS':'Vinet','criterion':'-'},\
    {'comp':'pv_fmw','MF':0.6,'Rini':0.33,'Rend':1.0, 'EOS':'Vinet','criterion':'Radius'}]"
    
    #Interpolant functions
    mr="None"
    rho="None"
    P="None"
    T="None"
    g="None"
    phi="None"
    c="None"
    
    #Other attributes
    funcs="['mr','rho','P','g','phi','T']"
    interptype="'linear'"
    
    #************************************************************************************
    #	METHODS
    #************************************************************************************
    def __init__(self,**kwargs):
	#Set attributes using: default and argument values
        updatedic(self.__dict__,planet.__dict__,**kwargs)
        
	#Set planet environment
        if self.environment is None:
            self.environment=planetary_system()
            
	#Set global properties
        if self.M is None:
            self.M=self.mrvec[-1]
        else:
            self.mrvec[-1]=self.M
        #Set properties vector according to urvec
        if len(self.urvec)>2:
            for func in self.funcs+['c']:
                if len(self.__dict__["%svec"%func])==2:
                    ini=self.__dict__["%svec"%func][0]
                    end=self.__dict__["%svec"%func][-1]
                    self.__dict__["%svec"%func][1:-1]=[ini]*(len(self.urvec)-2)
                    self.__dict__["%svec"%func][0]=ini
                    self.__dict__["%svec"%func][-1]=end
        #Verify size of property vectors
        lu=len(self.urvec)
        for func in self.funcs:
            if func=='urvec':continue
            lp=len(self.__dict__["%svec"%func])
            if lp!=lu:
                error("Property vector '%s' has a length (%d) different than urvec (%d)"%(func,lp,lu))
        #Set interpolant functions
        self.resetinterp()
        
        
    #Save function#......................................................................
    def save(self,**kwargs):
        """Save planet information

	@brief A function to save all physical profiles of the planet interior

        Parameters:
        ----------
        suffix: string
           Suffix for file.  Default 'state'
           
        dir: string
           Directory where to store data

        qheader: boolean
           Do you want to store header?.  Default True.
        
        Returns:
        -------
        fileplanet: string
           File where planet was saved.

        Examples:
        --------
        >> planet().save(dir='tmp')
        'tmp/planet-state000.dat'
        
        """
        suffix=kwargs.get('suffix','state')
        dir=kwargs.get('dir','.')
        qheader=kwargs.get('qheader',True)
        
        filestate="%s/%s-%s%s.dat"%(dir,self.name,suffix,"%03d"%self.state)
        verbose("Saving planet '%s' state %d in '%s'"%(self.name,self.state,filestate))
        fs=open(filestate,"w")
        self.state+=1
    
        #HEADER
        if qheader is True:
            header=""
            for attr in np.sort(self.__dict__.keys()):
                if ("__" in attr) or ('function' in `type(self.__dict__[attr])`)\
                or ('interp1d' in `type(self.__dict__[attr])`) or \
                isinstance(self.__dict__[attr],(list,np.ndarray)) or attr=="environment":continue
                
                val=self.__dict__[attr]
                if isinstance(val,(float,np.double,int,list,np.ndarray,tuple,dict)):
                    val=val
                else:
                    val="%s"%str(val)
                header+="#%s="%attr+`val`+"\n"
                
            #Composition
            header+="#composition\n"
            for layer in xrange(0,len(self.comp)):
                header+="#layer%d"%layer + "\t\t%s"%self.comp[layer]['comp'] + "\t\t%f\n"%self.comp[layer]['MF']
                
            header+="#Cols=\n #'ur\t\tr\t\tmr\t\trho\t\tP\t\tg\t\tphi\t\tT\t\tcomposition'\n"
            header+="#-end-"
            print >>fs,header
        
        #CONTENT
        Y=self.getprofile(self.urvec)
        np.savetxt(fs,Y,fmt="%e\t%e\t%e\t%e\t%e\t%e\t%e\t%e\t%d")
        fs.close()
        
        return filestate


    #Strcuture function#.................................................................
    def structure(self,R=None,mphi = False):
        """Internal calculations of planet structure

        Parameters:
        ----------
        R: radius of planet
            Guess of radius of planet. Default planet.R

        Returns:
        -------
        self: planet
           Returns the planet with its new properties. Its real radius
           and its profiles of propierties.

        Examples:
        --------
        >>> planet().structure()
        >>> print planet().urvec, planet().Tvec, planet().mrvec

        """
	#Guess Radius
        R_tmp = self.R
        if R!=None:
            R_tmp = R

	#Increment for n-section optimization code
	increment = R_tmp/confnum.n_section**2
	#R_min of integration
	r_min = confnum.r_min_int
	#Reset of temperature
	self.resetinterp('T')
	
	i = 0
	#Loop residual mass condition
	while True:
	    #Integration of eoe
	    self, signal = strprofile(self, R=R_tmp)
	    
	    no_mrc = False
	    if i > confnum.n_max_mr:
		no_mrc = True

	    #residual mass approximatte (adimensional)
	    m_res = abs(4*np.pi*self.rho(r_min)*(r_min*self.R*confmech.R_SI)**3\
	    /(3*self.M*confmech.M_SI))
	    mr_error = abs(m_res-self.mr(r_min)/self.M)
	    print R_tmp , mr_error
	    #criterion of residual mass convergence
	    if( signal == False and mr_error <= confnum.accuracy_mr ) or no_mrc:
				
		if no_mrc:
		    print 'WARNING: Maxim number of step achieved in residual mass'
		    print ' condition.\n  Last residual error was %f'%mr_error
		    
		self.R = R_tmp
		break
		
	    #Mass Convergence Algoritm (general bisection)
	    if signal:
		R_tmp -= increment
		increment *= 1./confnum.n_section
		R_tmp += increment
		temp_signal = False
	    else:
		R_tmp += increment
		temp_signal = False
	    i += 1
	if mphi == True:
	    self.make_phi()
        return self


    def make_phi(self):
	"""Make potential function
        
        Parameters:
        ----------
        
        Returns:
        -------
        self: planet with new potential

        Examples:
        --------

	>> planet().make_phi()

        """
	phi1 = lambda r:-4*np.pi*mechanic.confmech.G*(self.R*mechanic.confmech.R_SI)**2*\
	integ.quad( lambda r1:( self.rho(r1)*r1 ), r, 1.0, full_output = 1 )[0]

	phi2 = lambda r:-4*np.pi*mechanic.confmech.G*(self.R*mechanic.confmech.R_SI)**2*\
	1/r*integ.quad( lambda r1:( self.rho(r1)*r1**2 ), 0, r, full_output = 1 )[0]

	self.phivec=[]
	for r in self.urvec:
	    self.phivec.append( phi1(r)+phi2(r) )
	self.phivec[0] = phi1(0)
	self.resetinterp(['phi'])
	return self


    #Reset interpolants..................................................................
    def resetinterp(self,funcs=None):
        """Reset interpolant functions
        
        Parameters:
        ----------
        funcs: list of strings
           List of func names to reset.  Default None (all funcs. are
           reset)

        Returns:
        -------
        self: planet with new interpolations

        Examples:
        --------

        >> planet().resetinterp()
        ['mr', 'rho', 'P', 'g', 'T', 'phi']

        >> planet().resetinterp(['mr','T'])
        ['mr', 'T']

        """
        if funcs is None:funcs=self.funcs
        for func in funcs:
            debug("Initializing interpolant function %s..."%func)
            exec("self.%s=interp(self.urvec,self.%svec,kind=self.interptype)"%(func,func))

        return funcs


    #Composition function................................................................
    def c(self,ur):
        """Composition function
        
        Parameters:
        ----------
        ur: radius
            list of radios to be evaluated, composition
           
        Returns:
        -------
        comp: list with number according to composition

        Examples:
        --------
        >> planet().c(1.0)
        1
        """
        if isinstance(ur, (np.double, float, np.ndarray, list)):
            if isinstance(ur, (np.double, float)):
                ur = [ur]
            comp=[]
            for r in ur:
                for layer in xrange(0,len(self.comp)):
                    if r<=self.comp[layer]['Rend']:
                        comp.append(layer)
                        break
                        
            if len(comp)==1:
                return comp[0]
            else:
                return comp
                
        else:
            return 0


    #Load a planet.......................................................................
    def load(self,**kwargs):
        """Load a planet profile

        Parameters:
        ----------
        filename: string
           Name of file that contain the properties.  Default 'Planet_state000'
           
	dir: string
           Directory where file are
           
        qheader: boolean
           Do you want to load header?.  Default False.
           
	fmt: format
	   Format of file, order of properties. Default ['ur','r','mr','rho','P','g','T','c']
	   '-' if column isn't important
        
        Returns:
        -------
        fileplanet: string
           File where planet was saved.

        Examples:
        --------
        >>> planet().load(filename='venus',fmt=['ur','T','mr','g','P','rho'])   
        """
        filename = kwargs.get('filename','%s-state000'%self.name)
        dir = kwargs.get('dir','.')
        qheader = kwargs.get('qheader',True)
        fmt = kwargs.get('fmt',['ur','r','mr','rho','P','g','phi','T','c'])
        
        filestate="%s/%s.dat"%(dir,filename)
        fs=np.transpose(np.loadtxt(filestate))
        
        #HEADER
        
        #CONTENT
        i = 0
        for prop in fmt:
	    if prop == 'r':
		self.urvec=fs[i]/(fs[i,-1])
		self.R = fs[i,-1]
	    if prop in self.funcs+['ur']+['c']:
		exec 'self.%svec=fs[%d]'%(prop,i)
		if prop == 'mr':
		    self.M = self.mrvec[-1]
	    i += 1
	
        return 0
  

    #Get planet profile..................................................................
    def getprofile(self,ur=None):
        """Get profile of a planet

        Parameters:
        ----------
        r: ndarray
           Array of rs where one wants to obtain the properties.

        Returns:
        -------
        Y: list of ndarrays 
           List of ndarrays containing values of 

        Examples:
        --------
        >> planet().getprofile([0.0,0.5,1.0])
        """
        if ur is None:
            ur=self.urvec
        ur=np.array(ur)
        Y=np.transpose(
            np.vstack(
                (ur,
                 ur*self.R,
                 self.mr(ur),
                 self.rho(ur),
                 self.P(ur),
                 self.g(ur),
                 self.phi(ur),
                 self.T(ur),
                 self.c(ur)
                 )
                )
            )
        return Y

    def property(self,prop):
        properties={'ur':0,'r':1,'mr':2,'rho':3,'P':4,'g':5,'phi':6,'T':6,'c':7}
        return properties.get(prop,0)


#========================================================================================
#		TEST MODULE
#========================================================================================
def test_planet_init():
    #Simple definition
    p=planet(name='simple1')
    p.save(dir='tmp')
    print "Simple definition:simple1"
    #Definition with attributes
    p=planet(name='simple2',M=2.0,f={'cmf':0.5,'mmf':0.5})
    p.save(dir='tmp')
    print "Definition with attributes:simple2"
    #Definition setting temperature profile vectorially
    p=planet(name='simple3',Tvec=[2000,100])
    p.save(dir='tmp')
    print "Definition with temperature vector:simple3"
    #Definition with custom profile
    ur=np.linspace(0.0,1.0,10)
    def T(ur):
        return 6000*(1-ur**2)
    p=planet(name='simple4',urvec=ur,Tvec=T(ur))
    p.save(dir='tmp')
    print "Simple definition:simple4"
    
def test_getprofile():
    #Simple profile
    p=planet()
    print "Planet simple profile:\n"
    ur=np.linspace(0.0,1.0,5)
    print p.getprofile(ur)    
