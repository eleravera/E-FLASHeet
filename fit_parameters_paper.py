import numpy as np
import glob
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import  pandas as pd
from scipy.optimize import curve_fit

import utilities.utilities as utils
import utilities.plot_size
import utilities.fit_functions as functions
import lib.Image_lib

def createFig(numSubFigure, sharex = True): 
  ratios = [1 for i in range(0, numSubFigure)]
  fig, ax = plt.subplots(numSubFigure,1, sharex=sharex, figsize=(9,10), gridspec_kw={'height_ratios': ratios})
  fig.subplots_adjust(hspace=0.09)
  fig.subplots_adjust(left=0.2)
  fig.subplots_adjust(right=0.92)
  fig.subplots_adjust(bottom=0.09)
  fig.subplots_adjust(top=0.96)
  return fig, ax, ratios



selections = ["dx_v*Derf*.txt", "sx_v*Derf*", "dx_h*Derf*", "sx_h*Derf*"]
orientations = ['v', 'v', 'h', 'h']
sides =['dx', 'sx', 'dx', 'sx']

directoryPath = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/'
infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

fit_directoryPath = directoryPath+'3_filter/outputFiles/fit_profiles/3mm/'


sigma = []
mu_vertical = []
mu_horizontal = []

for orientation, side in zip(orientations, sides):

  fitted_parameters = []
  doses = []
  for f, d in zip(info['data_file'], info['dose']): 
    selection = '%s*%s*%s*%s*Derf.txt' %(fit_directoryPath, side, orientation, f[:-4])
    sel_file = glob.glob(selection)[0]
    data = np.loadtxt(sel_file)
    fitted_parameters.append(data)
    doses.append(d)

  fitted_parameters = np.array(fitted_parameters)
  doses = np.array(doses)
  """
  fig, ax, ratios = createFig(3)
  ax[0].set(ylabel='$norm_{1}$ [mm]')
  ax[0].errorbar(doses, fitted_parameters[:, 0, 0], yerr= fitted_parameters[:, 0, 1], fmt = '.')
  ax[1].set(ylabel='$\mu_{1}$ [mm]')
  ax[1].errorbar(doses, fitted_parameters[:, 1, 0], yerr= fitted_parameters[:, 1, 1], fmt = '.')
  ax[2].set(ylabel='$\sigma_{1}$ [mm]')
  ax[2].errorbar(doses, fitted_parameters[:, 2, 0], yerr= fitted_parameters[:, 2, 1], fmt = '.')
  fig.suptitle('%s, %s' % (orientation, side))

  fig, ax, ratios = createFig(3)
  ax[0].set(ylabel='$norm_{2}$ [mm]')
  ax[0].errorbar(doses, fitted_parameters[:, 3, 0], yerr= fitted_parameters[:, 3, 1], fmt = '.')
  ax[1].set(ylabel='$\mu_{2}$ [mm]')
  ax[1].errorbar(doses, fitted_parameters[:, 4, 0], yerr= fitted_parameters[:, 4, 1], fmt = '.')
  ax[2].set(ylabel='$\sigma_{2}$ [mm]')
  ax[2].errorbar(doses, fitted_parameters[:, 5, 0], yerr= fitted_parameters[:, 5, 1], fmt = '.')
  fig.suptitle('%s, %s' % (orientation, side))

  fig, ax, ratios = createFig(1)
  ax.set(xlabel='DPP [Gy]', ylabel='constant')
  ax.errorbar(doses, fitted_parameters[:, 6, 0], yerr= fitted_parameters[:, 6, 1], fmt = '.')
  fig.suptitle('%s, %s' % (orientation, side))
  
  sigma1_mean = np.median(fitted_parameters[:, 2, 0])
  sigma1_err = np.std(fitted_parameters[:, 2, 0])/np.sqrt(len(fitted_parameters[:, 2, 0]))
  print("%s, %s:\nsigma 1: %.2f +- %.2f" % (orientation, side, sigma1_mean, sigma1_err))

  sigma2_mean = np.median(fitted_parameters[:, 5, 0])
  sigma2_err = np.std(fitted_parameters[:, 5, 0])/np.sqrt(len(fitted_parameters[:, 5, 0]))
  print("sigma 2: %.2f +- %.2f\n" % (sigma2_mean, sigma2_err))
  """

  s = np.abs(np.concatenate((fitted_parameters[:, 2, 0], fitted_parameters[:, 5, 0])))
  s_1 = s[s<5]
  s_2 = s[s>5]
  print("%s, %s, sigma1 = %.3f +- %.3f" % (side, orientation, np.mean(s_1), np.std(s_1)/np.sqrt(len(s_1))))
  print("%s, %s, sigma2 = %.3f +- %.3f" % (side, orientation, np.mean(s_2), np.std(s_2)/np.sqrt(len(s_2))))
  print("%s, %s, mu1 = %.3f +- %.3f" % (side, orientation, np.mean(fitted_parameters[:, 1, 0]), np.std(fitted_parameters[:, 1, 0])/np.sqrt(len(fitted_parameters[:, 1, 0]))))
  print("%s, %s, mu2 = %.3f +- %.3f" % (side, orientation, np.mean(fitted_parameters[:, 4, 0]), np.std(fitted_parameters[:, 4, 0])/np.sqrt(len(fitted_parameters[:, 4, 0]))))
  sigma.append(fitted_parameters[:, 2, 0])
  sigma.append(fitted_parameters[:, 5, 0])


  if orientation == 'v':
    mask = np.abs(fitted_parameters[:, 2, 0]) < np.abs(fitted_parameters[:, 5, 0])
    mu_vertical.append(fitted_parameters[:, 1, 0][mask])
    mu_vertical.append(fitted_parameters[:, 4, 0][~mask])

  if orientation == 'h':
    mask = np.abs(fitted_parameters[:, 2, 0]) < np.abs(fitted_parameters[:, 5, 0])
    mu_horizontal.append(fitted_parameters[:, 1, 0][mask])
    mu_horizontal.append(fitted_parameters[:, 4, 0][~mask])
  
  """
  if orientation == 'h' and side == 'sx': 

    fig, ax, _ = createFig(3)
    ax[0].set(ylabel='$\sigma_{1}$ [mm]')
    ax[0].errorbar(doses, fitted_parameters[:, 5, 0], yerr= fitted_parameters[:, 5, 1], fmt = 'o', fillstyle='none', markersize=4.,markeredgewidth=1.5)
    ax[0].grid()
    ax[1].set(ylabel='$\sigma_{2}$ [mm]')
    ax[1].errorbar(doses, fitted_parameters[:, 2, 0], yerr= fitted_parameters[:, 2, 1], fmt = 'o', fillstyle='none', markersize=4.,markeredgewidth=1.5)
    ax[1].set_ylim(6, 12.5)
    ax[1].grid()
    ax[2].set(xlabel='Dose Per Pulse [Gy]', ylabel='constant [au]')
    ax[2].errorbar(doses, fitted_parameters[:, 6, 0], yerr= fitted_parameters[:, 6, 1], fmt = 'o', fillstyle='none', markersize=4.,markeredgewidth=1.5)
    ax[2].grid()

  fig, ax, _ = createFig(2, sharex = False)
  ax[0].hist(fitted_parameters[:, 5, 0], bins =10)
  ax[0].set(ylabel='$\sigma_{1}$ [mm]')
  ax[1].hist(fitted_parameters[:, 2, 0], bins =10)
  ax[1].set(ylabel='$\sigma_{2}$ [mm]')
  fig.suptitle('%s, %s' % (orientation, side))

"""
sigma = np.concatenate(sigma)
sigma = np.abs(sigma)

