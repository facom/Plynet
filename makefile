#####################################################################
# PLYNET, https://github.com/sbustamante/Plynet/archive/master.zip
#####################################################################
#
# Copyright (C) 2013 S. Bustamante, Jorge I. Zuluaga
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the Academic Free License (AFL) version 3.0.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
# You should have received a copy of the Academic Free License along
# with this program; if not an online version is available at
# http://www.opensource.org/licenses/afl-3.0.php
#
#####################################################################
# PROJECT MAKEFILE
#####################################################################
PACKAGE=plynet
INSTALL_DIR=$(HOME)/usr
PACKAGE_DIR=$(INSTALL_DIR)/lib/python2.6/site-packages/$(PACKAGE)
TEST_CMD=nosetests $(TEST_OPT) --with-doctest --doctest-tests

install:
	python setup.py install --prefix=$(INSTALL_DIR)
	python -c"import plynet"

gendist:
	python setup.py sdist

edit:
	emacs -nw Project plynet/*.py plynet/conf/*rc.py 

editkate:
	kate plynet/*.py plynet/conf/*rc.py &

clean:
	find . -name *~ -exec rm -rf {} \;
	make -C plynet clean
	make -C examples clean

cleanall:clean
	rm -rf build
	rm -rf tmp/*
	rm -rf $(PACKAGE_DIR)

testall:test testdata testnumeric testthermal testmagnetic testmechanic

test:test$(PACKAGE) testdata testnumeric testthermal testmagnetic testmechanic

test$(PACKAGE):
	$(TEST_CMD) $(PACKAGE)

testdata:
	$(TEST_CMD) $(PACKAGE).data

testnumeric:
	$(TEST_CMD) $(PACKAGE).numeric

testthermal:
	$(TEST_CMD) $(PACKAGE).thermal

testmagnetic:
	$(TEST_CMD) $(PACKAGE).magnetic

testmechanics:
	$(TEST_CMD) $(PACKAGE).mechanic