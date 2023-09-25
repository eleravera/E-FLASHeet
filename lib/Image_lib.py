import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as PIL_Image
import os

import utilities.plot_size

class Image: 
    def __init__(self, file):
        self.inputFile = file
        self.image = self.openImage() 
        self.ROI_list = []

    #Deve essere eseguita sempre, per estrarre l'immagine
    def openImage(self):
        im = PIL_Image.open(self.inputFile)
        return np.array(im, dtype= np.int64)
    
    def plotImage(self, bounds=(None, None)):
        if bounds==(None, None):
            vmin, vmax = np.quantile(self.image, [0.02, 0.98])
        else: 
            vmin=bounds[0]
            vmax=bounds[1]
        fig, ax = plt.subplots(1,1, figsize=(8,8))
        im = ax.imshow(self.image, vmin=vmin, vmax=vmax)
        fig.colorbar(im)
        return fig

    def histImage(self, bounds=(None, None)):
        if bounds==(None, None):
            vmin, vmax = np.quantile(self.image, [0.02, 0.98])
        else: 
            vmin=bounds[0] 
            vmax=bounds[1]
        fig, ax = plt.subplots(1,1, figsize=(8,8))
        bins = np.linspace(int(vmin)-0.5, int(vmax)-0.5, min(int(vmax)-int(vmin)+1, 100))
        ax.hist(np.concatenate(self.image), bins = bins )
        return fig

    def createOutputFile(self, type, path=None):
        if path == None: 
            return self.inputFile.replace("TIF", type)
        elif os.path.exists(os.path.dirname(path)): 
            return path+(os.path.basename(os.path.abspath(self.inputFile))).replace("TIF", type)
        else: 
            os.mkdir(os.path.dirname(path))
            return path+(os.path.basename(os.path.abspath(self.inputFile))).replace("TIF", type)
   
    def savePlot(self, outputFilePdf, fig, title = ''):
        outputFilePdf.savefig(fig)
        fig.suptitle(title)
        return 

    def saveSomeInfo(self, outputFilePdf, someInfo):
        firstPage = plt.figure(figsize=(11.69, 8.27))
        firstPage.clf()
        firstPage.text(0.1,0.1, someInfo, size=22)
        outputFilePdf.savefig()
        return 


    def plotBeamProfile(self, calFactors=[], dl = 15.): #dl = 15 mm è la distanza tra gli scintillatori
        fig, ax = plt.subplots(1,1, figsize=(8,8))
        x = []
        y = []
        dy = []        

        ax.set_xlabel('dx beam [mm]')
        ax.set_ylabel('mean signal')
        if len(calFactors) < 1:
            calFactors = np.ones(len(self.ROI_list))
            ax.set_title('Beam profile')

        else: 
            ax.set_title('Calibrated beam profile')

        for i, r in zip(range(len(self.ROI_list)), self.ROI_list):
            x.append(i * dl)
            y.append(r.signalMean / calFactors[i])
            dy.append(r.signalStdev / calFactors[i])

        ax.errorbar(x, y, yerr = dy, fmt ='.')
        return fig 

    #Da testare
    def calculateCalibrationFactors(self):
        signal = [] 
        for r in self.ROI_list:
            signal.append(r.signalIntegral) 
        calFactors = np.array(signal)/max(signal)
        calFactorsErr = np.zeros(len(calFactors))
        return calFactors, calFactorsErr

    def saveCalibrationFactors(self, outputFile):
        calFactors, calFactorsErr = self.calculateCalibrationFactors()
        data = np.array([np.arange(1, len( self.ROI_list)+1 ), calFactors, calFactorsErr])
        np.savetxt(outputFile, np.transpose(data), fmt="%d %.3f", header="fibra   cal factor")
        return calFactors, calFactorsErr
    
    def readCalibrationFactors(self, calibrationFile):
        f, calFactors, calFactorsErr = np.loadtxt(calibrationFile, unpack=True) 
        return f, calFactors, calFactorsErr
