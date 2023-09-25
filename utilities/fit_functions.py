from scipy.special import erf
import numpy as np

def err_func(x, norm, mean, sigma):
    z = (x - mean)/sigma
    return norm * 0.5 * (1 + erf(z/np.sqrt(2)))

def exponential(x, norm, att): 
    return norm*np.exp(-x*att)

def err_func_exp(x, mu, sigma, norm , att):
    y = norm * np.exp(-x*att) *  err_func(x, 1., mu, sigma)
    return y 

def line(x, m, q):
    return x*m +q


def gauss(x, mu, sigma, norm): 
    return  norm* np.exp(-0.5*((x-mu)/sigma)**2) 

