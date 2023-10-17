import numpy as np
import argparse
import os
from scipy.ndimage import white_tophat
from matplotlib import pyplot as plt
from scipy.signal import medfilt2d


import lib.Image_lib
import utilities.plot_size

options_parser = argparse.ArgumentParser(description = '')
options_parser.add_argument('-input_file', '-f', default=None, type=str, help='input_file')
options_parser.add_argument('-dark_file', '-d', default=None, type=str, help='dark_file')

options = vars(options_parser.parse_args())
inputFIle = options['input_file']
darkFile = options['dark_file']


image = lib.Image_lib.Image(inputFIle)
dark = lib.Image_lib.Image(darkFile)

signalImage = image.image - dark.image

fig_hist_signal, ax_hist_signal = plt.subplots(1, 1, figsize=(20,12))
fig_hist_filter, ax_hist_filter = plt.subplots(1, 1, figsize=(20,12))
fig_hist_signal_res, ax_hist_signal_res = plt.subplots(1, 1, figsize=(20,12))

fig_profile, ax_profile = plt.subplots(1, 1, figsize=(20,12))
ax_profile.plot(signalImage[210, :], label = 'unfiltered')

vminIm, vmaxIm = 0, 25000#1000#25000
vminFilt, vmaxFilt = 0, 3000#500#3000

outputDir = os.path.dirname(inputFIle)+'/outputFiles/filtering/low/'
myList = [3, 5, 9]
bins = np.linspace(0, 6000, 100)
for n in myList: 
  plt.figure()
  plt.title('median %dx%d' %(n,n))
  filtIm_median = medfilt2d(signalImage,  kernel_size=[n,n])
  plt.imshow(filtIm_median)
  plt.colorbar()
  ax_profile.plot(filtIm_median[210, :], label = 'median %dx%d' %(n,n))

  plt.figure()
  plt.title('median filter %dx%d' %(n,n))
  plt.imshow(filtIm_median-signalImage, vmin = -1000, vmax=1000)
  plt.colorbar()


  filter = white_tophat(signalImage, size=(n,n))
  
  plt.figure(figsize=(7,7))
  plt.imshow(signalImage-filter, vmin=vminIm, vmax=vmaxIm)
  plt.title('%dx%d' % (n,n))
  plt.colorbar()
  #plt.savefig(outputDir+'imFiltered_%d.pdf' %n)

  plt.figure(figsize=(7,7))
  plt.imshow(filter, vmin=vminFilt, vmax = vmaxFilt)
  plt.title('%dx%d filter' % (n,n))
  plt.colorbar()
  #plt.savefig(outputDir+'filter_%d.pdf' %n)

  ax_hist_filter.hist(np.concatenate(filter), bins=np.linspace(-500, 8000, 100), label = 'filter o. %dx%d' %(n,n), histtype='step')
  ax_hist_filter.hist(np.concatenate(signalImage-filtIm_median), bins=np.linspace(-500, 8000, 100), label = 'median %dx%d' %(n,n), histtype='step')
  ax_hist_filter.set(xlabel='CCD Gray counts', title='filter')

  ax_hist_signal.hist(np.concatenate(signalImage-filter), bins=bins, label = 'filter o. %dx%d' %(n,n), histtype='step')
  ax_hist_signal.hist(np.concatenate(filtIm_median), bins=bins, label = 'median %dx%d' %(n,n), histtype='step')
  ax_hist_signal.set(xlabel='CCD Gray counts')

  ax_profile.plot(signalImage[210, :]-filter[ 210, :], label = '%dx%d' %(n,n))
  ax_profile.set(xlabel='col', title='beam profile')




ax_hist_signal.hist(np.concatenate(signalImage), bins=bins, label = 'unfiltered', histtype='step')

ax_hist_signal.set_yscale('log')
ax_hist_signal.set_yscale('log')

ax_hist_filter.set_yscale('log')

fig_hist_signal.legend()
fig_hist_filter.legend()
fig_profile.legend()

#fig_hist_signal.savefig(outputDir+'signalHist.pdf')
#fig_hist_filter.savefig(outputDir+'filterHist.pdf')
#fig_profile.savefig(outputDir+'profile.pdf')


plt.figure(figsize=(7,7))
plt.imshow(signalImage, vmin=vminIm, vmax=vmaxIm)
plt.title('unfiltered')
plt.colorbar()
#plt.savefig(outputDir+'unfilterd.pdf')




plt.show()
