Quick Start Example
===================

This is a simple example to demonstrate use of IPhreeqcPy. This example is included as a test case in IPhreeqcPy.

.. code:: Python

    from IPhreeqcPy import IPhreeqc
    x=IPhreeqc() #initalize IPhreeqc object
    x.LoadDatabase('cemdata07.dat') # Load database
    x.SetDumpStringOn()   #set DumpString output on
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
    ) # Do some Phrqc input
    x.RunAccumulated() #Run phreeqc
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
    ) #You can also run phreeqc like this 
    print x.GetSelectedOutputArray() #get selected output
    print x.GetDumpString() #get dump string

