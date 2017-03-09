"""module to demonstrate the workflow"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def load_chi(lib_dir):
    """method to load chi files from lib_dir"""
    chi_fn_list = sorted([f for f in os.listdir(lib_dir) if\
                          f.endswith('.chi')])
    Iq_list = []
    Q_list = []
    for chi in chi_fn_list:
        fn = os.path.join(lib_dir, chi)
        try:
            array = np.loadtxt(fn).T # pyFAI
        except:
            array = np.loadtxt(fn, skiprows=4).T # fit2D
        Q, Iq = array
        Iq_list.append(Iq)
        Q_list.append(Q)
    # return one-to-one Q array for more flexibility
    Q_array = np.asarray(Q_list)
    Iq_array = np.asarray(Iq_list)
    print("INFO: load Q_array.shape = {}, Iq_array.shape = {}"
          .format(Q_array.shape, Iq_array.shape))

    return chi_fn_list, Q_array, Iq_array

# lookup table
_df = pd.read_csv('example/EO75A_soh_1_21_17_morning.txt')

exclude_col = ['#number', 'time', 'pe1_stats1_total',
               'diff_x_user_setpoint', 'diff_y_user_setpoint',
               'pe1_image']
colum_mask = [col for col in _df.columns if col not in exclude_col]
df = _df[colum_mask].copy()  # the main df to work on

# list of file name
lib_dir = 'example/fit2d_raster/'
chi_name_list, Q_array, Iq_array = load_chi(lib_dir)
df['basename'] = pd.Series(chi_name_list)

# load real background
_bkg = np.loadtxt('example/background_W151005_ct_300_13f4d2.chi',
                  skiprows=4).T
q, bkg_Iq = _bkg

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
