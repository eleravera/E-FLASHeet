from scipy.special import erf
import numpy as np

def err_func_plus_constant(x, norm, mean, sigma, constant):
    z = (x - mean)/sigma
    return norm * 0.5 * (1 + erf(z/np.sqrt(2)))+ np.ones(len(x))*constant

def err_func(x, norm, mean, sigma):
    z = (x - mean)/sigma
    return norm * 0.5 * (1 + erf(z/np.sqrt(2)))


def double_err_func(x, norm1, mean1, sigma1, norm2, mean2, sigma2, constant):
    z1 = (x - mean1)/sigma1
    z2 = (x - mean2)/sigma2
    err_funct_1 = norm1 * 0.5 * (1 + erf(z1/np.sqrt(2)))
    err_funct_2 = (1 - norm2) * 0.5 * (1 + erf(z2/np.sqrt(2)))
    #return err_funct_1 + err_funct_2 + np.ones(len(x)) * constant
    return err_func(x, norm1, mean1, sigma1) + err_func_plus_constant(x, norm2, mean2, sigma2, constant)

def exponential(x, norm, att): 
    return norm*np.exp(-x*att)

def err_func_exp(x, mu, sigma, norm , att):
    y = norm * np.exp(-x*att) *  err_func(x, 1., mu, sigma)
    return y 

def line(x, m, q):
    return x*m +q


def gauss(x, mu, sigma, norm, const=0): 
    return  norm* np.exp(-0.5*((x-mu)/sigma)**2) + np.ones(len(x)) * const 



def double_gauss(x, mu1, mu2, sigma1, sigma2, norm1, norm2, const1=0, const2=0): 
    return gauss(x, mu1, sigma1, norm1, const1) + gauss(x, mu2, sigma2, norm2, const1)