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
from os.path import join
from setuptools import setup, find_namespace_packages, Command
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
    with open('src/IPhreeqcPy/IPhreeqcPy.py', 'r') as file:
        filedata = file.read()
    filedata = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{version}"', filedata)
    with open('src/IPhreeqcPy/IPhreeqcPy.py', 'w') as file:
        file.write(filedata)
    
class CompilePhrqc(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    """Custom install command to compile the IPhreeqc.dll for windows and libiphreeqc.so for linux"""
    def run(self):
        """Run the install command"""
        # URLs for the IPhreeqc source code for windows and linux. Update when new versions released
        iphreeqc_urls = {
            "win": "https://water.usgs.gov/water-resources/software/PHREEQC/iphreeqc-3.7.3-15968.zip",
            "linux":"https://water.usgs.gov/water-resources/software/PHREEQC/iphreeqc-3.7.3-15968.tar.gz"
        }
        current_path = os.path.abspath(os.getcwd())
        build_exists = False
        if  os.path.exists(join(current_path,'src','IPhreeqcPy','lib')):
            if (platform.system() == 'Linux'and
                os.path.exists(join(current_path,'src','IPhreeqcPy','lib','libiphreeqc.so'))
                ):
                    build_exists = True
            elif (platform.system() == 'Windows' and
                  os.path.exists(join(current_path,'src','IPhreeqcPy','lib','IPhreeqc.dll'))
                ):
                    build_exists = True
            else:
                shutil.rmtree(join(current_path,'src','IPhreeqcPy','lib'))
        # If the build does not exist, compile the IPhreeqc.dll for windows or libiphreeqc.so for linux
        if not build_exists:
            os.mkdir(join(current_path,'src','IPhreeqcPy','lib'))
            if platform.system() == 'Linux':
                self._linux_compile(iphreeqc_urls['linux'])
            elif platform.system() == 'Windows':
                self._windows_compile(iphreeqc_urls['win'])
            else:
                raise  ValueError(f'Installation not supported for {platform.system()}')
            return
        else:
            return
    def _windows_compile(self,phreeqc_url:str):
        """Compile the IPhreeqc.dll for windows"""
        #add line to unzip iphreeqc
        self.download_and_unzip(phreeqc_url)
        fpath= ".".join(phreeqc_url.split('/')[-1].split('.')[:-1])
        fpath= join('phreeqc',fpath)
        os.chdir(fpath)    
        if platform.architecture()[0]=='64bit':
            print("64 bit")
            subprocess.call('cmake -G "Visual Studio 16 2019" -A x64  -DBUILD_SHARED_LIBS=ON', shell=True)
            subprocess.call('cmake --build . --config Release', shell=True)
        if platform.architecture()[0]=='32bit':
            subprocess.call('cmake -G "Visual Studio 16 2019" -A Win32   -DBUILD_SHARED_LIBS=ON', shell=True)
            subprocess.call('cmake --build . --config Release', shell=True)  
        os.chdir(join("..",".."))  
        current_path = os.path.abspath(os.getcwd())
        shutil.copy(join(fpath,'Release','IPhreeqc.dll'),os.path.join(current_path,'src','IPhreeqcPy','lib'))

    def _linux_compile(self,phreeqc_url:str):
        """Compile the libiphreeqc.so for linux"""
        #add line to unzip iphreeqc
        self.download_and_unzip(phreeqc_url)
        fpath= ".".join(phreeqc_url.split('/')[-1].split('.')[:-2])
        fpath= join('phreeqc',fpath)
        os.chdir(fpath)    
        current_path = os.path.abspath(os.getcwd())
        subprocess.call(f'./configure --prefix={current_path} --exec-prefix={current_path}',shell=True)
        subprocess.call('make', shell=True)
        subprocess.call('make check', shell=True)
        subprocess.call('make install', shell=True)
        os.chdir(join('..','..'))
        current_path = os.path.abspath(os.getcwd())
        shutil.copy(join(fpath,'lib','libiphreeqc.so'),join(current_path,'src','IPhreeqcPy','lib'))

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
    current_path = os.path.abspath(os.getcwd())
    # Get the latest git version and update the version in the IPhreeqcPy.py file
    v  = get_latest_git_version()
    update_version_in_file(v)
    # Run the setup function
    setup(
        name='IPhreeqcPy',
        version=v,
        author = 'Ravi A. Patel',
        author_email = 'ravee.a.patel@gmail.com',
        license='LGPL V3',
        description='Python wrapper for Iphreeqc',
        long_description=open('README.md').read(),
        project_urls={
            'Documentation': 'https://iphreeqcpy.readthedocs.io/en/latest/',
            'Source': 'https://github.com/raviapatel/IPhreeqcPy/tree/main',
        },
        cmdclass={
            'compile_phreeqc': CompilePhrqc,
        },
        packages = find_namespace_packages('src'),
        package_data={
            "IPhreeqcPy.lib": ["*.dll","*.so"],
            "IPhreeqcPy.databases": ["*.dat"],
        },
        platforms=['Windows','Linux'],
        package_dir={'': 'src'},
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
    
    
    
    
    
    
    
    
