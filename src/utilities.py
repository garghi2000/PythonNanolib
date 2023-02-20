import numpy as np

def peak_detection(array, window, new_point_weight, threshold):
    """
    Peak detection algoritm inspired by: Brakel, J.P.G. van (2014).
    "Robust peak detection algorithm using z-scores". Stack Overflow.
    https://stackoverflow.com/questions/22583391/peak-signal-detection-in-
    realtime-timeseries-data/22640362#22640362 (version: 2020-11-08)

    INPUT ---------------------------------------------------------------
    array --> numerical numpy 1D-array of size n
    window --> constant integer: # of points to take for the moving average
    new_point_weight --> weight given to the new points for updating the
    moving average
    threshold --> threshold in std units for considering the new point out
    of the moving mean and therefore being marked as peak

    OUTPUT ---------------------------------------------------------------
    peak_indexes --> integer 1D-array of size n. Notice the first i-th elements
    with i < window are 0.
    """
    # rename some variable with shorter names
    np_weight = new_point_weight
    window = int(window)

    # parameters initialization
    avg_w_array = 0.
    std_w_array = 0.
    new_point = 0.
    avg_w_array = np.mean(array[0:window])
    std_w_array = np.std(array[0:window])
    peak_indexes = np.zeros_like(array)

    # loop over all new points classifing them as peaks(pos or neg) or no-peak
    for i in range(window, len(array)):
        first_point = array[i-window]
        new_point = array[i]
        if abs(new_point - avg_w_array) <= threshold*std_w_array:
            # no peak
            peak_indexes[i] = 0
        else:
            if new_point > avg_w_array:
                # pos peak
                peak_indexes[i] = 1
            else:
                # neg peak
                peak_indexes[i] = -1

        # updating new average(optimized) and std for nex peak detection
        if np_weight != 0 and i < (len(array) - 1):
            update_avg = (
                avg_w_array - first_point/window
                + new_point*np_weight/window)
            update_std = np.std(array[(i+1-window):(i+1)])
            avg_w_array = update_avg
            std_w_array = update_std
    return peak_indexes
