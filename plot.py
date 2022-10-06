# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 11:25:02 2022

@author: Gabriele Bertolini
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def _plot1Ddata(Nanonisfile, xChn, yChns, keepAxes):
    #conversion to pandas dataframe
    df = pd.DataFrame(Nanonisfile.data)
    
    #check on xChn input
    if xChn != None :
        if xChn in df.columns:
            X = xChn
        elif xChn in range(len(df.columns)):
            X = df.columns[xChn]
        else :
            raise Exception('The parameter xChn must be either None, a string present in '
                        'the list of the recorded channels names, or an index')
    else :
        X = None
        
    #check on yChns input
    if yChns == 'all' :
        Y = df.columns
    elif set(yChns).issubset(df.columns):
        Y = yChns
    elif set(yChns).issubset(range(len(df.columns))):
        Y = df.columns[yChns]
    else :
        raise Exception('The parameter yChns must be a list of column names,'
                        'a list of idexes, or a string == all')
    
    #check on keepAxes input
    if keepAxes == 'True' or keepAxes == True :
        df.plot(x = X, y = Y)
        plt.show()       
    elif keepAxes == 'False' or keepAxes == False :
        nAxes = len(Y)
        # nice way to distribute the subplots on a grid as square as possible
        nRow = math.floor(math.sqrt(nAxes)) 
        nCol = math.ceil(nAxes/nRow)
        fig, axes = plt.subplots(nRow, nCol)
        fig.tight_layout(pad = 1)
        axr = axes.ravel()
        i = 0
        for chName in Y:
            yAxChName = axr[i]         
            yAxChName.set_ylabel(chName)
            i += 1 
            if X == None or chName == X:
                df[chName].plot(xlabel = 'Index', ax = yAxChName, y = chName,
                                figsize =(9, 6))
            else:
                df.plot(ax = yAxChName, x = X, y = chName, figsize =(9, 6))

        for ax in axr[nAxes:]:
            ax.axis('off')
        plt.show()
    else :
        raise Exception('The parameter keepAxes must be a boolean')
            
############ It needed to perform a plot of y vs x chosen channels ######
def _plot2Ddata(Nanonisfile, yChns):
    pass

def plot(Nanonisfile, xChn = None, yChns = 'all', keepAxes = False) :
    
    if Nanonisfile.metadata['File extension'] == '.dat': 
        _plot1Ddata(Nanonisfile, xChn, yChns, keepAxes)
        
    elif Nanonisfile.metadata['File extension'] == '.sxm':
        _plot2Ddata(Nanonisfile, yChns, keepAxes)
    
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

   
    

