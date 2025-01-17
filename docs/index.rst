IPhreeqcPy
========== 
.. _PhreeqPy: http://www.phreeqpy.com/
.. _IPhreeqc: http://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc/
.. _IPhreeqcPy: https://github.com/raviapatel/IPhreeqcPy
.. _GitHub: https://github.com/raviapatel/IPhreeqcPy
.. _python: https://www.python.org/

`IPhreeqcPy`_  provides a wrapper to communicate with `IPhreeqc`_ in `python`_. It is an alternative to `PhreeqPy`_ and is derived from `PhreeqPy`_. One of the drawback of `PhreeqPy`_ was that it used pythonic names spaces for `IPhreeqc`_  function calls which made `PhreeqPy`_ function calls different from `IPhreeqc`_. Secondly it did not have automated compilation for `Iphreeqc`_  during installation. As `PhreeqPy`_ is an open source I took further liberty to address this issue and redistribute it as `IPhreeqcPy`_ to avoid conflicts with development of `PhreeqPy`_. Moreover more Iphreeqc function calls are included in `IPhreeqcPy`_ e.g. function calls related to dump which can be of use while restarting simulations.

Developer
++++++++++

Ravi A. Patel

email: ravee.a.patel@gmail.com


Citation
++++++++

If you are using `IPhreeqcPy`_ for academic work please cite this manual and `IPhreeqcPy`_ repository  in your publications. Below is the bibtex format for citing `IPhreeqcPy`_

::

    @manual{Patel2024, 
    title  = "IPhreeqcPy a python wrapper for IPhreeqc",
    author = "Ravi Patel", 
    url    = "https://github.com/raviapatel/IPhreeqcPy",
    year   = "2024 (accessed July 31, 2024)"  
    }

 

Hosted at
+++++++++

Source code is hosted on `GitHub`_ .


License and Terms of use
++++++++++++++++++++++++

`IPhreeqcPy`_ is a free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, version 3 of the License.   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details. You should have received a copy of the GNU Lesser General Public License along with this program.  If not, see `<http://www.gnu.org/licenses/>`_.


Contents:
+++++++++

.. toctree::
   :maxdepth: 1

   install
   example
   iphreeqc

	
Indices and tables
++++++++++++++++++

* :ref:`genindex`
* :ref:`search`

