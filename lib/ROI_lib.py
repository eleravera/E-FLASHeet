import numpy as np
from matplotlib import pyplot as plt

import utilities.plot_size

DEFAULT_ROI_RADIUS = 10

class Roi:

    def __init__(self, image, number=1, center=(0,0), radius= DEFAULT_ROI_RADIUS):
        self.number = number
        self.roiCenter = center
        self.roiRadius = radius
        self.squaredImage = self.makeSquaredROI(image)
        self.circularROI = self.makeCiruclarROI(image)
        self.signalIntegral = self.signalIntegral()
        self.signalIntegralError = self.signalIntegralError()
        self.signalMean = self.signalMean()
        self.signalStdev = self.signalStdev()
        self.signalMeanError = self.signalMeanError()


    def __str__(self):
        return "\tROI number %.1f:\n\tCenter: (%d,%d), radius: %d" % (self.number, self.roiCenter[0], self.roiCenter[1], self.roiRadius )

    ###Questa funzione essere lanciata sempre! Mi serve per creare una nuova variabile da quelle che ho già ho. Le due funzioni sotto servono per trovare questa nuova variabile; forse defineCircularROI e applyCircularROI possono essere definire come private?
    def makeCiruclarROI(self, image): 
        x, y = np.ogrid [:len(image[0]) , :len(image[1])]
        d = np.sqrt ((x-self.roiCenter[0])**2 + (y-self.roiCenter[1])**2)
        circularROI = d<self.roiRadius 
        return image[circularROI]

    #Stessa roba qui : setSquaredROI eseguita sempre, mentre defineSquaredROI e applySquaredROI possono essere private?
    def makeSquaredROI(self, image): 
        xrange = (self.roiCenter[0]-self.roiRadius,  self.roiCenter[0]+self.roiRadius)
        yrange = (self.roiCenter[1]-self.roiRadius,  self.roiCenter[1]+self.roiRadius)
        squaredROI = image[xrange[0]:xrange[1], yrange[0]:yrange[1]]
        return squaredROI

    def plotImage(self, bounds=(None, None)):
        #formatta asse x e y in modo che chi siano le roi giuste.
        if bounds==(None, None):
            vmin, vmax = np.nanquantile(self.squaredImage, [0.02, 0.98])
        else: 
            vmin, vmax = bounds[0], bounds[1]
        fig, ax = plt.subplots(1,1, figsize=(8, 8))
        shw1 = ax.imshow(self.squaredImage, vmin=vmin, vmax=vmax)    
        cbar = plt.colorbar(shw1)
        cbar.ax.tick_params(labelsize=14)  
        cbar.set_label('', labelpad=-40, y=1.05, rotation=0, size = 14)
        ax.set_xlabel('col')
        ax.set_ylabel('row')
        plt.title("ROI %.1f" % self.number)
        return fig


    def histImage(self, bins=None):
        if bins is None: 
            bins = np.linspace(self.squaredImage.min(), self.squaredImage.max(), 100)
        fig, ax = plt.subplots(1,1, figsize=(8,8))
        ax.hist(np.concatenate(self.squaredImage), bins=bins, alpha=0.4) 
        ax.set_yscale('log')
        ax.set_xlabel("Gray level")
        ax.set_ylabel("Counts")
        plt.title("ROI %.1f" %self.number)
        return fig

    #invece qui voglio l'immagine con ROI tonda
    def checkSaturation(self, satLimitCCD=2**16-1):
        args=np.argwhere(self.circularROI>=satLimitCCD)
        if len(args)!=0:
            print("CCD saturate in %d pixels; the max value recorded is %d" % (len(args), self.circularROI.max() ))
        return
    
    def signalIntegral(self): 
        return np.sum(self.circularROI)

    def signalIntegralError(self): 
        return np.sqrt(np.sum(self.circularROI[self.circularROI>1]))

    def signalMean(self): 
        return np.mean(self.circularROI)

    def signalStdev(self): 
        return np.std(self.circularROI)

    def signalMeanError(self): 
        return self.signalStdev/np.sqrt(self.circularROI.size)

    def ROIanalysis(self): 
        #print(self) #if logging == DEBUG scrivi. 
        self.checkSaturation()
        return np.array([self.signalIntegral, self.signalMean, self.signalMeanError])

    def ROIplots(self, bounds = (None, None), bins = None):
        fig1 = self.plotImage(bounds=bounds)
        fig2 = self.histImage(bins=bins)
        return fig1, fig2

    def saveInfo(self, outputFilePdf=None, outputFileTxt=None):
        if outputFilePdf is not None:
            infoROI="ROI number %.1f:\n\nCenter: (%d,%d), radius: %d\n\n N of pixels: %d" % (self.number, self.roiCenter[0], self.roiCenter[1], self.roiRadius, self.circularROI.size )
            div = "\n\n-------------------------\n\n"
            infoSignal="Signal informations:\n\n  -Integral: %d\n\n  -IntegralErr: %d\n\n  -Mean: %.2f\n\n  -MeanStdev): %.2f" %( self.signalIntegral, self.signalIntegralError, self.signalMean, self.signalMeanError)
            page = plt.figure(figsize=(11.69, 8.27))
            page.clf()
            page.text(0.2, 0.2, infoROI+div+infoSignal, size=24)
            outputFilePdf.savefig()
        if outputFileTxt is not None:
            #potresti controllare se è vuoto, e in caso pulirlo
            data = np.array([self.number, self.roiRadius, len(self.circularROI), self.signalIntegral, self.signalIntegralError, self.signalMean, self.signalStdev])
            np.savetxt(outputFileTxt, data.reshape(1, -1), fmt = "%.1f", delimiter='\t\t')
        return 

    def savePlot(self, outputFilePdf, fig):
        outputFilePdf.savefig(fig)
        fig.clf()
        plt.close('all')
        return 


