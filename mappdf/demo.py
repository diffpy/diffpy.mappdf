"""module to demonstrate the workflow"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

from diffpy.pdfgetx.pdfgetter import PDFGetter
from diffpy.pdfgetx.pdfconfig import PDFConfig

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


def bkg_subtraction(target_qgrid, target_Iq, bkg_qgrid, bkg_Iq):
    """function to subtract background Iq from target Iq.

    Note: If target_Iq and background Iq are not in the same 
    Q_grid, background Iq will be interped onto Q_grid of target Iq

    Parameters
    ----------
    target_qgrid : ndarray
        qgrid of input target_Iq
    target_Iq : ndarray
        Iq that background will be subtracted from. It could
        be single Iq or mutiple Iq
    bkg_qgrid : ndarray
        qgrid of bkground Iq
    bkg_Iq : ndarray
        background Iq is going to be appplied
    """
    assert bkg_Iq.ndim == 1
    _bkg_Iq = np.interp(target_qgrid, bkg_qgrid, bkg_Iq)
    subtracted_Iq = np.subtract(target_Iq, _bkg_Iq)

    return subtracted_Iq


def Gr_transform(q_grid, Iq_array, composition_info, config_dict):
    """function to transform Iq to Gr

    Parameters
    ----------
    q_grid : ndarray
        grid of Iq array going to be transformed
    Iq_array : ndarray
        Iq array will be transformed
    composition_info : list
        list of strings to specify chemical composition
    config_dict :
        keyword arguments to specify parameters of Gr transformation
        such as qmin, qmax, qmaxinst, rmin, rmax, rstep, rpoly
    """
    # initiate pdfgetter
    pdfconfig = PDFConfig()

    # expand dimension
    if Iq_array.ndim == 1:
        _Iq_array = np.expand_dims(Iq_array)
    _Iq_array = Iq_array

    # assert to protect error
    assert q_grid.ndim == 1
    assert _Iq_array.shape[0] == len(composition_info)

    # iterate through pairs
    Gr_list = []
    for Iq, compo in zip(_Iq_array, composition_info):
        config_dict.update({'composition':compo})
        pdfconfig.update(**config_dict)
        pdfgetter = PDFGetter(pdfconfig)
        r, Gr = pdfgetter(x=q_grid, y=Iq)
        Gr_list.append(Gr)
    Gr_array = np.asarray(Gr_list)
    print("INFO: finish transform. output Gr shape is {}"
          .format(Gr_array.shape))

    return r, Gr_array

#### mapPDF working example ####


# load lookup table
_df = pd.read_csv('example/EO75A_soh_1_21_17_morning.txt')

# optional; to exclude function
qoi_colmns  = ['#number', 'time', 'diff_x', 'diff_y']
df = _df[qoi_colmns].copy()  # the main df to work on

# list of file name
lib_dir = 'example/fit2d_raster/'
chi_name_list, Q_array, Iq_array = load_chi(lib_dir)
df['chi_file_name'] = pd.Series(chi_name_list)
# TODO: turn this into h5py. array + metadata

# load real background
_bkg = np.loadtxt('example/background_W151005_ct_300_13f4d2.chi',
                  skiprows=4).T
bkg_q, bkg_Iq = _bkg


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
