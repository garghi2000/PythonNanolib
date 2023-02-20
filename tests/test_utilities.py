import numpy as np
from peak_detection_scan import peak_detection
import pytest
# inputs = (array, window, new_point_weight, threshold)
def ex_1():
    "Example n1 of inputs parameters and expected result"
    example_1 = np.array([1, 0, -1, 6, 1.9, 0, -5])
    window, new_point_weight, threshold = 3, 0, 3.0
    mean, std = 0, 2/3 #of the first 3(window) elements of array
    inputs = (example_1, window, new_point_weight, threshold)
    exp_result = np.array([0, 0, 0, 1, 0, 0, -1])
    return inputs, exp_result

def ex_2():
    "Example n2 of inputs parameters and expected result"
    example_2 = np.array([0, 0, 0, 0, 4, 0, 1.5])
    window, new_point_weight, threshold = 4, 1, 1.0
    mean, std = ([0, 1, 1, ],[0, 1.73, 1.73])
    inputs = (example_2, window, new_point_weight, threshold)
    exp_result = np.array([0, 0, 0, 0, 1, 0, 0])
    return inputs, exp_result

def ex_3():
    "Example n3 of inputs parameters and expected result"
    example_3 = np.zeros(6)
    window, new_point_weight, threshold = 3, 0, 3.0
    inputs = (example_3, window, new_point_weight, threshold)
    exp_result = np.array([0, 0, 0, 0, 0, 0])
    return inputs, exp_result

def ex_4():
    "Example n4 of inputs parameters and expected result"
    example_4 = np.array([1, 0, -1, 1, 6, 6, 0, 1.9, 0, -5])
    window, new_point_weight, threshold = 3, 0, 3.0
    inputs = (example_4, window, new_point_weight, threshold)
    exp_result = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, -1])
    return inputs, exp_result

@pytest.mark.parametrize("inputs, expected_result",
                         [ex_1(), ex_2(), ex_3(), ex_4()])
def test_peak_detection_scan(inputs, expected_result):
    result = peak_detection(*inputs)
    assert np.array_equal(expected_result, result)
