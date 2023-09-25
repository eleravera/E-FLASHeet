#python3 -i show.py -f inputfile.TIF
import argparse 
import numpy as np
from matplotlib import pyplot as plt

import lib.Image_lib
import utilities.plot_size

options_parser = argparse.ArgumentParser(description = 'Questo script deve mostrarmi la colormap di un immagine')
options_parser.add_argument('-input_file', '-f', default=None, type=str, help='input_file')
options_parser.add_argument('-dark_file', '-d', default=None, type=str, help='dark_file')

options = vars(options_parser.parse_args())
inputFIle = options['input_file']
darkFile = options['dark_file']

image = lib.Image_lib.Image(inputFIle)

if darkFile is not None: 
  dark = lib.Image_lib.Image(darkFile)
  signalImage = image.image - dark.image
else:
  signalImage = image.image


plt.imshow(signalImage)
plt.colorbar()

#minibeam
#signalImageZoomed = signalImage[100:300,222:422]
#calFactor = 15/435 #cm/pixel
#vmin=4000, vmax= 25000

#PDD
#signalImageZoomed = signalImage[100:350, 150:400]
#calFactor = 8/243 #cm/pixel
#vmin , vmax = 0, 20000

#beam 
signalImageZoomed = signalImage[110:310,217:417]
calFactor = 14/438.5 #cm/pixel
vmin , vmax = 0, 24000


minorticks_X = np.arange(-signalImageZoomed.shape[0]/2, signalImageZoomed.shape[0]/2,)* calFactor
minorticks_Y = minorticks_X


extent = (minorticks_X.min(), minorticks_X.max(), minorticks_Y.min(), minorticks_Y.max())


fig, ax = plt.subplots(1, 1, figsize=(8,8))
ax.imshow(signalImageZoomed, vmin =vmin, vmax= vmax, extent = extent)
ax.xaxis.set_major_locator(plt.MaxNLocator(3))
ax.yaxis.set_major_locator(plt.MaxNLocator(3))

ax.set(xlabel='cm', ylabel='cm')
#plt.colorbar()
plt.show()