#python3 -i saturation.py -d /home/eleonora/FLASH-Scintillators/EFLASH___130423/Saturation/
# ./data/subDirectory

import numpy as np
from matplotlib import pyplot as plt
import argparse
from scipy.optimize import curve_fit

import utilities.plot_size 
import utilities.utilities as utils

calibration_factor = 1 #Gy/nC
RADIUS_SELECTED = 40

outputDir = '/home/eleonora/Dottorato/articolo_foglio/Figures/Results/'

def my_func_for_axis(x): 
  return x/4 
  
def getData(directoryPath, MIN_DOSE= 0, MAX_DOSE=10, roi_selected=1.0):
  infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
  info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

  roi = []
  roiRadius = []
  signal = []
  signalErr = []
  doses = []

  for inputFile, dose in zip(info['data_file'], info['dose']):
    f = utils.search_file_in_directory(directoryPath+'outputFiles',  "dSub*%s" %inputFile.replace('TIF', 'txt'))
    data = utils.parse_config_file(f, utils.DATA_DICT)
      
    roi.append(data['roiNumber'])
    roiRadius.append(data['roiRadius'])
    signal.append(data['SignalIntegral'])
    signalErr.append(data['SignalIntegralError'])
    doses.append(np.ones(len(data['roiNumber']))*dose*calibration_factor)
    
  roi = np.concatenate(roi)
  roiRadius = np.concatenate(roiRadius)
  signal = np.concatenate(signal)
  signalErr = np.concatenate(signalErr)
  doses = np.concatenate(doses)
  dosesErr =  np.ones(len(doses))* 0.01 #mah!!!

  mask_dose = (doses> MIN_DOSE) * (doses < MAX_DOSE)
  mask = mask_dose * (roi==roi_selected) * (roiRadius ==RADIUS_SELECTED)

  return signal[mask], signalErr[mask], doses[mask], dosesErr[mask]

def doFit(x, y, dx, dy):
  opt, pcov = curve_fit(utils.line, x, y, sigma = dy)
  print('OPT PRIMA: ', opt, ' +- ', np.sqrt(pcov.diagonal()))
  sigma = np.sqrt(dy**2 + (opt[0]*dx)**2)
  opt, pcov = curve_fit(utils.line, x, y, sigma = sigma)
  print('OPT DOPO: ', opt, ' +- ', np.sqrt(pcov.diagonal()))
  return opt

def createFig(): 
  fig, ax = plt.subplots(3,1, sharex=True, figsize=(9,10), gridspec_kw={'height_ratios': [4,2,2]})
  fig.subplots_adjust(hspace=0.06)
  fig.subplots_adjust(left=0.2)
  fig.subplots_adjust(right=0.92)
  fig.subplots_adjust(bottom=0.2)
  fig.subplots_adjust(top=0.96)
  return fig, ax

def doPlotPerAROI(doses, dosesErr, signal, signalErr, doses_filter, dosesErr_filter, signal_filter, signalErr_filter, opt, opt_filter,  legend=''):
  #linearity for signal, filtered signal, background, filtered background
  ax[0].errorbar(doses, signal, xerr=dosesErr, yerr = signalErr, fmt = 'o', fillstyle='none', markersize=9.,markeredgewidth=1.5, color='mediumblue', label = 'Unfiltered %s' %legend)
  ax[0].errorbar(doses_filter, signal_filter, xerr=dosesErr_filter, yerr = signalErr_filter, fmt = 'o', fillstyle='none', markersize=9.,markeredgewidth=1.5, color='red', label = 'Filtered %s' %legend)

  my_x =  np.linspace(doses.min(), doses.max(), 1000)
  ax[0].errorbar(my_x, utils.line(my_x, *opt), fmt = '--', color='cornflowerblue', alpha = 0.5)
  ax[0].errorbar(my_x, utils.line(my_x, *opt_filter), fmt = '--', color='salmon', alpha = 0.5)

  #residuals for signal, filtered signal, background, filtered background
  ax[1].errorbar(doses, (signal-utils.line(doses, *opt))/signalErr, fmt='o', fillstyle='none', color='mediumblue', markersize=9,markeredgewidth=1.5)
  ax[1].errorbar(doses_filter, (signal_filter-utils.line(doses_filter, *opt_filter))/signalErr_filter, fmt='o', fillstyle='none', color='red', markersize=9,markeredgewidth=1.5)

  #difference signal-filtered signal, background-filtered background
  normDifference = (signal-signal_filter)/(signal+signal_filter) *2 * 100
  errSquared = signalErr**2 + signalErr_filter**2 
  normDifferenceErr = 2*100* np.sqrt(errSquared/(signal+signal_filter)**2 * (1+1/(signal+signal_filter)**2) )
  ax[2].errorbar(doses, normDifference, yerr=normDifferenceErr, fmt='o', fillstyle='none', color='darkgreen', markersize=9,markeredgewidth=1.5)

  return


