"""ProcessSrimOutput.

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
  processsrimoutput.py [(-f <file> | -d <dir>)]
  processsrimoutput.py (-h | --help)
  processsrimoutput.py --version

Options:
  -d --dir      Complete path to directory to process
  -f --file     Complete path to input file <file> to process
  -h --help     Show this screen.
  --version     Show version.
"""

import numpy as np

def readPlotFiles(testname):
    """
    A function to read all of the plot data files from SRIM
    An assumption is made that all of the files exist
    """
    
    _vacancy = readVacancyFile('VACANCY_' + testname + '.txt')
    _range = readRangeFile('RANGE_' + testname + '.txt')
    _novac = readNovacFile('NOVAC_' + testname + '.txt')
    _lateral = readLateralFile('LATERAL_' + testname + '.txt')
    _ioniz = readIonizFile('IONIZ_' + testname + '.txt')
    _phonon = readPhononFile('PHONON_' + testname + '.txt')
    _e2recoil = readE2RecoilFile('E2RECOIL_' + testname + '.txt')

    return {"vacancy": _vacancy, "range": _range, "novac": _novac, "lateral": _lateral, "ioniz": _ioniz, "phonon": _phonon, "e2recoil": _e2recoil}
    
def readVacancyFile(filename):
    """
    Reads in the associated vacancy plot file from slim.
    Distribution of Vacancies
    """
    inputfile = open(filename, "r")
    line = inputfile.readline()

    while line != '   TARGET    \r\n':
        line = inputfile.readline()  

    line = inputfile.readline()
    labels = line.split()

    num_atoms = len(labels) - 2
    units = ['Angstroms', '(Knock-Ons) Number of Target Atoms Recoiling from the Ion']

    for i in range(num_atoms):
        units.append('Vacancies/(Angstrom-Ion)')

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line != '\r\n':
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()

    data = np.array(data, dtype='float')
    return {'labels': labels, 'units': units, 'data': data} 

def readE2RecoilFile(filename):
    """
    Reads in the associated E2Recoil plot file from slim.
    Energy transferred to recoils.
    """
    
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line.split()[0] != '(Ang.)':
        line = inputfile.readline()  

    num_atoms = len(line.split()) - 5
    labels = ['Depth', 'Energy from Ions']
    units = ['Angstroms', 'eV / (Angstrom-Ion)']

    tokens = line.split()
    for i in range(num_atoms):
        labels.append('Energy Absorbed by ' + tokens[3 + 2*i]) 
        units.append('eV / (Angstrom-Ion)')
        
    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()

    data = np.array(data, dtype='float')
    return {'labels': labels, 'units': units, 'data': data} 


def readRangeFile(filename):
    """
    "Reads in the associated range plot file from slim.
    Final distribution of Ions/Recoils
    """

    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line.split()[0] != 'DEPTH':
        line = inputfile.readline()

    labels = line.split()
    num_atoms = len(labels) - 2

    units = ['Angstroms', 'Ions (Atoms/cm^3)/ (Atoms/cm^2)']
    for i in range(num_atoms):
        units.append('(Atoms/cm^3) / (Atoms/cm^2)')
    
    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data, dtype='float')
    
    return {'labels': labels, 'units': units, 'data': data} 

def readNovacFile(filename):
    """
    Reads in the associated novac plot file from slim
    Replacement collisions
    """
    
    labels = ['Depth', 'Number of Vacancies']
    units = ['Angstroms', 'Number of Vacancies/(Angstrom-Ion)']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != '  DEPTH (A)      Number\r\n':
        line = inputfile.readline()

    # These 2 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data, dtype='float')
    
    return {'labels': labels, 'units': units, 'data': data} 

def readIonizFile(filename):
    """
    Reads in the associated ioniz plot file from slim
    Distribution of Ionization
    """
    
    labels = ['Depth', 'Ioniz by Ions', 'Ioniz by Recoils']
    units = ['Angstroms', 'eV / (Angstrom-Ion)', 'eV / (Angstrom-Ion)']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != '  TARGET       IONIZ.       IONIZ.  \r\n':
        line = inputfile.readline()

    # These 4 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data, dtype='float')
    
    return {'labels': labels, 'units': units, 'data': data} 

def readPhononFile(filename):
    """
    Reads in the associated ioniz plot file from slim
    Distribution of Phonons
    """
    
    labels = ['Depth', 'Phonons by Ion', 'Phonons by Recoils']
    units = ['Angstroms', 'Phonons / (Angstrom-Ion)', 'Phonons / (Angstrom-Ion)']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != '  DEPTH       PHONONS     PHONONS    \r\n':
        line = inputfile.readline()

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data, dtype='float')
    
    return {'labels': labels, 'units': units, 'data': data} 



def readLateralFile(filename):
    """
    Reads in the associated lateral plot file from slim
    Lateral Spread of Ions
    """
    
    labels = ['Target Depth', 'Lateral Projected Range', 'Projected Straggling', 'Lateral Radial', 'Radial Straggling']
    units = ['Angstroms', 'Angstroms', 'Angstroms', 'Angstroms']

    inputfile = open(filename, "r")
    line = inputfile.readline()

    while line != '  TARGET       PROJ.RANGE   Straggling      RADIAL      Straggling  \r\n':
        line = inputfile.readline()

    # These 3 lines are simply titles for the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()

    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
    
    inputfile.close()
    data = np.array(data, dtype='float')

    return {'labels': labels, 'units': units, 'data': data}

