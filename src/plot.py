#from Pynanolib import load
import load
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import math
from warnings import warn


def _handle_input_1(Nanonisfile):
    if not isinstance(Nanonisfile, load.Nanonisfile):
        raise Exception(
            f"The first input {Nanonisfile} is not a Nanonisfile Object"
            " of Pynanolib.load module. Please first load your data using"
            " the load module and pass the Nanonisfile object as first input")
    return Nanonisfile


def _handle_input_2(data, xChn):
    if xChn is True or xChn is False:
        raise Exception(
            f'The parameter xChn = {xChn} must be either None,'
            ' a string present in '
            'the list of the recorded channels names, or an integer')
    if xChn is None:
        # adding a column of indexes to data dict if xChn input misses
        xName = '#Index'
        data['#Index'] = np.arange(len(data[list(data.keys())[0]]))
    elif xChn in data.keys():
        xName = xChn
    elif xChn in range(len(data.keys())):
        xName = list(data.keys())[xChn]
    else:
        raise Exception(
            f'The parameter xChn = {xChn} must be either None,'
            ' a string present in '
            'the list of the recorded channels names, or an integer')
    return xName


def _handle_input_3(data, yChns):
    allchns = list(data.keys())
    if yChns is True or yChns is False:
        raise Exception(
            'The parameter yChns must be a list of column names,'
            'a list of idexes, or a string == all')
    if yChns == 'all':
        yNames = allchns
    elif yChns in allchns:
        yNames = [yChns]
    elif set(yChns).issubset(allchns):
        yNames = yChns
    elif set(yChns).issubset(range(len(allchns))):
        yNames = [allchns[i] for i in yChns]
    else:
        raise Exception(
            'The parameter yChns must be a list of column names,'
            'a list of idexes, or a string == all')
    return yNames


def _handle_input_4(keepAxes):
    if keepAxes not in ['True', 'False', True, False]:
        raise Exception('The parameter keepAxes must be a boolean')
    if keepAxes == 'True':
        keepAxes = True
    if keepAxes == 'False':
        keepAxes = False
    return keepAxes

def _handle_input_5(keepFigure):
    if keepFigure not in ['True', 'False', True, False]:
        raise Exception('The parameter keepFigure must be a boolean')
    if keepFigure == 'True':
        keepFigure = True
    if keepFigure == 'False':
        keepFigure = False
    return keepFigure


def _handle_input_6(sfigsize):
    if type(sfigsize) != tuple or len(sfigsize) != 2:
        raise Exception(
            f"The input figsize = {sfigsize} is not a tuple of size 2")
    elif not all(type(i) != str for i in sfigsize):
        raise Exception(
            f"The input figsize = {sfigsize} must be a tuple of 2 numbers"
            ", not strings")
    return sfigsize

def check_inputs(Nanonisfile, xChn, yChns, keepAxes, keepFigure, sfigsize):
    Nanonisfile = _handle_input_1(Nanonisfile)
    data = Nanonisfile.data
    yNames = _handle_input_3(data, yChns)
    xName = _handle_input_2(data, xChn)
    keepAxes = _handle_input_4(keepAxes)
    keepFigure = _handle_input_5(keepFigure)
    sfigsize = _handle_input_6(sfigsize)
    return xName, yNames, keepAxes, keepFigure


def _plot_all_figures_standalone(data, xName, yNames, sfigsize):
    colors = ["b", "g", "r", "c", "m", "y", "k"]
    wfig, hfig = sfigsize
    figs = []
    axs = []
    for i, yName in enumerate(yNames):
        f = plt.figure()
        figs.append(f)
        ax = plt.plot(
            data[xName], data[yName], colors[i % len(colors)], label=yName)
        axs.append(ax)
        plt.legend(loc="upper left")
        plt.xlabel(xName)
    plt.show()
    return figs, axs


def _plot_figure_all_in_one(data, xName, yNames, sfigsize):
    wfig, hfig = sfigsize
    fig, ax = plt.subplots(figsize=(wfig, hfig))
    for yName in yNames:
        ax.plot(data[xName], data[yName], label=yName)
        plt.legend(loc="upper left")
        plt.xlabel(xName)
    plt.show()
    return fig, ax


