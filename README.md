AutoSrim 
=========
version. 0.0.1

A tool for automating many of the tasks that are esential in running srim computations.
Detailed information about the software itself can be found at [SRIM.org](www.srim.org) along
with intallation instructions. While the program is for old DOS systems it will run on Windows 7
(I do not have Windows 8 thus I cannot test this..). Currently I have SRIM running on Linux
using wine. Currently I have yet to run into a bug.

*This tool is still under heavy develpment and will change rapidly*

*This project can be broken into three parts:*
- Managing (single|batch) input to Srim for the TRIM calculations and moving output files
  to appropriate directories
- Parsing output text files from TRIM calculations
- Ploting and Vizualization for the output of TRIM calculations

# Managing input to Srim

## Generate Example TRIM input file
   A simple trim file will be outputted to STDOUT using the command
   > ./processsriminput.py -s

## Validator for TRIM input file (Not Implemented Yet)
   Often times TRIM will quit due to an inproperly formatted input file and gives
   vauge error messages. Running
   > ./processsriminput.py -v <file>

   will check the inputfile if it is improperly formatted
   
## Running Srim in Batch mode
   Srim on its own is very intensive in the amount of manual work that it
   takes to run an application. This module's goal is to automate much of the time
   being spent to "babysit" the program. Using:
   > ./batchsrim.py -e <exec_path> (-d <dir> | -f <file>)
   
   A user can submit a file or directory (where all *.in file are run). All
   Output files from the Trim calculation will be moved to <dir> or the root of <file>. Make sure
   to include the __full pathname__.
   
### Future feature
    The script will automatically resubmit input_files
    that fail util they complete.

# Parsing Output of Trim Calculation
  Curently 75% of Trim output is parsed and stored in a dictionary data-structure.
  This part will be filled in as the output is completely parsed.

# Statistics, Vizualization, and Plotting of Srim Output
  Currently this module is not implemented. 