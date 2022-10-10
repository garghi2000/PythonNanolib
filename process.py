import numpy as np
import pandas as pd
import math

def _normalization(data, dataRef):
    return data
def _scaling(data, dataRef):
    return data
def _multiplycation(data, dataRef):
    dataProcessed = data * dataRef
    return dataProcessed
def _division(data, dataRef):
    dataProcessed = data / dataRef
    return dataProcessed
def _differentiation(data, dataRef):
    return data
def _sum(data, dataRef):
    dataProcessed = data + dataRef
    return dataProcessed
def _merge(data, dataRef):
    return data

processAllowed = {"Normalization":_normalization,
                  "Scaling":_scaling,
                  "Differentiation":_differentiation,
                  "Multiplycation":_multiplycation,
                  "Division":_division,
                  "Sum":_sum,
                  "Merge":_merge}

expTypesAllowed = ["CLAMPoints-dat", 
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
    process_data = processAllowed[processType](dataToProcess, dataRef)
    return process_data

def process(NanonisFile, processType = 'Division', chnsToProc = 'all', ref = None):
    data = NanonisFile.data
    allchns = list(data.keys())
    
    #check the input processType
    if not(processType in processAllowed.keys()):
        raise Exception('The processType must be one of the following: '
                        'Normalization, Scaling, Moltiplying, Sum, Differentiation, Merge.')
    
    #check the input chnsToProc
    if chnsToProc == 'all' :
        chnsToProc = allchns
    elif set(chnsToProc).issubset(allchns):
        chnsToProc = chnsToProc
    elif set(chnsToProc).issubset(range(len(allchns))):
        chnsToProc = [allchns[i] for i in chnsToProc]
    else :
        raise Exception('The parameter yChns must be a list of column names,'
                        'a list of integers, or a string == all')
    
    #check the input ref
    if ref != None:
        if ref in allchns:
            dataRef = data[ref]
        elif ref in range(len(allchns)):
            ref = allchns[ref]
            dataRef = data[ref]
        else :
            raise Exception('The parameter ref must be None or string present in '
                        'the list of the recorded channels names')
    else:
        dataRef = ref
    
    #each channel to process is processed by procesType with respect to the ref
    for chn in chnsToProc:
        dataToProcess = data[chn]
        dataProcessed = _process_data(dataToProcess, processType, dataRef)
        newDataName = chn + ' ' + processType + ' by ' + ref
        NanonisFile.data.update({newDataName: dataProcessed})
    return NanonisFile