def _plot_figures_in_a_grid(data, xName, yNames, sfigsize):
    colors = ["b", "g", "r", "c", "m", "y", "k"]
    wfig, hfig = sfigsize
    nAxes = len(yNames)
    # Organizing multiplots such that the figure is as square as possible
    nRow = math.floor(math.sqrt(nAxes))
    nCol = math.ceil(nAxes/nRow)
    # Vector of 2D indexes of the grid in order to use a single loop later
    gridIdxs = [[i, j] for i in range(nRow) for j in range(nCol)]
    wr = [wfig]*nCol
    hr = [hfig]*nRow
    fig = plt.figure(constrained_layout=False, figsize=(sum(wr), sum(hr)))
    grid = gridspec.GridSpec(
        nRow, nCol, width_ratios=wr, height_ratios=hr, figure=fig
        )
    for i, yName in enumerate(yNames):
        idx1, idx2 = gridIdxs[i]
        ax = plt.subplot(grid[idx1, idx2])
        ax.plot(data[xName], data[yName], colors[i % len(colors)])
        plt.ylabel(yName)
        plt.xlabel(xName)
    plt.show()
    return fig, grid, ax


def _plot_figure_along_multi_files(
        Nanonisfiles, xName, yNames, keepFigure, sfigsize):

    colors = ["b", "g", "r", "c", "m", "y", "k"]
    wfig, hfig = sfigsize
    nAxes = len(yNames)

    if keepFigure:
        # Organizing multiplots such that the figure is as square as possible
        nRow = math.floor(math.sqrt(nAxes))
        nCol = math.ceil(nAxes/nRow)
        # Vector of 2D indexes of the grid in order to use a single loop later
        gridIdxs = [[i, j] for i in range(nRow) for j in range(nCol)]
        wr = [wfig]*nCol
        hr = [hfig]*nRow
        fig = plt.figure(constrained_layout=True, figsize=(sum(wr), sum(hr)))
        grid = gridspec.GridSpec(
            nRow, nCol, width_ratios=wr, height_ratios=hr, figure=fig
            )
        for i, yName in enumerate(yNames):
            idx1, idx2 = gridIdxs[i]
            ax = plt.subplot(grid[idx1, idx2])
            for j, Nanonisfile in enumerate(Nanonisfiles):
                filename = Nanonisfile.metadata["File name"]
                data = Nanonisfile.data
                ax.plot(data[xName], data[yName],
                        colors[j % len(colors)], label=filename)
            plt.legend(loc="upper left")
            plt.ylabel(yName)
            plt.xlabel(xName)
        plt.show()
        figs = fig

    else:
        wfig, hfig = sfigsize
        figs = []
        axs = []
        for yName in yNames:
            f = plt.figure()
            figs.append(f)
            for j, Nanonisfile in enumerate(Nanonisfiles):
                filename = Nanonisfile.metadata["File name"]
                data = Nanonisfile.data
                ax = plt.plot(data[xName], data[yName],
                              colors[j % len(colors)], label=filename)
                axs.append(ax)
            plt.legend(loc="upper left")
            plt.xlabel(xName)
            plt.ylabel(yName)
        plt.show()
        return figs


def _plot1Ddata(Nanonisfile, xChn, yChns, keepAxes, keepFigure, sfigsize):
    # the order of the _handle_input functions must occur after _handle_input_3
    xName, yNames, keepAxes, keepFigure = check_inputs(
            Nanonisfile, xChn, yChns, keepAxes, keepFigure, sfigsize)
    data = Nanonisfile.data
    

    # plot accordingly with keepFigure amd keepAxes
    if keepFigure:
        if keepAxes:
            fig, ax = _plot_figure_all_in_one(data, xName, yNames, sfigsize)
        else:
            fig, grid, ax = _plot_figures_in_a_grid(data, xName, yNames, sfigsize)
    else:
        if keepAxes:
            warn("If the keepFigure variable is False, each selected data will"
                 " be plotted in a standalone figure,"
                 " therefore keepAxes variable will lose its meaning"
                 " and will not be considered."
                 )
        # notice that in this case fig is a list of figures
        fig, ax = _plot_all_figures_standalone(data, xName, yNames, sfigsize)
    
    # removing extra columns of indexes added in case of missing XChn input
    if '#Index' in data.keys():
        del data['#Index']
        
    if type(fig) == list:
        for fig in fig:
            fig.canvas.set_window_title(f'{Nanonisfile.metadata["File name"]}')
    else:
        fig.canvas.set_window_title(f'{Nanonisfile.metadata["File name"]}')
    return fig


