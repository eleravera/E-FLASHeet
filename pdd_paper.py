#fai la media delle 3 distribuzioni 

#per ogni file nel info sottrai il fondo e poi quelli con stessa dose fai la media delle immagini

import numpy as np
import argparse
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import utilities.utilities as utils
import lib.Image_lib

EXTENT = [118, 333, 185, 400]
CENTER_X = -147
CENTER_Y = -((EXTENT[3]-EXTENT[2])*0.5+EXTENT[2])
extent = [EXTENT[0]+CENTER_X, EXTENT[1]+CENTER_X, EXTENT[2]+CENTER_Y, EXTENT[3]+CENTER_Y ]

if __name__ == "__main__":
    directoryPath = '/home/eleonora/Scrivania/FLASH_2023_06_29/pdd/'
    inputFile = utils.search_file_in_directory(directoryPath, '/outputFiles/*.npz')

    data = np.load(inputFile)

    magnificationFile = utils.search_file_in_directory(directoryPath, '/magnification.txt')
    mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT )

    images = data['images']/( data['images'].max())
    extent = extent*mInfo['magnification']

    fig, ax = plt.subplots(1,2, sharex=True, sharey=True, figsize=(14,8))
    fig.subplots_adjust(wspace=0.35)
    fig.subplots_adjust(left=0.1)
    fig.subplots_adjust(right=0.9)
    fig.subplots_adjust(bottom=0.1)
    fig.subplots_adjust(top=0.9)

    
    vmin, vmax =  np.quantile(images[0], [0.1, 0.99])
    im0 = ax[0].imshow(images[0],vmin =vmin, vmax =vmax, extent=extent)
    ax[0].set(title='DPP = %.1f Gy' % data['doses'][0], xlabel='mm', ylabel='mm')

    vmin, vmax =  np.quantile(images[1], [0.1, 0.99])
    im1 =ax[1].imshow(images[1],vmin =vmin, vmax =vmax, extent=extent)
    ax[1].set(title='DPP = %.1f Gy' % data['doses'][1],  xlabel='mm')

    divider = make_axes_locatable(ax[0])
    cax0 = divider.append_axes('right', size='5%', pad=0.05)
    divider = make_axes_locatable(ax[1])
    cax1 = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im0, cax=cax0)
    fig.colorbar(im1, cax=cax1)


    fig, ax = plt.subplots(1,1, figsize=(10,8))
    fig.subplots_adjust(left=0.15)
    fig.subplots_adjust(right=0.98)
    fig.subplots_adjust(bottom=0.1)
    fig.subplots_adjust(top=0.9)

    p = 112
    profile0 = np.sum(images[0][p-1:p+1, :], axis = 0)
    profileErr0 = np.std(images[0][p-1:p+1, :], axis = 0)/np.sqrt(3) 
    profile1 = np.sum(images[1][p-1:p+1, :], axis = 0)
    profileErr1 = np.std(images[1][p-1:p+1, :], axis = 0)/np.sqrt(3)

    x = np.linspace(extent[0], extent[1], images[0].shape[1] )
    ax.errorbar(x, profile0, yerr = profileErr0, fmt = '.', fillstyle='none',color='mediumblue', label ='DPP = %.1f Gy' % data['doses'][0])
    ax.plot(x, profile0,  '--', color='cornflowerblue', alpha = 0.8)
    ax.errorbar(x, profile1, yerr = profileErr1, fmt = '.', fillstyle='none',color='green', label ='DPP = %.1f Gy' % data['doses'][1])
    ax.plot(x, profile1,  '--', color='limegreen', alpha = 0.8)
    ax.set(xlabel = 'Depth [mm]', ylabel='Signal [au]')
    ax.grid()
    ax.legend()
    plt.show()