import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare
from matplotlib.colors import LogNorm

import lib.utilities as utilities

def set_plot(xlabel, ylabel, title = '', grid =False, legend = False):
    """ Set the format of the plot
    """
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.yticks(fontsize=16, rotation=0)
    plt.xticks(fontsize=16, rotation=0)
    plt.subplots_adjust(bottom = 0.13, left = 0.15)
    if legend:
        plt.legend()
    if grid: 
        plt.grid()
    return

def fit_legend(param_values, param_errors, param_names, param_units, chi2 = None, ndof = None):
    """ Format (in a readable way) the fit parameters legend
    """
    legend = ''
    for (name, value, error, unit) in zip(param_names, param_values, param_errors, param_units):
        legend += ("%s: %s %s\n" % (name, utilities.format_value_error(value, error), unit))
    if chi2 is not None:
        legend += ("$\chi^2$/d.o.f.=%.2f/%d "% (chi2, ndof))
    return legend


def colormap(z, bounds = (None, None), xlabel = '', ylabel = '', zlabel='', title = '', norm=None):
    """ Create a colormap
    """
    fig, ax = plt.subplots(1,1, figsize=(8, 8))
    set_plot(xlabel = xlabel, ylabel = ylabel, title = title)
    if bounds==(None, None):
        vmin, vmax = numpy.nanquantile(z, [0.02, 0.98])
    else: 
        vmin, vmax = bounds[0], bounds[1]
    shw1 = ax.imshow(z, vmin=vmin, vmax=vmax, norm = norm )    
    cbar = plt.colorbar(shw1)
    cbar.ax.tick_params(labelsize=14)  
    cbar.set_label(zlabel, labelpad=-40, y=1.05, rotation=0, size = 14)
    return fig, ax

def colorbar_double_axis(x, f, zlabel1, zlabel2, title=''):
    """ Create a colormap with double axes
    """
    fig, ax = plt.subplots(1,1, figsize=(8, 8))
    vmin, vmax = numpy.nanquantile(x, [0.02, 0.98])
    shw1 = ax.imshow(x, vmin=vmin, vmax=vmax )
    shw2 = ax.imshow(x*f, vmin = vmin*f, vmax = vmax*f )    
    bar1 = plt.colorbar(shw1)
    bar2 = plt.colorbar(shw2)
    bar1.ax.tick_params(labelsize=14)  
    bar2.ax.tick_params(labelsize=14)  
    plt.gca().invert_yaxis()
    set_plot('col', 'row', title = '', grid = False)
    bar2.set_label(zlabel1, labelpad=-40, y=1.05, rotation=0, size = 14)
    bar1.set_label(zlabel2, labelpad=-40, y=1.05, rotation=0, size = 14)
    plt.title(title, fontsize=14)  
    return fig, ax