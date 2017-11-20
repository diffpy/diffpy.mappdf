"""module to provide helper functions needed for mapPDF"""
import os
import numpy as np
import pandas as pd
import scipy


def load_chi(lib_dir):
    """method to load chi files from lib_dir"""
    chi_fn_list = [f for f in os.listdir(lib_dir) if f.endswith('.chi')]
    chi_array = []
    Q_array = []
    for chi in chi_fn_list:
        fn = os.path.join(lib_dir, chi)
        try:
            array = np.loadtxt(fn).T # pyFAI
        except:
            array = np.loadtxt(fn, skiprows=4).T # fit2D
        Q, Iq = array
        chi_array.append(Iq)
        Q_array.append(Q)
    chi_array = np.asarray(chi_array)
    Q_array = np.asarray(Q_array)
    # just to reproduce, dont have to save q for each of them
    print("INFO: load {} by {} array"
          .format(Q_array.shape, chi_array.shape))
    return chi_fn_list, Q_array, chi_array

def magic():
    pass
