import srimbatch.py
import shutil
import os
import glob

def runSrimOnDir(datapath, srimpath):
    "Run srim on all inputfiles given in datapath. srimpath is the directory or TRIM.exe"
    print 'Working in data directory: ' + datapath + '\n'
    print 'Processing the following input files:'
    files = glob.glob(datapath + '*.in')
    print files
    os.chdir(srimpath)
    for f in files:
        shutil.copyfile(f, srimpath + '\\TRIM.in')
        os.system(srimpath + '\\TRIM.exe')
        outputfiles = ['range','tdata','ioniz','vacancy','phonon','novac']
        for outfile in outputfiles:
            if os.path.isfile(outfile + '.txt'):
                shutil.copyfile(srimpath + '\\' + outfile + '.txt', datapath + '\\' + outfile + '_' + os.path.basename(f).split('.')[0] + '.txt')
            else:
                print 'No ' + outfile + ' results were not saved for' + os.path.basename(f) + '...'
        readSlimTestFiles(os.path.basename(f).split('.')[0], datapath)