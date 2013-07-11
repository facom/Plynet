#!/usr/bin/env python
"""Distutil setup
Project PLYNET
"""
#========================================================================================
#IMPORTS
#========================================================================================
from distutils.core import setup
from distutils.extension import Extension


#========================================================================================
#SETUP
#========================================================================================
setup(
    name		=	'plynet', 
    version		=	'1.0',
    packages		=	['plynet','plynet.conf'],
    author		=	"Sebastian Bustamante, Jorge Zuluaga",
    author_email	=	"macsebas33@gmail.com",
    maintainer		=	"Sebastian Bustamante, Jorge Zuluaga",
    maintainer_email	=	"macsebas33@gmail.com",
    contact		=	"Sebastian Bustamante",
    contact_email	=	"macsebas33@gmail.com",
    license		=	"Academic Free License v3.0",
    description		=	"Package to simulate physics interior of rocky planets",
    long_description	=	open('README.md').read(),
    keywords		=	"Planetary systems: physical evolution",
    url			=	"https://github.com/facom/Plynet/tree/1.0-release",
    download_url	= 	"https://github.com/facom/Plynet/archive/1.0-release.zip",
    classifiers		=	["Programming Language :: Python",
				("Topic :: Scientific/Engineering"),
				("Intended Audience :: Science/Research"),
				("License :: OSI Approved :: Academic Free License v3.0 (AFLv3)"),
				("Operating System :: OS Independent"),
				("Environment :: Console"),
				],

    install_requires=['numpy','scipy']);