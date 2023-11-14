import numpy as np
import os
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import  pandas as pd
from scipy.optimize import curve_fit

import utilities.utilities as utils
import utilities.plot_size
import utilities.fit_functions as functions
import lib.Image_lib

from profile_paper import plot_profile as plot_profile

scint_05mm = {"inputDir" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/3_filter/",
              "name" : '05mm', 
              "center_x" : -240, 
              "center_y": -190, 
              "norm_col" : 172400, 
              "norm_row" :  173000, 
              "x_bounds_fit_DX" : [-10, 60],
              "x_bounds_fit_SX" : [-60, 10], 
              "y_bounds_fit_DX" : [-10, 60],
              "y_bounds_fit_SX" : [-60, 10],
              "outputDir" : '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/3_filter/outputFiles/fit_profiles/05mm/'
              }

scint_3mm = {"inputDir" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/3_filter/",
              "name" : "3mm", 
              "center_x" : -315,
              "center_y": -210, 
              "norm_col" : 110452,
              "norm_row" : 110504,
              "x_bounds_fit_DX" : [0, 70],
              "x_bounds_fit_SX" : [-70, 0], 
              "y_bounds_fit_DX" : [0, 70],
              "y_bounds_fit_SX" : [-70, 0],
              "outputDir" : '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/3_filter/outputFiles/fit_profiles/3mm/'
              }


def createFig(): 
  fig, ax = plt.subplots(1,1, figsize=(12,10))
  fig.subplots_adjust(left=0.15)
  fig.subplots_adjust(right=0.98)
  fig.subplots_adjust(bottom=0.1)
  fig.subplots_adjust(top=0.9)
  ax.grid()
  return fig, ax


def fit_profile(x, profile, profile_err, x_min, x_max, dose, p0 = None, p0_double=None, outputFile=''): 
    
    fig, ax = createFig()
    mask = (x < x_max) * (x > x_min)
    ax.set_xlim(x_min, x_max)
    xFit = np.linspace(x_min, x_max, 1000)
    ax.errorbar(x, profile, yerr = profile_err, fmt = '.', markersize=6., markeredgewidth=1.5, label ='%.2f Gy' % dose)
    try:
        p0 = p0
        opt, pcov = curve_fit(functions.err_func_plus_constant, x[mask], profile[mask], sigma = profile_err[mask], p0=p0)
        opt, pcov = curve_fit(functions.err_func_plus_constant, x[mask], profile[mask], sigma = profile_err[mask], p0=opt) #double for improve the fit
        ax.plot(xFit,  functions.err_func_plus_constant(xFit, *opt), '--', color='magenta', linewidth = 2, label ='Single erf')
        legend = 'norm, mean, sigma, constant: ', opt
        #print('Error function fit:\n', legend, '\n' )
        data = np.concatenate((opt, np.sqrt(pcov.diagonal())))
        np.savetxt(outputFile+'_erf.txt', np.transpose(data), header='#norm, mu, sigma, const  & errors', fmt = '%.4f')
    except: 
        print("no fit single err")
    try: 
        p0 = p0_double
        opt, pcov = curve_fit(functions.double_err_func, x[mask], profile[mask], sigma = profile_err[mask], p0=p0)
        opt, pcov = curve_fit(functions.double_err_func, x[mask], profile[mask], sigma = profile_err[mask], p0=opt)
        ax.plot(xFit,  functions.double_err_func(xFit, *opt),  '--', color='orangered', linewidth = 2, label ='Double erf')
        legend = 'norm, mean, sigma, constant: ', opt
        #print('Double error function fit:\n', legend, '\n' )
        data = np.array([opt, np.sqrt(pcov.diagonal())])
        np.savetxt(outputFile+'_Derf.txt', np.transpose(data), header='#norm1, mu1, sigma1, norm2, mu2, sigma2, const & errors', fmt = '%.4f')
    except:
        print("\nNo  opt param found with double erf\n")
    ax.legend()

    fig.savefig(outputFile +'.pdf' )
    return



if __name__ == "__main__":

    dict = scint_3mm
    save = False

    infoFile = utils.search_file_in_directory(dict['inputDir'], '/info*.txt')
    info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

    magnificationFile = utils.search_file_in_directory(dict['inputDir'], '/magnification.txt')
    mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT )

    for inputFile, darkFile, dose in zip (info['data_file'], info['dark_file'], info['dose']):
      inputFile = dict['inputDir'] + inputFile
      darkFile = dict['inputDir'] + darkFile
      image = lib.Image_lib.Image(inputFile)
      dark = lib.Image_lib.Image(darkFile)
      signalImage = image.image - dark.image
      

      
      fig_col, ax_col = createFig()
      fig_row, ax_row = createFig()
      x, y, profile_row, profile_col, profile_row_err, profile_col_err = plot_profile(signalImage, -dict['center_y'], -dict['center_x'], mInfo['magnification'], dict, dose, ax_row, ax_col, norm_col = dict['norm_col'], norm_row = dict['norm_row'])
      ax_row.set(xlabel ='r [mm]', ylabel = 'norm profile [au]')
      ax_col.set(xlabel ='r [mm]', ylabel = 'norm profile [au]')

      outputDir = dict['outputDir']
      
      fit_profile(x, profile_row, profile_row_err, x_min = dict['x_bounds_fit_SX'][0], x_max = dict["x_bounds_fit_SX"][1], dose=dose, outputFile=outputDir+'sx_v_%s' % os.path.basename(inputFile)[:-4], p0 = None, p0_double = [0.03, -22, 12, 0.13, -20, 3.5, 0.004])
      
      fit_profile(y, profile_col, profile_col_err, x_min = dict['y_bounds_fit_SX'][0], x_max = dict["y_bounds_fit_SX"][1], dose=dose, outputFile=outputDir+'sx_h_%s' % os.path.basename(inputFile)[:-4], p0=None, p0_double=[0.3, -24, 7, 0.6, -20, 2.6, 0.04])
      
      
      fit_profile(x, profile_row, profile_row_err, x_min = dict['x_bounds_fit_DX'][0], x_max = dict["x_bounds_fit_DX"][1], dose=dose, outputFile=outputDir+'dx_v_%s' % os.path.basename(inputFile)[:-4], p0=[0.75, 20., -4.6, 0.03], p0_double=[0.15, 23, -13, -0.8, 20., 3.4, 0.7])


      fit_profile(y, profile_col, profile_col_err, x_min = dict['y_bounds_fit_DX'][0], x_max = dict["y_bounds_fit_DX"][1], dose=dose, outputFile=outputDir+'dx_h_%s' % os.path.basename(inputFile)[:-4], p0=[0.97, 20.6, -4.4, 0.035], p0_double=[0.7, 20., -2.9, 0.25, 21.3, -9.6, 0.03])

      #plt.show()  
