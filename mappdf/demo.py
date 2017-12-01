"""module to demonstrate the workflow"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

#FIXME correct import later
from utils import *

#### mappdf working example ####

# load lookup table
_df =pd.read_csv('map_PDF_example_data/meta/20161115-220716_grid_scan_md.txt')

# optional; to exclude function
qoi_colmns  = ['#number', 'time', 'diff_x', 'diff_y']
df = _df[qoi_colmns].copy()  # the main df to work on

# list of file name
# TODO: turn this into h5py. array + metadata
chi_dir = 'map_PDF_example_data/chi/'
chi_name_list, Q_array, Iq_array = load_chi(chi_dir)
df['chi_file_name'] = pd.Series(chi_name_list)


# load real background
#TODO: check with Anton
#bkg_q, bkg_Iq =np.loadtxt('example/background_W151005_ct_300_13f4d2.chi',
#        skiprows=4).T
bkg_q, bkg_Iq = np.loadtxt('map_PDF_example_data/background/PCA_background.txt').T


# subtract background
sub_Iq = bkg_subtraction(Q_array, Iq_array, bkg_q, bkg_Iq)


# transform Gr
composition_info = ['CPtCu']*len(df)   # dummy for test
qmin, qmax, qmaxinst, rmin, rmax,\
        rstep, rpoly = (0.1, 25., 25, 0., 100., 0.01, 0.90)

config_dict = dict(dataformat='Qnm', mode='xray', qmaxinst=qmaxinst,
                   qmin=qmin, qmax=qmax, rmax=rmax, rmin=rmin,
                   rstep=rstep, rpoly=rpoly)

r, Gr_array = Gr_transform(Q_array[0], Iq_array,
                           composition_info, config_dict)

# pearson map
pearson_map1 = np.apply_along_axis(pearsonr, 1, Iq_array, Iq_array[0])
pearson_map2 = np.apply_along_axis(pearsonr, 1, Iq_array, bkg_Iq)

# create scatter plot with pearson map
fig, ax = plt.subplots(1,2, figsize=(15,9), sharey=True)
fig.suptitle('Pearson Map')
cax = fig.add_axes((0.93,0.1,0.03,0.8))
im = ax[0].scatter(df['diff_x'], df['diff_y'], c=pearson_map1[:,0])
ax[1].scatter(df['diff_x'], df['diff_y'], c=pearson_map2[:,0])
fig.colorbar(im, cax=cax)

ax[0].set_title('wrt corner mearsurement')
ax[1].set_title('wrt underlying background')
for el in ax:
    el.set_xlabel('diff_x readback value')
    el.set_ylabel('diff_y readback value')
plt.set_cmap('inferno')
plt.show()
