import numpy as np
import argparse
from scipy.optimize import curve_fit

import pandas as pd
import os
from scipy.ndimage import white_tophat
from matplotlib import pyplot as plt
from scipy.signal import medfilt2d

import lib.Image_lib
import utilities.plot_size
import utilities.utilities as utils
import utilities.fit_functions as functions

def createFig(): 
  fig, ax = plt.subplots(1,1, figsize=(12,10))
  fig.subplots_adjust(left=0.15)
  fig.subplots_adjust(right=0.98)
  fig.subplots_adjust(bottom=0.1)
  fig.subplots_adjust(top=0.9)
  ax.grid()
  return fig, ax

diamondFile = '/home/eleonora/FLASH-Scintillators/APP40mm.xlsx'
df = pd.read_excel(diamondFile, index_col=None)

fig, ax = createFig()
x_diamond = np.array(df['Unnamed: 0'][2:])
y_diamond = np.array(df['Unnamed: 2'][2:])
ax.errorbar(x_diamond, y_diamond, fmt='.')

magnificationFile = utils.search_file_in_directory('/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2', '/magnification.txt')
mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT )

dataFile = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/3_filter/t0010.TIF'
darkFile = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/3_filter/t0009.TIF'
image = lib.Image_lib.Image(dataFile)
dark = lib.Image_lib.Image(darkFile)
signalImage = image.image - dark.image



from profile_paper import plot_profile as plot_profile
from profile_paper import scint_3mm as scint_3mm

fig_row, ax_row = createFig()
fig_col, ax_col = createFig()


x, y, profile_row, profile_col, profile_row_err, profile_col_err = plot_profile(signalImage, -scint_3mm['center_y'], -scint_3mm['center_x'], mInfo['magnification'], scint_3mm, 2, ax_row, ax_col, norm_col = 1, norm_row =1)


fig_row, ax_row = createFig()
ax_row.set_xlim(-50, 50)

fig_col, ax_col = createFig()
ax_col.set_xlim(-50, 50)

ax_row.errorbar(x, (profile_row-np.ones(len(y))*3000)/8.1e+4, yerr=profile_row_err/8.1e+4, fmt='-', label ='Scintillator', linewidth = 2)
ax_col.errorbar(y, (profile_col-np.ones(len(y))*3000)/8.1e+4, yerr=profile_col_err/8.1e+4, fmt='-', label ='Scintillator', linewidth = 2)

ax_row.errorbar(x_diamond, y_diamond, fmt='-', color ='orangered', label='Diamond',  linewidth = 2)
ax_col.errorbar(x_diamond, y_diamond, fmt='-', color ='orangered', label='Diamond',  linewidth = 2)

ax_row.legend()
ax_col.legend()

outputDir = '/home/eleonora/Dottorato/articolo_foglio/Figures/Results/'

fig_col.savefig(outputDir+'v_comparisonDiamond.pdf')
fig_col.savefig(outputDir+'h_comparisonDiamond.pdf')

fig, ax = createFig()

ax.errorbar(x_diamond, y_diamond, fmt='-', color ='orangered', label='Diamond',  linewidth = 2)
x = np.linspace(x_diamond.min(), x_diamond.max(), 1000)

mask = x_diamond > 0
x_diamond = x_diamond[mask]
y_diamond = y_diamond[mask]

try:
        p0 = None
        opt, pcov = curve_fit(functions.err_func_plus_constant, x_diamond, y_diamond, p0=p0)
        opt, pcov = curve_fit(functions.err_func_plus_constant, x_diamond, y_diamond, p0=p0)
 #double for improve the fit
        ax.plot(x,  functions.err_func_plus_constant(x, *opt), '--', color='magenta', linewidth = 2, label ='Single erf')
        legend = 'norm, mean, sigma, constant: ', opt
        #print('Error function fit:\n', legend, '\n' )
        data = np.concatenate((opt, np.sqrt(pcov.diagonal())))
        #np.savetxt(outputFile+'_erf.txt', np.transpose(data), header='#norm, mu, sigma, const  & errors', fmt = '%.4f')
except: 
        print("no fit single err")
try: 
        p0 = None
        opt, pcov = curve_fit(functions.double_err_func, x_diamond, y_diamond, p0=p0)
        opt, pcov = curve_fit(functions.double_err_func, x_diamond, y_diamond, p0=p0)

        ax.plot(x,  functions.double_err_func(x, *opt),  '--', color='orangered', linewidth = 2, label ='Double erf')
        legend = 'norm, mean, sigma, constant: ', opt
        print('Double error function fit:\n', legend, '\n' )
        data = np.array([opt, np.sqrt(pcov.diagonal())])
        #np.savetxt(outputFile+'_Derf.txt', np.transpose(data), header='#norm1, mu1, sigma1, norm2, mu2, sigma2, const & errors', fmt = '%.4f')
        print('mu1: %.3f' %opt[1])
        print('mu2: %.3f' %opt[4])
        print('sigma1: %.3f' %opt[2])
        print('sigma2: %.3f' %opt[5])

except:
        print("\nNo  opt param found with double erf\n")

fig.legend()

plt.show()