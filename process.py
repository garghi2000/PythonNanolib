from Pynanolib import load
import numpy as np
import math


def _normalization(data, dataRef):
    return (data -  data.min())/(data.max() - data.min())


def _standardization(data, dataRef):
    return (data - data.mean())/(data.std())


def _multiplycation(data, dataRef):
    return data * dataRef


def _division(data, dataRef):
    return data / dataRef


def _differentiation(data, dataRef):
    data = np.diff(data)
    # the last array element is repeated to avoid the discreate 
    # differentiation having a different number of points
    return np.append(data, data[-1])


def _sum(data, dataRef):
    return data + dataRef


def _merge(data, dataRef):
    return data


def _average(data, dataRef):
    return (data + dataRef)/2


processAllowed = {
                    "Min-MaxNormalization": _normalization,
                    "Standardization": _standardization,
                    "Differentiation": _differentiation,
                    "Multiplycation": _multiplycation,
                    "Division": _division,
                    "Sum": _sum,
                    "Merge": _merge,
                    "Average": _average}


expTypesAllowed = [
                    "CLAMPoints-dat", 
                    "bias spectroscopy", 
                    "History Data", 
                    "Sweep",
                    "Oscilloscope",
                    "Z spectroscopy",
                    "Longterm",
                    "Spectrum",
                    "STM",
                    "SFEM"]


def _handle_input_1(Nanonisfile):
    if not isinstance(Nanonisfile, load.Nanonisfile):
        raise Exception(
            f"The first input {Nanonisfile} is not a Nanonisfile Object"
            " of Pynanolib.load module. Please first load your data using"
            " the load module and pass the Nanonisfile object as first input")
    return Nanonisfile


def _handle_input_2(processType):
    if not(processType in processAllowed.keys()):
        raise Exception('The processType must be one of the following: '
                        f'{processAllowed.keys()}')
    return processType


def _handle_input_3(data, chnsToProc):
    allchns = list(data.keys())
    if chnsToProc is True or chnsToProc is False:
        raise Exception(
            'The parameter chnsToProc must be a list of column names,'
            'a list of idexes, or a string == all')
    if chnsToProc == 'all' :
        chnsToProc = allchns
    elif chnsToProc in allchns:
        chnsToProc = [chnsToProc]
    elif set(chnsToProc).issubset(allchns):
        chnsToProc = chnsToProc
    elif set(chnsToProc).issubset(range(len(allchns))):
        chnsToProc = [allchns[i] for i in chnsToProc]
    else:
        raise Exception(
            'The parameter chnsToProc must be a list of column names,'
            'a list of integers, or a string == all')
    return chnsToProc


def _handle_input_4(data, ref):
    if ref is True or ref is False:
        raise Exception(
            'The parameter ref must be None or string present in '
            'the list of the recorded channels names or a number')
    if ref is None:
        dataRef = None
    elif ref in list(data.keys()):
        dataRef = data[ref]
    elif ref.isnumeric():
        dataRef = ref
    else:
        raise Exception(
            'The parameter ref must be None or string present in '
            'the list of the recorded channels names or a number')
    return dataRef


def _process_data(dataToProcess, processType, dataRef):
    """
    This function calls the process function corresponding to the processType.
    """
    return processAllowed[processType](dataToProcess, dataRef)

def processSingleFile(
        NanonisFile, processType = 'Division', chnsToProc = 'all', ref = None
        ):
    """
    This function processes data of one or more channels from a single 
    NanonisFile object.
    
    The process can be a stand alone process such as differenciation or scaling
    or it can be with respect to a reference channel or number(ref).
    
    The resulting processed data is added on a new channel of the NanonisFile 
    object.
    
    INPUT
    ---------------------------------------------------------------------------
    NanonisFile : (NanonisFile object of class NanonisFile) ->  
    the attribute 'data' of such a class is a dict containing the channel 
    names as keys and data as values.
    
    processType: (str) -> corresponds to the name of the process to apply
    
    chnsToProc : (str) ->  can be 'all' or a channel name
                 (list) -> can be list of channel names or channel indexes
    ref : (str) -> can be the name of a channel
          (number) -> can be a number
    """
    data = _handle_input_1(NanonisFile).data
    processType = _handle_input_2(processType)
    chnsToProc = _handle_input_3(data, chnsToProc)
    dataRef = _handle_input_4(data, ref)

    # each channel is processed by procesType with/without respect to ref
    for chn in chnsToProc:
        dataToProcess = data[chn]
        dataProcessed = _process_data(dataToProcess, processType, dataRef)
        if processType in [
                "Min-MaxNormalization", "Standardization", "Differentiation"
                ]:
            newDataName = chn + ' processed with: ' + processType + ' method'
        else:
            newDataName = chn + ' ' + processType + ' by ' + ref
        NanonisFile.data.update({newDataName: dataProcessed})

def processMultiFiles():
    pass
