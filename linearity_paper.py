#python3 -i saturation.py -d /home/eleonora/FLASH-Scintillators/EFLASH___130423/Saturation/
# ./data/subDirectory

import numpy as np
from matplotlib import pyplot as plt
import argparse
from scipy.optimize import curve_fit

import utilities.plot_size 
import utilities.utilities as utils

calibration_factor = 1 #Gy/nC
ROI_SELECTED = 1
RADIUS_SELECTED = 70


def my_func_for_axis(x): 
  return x/4 
  
def getData(directoryPath, MIN_DOSE= 0, MAX_DOSE=10):
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
  mask = mask_dose * (roi==ROI_SELECTED) * (roiRadius ==RADIUS_SELECTED)

  return signal[mask], signalErr[mask], doses[mask], dosesErr[mask]


#linearità_2
linearity = '/home/eleonora/Scrivania/FLASH_2023_06_29/linearità_2/'

#linearità
linearity_short = '/home/eleonora/Scrivania/FLASH_2023_06_29/linearità/'


signal, signalErr, doses, dosesErr = getData(linearity)
signal_short, signalErr_short, doses_short, dosesErr_short = getData(linearity_short)


opt, pcov = curve_fit(utils.line, doses, signal, sigma = signalErr)
print('OPT PRIMA: ', opt)
sigma = np.sqrt(signalErr**2 + (opt[0]*dosesErr)**2)
opt, pcov = curve_fit(utils.line, doses, signal, sigma = sigma)
print('OPT DOPO: ', opt)

opt_short, pcov_short = curve_fit(utils.line, doses_short, signal_short, sigma = signalErr_short)
print('OPT PRIMA: ', opt)
sigma_short = np.sqrt(signalErr_short**2 + (opt[0]*dosesErr_short)**2)
opt_short, pcov_short = curve_fit(utils.line, doses_short, signal_short, sigma = sigma_short)
print('OPT DOPO: ', opt)



fig, ax = plt.subplots(2,1, sharex=True, figsize=(9,10), gridspec_kw={'height_ratios': [3,1]})
fig.subplots_adjust(hspace=0.08)
fig.subplots_adjust(left=0.2)
fig.subplots_adjust(right=0.92)
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(top=0.95)

ax[0].errorbar(doses, signal, xerr=dosesErr, yerr = signalErr, fmt = 'o', fillstyle='none', markersize=9.,markeredgewidth=1.5, color='mediumblue', label = 'Roi 70 pixel')
ax[0].errorbar(doses_short, signal_short, xerr=dosesErr_short, yerr = signalErr_short, fmt = 'o', fillstyle='none', markersize=9.,markeredgewidth=1.5, color='green', label = 'Roi 70 pixel')

my_x =  np.linspace(doses.min(), doses.max(), 1000)
ax[0].errorbar(my_x, utils.line(my_x, *opt), fmt = '--', color='cornflowerblue', alpha = 0.5)
ax[0].errorbar(my_x, utils.line(my_x, *opt_short), fmt = '--', color='limegreen', alpha = 0.5)

ax[1].errorbar(doses, (signal-utils.line(doses, *opt))/signalErr, fmt='o', fillstyle='none', color='mediumblue', markersize=9,markeredgewidth=1.5)
ax[1].errorbar(doses_short, (signal_short-utils.line(doses_short, *opt_short))/signalErr_short, fmt='o', fillstyle='none', color='green', markersize=9,markeredgewidth=1.5)

ax[1].errorbar(my_x, utils.line(my_x, 0, 0), fmt='--', color ='darkgray')
ax[1].set(xlabel = 'Dose per pulse [Gy]', ylabel='Residuals [$\sigma$]')
ax[0].set(ylabel='Signal [au]')
ax[0].grid()
ax[0].legend()
ax[0].set_xlim([0, 5.5])
ax[0].set_ylim([0, 6.e+8])
ax[1].grid()

secondary_x_axis = ax[1].secondary_xaxis(-0.8, functions=(my_func_for_axis,my_func_for_axis), color='k')
secondary_x_axis.set_xlabel('Intra-pulse dose rate [MGy/s]', color='k' ) # da mettere gray 


plt.show()