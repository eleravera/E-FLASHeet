import numpy as np
import argparse
import os
from scipy.ndimage import white_tophat
from matplotlib import pyplot as plt
from scipy.signal import medfilt2d

import lib.Image_lib
import utilities.plot_size
import utilities.utilities as utils

def createFig(): 
  fig, ax = plt.subplots(1, figsize = (12,10)) 
  fig.subplots_adjust(left=0.11)
  fig.subplots_adjust(right=0.93)
  fig.subplots_adjust(bottom=0.11)
  fig.subplots_adjust(top=0.93)
  return fig, ax

def doPlots(dict, centerMin, centerMax, sideMin, sideMax): 
  inputFile = dict['inputFile']
  darkFile = dict['darkFile']
  cordinatesFile = dict['positionFile']
  imBounds = dict['imBounds']
  histBounds = dict['histBounds']
  pos = utils.parse_config_file(cordinatesFile, utils.ROI_POS_DICT)

  image = lib.Image_lib.Image(inputFile)
  dark = lib.Image_lib.Image(darkFile)
  signalImage = image.image - dark.image
  bins = np.linspace(histBounds[0]-0.5, histBounds[1]-0.5, 100)


  fig_hist, ax_hist = createFig()
  ax_hist.set(xlabel='CCD Gray counts')
  ax_hist.set_yscale('log')
  ax_hist.hist(np.concatenate(signalImage), bins=bins, label = 'Unfiltered', alpha = 0.2, color='C0')

  fig_profile, ax_profile = createFig()
  ax_profile.set(xlabel='col')
  ax_profile.plot(signalImage[:, pos['y_position'][0]], label = 'Unfiltered')

  fig_profile_single, ax_profile_single = createFig()
  ax_profile_single.set(xlabel='col')
  ax_profile_single.plot(signalImage[:, pos['y_position'][0]], label = 'Unfiltered')
  ax2 = ax_profile_single.inset_axes([0.5,0.5,0.5, 0.5],)
  ax2.plot(signalImage[sideMin:sideMax, pos['y_position'][0]], label = 'Unfiltered')


  fig_profile_center, ax_profile_center = createFig()
  ax_profile_center.set(xlabel='col')
  ax_profile_center.plot(signalImage[centerMin:centerMax, pos['y_position'][0]], label = 'Unfiltered')

  fig_profile_side, ax_profile_side = createFig()
  ax_profile_side.set(xlabel='col')
  ax_profile_side.plot(signalImage[sideMin:sideMax, pos['y_position'][0]], label = 'Unfiltered')

  fig_5x5median, ax_5x5median = createFig()
  fig_5x5median.gca().invert_yaxis()
  ax_5x5median.set(xlabel='', title ='')

  fig_5x5tophat, ax_5x5topha = createFig()
  ax_5x5topha.set(xlabel='',  title ='')
  fig_5x5tophat.gca().invert_yaxis()


  fig_5x5median_zoom, ax_5x5median_zoom = createFig()
  fig_5x5median_zoom.gca().invert_yaxis()
  ax_5x5median_zoom.set(xlabel='', title ='median')

  fig_5x5tophat_zoom, ax_5x5topha_zoom = createFig()
  ax_5x5topha_zoom.set(xlabel='',  title ='tophat')

  #fig_profile5x5, ax_profile5x5 = createFig()
  #ax_profile5x5.set(xlabel='col')
  #ax_profile5x5.plot(signalImage[sideMin:sideMax, pos['y_position'][0]], label = 'Unfiltered')

  for n, c in zip(kernel_dimensions, colors): 
    filtIm_median = medfilt2d(signalImage,  kernel_size=[n,n])
    filterTopHat = white_tophat(signalImage, size=(n,n))
    filtIm_topHat = signalImage-filterTopHat

    
    if n == 5: 
      median5x5 = filtIm_median
      tophat5x5 = filtIm_topHat

      ax_profile_single.plot(filtIm_topHat[:, pos['y_position'][1]], label = 'top hat %dx%d' %(n,n), linewidth = 1.5, linestyle='-', color= c)  
      ax_profile_single.plot(filtIm_median[:, pos['y_position'][1]], label = 'median hat %dx%d' %(n,n), linewidth = 1.5, linestyle='--', color= c)
      ax2.plot(filtIm_topHat[sideMin:sideMax, pos['y_position'][1]], label = 'top hat %dx%d' %(n,n), linewidth = 1.5, linestyle='-', color= c)  
      ax2.plot(filtIm_median[sideMin:sideMax, pos['y_position'][1]], label = 'median hat %dx%d' %(n,n), linewidth = 1.5, linestyle='--', color= c)
      

    ax_hist.hist(np.concatenate(filtIm_topHat), bins=bins, label = 'top hat %dx%d' %(n,n), histtype='step', linewidth = 1.5, linestyle='-', color =c)
    ax_hist.hist(np.concatenate(filtIm_median), bins=bins, label = 'median %dx%d' %(n,n), histtype='step', linewidth = 1.5, linestyle='--', color= c)

    ax_profile.plot(filtIm_topHat[:, pos['y_position'][1]], label = 'top hat %dx%d' %(n,n), linewidth = 1.5, linestyle='-', color= c)  
    ax_profile.plot(filtIm_median[:, pos['y_position'][1]], label = 'median hat %dx%d' %(n,n), linewidth = 1.5, linestyle='--', color= c)

    ax_profile_center.plot(filtIm_topHat[centerMin:centerMax, pos['y_position'][1]], label = 'top hat %dx%d' %(n,n), linewidth = 1.5, linestyle='-', color= c)  
    ax_profile_center.plot(filtIm_median[centerMin:centerMax, pos['y_position'][1]], label = 'median hat %dx%d' %(n,n), linewidth = 1.5, linestyle='--', color= c)

    ax_profile_side.plot(filtIm_topHat[sideMin:sideMax, pos['y_position'][1]], label = 'top hat %dx%d' %(n,n), linewidth = 1.5, linestyle='-', color= c)  
    ax_profile_side.plot(filtIm_median[sideMin:sideMax, pos['y_position'][1]], label = 'median hat %dx%d' %(n,n), linewidth = 1.5, linestyle='--', color= c)

  ax_hist.legend()
  ax_profile.legend(loc='upper left')
  ax_profile.grid()
  ax_profile_single.legend(loc='upper left')
  ax_profile_single.grid()
  ax2.grid()
  #remove yticks
  
  ax_profile_center.legend()
  ax_profile_center.grid()
  ax_profile_side.legend()
  ax_profile_side.grid()


  im = ax_5x5median_zoom.imshow(median5x5[370:470, 100:200], vmin = imBounds[0], vmax = imBounds[1])
  fig_5x5median_zoom.colorbar(im)


  im = ax_5x5topha_zoom.imshow(tophat5x5[370:470, 100:200], vmin = imBounds[0], vmax = imBounds[1])
  fig_5x5tophat_zoom.colorbar(im)

  im = ax_5x5median.imshow(median5x5, vmin = imBounds[0], vmax = imBounds[1])
  fig_5x5median.colorbar(im)


  im = ax_5x5topha.imshow(tophat5x5, vmin = imBounds[0], vmax = imBounds[1])
  fig_5x5tophat.colorbar(im)

  fig_hist.savefig(outputDir+'filtered_hist_'+dict['name']+'.pdf')
  fig_profile.savefig(outputDir+'profile_'+dict['name']+'.pdf')
  fig_profile_center.savefig(outputDir+'profile_center_'+dict['name']+'.pdf')
  fig_profile_side.savefig(outputDir+'profile_side_'+dict['name']+'.pdf')
  fig_5x5median.savefig(outputDir+'Image_5x5median_'+dict['name']+'.pdf')
  fig_5x5median_zoom.savefig(outputDir+'Image_5x5median_zoom_'+dict['name']+'.pdf')
  fig_5x5tophat.savefig(outputDir+'Image_5x5tophat_'+dict['name']+'.pdf')
  fig_5x5tophat_zoom.savefig(outputDir+'Image_5x5tophat_zoom_'+dict['name']+'.pdf')
  fig_profile_single.savefig(outputDir+'profile_5x5_'+dict['name']+'.pdf')
  return 

