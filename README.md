PLYNET 1.0-release
==================
**Python Planetary Physics Package**

1.  [DESCRIPTION]
    (https://github.com/sbustamante/Plynet1.0-relaease#description)
2.  [USER VERSION (Read-Only version)]
    (https://github.com/sbustamante/Plynet1.0-relaease#user-version-read-only-version)
3.  [DEVELOPER VERSION (Read-Write version)]
    (https://github.com/sbustamante/Plynet1.0-relaease#developer-version-read-write-version)
4.  [PACKAGE INSTALLATION]
    (https://github.com/sbustamante/Plynet1.0-relaease#package-installation)
5.  [VERSION HISTORY]
    (https://github.com/sbustamante/Plynet1.0-relaease#version-history)
6.  [LICENSE]
    (https://github.com/sbustamante/Plynet1.0-relaease#license)


DESCRIPTION:
-----------------------------------------------------------------------------------------
*Plynet* is a free and object-oriented code in python to calculate physical 
properties of rocky planets. The aim of this proyect is to compile in just one code 
several algorithms commonly used in planetary sciences to compute mechanical, thermal 
and magnetic properties of planets. We make use of the OOP paradigm to make a versatile 
code that allows to work with many planets (grid) at time unlike the current private 
existing codes.


USER VERSION (Read-Only version):
-----------------------------------------------------------------------------------------
Download the zip file of Plynet in GitHub from 
[here.](https://github.com/sbustamante/Plynet/archive/master.zip)


DEVELOPER VERSION (Read-Write version):
-----------------------------------------------------------------------------------------
Plynet is a open source code, thus you can contribuite with us. With the next steps 
you can get a read-write version of *Plynet*


1.  Create the *Plynet* folder for your personal copy of the code.

        $ mkdir Plynet

2.  Initialize your local git repository

        $ git init

3.  Link with the github proyect

        $ git remote add origin git@github.com:sbustamante/Plynet.git

4.  Pull the proyect in your local copy

        $ git pull

5.  Finally, link with 'master' branch

        $ git push -u origin master

    *Before this step, the user must request to macsebas33@gmail.com to be
    added as collaborator of Plynet. It's also necessary create a personal ssh 
    key, for this, the user must add a new associated email direction, view github 
    [user-help](https://help.github.com/)*

6.  *(Optional)* If you want to push your changes in master branch of repository

        $ git add <files>
        $ git commit -m 'commit message'
        $ git push -u origin master


PACKAGE INSTALLATION:
-----------------------------------------------------------------------------------------
Once you had get a (user or developer) copy of Plynet, to install it perform the 
following operations:

1.  Create the directory usr/local in your home directory:
   
        $ mkdir -p $HOME/usr/local

2.  Add the following line to your .bashrc:

        $ export PYTHONPATH=$PYTHONPATH:$HOME/usr/lib/python2.6/site-packages

    *Steps 1 and 2 must be followed only the first time your install.*

3.  Executes:
   
        $ make install

* The installation ends with the command `"python -c'import plynet'"`.  If
  you don't see this command at the end of the last command, see if any
  language error has arosen.

* Otherwise if the command is executed but it show errors like:

To test all the package:
   
    $ make test

To test a given module executes:

    $ make test<module>

To clean all the package

    $ make clean


VERSION HISTORY:
-----------------------------------------------------------------------------------------
* Plynet 1.0-release:

  **Principal features**
  * A code with a completely oriented object structure. 
  * The class planet contains principal physical profile to work with rocky planetary
  interiors.
  * Different methods in class planet to load and save the physical profiles, allowing to 
  load precalculate planet interiors, like the PREM in the case of the earth, and saving
  the computed profiles.
  * Three integration schemes to compute the differential equation system of the planetary
  interior. RK4, Euler and the odestep functionality of scipy library.


LICENSE:
-----------------------------------------------------------------------------------------
This program is free software; you can redistribute it and/or modify it under the terms 
of the Academic Free License (AFL) version 3.0.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 

You should have received a copy of the Academic Free License along with this program; if 
not an online version is available [here.](http://www.opensource.org/licenses/afl-3.0.php)


-----------------------------------------------------------------------------------------
**Instituto de Fisica - FCEN - Universidad de Antioquia (C) 2013**

Sebastian Bustamante (macsebas33@gmail.com), Jorge Zuluaga