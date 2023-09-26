#fai la media delle 3 distribuzioni 

#per ogni file nel info sottrai il fondo e poi quelli con stessa dose fai la media delle immagini

import numpy as np
import argparse
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import utilities.utilities as utils
import lib.Image_lib

EXTENT = [118, 333, 185, 400]

if __name__ == "__main__":

    options_parser = argparse.ArgumentParser(description = '')
    options_parser.add_argument('-input_directory', '-d', default=None, type=str, help='input_directory')
    options = vars(options_parser.parse_args())
    directoryPath = options['input_directory']

    magnificationFile = utils.search_file_in_directory(directoryPath, '/magnification.txt')
    mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT )
    infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
    info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)
    
    images = []
    doses = []
    errors = []

    #Analyze data file only
    for inputFile, darkFile, d in  zip(info['data_file'], info['dark_file'], info['dose'] ):
        inputFile = directoryPath + inputFile
        darkFile = directoryPath + darkFile
        image = lib.Image_lib.Image(inputFile)
        dark = lib.Image_lib.Image(darkFile)
        signalImage = image.image - dark.image
        errorImage = image.image + dark.image
        images.append(signalImage)
        doses.append(d)
        errors.append(errorImage)
    
    images = np.array(images)
    meanImages = []

    uniqueDoses = np.unique(doses)
    for d in uniqueDoses:
      mean = np.mean(images[doses==d], axis=0) 
      meanImages.append(mean[EXTENT[0]:EXTENT[1], EXTENT[2]:EXTENT[3]])

    outputFile = '/home/eleonora/Scrivania/FLASH_2023_06_29/pdd/outputFiles/PDD.npz'
    np.savez(outputFile, images =meanImages, doses=uniqueDoses )

    #SALVA SU FILE IN OUTPUTDIRECTORYY
    #MERGIA CON PDD.PY

