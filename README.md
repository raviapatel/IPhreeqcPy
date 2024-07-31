# IPhreeqcPy

[IPhreeqcPy](https://github.com/raviapatel/IPhreeqcPy) provides a wrapper to communicate with [IPhreeqc](http://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc/) in [python](https://www.python.org/). It is an alternative to [PhreeqPy](http://www.phreeqpy.com/) and is derived from PhreeqcPy. One of the drawback of PhreeqcPy was that it used pythonic names spaces for IPhreeqc function calls which made Phreeqpy function calls different from IPhreeqc and has IPhreeqc manual couldnot be referred to. Secondly it did not have automated compilation for IPhreeqc during installation. As PhreeqPy is an open source I took further liberty to address this issue and redistribute it as IPhreeqcPy to avoid conflicts with development of PhreeqPy. Moreover more Iphreeqc function calls are included in
IPhrereqcPy e.g. function calls related to dump which can be of use while restarting simulations.

## Developer

Ravi A. Patel

## Contact me

email (personal): <ravee.a.patel@gmail.com>

## Citation

If you are using
IPhreeqcPy for academic
work please cite this manual and
IPhreeqcPy repository in
your publications. Below is the bibtex format for citing IPhreeqcPy
    @manual{Patel2024, 
    title  = "IPhreeqcPy a python wrapper for IPhreeqc",
    author = "Ravi Patel", 
    url    = "https://github.com/raviapatel/IPhreeqcPy",
    year   = "2024 (accessed July 31, 2024)"  
    }

## Hosted at

Source code is hosted on
[GitHub](https://github.com/raviapatel/IPhreeqcPy) 

## Installation

    pip install IPhreeqcPy

for installation for source read the documentation

## Detailed Documentation

For documentation visit <http://raviapatel.bitbucket.org/IPhreeqcPy/>

## License and Terms of use

IPhreeqcPy is a free
software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software
Foundation, version 3 of the License. This program is distributed in the
hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details. You should
have received a copy of the GNU Lesser General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.