import argparse 
import numpy as np
from matplotlib import pyplot as plt

import lib.Image_lib
import utilities.plot_size
import utilities.utilities as utils

options_parser = argparse.ArgumentParser(description = 'Questo script deve mostrarmi la colormap di un immagine')
options_parser.add_argument('-input_file', '-f', default=None, type=str, help='input_file')
options_parser.add_argument('-dark_file', '-d', default=None, type=str, help='dark_file')
options_parser.add_argument('-magnification', '-m', default=None, type=str, help='magnification file')
options_parser.add_argument('-selected_line', '-l', default=212, type=int, help='selected line for profile')


options = vars(options_parser.parse_args())
inputFile = options['input_file']
darkFile = options['dark_file']
magnificationFile = options['magnification']
selected_line = options['selected_line']

image = lib.Image_lib.Image(inputFile)

if darkFile is not None: 
    dark = lib.Image_lib.Image(darkFile)
    signalImage = image.image - dark.image
    errorImage = image.image + dark.image
else:
    signalImage = image.image
    errorImage  = signalImage

mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT)
extent = [0, signalImage.shape[0]*mInfo['magnification'], 0, signalImage.shape[1]*mInfo['magnification']]

fig, ax = plt.subplots(1, 1, figsize=(8,8))
vmin, vmax =  np.quantile(signalImage, [0.1, 0.99])
im =ax.imshow(signalImage, vmin =vmin, vmax =vmax, extent=extent) 
ax.set(xlabel = 'mm')
plt.colorbar(im)


fig, ax = plt.subplots(1, 1, figsize=(8,8))
x = np.linspace(extent[0], extent[1], len(signalImage[selected_line, :]))
ax.plot(x, signalImage[selected_line, :], '-')

plt.show()