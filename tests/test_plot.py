from Pynanolib import load, plot
import os
import pytest


@pytest.fixture
def Nanonis_obj():
    cwd = os.getcwd()
    cwd = cwd[::-1].split('\\', 1)[-1]
    cwd = cwd[::-1]
    ffname = cwd + '\\ExampleFiles\\' + 'Bias-Spectroscopy.dat'
    return load.Nanonisfile(ffname)


def test_input_1_handle_correct(Nanonis_obj):
    assert isinstance(Nanonis_obj, load.Nanonisfile)


def test_input_1_handle_none():
    with pytest.raises(Exception) as e_info:
        Nanonis_obj = None
        plot.plot(Nanonis_obj)


def test_input_2_handle(Nanonis_obj):
    with pytest.raises(Exception) as e_info:
        plot.plot(Nanonis_obj, xChn=True)


def test_input_3_handle(Nanonis_obj):
    with pytest.raises(Exception) as e_info:
        plot.plot(Nanonis_obj, yChns=None)


def test_input_4_handle(Nanonis_obj):
    with pytest.raises(Exception) as e_info:
        plot.plot(Nanonis_obj, keepAxes="randomtext")


def test_input_5_handle(Nanonis_obj):
    with pytest.raises(Exception) as e_info:
        plot.plot(Nanonis_obj, figsize=("randomtext", 2))


def test_plot2D():
    pass


def test_plot():
    pass