mu_vertical = np.concatenate(mu_vertical)
mu_horizontal = np.concatenate(mu_horizontal)

mu_vertical=mu_vertical[mu_vertical<30]
prof_v = np.mean(mu_vertical[mu_vertical>0]) - np.mean(mu_vertical[mu_vertical<0])
prof_v_err = np.sqrt((np.std(mu_vertical[mu_vertical>0])/np.sqrt(len(mu_vertical[mu_vertical>0])))**2+(np.std(mu_vertical[mu_vertical<0])/np.sqrt(len(mu_vertical[mu_vertical<0])))**2)

prof_h = np.mean(mu_horizontal[mu_horizontal>0]) - np.mean(mu_horizontal[mu_horizontal<0])
prof_h_err = np.sqrt((np.std(mu_horizontal[mu_horizontal>0])/np.sqrt(len(mu_horizontal[mu_horizontal>0])))**2+(np.std(mu_horizontal[mu_horizontal<0])/np.sqrt(len(mu_horizontal[mu_horizontal<0])))**2)


print('width:\n horizontal %.3f +- %.3f\n vertical: %.3f +- %.3f' % (prof_h, prof_h_err, prof_v, prof_v_err))

sigma_1 = sigma[sigma<5]
sigma_2 = sigma[sigma>5]

print("----------\n")
print("sigma1 = %.3f +- %.3f" % (np.mean(sigma_1), np.std(sigma_1)/np.sqrt(len(sigma_1))))
print("sigma2 = %.3f +- %.3f" % (np.mean(sigma_2), np.std(sigma_2)/np.sqrt(len(sigma_2))))

plt.show()