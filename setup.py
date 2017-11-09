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
from __future__ import print_function
import subprocess
import os,sys
import zipfile 
import tarfile
import platform
import shutil
from os import  listdir
from os.path import join, isfile, splitext 
from numpy.distutils.core import setup
from numpy.distutils.command.install import install
sys.path.append('./src')
import IPhreeqcPy
v=IPhreeqcPy.__version__
class CompilePhrqc(install):
    def run(self):
        if platform.system() == 'Linux':
            linux_compile()
        elif platform.system() == 'Windows':
            windows_compile()
        else:
            raise  ValueError('Installation not supported for %s'%platform.system())
        install.run(self)
            
def list_extra_data(
        parent_folder,
        exclude = [],
        exclude_ext = [],
        result = None):
    # Using os.walk was considered but ruled out because it would not be
    # practical to use with the exclude variable
    build_at_end = False
    if result == None:
        build_at_end = True
        result = {'dirs': [], 'files': []}
    result['dirs'].append(parent_folder)
    curdir = len(result['files'])
    result['files'].append([])
    for fname in listdir(parent_folder):
        path = join(parent_folder,fname)
        acceptable = path not in exclude and fname not in exclude
        acceptable = acceptable and "_ignore" not in fname
        if acceptable:
            if isfile(path):
                name, ext = splitext(fname)
                if ext not in exclude_ext:
                    result['files'][curdir].append(path)
            else:
                result = list_extra_data(path, exclude, exclude_ext, result)
    if build_at_end:
        result = zip(result['dirs'],result['files'])
    return result    
    
def windows_compile():
    #add line to unzip iphreeqc
    f='iphreeqc-3.3.8-11728'
    os.chdir('iphreeqc_src')    
    zipfile.ZipFile(f+'.zip').extractall()
    os.chdir(f)    
    if platform.architecture()[0]=='64bit':
        subprocess.call('cmake -G "Visual Studio 15 2017 Win64" "..\%s"'%f, shell=True)
        subprocess.call('cmake --build . --config Release', shell=True)
    if platform.architecture()[0]=='32bit':
        subprocess.call('cmake -G "Visual Studio 10 2017" "..\%s"'%f, shell=True)
        subprocess.call('cmake --build . --config Release', shell=True)    
    shutil.copy(join(os.getcwd(),'Release','IPhreeqc.dll'),join('..','..'))
    os.chdir(join('..','..'))

def linux_compile():
    #add line to unzip iphreeqc
    f='iphreeqc-3.3.8-11728'
    os.chdir('iphreeqc_src')    
    tar = tarfile.open(f+'.tar.gz', "r:gz")
    tar.extractall()
    tar.close()
    os.chdir(f)
    ptemp=os.path.abspath(os.getcwd())
    subprocess.call('./configure --prefix=%s --exec-prefix=%s'%(ptemp,ptemp),shell=True)
    subprocess.call('make', shell=True)
    subprocess.call('make check', shell=True)
    subprocess.call('make install', shell=True)
    shutil.copy(join(ptemp,'lib','libiphreeqc.so'),join('..','..'))
    os.chdir(join('..','..'))

def run_setup():
    data=[]
    data.extend(list_extra_data('databases'))
    data.extend(list_extra_data('iphreeqc_src'))
    data.append('README.rst')
    if platform.system() == 'Linux':
        data.append(join('libiphreeqc.so'))
    elif platform.system() == 'Windows':
        data.append(join('IPhreeqc.dll'))
    setup(
        cmdclass={'install': CompilePhrqc},
        name='IPhreeqcPy',
        version=v,
        author = 'Ravi A. Patel',
        author_email = 'ravee.a.patel@gmail.com',
        download_url = 'http://raviapatel.bitbucket.org/IPhreeqcPy' ,
        url='https://bitbucket.org/raviapatel/iphreeqcpy/get/1.0.1.tar.gz',
        license='LGPL V3',
        description='Python wrapper for Iphreeqc',
        long_description=open('README.rst').read(),
        package_dir={'': 'src'},
        py_modules = ['IPhreeqcPy'],
        data_files=data,
        platforms=['Windows','Linux'],
#        install_requires=['numpy'],
        classifiers=[
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Intended Audience :: Science/Research',
         ]
    )
    
if __name__ == '__main__':

    run_setup()
    
    
    
    
    
    
    
    