def readBackScatFile(filename):
    """
    Reads in the associated backscatter plot file from slim
    This file tabulates the kinetics of ions or atoms leaving the target.
    """
    
    labels = ['Type Atom', 'Ion Number', 'Atom Number', 'Energy', 'Depth', 'Lateral-Position-X', 'Lateral-Position Y', 'Atom-Direction Cos(X)', 'Atom-Direction Cos(Y)', 'Atom Direction Cos(Z)' ]
    units = ['S = Sputtered Atom, B = Backscattered Ion, T = Transmitted Ion', 'Ion Number', 'Z of Atom Leaving', 'eV', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != ' Ion  Atom   Energy        Depth       Lateral-Position        Atom Direction      \r\n':
        line = inputfile.readline()

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data)
    
    return {'labels': labels, 'units': units, 'data': data} 

def readEXYZFile(filename):
    """
    Reads in the special EXYZ file from slim
    This file gives the rough position of the ion every 10eV
    """
    
    labels = ['Ion Number', 'Energy', 'Depth', 'Lateral-Position-X', 'Lateral-Position Y', 'Electronic Stop', 'Energy Lost to Last Recoil' ]
    units = ['Ion Number', 'keV', 'Angstroms', 'Angstroms', 'Angstroms', 'eV/A', 'eV']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != 'Ion       Energy     Depth (X)     Y           Z       Electronic   Energy Lost to\r\n':
        line = inputfile.readline()

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data, dtype='float')
    
    return {'labels': labels, 'units': units, 'data': data} 


def readRange3DFile(filename):
    """
    Reads in the Range 3D file from slim
    This file gives the final ion positions
    """
    
    labels = ['Ion Number', 'Depth', 'Lateral-Position-Y', 'Lateral-Position Z']
    units = ['Ion Number', 'Angstroms', 'Angstroms', 'Angstroms']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != 'Ion       Depth  X   Lateral Y   Lateral Z  \r\n':
        line = inputfile.readline()

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data, dtype='float')
    
    return {'labels': labels, 'units': units, 'data': data} 

def readSputterFile(filename):
    """
    Reads in the associated backscatter plot file from slim
    This file tabulates the kinetics of ions or atoms leaving the target.
    """
    
    labels = ['Type Atom', 'Ion Number', 'Atom Number', 'Energy', 'Depth X', 'Lateral-Position-Y', 'Lateral-Position Z', 'Atom-Direction Cos(X)', 'Atom-Direction Cos(Y)', 'Atom Direction Cos(Z)' ]
    units = ['S = Sputtered Atom, B = Backscattered Ion, T = Transmitted Ion', 'Ion Number', 'Z of Atom Leaving', 'eV', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != ' Ion  Atom   Energy        Depth       Lateral-Position        Atom Direction      \r\n':
        line = inputfile.readline()

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data)
    
    return {'labels': labels, 'units': units, 'data': data} 

def readTransmitFile(filename):
    """
    Reads in the associated backscatter plot file from slim
    This file tabulates the kinetics of ions or atoms leaving the target.
    """
    
    labels = ['Type Atom', 'Ion Number', 'Atom Number', 'Energy', 'Depth X', 'Lateral-Position-Y', 'Lateral-Position Z', 'Atom-Direction Cos(X)', 'Atom-Direction Cos(Y)', 'Atom Direction Cos(Z)' ]
    units = ['S = Sputtered Atom, B = Backscattered Ion, T = Transmitted Ion', 'Ion Number', 'Z of Atom Leaving', 'eV', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != ' Ion  Atom   Energy        Depth       Lateral-Position        Atom Direction      \r\n':
        line = inputfile.readline()

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data)
    
    return {'labels': labels, 'units': units, 'data': data}

def readTrimOutFile(filename):
    """
    Reads in the associated backscatter plot file from slim
    This file tabulates the kinetics of ions or atoms leaving the target.
    """
    
    labels = ['Type Atom', 'Ion Number', 'Atom Number', 'Energy', 'Depth X', 'Lateral-Position-Y', 'Lateral-Position Z', 'Atom-Direction Cos(X)', 'Atom-Direction Cos(Y)', 'Atom Direction Cos(Z)' ]
    units = ['S = Sputtered Atom, B = Backscattered Ion, T = Transmitted Ion', 'Ion Number', 'Z of Atom Leaving', 'eV', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms', 'Angstroms']
    inputfile = open(filename, "r")
    line = inputfile.readline()
    
    while line != ' Ion  Atom   Energy        Depth       Lateral-Position        Atom Direction      \r\n':
        line = inputfile.readline()

    # These 3 lines are simply to label the data
    line = inputfile.readline()
    line = inputfile.readline()
    line = inputfile.readline()
    
    data = []
    while line:
        data.append(line.split())
        line = inputfile.readline()
        
    inputfile.close()
    data = np.array(data)
    
    return {'labels': labels, 'units': units, 'data': data}

if __name__ == '__main__':    
    from docopt import docopt
    from schema import Schema, And, Or, Use, SchemaError
    
    arguments = docopt(__doc__, version='ProcessSrimOutput 0.0.1')

    if arguments['--file'] == True:
        print 'You want to opperate the tests on a testfile'
    elif arguments['--dir'] == True:
        print 'You want to opperate the tests on a directory'
    else:
        print 'You want to opperate on the current directory'
    
