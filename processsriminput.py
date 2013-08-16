"""ProcessSrimInput

   ProcessSrim assumes a naming convention where <testname>.in is
   the tests name. All appropriate output files from srim should be
   labeled <outputfile>_<testname>.txt.

   For Example:
   TRIM input file is named test1.in

   Output files would be in the same directory named as:
   RANGE_test1.txt
   NOVAC_test1.txt
   etc.

   processsrim.py with no arguments will opperate on the current
   directory.
   
Usage:
  processsriminput.py -c <file>
  processsriminput.py -v <file>
  processsriminput.py -s
  processsriminput.py (-h | --help)
  processsriminput.py --version

Options:
  -c --create   Create new inputfile with prompt
  -v --verify   Inspect inputfile for correctness
  -s --sample   Generate Sample Inputfile to Standard Output
  -h --help     Show this screen.
  --version     Show version.
"""

def generateSampleInputFile():
    """
    Generates a dos format file to be read as input to trim.exe
    """
    print "==> SRIM-2008.04 This file controls TRIM Calculations.\r\nIon: Z1 ,  M1,  Energy (keV), Angle,Number,Bragg Corr,AutoSave Number.\r\n     5      11         20       0   9        0    10000\r\nCascades(1=No;2=Full;3=Sputt;4-5=Ions;6-7=Neutrons), Random Number Seed, Reminders\r\n                      2                                   0       0\r\nDiskfiles (0=no,1=yes): Ranges, Backscatt, Transmit, Sputtered, Collisions(1=Ion;2=Ion+Recoils), Special EXYZ.txt file\r\n                          1       1           1       1               1                               1\r\nTarget material : Number of Elements & Layers\r\n\"B (10 keV) in SiO2/Si (Shallow Implant) \"       3               2\r\nPlotType (0-5); Plot Depths: Xmin, Xmax(Ang.) [=0 0 for Viewing Full Target]\r\n       1                         0            2000\r\nTarget Elements:    Z   Mass(amu)\r\nAtom 1 = Si =       14      28\r\nAtom 2 = O =         8      16\r\nAtom 3 = Si =       14      28\r\nLayer   Layer Name /               Width Density    Si(14)    O(8)  Si(14)\r\nNumb.   Description                (Ang) (g/cm3)    Stoich  Stoich  Stoich\r\n 1      \"Si/O@2\"           900  2.32 .333333 .666667       0\r\n 2      \"Silicon\"           1100  2.32       0       0       1\r\n0  Target layer phases (0=Solid, 1=Gas)\r\n0 0 \r\nTarget Compound Corrections (Bragg)\r\n 1   1  \r\nIndividual target atom displacement energies (eV)\r\n      21      22      21\r\nIndividual target atom lattice binding energies (eV)\r\n     2.1     2.2     2.1\r\nIndividual target atom surface binding energies (eV)\r\n     3.1     3.2     3.1\r\nStopping Power Version (1=2008, 0=2008)\r\n 0 \r\n"

def parseInputFile(filename):
    """
    Parses a srim inputfile an returns a dictionary data-structure of the input
    """
    
if __name__ == '__main__':    
    from docopt import docopt
    from schema import Schema, And, Or, Use, SchemaError
    
    arguments = docopt(__doc__, version='ProcessSrimOutput 0.0.1')

    if arguments['--create'] == True:
        print 'You want to create a new srim input file'
    elif arguments['--verify'] == True:
        print 'You want to inpect an input file for correctness'
    elif arguments['--sample'] == True:
        generateSampleInputFile()
