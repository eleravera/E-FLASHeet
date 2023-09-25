#python3 -i launch_process_image.py -d /.../ -r 15
import subprocess
import os
import numpy as np
import argparse

import utilities.utilities as utils

if __name__ == "__main__":

    options_parser = argparse.ArgumentParser(description = '')
    options_parser.add_argument('-input_directory', '-d', default=None, type=str, help='input_directory')
    options_parser.add_argument('-radius', '-r', default=15, type=int, help='ROI radius')
    options = vars(options_parser.parse_args())
    directoryPath = options['input_directory']
    roi_radius = options['radius']

    fiberPositionsFile = utils.search_file_in_directory(directoryPath, '/fiberPositions.txt')
    pos = utils.parse_config_file(fiberPositionsFile, utils.FIBER_POS_DICT)
    infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
    info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)
    
    #Analyze data file only
    for inputFile in info['data_file']:
        inputFile = directoryPath + inputFile
        
        cmd = 'python3 process_image.py -f %s -p %s ' % (inputFile, fiberPositionsFile)
        subprocess.run(cmd, shell = True)

    #Analyze dark file only
    for darkFile in np.unique(info['dark_file']):
        inputFile = directoryPath + darkFile
        
        cmd = 'python3 process_image.py -f %s -p %s ' % (inputFile, fiberPositionsFile) 
        subprocess.run(cmd, shell = True)

    #Make the subtraction data-dark
    for inputFile in info['data_file']:
        darkFile = directoryPath + info['dark_file'][np.where(info['data_file']==os.path.basename(inputFile))[0]][0]
        inputFile = directoryPath + inputFile
                
        cmd = 'python3 process_image.py -f %s -d %s -p %s ' % (inputFile, darkFile, fiberPositionsFile) 
        subprocess.run(cmd, shell = True)