def _plot1Ddata_along_multi_files(Nanonisfiles, xChn, yChns,
                                  keepAxes, keepFigure, sfigsize):

    # Check the nanonisfiles contain the channels the user has used as input 
    for Nanonisfile in Nanonisfiles:
        xName, yNames, keepAxes, keepFigure = check_inputs(
                Nanonisfile, xChn, yChns, keepAxes, keepFigure, sfigsize)
        
    keepAxes = _handle_input_4(keepAxes)
    keepFigure = _handle_input_5(keepFigure)
    sfigsize = _handle_input_6(sfigsize)
    
    if keepAxes:
        figs = _plot_figure_along_multi_files(
            Nanonisfiles, xName, yNames, keepFigure, sfigsize)
    else:
        figs = [plotSingleFile(
            Nanonisfile, xName, yNames, keepAxes,keepFigure, sfigsize)
            for Nanonisfile in Nanonisfiles]  
    return figs

# It needed to perform a plot of y vs x chosen channels #
def _plot2Ddata(Nanonisfile, yChns):
    pass


def plotSingleFile(
        Nanonisfile, xChn=None, yChns='all',
        keepAxes=False, keepFigure=False, sfigsize=(3.2, 2)
        ):
    """
    Plot a single file structured in Nanonisfile class.

    Inputs
    -------
        Nanonisfile --> Nanonisfile object (see Pynanonislib.load module).
        xChn (str or index) --> single channel taken as X-axis.
        yChns (list of channels, of integers,
               or single str = 'all', or to a channel name) --> single  or
                                        multiple channels to plot in Y-axis.
        keepAxes(boolean or str='False' or 'True') --> option for plotting
                                                all graphs in a set of axes.
    Returns
    -------
    fig --> figure object (see matlibplot.figure module).

    """
    plot_case = {".dat": _plot1Ddata, ".sxm": _plot2Ddata}
    key = Nanonisfile.metadata['File extension']
    fig = plot_case[key](
            Nanonisfile, xChn, yChns, keepAxes, keepFigure, sfigsize)

    return fig


def plotMultiFiles(
        Nanonisfiles, xChn=None, yChns='all',
        keepAxes=False, keepFigure=False, sfigsize=(3.2, 2)
        ):
    """
    Plot multiple files structured in Nanonisfile class.

    Inputs
    -------
        Nanonisfiles --> list of Nanonisfile objects (see Pynanonislib.load
                                                      module).
        xChn (str or index) --> single channel taken as X-axis.
        yChns (list of channels, of integers,
               or single str = 'all', or to a channel name) --> single  or
                                        multiple channels to plot in Y-axis.
        keepAxes(boolean or str='False' or 'True') --> option for plotting
                                                all graphs in a set of axes.
    Returns
    -------
    figs --> list of figure objects (see matlibplot.figure module).

    """
    f_ext = []
    for Nanonisfile in Nanonisfiles:
        f_ext.append(_handle_input_1(Nanonisfile).metadata['File extension'])

    if f_ext.count(".dat") == len(f_ext):
        key = ".dat"
    elif f_ext.count(".sxm") == len(f_ext):
        key = ".sxm"
    else:
        raise Exception(
            'The Nanonisfiles loaded do not have the same extension,'
            'therefore they cannot be plot all togheter. Please use a for loop'
            'and plot them using the plotSingleFile module')

    plot_case = {".dat": _plot1Ddata_along_multi_files, ".sxm": _plot2Ddata}
    figs = plot_case[key](
            Nanonisfiles, xChn, yChns, keepAxes, keepFigure, sfigsize)

    return figs
