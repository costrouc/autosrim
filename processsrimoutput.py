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

Vacancy = namedtuple("Vacancy","names units data")
Range = namedtuple("Range","names units data")
Novac = namedtuple("Novac","names units data")
Layer = namedtuple("Layer","id material depth density")
Density = namedtuple("Density","val units")

def readTDataFile(filename):
    "Reads in the infomation about the target material"
    temp_layer = []
    f = open(filename, "r")
    line = f.readline()
    while line.split()[0] != 'Layer':
        line = f.readline() 
    while line.split()[0] == 'Layer':
         temp_id = int(line.split()[2])
         temp_name = line.split()[4]
         line = f.readline()
         temp_depth = float(line.split()[6])
         line = f.readline()
         temp_density = []
         temp_density.append(Density(float(line.split()[5]),line.split()[6]))
         temp_density.append(Density(float(line.split()[8]),line.split()[9]))
         while line[0] != '=':
             line = f.readline()
         line = f.readline()
         temp_layer.append(Layer(temp_id, temp_name, temp_depth, temp_density))
    return temp_layer
                  
def readVacancyFile(filename):
    "Reads in the associated vacancy file from slim"
    f = open(filename, "r")
    line = f.readline()
    while line != '   TARGET    \n':
        line = f.readline()  
    line = f.readline()
    temp_names = line.split()
    line = f.readline()
    temp_units = line.split()
    line = f.readline()
    line = f.readline()
    temp_data = []
    while line != '\n':
        temp_data.append(line.split())
        line = f.readline()
    f.close()
    temp_data = np.array(temp_data, dtype='float')
    return Vacancy(temp_names, temp_units, temp_data)
    
def readRangeFile(filename):
    "Reads in the associated range file from slim"
    f = open(filename, "r")
    line = f.readline()
    while line.split()[0] != 'DEPTH':
        line = f.readline()  
    temp_names = line.split()
    line = f.readline()
    temp_units = line.split()
    line = f.readline()
    line = f.readline()
    temp_data = []
    while line:
        temp_data.append(line.split())
        line = f.readline()
    f.close()
    temp_data = np.array(temp_data, dtype='float')
    return Range(temp_names, temp_units, temp_data)
    
def readNovacFile(filename):
    "Reads in the associated novac file from slim"
    f = open(filename, "r")
    line = f.readline()
    while line.split()[0] != 'DEPTH':
        line = f.readline()  
    temp_names = line.split()
    line = f.readline()
    line = f.readline()
    temp_data = []
    while line:
        temp_data.append(line.split())
        line = f.readline()
    f.close()
    temp_data = np.array(temp_data, dtype='float')
    return Novac(temp_names, ['(Ang.)','Number'], temp_data)

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
    
