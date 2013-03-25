PLYNET
Python Planetary Physics Package
================================================================================

User Installation (Read-Only version)
................................................................................
Download the tarball of the package from GitHub:

   https://github.com/sbustamante/Plynet/tarball/master
................................................................................


Developer Installation (Read-Write version)
................................................................................
Download the tarball of the package from GitHub:

   https://github.com/sbustamante/Plynet/tarball/master

Initialize git version

   $ git init

Link the git proyect

   $ git remote add origin git@github.com:facomdev/PLYNET.git

Link with 'master' branch

   $ git push -u origin master

[ In this step is necessary create a personal ssh key, for this, the user 
must add a new associated email direction, view github user-help ]

For commit

   $ git add <files>
   $ git commit -m 'commit message'
   $ git push -u origin master
................................................................................


To install package perform the following operations:

1) Create the directory usr/local in your home directory:
   
   mkdir -p $HOME/usr/local

2) Add the following line to your .bashrc:

   export PYTHONPATH=$PYTHONPATH:$HOME/usr/lib/python2.6/site-packages

Steps 1 and 2 must be followed only the first time your install.

3) Executes:
   
   make install

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