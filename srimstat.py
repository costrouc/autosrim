from collections import namedtuple
import numpy as np
import shutil
import os
import glob

srim_module_path = "C:/Users/Chris/Desktop/srim/"

Vacancy = namedtuple("Vacancy","names units data")
Range = namedtuple("Range","names units data")
Novac = namedtuple("Novac","names units data")
Layer = namedtuple("Layer","id material depth density")
Density = namedtuple("Density","val units")

def runSrimOnDirectory(datapath):
    "Run srim on all inputfiles given in data_path. srim_module_path is the directory or TRIM.exe"
    print 'Working in data directory: ' + datapath + '\n'
    print 'Executable in directory: ' + srim_module_path + '\n'
    print 'Processing the following input files:'
    files = glob.glob(datapath + '*.in')
    print files
    os.chdir(srim_module_path)
    for f in files:
        runSrimOnFile(f)
        
def runSrimOnFile(filename):
    "Run Srim on filename"
    shutil.copyfile(filename, srim_module_path + '\\TRIM.in')
    os.system(srim_module_path + '\\TRIM.exe')
    outputfiles = ['range','tdata','ioniz','vacancy','phonon','novac']
    for outfile in outputfiles:
        if os.path.isfile(outfile + '.txt'):
            shutil.copyfile(srim_module_path + '\\' + outfile + '.txt', os.path.split(filename)[0] + '\\' + outfile + '_' + os.path.basename(filename).split('.')[0] + '.txt')
        else:
            print 'No ' + outfile + ' results were not saved for' + os.path.basename(filename) + '...'
    readSlimTestFiles(os.path.basename(filename).split('.')[0], os.path.split()[0])

def readSlimTestFiles(testname, datapath):
    "Reads in the appropriate slim files"
    fluence = float(raw_input("Enter the Fluence of the Ion Beam [ion/cm^3]:"))
    materialinfo = readTDataFile(datapath + '\\' + 'tdata_' + testname + '.txt')
    slim_vacancy = readVacancyFile(datapath + '\\' + 'vacancy_' + testname + '.txt')
    slim_range = readRangeFile(datapath + '\\' + 'range_' + testname + '.txt')
    slim_novac = readNovacFile(datapath + '\\' + 'novac_' + testname + '.txt')
    plotDPA(fluence, materialinfo, slim_vacancy, slim_range, slim_novac)

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
    
def plotDPA(fluence, materialinfo, slim_vacancy, slim_range, slim_novac):
    "Plots DPA curve of given srim data"
    
