# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 11:25:02 2022

@author: Gabriele Bertolini
"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import math

def _plot1Ddata(Nanonisfile, xChn, yChns, keepAxes):
    data = Nanonisfile.data
    # some variable for the Width/hight ratio of the plots    
    unitHeight, goldenRatio = 2, 1.6
    #extra check for the case xChn is None
    if '#Index' in data.keys():
        raise Exception(
            'The data contains a channel name #Index,'
            ' this channel might be erased after plot')
    #check yChns input and convert it in a list of channels name to plot
    if yChns == 'all' :
        yNames = list(data.keys())
    elif yChns in data.keys():
        yNames = [yChns]
    elif set(yChns).issubset(data.keys()):
        yNames = yChns
    elif set(yChns).issubset(range(len(data.keys()))):
        yNames = [data.keys()[i] for i in yChns]
    else :
        raise Exception(
            'The parameter yChns must be a list of column names,'
            'a list of idexes, or a string == all')
        
    #check on xChn input
    if xChn == None :
        # adding a column of indexes to data dict if xChn is not given
       xName = '#Index'
       data['#Index'] = np.arange(len(data[list(data.keys())[0]]))
    elif xChn in data.keys():
        xName = xChn
    elif xChn in range(len(data.keys())):
        xName = list(data.keys())[xChn]
    else :
        raise Exception(
            'The parameter xChn must be either None, a string present in '
            'the list of the recorded channels names, or an integer')
       
    #check on keepAxes input
    if keepAxes == 'True' or keepAxes == True :
        fig, ax = plt.subplots(figsize=(unitHeight*goldenRatio, unitHeight))
        for yName in yNames:
            ax.plot(data[xName],data[yName], label = yName)
            plt.legend(loc="upper left")
            plt.xlabel(xName)
        plt.show()
        
    elif keepAxes == 'False' or keepAxes == False :
        nAxes = len(yNames)
        #Organizing multiplots such that the figure is as square as possible
        nRow = math.floor(math.sqrt(nAxes)) 
        nCol = math.ceil(nAxes/nRow)
        #Vector of 2D indexes of the grid in order to use a single loop later
        gridIdxs = [[i,j] for i in range(nRow) for j in range(nCol)]
        wr = [unitHeight*goldenRatio]*nCol
        hr = [unitHeight]*nRow
        fig = plt.figure(constrained_layout=True, figsize=(sum(wr),sum(hr)))
        grid = gridspec.GridSpec(
            nRow, nCol, width_ratios= wr, height_ratios= hr, figure = fig
            )
        for i, yName in enumerate(yNames):
            idx1, idx2 = gridIdxs[i]
            ax = plt.subplot(grid[idx1, idx2])
            ax.plot(data[xName], data[yName])
            plt.ylabel(yName)
            plt.xlabel(xName)
        plt.show()
    else :
        raise Exception('The parameter keepAxes must be a boolean')
    # removing extra columns of indexes added before if it exists
    if '#Index' in data.keys():
        del data['#Index']
        
############ It needed to perform a plot of y vs x chosen channels ######
def _plot2Ddata(Nanonisfile, yChns):
    pass

def plot(Nanonisfile, xChn = None, yChns = 'all', keepAxes = False) :

    if Nanonisfile.metadata['File extension'] == '.dat': 
        _plot1Ddata(Nanonisfile, xChn, yChns, keepAxes)
        
    elif Nanonisfile.metadata['File extension'] == '.sxm':
        _plot2Ddata(Nanonisfile, yChns, keepAxes)
    