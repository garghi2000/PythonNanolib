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
    return np.add(data, data[-1])

def _sum(data, dataRef):
    return data + dataRef

def _merge(data, dataRef):
    return data

def _average(data, dataRef):
    return (data + dataRef)/2

processAllowed = {
    "Min-MaxNormalization":_normalization,
    "Standardization":_standardization,
    "Differentiation":_differentiation,
    "Multiplycation":_multiplycation,
    "Division":_division,
    "Sum":_sum,
    "Merge":_merge,
    "Average":_average}

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
    data = NanonisFile.data
    allchns = list(data.keys())
    
    #check the input processType
    if not(processType in processAllowed.keys()):
        raise Exception('The processType must be one of the following: '
                        'Normalization, Scaling, Moltiplying, Sum, Differentiation, Merge.')
    
    #check the input chnsToProc
    if chnsToProc == 'all' :
        chnsToProc = allchns
    elif chnsToProc in allchns:
        chnsToProc = [chnsToProc]
    elif set(chnsToProc).issubset(allchns):
        chnsToProc = chnsToProc
    elif set(chnsToProc).issubset(range(len(allchns))):
        chnsToProc = [allchns[i] for i in chnsToProc]
    else :
        raise Exception('The parameter yChns must be a list of column names,'
                        'a list of integers, or a string == all')
    
    #check the input ref
    if ref == None:
        dataRef = None
    elif ref in allchns:
        dataRef = data[ref]
    elif ref.isnumeric():
        dataRef = ref           
    else:
        raise Exception('The parameter ref must be None or string present in '
                    'the list of the recorded channels names or a number')
    
    #each channel to process is processed by procesType with respect to the ref
    for chn in chnsToProc:
        dataToProcess = data[chn]
        dataProcessed = _process_data(dataToProcess, processType, dataRef)
        if processType in ["Min-MaxNormalization","Standardization"]:
            newDataName = chn + 'scaled by: ' + processType + ' method'
        else:
            newDataName = chn + ' ' + processType + ' by ' + ref
        
        NanonisFile.data.update({newDataName: dataProcessed})

def processMultiFiles(processType = 'Division', chnsToProc = 'all', ref = None):
    pass        