from Pynanolib import process as prc
import numpy as np
# import pytest


def test_normalization():
    arg = np.array([2, 4, 6, 8, 10, 12])
    result = prc._normalization(arg, None)
    exp_result = np.array([0., 0.2, 0.4, 0.6, 0.8, 1.])
    assert np.array_equal(exp_result, result)

# def test_standardization():
#     pass 

# def test_multiplycation():
#     pass 

# def test_division():
#     pass

# def test_differentiation():
#     pass

# def test_sum():
#     pass 

# def test_merge():
#     pass

# def test_average():
#     pass
