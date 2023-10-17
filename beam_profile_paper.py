import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import  pandas as pd
from scipy.optimize import curve_fit

import utilities.utilities as utils
import utilities.plot_size
import utilities.fit_functions as functions

"""
# 3 mm 
directoryPath = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/'

EXTENT = [0, 512, 0, 512]
CENTER_X = -210
CENTER_Y = -315
extent = [EXTENT[0]+CENTER_X, EXTENT[1]+CENTER_X, EXTENT[2]+CENTER_Y, EXTENT[3]+CENTER_Y ]

ROW_SEL = 212
COL_SEL = 316
DOSE_SEL = 0.18

"""

# 0.5 mm
directoryPath = '/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/'

EXTENT = [0, 512, 0, 512]
CENTER_X = -190
CENTER_Y = -240
extent = [EXTENT[0]+CENTER_X, EXTENT[1]+CENTER_X, EXTENT[2]+CENTER_Y, EXTENT[3]+CENTER_Y ]

ROW_SEL = 190
COL_SEL = 240
DOSE_SEL = 0.07

if __name__ == "__main__":

    inputFile = utils.search_file_in_directory(directoryPath, '/outputFiles/*.npz')
    data = np.load(inputFile)
    magnificationFile = utils.search_file_in_directory(directoryPath, '/magnification.txt')
    mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT )

    images = data['images']/( data['images'].max())
    extent = extent*mInfo['magnification']

    fig, ax = plt.subplots(1,1, figsize=(10,8))
    fig.subplots_adjust(left=0.15)
    fig.subplots_adjust(right=0.98)
    fig.subplots_adjust(bottom=0.1)
    fig.subplots_adjust(top=0.9)

    doses = data['doses']
    doseIndex = np.argwhere(doses == DOSE_SEL)[0]
    images = images[doseIndex, :, :]
    doses = doses[doseIndex]

    for im, d in zip(images, doses): 
      profile_r = np.sum(im[ROW_SEL-2:ROW_SEL+2, :], axis = 0)
      profileErr_r = np.std(im[ROW_SEL-2:ROW_SEL+2, :], axis = 0)/np.sqrt(4) 
      profile_c = np.sum(im[:,COL_SEL-2:COL_SEL+2], axis = 1)
      profileErr_c = np.std(im[:,COL_SEL-2:COL_SEL+2], axis = 1)/np.sqrt(4) 

      profileErr_r = profileErr_r/ (profile_r.max())
      profile_r = profile_r/ (profile_r.max())
      profileErr_c = profileErr_c/ (profile_c.max())
      profile_c = profile_c/ (profile_c.max())

      x = np.linspace(extent[2], extent[3], im.shape[0] )
      ax.errorbar(x, profile_r, yerr = profileErr_r, fmt = '.', fillstyle='none',color='mediumblue', label ='h, %.2f Gy' % d)

      mask = x<0
      opt, pcov = curve_fit(functions.err_func, x[mask], profile_r[mask], sigma = profileErr_r[mask])
      xFit = np.linspace(-80, 0, 1000)
      ax.plot(xFit,  functions.err_func(xFit, *opt), '--m')
      ax.set_xlim(-50, 0)
      legend = 'norm, mean, sigma, constant: ', opt

      fig.legend(legend)

      #ax.plot(x, profile_r,  '--', color='cornflowerblue', alpha = 0.8)
      #x = np.linspace(extent[0], extent[1], im.shape[1] )
      #ax.errorbar(x, profile_c, yerr = profileErr_c, fmt = '.', fillstyle='none',color='green', label ='v, %.2f Gy' % d)
      #ax.plot(x, profile_c,  '--', color='limegreen', alpha = 0.8)



    ax.set(xlabel = 'r [mm]', ylabel='Signal [au]')
    ax.grid()
    ax.legend()


    
    sim = pd.read_csv('/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/app40_profile.out', skiprows=2)
    #mask = (sim['# iX']>=12)*(sim['# iX']<15) #mm in acqua solida
    #imSim = sim[' total(value) [Gy]'][mask]
    #imSim = np.reshape(imSim, (3, 100, 100))
    #profileSim = np.sum(imSim, axis = 0)[50, :]

    mask = (sim['# iX']==12) #mm in acqua solida
    imSim = sim[' total(value) [Gy]'][mask]
    imSim = np.reshape(imSim, (100, 100))
    profileSim =  imSim[50, :]

    x =  np.linspace(-100, 100, len(profileSim))
    profileSim =  profileSim/(profileSim.max())
    profileSim = profileSim + np.ones(len(profileSim))*0.00

    #ax.plot(x,profileSim, '-r')
    
    """
    mask = x<0
    opt, pcov = curve_fit(functions.err_func, x[mask], profileSim[mask])#, sigma = profileErr_c[mask])
    xFit = np.linspace(-80, 0, 1000)
    ax.plot(xFit,  functions.err_func(xFit, *opt), '--m')
    ax.set_xlim(-50, 0)

    legend = 'norm, mean, sigma, constant: ', opt

    fig.legend(legend)
    """

    plt.show()