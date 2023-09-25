import numpy as np
from matplotlib import pyplot as plt
import argparse

import utilities.plot_size
import utilities.utilities as utils

options_parser = argparse.ArgumentParser(description = '')
options_parser.add_argument('-input_directory', '-d', default=None, type=str, help='input_directory')
options_parser.add_argument('-variable', '-v', default=None, type=str, help='selected variable (from the info file)')
options_parser.add_argument('-xlabel', '-x', default='', type=str, help='xlabel in the plot')


options = vars(options_parser.parse_args())
directoryPath = options['input_directory']
selVariable = options['variable']
xlabel = options['xlabel']

if xlabel == '': 
  xlabel = selVariable

infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

dataSavedOnFile  = utils.read_roi_data_from_file(directoryPath, info['data_file'], info[selVariable])

rois = dataSavedOnFile[0][0]
radius = dataSavedOnFile[0][1]
signal = dataSavedOnFile[0][2]
signalErr = dataSavedOnFile[0][3]

fig_unique, ax_unique = plt.subplots(1, 1, figsize=(10,8))

variable = dataSavedOnFile[1]
for r in np.unique(rois):
    for rr in np.unique(radius):
      fig, ax = plt.subplots(1, 1, figsize=(10,8))
      mask = (rois == r)*(radius==rr) 
      ax.errorbar(variable[mask], signal[mask], yerr = signalErr[mask], fmt = '.')
      ax.set_title('ROI %d, radius %d' %(r, rr))
      ax.set(xlabel='%s'  %xlabel, ylabel='Signal [au]')
      fig.savefig(directoryPath+"/outputFiles/%s_roi%d_radius%d.pdf" %(xlabel, r, rr))

      ax_unique.errorbar(variable[mask], signal[mask], yerr = signalErr[mask], fmt = '.', label = 'ROI %d' %r)
      ax_unique.set_title('ROI %d, radius %d' %(r, rr))
      ax_unique.set(xlabel='%s'  %xlabel, ylabel='Signal [au]')  
      fig_unique.legend()
      #fig_unique.savefig(directoryPath+"/outputFiles/%s.pdf" %(xlabel, f))

plt.show()

