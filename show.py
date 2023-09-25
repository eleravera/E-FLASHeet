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

rangemin= 2055
rangemax = 20000

plt.imshow(signalImage)
plt.colorbar()
#signalImage.plotImage(bounds=(rangemin, rangemax))
#signalImage.histImage(bounds = (rangemin, rangemax))


plt.show()