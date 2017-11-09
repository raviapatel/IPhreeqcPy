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
#>GNU Lesser General Public License for more details.
#>You should have received a copy of the GNU Lesser General Public License
#>along with this program.  If not, see <http://www.gnu.org/licenses/>.
#>=============================================================================
from __future__ import print_function
import ctypes
import os
import sys
import platform
__version__ = '1.0.2'

if sys.version_info[0] == 2:
    def bytes(str_, encoding):
        """Compatibilty function for Python 3.
        """
        return str_
    range = xrange 


class IPhreeqc():
    """
    Python wrapper for the compiled IPhreeqc.
    
    Parameters
    ----------
    dll_path  (optional) string 
        path for the iphreeqc compiled library .dll for windows or .so for linux       

    Note
    ----
    
    IPhreeqc is compiled on installation for Linux GNU compilers are used
    and for windows visual studio 10 compilers are used. By default these compiled
    files are used.         
    """
    def __init__(self, dll_path=None):
        if not dll_path:
            system= platform.system()
            if system == 'Windows':
                dll_name = 'IPhreeqc.dll'
            elif system == 'Linux':
                dll_name = 'libiphreeqc.so'

            else:
                msg = 'Platform %s is not supported.' % sys.platform
                raise NotImplementedError(msg)
            dll_path = os.path.join(os.path.dirname(__file__), dll_name)
        phreeqc = ctypes.cdll.LoadLibrary(dll_path)
        c_int = ctypes.c_int
        #map iphreeqc methods
        method_mapping = [('_AccumulateLine', phreeqc.AccumulateLine,
                           [c_int, ctypes.c_char_p], c_int),
                          ('_AddError', phreeqc.AddError,
                           [c_int, ctypes.c_char_p], c_int),
                          ('_AddWarning', phreeqc.AddWarning,
                           [c_int, ctypes.c_char_p], c_int),
                          ('_ClearAccumulatedLines',
                            phreeqc.ClearAccumulatedLines, [c_int], c_int),
                          ('_CreateIPhreeqc', phreeqc.CreateIPhreeqc,
                           [ctypes.c_voidp], c_int),
                          ('_DestroyIPhreeqc', phreeqc.DestroyIPhreeqc,
                           [c_int], c_int),
                          ('_GetComponent', phreeqc.GetComponent,
                           [c_int, c_int], ctypes.c_char_p),
                          ('_GetComponentCount', phreeqc.GetComponentCount,
                           [c_int], c_int),
                          ('_GetErrorString', phreeqc.GetErrorString,
                           [c_int],  ctypes.c_char_p),
                          ('_RunAccumulated', phreeqc.RunAccumulated,
                           [c_int], c_int),
                          ('_GetSelectedOutputColumnCount',
                           phreeqc.GetSelectedOutputColumnCount, [c_int],
                           c_int),
                          ('_GetSelectedOutputRowCount',
                           phreeqc.GetSelectedOutputRowCount, [c_int], c_int),
                          ('_GetSelectedOutputValue', phreeqc.GetSelectedOutputValue,
                           [c_int, c_int, c_int, ctypes.POINTER(_VAR)], c_int),
                          ('_LoadDatabase', phreeqc.LoadDatabase,
                           [c_int, ctypes.c_char_p], c_int),
                          ('_LoadDatabaseString', phreeqc.LoadDatabaseString,
                           [c_int, ctypes.c_char_p], c_int),
                          ('_RunString', phreeqc.RunString,
                           [c_int, ctypes.c_char_p], c_int),
                          ('_SetSelectedOutputFileOn',
                           phreeqc.SetSelectedOutputFileOn, [c_int, c_int],
                           c_int),
                          ('_SetSelectedOutputFileOff',
                           phreeqc.SetSelectedOutputFileOn, [c_int, c_int],
                           c_int),
                          ('_SetDumpFileOn',
                           phreeqc.SetDumpFileOn, [c_int,c_int],
                           c_int),
                          ('_SetDumpFileOff',
                           phreeqc.SetDumpFileOn, [c_int,c_int],
                           c_int),
                          ('_SetDumpStringOn',
                           phreeqc.SetDumpStringOn, [c_int,c_int],
                           c_int),
                          ('_SetDumpStringOff',
                           phreeqc.SetDumpStringOn, [c_int,c_int],
                           c_int),
                           ('_GetDumpString',
                           phreeqc.GetDumpString, [c_int],
                           ctypes.c_char_p),
                           ]
        for name, com_obj, argtypes, restype in method_mapping:
            com_obj.argtypes = argtypes
            com_obj.restype = restype
            setattr(self, name, com_obj)
        self.var = _VAR ()
        self.phc_error_count = 0
        self.phc_warning_count = 0
        self.phc_database_error_count = 0
        self.id = self.CreateIPhreeqc()

    @staticmethod
    def _RaisePhreeqcError(error_code):
        """
        There was an error, raise an exception.
        
        Parameters
        ----------
        error_code:  integer
            equal to  0 gives 'ok'
            equal to -1 raises 'out of memory'
            equal to -2 raises 'bad value'
            equal to -3 raises 'invalid argument type'
            equal to -4 raises 'invalid row'
            equal to -5 raises 'invalid column'
            equal to -6 raises 'invalid instance id'
        """
        error_types = {0: 'ok', -1: 'out of memory', -2: 'bad value',
                       -3: 'invalid argument type', -4: 'invalid row',
                       -5: 'invalid column', -6: 'invalid instance id'}
        error_type = error_types[error_code]
        if error_type:
            raise PhreeqcException(error_type)

    def _RaiseStringError(self, errors):
        """
        Raise an exception with message from IPhreeqc error.
        
        Parameters
        ----------
        errors: integer
           Number of error occured
        
        """
        if errors > 1:
            msg = '%s errors occured.\n' % errors
        elif errors == 1:
            msg = 'An error occured.\n'
        else:
            msg = 'Wrong error number.'
        raise Exception(msg + self.GetErrorString())

    def AccumulateLine(self, line):
        """
        Accumlate line(s) for input to phreeqc
        """
        errors = self._AccumulateLine(self.id, bytes(line, 'utf-8'))
        if errors != 0:
            self._RaiseStringError(errors)
    
    def RunAccumulated(self):
        """
        Run the input buffer as defined by calls to :func:`~IphreeqcPy.IPhreeqc.AccumulateLine`
        """
        errors = self._RunAccumulated(self.id)
        if errors != 0:
            self._RaiseStringError(errors)
    
    def AddError(self, phc_error_msg):
        """
        Appends the given error message and increments the error count. Internally
        used fo create an error condition
        
        Parameters
        ----------
        phc_error_msg: string
            Error message to append
        """
        errors = self._AddError(self.id, bytes(phc_error_msg, 'utf-8'))
        if errors < 0:
            self._RaiseStringError(errors)
        else:
            self.phc_error_count = errors

    def AddWarning(self, phc_warn_msg):
        """
        Appends the given warning message and increments the warning count.
        Internally used to create warning condition
        
        Parameters
        ----------
        phc_warn_msg: string
            Warning message to append
        """
        errors = self._AddWarning(self.id, bytes(phc_warn_msg, 'utf-8'))
        if errors < 0:
            self._RaiseStringError(errors)
        else:
            self.phc_warning_count = errors

    def ClearAccumulatedLines(self):
        """
        Clear the accumlated input buffer. Input buffer is accumlated from
        calls to :func:`~IphreeqcPy.IPhreeqc.AccumulateLine`
        """
        errors = self._ClearAccumulatedLines(self.id)
        if errors != 0:
            self._RaiseStringError(errors)

    @property
    def GetSelectedOutputColumnCount(self):
        """
        Retrieves the number of columns in the selected output buffer
        """
        return self._GetSelectedOutputColumnCount(self.id)

    def CreateIPhreeqc(self):
        """
        Create a new IPhreeqc instance
        """
        error_code = self._CreateIPhreeqc(ctypes.c_voidp())
        if error_code < 0:
            self._RaisePhreeqcError(error_code)
        id = error_code
        return id

    def DestroyIPhreeqc(self):
        """
        Release an IPhreeqc instance from memory
        """
        error_code = self._DestroyIPhreeqc(self.id)
        if error_code < 0:
            self._RaisePhreeqcError(error_code)

    def GetComponent(self, index):
        """
        Retrieves the given component
        
        Parameters
        ----------
        index: integer
            The zero-based index of the component to retrieve
        """
        component = self._GetComponent(self.id, index).decode('utf-8')
        if not component:
            raise IndexError('No component for index %s' % index)
        return component

    @property
    def GetComponentCount(self):
        """
        Retrieves the number of component in the current component list
        """
        return self._GetComponentCount(self.id)

    def GetComponentList(self):
        """
        Get names of all components
        
        Returns
        -------
        list
            list with component names
        """
        get_component = self.GetComponent
        return [get_component(index) for index in range(self.GetComponentCount)]

    def GetErrorString(self):
        """
        Retrieves the error messages from the last call to :func:`~IphreeqcPy.IPhreeqc.RunAccumulated`, 
        :func:`~IphreeqcPy.IPhreeqc.RunFile`, :func:`~IphreeqcPy.IPhreeqc.RunString`, :func:`~IphreeqcPy.IPhreeqc.LoadDatabase`,
        :func:`~IphreeqcPy.IPhreeqc.LoadDatabaseString`
        
        Returns
        -------
        string        
            Error string
        """
        return self._GetErrorString(self.id).decode('utf-8')

    def GetSelectedOutputValue(self, row, col):
        """
        Get one value from selected output at given row and column
        
        Parameters
        ----------
        row: integer
            row index
        
        column: integer
            column index
        
        Returns
        -------
        Real
            Selected output value
        """
        error_code = self._GetSelectedOutputValue(self.id, row, col, self.var)
        if error_code != 0:
            self._RaisePhreeqcError(error_code)
        type_ = self.var.type
        value = self.var.value
        if type_ == 3:
            val = value.double_value
        elif type_ == 2:
            val = value.long_value
        elif type_ == 4:
            val = value.string_value.decode('utf-8')
        elif type_ == 0:
            val = None
        if type_ == 1:
            self.raise_error(value.error_code)
        return val

    def GetSelectedOutputArray(self):
        """
        Get all values from selected output
        
        Returns
        -------
        list
            All values of the selected output in multi-list form
        """
        nrows = self.GetSelectedOutputRowCount
        ncols = self.GetSelectedOutputColumnCount
        results = []
        for row in range(nrows):
            result_row = []
            for col in range(ncols):
                result_row.append(self.GetSelectedOutputValue(row, col))
            results.append(result_row)
        return results

    def GetSelectedOutputRow(self, row):
        """
        Get all values for one row from  selected output 
        
        Parameters
        ----------
        row: integer
            row index
        
        Returns
        -------
        list
            list of selected output for a given row
        """
        if row < 0:
            row = self.GetSelectedOutputRowCount + row
        ncols = self.GetSelectedOutputColumnCount
        results = []
        for col in range(ncols):
            results.append(self.GetSelectedOutputValue(row, col))
        return results

    def GetSelectedOutputCol(self, col):
        """
        Get all values for one column from selected output
        
        Parameters
        ----------
        col: integer
            column index
        
        Returns
        -------
        list
            list of selected output for a given column
        """
        if col < 0:
            col = self.GetSelectedOutputColumnCount + col
        nrows = self.GetSelectedOutputRowCount
        results = []
        for row in range(nrows):
            results.append(self.GetSelectedOutputValue(row, col))
        return results

    def SetSelectedOutputFileOff(self):
        """
        Turn on writing to selected output file 
        """
        self._SetSelectedOutputFileOff(self.id, 0)

    def SetSelectedOutputFileOn(self):
        """
        Turn on writing to selected output file 
        """
        self._SetSelectedOutputFileOn(self.id, 1)

    def LoadDatabase(self, database_name):
        """
        Load a database with given file_name
        
        Parameters
        ----------
        
        database_name: string
            path to the database. IphreeqcPy comes with all databases of 
            phreeqc and cemdata07.To use one of these database type the relevant
            filename. Filenames are listed below
 
            * alkaline.dat
            * cemdata07.dat
            * ex15.dat
            * llnl.dat
            * mcatexch.dat
            * minteq.dat
            * minteq.V4.dat
            * phreeqc.dat
            * phreeqcU.dat
            * phreeqd.dat
            * pitzer.dat
            * wateq4f.dat
        """
        fpath = os.path.join(os.path.dirname(__file__),'databases',database_name)
        if os.path.isfile(fpath): 
            database_name=fpath
        self.phc_database_error_count = self._LoadDatabase(
            self.id, bytes(database_name, 'utf-8'))

    def LoadDatabaseString(self, input_string):
        """
        Loads a database from a string
        
        Parameters
        ----------
        input_string: string
            input database string
        """
        self.phc_database_error_count = self._LoadDatabaseString(
            self.id, ctypes.c_char_p(bytes(input_string, 'utf-8')))

    @property
    def GetSelectedOutputRowCount(self):
        """
        Get number of rows in selected output 
        """
        return self._GetSelectedOutputRowCount(self.id)

    def RunString(self, cmd_string):
        """
        Run PHREEQC input from string
        
        Parameters
        ----------
        cmd_string: string
            string of phreeqc command to be executed
        """
        errors = self._RunString(self.id,
                                  ctypes.c_char_p(bytes(cmd_string, 'utf-8')))
        if errors != 0:
            self._RaiseStringError(errors)
    
    def RunFile(self,Filename):
        """
        run instructions from a file
        
        Parameters
        ----------
        Filename: string
            path to file to run instructions from
        """
        input_file = open(Filename,'r')
        frun = input_file.read()
        errors = self._RunString(self.id,
                                  ctypes.c_char_p(bytes(frun, 'utf-8')))
        if errors != 0:
            self._RaiseStringError(errors)
            
    def SetDumpFileOn(self):
        """
        Set the dump file switch on to write dump file
        """
        errors = self._SetDumpFileOn(self.id,1)
        if errors != 0:
            self._RaiseStringError(errors)

    def SetDumpFileOff(self):
        """
        Set the dump file switch off  
        """
        errors = self._SetDumpFileOff(self.id,0)
        if errors != 0:
            self._RaiseStringError(errors)

    def SetDumpStringOn(self):
        """
        Set the dump string switch on to get dump string
        """
        errors = self._SetDumpStringOn(self.id,1)
        if errors != 0:
            self._RaiseStringError(errors)

    def SetDumpStringOff(self):
        """
        Set the dump string switch off
        """
        errors = self._SetDumpStringOff(self.id,0)
        if errors != 0:
            self._RaiseStringError(errors)
            
    def GetDumpString(self):
        """
        Gives dump string as output
        """
        return self._GetDumpString(self.id)
 

