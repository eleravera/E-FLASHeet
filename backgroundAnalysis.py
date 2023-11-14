
import argparse
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as PIL_Image
from scipy.optimize import curve_fit


import glob 

import utilities.plot_size
import utilities.utilities as utils
import utilities.fit_functions as functions



directoryPath = '/home/eleonora/Scrivania/FLASH_2023_06_29/linearità_2/'
infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

norm = 1.e+5
sigma = 15.

for f, d in zip(info['data_file'], info['dark_file']): 
  im = PIL_Image.open(directoryPath+f)
  im = np.array(im, dtype= np.int64)

  dark = PIL_Image.open(directoryPath+d)
  dark = np.array(dark, dtype= np.int64)

  im = im-dark

  cuttedIm = im[340:420, 80:160]
  bins = np.linspace(cuttedIm.min()-0.5, cuttedIm.max()+0.5, int((cuttedIm.max()-cuttedIm.min()+2)/19))
  hist, bin_edges = np.histogram(np.concatenate(cuttedIm), bins=bins)
  bin_centers = (bin_edges[1:]+bin_edges[:-1])*0.5

  mu = 2600
  sigma = sigma -0.3
  att = 2.e-3
  norm = norm *3
  p0 = [mu, sigma, norm, att]

  plt.figure()
  plt.plot(bin_centers, hist)
  plt.xlim(0, 2000)
  title = '%s' %f
  plt.title(title)
  x = np.linspace(bin_centers.min()-1, bin_centers.max()+1, 1000)
  hist_err = np.ones(len(hist))
  hist_err[hist!=0] = np.sqrt(hist[hist!=0])
  try: 
    opt, pcov = curve_fit(functions.err_func_exp, bin_centers, hist, sigma = hist_err, p0=p0)
    opt, pcov = curve_fit(functions.err_func_exp, bin_centers, hist, sigma = hist_err, p0=opt)

    print(f, opt)
    y = functions.err_func_exp(x, *opt)
    plt.plot(x, y, '--')
  except: 
    print('%s, No optimal parameter found' %f)



plt.show()



