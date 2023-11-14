import numpy as np
import argparse
import os
from scipy.ndimage import white_tophat
from matplotlib import pyplot as plt
from scipy.signal import medfilt2d

import lib.Image_lib
import utilities.plot_size

def createFig(): 
  fig, ax = plt.subplots(1,1, figsize=(9,8))
  fig.subplots_adjust(left=0.11)
  fig.subplots_adjust(right=0.93)
  fig.subplots_adjust(bottom=0.11)
  fig.subplots_adjust(top=0.93)
  return fig, ax

low_dose_05mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0009.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0008.TIF", 
                 "dose" : 0.07, #Gy
                 "mm" : 0.5 , 
                 'imBounds' : [0, 2000], 
                 'histBounds': [0, 15000],
                 'name' : 'low_dose_05mm',
                 'xticks' : np.arange(0, 16000, 5000) }

high_dose_05mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0001.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0000.TIF", 
                 "dose" : 2.3, #Gy
                 "mm" : 0.5,
                 'imBounds' : [0, 45000],
                 'histBounds': [0, 65000],
                 'name' : 'high_dose_05mm',
                 'xticks': np.arange(0, 65000, 20000)}


low_dose_3mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0034.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0033.TIF", 
                 "dose" : 0.18, #Gy
                 "mm" : 3, 
                 'imBounds' : [0, 1500],
                 'histBounds': [0, 3000],
                 'name' : 'low_dose_3mm',
                 'xticks': np.arange(0, 3000, 500)}

high_dose_3mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0001.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0000.TIF", 
                 "dose" : 4.93, #Gy
                 "mm" : 3,
                 'imBounds' : [0, 20000],
                 'histBounds': [0, 32000],
                 'name' : 'high_dose_3mm',
                 'xticks': np.arange(0, 32000, 10000) }


outputDir = '/home/eleonora/Dottorato/articolo_foglio/Figures/Matherials_and_methods/'


#0.5 mm

for dict in (low_dose_05mm, high_dose_05mm):

  inputFile = dict['inputFile']
  darkFile = dict['darkFile']
  imBounds = dict['imBounds']
  histBounds = dict['histBounds']

  image = lib.Image_lib.Image(inputFile)
  dark = lib.Image_lib.Image(darkFile)

  signalImage = image.image - dark.image

  fig, ax = createFig()
  im = ax.imshow(signalImage, vmin = imBounds[0], vmax = imBounds[1])
  fig.gca().invert_yaxis()
  fig.colorbar(im)
  plt.savefig(outputDir+'Image_'+dict['name']+'.pdf')

  fig, ax = createFig()
  im = ax.imshow(signalImage[370:470, 100:200], vmin = imBounds[0], vmax = imBounds[1])
  fig.gca().invert_yaxis()
  fig.colorbar(im)
  plt.savefig(outputDir+'ImageZoom_'+dict['name']+'.pdf')

  fig, ax = createFig()
  bins = np.linspace(histBounds[0]-0.5, histBounds[1]-0.5, 100)
  ax.hist(np.concatenate(signalImage), bins = bins, alpha = 0.4)
  ax.set_yscale('log') 
  ax.set(xlabel='Gray level')
  ax.set_xticks(dict['xticks'])
  plt.savefig(outputDir+'Hist_'+dict['name']+'.pdf')

  





#3 mm
"""
for dict in (low_dose_3mm, high_dose_3mm):

  inputFile = dict['inputFile']
  darkFile = dict['darkFile']
  imBounds = dict['imBounds']
  histBounds = dict['histBounds']

  image = lib.Image_lib.Image(inputFile)
  dark = lib.Image_lib.Image(darkFile)

  signalImage = image.image - dark.image

  fig, ax = createFig()
  im = ax.imshow(signalImage, vmin = imBounds[0], vmax = imBounds[1])
  fig.gca().invert_yaxis()
  fig.colorbar(im)
  plt.savefig(outputDir+'Image_'+dict['name']+'.pdf')

  fig, ax = createFig()
  im = ax.imshow(signalImage[370:470, 100:200], vmin = imBounds[0], vmax = imBounds[1])
  fig.gca().invert_yaxis()
  fig.colorbar(im)
  plt.savefig(outputDir+'ImageZoom_'+dict['name']+'.pdf')

  fig, ax = createFig()
  bins = np.linspace(histBounds[0]-0.5, histBounds[1]-0.5, 100)
  ax.hist(np.concatenate(signalImage), bins = bins, alpha = 0.4)
  ax.set_yscale('log') 
  ax.set(xlabel='Gray level')
  ax.set_xticks(dict['xticks'])
  plt.savefig(outputDir+'Hist_'+dict['name']+'.pdf')

  median3x3 = medfilt2d(signalImage,  kernel_size=[3,3])
  tophat3x3 = signalImage- white_tophat(signalImage, size=(3,3))

  fig_3x3median, ax_3x3median = createFig()
  ax_3x3median.set(xlabel='', title ='median')
  im = ax_3x3median.imshow(median3x3[370:470, 100:200], vmin = imBounds[0], vmax = imBounds[1])
  fig_3x3median.gca().invert_yaxis()
  fig_3x3median.colorbar(im)


  fig_3x3tophat, ax_3x3topha = createFig()
  ax_3x3topha.set(xlabel='',  title ='tophat')
  im = ax_3x3topha.imshow(tophat3x3[370:470, 100:200], vmin = imBounds[0], vmax = imBounds[1])
  fig_3x3tophat.gca().invert_yaxis()
  fig_3x3tophat.colorbar(im)
"""
plt.show()