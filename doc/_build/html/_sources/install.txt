Installation 
============

Please follow the following instructions for installation

windows
+++++++

* Install cmake which can be downloaded from https://cmake.org/. After installing make sure that path to cmake.exe is added to *path* in Environment variable otherwise you will get error *cmake not found*

* Make sure visual studio 2010 is installed which can be downloaded from https://www.microsoft.com/en-us/download/details.aspx?id=23507


* Open windows console and type following commands

.. code:: console

	pip install IPhreeqcPy

* If you want to install IPhreeqcPy in a specific location specify following additional directives  

.. code:: console

	pip install --install-option="--prefix=*YOUR INSTALL PATH*" --ignore-installed IPhreeqcPy 

* Specific version available in *PyPi* can be installed using following directives

.. code:: console

	pip install IPhreeqcPy==*version name* 
    

* To test installation type following in python console

.. code:: Python

	import IPhreeqcPy
	IPhreeqcPy.test()

* To upgrade your current installation type following in windows console

.. code:: console

	pip install --upgrade IPhreeqcPy

* To uninstall IPhreeqcPy type following in windows console

.. code:: console
	
	pip uninstall IPhreeqcPy 

Linux
+++++

* Open linux terminal and type following

.. code:: bash

	sudo pip install IPhreeqcPy

* If you want to install IPhreeqcPy in a specific location specify following additional directives  

.. code:: bash

	pip install --install-option="--prefix=*YOUR INSTALL PATH*" --ignore-installed IPhreeqcPy 
    
* Specific version available in *PyPi* can be installed using following directives

.. code:: bash

	pip install IPhreeqcPy==*version name* 

* To test installation type following in python console

.. code:: Python

	IPhreeqcPy.test()

* To upgrade your current installation type following in linux terminal

.. code:: bash

	pip install --upgrade IPhreeqcPy

* To uninstall IPhreeqcPy type following in linux terminal

.. code:: bash
	
	pip uninstall IPhreeqcPy 
