#!/usr/bin/python
#>=============================================================================
#>IphreeqcPy a python wrapper for Iphreeqc
#>----------------------------------------------------------------------------- 
#>
#>Copyright (C) 2016  Ravi Patel
#
#>This program is free software: you can redistribute it and/or modify
#>it under the terms of the GNU Lesser General Public License as
#>published by the Free Software Foundation, version 3
#>This program is distributed in the hope that it will be useful, 
#>but WITHOUT ANY WARRANTY; without even the implied warranty of
#>MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#>GNU General Public License for more details.
#>You should have received a copy of the GNU Lesser General Public License
#>along with this program.  If not, see <http://www.gnu.org/licenses/>.
#>=============================================================================
import subprocess
import os,sys
import zipfile 
import tarfile
import platform
import shutil
from os import  listdir
from os.path import join, isfile, splitext 
from distutils.core import setup
from distutils.command.install import install
import io
sys.path.append('./src')
import re
import requests

def get_latest_git_version()->str:
    """Get the latest git version from the current tag of the git repository"""
    try:
        version = subprocess.check_output(["git", "describe", "--tags"]).strip().decode('utf-8')
        return version.split("-")[0]
    except subprocess.CalledProcessError:
        return None 

def update_version_in_file(version:str):
    """Update the version in the IPhreeqcPy.py file"""
    with open('src/IPhreeqcPy.py', 'r') as file:
        filedata = file.read()
    filedata = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{version}"', filedata)
    with open('src/IPhreeqcPy.py', 'w') as file:
        file.write(filedata)


def list_extra_data(parent_folder):
    """List all files and directories in the parent folder which are to be included as data in the package"""
    result = {'dirs': [], 'files': []}
    for root, dirs, files in os.walk(parent_folder):
        # Filter out directories containing "_ignore"
        dirs[:] = [d for d in dirs if "_ignore" not in d]
        result['dirs'].append(root)
        filtered_files = [os.path.join(root, fname) for fname in files if "_ignore" not in fname]
        result['files'].append(filtered_files)
    return zip(result['dirs'], result['files'])
    
class CompilePhrqc(install):
    """Custom install command to compile the IPhreeqc.dll for windows and libiphreeqc.so for linux"""

    def run(self):
        """Run the install command"""
        # URLs for the IPhreeqc source code for windows and linux. Update when new versions released
        iphreeqc_urls = {
            "win": "https://water.usgs.gov/water-resources/software/PHREEQC/iphreeqc-3.7.3-15968.zip",
            "linux":"https://water.usgs.gov/water-resources/software/PHREEQC/iphreeqc-3.7.3-15968.tar.gz"
        }
        if platform.system() == 'Linux':
            self._linux_compile(iphreeqc_urls['linux'])
        elif platform.system() == 'Windows':
            self._windows_compile(iphreeqc_urls['win'])
        else:
            raise  ValueError(f'Installation not supported for {platform.system()}')
        install.run(self)

    def _windows_compile(self,phreeqc_url:str):
        """Compile the IPhreeqc.dll for windows"""
        #add line to unzip iphreeqc
        self.download_and_unzip(phreeqc_url)
        fpath= ".".join(phreeqc_url.split('/')[-1].split('.')[:-1])
        fpath= os.path.join('phreeqc',fpath)
        os.chdir(fpath)    
        if platform.architecture()[0]=='64bit':
            print("64 bit")
            subprocess.call('cmake -G "Visual Studio 16 2019" -A x64  -DBUILD_SHARED_LIBS=ON', shell=True)
            subprocess.call('cmake --build . --config Release', shell=True)
        if platform.architecture()[0]=='32bit':
            subprocess.call('cmake -G "Visual Studio 16 2019" -A Win32   -DBUILD_SHARED_LIBS=ON', shell=True)
            subprocess.call('cmake --build . --config Release', shell=True)  
        os.chdir(join("..",".."))  
        shutil.copy(join(fpath,'Release','IPhreeqc.dll'),".")

    def _linux_compile(self,phreeqc_url:str):
        """Compile the libiphreeqc.so for linux"""
        #add line to unzip iphreeqc
        self.download_and_unzip(phreeqc_url)
        fpath= ".".join(phreeqc_url.split('/')[-1].split('.')[:-2])
        fpath= os.path.join('phreeqc',fpath)
        os.chdir(fpath)    
        current_path = os.path.abspath(os.getcwd())
        subprocess.call(f'./configure --prefix={current_path} --exec-prefix={current_path}',shell=True)
        subprocess.call('make', shell=True)
        subprocess.call('make check', shell=True)
        subprocess.call('make install', shell=True)
        os.chdir(join('..','..'))
        shutil.copy(join(fpath,'lib','libiphreeqc.so'),".")

    @staticmethod
    def download_and_unzip(link:str):
        """downloads gz or zip file and unzips it"""
        response =requests.get(link)   
        if response.status_code != 200:
            raise ValueError(f"Failed to download file. Status code: {response.status_code}") 
        if link.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall("phreeqc")
        elif link.endswith('.tar.gz'):
            with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar:
                tar.extractall("phreeqc")
        else:
            raise ValueError("Unknown file type")

def run_setup():
    """Run the setup function"""
    # Get the latest git version and update the version in the IPhreeqcPy.py file
    v  = get_latest_git_version()
    update_version_in_file(v)
    # List all the data files to be included in the package
    current_path = os.path.join(os.path.dirname(__file__))
    data=[]
    data.extend(list_extra_data('databases'))
    data.append((current_path,['README.rst']))
    if platform.system() == 'Linux':
        data.append(join(current_path,'libiphreeqc.so'))
    elif platform.system() == 'Windows':
        data.append(join(current_path,'IPhreeqc.dll'))
    # Run the setup function
    setup(
        cmdclass={'install': CompilePhrqc},
        name='IPhreeqcPy',
        version=v,
        author = 'Ravi A. Patel',
        author_email = 'ravee.a.patel@gmail.com',
        license='LGPL V3',
        description='Python wrapper for Iphreeqc',
        long_description=open('README.rst').read(),
        project_urls={
            'Documentation': 'https://iphreeqcpy.readthedocs.io/en/latest/',
            'Source': 'https://github.com/raviapatel/IPhreeqcPy/tree/main',
        },
        package_dir={'': 'src'},
        py_modules = ['IPhreeqcPy'],
        data_files=data,
        platforms=['Windows','Linux'],
        include_package_data=True,
        install_requires=[
            "numpy",
        ],
        python_requires = ">=3.0",
        classifiers=[
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Intended Audience :: Science/Research',
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
         ]
    )
    
if __name__ == '__main__':

    run_setup()
    
    
    
    
    
    
    
    
