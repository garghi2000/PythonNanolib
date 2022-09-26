# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 11:25:02 2022

@author: Gabriele Bertolini
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def _plot1Ddata(Nanonisfile, Chn2plot, KeepAxes):
    if Chn2plot == 'all':
        df = pd.DataFrame(Nanonisfile.data)
    else :
        df = pd.DataFrame(Nanonisfile.data)[Chn2plot]
        
    if KeepAxes == 'True':
        df.plot()
        plt.show()       
    else :
        naxs = len(df.columns)
        # nice way to distribute the subplots on a grid
        nrow = math.floor(math.sqrt(naxs)) 
        ncol = math.ceil(naxs/nrow)
        fig, axs = plt.subplots(nrow, ncol)
        fig.tight_layout(pad = 1)
        for chname in df.columns:
            axr = axs.ravel()
            axchname = axr[df.columns.get_loc(chname)]         
            axchname.set_ylabel(chname)
            df[chname].plot(ax = axchname, y = chname, figsize =(12, 5))    
        for ax in axr[naxs:]: ax.axis('off')
        plt.show()
        #I mihgt think of a way to plot a channel vs an other channel
        
############ It needed to perform a plot of y vs x chosen channels ######
def _plot2Ddata(Nanonisfile, Chn2plot, KeepAxes):
    pass

def nsfile(Nanonisfile, Chn2plot = 'all', KeepAxes = 'False') :
    
    if Nanonisfile.metadata['File extension'] == '.dat': 
        _plot1Ddata(Nanonisfile, Chn2plot, KeepAxes)
        
    elif Nanonisfile.metadata['File extension'] == '.sxm':
        _plot2Ddata(Nanonisfile, Chn2plot, KeepAxes)
    
#     data_header = Nanonisfile.header
#     if Nanonisfile.metadata['File extension'] == '.dat'
#         try :
#             exp_type = data_header['Experiment']
#         except :
#             print('No Experiment type detected. Such information is not in the' 
#                  'header.')
#             exp_type = 'generic dat file'
#     elif Nanonisfile.metadata['File extension'] == '.sxm' :
#         if Nanonisfile. :
#             exp_type = data_header
#         elif
   
#     return exp_type



# def plot_data_from_file(Nanonisfile):
#     pass

# def alldata(Nanonisfile):
#     pass

# def channels(Nanonisfile):
#     pass


# Xlabel = "Energy (eV)"
# Ylabel = "Counter 2 (cps)"
# Ylabelnorm = "Counts/Current (cps/A)"
# Xdata = myfile.data[Xlabel]
# Ydata = myfile.data[Ylabel]
# Ydatanorm = Ydata/np.abs(myfile.data['Tip Current (A)'])

# fig, ax = plt.subplots()
# ax.plot(Xdata, Ydata, '.-b', label='row')
# ax.set_xlabel(Xlabel)
# ax.set_ylabel(Ylabel)

# ax2 = ax.twinx()
# ax2.plot(Xdata, Ydatanorm, '.-r', label='norm by current')
# ax2.set_ylabel(Ylabelnorm)

# plt.title(myfile.metadata["File name"])

# ax.legend(loc=0)
# ax2.legend(loc=1)

# plt.show()

   
    

