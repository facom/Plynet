PLYNET
======
**Python Planetary Physics Package**




DESCRIPTION:
------------
*Plynet* is a open source and object-oriented code in python to calculate physical 
properties of rocky planets. The aim of this proyect is to compile in just one code 
several algorithms commonly used in planetary sciences to compute mechanical, thermal 
and magnetic properties of planets. We make use of the OOP paradigm to make a versatile 
code that allows to work with many planets (grid) at time unlike the current private 
existing codes.




USER INSTALLATION (Read-Only version):
--------------------------------------
Download the zip file of Plynet in GitHub from 
[here.](https://github.com/sbustamante/Plynet/archive/master.zip)




DEVELOPER INSTALLATION (Read-Write version):
--------------------------------------------
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

    *In this step is necessary create a personal ssh key, for this, the user 
    must add a new associated email direction, view github user-help*

6.  *(Optional)* If you want to push your changes in master branch of repository

        $ git add <files>
        $ git commit -m 'commit message'
        $ git push -u origin master




PACKAGE INSTALLATION:
---------------------
Once you had get a (user or developer) copy of Plynet, to install it perform the 
following operations:

1.  Create the directory usr/local in your home directory:
   
        $ mkdir -p $HOME/usr/local

2.  Add the following line to your .bashrc:

        $ export PYTHONPATH=$PYTHONPATH:$HOME/usr/lib/python2.6/site-packages

    *Steps 1 and 2 must be followed only the first time your install.*

3.  Executes:
   
        $ make install

The installation ends with the command "python -c'import plynet'".  If
you don't see this command at the end of the last command, see if any
language error has arosen.

Otherwise if the command is executed but it show errors like:

To test all the package:
   
   make test

To test a given module executes:

   make test<module>

To clean all the package

   make clean

--------------------------------------------------------------------------------
Instituto de Fisica - FCEN - Universidad de Antioquia
(C) 2011 - Jorge Zuluaga, Sebastian Bustamante, Pablo Cuartas