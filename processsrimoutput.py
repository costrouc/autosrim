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
    
