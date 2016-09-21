Installation 
============

Please follow the following instructions for installation

windows
+++++++

* Install cmake which can be downloaded from https://cmake.org/

* Make sure visual studio 2010 is installed which can be downloaded from https://www.microsoft.com/en-us/download/details.aspx?id=23507


* Open windows console and type following commands

.. code:: batch

	set path="C:\Program Files\CMake\bin";%PATH% #Includes CMake in search path
	pip install IPhreeqcPy

* If you want to install IPhreeqcPy in a specific location specify following additional directives  

.. code:: batch

	pip install --install-option="--prefix=*YOUR INSTALL PATH*" --ignore-installed IPhreeqcPy 
    

* To test installation type following in python console

.. code:: Python

	import IPhreeqcPy
	IPhreeqcPy.test()

* To upgrade your current installation type following in windows console

.. code:: batch

	set path="C:\Program Files\CMake\bin";%PATH% #Includes CMake in search path
	pip install --upgrade IPhreeqcPy

* To uninstall IPhreeqcPy type following in windows console

.. code:: bash
	
	pip uninstall IPhreeqcPy 

Linux
+++++

* Open linux terminal and type following

.. code:: bash

	sudo pip install IPhreeqcPy

* If you want to install IPhreeqcPy in a specific location specify following additional directives  

.. code:: bash

	pip install --install-option="--prefix=*YOUR INSTALL PATH*" --ignore-installed IPhreeqcPy 
    

* To test installation type following in python console

.. code:: Python

	IPhreeqcPy.test()

* To upgrade your current installation type following in linux terminal

.. code:: bash

	pip install --upgrade IPhreeqcPy

* To uninstall IPhreeqcPy type following in linux terminal

.. code:: bash
	
	pip uninstall IPhreeqcPy 
