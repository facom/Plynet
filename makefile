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
PACKAGE		=	Plynet
VERSION		=	1.0-release
PYTHON 		=	python2.6 
INSTALL_DIR	=	$(HOME)/usr
PACKAGE_DIR	=	$(INSTALL_DIR)/lib/$(PYTHON)/site-packages/$(PACKAGE)
TEST_CMD	=	nosetests $(TEST_OPT) --with-doctest --doctest-tests
EDITOR		=	kate
DOC_DIR		=	./doc

install:
	$(PYTHON) setup.py install --prefix=$(INSTALL_DIR)
	$(PYTHON) -c"import plynet"

documentation:
	doxygen $(DOC_DIR)/config.dox

gendist:
	$(PYTHON) setup.py sdist

edit:
	$(EDITOR) plynet/*.py plynet/conf/*rc.py 

clean:	
	find . -name *~ -exec rm -rf {} \;
	make -C plynet clean
	make -C examples clean

cleanall:clean
	rm -rf build
	rm -rf tmp/*
	rm -rf $(PACKAGE_DIR)

testall:test testdata testnumeric testmechanic

test:test$(PACKAGE) testdata testnumeric testmechanic

test$(PACKAGE):$(TEST_CMD) $(PACKAGE)

testdata:$(TEST_CMD) $(PACKAGE).data

testnumeric:$(TEST_CMD) $(PACKAGE).numeric

testmechanics:$(TEST_CMD) $(PACKAGE).mechanic

help:
	@echo -e 'Makefile Help: ($(PACKAGE) $(VERSION))'
	@echo -e '\tmake cleanall\t\tdelete all previous installation, including documentation'
	@echo -e '\tmake install\t\tinstall $(PACKAGE) $(VERSION)'
	@echo -e '\tmake help\t\tthis help'
	@echo -e '\tmake version\t\tcurrent $(PACKAGE) version'
	@echo -e '\tmake documentation\tgenerate the doxygen documentation'
	@echo -e '\tmake edit\t\tedit the code with $(EDITOR)'

version:
	@echo -e '$(PACKAGE) $(VERSION)'