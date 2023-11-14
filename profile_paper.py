import numpy as np
from matplotlib import pyplot as plt

import lib.Image_lib
import utilities.utilities as utils

outputDir = '/home/eleonora/Dottorato/articolo_foglio/Figures/Results/'

scint_05mm = {"inputDir" :  "/home/eleonora/FLASH-Scintillators/Flash_2023_06_30/open/3_filter/",
              "name" : '05mm', 
              "center_x" : -240, 
              "center_y": -190, 
              "norm_col" : 172400, 
              "norm_row" : 173000, 
              }

scint_3mm = {"inputDir" :  "/home/eleonora/FLASH-Scintillators/FLASH_2023_06_29/linearità_2/3_filter/",
              "name" : "3mm", 
              "center_x" : -315,
              "center_y": -210, 
              "norm_col" : 110452,
              "norm_row" : 110504,
              }

def createFig(): 
  fig, ax = plt.subplots(1,1, figsize=(12,10))
  fig.subplots_adjust(left=0.15)
  fig.subplots_adjust(right=0.98)
  fig.subplots_adjust(bottom=0.1)
  fig.subplots_adjust(top=0.9)
  ax.grid()
  return fig, ax
 


#norm factor preso sperimentalmente dalle immagini
def plot_profile(image, row, col, magnification, dict, dose, axis_row, axis_col, width = 2, norm_col = 1, norm_row=1):
  x, y = utils.applyMagnificationFactor(image, magnification, dict["center_x"], dict["center_y"])
  profile_row = np.sum(image[ row - width : row + width, : ], axis = 0 ) / norm_row
  profile_row_err = np.std(image[ row - width : row + width, : ], axis = 0 ) / np.sqrt(width*2) / norm_row

  profile_col = np.sum(image[:, col - width : col + width ], axis = 1 ) / norm_col
  profile_col_err = np.std(image[:, col - width : col + width ], axis = 1 ) / np.sqrt(width*2) / norm_col

  axis_row.errorbar(x, profile_row, yerr = profile_row_err, fmt = '.', markeredgewidth=1., label ='%.2f Gy' % dose)
  axis_col.errorbar(y, profile_col, yerr = profile_col_err, fmt = '.', markeredgewidth=1., label ='%.2f Gy' % dose)
  return x, y, profile_row, profile_col, profile_row_err, profile_col_err

 
def main_profile(dict, save=False): 
    infoFile = utils.search_file_in_directory(dict['inputDir'], '/info*.txt')
    info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

    magnificationFile = utils.search_file_in_directory(dict['inputDir'], '/magnification.txt')
    mInfo = utils.parse_config_file(magnificationFile, utils.MAGNIFICATION_DICT )

    fig_col, ax_col = createFig()
    fig_row, ax_row = createFig()

    #for inputFile, darkFile, dose in zip (info['data_file'], info['dark_file'], info['dose']):
      #inputFile = dict['inputDir'] + inputFile
      #darkFile = dict['inputDir'] + darkFile
    for dose in np.unique(info['dose']):
      arg = np.argwhere(info['dose']==dose)[0][0]
      inputFile = dict['inputDir'] + info['data_file'][arg]
      darkFile = dict['inputDir'] + info['dark_file'][arg]
      
      image = lib.Image_lib.Image(inputFile)
      dark = lib.Image_lib.Image(darkFile)
      signalImage = image.image - dark.image
      plot_profile(signalImage, -dict['center_y'], -dict['center_x'], mInfo['magnification'], dict, dose, ax_row, ax_col, norm_col = dict['norm_col'], norm_row = dict['norm_row'])

      ax_col.legend()
      ax_row.legend()
      ax_row.set_xlim(-50, +50)
      ax_col.set_xlim(-50, +50)

      ax_row.set(xlabel ='r [mm]', ylabel = 'norm profile [au]')
      ax_col.set(xlabel ='r [mm]', ylabel = 'norm profile [au]')

      if save == True:
        fig_col.savefig(outputDir + '%s_profile_horizontal.pdf' % dict['name'] )
        fig_row.savefig(outputDir + '%s_profile_vertical.pdf' % dict['name'] )
      
    return 



if __name__ == "__main__":

    main_profile(dict = scint_3mm, save = True)
    main_profile(dict = scint_05mm, save = True)
   
    plt.show()
