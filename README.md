# Map PDF protocol demo

mapPDF is a set of software scripts for automating the collection of large numbers of x-ray datasets in a high-throughput experiment. Please see the Readme below for how to use it.

This demo is intended to show the capability and general workflow of the mapPDF protocol as described in [insert link to paper]. It is intended as a quick start soution for a novel python user who doesnt want to create a similar solution from scratch.

## Introduction:

MapPDF protocol was developed as a responce to increasing data quantity during modern total scattering experiments. The main idea is to address the problem of disjointed analysis workflows where different aspects of data reduction and modelling end up in various locations and formats.

This protocol attempts to simplify the process of handling large sets of experimental files and create one "collection" of information from which further analysis would be possible. The collection contains all of the metadata about the experiment, the data and the analysis results.
The demo provides an example of a typical workflow, shows how to create and provides a few suggestions on how to use the "collection".

The current implementation is aimed at users of the XPD beamline at NSLSII but can be readily extended to other sources by the user through it's transparent structure and use of easily available python packages.

### Overall workflow:

1. Set up the paths to metadata and images / data files.
2. Load the data into a "collection" dataframe including that information.
3. Transform data to PDF
4. Use pearsonr to screen the dataset.
5. Apply a fit recipe and save refined parameters
6. Visualize refined parameters.
7. Adjust/improve model

It was designed to work with output files from the XPD beamline at NSLSII.
Output from other instruments can be used given the general metadata format is the same, or if the user is willing to adjust the import script. Once set up, the protocol is intended to work with minimal adjustments between the experiments.

### Requirements:

For this to run you will need:

Python3 (f.x. Anaconda Python) with following packages: 
numpy, pandas, matplotlib, scipy

You would also need PDFGetX. The guidelines on how to obtain it can be found on diffpy.org

The custom functions used for diffpy.mappdf are found in 'mappdf_utils.py' which is downloaded together with the demo.

### Installation:

Make sure you have all the required packages installed into your python environment and have downloaded the demo folder containing 'mappdf_utils.py' together with the data files required for the demo located in 'example_data' folder.

### Use instructions:

Follow the workflow in the demo example and make necessary changes to suit your problem.
