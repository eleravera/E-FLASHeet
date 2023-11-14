import argparse 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import lib.Image_lib
import utilities.plot_size
import utilities.utilities as utils


minibeam = {'inputDir' : '/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/minibeam_05mm/', 
            'dataFile' : 't0001.TIF', 
            'darkFile' : 't0000.TIF', 
            'selection' : [170,250, 208,288],
            'imBounds' : [5000, 30000],
            'title' : 'DPP = 2.3 Gy'
}


miniPDD = {'inputDir' : '/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/minipdd_3mm/', 
            'dataFile' : 't0001.TIF', 
            'darkFile' : 't0000.TIF', 
            'selection' : [160, 290, 188, 318],
            'imBounds' : [1000, 16000],#650],
            'title' : 'DPP = 2.3 Gy'
}

def plot(dict): 

  magnificationFile = utils.search_file_in_directory(dict['inputDir'], '/magnification.txt')
  mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT )

  inputFile = dict['inputDir'] + dict['dataFile']
  darkFile = dict['inputDir'] + dict['darkFile']
  image = lib.Image_lib.Image(inputFile)

  dark = lib.Image_lib.Image(darkFile)
  signalImage = image.image - dark.image

  signalImage = signalImage[dict['selection'][0]:dict['selection'][1], dict['selection'][2]:dict['selection'][3]]
  extent    =  (-signalImage.shape[0]*0.5, +signalImage.shape[0]*0.5, -signalImage.shape[0]*0.5, +signalImage.shape[0]*0.5)

  plt.figure(figsize = (9,8))
  plt.imshow(signalImage, vmin = dict['imBounds'][0], vmax = dict['imBounds'][1], extent = extent)
  plt.title(dict['title'])
  plt.xlabel('[mm]')
  plt.ylabel('[mm]')
  #plt.colorbar()
  plt.savefig(dict['inputDir']+dict['dataFile'][:-3]+'pdf')
  return 

plot(minibeam)
plot(miniPDD)


plt.show()