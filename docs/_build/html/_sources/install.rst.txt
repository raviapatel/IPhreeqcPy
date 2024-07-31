Installation 
============

Prebuilt wheels are made available for Windows and Linux on PyPI. To install the latest version of IPhreeqcPy, simply run:

.. code:: bash

	pip install IPhreeqcPy

If you want to install IPhreeqcPy in a specific location, you can specify the `--prefix` option:

.. code:: bash

	pip install --install-option="--prefix=*YOUR INSTALL PATH*" --ignore-installed IPhreeqcPy

If you want to install a specific version of IPhreeqcPy, you can specify the version number:

.. code:: bash

	pip install IPhreeqcPy==*version name*

To test the installation, run the following in a Python console:

.. code:: Python

	import IPhreeqcPy
	IPhreeqcPy.test()

To upgrade your current installation, run the following in a terminal:

.. code:: bash

	pip install --upgrade IPhreeqcPy

To uninstall IPhreeqcPy, run the following in a terminal:

.. code:: bash

	pip uninstall IPhreeqcPy

If you want to install IPhreeqcPy from source, you can clone the repository and run the following command:

windows
+++++++

* Install cmake which can be downloaded from https://cmake.org/. After installing make sure that path to cmake.exe is added to *path* in Environment variable otherwise you will get error *cmake not found*

* Install visual studio 19 which can be downloaded from https://www.visualstudio.com/ or my preferred way is to install it through conda using following command

.. code:: console

	conda install -c conda-forge vs2019_win-64 

* After installing visual studio 2019 build IPhreeqcPy source using following command

.. code:: console

	python setup.py compile_phreeqc

* Once phreeqc is compiled install IPhreeqcPy using following command

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

* First build IPhreeqcPy source using following command

.. code:: console

	python setup.py compile_phreeqc

* Once phreeqc is compiled install IPhreeqcPy using following command

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