if __name__ == "__main__":

  #linearità_2
  linearity = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/'

  #linearità_2_filter
  linearity_filter = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/filter/'

  #linearità
  linearity_short = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità/'
  
  fig, ax = createFig()

  signal, signalErr, doses, dosesErr = getData(linearity, roi_selected=1.0)
  print('fit signal unfiltered')
  opt_signal = doFit(doses, signal, dosesErr, signalErr)
  
  signal_filter, signalErr_filter, doses_filter, dosesErr_filter = getData(linearity_filter, roi_selected=1.0)
  print('fit signal filtered')
  opt_signal_filter = doFit(doses_filter, signal_filter, dosesErr, signalErr_filter)

  doPlotPerAROI(doses, dosesErr, signal, signalErr, doses_filter, dosesErr_filter, signal_filter, signalErr_filter, opt_signal, opt_signal_filter, legend='signal')


  my_x = np.linspace(doses.min(), doses.max(), 1000)
  ax[1].errorbar(my_x, utils.line(my_x, 0, 0), fmt='--', color ='darkgray')
  ax[1].set(ylabel='Residuals [$\sigma$]')
  ax[0].set(ylabel='Signal [au]')
  ax[0].grid()
  ax[0].legend()
  ax[0].set_xlim([0, 5.5])
  ax[1].grid()
  ax[2].set(xlabel = 'Dose per pulse [Gy]', ylabel='$\Delta$ [%]')
  ax[2].grid()

  secondary_x_axis = ax[1].secondary_xaxis(-1.65, functions=(my_func_for_axis,my_func_for_axis), color='k')
  secondary_x_axis.set_xlabel('Intra-pulse dose rate [MGy/s]', color='k' ) # da mettere gray 
  
  fig.savefig(outputDir+'linearity_signal.pdf')

  ####################################################################################################
  #background
  fig, ax = createFig()
  print('BACKGROUND ')

  signal, signalErr, doses, dosesErr = getData(linearity, roi_selected=2.0)
  print('fit background unfiltered')
  opt_signal = doFit(doses, signal, dosesErr, signalErr)
  
  signal_filter, signalErr_filter, doses_filter, dosesErr_filter = getData(linearity_filter, roi_selected=2.0)
  print('fit backgorund filtered')
  opt_signal_filter = doFit(doses_filter, signal_filter, dosesErr, signalErr_filter)

  doPlotPerAROI(doses, dosesErr, signal, signalErr, doses_filter, dosesErr_filter, signal_filter, signalErr_filter, opt_signal, opt_signal_filter, legend='background')

  my_x = np.linspace(doses.min(), doses.max(), 1000)
  ax[1].errorbar(my_x, utils.line(my_x, 0, 0), fmt='--', color ='darkgray')
  ax[1].set(ylabel='Residuals [$\sigma$]')
  ax[0].set(ylabel='Signal [au]')
  ax[0].grid()
  ax[0].legend()
  ax[0].set_xlim([0, 5.5])
  #ax[0].set_ylim([0, 3.5e+8])
  ax[1].grid()
  ax[2].set(xlabel = 'Dose per pulse [Gy]', ylabel='$\Delta$ [%]')
  ax[2].grid()

  secondary_x_axis = ax[1].secondary_xaxis(-1.65, functions=(my_func_for_axis,my_func_for_axis), color='k')
  secondary_x_axis.set_xlabel('Intra-pulse dose rate [MGy/s]', color='k' ) # da mettere gray 
  
  fig.savefig(outputDir+'linearity_background.pdf')

  """
  signal_short, signalErr_short, doses_short, dosesErr_short = getData(linearity_short)

  #opt_short = doFit(doses_short, signal_short, dosesErr, signalErr_short)
  #ax[0].errorbar(doses_short, signal_short, xerr=dosesErr_short, yerr = signalErr_short, fmt = 'o', fillstyle='none', markersize=9.,markeredgewidth=1.5, color='green', label = 'Roi 70 pixel')
  #ax[0].errorbar(my_x, utils.line(my_x, *opt_short), fmt = '--', color='limegreen', alpha = 0.5)
  #ax[1].errorbar(doses_short, (signal_short-utils.line(doses_short, *opt_short))/signalErr_short, fmt='o', fillstyle='none', color='green', markersize=9,markeredgewidth=1.5)
  """

  plt.show()