low_dose_05mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0009.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0008.TIF",
                 "positionFile" : "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/fiberPositions.txt",
                 "dose" : 0.07, #Gy
                 "mm" : 0.5, 
                 'imBounds' : [0, 2000],
                 'histBounds': [0, 3000],
                 'name' : 'low_dose_05mm',
                 'xticks': np.arange(0, 3000, 500),
                 'rowProfile' : 200}

high_dose_05mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0001.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/t0000.TIF", 
                  "positionFile" : "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/fiberPositions.txt",
                 "dose" : 2.3, #Gy
                 "mm" : 0.5,
                 'imBounds' : [0, 45000],
                 'histBounds': [0, 65000],
                 'name' : 'high_dose_05mm',
                 'xticks': np.arange(0, 65000, 20000),
                 'rowProfile' : 200}


"""low_dose_3mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0034.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0033.TIF", 
                 "positionFile" : "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/fiberPositions.txt",
                 "dose" : 0.18, #Gy
                 "mm" : 3 ,
                 'imBounds' : [0, 1500],
                 'histBounds': [0, 3000],
                 'name' : 'low_dose_3mm',
                 'xticks': np.arange(0, 3000, 500),
                 'rowProfile' : 200}
"""

low_dose_3mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0032.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0029.TIF", 
                 "positionFile" : "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/fiberPositions.txt",
                 "dose" : 0.82, #Gy
                 "mm" : 3 ,
                 'imBounds' : [0, 1500],
                 'histBounds': [0, 5000],
                 'name' : 'low_dose_3mm',
                 'xticks': np.arange(0, 3000, 500),
                 'rowProfile' : 200}


high_dose_3mm = {"inputFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0001.TIF",
                 "darkFile" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/t0000.TIF", 
                 "positionFile" : "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/fiberPositions.txt",
                 "dose" : 4.93, #Gy
                 "mm" : 3,
                  'imBounds' : [0, 20000],
                 'histBounds': [0, 32000],
                 'name' : 'high_dose_3mm',
                 'xticks': np.arange(0, 32000, 10000), 
                 'rowProfile' : 200}

kernel_dimensions = [3, 5, 9]
colors = ['green', 'orangered', 'darkorchid']

outputDir = '/home/eleonora/Dottorato/articolo_foglio/Figures/Matherials_and_methods/'


#0.5 mm
for dict in (low_dose_05mm, high_dose_05mm):
  centerMin, centerMax = 120, 160
  sideMin, sideMax = 115, 145
  doPlots(dict, centerMin, centerMax, sideMin, sideMax )


#3 mm
for dict in (low_dose_3mm, high_dose_3mm):
  centerMin, centerMax = 160, 260
  sideMin, sideMax = 130, 170
  doPlots(dict, centerMin, centerMax, sideMin, sideMax )




plt.show()
