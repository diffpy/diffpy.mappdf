"""module to provide class for performing analysis pipeline on 
spatial resolved PDF"""
import os
import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from .glbl import glbl
from .utils import *

class MapPDF:
    """class to provide pipeline of spatially resolved PDF"""
    def __init__(self, lib_dir):
        """
        Paramters
        ---------
        lib_dir : str
            path to chi files collected from experiment
        """
        self._lib_dir = lib_dir
        # expect attributes
        self.Gr_list = None
        self.Iq_list = None
        self.Rw_list = None
        self._data_df = None
        self._recipe = None

    @property
    def lib_dir(self):
        return self._lib_dir

    @lib_dir.setter
    def lib_dir(self, new_dir):
        self.flush()
        self._lib_dir = new_dir
        self.load_chi()

    def flush(self):
        """method to flush all the data attributes"""
        self.Gr_list = None
        self.Iq_list = None
        self.Rw_list = None
        self._data_df = None
        self._recipe = None

    @property
    def recipe(self):
        return self._recipe

    @recipe.setter
    def recipe(self, new_res):
        self.Rw_list = None
        self._recipe = new_res

    @property
    def data_df(self):
        return data_df

    def load_chi(self):
        """method to load chi files on lib_dir set to class"""
        pass

    def generate_dataDF(self):
        """method to generate a panda dataframe as lookup table,
        no data processing is involved"""
        pass

    def update_Gr(self):
        """method to calculate G(r) based on I(Q) curves from the 
        `data_df` set to the class"""
        pass

    def fit_recipe(self):
        """method to run refinement based on recipe set to class and
        update Rw column in the data fame"""
        pass
