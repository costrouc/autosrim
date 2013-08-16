"""BatchSrim.

Usage:
  batchsrim.py -e <exec> (-d <dir> | -f <file>)
  batchsrim.py (-h | --help)
  batchsrim.py --version

Options:
  -e --exe      Complete path to srim executable directory
  -d --dir     Complete path to input *.in files
  -f --file     Complete path to input file <file>
  -h --help     Show this screen.
  --version     Show version.
"""

import os
import shutil
import glob

def runSrimOnDirectory(srim_module_path, directory):
    """
    Execute trim.exe on given directory
    """
    print 'Grabing input files for directory: ' + directory
    print 'Srim Module is in directory: ' + srim_module_path
    print 'Processing the following input files:'
    files = glob.glob(directory + '/*.in')
    for i,_file in enumerate(files):
        print '[', i, '] ', _file
    
    for filename in files:
        runSrimOnFile(srim_module_path, _file)
        
def runSrimOnFile(srim_module_path, filename):
    """
    Run trim.exe on given filename
    """
    print 'Processing ', filename
    
    os.chdir(srim_module_path)

    shutil.copyfile(filename, srim_module_path + '/TRIM.IN')
    
    os.system('wine TRIM.exe')

    outputfiles = ['RANGE','TDATA','IONIZ','VACANCY','PHONON','NOVAC']
    for outfile in outputfiles:
        if os.path.isfile(outfile + '.txt'):
            shutil.copyfile(srim_module_path + '/' + outfile + '.txt', os.path.split(filename)[0] + '/' + outfile + '_' + os.path.basename(filename).split('.')[0] + '.txt')
        else:
            print 'No ' + outfile + ' results were not saved for' + os.path.basename(filename) + '...'

if __name__ == '__main__':    
    from docopt import docopt
    from schema import Schema, And, Or, Use, SchemaError
    
    arguments = docopt(__doc__, version='BatchSrim 0.0.1')

    """
    I hope to integrate schema into validating the input
    for now I will just have to trust user input

    schema = Schema({
    '<data_path>': Use(os.path.exists, error='Must provide valid exec path'),
    '<exec_path>': Use(os.path.exists, error='Must provide valid data path'),
    object: object})

    try:
    arguments = schema.validate(arguments)
    except SchemaError as error:
    exit(error)
    """

    print(arguments)

    if arguments['--file'] == True:
        runSrimOnFile(arguments['<exec>'], arguments['<file>'])
    elif arguments['--dir'] == True:
        runSrimOnDirectory(arguments['<exec>'], arguments['<dir>'])