class _VARUNION(ctypes.Union):
    # pylint: disable-msg=R0903
    # no methods
    """Union with types.

    See Var.h in PHREEQC source.
    """
    _fields_ = [('long_value', ctypes.c_long),
                ('double_value', ctypes.c_double),
                ('string_value', ctypes.c_char_p),
                ('error_code', ctypes.c_int)]


class _VAR (ctypes.Structure):
    # pylint: disable-msg=R0903
    # no methods
    """Struct with data type and data values.

    See Var.h in PHREEQC source.
    """
    _fields_ = [('type', ctypes.c_int),
                ('value', _VARUNION)]


class PhreeqcException(Exception):
    """Error in Phreeqc call.
    """
    pass


def test():
    """
    """
    x=IPhreeqc()
    x.LoadDatabase('cemdata07.dat')
    x.SetDumpStringOn()   
    x.AccumulateLine(
    """
    solution 0-1
    -pH 7 charge
    -water 1.0  
    Equilibrium phases 1
    portlandite 0 1
    save solution 1
    save Equilibrium phases 1
    save solution 0
    selected_output
    -file abstracted_model.xls
    -totals Ca Si
    -temp true
    -high_precision true
    -equilibrium_phases  portlandite
    Dump
    -all
    end
    """    
    )
    x.RunAccumulated()
    x.RunString(
    """
    use solution 1
    use Equilibrium phases 1
    use solution 0
    Advection
    -cells 1
    -shifts 10000
    -punch_frequency 500    
    """    
    )
    print( x.GetSelectedOutputArray())
    print( x.GetDumpString())
    return

if __name__ == '__main__':
    test()

