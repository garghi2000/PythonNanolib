from Pynanolib import load
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import math


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
        # adding a column of indexes to data dict if xChn is not given
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


def _handle_input_5(sfigsize):
    if type(sfigsize) != tuple or len(sfigsize) != 2:
        raise Exception(
            f"The input figsize = {sfigsize} is not a tuple of size 2")
    elif not all(type(i) != str for i in sfigsize):
        raise Exception(
            f"The input figsize = {sfigsize} must be a tuple of 2 numbers"
            ", not strings")
    return sfigsize


def _figure_all_in_one(data, xName, yNames, sfigsize):
    wfig, hfig = sfigsize
    fig, ax = plt.subplots(figsize=(wfig, hfig))
    for yName in yNames:
        ax.plot(data[xName], data[yName], label=yName)
        plt.legend(loc="upper left")
        plt.xlabel(xName)
    plt.show()
    return fig, ax


def _figures_in_a_grid(data, xName, yNames, sfigsize):
    colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
    wfig, hfig = sfigsize
    nAxes = len(yNames)
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
        ax.plot(data[xName], data[yName], colors[i % len(colors)])
        plt.ylabel(yName)
        plt.xlabel(xName)
    plt.show()
    return fig, grid, ax


def _plot1Ddata(nanonisfile, xChn, yChns, keepAxes, sfigsize):
    # the order of the _handle_input functions must occur after _handle_input_3
    nanonisfile = _handle_input_1(nanonisfile)
    data = nanonisfile.data
    yNames = _handle_input_3(data, yChns)
    xName = _handle_input_2(data, xChn)
    keepAxes = _handle_input_4(keepAxes)
    sfigsize = _handle_input_5(sfigsize)

    # check on keepAxes input
    if keepAxes:
        fig, ax = _figure_all_in_one(data, xName, yNames, sfigsize)
    else:
        fig, grid, ax = _figures_in_a_grid(data, xName, yNames, sfigsize)

    # removing extra columns of indexes added before if it exists
    if '#Index' in data.keys():
        del data['#Index']

    return fig


# It needed to perform a plot of y vs x chosen channels #
def _plot2Ddata(Nanonisfile, yChns):
    pass


def plotSingleFile(
        Nanonisfile, xChn=None, yChns='all',
        keepAxes=False, sfigsize=(3.2, 2)
        ):
    """
    Plot file structured in Nanonisfile class.

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
            Nanonisfile, xChn, yChns, keepAxes, sfigsize)

    return fig


def plotMultiFiles():
    pass
