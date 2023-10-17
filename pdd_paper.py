#fai la media delle 3 distribuzioni 

#per ogni file nel info sottrai il fondo e poi quelli con stessa dose fai la media delle immagini

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import utilities.utilities as utils
import lib.Image_lib
import utilities.plot_size

EXTENT = [118, 333, 185, 400]
CENTER_X = -147
CENTER_Y = -((EXTENT[3]-EXTENT[2])*0.5+EXTENT[2])
extent = [EXTENT[0]+CENTER_X, EXTENT[1]+CENTER_X, EXTENT[2]+CENTER_Y, EXTENT[3]+CENTER_Y ]

if __name__ == "__main__":
    directoryPath = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/pdd/'
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
    images[1]  = images[1]/(images[1].max())
    vmin, vmax =  np.quantile(images[1], [0.1, 0.99])
    im1 =ax[1].imshow(images[1],vmin =vmin, vmax =vmax, extent=extent)
    ax[1].set(title='DPP = %.1f Gy' % data['doses'][1],  xlabel='mm')

    divider = make_axes_locatable(ax[0])
    cax0 = divider.append_axes('right', size='5%', pad=0.05)
    divider = make_axes_locatable(ax[1])
    cax1 = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im0, cax=cax0)
    fig.colorbar(im1, cax=cax1)

    


    #SIMULAZIONE
    """
    df = pd.read_csv('/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/simulazionePDD.csv', skiprows=2)
    mask = df[' iY']==50
    mc = df[' total(value) [Gy]'][mask]
    mc = np.transpose(np.reshape(mc, (100,100)))

    fig, ax = plt.subplots(1,1, figsize=(10,8))
    mc = mc/(mc.max())
    vmin, vmax =  np.quantile(mc, [0.1, 0.99])
    im =ax.imshow(mc, extent=(0, 10, -10, +10), vmin=vmin, vmax=vmax)
    ax.set_ylim((-3.5, +3.5))
    ax.set_xlim((0,6))
    fig.colorbar(im)
    """
    #GAF
    gafFile= '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/pdd.tiff'
    image = lib.Image_lib.Image(gafFile)
    signalImage = np.transpose(image.image )
    fig, ax = plt.subplots(1,1, figsize=(10,8))
    signalImage = signalImage/(signalImage.max())
    vmin, vmax =  np.quantile(signalImage, [0.1, 0.99])
    im =ax.imshow(signalImage, vmin=vmin, vmax=vmax)
    #ax.set_ylim((-3.5, +3.5))
    #ax.set_xlim((0,6))
    fig.colorbar(im)

    diamondFile = '/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/app40_pdd.csv'
    pddDiamond = pd.read_csv(diamondFile)

    fig, ax = plt.subplots(1,1, figsize=(10,8))
    fig.subplots_adjust(left=0.15)
    fig.subplots_adjust(right=0.98)
    fig.subplots_adjust(bottom=0.1)
    fig.subplots_adjust(top=0.9)

    p = 112
    normFactor0 = (np.sum(images[0][p-1:p+1, :], axis = 0)).max()
    profile0 = np.sum(images[0][p-1:p+1, :], axis = 0)/normFactor0
    profileErr0 = np.std(images[0][p-1:p+1, :], axis = 0)/np.sqrt(2)/normFactor0
    normFactor1 = (np.sum(images[1][p-1:p+1, :], axis = 0)).max()
    profile1 = np.sum(images[1][p-1:p+1, :], axis = 0)/normFactor1
    profileErr1 = np.std(images[1][p-1:p+1, :], axis = 0)/np.sqrt(2)/normFactor1

    ax.plot(images[0][220, :]/(images[0][220,:].max()))
    x = np.linspace(extent[0], extent[1], images[0].shape[1] )
    xerr =  x * mInfo['magnificationErr']/mInfo['magnification']
    ax.errorbar(x, profile0, xerr=xerr, yerr = profileErr0, fmt = '.', fillstyle='none',color='mediumblue', label ='DPP = %.1f Gy' % data['doses'][0])
    ax.plot(x, profile0,  '--', color='cornflowerblue', alpha = 0.8)
    ax.errorbar(x, profile1, xerr=xerr, yerr = profileErr1, fmt = '.', fillstyle='none',color='green', label ='DPP = %.1f Gy' % data['doses'][1])
    ax.plot(x, profile1,  '--', color='limegreen', alpha = 0.8)
    ax.set(xlabel = 'Depth [mm]', ylabel='Signal [au]')
    #x = np.linspace(0, 100,   signalImage[295, :].shape[1])

    ax.errorbar(pddDiamond['App 40'], pddDiamond['Unnamed: 1']/(pddDiamond['Unnamed: 1'].max()), fmt = '-r', label='diamond')
    #ax.plot(x, signalImage[295, :]/(signalImage[295, :].max()), label='gaf')
    #profileMC = np.sum(mc, axis = 1)
    #ax.plot(x, profileMC[50, :]*1.1,  '-', color='red', alpha = 0.8)
    #da sistemare 

    ax.grid()
    ax.legend()



    plt.show()