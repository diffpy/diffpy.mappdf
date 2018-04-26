#mapPDF overview

mapPDF is a set of software scripts for automating the collection of large numbers of x-ray datasets in a high-throughput experiment.

## Getting started

We assume that you have collected/are about to collect some diffraction for PDF analysis from a high throughut experiment such as from a synchrotron experiment.

By downloading and running mapPDF scripts you can organize and visualize your large dataset.
You can download the zip file by clicking on the green button or clone the git repository.
When you've extracted the distibution navigate to the demo folder.
It contains two files: mappdf_utils.py and mapPDF_demo.ipynb jupyter notebook.
You will work with mapPDF_demo.ipynb and should not change the mappdf_utils.py file, though a copy of this file should be present in the directory as the demo notebook.

Start by opening the mapPDF_demo.ipynb.
To do this you need to have Jupyter Notebook installed and working, which you can get at http://jupyter.org/install
The mapPDF notebook is using Python 3.

To run the demo type `jupyter notebook` on the command line then navigate to the folder where the mapPDF_demo.ipynb file is and click on it.

Then follow the instructions in the notebook.

This demo is intended to show the capability and general workflow of the mapPDF protocol as described in [insert link to paper]. It is intended as a quick start soution for a novel python user who doesnt want to create a similar solution from scratch.

For questions and help with mapPDF post questions at https://groups.google.com/forum/#!forum/diffpy-users

## Introduction:

MapPDF protocol was developed as a responce to increasing data quantity during modern total scattering experiments. The main idea is to address the problem of disjointed analysis workflows where different aspects of data reduction and modelling end up in various locations and formats.

This protocol attempts to simplify the process of handling large sets of experimental files and create one "collection" of information from which further analysis would be possible. The collection contains all of the metadata about the experiment, the data and the analysis results.
The demo provides an example of a typical workflow, shows how to create and provides a few suggestions on how to use the "collection".

The current implementation is aimed at users of the XPD beamline at NSLSII but can be readily extended to other sources by the user through it's transparent structure and use of easily available python packages.

## Requirements:
For this to run you will need:

Python3 (e.g., Anaconda Python) with following packages: numpy, pandas, matplotlib, scipy

You would also need the pdfGetX3 package installed (http://www.diffpy.org/products/pdfgetx3.html).


