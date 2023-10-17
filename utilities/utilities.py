import numpy as np
import glob
import sys
import json
import pandas as pd
import os

def line(x, m, q): 
    return x*m+q

def exponential(x, n, m): 
  return n * np.e**(m*x)  

def log(x, n, m): 
  return n * np.log(m*x) 

def birk(x, a, b):
  return a * x / (a + b * x)

DTYPE_DICT = {'data_file' : '<U40', #data file name
              'dark_file' : '<U40', #data file name
              'monitor_units' : float, #accelerator units or diamond 
              'dose_irradiation' : float, 
              'time' : float, #if you need to save the time of the acquisition (for example for anealing purpose)
              'flag' : '<U40', 
              'shutter_close' : '<U40', #data file name
              'I_tube' : float, #accerator parameter
              'monitor_units_2' : float, #accelerator units or diamond 
              'mask' : int, 
              'position' : float, #posion of the array
              'PRF' : float, #pulse rate freq
              'IPDR' : float, 
              't_pulse': float,
              't_pulse_inv': float, 
              'lenght' : float, 
              'dose' : float,
              'cer_file' :'<U40' }

DATA_DICT = {'roiNumber' : int,
              'roiRadius' : float,
              'pixelNumber' : int,
              'SignalIntegral' : int,
              'SignalIntegralError' : int,
              'SignalMean' : float,
              'SignalMeanError' : float}

ROI_POS_DICT = {'roi_number' : float,
              'radius' : float,
              'y_position' : int, 
              'x_position' : int}


MAGNIFICATION_DICT = {'magnification' : float,
              'magnificationErr' : float, 
              'angle': float}


def parse_config_file(file_path, info_dictionary):
    """
    """
    with open(file_path, 'r') as input_file:
        header = input_file.readline()
        if not header.startswith('#'):
            raise UnicodeEncodeError('No header found in file %s' % file_path)
        names = header.strip('\n # ').split(' ')
        formats = [info_dictionary[name] for name in names]
        dtype = dict(names=names, formats=formats)
    return np.loadtxt(file_path, dtype=dtype, unpack=False)


def search_file_in_directory(directory_path, file_name):
    file_list = glob.glob(directory_path+'/%s' %file_name)
    if len(file_list)==1: 
        return file_list[0]
    elif len(file_list)==0:
        raise FileNotFoundError('No similar file -%s- found in directory %s' % (file_name, directory_path))
    else: 
        raise FileNotFoundError('Too many similar file -%s- found in directory %s' % (file_name, directory_path))



def decimal_places(val):
    """Calculate the number of decimal places so that a given value is rounded
    to exactly two signficant digits.
    Note that we add epsilon to the argument of the logarithm in such a way
    that, e.g., 0.001 is converted to 0.0010 and not 0.00100. For values greater
    than 99 this number is negative.
    """
    return 1 - int(np.log10(val + sys.float_info.epsilon)) + 1 * (val < 1.)


def decimal_power(val):
    """Calculate the order of magnitude of a given value,i.e., the largest
    power of ten smaller than the value.
    """
    return int(np.log10(val + sys.float_info.epsilon)) - 1 * (val < 1.)


def format_value(value, precision=3):
    """Format a number with a reasonable precision
    """
    if isinstance(value, str):
        return value
    else:
        fmt = '%%.%dg' % precision
        return fmt % value


def format_value_error(value, error, pm='+/-', max_dec_places=6):
    """Format a measurement with the proper number of significant digits.
    """
    value = float(value)
    error = float(error)
    if not np.isnan(error):
        assert error >= 0
    else:
        return '%s %s nan' % (format_value(value), pm)
    if error == 0 or error == NotImplementedError.inf:
        return '%e' % value
    dec_places = decimal_places(error)
    if dec_places >= 0 and dec_places <= max_dec_places:
        fmt = '%%.%df %s %%.%df' % (dec_places, pm, dec_places)
    else:
        p = decimal_power(abs(value))
        scale = 10 ** p
        value /= scale
        error /= scale
        dec_places = decimal_places(error)
        if dec_places > 0:
            if p > 0:
                exp = 'e+%02d' % p
            else:
                exp = 'e-%02d' % abs(p)
            fmt = '%%.%df%s %s %%.%df%s' %\
                  (dec_places, exp, pm, dec_places, exp)
        else:
            fmt = '%%d %s %%d' % pm
    return fmt % (value, error)

def make_opt_string(opt, pcov, s = '', s_f = ''):
    """ Make a string starting from an array (opt) and a matrix (pcov)
    """
    np.set_printoptions(linewidth = np.inf, precision = 5)
    opt_err = np.sqrt(pcov.diagonal())
    array_str = np.array_str(np.concatenate((opt, opt_err)) )
    array_str = array_str.strip('[]')
    string = s + ' ' + array_str + s_f + '\n'
    return string



#metti default senza variable. Puoi anche leggere solo i segnali..
def read_roi_data_from_file(directoryPath, header_data_file, header_variable_file=None, dataTypeToRead='dSub'): 
    roi = []
    radius = []
    signal = []
    signalErr = []

    if header_variable_file is not None: 
        variable = []
        for inputFile, v in zip(header_data_file, header_variable_file):
            f = search_file_in_directory(directoryPath+'outputFiles',  "%s*%s" %(dataTypeToRead, inputFile.replace('TIF', 'txt')))
            data = parse_config_file(f, DATA_DICT)
                
            roi.append(data['roiNumber'])
            radius.append(data['roiRadius'])
            signal.append(data['SignalIntegral'])
            signalErr.append(data['SignalIntegralError'])
            variable.append(np.ones(len(data['roiNumber']))*v)

        roi = np.concatenate(roi)
        radius = np.concatenate(radius)
        signal = np.concatenate(signal)
        signalErr = np.concatenate(signalErr)
        variable = np.concatenate(variable)

        return np.array([roi, radius, signal, signalErr]), variable
    else: 
        for inputFile in header_data_file:
            f = search_file_in_directory(directoryPath+'outputFiles',  "dSub*%s" %inputFile.replace('TIF', 'txt'))
            data = parse_config_file(f, DATA_DICT)
                    
            roi.append(data['roiNumber'])
            radius.append(data['roiRadius'])
            signal.append(data['SignalIntegral'])
            signalErr.append(data['SignalIntegralError'])

            roi = np.concatenate(roi)
            radius = np.concatenate(radius)
            signal = np.concatenate(signal)
            signalErr = np.concatenate(signalErr)
            return np.array([roi, radius, signal, signalErr])


def readFiberPos_atBeam(arrayPositionsFile):
  with open(arrayPositionsFile) as f:
      data = f.read()
  array_with_pos = json.loads(data)
  array_with_pos = pd.DataFrame(data=array_with_pos)
  return array_with_pos


def createOutputDirectory(path, dirName): 

    if os.path.exists(os.path.dirname( path+dirName)): 
        return path+dirName
    else: 
        os.mkdir(os.path.dirname(path+dirName))
        return path+dirName
