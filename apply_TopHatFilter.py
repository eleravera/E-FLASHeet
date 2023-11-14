import argparse
import os
from scipy.ndimage import white_tophat

import lib.Image_lib
import utilities.utilities as utils

options_parser = argparse.ArgumentParser(description = '')
options_parser.add_argument('-input_directory', '-d', default=None, type=str, help='input_directory')
options_parser.add_argument('-filter_order', '-o', default=1, type=int, help='filter order')

options = vars(options_parser.parse_args())
directoryPath = options['input_directory']
filterSize = options['filter_order']

infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

for inputFile in info['data_file']:
    inputFile = directoryPath + inputFile
    #darkFile = directoryPath + darkFile

    image = lib.Image_lib.Image(inputFile)
    filter = white_tophat(image.image, size=(filterSize,filterSize))
    filteredImage = image.image - filter
    outputFile = image.createOutputFile('TIF', path=os.path.dirname(inputFile)+"/%d_filter/" %(filterSize) )
    image.saveImageAsTIF(outputFile, filteredImage)

