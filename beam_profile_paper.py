import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import  pandas as pd

import utilities.utilities as utils
import utilities.plot_size

EXTENT = [0, 512, 0, 512]
CENTER_X = -210
CENTER_Y = -315
extent = [EXTENT[0]+CENTER_X, EXTENT[1]+CENTER_X, EXTENT[2]+CENTER_Y, EXTENT[3]+CENTER_Y ]

if __name__ == "__main__":
    directoryPath = '/home/eleonora/Scrivania/FLASH_2023_06_29/linearità_2/'
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

    r = 212
    c = 316

    doses = data['doses']
    images = images[2:3, :, :]
    doses = doses[2:3]

    for im, d in zip(images, doses): 
      #fig, ax = plt.subplots(1,1, figsize=(10,8))
      profile_r = np.sum(im[r-2:r+2, :], axis = 0)
      profileErr_r = np.std(im[r-2:r+2, :], axis = 0)/np.sqrt(4) 
      #profile_r, profileErr_r = profile_r/(profile_r.max()), profileErr_r/(profile_r.max())
      profile_c = np.sum(im[:,c-2:c+2], axis = 1)
      profileErr_c = np.std(im[:,c-2:c+2], axis = 1)/np.sqrt(4) 
      #profile_c, profileErr_c = profile_c/(profile_c.max()), profileErr_c/(profile_c.max())

      x = np.linspace(extent[2], extent[3], im.shape[0] )
      ax.errorbar(x, profile_r, yerr = profileErr_r, fmt = '.', fillstyle='none',color='mediumblue', label ='h, %.2f Gy' % d)
      ax.plot(x, profile_r,  '--', color='cornflowerblue', alpha = 0.8)
      x = np.linspace(extent[0], extent[1], im.shape[1] )
      ax.errorbar(x, profile_c, yerr = profileErr_c, fmt = '-', fillstyle='none',color='green', label ='v, %.2f Gy' % d)
      ax.plot(x, profile_c,  '--', color='limegreen', alpha = 0.8)
      #plt.show()

    ax.set(xlabel = 'r [mm]', ylabel='Signal [au]')
    ax.grid()
    ax.set_xlim([-7, +7])
    ax.legend()


    df = pd.read_csv('/home/eleonora/Scrivania/FLASH_2023_06_29/dose 2.out', skiprows=2)
    mask = df['# iX']==12 #mm in acqua solida
    im12mm = df[' total(value) [Gy]'][mask]
    imresh12mm = np.reshape(im12mm, (100,100))

    profile = imresh12mm[50, :]
    x =  np.linspace(-10, 10, len(profile))
    profile =  profile/(profile.max())
    profile = profile + np.ones(len(profile))*0.04

    ax.plot(x,profile, '-r')

    plt.show()