"""module to provide helper functions needed for mapPDF"""
import os
import scipy
import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy.stats import pearsonr
# import seaborn.apionly as sns

from diffpy.pdfgetx.pdfgetter import PDFGetter
from diffpy.pdfgetx.pdfconfig import PDFConfig


def process_chi_df(df, compositions, pdf_parameters,
                   background=None, iq_pearson_data=None,
                   gr_pearson_data=None):
    if iq_pearson_data is not None:
        df['iq_pearson'] = [pearsonr(i, iq_pearson_data)[0] for i in df['iq']]
    pdfgetter = PDFGetter()
    if background is not None:
        df['corrected_iq'] = df['iq'] - background
        df['gr'] = [pdfgetter(q, iq, composition=comp, **pdf_parameters)[1]
                    for q, iq, comp in zip(df['q'], df['corrected_iq'], compositions)]
    else:
        df['gr'] = [pdfgetter(q, iq, composition=comp, **pdf_parameters)[1]
                    for q, iq, comp in
                    zip(df['q'], df['iq'], compositions)]
    if gr_pearson_data is not None:
        df['gr_pearson'] = [pearsonr(i, gr_pearson_data)[0] for i in
                            df['gr']]


def mappdf_load_chi(csv_file, qoi_columns=None, root=''):
    raw_df = pd.read_csv(csv_file)
    if qoi_columns:
        df = raw_df[qoi_columns].copy()
    else:
        df = raw_df.copy()
    qs = []
    iqs = []
    for fn in df['filename']:
        fn = os.path.join(root, fn)
        try:
            q, iq = np.loadtxt(fn).T
        # TODO: limit scope
        except:
            q, iq = np.loadtxt(fn, skiprows=4).T
        qs.append(q)
        iqs.append(iq)
    df['q'] = qs
    df['iq'] = iqs
    return df


def load_chi(lib_dir):
    """method to load chi files from lib_dir"""
    chi_fn_list = sorted([f for f in os.listdir(lib_dir) if \
                          f.endswith('.chi')])
    Iq_list = []
    Q_list = []
    for chi in chi_fn_list:
        fn = os.path.join(lib_dir, chi)
        try:
            array = np.loadtxt(fn).T  # pyFAI
        except:
            array = np.loadtxt(fn, skiprows=4).T  # fit2D
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
        config_dict.update({'composition': compo})
        pdfconfig.update(**config_dict)
        pdfgetter = PDFGetter(pdfconfig)
        r, Gr = pdfgetter(x=q_grid, y=Iq)
        Gr_list.append(Gr)
    Gr_array = np.asarray(Gr_list)
    print("INFO: finish transform. output Gr shape is {}"
        .format(Gr_array.shape))

    return r, Gr_array


def conf_label_size(ax, label_size):
    ax.xaxis.label.set_size(label_size)
    ax.yaxis.label.set_size(label_size)


def conf_tick_size(ax, tick_size):
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(tick_size)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(tick_size)


# def bSeabornStyle(ticks=False, cycle='simon', context='notebook', f_scale=1,
#                   a_scale=1,
#                   l_width=1, m_size=1, xt_col='black'):
#     sns.reset_orig()
#     if ticks == False:
#         sns.set_style("whitegrid")
#     else:
#         sns.set_style("ticks")
#
#     sns.set_style({
#         'grid.linestyle': '--',
#         'grid.color': 'b2b2b2',
#         'axes.linewidth': (a_scale * 1.75),
#         'axes.labelcolor': 'black',
#         'axes.edgecolor': 'black',
#         'xtick.color': xt_col,
#         'ytick.color': 'black',
#         'xtick.direction': 'in',
#         'ytick.direction': 'in',
#     })
#
#     sns.set_context(context, font_scale=(f_scale * 1.5),
#                     rc={"lines.linewidth": (l_width * 2),
#                         "lines.markersize": (m_size * 5), })
#     mpl.rcParams['font.family'] = 'Arial'
#     mpl.rcParams['mathtext.fontset'] = 'stixsans'
#     mpl.rcParams['font.size'] = 18
#     mpl.rcParams['figure.dpi'] = 150
#     mpl.rcParams['figure.figsize'] = 9, 6
#     mpl.rcParams['grid.linewidth'] = 0.5
#     mpl.rcParams['savefig.bbox'] = 'tight'
#
#     if cycle == 'simon':
#         simonCycle = ["#0B3C5D", "#062F4F", "#328CC1", "#D9B310", "#984B43",
#                       "#B82601",
#                       "#57652A", "#76323F", "#626E60", "#AB987A", "#C09F80",
#                       "#b0b0b0ff"]
#         sns.set_palette(simonCycle)
#     elif cycle == 'simon2':
#         simonCycle2 = ["#0B3C5D", "#B82601", "#1c6b0a", "#328CC1", "#062F4F",
#                        "#D9B310", "#984B43",
#                        "#76323F", "#626E60", "#AB987A", "#C09F80", "#b0b0b0ff"]
#         sns.set_palette(simonCycle2)
#     else:
#         # Use another SNS preset: deep, muted, bright, pastel, dark, colorblind
#         sns.set_palette(cycle)
