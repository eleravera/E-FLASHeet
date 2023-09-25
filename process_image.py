#python3 -i process_image.py -f /home/eleonora/Scrivania/testPy/Calib100_20Gy_20p_4us_s1_2.TIF -d /home/eleonora/Scrivania/testPy/Buio_s1.TIF -p /home/eleonora/Scrivania/testPy/fiberPositions.txt 

#L'idea di questo script è che venga lanciato in automatico ad ogni immagine che viene fatta, e che per ogni immagine abbia poi un file pdf e uno txt contenente le informazioni delle ROI. 
import argparse 
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import os

from scipy.signal import medfilt2d

import lib.ROI_lib as roi_lib
import lib.Image_lib
import utilities.utilities as utils

options_parser = argparse.ArgumentParser(description = '')
options_parser.add_argument('-input_file', '-f', default=None, type=str, help='input_file')
options_parser.add_argument('-dark_file', '-d', default=None, type=str, help='dark_file')
options_parser.add_argument('-cordinates', '-p', default=None, type=str, help='fibers_positions')

options = vars(options_parser.parse_args())
cordinatesFile = options['cordinates']
inputFile = options['input_file']
darkFile = options['dark_file']

pos = utils.parse_config_file(cordinatesFile, utils.FIBER_POS_DICT)

image = lib.Image_lib.Image(inputFile)
print("Processing input file: %s" % inputFile)

if darkFile is not None: 
    print(image.createOutputFile("pdf", path=os.path.dirname(inputFile)+"/outputFiles/dSub_"))
    pdf = PdfPages(image.createOutputFile("pdf", path=os.path.dirname(inputFile)+"/outputFiles/dSub_"))
    txt = open(image.createOutputFile("txt", path=os.path.dirname(inputFile)+"/outputFiles/dSub_"),'a')
else:
    print(image.createOutputFile("pdf", path=os.path.dirname(inputFile)+"/outputFiles/"))
    pdf = PdfPages(image.createOutputFile("pdf", path=os.path.dirname(inputFile)+"/outputFiles/"))
    txt = open(image.createOutputFile("txt", path=os.path.dirname(inputFile)+"/outputFiles/"),'a')
image.savePlot(pdf, image.plotImage(bounds=(None, None)), title ='Image')

if darkFile is not None: 
    info = "DATA: %s\n\nBUIO: %s\n\nROI POSITIONS: %s" % (inputFile, darkFile, cordinatesFile )
    dark = lib.Image_lib.Image(darkFile)
    signalImage = image.image - dark.image
    errorImage = image.image + dark.image
    image.savePlot(pdf, dark.plotImage(bounds=(None, None)), title = 'Dark')
    #image.savePlot(pdf, signalImage.plotImage(bounds=(None, None)), title = 'Signal = Image-Dark')
else:
    info = "DATA: %s\n\nROI POSITIONS: %s" % (inputFile, cordinatesFile )
    signalImage = image.image
    errorImage  = signalImage


image.saveSomeInfo(pdf, info)

txt.write("#roiNumber roiRadius pixelNumber SignalIntegral SignalIntegralError SignalMean SignalMeanError \n")
data = []

for n, x, y, r in zip(pos['roi_number'], pos['x_position'], pos['y_position'], pos['radius']):
    roi = roi_lib.Roi(signalImage, errorImage, number=n, center = (x, y), radius= int(r))
    data.append(roi.ROIanalysis())
    roi.saveInfo(outputFilePdf=pdf, outputFileTxt=txt)
    roi.savePlot(pdf, roi.plotImage())
    roi.savePlot(pdf, roi.histImage())
    image.ROI_list.append(roi)

pdf.close()
txt.close()
